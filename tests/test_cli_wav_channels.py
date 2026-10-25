"""The CLI adapter must not destroy multichannel measurements before analysis."""

import wave

import numpy as np
import pytest

from unvtrslr.cli import _read_wav


def _write_pcm16(path, frames: np.ndarray) -> None:
    samples = np.asarray(frames, dtype="<i2")
    if samples.ndim != 2:
        raise ValueError("test frames must have (time, channel) shape")
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(samples.shape[1])
        stream.setsampwidth(2)
        stream.setframerate(16000)
        stream.writeframes(samples.tobytes())


def test_multichannel_wav_preserves_antiphase_and_shape(tmp_path):
    path = tmp_path / "antiphase.wav"
    tone = np.array([0, 8192, -8192, 16384, -16384], dtype="<i2")
    _write_pcm16(path, np.column_stack([tone, -tone]))

    observed, rate = _read_wav(str(path))

    assert rate == 16000
    assert observed.shape == (len(tone), 2)
    np.testing.assert_allclose(observed[:, 0], tone / 32768.0)
    np.testing.assert_allclose(observed[:, 1], -tone / 32768.0)


def test_mono_wav_retains_existing_vector_shape(tmp_path):
    path = tmp_path / "mono.wav"
    tone = np.array([0, -8192, 8192], dtype="<i2")
    _write_pcm16(path, tone[:, None])

    observed, rate = _read_wav(str(path))

    assert rate == 16000
    assert observed.shape == (len(tone),)
    np.testing.assert_allclose(observed, tone / 32768.0)


def test_pcm_byte_width_validation_is_unchanged(tmp_path):
    path = tmp_path / "unsupported-width.wav"
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(1)
        stream.setsampwidth(3)
        stream.setframerate(16000)
        stream.writeframes(bytes(3))

    with pytest.raises(ValueError, match="unsupported PCM sample width"):
        _read_wav(str(path))
