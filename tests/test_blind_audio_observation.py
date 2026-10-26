"""R0.5 blind audio ingress: structural disclosure and exact binary roundtrips."""

import base64

import numpy as np
import pytest

from unvtrslr.blind_audio_observation import (
    MAX_SAMPLE_VALUES,
    decode_audio_observation,
    project_audio_observation,
)
from unvtrslr.acoustics import acoustic_fingerprint
from unvtrslr.events import discover_candidate_units


EXPECTED_KEYS = {"schema", "sample_rate_hz", "shape", "float64_le_b64"}


def test_only_allowlisted_raw_signal_fields_reach_learner():
    packet = project_audio_observation(np.array([0.0, 1e-320, -0.0]), 16000)
    assert set(packet) == EXPECTED_KEYS
    assert packet["schema"] == "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1"
    assert packet["sample_rate_hz"] == 16000
    assert packet["shape"] == [3, 1]
    assert isinstance(packet["float64_le_b64"], str)
    assert all(
        key not in packet
        for key in (
            "english", "meaning", "ipa", "igt", "translation", "truth",
            "source_id", "recording_id", "source_line", "trial_id", "seed",
            "episode_id", "nuisance", "answer", "factor", "symbols",
        )
    )


@pytest.mark.parametrize(
    "samples",
    [
        np.array([0.0, -0.0, 1e-320, -1e-320], dtype=np.float64),
        np.array([[0.1, -0.1], [0.0, -0.0], [1e-250, 2e-250]], dtype=np.float64),
        np.array([[-1.0, 0.0], [0.125, -0.125]], dtype=np.float64),
    ],
)
def test_roundtrip_is_bitwise_lossless_in_canonical_channel_layout(samples):
    packet = project_audio_observation(samples, 16000)
    decoded, sr = decode_audio_observation(packet)
    expected = samples.reshape(-1, 1) if samples.ndim == 1 else samples
    assert sr == 16000
    assert decoded.shape == expected.shape
    assert decoded.dtype == np.dtype("<f8")
    assert decoded.tobytes() == expected.astype("<f8").tobytes()
    assert not decoded.flags.writeable


@pytest.mark.parametrize("sample_rate", [0, -1, True, False, 44.1, float("nan"), "16000", 2**256])
def test_rejects_invalid_sample_rate(sample_rate):
    with pytest.raises(ValueError, match="sample_rate"):
        project_audio_observation([0.0, 0.1], sample_rate)


@pytest.mark.parametrize("bad", [np.nan, np.inf, -np.inf])
def test_rejects_invalid_signal_values(bad):
    with pytest.raises(ValueError, match="finite"):
        project_audio_observation([0.0, bad], 16000)


def test_rejects_oversized_signal_before_serialization():
    with pytest.raises(ValueError, match="limit"):
        project_audio_observation(np.zeros(MAX_SAMPLE_VALUES + 1), 16000)


def test_strict_decoder_rejects_extra_semantic_fields_and_wrong_format_tag():
    valid = project_audio_observation([0.0, 0.1], 16000)
    for key, value in (
        ("source_id", "s1"), ("translation", "danger"),
        ("trial_id", "e0"), ("dtype", "f64be"),
    ):
        with pytest.raises(ValueError, match="fields"):
            decode_audio_observation({**valid, key: value})
    with pytest.raises(ValueError, match="schema"):
        decode_audio_observation({**valid, "schema": "UNVTRSLR_FAKE"})


def test_decoder_checks_shape_and_size_before_base64_decode():
    valid = project_audio_observation([0.0, 0.1], 16000)
    with pytest.raises(ValueError, match="limit"):
        decode_audio_observation({**valid, "shape": [MAX_SAMPLE_VALUES + 1, 1]})
    with pytest.raises(ValueError, match="shape"):
        decode_audio_observation({**valid, "shape": [1, 1]})
    with pytest.raises(ValueError, match="shape"):
        decode_audio_observation({**valid, "shape": [2, True]})
    with pytest.raises(ValueError, match="encoding"):
        decode_audio_observation({**valid, "float64_le_b64": "not base64*"})


def test_decoder_rejects_nonfinite_encoded_data():
    valid = project_audio_observation([0.0], 16000)
    invalid_bytes = np.array([float("inf")], dtype="<f8").tobytes()
    packet = {**valid, "float64_le_b64": base64.b64encode(invalid_bytes).decode("ascii")}
    with pytest.raises(ValueError, match="finite"):
        decode_audio_observation(packet)


def test_private_truth_cannot_be_submitted_to_projection_api():
    with pytest.raises(TypeError):
        project_audio_observation([0.0], 16000, truth="danger")


def test_wire_roundtrip_preserves_existing_acoustic_and_event_behavior():
    sample_rate = 8000
    t = np.arange(sample_rate, dtype=np.float64) / sample_rate
    signal = np.sin(2.0 * np.pi * 440.0 * t) * 1e-12
    restored, rate = decode_audio_observation(project_audio_observation(signal, sample_rate))
    assert acoustic_fingerprint(restored, rate) == acoustic_fingerprint(signal, sample_rate)
    assert discover_candidate_units(restored, rate) == discover_candidate_units(signal, sample_rate)
