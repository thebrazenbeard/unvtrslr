"""Optional audio.cpp CLI diagnostic adapter; never Num'ta'reen semantic evidence.

Only trusted local executables/models may be configured. Raw WAV bytes are not
preprocessed. Output is an untrusted, unqualified ASR hypothesis, not a gloss.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import io
import math
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import threading
import wave

FAMILIES = frozenset({"nemotron_asr", "parakeet_tdt"})
MAX_WAV_BYTES = 16 * 1024 * 1024
MAX_OUTPUT_BYTES = 8192
CLAIM_CEILING = "HUMAN_ASR_DIAGNOSTIC_UNQUALIFIED"


def _digest(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        raise ValueError("configured dependency must be a regular, non-symlink file")
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class AudioCppConfig:
    command: tuple[str, ...]
    model_path: str
    family: str
    backend: str = "cpu"
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if (type(self.command) is not tuple or not 1 <= len(self.command) <= 8
                or any(type(arg) is not str or not arg or len(arg) > 4096
                       for arg in self.command)
                or not Path(self.command[0]).is_absolute()):
            raise ValueError("command requires absolute trusted executable")
        if self.family not in FAMILIES or self.backend not in ("cpu", "cuda", "vulkan"):
            raise ValueError("unsupported audio.cpp family or backend")
        if type(self.model_path) is not str or not Path(self.model_path).is_absolute():
            raise ValueError("model_path must be absolute")
        t = self.timeout_seconds
        if type(t) not in (int, float) or not math.isfinite(t) or not 0 < t <= 60:
            raise ValueError("timeout must be finite in (0,60] seconds")


@dataclass(frozen=True)
class ASRDiagnostic:
    raw_stdout: str
    wav_sha256: str
    executable_sha256: str
    model_sha256: str
    family: str
    dependency_sha256: tuple[tuple[str, str], ...]
    claim_ceiling: str = CLAIM_CEILING
    semantic_qualification: bool = False
    language_grounding_qualified: bool = False


def _validate_wav(data: bytes) -> None:
    if type(data) is not bytes or not 44 <= len(data) <= MAX_WAV_BYTES:
        raise ValueError("bounded PCM WAV bytes required")
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError("input must be a RIFF/WAVE recording")
    try:
        with wave.open(io.BytesIO(data), "rb") as recorded:
            if (recorded.getcomptype() != "NONE" or recorded.getnchannels() not in (1, 2)
                    or not 8000 <= recorded.getframerate() <= 48000
                    or recorded.getsampwidth() not in (1, 2, 3, 4)
                    or recorded.getnframes() < 1):
                raise ValueError("unsupported WAV format")
    except (EOFError, wave.Error) as exc:
        raise ValueError("malformed PCM WAV") from exc


def _worker_environment() -> dict[str, str]:
    # Restrict inherited credentials; do not pretend this is an OS sandbox.
    env = {}
    for name in ("SystemRoot", "WINDIR"):
        if name in os.environ:
            env[name] = os.environ[name]
    return env


def _stop_process(proc: subprocess.Popen) -> None:
    if os.name == "posix":
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif proc.poll() is None:
        proc.kill()


def transcribe_diagnostic(data: bytes, config: AudioCppConfig) -> ASRDiagnostic:
    """Run one offline ASR attempt with bounded stdout and pinned file inputs.

    No transcript parsing or semantic qualification is inferred from CLI logs.
    """
    _validate_wav(data)
    if type(config) is not AudioCppConfig:
        raise ValueError("explicit audio.cpp configuration required")
    executable = Path(config.command[0])
    model = Path(config.model_path)
    # Existing helper scripts in command are hashed too, not just Python.exe.
    dependencies = [executable, model] + [
        Path(arg) for arg in config.command[1:] if Path(arg).is_absolute()
        and Path(arg).is_file()
    ]
    fingerprints = tuple((str(p), _digest(p)) for p in dependencies)
    wav_digest = hashlib.sha256(data).hexdigest()
    with tempfile.TemporaryDirectory(prefix="unvtrslr-audiocpp-") as directory:
        wav_file = Path(directory) / "original.wav"
        wav_file.write_bytes(data)
        command = [*config.command, "--task", "asr", "--family", config.family,
                   "--model", str(model), "--backend", config.backend,
                   "--mode", "offline", "--audio", str(wav_file)]
        try:
            proc = subprocess.Popen(
                command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, cwd=directory, env=_worker_environment(),
                shell=False, start_new_session=(os.name == "posix"),
            )
        except OSError as exc:
            raise ValueError("audio.cpp executable could not be started") from exc
        output = bytearray()
        excess = threading.Event()
        failed = threading.Event()

        def drain() -> None:
            assert proc.stdout is not None
            try:
                while chunk := proc.stdout.read(4096):
                    if len(output) + len(chunk) > MAX_OUTPUT_BYTES:
                        excess.set()
                        _stop_process(proc)
                        return
                    output.extend(chunk)
            except (OSError, ValueError):
                failed.set()

        reader = threading.Thread(target=drain, daemon=True)
        reader.start()
        try:
            returncode = proc.wait(timeout=config.timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            _stop_process(proc)
            proc.wait()
            raise TimeoutError("audio.cpp attempt timed out") from exc
        finally:
            _stop_process(proc)
            reader.join(timeout=1.5)
            if proc.stdout:
                proc.stdout.close()
        if excess.is_set():
            raise ValueError("audio.cpp output exceeded byte limit")
        if reader.is_alive() or failed.is_set() or returncode != 0:
            raise ValueError("audio.cpp worker did not finish cleanly")
        if hashlib.sha256(wav_file.read_bytes()).hexdigest() != wav_digest:
            raise ValueError("audio input was modified during inference")
        if tuple((name, _digest(Path(name))) for name, _ in fingerprints) != fingerprints:
            raise ValueError("engine, model or helper changed during inference")
    try:
        decoded = output.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("audio.cpp output is not UTF-8") from exc
    return ASRDiagnostic(decoded, wav_digest, fingerprints[0][1],
                         fingerprints[1][1], config.family, fingerprints)
