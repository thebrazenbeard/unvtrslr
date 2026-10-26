"""Frozen supervised tone-ratio probe with waveform-only prediction.

The labels exist during training and evaluator scoring, never in the prediction
method's input. A correct result demonstrates an invariant acoustic feature in
synthetic signals, not semantic acquisition, unsupervised translation, or
independent sender/receiver communication.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from statistics import median
from typing import Mapping, Sequence

import numpy as np

from .blind_audio_observation import decode_audio_observation
from .empirical_signal_baselines import LabeledAcousticTrial, _validate_trials


CLAIM_CEILING = "ORACLE_SUPERVISED_RATIO_INVARIANCE_SYNTHETIC_ONLY"


def _tone_ratio(payload: Mapping[str, object]) -> float:
    samples, rate = decode_audio_observation(payload)
    if samples.shape[1] != 1 or samples.shape[0] < 256:
        raise ValueError("spectral ratio requires at least 256 mono frames")
    centered = samples[:, 0] - np.mean(samples[:, 0])
    spectrum = np.abs(np.fft.rfft(centered * np.hanning(centered.size)))
    spectrum[0] = 0.0
    # Local maxima suppress two-bin skirts around a strong single tone.
    maxima = np.nonzero(
        (spectrum[1:-1] > spectrum[:-2]) &
        (spectrum[1:-1] >= spectrum[2:])
    )[0] + 1
    if len(maxima) < 2:
        raise ValueError("spectral ratio requires two distinct measurable tones")
    strongest = sorted(maxima, key=lambda idx: (-spectrum[idx], idx))[:2]
    if min(spectrum[strongest]) < max(spectrum[strongest]) * 0.08:
        raise ValueError("spectral ratio requires two sufficiently strong tones")
    freqs = np.fft.rfftfreq(centered.size, 1 / rate)
    low, high = sorted(float(freqs[idx]) for idx in strongest)
    if low <= 0 or not np.isfinite(high):
        raise ValueError("spectral ratio has no valid pair")
    return high / low


@dataclass(frozen=True)
class FrozenRatioModel:
    class_ratios: tuple[tuple[int, float], ...]
    sample_rate_hz: int
    shape: tuple[int, int]
    provenance_sha256: str
    oracle_supervision_used: bool = True
    semantic_qualification: bool = False
    claim_ceiling: str = CLAIM_CEILING

    def predict(self, payload: Mapping[str, object]) -> int:
        # No opaque answer, trial ID, family ID or generator seed in this API.
        samples, rate = decode_audio_observation(payload)
        if rate != self.sample_rate_hz or tuple(samples.shape) != self.shape:
            raise ValueError("model public sample-rate/shape mismatch")
        observed = _tone_ratio(payload)
        return min(
            self.class_ratios,
            key=lambda item: (abs(item[1] - observed), item[0]),
        )[0]


@dataclass(frozen=True)
class RatioProbeScore:
    model: FrozenRatioModel
    accuracy: float
    accuracy_by_class: tuple[tuple[int, float], ...]
    train_count: int
    holdout_count: int
    oracle_supervision_used: bool = True
    semantic_qualification: bool = False
    claim_ceiling: str = CLAIM_CEILING


def fit_and_score_ratio_probe(
    train: Sequence[LabeledAcousticTrial],
    holdout: Sequence[LabeledAcousticTrial],
) -> RatioProbeScore:
    """Fit on supervised training rows, freeze, then predict on raw holdout.

    Label access during fitting is intentional. Scoring is evaluator-side.
    No semantic or autonomous-language claim follows from any accuracy.
    """
    train_rows, holdout_rows = tuple(train), tuple(holdout)
    _validate_trials(train_rows, holdout_rows)

    grouped: dict[int, list[float]] = defaultdict(list)
    proof = hashlib.sha256(b"unvtrslr/train-only-ratio-learner/v1\n")
    for row in sorted(train_rows, key=lambda row: row.trial_id):
        grouped[row.opaque_class_id].append(_tone_ratio(row.payload))
        # A provenance commitment to the complete labeled training examples;
        # no private labels or fingerprints enter prediction arguments.
        canonical_row = {
            "trial_id": row.trial_id,
            "family_id": row.family_id,
            "opaque_class_id": row.opaque_class_id,
            "payload": dict(row.payload),
        }
        proof.update(json.dumps(canonical_row, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        proof.update(b"\n")

    model = FrozenRatioModel(
        class_ratios=tuple((label, float(median(values))) for label, values in sorted(grouped.items())),
        sample_rate_hz=int(train_rows[0].payload["sample_rate_hz"]),
        shape=tuple(train_rows[0].payload["shape"]),
        provenance_sha256=proof.hexdigest(),
    )
    hits: dict[int, int] = defaultdict(int)
    counts: dict[int, int] = defaultdict(int)
    for row in holdout_rows:
        counts[row.opaque_class_id] += 1
        hits[row.opaque_class_id] += int(model.predict(row.payload) == row.opaque_class_id)

    return RatioProbeScore(
        model=model,
        accuracy=sum(hits.values()) / len(holdout_rows),
        accuracy_by_class=tuple((label, hits[label] / counts[label]) for label, _ in model.class_ratios),
        train_count=len(train_rows),
        holdout_count=len(holdout_rows),
    )
