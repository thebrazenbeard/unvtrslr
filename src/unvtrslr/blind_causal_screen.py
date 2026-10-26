"""Evaluator-private acoustic channel controls, NOT semantic qualification.

The caller supplies both sides as in-process Python callbacks. This API can
detect some obvious no-message and shuffle shortcuts, but cannot prove actor
isolation, frozen neural state, independent observations, or true learning.
See docs/R2_THREE_HOST_CAUSAL_ACQUISITION_GATE.md for the missing host gate.
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from hashlib import sha256
import json
import secrets
from typing import Callable, Mapping, Sequence

import numpy as np


_AUDIO_SCHEMA = "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1"
_PUBLIC_AUDIO_KEYS = frozenset({
    "schema", "sample_rate_hz", "shape", "float64_le_b64",
})
_MAX_SAMPLES = 262_144
_MAX_CHANNELS = 64
_MAX_SAMPLE_RATE = 2**31 - 1
_MAX_MESSAGE_BYTES = 256
_CLAIM_CEILING = "IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED"


@dataclass(frozen=True)
class PrivateTrial:
    """Evaluator-only source and target; never pass this object to learners."""

    trial_id: str
    group_id: str
    observation_payload: Mapping[str, object]
    correct_action: int


@dataclass(frozen=True)
class _SealedTrial:
    trial_id: str
    group_id: str
    payload_json: str
    correct_action: int


@dataclass(frozen=True)
class FrozenEvaluation:
    """Private evaluator manifest; the digest must not be given to learners."""

    train: tuple[_SealedTrial, ...]
    holdout: tuple[_SealedTrial, ...]
    private_commitment_sha256: str


@dataclass(frozen=True)
class ReceiverView:
    """Entire receiver-side API; no episode IDs or evaluator truth."""

    message: bytes | None
    available_actions: tuple[int, int] = (0, 1)


@dataclass(frozen=True)
class CausalScreenResult:
    claim_ceiling: str
    holdout_count: int
    original_accuracy: float
    absent_accuracy: float
    shuffled_accuracy: float | None
    partner_accuracy: float | None
    replay_consistent: bool
    # This means only bytes differ across a rotation; it says NOTHING about
    # causal intervention adequacy or receiver-state isolation.
    message_shuffle_changes_payload: bool
    state_isolation_verified: bool
    causal_listening_qualified: bool
    private_commitment_sha256: str


def _canonical_public_audio(payload: Mapping[str, object]) -> str:
    if not isinstance(payload, Mapping) or set(payload) != _PUBLIC_AUDIO_KEYS:
        raise ValueError("public audio payload must contain exactly the four audio keys")
    if payload["schema"] != _AUDIO_SCHEMA:
        raise ValueError("unsupported blind acoustic observation schema")
    rate = payload["sample_rate_hz"]
    if type(rate) is not int or not 0 < rate <= _MAX_SAMPLE_RATE:
        raise ValueError("sample_rate_hz must be a supported positive integer")
    shape = payload["shape"]
    if (
        not isinstance(shape, list)
        or len(shape) != 2
        or any(type(v) is not int or v <= 0 for v in shape)
        or shape[1] > _MAX_CHANNELS
        or shape[0] * shape[1] > _MAX_SAMPLES
    ):
        raise ValueError("audio shape must be bounded positive [frames, channels]")
    encoded = payload["float64_le_b64"]
    if not isinstance(encoded, str):
        raise ValueError("float64_le_b64 must be ASCII base64 text")
    # Bound input *before* base64 decode allocates its output. The bridge
    # enforces the same exact scalar/channel/frame/sample-rate contract.
    expected_bytes = shape[0] * shape[1] * 8
    expected_chars = 4 * ((expected_bytes + 2) // 3)
    if len(encoded) != expected_chars:
        raise ValueError("float64_le_b64 encoded length does not match shape")
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise ValueError("float64_le_b64 must be canonical base64") from exc
    if len(raw) != expected_bytes or base64.b64encode(raw).decode("ascii") != encoded:
        raise ValueError("float64_le_b64 length or encoding is invalid")
    samples = np.frombuffer(raw, dtype="<f8")
    if not np.all(np.isfinite(samples)):
        raise ValueError("raw acoustic observation must contain only finite samples")
    if np.max(np.abs(samples)) > 1e100:
        raise ValueError("raw acoustic amplitude exceeds stable analysis range")
    # Serialize only this allowlisted, validated projection. A mutable caller
    # dictionary or nested list cannot change the frozen learner input later.
    return json.dumps(
        {"schema": _AUDIO_SCHEMA, "sample_rate_hz": rate,
         "shape": shape, "float64_le_b64": encoded},
        sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    )


def freeze_evaluation(
    train: Sequence[PrivateTrial],
    holdout: Sequence[PrivateTrial],
    *,
    nonce: bytes | None = None,
) -> FrozenEvaluation:
    """Freeze a private split with no overlapping trial or nuisance-group IDs.

    The commitment covers private truth and should not be released before the
    evaluator reveals its salt and the holdout. This is *not* access control.
    """
    if len(train) < 2 or len(holdout) < 2:
        raise ValueError("both training and holdout require at least two trials")
    if nonce is None:
        nonce = secrets.token_bytes(16)
    if not isinstance(nonce, bytes) or len(nonce) < 16:
        raise ValueError("nonce must contain at least 16 secret bytes")
    seen_ids: set[str] = set()
    def prepare(rows: Sequence[PrivateTrial]) -> tuple[_SealedTrial, ...]:
        result = []
        for row in rows:
            if not isinstance(row, PrivateTrial):
                raise ValueError("trials must be PrivateTrial instances")
            if any(not isinstance(v, str) or not v.strip() for v in (row.trial_id, row.group_id)):
                raise ValueError("trial_id and group_id must be nonempty strings")
            if row.trial_id in seen_ids:
                raise ValueError("trial_id must be unique across splits")
            seen_ids.add(row.trial_id)
            if type(row.correct_action) is not int or row.correct_action not in (0, 1):
                raise ValueError("correct_action must be integer 0 or 1")
            result.append(_SealedTrial(
                row.trial_id, row.group_id,
                _canonical_public_audio(row.observation_payload), row.correct_action,
            ))
        return tuple(result)
    frozen_train = prepare(train)
    frozen_holdout = prepare(holdout)
    if {r.group_id for r in frozen_train} & {r.group_id for r in frozen_holdout}:
        raise ValueError("group_id must be disjoint between training and holdout")
    # Distinct filenames/trial IDs are not independent evidence if the
    # learner already saw the exact same observation during training.
    if {r.payload_json for r in frozen_train} & {r.payload_json for r in frozen_holdout}:
        raise ValueError("exact raw observation overlap between training and holdout")
    if {r.correct_action for r in frozen_holdout} != {0, 1}:
        raise ValueError("holdout must contain both actions")
    # Format metadata is visible to the learner. Balance each rate/shape
    # stratum across class labels independently in BOTH splits so neither
    # header length nor sample rate predicts the private action by itself.
    for split_name, rows in (("training", frozen_train), ("holdout", frozen_holdout)):
        metadata_counts: dict[tuple, list[int]] = {}
        for row in rows:
            payload = json.loads(row.payload_json)
            key = (payload["sample_rate_hz"], tuple(payload["shape"]))
            counts = metadata_counts.setdefault(key, [0, 0])
            counts[row.correct_action] += 1
        if any(counts[0] != counts[1] for counts in metadata_counts.values()):
            raise ValueError(f"{split_name} public audio metadata is label-skewed")
    private_manifest = [
        [split, r.trial_id, r.group_id, r.payload_json, r.correct_action]
        for split, rows in (("train", frozen_train), ("holdout", frozen_holdout))
        for r in rows
    ]
    commitment = sha256(nonce + json.dumps(
        private_manifest, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()
    return FrozenEvaluation(frozen_train, frozen_holdout, commitment)


def _message(sender: Callable[[dict], bytes], payload_json: str) -> bytes:
    # Loads a fresh allowlisted copy; no private trial object/IDs/split/truth.
    message = sender(json.loads(payload_json))
    if not isinstance(message, bytes) or not (1 <= len(message) <= _MAX_MESSAGE_BYTES):
        raise ValueError("sender message must be 1-256 opaque bytes")
    return message


def _action(receiver: Callable[[ReceiverView], int], message: bytes | None) -> int:
    result = receiver(ReceiverView(message=message))
    if type(result) is not int or result not in (0, 1):
        raise ValueError("receiver action must be integer 0 or 1")
    return result


def _accuracy(actions: Sequence[int], rows: Sequence[_SealedTrial]) -> float:
    return sum(action == trial.correct_action for action, trial in zip(actions, rows)) / len(rows)


def screen_frozen_holdout(
    plan: FrozenEvaluation,
    sender: Callable[[dict], bytes],
    receiver: Callable[[ReceiverView], int],
    *,
    partner_receiver: Callable[[ReceiverView], int] | None = None,
    shuffle_offset: int = 1,
) -> CausalScreenResult:
    """Run in-process controls. Accuracy deltas are *not* causal qualification.

    Callbacks may share globals, inspect the host or change hidden state. Even
    if replay is stable, this cannot certify a physically frozen receiver.
    """
    if not isinstance(plan, FrozenEvaluation) or len(plan.holdout) < 2:
        raise ValueError("a valid frozen holdout is required")
    rows = plan.holdout
    if type(shuffle_offset) is not int or not 1 <= shuffle_offset < len(rows):
        raise ValueError("shuffle_offset must be within 1..holdout_count-1")
    messages = [_message(sender, r.payload_json) for r in rows]
    originals = [_action(receiver, m) for m in messages]
    replay_messages = [_message(sender, r.payload_json) for r in rows]
    replay_actions = [_action(receiver, m) for m in replay_messages]
    absent = [_action(receiver, None) for _ in rows]
    shifted = messages[-shuffle_offset:] + messages[:-shuffle_offset]
    # Rotating an identical message (or a periodic sequence that rotates onto
    # itself) changes nothing. Report the shuffle as *unidentifiable*, rather
    # than a misleading numerical intervention result.
    changed = len(set(messages)) > 1 and any(
        original != shifted_message
        for original, shifted_message in zip(messages, shifted)
    )
    shuffled = [_action(receiver, m) for m in shifted] if changed else None
    partner = (
        [_action(partner_receiver, m) for m in messages]
        if partner_receiver is not None else None
    )
    return CausalScreenResult(
        claim_ceiling=_CLAIM_CEILING,
        holdout_count=len(rows),
        original_accuracy=_accuracy(originals, rows),
        absent_accuracy=_accuracy(absent, rows),
        shuffled_accuracy=_accuracy(shuffled, rows) if shuffled is not None else None,
        partner_accuracy=_accuracy(partner, rows) if partner is not None else None,
        replay_consistent=(messages == replay_messages and originals == replay_actions),
        message_shuffle_changes_payload=changed,
        state_isolation_verified=False,
        causal_listening_qualified=False,
        private_commitment_sha256=plan.private_commitment_sha256,
    )
