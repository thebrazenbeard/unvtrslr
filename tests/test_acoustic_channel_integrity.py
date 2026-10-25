"""Falsifiers for silent losses during acoustic observation preprocessing."""

import math

import numpy as np
import pytest

from unvtrslr.acoustics import (
    acoustic_fingerprint,
    extract_channel_frame_features,
    extract_frame_features,
)


SR = 16000


def _tone(amplitude=0.5, frequency=220.0):
    t = np.arange(SR, dtype=np.float64) / SR
    return amplitude * np.sin(2 * np.pi * frequency * t)


def test_antiphase_channels_are_not_misclassified_as_silence():
    signal = _tone()
    antiphase = np.column_stack((signal, -signal))

    observed = acoustic_fingerprint(antiphase, SR)
    silent = acoustic_fingerprint(np.zeros_like(signal), SR)

    assert observed["channels"]["intensity_db"]["median"] > -12
    assert observed["channels"]["pitch_raw_hz"]["median"] == pytest.approx(220, abs=3)
    assert silent["channels"]["pitch_raw_hz"]["median"] is None
    evidence = observed["input_channel_evidence"]
    assert evidence["channel_count"] == 2
    assert evidence["representative_channel_index"] == 0
    assert evidence["signed_mean_mix_rms"] < 1e-12
    assert evidence["channel_energy_rms"] > 0.3
    assert evidence["cancellation_ratio"] < 1e-10


def test_floating_point_amplitude_is_not_arbitrarily_peak_normalized():
    low = acoustic_fingerprint(_tone(amplitude=1.5), SR)
    high = acoustic_fingerprint(_tone(amplitude=3.0), SR)
    db_diff = high["channels"]["intensity_db"]["median"] - low["channels"]["intensity_db"]["median"]
    assert db_diff == pytest.approx(20 * math.log10(2), abs=0.02)
    assert low["input_channel_evidence"]["per_channel"][0]["sample_peak"] == pytest.approx(1.5)
    assert high["input_channel_evidence"]["per_channel"][0]["sample_peak"] == pytest.approx(3.0)


def test_representation_explicitly_records_dominant_channel_choice():
    quiet_low_pitch = _tone(amplitude=0.1, frequency=120)
    strong_high_pitch = _tone(amplitude=0.8, frequency=240)
    result = acoustic_fingerprint(np.column_stack((quiet_low_pitch, strong_high_pitch)), SR)
    evidence = result["input_channel_evidence"]

    assert evidence["representative_channel_policy"] == "MAXIMUM_RAW_RMS_CHANNEL"
    assert evidence["representative_channel_index"] == 1
    assert result["channels"]["pitch_raw_hz"]["median"] == pytest.approx(240, abs=3)
    assert evidence["per_channel"][0]["sample_rms"] < evidence["per_channel"][1]["sample_rms"]


def test_explicit_per_channel_features_retain_nonrepresentative_signal():
    source = np.column_stack((_tone(frequency=120), _tone(amplitude=0.8, frequency=240)))
    per_channel = extract_channel_frame_features(source, SR)

    assert len(per_channel) == 2
    detected = [np.median([frame.f0_hz for frame in frames if frame.f0_hz]) for frames in per_channel]
    assert detected[0] == pytest.approx(120, abs=3)
    assert detected[1] == pytest.approx(240, abs=3)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_input_is_rejected_instead_of_fabricating_samples(bad):
    signal = _tone()
    signal[0] = bad
    with pytest.raises(ValueError, match="finite"):
        extract_frame_features(signal, SR)


def test_zero_channel_input_is_rejected():
    with pytest.raises(ValueError, match="channel"):
        extract_frame_features(np.empty((SR, 0)), SR)


def test_complex_audio_is_rejected_instead_of_silently_discarding_quadrature():
    with pytest.raises(ValueError, match="real"):
        extract_frame_features(_tone() + 1j * _tone(frequency=330), SR)


def test_finite_but_numeric_overflowing_samples_fail_closed():
    # Finite input is not sufficient when later squared energies overflow.
    # A JSON result containing Infinity/NaN would be invalid evidence.
    with pytest.raises(ValueError, match="amplitude"):
        acoustic_fingerprint(np.full((320, 2), 1e200), 8000)
