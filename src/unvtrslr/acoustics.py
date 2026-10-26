from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import math

import numpy as np
from scipy.fft import dct
from scipy.signal import get_window

_EPS = 1e-12


@dataclass(frozen=True)
class FrameFeatures:
    time_s: float
    rms_db: float
    f0_hz: float | None
    periodicity: float
    spectral_centroid_hz: float
    spectral_bandwidth_hz: float
    spectral_flatness: float
    spectral_rolloff_hz: float
    spectral_slope_db_octave: float
    h1_h2_db: float | None
    mfcc: tuple[float, ...]
    # False means spectral floats/MFCCs are compatibility placeholders, not
    # measurements. Timing/intensity retain the original frame observation.
    spectral_valid: bool = True
    # Exact zero has no finite logarithmic intensity. Its numeric -120 dB
    # placeholder is invalid; consumers should use this evidence mask.
    intensity_valid: bool = True


def _channels(samples: np.ndarray | Iterable[float]) -> np.ndarray:
    """Validate input observations, retaining all provided channel samples.

    No physical reference amplitude, ADC full scale, or interchannel phase
    alignment is inferred from arbitrary numeric sample values.
    """
    raw = np.asarray(samples)
    if np.iscomplexobj(raw):
        raise ValueError("samples must be real-valued audio, not complex I/Q samples")
    x = np.asarray(raw, dtype=np.float64)
    if x.ndim == 1:
        x = x[:, np.newaxis]
    elif x.ndim != 2:
        raise ValueError("samples must be mono or shape (n_samples, n_channels)")
    if x.shape[0] == 0:
        raise ValueError("samples must not be empty")
    if x.shape[1] == 0:
        raise ValueError("samples must have at least one channel")
    if not np.all(np.isfinite(x)):
        raise ValueError("samples must contain only finite values")
    # Energies, autocorrelations and FFT power all square/accumulate values.
    # Finite float64 input alone is not enough to keep those computations
    # finite. Fail closed on pathological magnitudes instead of emitting
    # Infinity/NaN into evidence; this broad bound is numerical, not a claim
    # about physical calibration or the format's full dynamic range.
    if np.max(np.abs(x)) > 1e100:
        raise ValueError("sample amplitude exceeds stable numeric analysis range")
    return x


def _channel_rms(channels: np.ndarray) -> np.ndarray:
    # Rescale before squaring: direct x*x would underflow for small valid
    # numeric samples (or overflow before _channels applies its input bound).
    peaks = np.max(np.abs(channels), axis=0)
    normalized = channels / np.where(peaks > 0.0, peaks, 1.0)
    return peaks * np.sqrt(np.mean(np.square(normalized), axis=0))


def _representative_channel_index(channels: np.ndarray) -> int:
    # Signed channel averaging can erase genuine antiphase observations.
    # Highest-energy is only a deterministic representative, not a beamformer
    # or a claim that the remaining channels lack distinct structure.
    return int(np.argmax(_channel_rms(channels)))


def _mono(samples: np.ndarray | Iterable[float]) -> np.ndarray:
    """Select a representative channel without phase-cancelling downmixing."""
    channels = _channels(samples)
    return channels[:, _representative_channel_index(channels)]


def _channel_evidence(channels: np.ndarray) -> dict:
    """Retain basic per-channel magnitudes and downmix-loss diagnostics.

    This summary is lossy: original per-channel samples remain necessary for
    phase, spatial, timing, provenance, and alternative-channel analyses.
    """
    rms = _channel_rms(channels)
    peaks = np.max(np.abs(channels), axis=0)
    signed_mean_rms = float(_channel_rms(np.mean(channels, axis=1)[:, np.newaxis])[0])
    channel_energy_rms = float(_channel_rms(channels.reshape(-1, 1))[0])
    return {
        "channel_count": int(channels.shape[1]),
        "representative_channel_policy": "MAXIMUM_RAW_RMS_CHANNEL",
        "representative_channel_index": _representative_channel_index(channels),
        "measurement_units": "ORIGINAL_INPUT_NUMERIC_UNITS_NOT_CALIBRATED",
        "per_channel": [
            {
                "channel_index": i,
                "sample_rms": float(rms[i]),
                "sample_peak": float(peaks[i]),
            }
            for i in range(channels.shape[1])
        ],
        "signed_mean_mix_rms": signed_mean_rms,
        "channel_energy_rms": channel_energy_rms,
        "cancellation_ratio": (
            float(signed_mean_rms / channel_energy_rms)
            if channel_energy_rms > 0.0
            else None
        ),
        "claim_limit": "SUMMARY_ONLY_RETAIN_RAW_CHANNELS_FOR_REANALYSIS",
    }


def _frames(x: np.ndarray, frame_size: int, hop: int) -> np.ndarray:
    if x.size < frame_size:
        x = np.pad(x, (0, frame_size - x.size))
    n = 1 + max(0, (x.size - frame_size) // hop)
    return np.stack([x[i * hop : i * hop + frame_size] for i in range(n)])


def _estimate_f0(frame: np.ndarray, sr: int, fmin: float, fmax: float) -> tuple[float | None, float]:
    centered = frame - frame.mean()
    peak = float(np.max(np.abs(centered)))
    reference = float(np.max(np.abs(frame)))
    if peak <= 32.0 * np.finfo(np.float64).eps * reference:
        return None, 0.0
    # Periodicity is a scale-relative measurement. A fixed absolute-energy
    # gate silently erases identical low-amplitude contours in raw units.
    centered = centered / peak
    energy = float(np.dot(centered, centered))
    if energy < 1e-9:
        return None, 0.0
    corr = np.correlate(centered, centered, mode="full")[len(centered) - 1 :]
    corr /= max(float(corr[0]), _EPS)
    min_lag = max(1, int(sr / fmax))
    max_lag = min(len(corr) - 1, int(sr / fmin))
    if max_lag <= min_lag:
        return None, 0.0
    segment = corr[min_lag : max_lag + 1]
    rel = int(np.argmax(segment))
    lag = min_lag + rel
    periodicity = float(segment[rel])
    if periodicity < 0.25:
        return None, max(0.0, periodicity)
    if 1 <= lag < len(corr) - 1:
        a, b, c = corr[lag - 1], corr[lag], corr[lag + 1]
        denom = a - 2 * b + c
        if abs(denom) > _EPS:
            lag = lag + 0.5 * (a - c) / denom
    return float(sr / lag), periodicity


def _mel(freq_hz):
    return 2595.0 * np.log10(1.0 + np.asarray(freq_hz) / 700.0)


def _inv_mel(mel):
    return 700.0 * (10.0 ** (np.asarray(mel) / 2595.0) - 1.0)


def _mfcc(power: np.ndarray, freqs: np.ndarray, sr: int, n_mels: int = 26, n_coeffs: int = 13) -> tuple[float, ...]:
    mel_points = np.linspace(float(_mel(20.0)), float(_mel(sr / 2.0)), n_mels + 2)
    hz_points = _inv_mel(mel_points)
    energies = []
    for left_hz, center_hz, right_hz in zip(hz_points[:-2], hz_points[1:-1], hz_points[2:]):
        up = (freqs - left_hz) / max(center_hz - left_hz, _EPS)
        down = (right_hz - freqs) / max(right_hz - center_hz, _EPS)
        weights = np.maximum(0.0, np.minimum(up, down))
        energies.append(float(np.sum(power * weights)))
    log_e = np.log(np.maximum(np.asarray(energies), _EPS))
    return tuple(float(v) for v in dct(log_e, type=2, norm="ortho")[:n_coeffs])


def _spectral_slope(freqs: np.ndarray, mag: np.ndarray) -> float:
    mask = (freqs >= 80.0) & (mag > _EPS)
    if np.count_nonzero(mask) < 4:
        return 0.0
    x = np.log2(freqs[mask])
    y = 20.0 * np.log10(mag[mask])
    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def _harmonic_amplitude(freqs: np.ndarray, mag: np.ndarray, target: float) -> float:
    if target <= 0 or target > freqs[-1]:
        return 0.0
    idx = int(np.argmin(np.abs(freqs - target)))
    return float(np.max(mag[max(0, idx - 1) : min(len(mag), idx + 2)]))


def extract_frame_features(
    samples: np.ndarray | Iterable[float],
    sample_rate: int,
    *,
    frame_ms: float = 40.0,
    hop_ms: float = 10.0,
    fmin: float = 60.0,
    fmax: float = 500.0,
) -> list[FrameFeatures]:
    """Extract acoustic frame descriptors from one representative channel.

    For multichannel inputs, the channel with maximum RMS is selected, with
    first-channel tie breaking. Supply a single channel explicitly to examine
    any other channel; no multichannel fusion or spatial inference is made.
    """
    if sample_rate < 2000:
        raise ValueError("sample_rate is too low for speech-like acoustic analysis")
    for name, value in (("frame_ms", frame_ms), ("hop_ms", hop_ms)):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be positive and finite")
    if not math.isfinite(fmin) or fmin <= 0:
        raise ValueError("fmin must be positive and finite")
    if not math.isfinite(fmax) or fmax <= fmin or fmax > sample_rate / 2:
        raise ValueError("fmax must be finite, greater than fmin, and at most Nyquist")
    x = _mono(samples)
    frame_size = max(64, int(round(sample_rate * frame_ms / 1000.0)))
    hop = max(1, int(round(sample_rate * hop_ms / 1000.0)))
    window = get_window("hann", frame_size, fftbins=True)
    rows: list[FrameFeatures] = []

    for i, frame in enumerate(_frames(x, frame_size, hop)):
        f0, periodicity = _estimate_f0(frame, sample_rate, fmin, fmax)
        raw_peak = float(np.max(np.abs(frame)))
        intensity_valid = raw_peak > 0.0
        if intensity_valid:
            # The logarithm is additive, so unit-scaled squaring retains
            # nonzero magnitudes far below float64's direct-square range.
            scaled_rms = math.sqrt(float(np.mean(np.square(frame / raw_peak))))
            rms_db = 20.0 * (math.log10(raw_peak) + math.log10(scaled_rms))
        else:
            # Retain existing finite float contract for event consumers but
            # do not present this number as a measured intensity.
            rms_db = -120.0
        centered = frame - frame.mean()
        # An all-zero or constant-DC frame has no observable AC spectrum.
        # Use the amplitude-relative roundoff floor, not a fixed sound-level
        # threshold: these input numbers have no physical amplitude units.
        numerical_floor = 32.0 * np.finfo(np.float64).eps * float(np.max(np.abs(frame)))
        spectral_valid = bool(np.max(np.abs(centered)) > numerical_floor)
        h1_h2 = None
        if spectral_valid:
            # Shape descriptors are source-relative, not acoustic level
            # meters. Normalize BEFORE FFT so arbitrary input scale does not
            # turn a very quiet tonal signal into a fabricated flat spectrum.
            normalized = centered / float(np.max(np.abs(centered)))
            spectrum = np.fft.rfft(normalized * window)
            mag = np.abs(spectrum)
            power = mag * mag
            freqs = np.fft.rfftfreq(frame_size, d=1.0 / sample_rate)
            total = float(np.sum(power))
            centroid = float(np.sum(freqs * power) / total)
            bandwidth = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * power) / total))
            relative_floor = max(float(np.max(power)) * 1e-12, np.finfo(np.float64).tiny)
            flatness = float(np.exp(np.mean(np.log(np.maximum(power, relative_floor)))) / max(np.mean(power), relative_floor))
            cdf = np.cumsum(power)
            roll_idx = int(np.searchsorted(cdf, 0.85 * cdf[-1]))
            rolloff = float(freqs[min(roll_idx, len(freqs) - 1)])
            slope = _spectral_slope(freqs, mag)
            coefficients = _mfcc(power, freqs, sample_rate)
            if f0 is not None:
                h1 = _harmonic_amplitude(freqs, mag, f0)
                h2 = _harmonic_amplitude(freqs, mag, 2.0 * f0)
                if h1 > _EPS and h2 > _EPS:
                    h1_h2 = float(20.0 * np.log10(h1 / h2))
        else:
            # Preserve the numeric field contract for event consumers. These
            # zeros are explicitly invalid placeholders, NOT measured values.
            centroid = bandwidth = flatness = rolloff = slope = 0.0
            coefficients = (0.0,) * 13
        rows.append(
            FrameFeatures(
                time_s=(i * hop + frame_size / 2) / sample_rate,
                rms_db=rms_db,
                f0_hz=f0,
                periodicity=float(periodicity),
                spectral_centroid_hz=centroid,
                spectral_bandwidth_hz=bandwidth,
                spectral_flatness=flatness,
                spectral_rolloff_hz=rolloff,
                spectral_slope_db_octave=slope,
                h1_h2_db=h1_h2,
                mfcc=coefficients,
                spectral_valid=spectral_valid,
                intensity_valid=intensity_valid,
            )
        )
    return rows


def extract_channel_frame_features(
    samples: np.ndarray | Iterable[float],
    sample_rate: int,
    *,
    frame_ms: float = 40.0,
    hop_ms: float = 10.0,
    fmin: float = 60.0,
    fmax: float = 500.0,
) -> tuple[list[FrameFeatures], ...]:
    """Extract frame features for *every* channel, retaining channel order.

    Unlike the representative-channel `extract_frame_features`, this function
    makes no implicit channel selection. It still compresses frame observations;
    preserve the original sampled signals for source-level reanalysis.
    """
    channels = _channels(samples)
    return tuple(
        extract_frame_features(
            channels[:, i],
            sample_rate,
            frame_ms=frame_ms,
            hop_ms=hop_ms,
            fmin=fmin,
            fmax=fmax,
        )
        for i in range(channels.shape[1])
    )


def _summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"median": None, "iqr": None, "mean": None, "std": None}
    a = np.asarray(values, dtype=np.float64)
    q25, q75 = np.quantile(a, [0.25, 0.75])
    return {
        "median": float(np.median(a)),
        "iqr": float(q75 - q25),
        "mean": float(np.mean(a)),
        "std": float(np.std(a)),
    }


def _trajectory_stats(values: np.ndarray) -> dict[str, float | None]:
    if values.size < 2:
        return {"slope": None, "curvature": None, "range": None}
    t = np.linspace(-1.0, 1.0, values.size)
    curvature = float(np.polyfit(t, values, 2)[0]) if values.size >= 3 else None
    return {
        "slope": float(np.polyfit(t, values, 1)[0]),
        "curvature": curvature,
        "range": float(np.max(values) - np.min(values)),
    }


def acoustic_fingerprint(samples: np.ndarray | Iterable[float], sample_rate: int) -> dict:
    """Return a source-relative multidimensional acoustic fingerprint."""
    channels = _channels(samples)
    input_channel_evidence = _channel_evidence(channels)
    # Reuse the audited choice for both the frame descriptors and the summary.
    representative = channels[:, input_channel_evidence["representative_channel_index"]]
    rows = extract_frame_features(representative, sample_rate)
    f0 = np.asarray([r.f0_hz for r in rows if r.f0_hz is not None], dtype=np.float64)
    f0_semitones = np.asarray([], dtype=np.float64)
    if f0.size:
        anchor = float(np.median(f0))
        f0_semitones = 12.0 * np.log2(f0 / anchor)

    rms = [r.rms_db for r in rows if r.intensity_valid]
    spectral_rows = [r for r in rows if r.spectral_valid]
    centroid = [r.spectral_centroid_hz for r in spectral_rows]
    bandwidth = [r.spectral_bandwidth_hz for r in spectral_rows]
    flatness = [r.spectral_flatness for r in spectral_rows]
    rolloff = [r.spectral_rolloff_hz for r in spectral_rows]
    slope = [r.spectral_slope_db_octave for r in spectral_rows]
    h1h2 = [r.h1_h2_db for r in rows if r.h1_h2_db is not None]
    periodicity = [r.periodicity for r in rows]
    mfcc_matrix = np.asarray([r.mfcc for r in spectral_rows], dtype=np.float64)
    mfcc_summary = []
    if mfcc_matrix.size:
        for i in range(mfcc_matrix.shape[1]):
            mfcc_summary.append({"index": i, **_summary(mfcc_matrix[:, i].tolist())})
    else:
        mfcc_summary = [{"index": i, **_summary([])} for i in range(13)]

    envelope = np.asarray([
        10.0 ** (r.rms_db / 20.0) if r.intensity_valid else 0.0
        for r in rows
    ])
    envelope_constant = bool(np.ptp(envelope) == 0.0)
    envelope = envelope - np.mean(envelope)
    peak_mod_hz = None
    if envelope.size >= 8 and not envelope_constant:
        mod_freqs = np.fft.rfftfreq(envelope.size, d=0.010)
        mod_power = np.abs(np.fft.rfft(envelope)) ** 2
        band = (mod_freqs >= 0.5) & (mod_freqs <= 12.0)
        # A zero modulation spectrum has no measured peak. In particular,
        # argmax(zeros) would turn silence into an arbitrary nonzero frequency.
        # Check the uncentered envelope too: mean subtraction of a constant
        # array can leave floating-point roundoff that has a spurious FFT peak.
        # For nonzero spectra this remains a descriptive maximum, not a
        # significance test or evidence that the modulation is communicative.
        if np.any(band) and np.any(mod_power[band] > 0.0):
            band_freqs = mod_freqs[band]
            band_power = mod_power[band]
            peak_mod_hz = float(band_freqs[int(np.argmax(band_power))])

    return {
        "schema": "UNVTRSLR_ACOUSTIC_FINGERPRINT_V1",
        "claim_ceiling": "ACOUSTIC_STRUCTURE_ONLY_NO_SEMANTIC_QUALIFICATION",
        "input_channel_evidence": input_channel_evidence,
        "frame_count": len(rows),
        "spectral_valid_frame_fraction": float(len(spectral_rows) / max(len(rows), 1)),
        "intensity_valid_frame_fraction": float(len(rms) / max(len(rows), 1)),
        "voiced_frame_fraction": float(len(f0) / max(len(rows), 1)),
        "channels": {
            "pitch_raw_hz": _summary(f0.tolist()),
            "pitch_relative_semitones": {**_summary(f0_semitones.tolist()), **_trajectory_stats(f0_semitones)},
            "intensity_db": {**_summary(rms), **_trajectory_stats(np.asarray(rms))},
            "periodicity": _summary(periodicity),
            "spectral_centroid_hz": _summary(centroid),
            "spectral_bandwidth_hz": _summary(bandwidth),
            "spectral_flatness": _summary(flatness),
            "spectral_rolloff_hz": _summary(rolloff),
            "spectral_slope_db_octave": _summary(slope),
            "h1_h2_db": _summary(h1h2),
            "mfcc": mfcc_summary,
            "envelope_modulation_peak_hz": peak_mod_hz,
        },
    }
