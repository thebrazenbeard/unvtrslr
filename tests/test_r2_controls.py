"""R2 control smoke checks; do not claim learned grounding from these."""

from dataclasses import asdict

import pytest

from unvtrslr.r2_controls import (
    ActionPlanCode,
    AlternatingReceiverLeak,
    ControlEpisode,
    EpisodeIdCode,
    GroundedConventionOracle,
    ReceiverObservation,
    SenderObservation,
    SharedSenderStateLeak,
    SilentCompetentReceiver,
    probe_controls,
)


def cases(*, receiver_hint: bool = False) -> tuple[ControlEpisode, ...]:
    return tuple(
        ControlEpisode(i % 2, f"train:{i}", receiver_hint=i % 2 if receiver_hint else None)
        for i in range(10)
    )


def test_arbitrary_symbol_oracle_passes_all_toy_gates():
    for symbols in (("◈", "◇"), ("◇", "◈"), ("blue", "omega")):
        result = probe_controls(GroundedConventionOracle(symbols), cases())
        assert result.status == "TOY_CONTROLS_PASSED"
        assert result.iid_accuracy == 1.0
        assert result.causal_listening == 1.0
        assert result.message_ablation_drop == 0.5
        assert result.cross_task_accuracy == 1.0
        assert result.episode_id_shift_accuracy == 1.0


def test_action_plan_shortcut_fools_iid_and_causal_listening_but_fails_transfer():
    result = probe_controls(ActionPlanCode(), cases())
    assert result.iid_accuracy == 1.0
    assert result.causal_listening == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.cross_task_accuracy == 0.0
    assert result.status == "CONTROL_REJECTED"


def test_episode_id_shortcut_fools_iid_but_fails_id_regeneration():
    train = cases()
    result = probe_controls(EpisodeIdCode(train), train)
    assert result.iid_accuracy == 1.0
    assert result.causal_listening == 1.0
    assert result.cross_task_accuracy == 1.0
    assert result.episode_id_shift_accuracy == 0.5
    assert result.status == "CONTROL_REJECTED"


def test_holdout_episode_ids_never_collide_with_declared_training_ids():
    train = (
        ControlEpisode(0, "__r2_holdout__:0"),
        ControlEpisode(1, "__r2_holdout__:1"),
    )
    result = probe_controls(EpisodeIdCode(train), train)
    assert result.iid_accuracy == 1.0
    assert result.episode_id_shift_accuracy == 0.5


def test_competent_receiver_with_private_cue_has_no_communication_causality():
    result = probe_controls(SilentCompetentReceiver(), cases(receiver_hint=True))
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.0
    assert result.causal_listening == 0.0
    assert result.status == "CONTROL_REJECTED"


def test_shared_sender_state_cannot_masquerade_as_message_causality():
    agent = SharedSenderStateLeak()
    assert agent.send(SenderObservation(1, "sample")) == "sign-B"
    assert agent.receive(None, ReceiverObservation("align", "sample")) == 1
    result = probe_controls(SharedSenderStateLeak(), cases())
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.causal_listening == 0.0
    assert result.status == "CONTROL_REJECTED"


def test_receiver_call_order_cannot_masquerade_as_counterfactual_sensitivity():
    result = probe_controls(AlternatingReceiverLeak(), cases())
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.causal_listening == 0.0
    assert result.status == "CONTROL_REJECTED"


def test_counterfactual_rejects_identity_clone_with_shared_mutable_state():
    class IdentityCloneLeak(SharedSenderStateLeak):
        def __deepcopy__(self, memo: dict[int, object]) -> "IdentityCloneLeak":
            return self

    result = probe_controls(IdentityCloneLeak(), cases())
    assert result.causal_listening is None
    assert result.status == "COUNTERFACTUAL_UNQUALIFIED"


def test_counterfactual_rejects_nonexchangeable_snapshot_faking_message_effect():
    class CloneOrdinalLeak:
        """No message is ever read; clone creation order fakes interventions."""

        def __init__(self):
            self._sender_latent = 0
            self._clone_count = 0
            self._snapshot_output = None

        def send(self, observation: SenderObservation) -> str:
            self._sender_latent = observation.factor
            return ("observed-A", "observed-B")[observation.factor]

        def receive(self, message: str | None, observation: ReceiverObservation) -> int:
            del message
            factor = (
                self._sender_latent
                if self._snapshot_output is None
                else self._snapshot_output
            )
            return factor ^ (observation.task == "invert")

        def __deepcopy__(self, memo):
            del memo
            self._clone_count += 1
            clone = type(self)()
            clone._snapshot_output = self._clone_count % 2
            return clone

    result = probe_controls(CloneOrdinalLeak(), cases())
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.causal_listening is None
    assert result.status == "COUNTERFACTUAL_UNQUALIFIED"


def test_counterfactual_rejects_class_shared_receive_call_counter():
    class ClassWideCounterLeak:
        """Default deepcopy still shares process-level class state."""

        _original = None
        _receiver_calls = 0

        def __init__(self):
            self._factor = 0
            type(self)._original = self

        def send(self, observation: SenderObservation) -> str:
            self._factor = observation.factor
            return ("sign-A", "sign-B")[observation.factor]

        def receive(self, message: str | None, observation: ReceiverObservation) -> int:
            del message
            if self is type(self)._original:
                factor = self._factor
            else:
                factor = type(self)._receiver_calls % 2
                type(self)._receiver_calls += 1
            return factor ^ (observation.task == "invert")

    result = probe_controls(ClassWideCounterLeak(), cases())
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.causal_listening is None
    assert result.status == "COUNTERFACTUAL_UNQUALIFIED"


def test_four_slot_clone_side_effect_is_harness_invalid_not_message_evidence():
    class FourSlotLeak:
        """Copy hooks can mimic the entire fixed sham/intervention schedule."""

        def __init__(self):
            self.latent = 0
            self.counter = 0
            self.fixed = None

        def send(self, observation: SenderObservation) -> str:
            self.latent = observation.factor
            return ("A", "B")[observation.factor]

        def receive(self, message: str | None, observation: ReceiverObservation) -> int:
            del message
            return (self.latent if self.fixed is None else self.fixed) ^ (observation.task == "invert")

        def __deepcopy__(self, memo):
            del memo
            self.counter += 1
            clone = type(self)()
            clone.fixed = (0, 1, 1, 0)[(self.counter - 1) % 4]
            return clone

    episodes = tuple(ControlEpisode(i % 2, f"case-{i}") for i in range(4))
    # Previous four-sham schedule returned TOY_CONTROLS_PASSED although the
    # receiver ignored every message. A private deepcopy hook is not a
    # trustworthy mechanism for freezing a receiver's state.
    result = probe_controls(FourSlotLeak(), episodes)
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.causal_listening is None
    assert result.status == "COUNTERFACTUAL_UNQUALIFIED"


def test_global_clock_leak_without_copy_hooks_cannot_qualify_unknown_agent():
    class GlobalClockLeak:
        """Default deepcopy leaves a shared class clock; messages are ignored."""

        _owner = None
        _receiver_calls = 0

        def __init__(self):
            self._latent = 0
            type(self)._owner = self

        def send(self, observation: SenderObservation) -> str:
            self._latent = observation.factor
            return ("sign-A", "sign-B")[observation.factor]

        def receive(self, message: str | None, observation: ReceiverObservation) -> int:
            del message
            if self is type(self)._owner:
                factor = self._latent
            else:
                factor = (0, 1, 1, 0)[type(self)._receiver_calls % 4]
                type(self)._receiver_calls += 1
            return factor ^ (observation.task == "invert")

    episodes = tuple(ControlEpisode(i % 2, f"case-{i}") for i in range(4))
    result = probe_controls(GlobalClockLeak(), episodes)
    assert result.iid_accuracy == 1.0
    assert result.message_ablation_drop == 0.5
    assert result.episode_id_shift_accuracy == 1.0
    assert result.cross_task_accuracy == 1.0
    # All apparent metric success on an arbitrary candidate class cannot be
    # promoted by a finite in-process schedule, even without custom hooks.
    assert result.causal_listening is None
    assert result.status == "COUNTERFACTUAL_UNQUALIFIED"


def test_harness_rejects_unbalanced_or_duplicate_id_input():
    with pytest.raises(ValueError, match="balanced"):
        probe_controls(GroundedConventionOracle(), (ControlEpisode(0, "a"), ControlEpisode(0, "b")))
    with pytest.raises(ValueError, match="unique"):
        probe_controls(GroundedConventionOracle(), (ControlEpisode(0, "a"), ControlEpisode(1, "a")))


def test_no_grounding_certificate_status_can_be_emitted():
    result = asdict(probe_controls(GroundedConventionOracle(), cases()))
    assert set(result) == {
        "iid_accuracy", "message_ablation_drop", "causal_listening",
        "episode_id_shift_accuracy", "cross_task_accuracy", "status",
    }
    assert result["status"] == "TOY_CONTROLS_PASSED"


def test_evaluator_truth_is_not_passed_to_receiver():
    class OracleLeakAttempt(GroundedConventionOracle):
        def receive(self, message: str | None, observation: ReceiverObservation) -> int:
            # A naive harness that hands the full ControlEpisode to receive()
            # would let a receiver solve the task by inspecting evaluator truth.
            return observation.factor  # type: ignore[attr-defined]

    with pytest.raises(AttributeError, match="factor"):
        probe_controls(OracleLeakAttempt(), cases())
