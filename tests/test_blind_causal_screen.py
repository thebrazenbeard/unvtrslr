"""Synthetic evaluator controls are diagnostics, not grounding certificates."""

import base64
import inspect
import struct

import pytest

import unvtrslr.blind_causal_screen as screen_module
from unvtrslr.blind_causal_screen import (
    PrivateTrial,
    ReceiverView,
    freeze_evaluation,
    screen_frozen_holdout,
)


def observation(value: float) -> dict:
    return {
        "schema": "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1",
        "sample_rate_hz": 16000,
        "shape": [1, 1],
        "float64_le_b64": base64.b64encode(struct.pack("<d", value)).decode("ascii"),
    }


def trials():
    train = (
        PrivateTrial("train-a", "train-source", observation(-1.0), 0),
        PrivateTrial("train-b", "train-source", observation(1.0), 1),
    )
    holdout = (
        PrivateTrial("hold-0", "holdout-source", observation(-0.4), 0),
        PrivateTrial("hold-1", "holdout-source", observation(0.4), 1),
        PrivateTrial("hold-2", "holdout-source", observation(-0.7), 0),
        PrivateTrial("hold-3", "holdout-source", observation(0.7), 1),
    )
    return train, holdout


def sender(public_view):
    assert set(public_view) == {
        "schema", "sample_rate_hz", "shape", "float64_le_b64"
    }
    raw = base64.b64decode(public_view["float64_le_b64"])
    value = struct.unpack("<d", raw)[0]
    return b"a" if value < 0.0 else b"b"


def receiver(view: ReceiverView):
    assert set(vars(view)) == {"message", "available_actions"}
    assert view.available_actions == (0, 1)
    return 1 if view.message == b"b" else 0


def test_private_truth_and_identifiers_never_enter_learner_callback():
    train, holdout = trials()
    plan = freeze_evaluation(train, holdout, nonce=b"1234567890123456")
    received_sender = []

    def observed_sender(view):
        received_sender.append(view)
        return sender(view)

    result = screen_frozen_holdout(plan, observed_sender, receiver,
                                   partner_receiver=lambda _: 0,
                                   shuffle_offset=1)
    assert result.claim_ceiling == "IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED"
    assert result.holdout_count == 4
    assert result.original_accuracy == 1.0
    assert result.absent_accuracy == 0.5
    assert result.shuffled_accuracy == 0.0
    assert result.partner_accuracy == 0.5
    assert result.replay_consistent is True
    assert result.message_shuffle_changes_payload is True
    assert result.causal_listening_qualified is False
    assert len(received_sender) >= len(holdout)
    assert all(set(view) == set(observation(0.0)) for view in received_sender)


def test_input_observation_mutation_after_freeze_does_not_change_holdout():
    train, holdout = trials()
    mutable = observation(-0.4)
    holdout = (PrivateTrial("hold-0", "held", mutable, 0), *holdout[1:])
    plan = freeze_evaluation(train, holdout, nonce=b"1234567890123456")
    original = mutable["float64_le_b64"]
    mutable["float64_le_b64"] = observation(1.0)["float64_le_b64"]
    seen = []

    def inspect(view):
        seen.append(view["float64_le_b64"])
        return sender(view)

    result = screen_frozen_holdout(plan, inspect, receiver, shuffle_offset=1)
    assert result.original_accuracy == 1.0
    assert seen[0] == original


@pytest.mark.parametrize("hidden", ["translation", "target_action", "trial_id", "seed", "recording_id"])
def test_rejects_hidden_answer_or_metadata_in_public_audio_payload(hidden):
    train, holdout = trials()
    poisoned = observation(-1.0)
    poisoned[hidden] = "private"
    train = (PrivateTrial("train-a", "train-source", poisoned, 0), *train[1:])
    with pytest.raises(ValueError, match="exactly"):
        freeze_evaluation(train, holdout)


def test_holdout_split_is_sealed_against_group_and_trial_reuse():
    train, holdout = trials()
    with pytest.raises(ValueError, match="group"):
        freeze_evaluation(train, (PrivateTrial("fresh", "train-source", observation(-1), 0), *holdout))
    with pytest.raises(ValueError, match="trial_id"):
        freeze_evaluation(train, (PrivateTrial("train-a", "held", observation(-1), 0), *holdout))


def test_exact_training_audio_cannot_be_replayed_as_heldout_generalization():
    train, _ = trials()
    holdout = (
        PrivateTrial("held-a", "unseen-group", observation(-1.0), 0),
        PrivateTrial("held-b", "unseen-group", observation(1.0), 1),
    )
    # Different trial/group labels cannot hide identical raw PCM payloads.
    with pytest.raises(ValueError, match="observation overlap"):
        freeze_evaluation(train, holdout)


def test_near_duplicate_waveforms_can_fake_holdout_transfer_without_qualification():
    # Exact-byte separation is insufficient: an arbitrarily tiny amplitude
    # perturbation gives fresh bytes while preserving a trivial nuisance cue.
    # This is an explicitly ADMITTED negative control, not a claimed fix.
    train = (
        PrivateTrial("train-low", "train-recording", observation(0.1), 0),
        PrivateTrial("train-high", "train-recording", observation(0.9), 1),
    )
    holdout = tuple(
        PrivateTrial(f"held-{i}", "claimed-independent-recording",
                     observation(amplitude), action)
        for i, (amplitude, action) in enumerate((
            (0.10001, 0), (0.90001, 1),
            (0.10002, 0), (0.90002, 1),
        ))
    )
    assert {r.observation_payload["float64_le_b64"] for r in train}.isdisjoint(
        {r.observation_payload["float64_le_b64"] for r in holdout}
    )
    plan = freeze_evaluation(train, holdout, nonce=b"near-duplicates!!")

    def nuisance_threshold_sender(view):
        (amplitude,) = struct.unpack(
            "<d", base64.b64decode(view["float64_le_b64"])
        )
        return b"high" if amplitude > 0.5 else b"low"

    def nuisance_receiver(view):
        return int(view.message == b"high")

    result = screen_frozen_holdout(plan, nuisance_threshold_sender,
                                   nuisance_receiver)
    assert result.original_accuracy == 1.0
    assert result.absent_accuracy == 0.5
    assert result.shuffled_accuracy == 0.0
    assert result.replay_consistent is True
    assert result.message_shuffle_changes_payload is True
    assert result.state_isolation_verified is False
    assert result.causal_listening_qualified is False
    assert result.claim_ceiling == "IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED"


def test_strict_adapter_outputs_and_stateful_replay_detection():
    plan = freeze_evaluation(*trials())
    with pytest.raises(ValueError, match="sender message"):
        screen_frozen_holdout(plan, lambda _: "a", receiver)
    with pytest.raises(ValueError, match="receiver action"):
        screen_frozen_holdout(plan, sender, lambda _: True)

    counter = 0

    def stateful_receiver(view):
        nonlocal counter
        counter += 1
        if counter > 4:
            return 1 - receiver(view)
        return receiver(view)

    result = screen_frozen_holdout(plan, sender, stateful_receiver)
    assert result.replay_consistent is False
    assert result.claim_ceiling == "IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED"


def test_rejects_metadata_only_label_shortcut_from_rate_or_shape():
    train, _ = trials()
    # Identical silence for each class: only rate or shape reveals the answer.
    holdout = (
        PrivateTrial("a", "held", observation(0.0), 0),
        PrivateTrial("b", "held", {**observation(0.0), "sample_rate_hz": 8000}, 1),
        PrivateTrial("c", "held", observation(0.0), 0),
        PrivateTrial("d", "held", {**observation(0.0), "sample_rate_hz": 8000}, 1),
    )
    with pytest.raises(ValueError, match="metadata"):
        freeze_evaluation(train, holdout)

    altered = observation(0.0)
    altered["shape"] = [2, 1]
    altered["float64_le_b64"] = base64.b64encode(struct.pack("<dd", 0, 0)).decode("ascii")
    holdout = (
        PrivateTrial("a", "held", observation(0.0), 0),
        PrivateTrial("b", "held", altered, 1),
        PrivateTrial("c", "held", observation(0.0), 0),
        PrivateTrial("d", "held", altered, 1),
    )
    with pytest.raises(ValueError, match="metadata"):
        freeze_evaluation(train, holdout)


def test_predecode_length_validation_blocks_oversized_base64(monkeypatch):
    train, holdout = trials()
    poisoned = observation(1.0)
    poisoned["float64_le_b64"] = "A" * 100_000
    train = (PrivateTrial("train-a", "train-source", poisoned, 0), *train[1:])

    def never_decode(*_args, **_kwargs):
        raise AssertionError("unbounded base64 was decoded before checking length")

    monkeypatch.setattr(screen_module.base64, "b64decode", never_decode)
    with pytest.raises(ValueError, match="encoded length"):
        freeze_evaluation(train, holdout)


@pytest.mark.parametrize("mutation,match", [
    ({"sample_rate_hz": 2**31}, "sample_rate_hz"),
    ({"shape": [1, 65]}, "shape"),
    ({"shape": [262145, 1]}, "shape"),
])
def test_matches_bridge_numeric_limits(mutation, match):
    train, holdout = trials()
    poisoned = {**observation(0.0), **mutation}
    train = (PrivateTrial("train-a", "train-source", poisoned, 0), *train[1:])
    with pytest.raises(ValueError, match=match):
        freeze_evaluation(train, holdout)


def test_rejects_finite_but_unsupported_sample_amplitude():
    train, holdout = trials()
    train = (PrivateTrial("train-a", "train-source", observation(1e101), 0), *train[1:])
    with pytest.raises(ValueError, match="amplitude"):
        freeze_evaluation(train, holdout)


def test_constant_messages_cannot_be_reported_as_adequate_shuffle_intervention():
    train, holdout = trials()
    # All raw observations are identical, and only private evaluator labels
    # differ. A sham receiver exploits fixed phase/call order, not messages.
    holdout = tuple(
        PrivateTrial(r.trial_id, r.group_id, observation(0.0), r.correct_action)
        for r in holdout
    )
    plan = freeze_evaluation(train, holdout)
    calls = 0

    def phase_spoofer(_view):
        nonlocal calls
        phase, idx = divmod(calls, 4)
        calls += 1
        if phase in (0, 1):
            return idx % 2  # original/replay appear perfect without messages
        if phase == 2:
            return 0  # absent appears to reduce performance
        return 1 - idx % 2  # shuffled appears maximally disruptive

    result = screen_frozen_holdout(plan, lambda _: b"CONSTANT", phase_spoofer)
    assert result.original_accuracy == 1.0
    assert result.absent_accuracy == 0.5
    assert result.replay_consistent is True
    assert result.message_shuffle_changes_payload is False
    assert result.causal_listening_qualified is False
    assert result.shuffled_accuracy is None


def test_distinct_messages_and_good_metrics_do_not_certify_causal_listening():
    # Four genuinely different bytes, yet a receiver ignoring ALL of them
    # can spoof every phase because callback order is deterministic.
    plan = freeze_evaluation(*trials())
    calls = 0

    def phase_spoofer(_view):
        nonlocal calls
        phase, index = divmod(calls, 4)
        calls += 1
        if phase in (0, 1):
            return index % 2
        if phase == 2:
            return 0
        return 1 - index % 2

    def nonsemantic_sender(view):
        return base64.b64decode(view["float64_le_b64"])

    result = screen_frozen_holdout(plan, nonsemantic_sender, phase_spoofer)
    assert result.original_accuracy == 1.0
    assert result.absent_accuracy == 0.5
    assert result.shuffled_accuracy == 0.0
    assert result.replay_consistent is True
    assert result.message_shuffle_changes_payload is True
    assert result.causal_listening_qualified is False


def test_in_process_sender_can_read_sealed_answers_from_python_stack():
    # A four-key callback argument is NOT an isolation boundary. The trusted
    # evaluator's comprehension frame still holds the sealed trial object.
    # This test intentionally documents a reproducible oracle, not behavior
    # that is acceptable for a qualified learner.
    plan = freeze_evaluation(*trials())
    recovered_actions = []

    def oracle_sender(view):
        assert set(view) == set(observation(0.0))
        for info in inspect.stack():
            trial = info.frame.f_locals.get("r")
            if isinstance(trial, screen_module._SealedTrial):
                recovered_actions.append(trial.correct_action)
                return b"B" if trial.correct_action == 1 else b"A"
        raise AssertionError("evaluator trial frame unexpectedly inaccessible")

    def oracle_receiver(view):
        return int(view.message == b"B") if view.message is not None else 0

    result = screen_frozen_holdout(plan, oracle_sender, oracle_receiver)
    assert recovered_actions == [0, 1, 0, 1] * 2
    assert result.original_accuracy == 1.0
    assert result.absent_accuracy == 0.5
    assert result.shuffled_accuracy == 0.0
    assert result.replay_consistent is True
    assert result.message_shuffle_changes_payload is True
    assert result.state_isolation_verified is False
    assert result.causal_listening_qualified is False
    assert result.claim_ceiling == "IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED"
