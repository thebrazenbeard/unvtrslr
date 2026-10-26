"""Opt-in subprocess transport for trusted, separately executed learners.

The worker sees a restricted JSON request on stdin and replies with JSON on
stdout. It cannot inspect the evaluator's Python stack from another process.
This is *not* an operating-system sandbox: same-user files, services, caches,
clocks, and network paths may still expose private truth or create shortcuts.
Neither this adapter nor high intervention scores qualify semantic learning.
"""

from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass
import json
import math
import os
import signal
import subprocess
import sys
import tempfile
import threading
from typing import Mapping, Sequence

from .blind_audio_observation import SCHEMA as AUDIO_SCHEMA, decode_audio_observation
from .blind_causal_screen import ReceiverView


SENDER_RESPONSE_SCHEMA = "UNVTRSLR_SUBPROCESS_SENDER_RESPONSE_V1"
RECEIVER_REQUEST_SCHEMA = "UNVTRSLR_SUBPROCESS_RECEIVER_REQUEST_V1"
RECEIVER_RESPONSE_SCHEMA = "UNVTRSLR_SUBPROCESS_RECEIVER_RESPONSE_V1"
_AUDIO_FIELDS = frozenset(("schema", "sample_rate_hz", "shape", "float64_le_b64"))
_MAX_MESSAGE_BYTES = 256
_MAX_REQUEST_BYTES = 3_000_000
_MAX_RESPONSE_BYTES = 1024


def _command(argv: Sequence[str], timeout_seconds: float) -> tuple[tuple[str, ...], float]:
    if (
        not isinstance(argv, (list, tuple))
        or not 1 <= len(argv) <= 16
        or any(type(item) is not str or not item or len(item) > 4096 for item in argv)
        or not os.path.isabs(argv[0])
    ):
        raise ValueError("worker argv requires an absolute executable path and bounded arguments")
    if (
        type(timeout_seconds) not in (int, float)
        or not math.isfinite(timeout_seconds)
        or not 0 < timeout_seconds <= 30
    ):
        raise ValueError("worker timeout must be finite and within (0, 30] seconds")
    return tuple(argv), float(timeout_seconds)


def _worker_env() -> dict[str, str]:
    # No inherited PYTHONPATH, HOME, user tokens, or application credentials.
    # Windows needs a system directory to start some executables. This is a
    # privacy reduction, NOT a firewall, filesystem ACL, or security token.
    env = {"PYTHONDONTWRITEBYTECODE": "1"}
    if sys.platform == "win32":
        for key in ("SystemRoot", "WINDIR"):
            if value := os.environ.get(key):
                env[key] = value
    return env


def _unique_json_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate worker JSON key")
        result[key] = value
    return result


def _stop_worker_descendants(child: subprocess.Popen) -> None:
    """Best-effort cleanup of ordinary POSIX descendants in our worker session.

    This is process hygiene, not a sandbox. A descendant can escape its process
    group with setsid(2), and Windows workers are not covered by this mechanism.
    """
    if os.name == "posix":
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def _run_worker(argv: tuple[str, ...], timeout_seconds: float, request: Mapping[str, object]) -> dict:
    wire = json.dumps(request, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
    if len(wire) > _MAX_REQUEST_BYTES:
        raise ValueError("worker request exceeds transport limit")

    # stdout is consumed on a separate thread with a hard byte cap, avoiding
    # subprocess.communicate()'s unbounded-memory stdout accumulation.
    with tempfile.TemporaryDirectory(prefix="unv-blind-worker-") as cwd:
        try:
            child = subprocess.Popen(
                argv,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                cwd=cwd,
                env=_worker_env(),
                shell=False,
                # Isolate a dedicated process group so normal grandchildren can
                # be stopped even after the direct worker has exited.
                start_new_session=(os.name == "posix"),
            )
        except OSError as exc:
            raise ValueError("worker executable could not be started") from exc
        output = bytearray()
        too_large = threading.Event()
        reader_errors: list[OSError] = []

        def send() -> None:
            assert child.stdin is not None
            try:
                child.stdin.write(wire)
                child.stdin.close()
            except (BrokenPipeError, OSError):
                # Child may reject input or exit before reading it.
                pass

        def read() -> None:
            assert child.stdout is not None
            try:
                while chunk := os.read(child.stdout.fileno(), 4096):
                    if len(output) + len(chunk) > _MAX_RESPONSE_BYTES:
                        too_large.set()
                        try:
                            child.kill()
                        except ProcessLookupError:
                            pass
                        return
                    output.extend(chunk)
            except OSError as exc:
                reader_errors.append(exc)

        writer = threading.Thread(target=send, name="unv-blind-stdin", daemon=True)
        reader = threading.Thread(target=read, name="unv-blind-stdout", daemon=True)
        writer.start()
        reader.start()
        try:
            returncode = child.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired as exc:
            child.kill()
            child.wait()
            raise TimeoutError("worker timeout exceeded") from exc
        finally:
            # This must run *before* joining readers: a completed worker may
            # leave descendants holding inherited stdout/stderr pipe FDs open.
            _stop_worker_descendants(child)
            if child.poll() is None:
                child.kill()
                child.wait()
            writer.join(timeout=1)
            reader.join(timeout=1)
            if child.stdin is not None:
                child.stdin.close()
            if child.stdout is not None:
                child.stdout.close()
        if too_large.is_set():
            raise ValueError("worker output limit exceeded")
        if reader_errors or reader.is_alive() or writer.is_alive():
            raise ValueError("worker response channel did not finish cleanly")
        if returncode != 0:
            raise ValueError("worker exited with nonzero status")
        try:
            result = json.loads(output.decode("utf-8"), object_pairs_hook=_unique_json_object)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("worker response must be valid UTF-8 JSON") from exc
        if not isinstance(result, dict):
            raise ValueError("worker response must be a JSON object")
        return result


def _decode_message(encoded: object) -> bytes:
    if not isinstance(encoded, str) or not 4 <= len(encoded) <= 4 * ((_MAX_MESSAGE_BYTES + 2) // 3):
        raise ValueError("message_b64 must encode 1-256 bytes")
    try:
        raw = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (UnicodeEncodeError, binascii.Error) as exc:
        raise ValueError("message_b64 must be canonical ASCII base64") from exc
    if not 1 <= len(raw) <= _MAX_MESSAGE_BYTES or base64.b64encode(raw).decode("ascii") != encoded:
        raise ValueError("message_b64 must encode 1-256 canonical bytes")
    return raw


@dataclass(frozen=True)
class SubprocessBlindSender:
    """Callable sender suitable for `screen_frozen_holdout`, with new process per trial."""

    argv: tuple[str, ...]
    timeout_seconds: float = 5.0

    def __post_init__(self) -> None:
        argv, timeout = _command(self.argv, self.timeout_seconds)
        object.__setattr__(self, "argv", argv)
        object.__setattr__(self, "timeout_seconds", timeout)

    def __call__(self, public_audio: Mapping[str, object]) -> bytes:
        if not isinstance(public_audio, Mapping) or set(public_audio) != _AUDIO_FIELDS:
            raise ValueError("sender input must contain exactly four acoustic observation keys")
        # Validate before starting child. Explicit on-wire primitives avoid
        # serializing arbitrary Python objects through a compromised __repr__.
        if (
            public_audio["schema"] != AUDIO_SCHEMA
            or type(public_audio["sample_rate_hz"]) is not int
            or type(public_audio["shape"]) is not list
            or any(type(value) is not int for value in public_audio["shape"])
        ):
            raise ValueError("sender input must use canonical JSON audio primitives")
        decode_audio_observation(public_audio)
        reply = _run_worker(self.argv, self.timeout_seconds, dict(public_audio))
        if set(reply) != {"schema", "message_b64"}:
            raise ValueError("sender response must contain exactly two fields")
        if reply["schema"] != SENDER_RESPONSE_SCHEMA:
            raise ValueError("unsupported subprocess sender response schema")
        return _decode_message(reply["message_b64"])


@dataclass(frozen=True)
class SubprocessBlindReceiver:
    """Callable receiver with no evaluator trial metadata in child arguments."""

    argv: tuple[str, ...]
    timeout_seconds: float = 5.0

    def __post_init__(self) -> None:
        argv, timeout = _command(self.argv, self.timeout_seconds)
        object.__setattr__(self, "argv", argv)
        object.__setattr__(self, "timeout_seconds", timeout)

    def __call__(self, view: ReceiverView) -> int:
        if type(view) is not ReceiverView or view.available_actions != (0, 1):
            raise ValueError("receiver input must be canonical ReceiverView")
        if view.message is not None and (
            type(view.message) is not bytes or not 1 <= len(view.message) <= _MAX_MESSAGE_BYTES
        ):
            raise ValueError("receiver message must be 1-256 bytes or None")
        request = {
            "schema": RECEIVER_REQUEST_SCHEMA,
            "message_b64": base64.b64encode(view.message).decode("ascii") if view.message is not None else None,
            "available_actions": [0, 1],
        }
        reply = _run_worker(self.argv, self.timeout_seconds, request)
        if set(reply) != {"schema", "action"}:
            raise ValueError("receiver response must contain exactly two fields")
        if reply["schema"] != RECEIVER_RESPONSE_SCHEMA:
            raise ValueError("unsupported subprocess receiver response schema")
        if type(reply["action"]) is not int or reply["action"] not in (0, 1):
            raise ValueError("receiver action must be integer 0 or 1")
        return reply["action"]
