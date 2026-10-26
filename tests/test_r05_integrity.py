"""Adversarial fixtures for the bounded R0.5 information-integrity checks."""

from hashlib import sha256

import pytest

from unvtrslr.r05_integrity import (
    ExposurePath,
    MatchedAblation,
    PreservationWitness,
    SemanticClaimEvidence,
    SourcePayloadPair,
    audit_exposure_paths,
    audit_executed_preprocessing,
    audit_matched_ablation,
    audit_preprocessing,
    audit_semantic_confirmation,
)


def test_ctrl_destructive_quotient_rejects_lost_target_distinction():
    witness = PreservationWitness(
        "source:left", "source:right", "same-token", "same-token", True
    )
    result = audit_preprocessing([witness])
    assert result.status == "PREPROCESSING_DESTRUCTIVE_QUOTIENT_DETECTED"
    assert result.counterexample_indices == (0,)


def test_irrelevant_information_loss_does_not_trigger_claim_relative_gate():
    irrelevant = PreservationWitness("s:a", "s:b", "x", "x", False)
    relevant = PreservationWitness("s:c", "s:d", "c", "d", True)
    assert audit_preprocessing([irrelevant, relevant]).status == (
        "NO_DESTRUCTIVE_QUOTIENT_WITNESSED_IN_SCOPE"
    )


def test_preprocessing_without_target_witness_remains_unknown():
    assert audit_preprocessing([]).status == "PREPROCESSING_PRESERVATION_UNKNOWN"
    only_irrelevant = [PreservationWitness("a", "b", "0", "0", False)]
    assert audit_preprocessing(only_irrelevant).status == "PREPROCESSING_PRESERVATION_UNKNOWN"


def test_ctrl_raw_scene_oracle_matched_bookkeeping_permutation():
    # Declared world and capture randomness are fixed; only evaluator bookkeeping changes.
    pair = MatchedAblation(
        world_left="physical-scene-1",
        world_right="physical-scene-1",
        capture_left="noise-1",
        capture_right="noise-1",
        adjudication_left="target:red",
        adjudication_right="target:blue",
        exposed_left="sound-A",
        exposed_right="sound-B",
    )
    assert audit_matched_ablation([pair]).status == "RAW_SCENE_ORACLE_DETECTED"


def test_matched_bookkeeping_change_without_visible_change_is_narrow_evidence():
    pair = MatchedAblation("world", "world", "seed", "seed", "label-A", "label-B", "same", "same")
    assert audit_matched_ablation([pair]).status == "NO_RAW_SCENE_ORACLE_WITNESSED_IN_SCOPE"


def test_unmatched_or_undifferentiated_ablation_cannot_claim_a_pass():
    pairs = [MatchedAblation("world", "world", "seed", None, "A", "B", "left", "right")]
    assert audit_matched_ablation(pairs).status == "GENERATIVE_PROVENANCE_UNVERIFIED"
    assert audit_matched_ablation([]).status == "GENERATIVE_PROVENANCE_UNVERIFIED"


def test_unmatched_world_or_capture_is_not_false_oracle_evidence():
    pairs = [MatchedAblation("world-a", "world-b", "seed", "seed", "A", "B", "left", "right")]
    assert audit_matched_ablation(pairs).status == "GENERATIVE_PROVENANCE_UNVERIFIED"


def test_ctrl_global_state_watermark_detected_even_without_target_partition():
    route = ExposurePath(
        origin="SIMULATOR_LATENT",
        path=("instrumentation", "audio-renderer", "learner-exposure"),
        learner_visible=True,
        declared_world_process=False,
    )
    assert audit_exposure_paths([route]).status == "FORBIDDEN_LEARNER_EXPOSURE_PATH_DETECTED"


def test_declared_physical_world_path_does_not_alone_prove_integrity():
    route = ExposurePath(
        origin="SIMULATOR_LATENT",
        path=("world-dynamics", "physical-wave", "learner-exposure"),
        learner_visible=True,
        declared_world_process=True,
    )
    assert audit_exposure_paths([route]).status == "GENERATIVE_PROVENANCE_UNVERIFIED"


def test_ctrl_posthoc_semantic_naming_fails_closed_despite_fresh_iid_holdout():
    evidence = SemanticClaimEvidence(
        target_frozen_before_candidate=False,
        rival_family_frozen_before_candidate=False,
        new_evidence_ids=("holdout-new",),
        claim_discriminating_against_structured_rivals=False,
        selection_evidence_ids=("selection-old",),
    )
    result = audit_semantic_confirmation(evidence)
    assert result.hypothesis_status == "EXPLORATORY_POST_HOC_INTERPRETATION"
    assert result.holdout_status == "FRESH_BUT_NONDISCRIMINATING_EVIDENCE"
    assert result.claim_ceiling == "SEMANTIC_INTERPRETATION_STILL_CONFOUNDED"


def test_discriminating_evidence_cannot_retroactively_freeze_selected_claim():
    evidence = SemanticClaimEvidence(False, False, ("shift-1",), True, ("selection-old",))
    result = audit_semantic_confirmation(evidence)
    assert result.hypothesis_status == "EXPLORATORY_POST_HOC_INTERPRETATION"
    assert result.claim_ceiling == "SEMANTIC_INTERPRETATION_STILL_CONFOUNDED"


def test_frozen_claim_and_discriminating_holdout_without_result_are_not_supported():
    evidence = SemanticClaimEvidence(True, True, ("shift-1",), True)
    result = audit_semantic_confirmation(evidence)
    assert result.hypothesis_status == "CONFIRMATORY_TARGET_CLAIM"
    assert result.holdout_status == "CLAIM_DISCRIMINATING_HOLDOUT"
    assert result.claim_ceiling == "SEMANTIC_CONFIRMATION_NOT_ESTABLISHED"


def test_explicit_pass_on_frozen_discriminating_holdout_only_earns_scoped_support():
    evidence = SemanticClaimEvidence(
        True, True, ("shift-1",), True, holdout_result="SUPPORTED"
    )
    assert audit_semantic_confirmation(evidence).claim_ceiling == (
        "SUPPORTED_AMONG_DECLARED_RIVALS_WITHIN_TESTED_SCOPE"
    )


def test_posthoc_interpretation_may_be_retested_after_a_second_freeze():
    evidence = SemanticClaimEvidence(
        False, False, ("shift-new",), True, ("selection-old",),
        interpretation_frozen_before_holdout=True,
        rivals_frozen_before_holdout=True,
        holdout_result="SUPPORTED",
    )
    result = audit_semantic_confirmation(evidence)
    assert result.hypothesis_status == "POST_HOC_INTERPRETATION_RETESTED"
    assert result.claim_ceiling == "SUPPORTED_AMONG_DECLARED_RIVALS_WITHIN_TESTED_SCOPE"


def test_falsifying_discriminating_holdout_cannot_be_promoted_to_support():
    evidence = SemanticClaimEvidence(
        True, True, ("shift-new",), True, holdout_result="FALSIFIED"
    )
    assert audit_semantic_confirmation(evidence).claim_ceiling == (
        "SEMANTIC_INTERPRETATION_NOT_SUPPORTED_IN_TESTED_SCOPE"
    )


def test_empty_holdout_never_earns_confirmation():
    evidence = SemanticClaimEvidence(True, True, (), True)
    assert audit_semantic_confirmation(evidence).holdout_status == "NO_FRESH_EVIDENCE"


def test_posthoc_claim_with_unknown_selection_evidence_cannot_prove_freshness():
    evidence = SemanticClaimEvidence(False, False, ("claim-evidence",), True)
    assert audit_semantic_confirmation(evidence).holdout_status == "FRESHNESS_UNVERIFIED"


def test_reused_selection_evidence_is_not_fresh():
    evidence = SemanticClaimEvidence(False, False, ("old", "new"), True, ("old",))
    assert audit_semantic_confirmation(evidence).holdout_status == "NO_FRESH_EVIDENCE"


def test_executed_transform_exposes_metadata_laundered_destructive_quotient():
    """Caller-supplied transformed IDs can disagree with executable behavior."""
    misleading = PreservationWitness("raw-left", "raw-right", "output-A", "output-B", True)
    assert audit_preprocessing([misleading]).status == "NO_DESTRUCTIVE_QUOTIENT_WITNESSED_IN_SCOPE"

    left, right = b"pitch=high", b"pitch=low"
    result = audit_executed_preprocessing(
        [SourcePayloadPair(left, right, True)], lambda raw: raw.split(b"=")[0]
    )
    assert result.disposition.status == "PREPROCESSING_DESTRUCTIVE_QUOTIENT_DETECTED"
    assert result.disposition.counterexample_indices == (0,)
    assert result.receipts[0].source_left_sha256 == sha256(left).hexdigest()
    assert result.receipts[0].source_right_sha256 == sha256(right).hexdigest()
    assert result.receipts[0].output_left_sha256 == sha256(b"pitch").hexdigest()
    assert result.receipts[0].output_left_sha256 == result.receipts[0].output_right_sha256
    assert result.receipts[0].replay_stable is True


def test_executed_preprocessing_identity_is_only_scoped_narrow_evidence():
    result = audit_executed_preprocessing(
        [SourcePayloadPair(b"signal-A", b"signal-B", True)], lambda raw: raw
    )
    assert result.disposition.status == "NO_DESTRUCTIVE_QUOTIENT_WITNESSED_IN_SCOPE"
    assert result.receipts[0].source_left_sha256 == result.receipts[0].output_left_sha256
    assert result.receipts[0].replay_stable is True


def test_executed_preprocessing_unstable_replay_never_claims_preservation():
    counter = iter(range(8))

    def nondeterministic(_raw: bytes) -> bytes:
        return bytes([next(counter)])

    result = audit_executed_preprocessing(
        [SourcePayloadPair(b"A", b"B", True)], nondeterministic
    )
    assert result.disposition.status == "PREPROCESSING_REPLAY_UNSTABLE"
    assert result.disposition.counterexample_indices == (0,)
    assert result.receipts[0].replay_stable is False


def test_executed_preprocessing_detects_call_order_only_false_preservation():
    """An alternating callback cannot masquerade as two distinguished outputs.

    With left/right/left/right invocation, an input-ignorant two-state clock
    gives apparently stable different outputs and the old gate incorrectly
    claims no witnessed destructive quotient. Reverse the replay order to
    expose this scheduling confound before recording narrow preservation.
    """
    calls = 0

    def alternating(_raw: bytes) -> bytes:
        nonlocal calls
        calls += 1
        return b"even" if calls % 2 == 0 else b"odd"

    result = audit_executed_preprocessing(
        [SourcePayloadPair(b"meaning-A", b"meaning-B", True)], alternating
    )
    assert result.disposition.status == "PREPROCESSING_REPLAY_UNSTABLE"
    assert result.disposition.counterexample_indices == (0,)
    assert result.receipts[0].replay_stable is False


def test_executed_preprocessing_detects_four_period_call_order_spoofing():
    """Reversed replay alone is fooled by A,B,B,A cycling outputs.

    The callback ignores its input completely. L,R,R,L produces stable
    distinct apparent outputs, yet another same-input replay in a different
    invocation position proves the outputs are schedule-conditioned.
    """
    cycle = (b"A", b"B", b"B", b"A")
    calls = 0

    def four_period(_raw: bytes) -> bytes:
        nonlocal calls
        output = cycle[calls % len(cycle)]
        calls += 1
        return output

    result = audit_executed_preprocessing(
        [SourcePayloadPair(b"source-left", b"source-right", True)], four_period
    )
    assert result.disposition.status == "PREPROCESSING_REPLAY_UNSTABLE"
    assert result.disposition.counterexample_indices == (0,)
    assert result.receipts[0].replay_stable is False


def test_executed_preprocessing_empty_or_irrelevant_witnesses_remain_unknown():
    assert audit_executed_preprocessing([], bytes).disposition.status == (
        "PREPROCESSING_PRESERVATION_UNKNOWN"
    )
    irrelevant = [SourcePayloadPair(b"A", b"B", False)]
    assert audit_executed_preprocessing(irrelevant, bytes).disposition.status == (
        "PREPROCESSING_PRESERVATION_UNKNOWN"
    )


def test_executed_preprocessing_rejects_invalid_payloads_and_results():
    with pytest.raises(ValueError, match="must differ"):
        audit_executed_preprocessing([SourcePayloadPair(b"A", b"A", True)], bytes)
    with pytest.raises(TypeError, match="source payload"):
        audit_executed_preprocessing([SourcePayloadPair("A", b"B", True)], bytes)
    with pytest.raises(TypeError, match="target_distinguishable"):
        audit_executed_preprocessing([SourcePayloadPair(b"A", b"B", "false")], bytes)
    with pytest.raises(TypeError, match="preprocessor output"):
        audit_executed_preprocessing([SourcePayloadPair(b"A", b"B", True)], lambda _raw: "x")
