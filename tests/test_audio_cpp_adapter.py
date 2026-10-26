"""Fake-worker integration tests; no model inference or semantic claims."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
import struct
import sys
import wave

import pytest

from unvtrslr.audio_cpp_adapter import (
    ASRDiagnostic, AudioCppConfig, CLAIM_CEILING, transcribe_diagnostic,
)


def _wav():
    handle = io.BytesIO()
    with wave.open(handle, "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(16000)
        writer.writeframes(struct.pack("<h", 100) * 200)
    return handle.getvalue()


def _setup(tmp_path, body="print('hypothesis only')", timeout=5):
    script = tmp_path / "fake_cli.py"
    script.write_text("import pathlib, sys, time\n" + body + "\n", encoding="utf-8")
    model = tmp_path / "pretend.gguf"
    model.write_bytes(b"TEST_PLACEHOLDER_NOT_MODEL")
    return AudioCppConfig((str(Path(sys.executable).resolve()), str(script)),
                          str(model), "parakeet_tdt", timeout_seconds=timeout), script


def test_trusted_worker_returns_unqualified_provenance(tmp_path):
    cfg, script = _setup(tmp_path, """
assert sys.argv[1:5] == ['--task','asr','--family','parakeet_tdt']
assert '--backend' in sys.argv and '--audio' in sys.argv
audio = pathlib.Path(sys.argv[sys.argv.index('--audio') + 1]).read_bytes()
assert audio[:4] == b'RIFF'
print('hello ASR')
""")
    waveform = _wav()
    result = transcribe_diagnostic(waveform, cfg)
    assert result.raw_stdout.strip() == "hello ASR"
    assert result.wav_sha256 == hashlib.sha256(waveform).hexdigest()
    assert result.semantic_qualification is False
    assert result.language_grounding_qualified is False
    assert result.claim_ceiling == CLAIM_CEILING
    assert (str(script), hashlib.sha256(script.read_bytes()).hexdigest()) in result.dependency_sha256
    assert len(result.model_sha256) == len(result.executable_sha256) == 64


def test_mismatched_helper_identity_is_visible_between_invocations(tmp_path):
    cfg, script = _setup(tmp_path)
    first = transcribe_diagnostic(_wav(), cfg)
    script.write_text("print('different text')\n", encoding="utf-8")
    second = transcribe_diagnostic(_wav(), cfg)
    assert first.executable_sha256 == second.executable_sha256
    assert first.dependency_sha256 != second.dependency_sha256


def test_helper_mutation_during_execution_rejected(tmp_path):
    cfg, _ = _setup(tmp_path, """pathlib.Path(__file__).write_text("print('changed')",encoding='utf-8')
print('unsafe output')
""")
    with pytest.raises(ValueError, match="changed during inference"):
        transcribe_diagnostic(_wav(), cfg)


def test_bounded_stdout_and_failure_status(tmp_path):
    cfg, _ = _setup(tmp_path, "sys.stdout.write('x' * 100000)")
    with pytest.raises(ValueError, match="byte limit"):
        transcribe_diagnostic(_wav(), cfg)
    cfg, _ = _setup(tmp_path, "raise SystemExit(5)")
    with pytest.raises(ValueError, match="cleanly"):
        transcribe_diagnostic(_wav(), cfg)


def test_timeout_cannot_produce_qualification(tmp_path):
    cfg, _ = _setup(tmp_path, "time.sleep(3)", timeout=0.15)
    with pytest.raises(TimeoutError, match="timed out"):
        transcribe_diagnostic(_wav(), cfg)


@pytest.mark.parametrize("invalid", [
    b"", b"fake", b"RIFF" + b"x" * 40,
    b"RIFX" + _wav()[4:], _wav()[:22],
])
def test_invalid_waveform_fails_before_worker(tmp_path, invalid):
    cfg, _ = _setup(tmp_path)
    with pytest.raises(ValueError):
        transcribe_diagnostic(invalid, cfg)


def test_explicit_family_and_absolute_paths_required(tmp_path):
    cfg, _ = _setup(tmp_path)
    with pytest.raises(ValueError, match="family"):
        AudioCppConfig(cfg.command, cfg.model_path, "unknown")
    with pytest.raises(ValueError, match="absolute"):
        AudioCppConfig(("python",), cfg.model_path, "nemotron_asr")
    with pytest.raises(ValueError, match="absolute"):
        AudioCppConfig(cfg.command, "relative.gguf", "nemotron_asr")
    with pytest.raises(ValueError, match="timeout"):
        AudioCppConfig(cfg.command, cfg.model_path, "nemotron_asr", timeout_seconds=float("nan"))
