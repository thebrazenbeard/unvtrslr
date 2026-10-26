"""Known, trusted toy scripts exercise the process boundary—not a sandbox."""

import os
import sys
import time

import pytest

from unvtrslr.r2_controls import ControlEpisode
from unvtrslr.r2_process_probe import ProcessEndpoint, _ask, screen_process_channel


SCRIPT = '''
import json, os, pathlib, subprocess, sys, time
mode = sys.argv[1]
input_data = json.load(sys.stdin)
if mode.startswith("send"):
    assert set(input_data) == {"factor"}
    if mode == "send-collision":
        shared = pathlib.Path(sys.argv[2])
        n = int(shared.read_text()) if shared.exists() else 0
        shared.write_text(str(n + 1))
        print(json.dumps({"message": ("A", "B", "C", "C")[n]}))
        sys.exit()
    if mode == "send-collude":
        shared = pathlib.Path(sys.argv[2])
        state = json.loads(shared.read_text()) if shared.exists() else {"factors": [], "n": 0}
        state["factors"].append(input_data["factor"])
        shared.write_text(json.dumps(state))
        print(json.dumps({"message": "SAME_FOR_ALL_FACTORS"}))
        sys.exit()
    if mode == "send-leak":
        os.environ["UNVTRSLR_SENDER_FACTOR"] = str(input_data["factor"])
    print(json.dumps({"message": ("◇", "◈")[input_data["factor"]]}))
else:
    assert set(input_data) == {"message", "task"}
    if mode == "recv-collude":
        shared = pathlib.Path(sys.argv[2])
        state = json.loads(shared.read_text())
        factor = state["factors"][state["n"] // 5]
        position = state["n"] % 5
        state["n"] += 1
        shared.write_text(json.dumps(state))
        # Deliberately ignores message AND task; replays expected evaluator calls.
        action = (factor, 1-factor, factor, 1-factor, 1-factor)[position]
        print(json.dumps({"action": action}))
        sys.exit()
    if mode == "recv-constant":
        factor = 0
    elif mode == "recv-leak":
        factor = int(os.getenv("UNVTRSLR_SENDER_FACTOR", "0"))
    elif mode == "recv-sleep":
        time.sleep(1)
        factor = 0
    elif mode == "recv-descendant":
        shared = pathlib.Path(sys.argv[2])
        child = subprocess.Popen(
            [sys.executable, "-c", "import pathlib,sys,time; time.sleep(0.45); pathlib.Path(sys.argv[1]).write_text('escaped')", str(shared)],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
        factor = 0
    elif mode == "recv-return-with-descendant":
        shared = pathlib.Path(sys.argv[2])
        subprocess.Popen(
            [sys.executable, "-c", "import pathlib,sys,time; time.sleep(0.45); pathlib.Path(sys.argv[1]).write_text('escaped')", str(shared)],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        factor = 0
    elif mode == "recv-invalid":
        print(json.dumps({"action": True}))
        sys.exit()
    else:
        factor = 1 if input_data["message"] == "◈" else 0
    print(json.dumps({"action": factor ^ (input_data["task"] == "invert")}))
'''


@pytest.fixture
def executable(tmp_path):
    script = tmp_path / "trusted_toy_adapter.py"
    script.write_text(SCRIPT, encoding="utf-8")

    def build(mode):
        return ProcessEndpoint((sys.executable, str(script), mode))

    return build


@pytest.fixture
def episodes():
    return tuple(ControlEpisode(i % 2, f"hidden-{i}") for i in range(4))


def test_process_boundary_reference_positive_is_only_a_synthetic_smoke(executable, episodes):
    result = screen_process_channel(executable("send"), executable("recv"), episodes)
    assert result.status == "COUNTERFACTUAL_UNQUALIFIED"
    assert result.claim_ceiling == "UNQUALIFIED_SYNTHETIC_CHANNEL_DIAGNOSTIC"
    assert result.isolation_statement == "FRESH_PROCESSES_WITHOUT_OS_SANDBOX"
    assert result.numerical_gates_met is True
    assert result.distinct_opposite_factor_messages is True
    assert result.baseline_accuracy == 1.0
    assert result.ablation_drop == 0.5
    assert result.counterfactual_flip_rate == 1.0
    assert result.repeat_consistency == 1.0
    assert result.inverted_task_accuracy == 1.0
    assert result.receiver_input_fields == ("message", "task")
    assert len(result.intervention_order) == len(episodes)
    assert all(set(order) == {"original", "manipulated", "repeated", "ablated", "inverted"} for order in result.intervention_order)


def test_constant_receiver_does_not_pass_even_with_correlated_messages(executable, episodes):
    result = screen_process_channel(executable("send"), executable("recv-constant"), episodes)
    assert result.status == "PROCESS_CONTROL_REJECTED"
    assert result.baseline_accuracy == 0.5
    assert result.counterfactual_flip_rate == 0.0


def test_sender_process_environment_cannot_implicitly_transfer_truth(executable, episodes):
    result = screen_process_channel(executable("send-leak"), executable("recv-leak"), episodes)
    assert result.status == "PROCESS_CONTROL_REJECTED"
    assert result.counterfactual_flip_rate == 0.0


def test_shared_host_file_and_fixed_call_order_must_not_earn_positive_status(tmp_path, episodes):
    script = tmp_path / "colluding_adapter.py"
    script.write_text(SCRIPT, encoding="utf-8")
    shared = tmp_path / "undeclared_host_side_channel.json"
    sender = ProcessEndpoint((sys.executable, str(script), "send-collude", str(shared)))
    receiver = ProcessEndpoint((sys.executable, str(script), "recv-collude", str(shared)))
    result = screen_process_channel(sender, receiver, episodes)
    assert result.status == "PROCESS_CONTROL_REJECTED"
    assert result.distinct_opposite_factor_messages is False
    assert result.counterfactual_flip_rate is None
    assert result.numerical_gates_met is False


def test_any_cross_factor_message_collision_invalidates_distinctness(tmp_path, episodes):
    script = tmp_path / "colliding_adapter.py"
    script.write_text(SCRIPT, encoding="utf-8")
    counter = tmp_path / "sender_counter.txt"
    sender = ProcessEndpoint((sys.executable, str(script), "send-collision", str(counter)))
    receiver = ProcessEndpoint((sys.executable, str(script), "recv-constant"))
    result = screen_process_channel(sender, receiver, episodes)
    assert result.status == "PROCESS_CONTROL_REJECTED"
    assert result.distinct_opposite_factor_messages is False
    assert result.counterfactual_flip_rate is None


def test_fail_closed_on_timeout_and_invalid_binary_response(executable, episodes):
    with pytest.raises(ValueError, match="timed out"):
        screen_process_channel(
            executable("send"), executable("recv-sleep"), episodes,
            timeout_seconds=0.05,
        )
    with pytest.raises(ValueError, match="binary integer"):
        screen_process_channel(executable("send"), executable("recv-invalid"), episodes)


@pytest.mark.skipif(os.name != "posix", reason="POSIX process-group containment only")
def test_timeout_kills_endpoint_descendants_before_they_can_emit(tmp_path, executable, episodes):
    escaped_output = tmp_path / "late_descendant_output.txt"
    receiver = ProcessEndpoint((*executable("recv-descendant").argv, str(escaped_output)))
    with pytest.raises(ValueError, match="timed out"):
        screen_process_channel(executable("send"), receiver, episodes, timeout_seconds=0.15)
    # A bounded, benign child would write this file if the parent-only timeout
    # left it running. The original code reliably failed this test on POSIX.
    time.sleep(0.65)
    assert not escaped_output.exists(), "endpoint spawned process survived the timeout"


@pytest.mark.skipif(os.name != "posix", reason="POSIX process-group containment only")
def test_successful_endpoint_also_cleans_up_background_descendants(tmp_path, executable):
    escaped_output = tmp_path / "late_success_descendant.txt"
    receiver = ProcessEndpoint((*executable("recv-return-with-descendant").argv, str(escaped_output)))
    response = _ask(receiver, {"message": "◇", "task": "align"}, timeout_seconds=1, max_reply_bytes=4096)
    assert response == {"action": 0}
    time.sleep(0.65)
    assert not escaped_output.exists(), "successful endpoint left background process running"


def test_rejects_invalid_episode_batch_and_endpoint_commands(executable, episodes):
    with pytest.raises(ValueError, match="balance"):
        unbalanced = tuple(ControlEpisode(0, f"unbalanced-{i}") for i in range(4))
        screen_process_channel(executable("send"), executable("recv"), unbalanced)
    with pytest.raises(ValueError, match="argv"):
        ProcessEndpoint((sys.executable, ""))
