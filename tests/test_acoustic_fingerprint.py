import math

import numpy as np
import pytest

from unvtrslr.acoustics import acoustic_fingerprint, extract_frame_features
from unvtrslr.information import conditional_mutual_information, mutual_information

SR = 16000


def tone(freq=220.0, seconds=1.0, amp=0.5):
    t = np.arange(int(SR * seconds)) / SR
    return amp * np.sin(2 * np.pi * freq * t)


def chirp(f0, f1, seconds=1.0, amp=0.5):
    t = np.arange(int(SR * seconds)) / SR
    k = (f1 - f0) / seconds
    phase = 2 * np.pi * (f0 * t + 0.5 * k * t * t)
    return amp * np.sin(phase)


def harmonic_tone(f0=180.0, bright=False, seconds=1.0):
    t = np.arange(int(SR * seconds)) / SR
    if bright:
        return (
            0.25 * np.sin(2 * np.pi * f0 * t)
            + 0.30 * np.sin(2 * np.pi * 3 * f0 * t)
            + 0.25 * np.sin(2 * np.pi * 6 * f0 * t)
        )
    return (
        0.55 * np.sin(2 * np.pi * f0 * t)
        + 0.18 * np.sin(2 * np.pi * 2 * f0 * t)
        + 0.08 * np.sin(2 * np.pi * 3 * f0 * t)
    )


def test_f0_estimator_tracks_known_pitch():
    rows = extract_frame_features(tone(220.0), SR)
    f0 = np.array([r.f0_hz for r in rows if r.f0_hz is not None])
    assert len(f0) > 50
    assert abs(np.median(f0) - 220.0) < 3.0


def test_relative_pitch_is_speaker_scale_resistant_for_same_contour():
    low = acoustic_fingerprint(chirp(110.0, 220.0), SR)
    high = acoustic_fingerprint(chirp(220.0, 440.0), SR)
    a = low["channels"]["pitch_relative_semitones"]
    b = high["channels"]["pitch_relative_semitones"]
    assert a["slope"] > 0
    assert b["slope"] > 0
    assert abs(a["range"] - b["range"]) < 0.8


def test_pitch_contour_direction_is_preserved():
    rising = acoustic_fingerprint(chirp(140.0, 280.0), SR)
    falling = acoustic_fingerprint(chirp(280.0, 140.0), SR)
    assert rising["channels"]["pitch_relative_semitones"]["slope"] > 0
    assert falling["channels"]["pitch_relative_semitones"]["slope"] < 0


def test_timbre_changes_without_changing_fundamental():
    dark = acoustic_fingerprint(harmonic_tone(bright=False), SR)
    bright = acoustic_fingerprint(harmonic_tone(bright=True), SR)
    f0a = dark["channels"]["pitch_raw_hz"]["median"]
    f0b = bright["channels"]["pitch_raw_hz"]["median"]
    assert abs(f0a - f0b) < 4.0
    ca = dark["channels"]["spectral_centroid_hz"]["median"]
    cb = bright["channels"]["spectral_centroid_hz"]["median"]
    assert cb > ca * 1.5


def test_amplitude_scale_does_not_move_pitch_or_spectral_centroid_much():
    a = acoustic_fingerprint(tone(200, amp=0.2), SR)
    b = acoustic_fingerprint(tone(200, amp=0.8), SR)
    assert abs(a["channels"]["pitch_raw_hz"]["median"] - b["channels"]["pitch_raw_hz"]["median"]) < 2.0
    assert abs(a["channels"]["spectral_centroid_hz"]["median"] - b["channels"]["spectral_centroid_hz"]["median"]) < 10.0
    assert b["channels"]["intensity_db"]["median"] > a["channels"]["intensity_db"]["median"]


def test_mutual_information_finds_perfect_discrete_channel():
    x = ["low", "low", "high", "high"] * 8
    y = ["A", "A", "B", "B"] * 8
    assert math.isclose(mutual_information(x, y), 1.0, abs_tol=1e-9)


def test_conditional_mi_removes_speaker_only_correlation():
    x = ["low", "low", "high", "high"] * 8
    speaker = ["s1", "s1", "s2", "s2"] * 8
    meaning = ["A", "A", "B", "B"] * 8
    assert mutual_information(x, meaning) > 0.9
    assert math.isclose(conditional_mutual_information(x, meaning, speaker), 0.0, abs_tol=1e-9)


def test_constant_channel_has_zero_information():
    assert mutual_information(["same"] * 20, list("AABB" * 5)) == 0.0


def test_silence_does_not_report_a_fabricated_modulation_peak():
    """The FFT argmax of an all-zero modulation spectrum is not a peak."""
    fingerprint = acoustic_fingerprint(np.zeros(SR, dtype=float), SR)

    assert fingerprint["channels"]["envelope_modulation_peak_hz"] is None


@pytest.mark.parametrize("samples", [np.zeros(SR), np.full(SR, 0.25)])
def test_no_ac_spectrum_is_marked_unmeasurable_without_losing_observation(samples):
    """Silent and DC-only observations have duration but no spectral shape."""
    frames = extract_frame_features(samples, SR)
    fingerprint = acoustic_fingerprint(samples, SR)

    assert len(frames) > 0
    assert all(not frame.spectral_valid for frame in frames)
    assert fingerprint["frame_count"] == len(frames)
    assert fingerprint["spectral_valid_frame_fraction"] == 0.0
    assert fingerprint["channels"]["spectral_centroid_hz"]["median"] is None
    assert fingerprint["channels"]["spectral_rolloff_hz"]["median"] is None
    assert fingerprint["channels"]["spectral_flatness"]["median"] is None
    assert all(coef["median"] is None for coef in fingerprint["channels"]["mfcc"])


def test_measurable_tone_keeps_spectral_values_and_validity():
    frames = extract_frame_features(tone(220.0), SR)
    fingerprint = acoustic_fingerprint(tone(220.0), SR)

    assert all(frame.spectral_valid for frame in frames)
    assert fingerprint["spectral_valid_frame_fraction"] == 1.0
    assert 180 < fingerprint["channels"]["spectral_centroid_hz"]["median"] < 260


def test_spectral_shape_is_stable_under_arbitrary_numeric_amplitude_units():
    """A real tone must not become broadband when its amplitude is tiny."""
    baselines = [
        extract_frame_features(tone(440.0, amp=scale), SR)[0]
        for scale in (1.0, 1e-12, 1e-16)
    ]
    assert all(frame.spectral_valid for frame in baselines)
    assert all(abs(frame.spectral_centroid_hz - 440.0) < 10.0 for frame in baselines)
    assert max(frame.spectral_rolloff_hz for frame in baselines) - min(
        frame.spectral_rolloff_hz for frame in baselines
    ) < 20.0


def test_relative_pitch_is_not_erased_by_arbitrary_input_amplitude_scale():
    for scale in (1.0, 1e-12, 1e-16):
        frames = extract_frame_features(tone(220.0, amp=scale), SR)
        pitches = [frame.f0_hz for frame in frames if frame.f0_hz is not None]
        assert len(pitches) > 50
        assert abs(np.median(pitches) - 220.0) < 3.0


def test_tiny_nonzero_intensities_remain_distinct_from_each_other_and_silence():
    a = acoustic_fingerprint(tone(220.0, amp=1e-12), SR)
    b = acoustic_fingerprint(tone(220.0, amp=1e-16), SR)
    zero = acoustic_fingerprint(np.zeros(SR), SR)
    assert a["channels"]["intensity_db"]["median"] - b["channels"]["intensity_db"]["median"] == pytest.approx(80, abs=0.1)
    assert a["intensity_valid_frame_fraction"] == 1.0
    assert b["intensity_valid_frame_fraction"] == 1.0
    assert zero["intensity_valid_frame_fraction"] == 0.0
    assert zero["channels"]["intensity_db"]["median"] is None


def test_tiny_multichannel_signal_does_not_underflow_channel_selection():
    samples = np.column_stack((tone(220.0, amp=1e-300), tone(440.0, amp=1e-200)))
    result = acoustic_fingerprint(samples, SR)
    channels = result["input_channel_evidence"]
    assert channels["representative_channel_index"] == 1
    assert channels["per_channel"][0]["sample_rms"] > 0
    assert channels["per_channel"][1]["sample_rms"] > channels["per_channel"][0]["sample_rms"]
    assert result["channels"]["pitch_raw_hz"]["median"] == pytest.approx(440, abs=3)


def test_subnormal_second_channel_keeps_valid_signal_and_downmix_diagnostics():
    tiny_tone = tone(440.0, amp=1e-320)
    samples = np.column_stack((np.zeros(SR), tiny_tone))
    result = acoustic_fingerprint(samples, SR)
    evidence = result["input_channel_evidence"]

    assert evidence["representative_channel_index"] == 1
    assert evidence["per_channel"][1]["sample_rms"] > 0
    assert evidence["channel_energy_rms"] > 0
    assert evidence["signed_mean_mix_rms"] > 0
    assert evidence["cancellation_ratio"] is not None
    assert result["intensity_valid_frame_fraction"] == 1.0
    assert result["channels"]["pitch_raw_hz"]["median"] == pytest.approx(440, abs=3)


def test_known_amplitude_modulation_retains_measured_peak():
    t = np.arange(SR * 2) / SR
    amplitude_modulated_tone = (
        0.45 + 0.3 * np.sin(2 * np.pi * 4.0 * t)
    ) * np.sin(2 * np.pi * 200.0 * t)

    fingerprint = acoustic_fingerprint(amplitude_modulated_tone, SR)

    assert abs(fingerprint["channels"]["envelope_modulation_peak_hz"] - 4.0) < 0.2


@pytest.mark.parametrize(
    "settings",
    [
        {"frame_ms": 0.0},
        {"hop_ms": -10.0},
        {"frame_ms": float("nan")},
        {"hop_ms": float("inf")},
        {"fmin": 0.0},
        {"fmin": 500.0, "fmax": 300.0},
        {"fmax": SR},
    ],
)
def test_invalid_acoustic_analysis_settings_fail_closed(settings):
    """Do not silently clamp invalid timing or admit unmeasurable pitch bands."""
    with pytest.raises(ValueError, match="(frame_ms|hop_ms|fmin|fmax)"):
        extract_frame_features(tone(220.0, seconds=0.1), SR, **settings)
