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

    with pytest.raises(ValueError, match="independent copies"):
        probe_controls(IdentityCloneLeak(), cases())


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
