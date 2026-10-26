"""Evaluator-side spectral shortcut baseline for blind acoustic research.

This is an *oracle-supervised* negative control: a trusted evaluator hands
opaque class IDs to a nearest-frequency lookup fit. The labels and learned
frequencies MUST NOT reach an untrained sender or receiver. A high score is
evidence of a recoverable codebook, not semantics, emergent communication, or
causal listening. No Num'ta'reen source/corpus is imported here.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from statistics import median
from typing import Mapping, Sequence

import numpy as np

from .blind_audio_observation import decode_audio_observation


CLAIM_CEILING = "SUPERVISED_SPECTRAL_LOOKUP_NEGATIVE_CONTROL_ONLY"


@dataclass(frozen=True)
class LabeledAcousticTrial:
    """Evaluator-private row; never serialize this object to a learner."""

    trial_id: str
    family_id: str
    payload: Mapping[str, object]
    opaque_class_id: int


@dataclass(frozen=True)
class PeakLookupScore:
    accuracy: float
    class_carriers_hz: tuple[tuple[int, float], ...]
    accuracy_by_class: tuple[tuple[int, float], ...]
    train_count: int
    holdout_count: int
    oracle_supervision_used: bool = True
    semantic_qualification: bool = False
    claim_ceiling: str = CLAIM_CEILING


def _spectral_peak_hz(payload: Mapping[str, object]) -> float:
    """Decode only the four-key waveform and find its dominant non-DC bin."""

    samples, sample_rate = decode_audio_observation(payload)
    if samples.shape[1] != 1 or samples.shape[0] < 64:
        raise ValueError("spectral peak needs at least 64 mono frames")
    centered = samples[:, 0] - np.mean(samples[:, 0])
    windowed = centered * np.hanning(centered.size)
    magnitudes = np.abs(np.fft.rfft(windowed))
    magnitudes[0] = 0.0
    index = int(np.argmax(magnitudes))
    if index == 0 or not np.isfinite(magnitudes[index]) or magnitudes[index] <= 0:
        raise ValueError("no measurable non-DC spectral peak")
    return float(np.fft.rfftfreq(centered.size, d=1.0 / sample_rate)[index])


def _validate_trials(
    train: Sequence[LabeledAcousticTrial],
    holdout: Sequence[LabeledAcousticTrial],
) -> None:
    if not train or not holdout:
        raise ValueError("nonempty train and holdout splits required")

    identities: set[str] = set()
    train_families: set[str] = set()
    holdout_families: set[str] = set()
    rates_and_shapes: set[tuple[int, tuple[int, int]]] = set()
    train_waveforms: set[tuple[int, tuple[int, int], str]] = set()
    holdout_waveforms: set[tuple[int, tuple[int, int], str]] = set()
    for split, rows in (("train", train), ("holdout", holdout)):
        for row in rows:
            if not isinstance(row, LabeledAcousticTrial):
                raise ValueError("each row must be an evaluator-private LabeledAcousticTrial")
            if not isinstance(row.trial_id, str) or not row.trial_id or row.trial_id in identities:
                raise ValueError("trial_id must be nonempty and unique")
            identities.add(row.trial_id)
            if not isinstance(row.family_id, str) or not row.family_id:
                raise ValueError("family_id must be a nonempty string")
            if type(row.opaque_class_id) is not int or row.opaque_class_id < 0:
                raise ValueError("opaque_class_id must be a nonnegative integer")
            # The exact public allowlist and dimensions are enforced by the
            # existing transport decoder before consulting any evaluator label.
            decode_audio_observation(row.payload)
            signature = (int(row.payload["sample_rate_hz"]), tuple(row.payload["shape"]))
            rates_and_shapes.add(signature)
            key = (*signature, str(row.payload["float64_le_b64"]))
            if split == "train":
                train_families.add(row.family_id)
                train_waveforms.add(key)
            else:
                holdout_families.add(row.family_id)
                holdout_waveforms.add(key)
    if train_families & holdout_families:
        raise ValueError("train and holdout family identifiers overlap")
    if train_waveforms & holdout_waveforms:
        raise ValueError("train/holdout exact waveform replay detected")
    if len(rates_and_shapes) != 1:
        raise ValueError("public sample-rate/shape metadata must be frozen across splits/classes")

    train_ids = {row.opaque_class_id for row in train}
    holdout_ids = {row.opaque_class_id for row in holdout}
    if len(train_ids) < 2 or holdout_ids != train_ids:
        raise ValueError("all classes must appear in both splits, with at least two classes")


def score_supervised_peak_lookup(
    train: Sequence[LabeledAcousticTrial],
    holdout: Sequence[LabeledAcousticTrial],
) -> PeakLookupScore:
    """Measure a memorized codebook shortcut using evaluator-provided labels.

    Call this on trusted evaluator rows only. It is deliberately NOT a zero-
    shared-language candidate: providing the opaque class IDs during fitting
    is oracle supervision. There is no process isolation or semantic claim.
    """

    training_rows, holdout_rows = tuple(train), tuple(holdout)
    _validate_trials(training_rows, holdout_rows)
    training_peaks: dict[int, list[float]] = defaultdict(list)
    for row in training_rows:
        training_peaks[row.opaque_class_id].append(_spectral_peak_hz(row.payload))
    carriers = tuple((label, float(median(peaks))) for label, peaks in sorted(training_peaks.items()))

    matched = 0
    right_by_class: dict[int, int] = defaultdict(int)
    count_by_class: dict[int, int] = defaultdict(int)
    for row in holdout_rows:
        peak = _spectral_peak_hz(row.payload)
        # Deterministic tie policy makes the shortcut's failure reproducible.
        prediction = min(carriers, key=lambda pair: (abs(pair[1] - peak), pair[0]))[0]
        hit = int(prediction == row.opaque_class_id)
        matched += hit
        right_by_class[row.opaque_class_id] += hit
        count_by_class[row.opaque_class_id] += 1
    return PeakLookupScore(
        accuracy=matched / len(holdout_rows),
        class_carriers_hz=carriers,
        accuracy_by_class=tuple(
            (label, right_by_class[label] / count_by_class[label]) for label, _ in carriers
        ),
        train_count=len(training_rows),
        holdout_count=len(holdout_rows),
    )
