"""Opt-in, learner-visible *raw* acoustic observation wire contract.

This is a transport boundary, not a semantic bridge. A separate evaluator
must retain any generator seed, symbols, English translation, trial identity,
labels, scoring key, and source provenance. In particular, this module never
imports a Num'ta'reen translator or its private lexicon.

Exact audio bytes can still encode shortcuts through length, timing, source
characteristics, or upstream generation. Three-host/process isolation and
causal grounding are neither provided nor claimed here.
"""

from __future__ import annotations

import base64
import binascii
from numbers import Integral
from typing import Mapping, Sequence

import numpy as np

from .acoustics import _channels


SCHEMA = "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1"
MAX_SAMPLE_VALUES = 262_144
MAX_CHANNELS = 64
MAX_SAMPLE_RATE_HZ = 2_147_483_647
_FIELDS = frozenset(("schema", "sample_rate_hz", "shape", "float64_le_b64"))


def _sample_rate(value: object) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (Integral, np.integer)) or value <= 0:
        raise ValueError("sample_rate_hz must be a positive integer")
    if value > MAX_SAMPLE_RATE_HZ:
        raise ValueError("sample_rate_hz exceeds numeric transport limit")
    return int(value)


def _shape(value: object) -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("shape must be a two-element [frames, channels] list")
    if any(isinstance(n, bool) or not isinstance(n, Integral) or n <= 0 for n in value):
        raise ValueError("shape must contain positive integer dimensions")
    frames, channels = int(value[0]), int(value[1])
    if channels > MAX_CHANNELS or frames * channels > MAX_SAMPLE_VALUES:
        raise ValueError("observation shape exceeds sample limit")
    return frames, channels


def project_audio_observation(
    samples: np.ndarray | Sequence[float] | Sequence[Sequence[float]],
    sample_rate: int,
) -> dict:
    """Expose only losslessly encoded audio and rate, never evaluator metadata.

    Canonical on-wire shape is frames x channels, including mono's one channel.
    The four-key output intentionally contains no stable content hash or source
    identifier; even a truthful hash could become a holdout/episode shortcut.
    """
    rate = _sample_rate(sample_rate)
    raw = np.asarray(samples)
    if raw.size > MAX_SAMPLE_VALUES:
        raise ValueError("observation exceeds sample limit")
    if raw.ndim == 2 and raw.shape[1] > MAX_CHANNELS:
        raise ValueError("observation exceeds channel limit")
    channels = _channels(raw)
    frames, count = _shape(list(channels.shape))
    canonical = np.ascontiguousarray(channels, dtype="<f8")
    return {
        "schema": SCHEMA,
        "sample_rate_hz": rate,
        "shape": [frames, count],
        "float64_le_b64": base64.b64encode(canonical.tobytes(order="C")).decode("ascii"),
    }


def decode_audio_observation(payload: Mapping[str, object]) -> tuple[np.ndarray, int]:
    """Reject additional fields and malformed bodies before PCM allocation.

    Byte order is contractually fixed to IEEE-754 binary64 little endian.
    No algorithm can discover whether arbitrary *unlabelled* finite bytes were
    intentionally serialized with the opposite endianness: some swapped
    patterns are also valid finite little-endian waveforms. Callers must
    independently bind producer wire-format provenance when that matters.
    """
    if not isinstance(payload, Mapping) or set(payload) != _FIELDS:
        raise ValueError("observation fields must match the strict learner allowlist")
    if payload["schema"] != SCHEMA:
        raise ValueError("unsupported observation schema")
    rate = _sample_rate(payload["sample_rate_hz"])
    frames, channels = _shape(payload["shape"])
    encoded = payload["float64_le_b64"]
    if not isinstance(encoded, str):
        raise ValueError("float64_le_b64 encoding must be a string")
    byte_count = frames * channels * 8
    encoded_length = 4 * ((byte_count + 2) // 3)
    if len(encoded) != encoded_length:
        raise ValueError("shape/encoding byte length mismatch")
    try:
        data = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (UnicodeEncodeError, binascii.Error) as exc:
        raise ValueError("invalid canonical base64 encoding") from exc
    if len(data) != byte_count or base64.b64encode(data).decode("ascii") != encoded:
        raise ValueError("invalid canonical base64 encoding length")
    decoded = np.frombuffer(data, dtype="<f8").reshape((frames, channels))
    if not np.all(np.isfinite(decoded)):
        raise ValueError("waveform must contain only finite values")
    if np.max(np.abs(decoded)) > 1e100:
        raise ValueError("sample amplitude exceeds stable numeric analysis range")
    # Backed by immutable bytes. A learner cannot mutate the decoded buffer
    # in-place and thereby alter the shared evaluator observation.
    return decoded, rate
