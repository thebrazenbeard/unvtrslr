"""Process-separated R2 binary-channel *smoke screen*, not semantic qualification.

Each invocation starts a fresh OS process. The sender receives only the toy
binary factor; the receiver receives only a message and task. No episode IDs,
simulator objects or shared Python instances cross that interface.

IMPORTANT: Child processes are NOT sandboxed; they may still communicate by
host files, network, clocks, executable internals or other undeclared means.
Run only explicitly trusted, pre-inspected adapters. A passing reference
screen does not establish language learning, grounded semantics or security.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from secrets import SystemRandom
import signal
import subprocess
import tempfile

from .r2_controls import ControlEpisode


@dataclass(frozen=True)
class ProcessEndpoint:
    """An explicitly authorized argv (no shell), not an untrusted code sandbox."""

    argv: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.argv, tuple) or not self.argv or any(
            not isinstance(arg, str) or not arg for arg in self.argv
        ):
            raise ValueError("endpoint argv must be a nonempty tuple of nonempty strings")


@dataclass(frozen=True)
class ProcessChannelScreen:
    status: str
    baseline_accuracy: float
    ablation_drop: float
    counterfactual_flip_rate: float | None
    repeat_consistency: float
    inverted_task_accuracy: float
    episodes: int
    receiver_input_fields: tuple[str, ...]
    distinct_opposite_factor_messages: bool
    numerical_gates_met: bool
    intervention_order: tuple[tuple[str, ...], ...]
    isolation_statement: str = "FRESH_PROCESSES_WITHOUT_OS_SANDBOX"
    claim_ceiling: str = "UNQUALIFIED_SYNTHETIC_CHANNEL_DIAGNOSTIC"


def _stop_endpoint(process: subprocess.Popen, *, posix_group: bool) -> None:
    """Best-effort descendant cleanup, NOT process isolation or a sandbox.

    POSIX children receive their own session/group at startup. Killing that
    group also stops ordinary descendants even if the initial process exited.
    Windows Python has no equivalent Job Object ownership here, so the direct
    child alone is killed and that limitation must remain explicit.
    """
    if posix_group:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        process.kill()


def _ask(
    endpoint: ProcessEndpoint, payload: dict, *, timeout_seconds: float, max_reply_bytes: int
) -> dict:
    # Minimal child environment and a fresh cwd reduce accidental coupling,
    # but neither prevents intentional shared-file/network collusion. On
    # POSIX the child starts a fresh process group for timeout cleanup; it
    # can still escape that group (e.g. setsid) and is NOT sandboxed.
    env = {"PATH": os.environ.get("PATH", os.defpath), "PYTHONIOENCODING": "utf-8"}
    posix_group = os.name == "posix"
    with tempfile.TemporaryDirectory(prefix="unvtrslr-r2-") as cwd, tempfile.TemporaryFile() as output:
        try:
            process = subprocess.Popen(
                endpoint.argv,
                stdin=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                stdout=output,
                stderr=subprocess.DEVNULL,
                cwd=Path(cwd),
                env=env,
                shell=False,
                start_new_session=posix_group,
            )
        except OSError as exc:
            raise ValueError("process endpoint could not start") from exc
        try:
            try:
                process.communicate(
                    input=json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
                    timeout=timeout_seconds,
                )
            except subprocess.TimeoutExpired as exc:
                raise ValueError("process endpoint timed out") from exc
        finally:
            # Clean the group on normal exits too: a child can fork and exit
            # leaving a descendant active without triggering the timeout.
            _stop_endpoint(process, posix_group=posix_group)
            process.wait()
        if process.returncode != 0:
            raise ValueError("process endpoint returned a nonzero exit status")
        # A temporary file avoids unbounded stdout accumulation in RAM. Check
        # its actual size: an endpoint may seek its inherited stdout backwards
        # and leave the shared file offset below its emitted byte count.
        # This is still only a *post-execution disk* check, not a write quota.
        if os.fstat(output.fileno()).st_size > max_reply_bytes:
            raise ValueError("process endpoint exceeded reply size limit")
        output.seek(0)
        raw = output.read(max_reply_bytes + 1)
    try:
        reply = json.loads(raw.decode("utf-8"))
    except (ValueError, TypeError, UnicodeError) as exc:
        raise ValueError("process endpoint did not return one valid JSON object") from exc
    if not isinstance(reply, dict):
        raise ValueError("process endpoint must return a JSON object")
    return reply


def screen_process_channel(
    sender: ProcessEndpoint,
    receiver: ProcessEndpoint,
    episodes: tuple[ControlEpisode, ...],
    *,
    timeout_seconds: float = 3.0,
    max_reply_bytes: int = 4096,
) -> ProcessChannelScreen:
    """Intervene on receiver messages using fresh process instances.

    The test's binary factor and task are explicitly evaluator-authored. This
    proves only a process-separated synthetic channel on the supplied cases.
    """
    if not isinstance(sender, ProcessEndpoint) or not isinstance(receiver, ProcessEndpoint):
        raise TypeError("sender and receiver must be ProcessEndpoint instances")
    if not 0 < timeout_seconds <= 60 or not 64 <= max_reply_bytes <= 65536:
        raise ValueError("invalid resource bounds")
    if not isinstance(episodes, tuple) or not episodes or len(episodes) % 2:
        raise ValueError("baseline episodes must be a nonempty even tuple")
    if any(not isinstance(ep, ControlEpisode) or ep.task != "align" for ep in episodes):
        raise ValueError("baseline episodes must be align ControlEpisode values")
    if sum(ep.factor for ep in episodes) * 2 != len(episodes):
        raise ValueError("baseline episodes must balance factors")
    if len({ep.episode_id for ep in episodes}) != len(episodes):
        raise ValueError("baseline episode IDs must be unique")

    def receive(message: str | None, task: str) -> int:
        response = _ask(
            receiver,
            {"message": message, "task": task},
            timeout_seconds=timeout_seconds,
            max_reply_bytes=max_reply_bytes,
        )
        if set(response) != {"action"} or type(response["action"]) is not int or response["action"] not in (0, 1):
            raise ValueError("receiver response must contain only a binary integer action")
        return response["action"]

    messages = []
    for ep in episodes:
        response = _ask(
            sender,
            {"factor": ep.factor},
            timeout_seconds=timeout_seconds,
            max_reply_bytes=max_reply_bytes,
        )
        if set(response) != {"message"} or not isinstance(response["message"], str):
            raise ValueError("sender response must contain only a string message")
        if not 0 < len(response["message"].encode("utf-8")) <= 256:
            raise ValueError("sender message must be 1..256 UTF-8 bytes")
        messages.append(response["message"])

    correct = ablated_correct = flips = repeats = inverted_correct = 0
    # Compare *all* messages from both factor classes. Checking only one
    # opposite-factor partner misses collisions among later observations.
    distinct_messages = {
        message for ep, message in zip(episodes, messages) if ep.factor == 0
    }.isdisjoint({
        message for ep, message in zip(episodes, messages) if ep.factor == 1
    })
    intervention_order = []
    rng = SystemRandom()
    for i, ep in enumerate(episodes):
        message = messages[i]
        alternate = messages[next(j for j, other in enumerate(episodes) if other.factor != ep.factor)]
        interventions = [
            ("original", message, "align"),
            ("manipulated", alternate, "align"),
            ("repeated", message, "align"),
            ("ablated", None, "align"),
            ("inverted", message, "invert"),
        ]
        rng.shuffle(interventions)
        intervention_order.append(tuple(label for label, _, _ in interventions))
        actions = {label: receive(token, task) for label, token, task in interventions}
        original = actions["original"]
        manipulated = actions["manipulated"]
        repeated = actions["repeated"]
        ablated = actions["ablated"]
        inverted = actions["inverted"]
        correct += original == ep.factor
        ablated_correct += ablated == ep.factor
        flips += original != manipulated
        repeats += original == repeated
        inverted_correct += inverted == (ep.factor ^ 1)

    n = len(episodes)
    accuracy = correct / n
    ablation_drop = accuracy - ablated_correct / n
    flip_rate = flips / n
    consistency = repeats / n
    inversion = inverted_correct / n
    passed = (
        accuracy == 1.0 and ablation_drop >= 0.5 and flip_rate == 1.0
        and consistency == 1.0 and inversion == 1.0 and distinct_messages
    )
    return ProcessChannelScreen(
        # Even seemingly perfect external subprocesses can collude using host
        # files and clocks. The evaluator can never attest them as an oracle.
        status="COUNTERFACTUAL_UNQUALIFIED" if passed else "PROCESS_CONTROL_REJECTED",
        baseline_accuracy=accuracy,
        ablation_drop=ablation_drop,
        counterfactual_flip_rate=flip_rate if distinct_messages else None,
        repeat_consistency=consistency,
        inverted_task_accuracy=inversion,
        episodes=n,
        receiver_input_fields=("message", "task"),
        distinct_opposite_factor_messages=distinct_messages,
        numerical_gates_met=passed,
        intervention_order=tuple(intervention_order),
    )
