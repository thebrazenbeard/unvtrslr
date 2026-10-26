"""Cross-process acoustic transport smoke controls, never grounding claims."""

import base64
import struct
import sys
import textwrap

import pytest

from unvtrslr.blind_causal_screen import (
    PrivateTrial,
    ReceiverView,
    freeze_evaluation,
    screen_frozen_holdout,
)
from unvtrslr.subprocess_blind_adapter import (
    SubprocessBlindReceiver,
    SubprocessBlindSender,
)


def _worker(script: str) -> tuple[str, ...]:
    # The test's own constant Python source is intentional. No shell is used.
    return (sys.executable, "-I", "-c", textwrap.dedent(script))


SENDER = """
    import base64, inspect, json, os, struct, sys
    view = json.load(sys.stdin)
    assert set(view) == {'schema', 'sample_rate_hz', 'shape', 'float64_le_b64'}
    assert view['shape'] == [1, 1]
    assert os.environ.get('UNV_PRIVATE_ANSWER_SENTINEL') is None
    assert not any('_SealedTrial' in str(type(obj))
        for frame in inspect.stack() for obj in frame.frame.f_locals.values())
    value = struct.unpack('<d', base64.b64decode(view['float64_le_b64']))[0]
    message = b'B' if value > 0 else b'A'
    json.dump({'schema': 'UNVTRSLR_SUBPROCESS_SENDER_RESPONSE_V1',
               'message_b64': base64.b64encode(message).decode('ascii')}, sys.stdout)
"""

RECEIVER = """
    import base64, json, sys
    view = json.load(sys.stdin)
    assert set(view) == {'schema', 'message_b64', 'available_actions'}
    assert view['available_actions'] == [0, 1]
    msg = base64.b64decode(view['message_b64']) if view['message_b64'] else None
    action = 1 if msg == b'B' else 0
    json.dump({'schema': 'UNVTRSLR_SUBPROCESS_RECEIVER_RESPONSE_V1',
               'action': action}, sys.stdout)
"""


def _observation(value: float) -> dict:
    return {
        "schema": "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1",
        "sample_rate_hz": 16000,
        "shape": [1, 1],
        "float64_le_b64": base64.b64encode(struct.pack("<d", value)).decode("ascii"),
    }


def test_cross_process_sender_and_receiver_hide_evaluator_frames(monkeypatch):
    monkeypatch.setenv("UNV_PRIVATE_ANSWER_SENTINEL", "private-test-answer")
    sender = SubprocessBlindSender(_worker(SENDER))
    receiver = SubprocessBlindReceiver(_worker(RECEIVER))
    train = [
        PrivateTrial("t-a", "train", _observation(-1), 0),
        PrivateTrial("t-b", "train", _observation(1), 1),
    ]
    held = [
        PrivateTrial(f"h-{i}", "held", _observation(x), 1 if x > 0 else 0)
        for i, x in enumerate((-0.5, 0.5, -0.75, 0.75))
    ]
    plan = freeze_evaluation(train, held, nonce=b"per-trial-private")
    result = screen_frozen_holdout(plan, sender, receiver)
    assert result.original_accuracy == 1.0
    assert result.absent_accuracy == 0.5
    assert result.shuffled_accuracy == 0.0
    assert result.replay_consistent is True
    assert result.state_isolation_verified is False
    assert result.causal_listening_qualified is False
    assert result.claim_ceiling == "IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED"


def test_reject_private_fields_before_launch():
    sender = SubprocessBlindSender(_worker("raise SystemExit(73)"))
    poisoned = _observation(0.2)
    poisoned["correct_action"] = 1
    with pytest.raises(ValueError, match="exactly"):
        sender(poisoned)


def test_reject_sender_response_with_extra_or_wrong_fields():
    sender = SubprocessBlindSender(_worker("""
        import json
        print(json.dumps({'schema':'UNVTRSLR_SUBPROCESS_SENDER_RESPONSE_V1',
             'message_b64':'QQ==','correct_action':1}))
    """))
    with pytest.raises(ValueError, match="exactly"):
        sender(_observation(0.5))

    duplicate = SubprocessBlindSender(_worker("""
        print('{"schema":"UNVTRSLR_SUBPROCESS_SENDER_RESPONSE_V1",'
              '"message_b64":"QQ==","message_b64":"Qg=="}')
    """))
    with pytest.raises(ValueError, match="duplicate worker JSON key"):
        duplicate(_observation(0.5))


def test_reject_receiver_bool_action_and_bad_input():
    receiver = SubprocessBlindReceiver(_worker("""
        import json
        print(json.dumps({'schema':'UNVTRSLR_SUBPROCESS_RECEIVER_RESPONSE_V1',
            'action':True}))
    """))
    with pytest.raises(ValueError, match="integer 0 or 1"):
        receiver(ReceiverView(b"B"))
    with pytest.raises(ValueError, match="ReceiverView"):
        receiver({"message": b"A"})


def test_nonzero_exit_timeout_and_bounded_response():
    failed = SubprocessBlindSender(_worker("raise SystemExit(19)"))
    with pytest.raises(ValueError, match="nonzero"):
        failed(_observation(0.1))

    hung = SubprocessBlindSender(_worker("import time; time.sleep(5)"), timeout_seconds=0.2)
    with pytest.raises(TimeoutError, match="timeout"):
        hung(_observation(0.1))

    noisy = SubprocessBlindSender(_worker("import sys; sys.stdout.write('x' * 100_000)"))
    with pytest.raises(ValueError, match="output limit"):
        noisy(_observation(0.1))


def test_command_and_timeout_validation():
    with pytest.raises(ValueError, match="absolute"):
        SubprocessBlindSender(("python", "-c", "print(1)"))
    with pytest.raises(ValueError, match="timeout"):
        SubprocessBlindSender((sys.executable,), timeout_seconds=float("inf"))
