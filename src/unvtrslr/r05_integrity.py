"""Bounded R0.5 integrity falsifiers, not a semantic-qualification harness.

These audits operate on *auditor-supplied* paired observations and provenance
declarations. A detected counterexample is useful negative evidence. Failure to
detect one is only a result within the submitted witness set; it is not proof
that a renderer, mediator, or generative process is uncontaminated.

All inputs are evaluator-side. No adjudication labels should be sent into a
learner's features, rewards, prompts, or training examples by these checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Callable, Iterable


@dataclass(frozen=True)
class AuditDisposition:
    status: str
    counterexample_indices: tuple[int, ...] = ()


@dataclass(frozen=True)
class PreservationWitness:
    """Claim-relative pair: raw learner-accessible history -> transformed input.

    ``target_distinguishable`` is an externally established comparison of the
    rival hypotheses on these source histories, never a semantic label inferred
    from the transformed output. Pair identifiers should be opaque digests or
    stable references, with original evidence retained elsewhere.
    """

    source_left: str
    source_right: str
    transformed_left: str
    transformed_right: str
    target_distinguishable: bool


def audit_preprocessing(witnesses: Iterable[PreservationWitness]) -> AuditDisposition:
    """Falsify preservation if a witnessed target distinction is quotiented out.

    The absence of a counterexample cannot establish preservation for untested
    histories or unavailable source information.
    """

    counterexamples: list[int] = []
    tested_relevant = False
    for index, witness in enumerate(witnesses):
        if not witness.target_distinguishable:
            continue
        if witness.source_left == witness.source_right:
            raise ValueError("a target-distinguishing pair must differ at the source")
        tested_relevant = True
        if witness.transformed_left == witness.transformed_right:
            counterexamples.append(index)

    if counterexamples:
        return AuditDisposition(
            "PREPROCESSING_DESTRUCTIVE_QUOTIENT_DETECTED", tuple(counterexamples)
        )
    if tested_relevant:
        return AuditDisposition("NO_DESTRUCTIVE_QUOTIENT_WITNESSED_IN_SCOPE")
    return AuditDisposition("PREPROCESSING_PRESERVATION_UNKNOWN")


@dataclass(frozen=True)
class SourcePayloadPair:
    """Raw *supplied* learner-accessible payloads and an external rival contrast.

    A payload should include the complete source history relevant to the claim,
    not only a selected acoustic frame. This type does not authenticate capture
    provenance or verify ``target_distinguishable``; both remain external.
    """

    source_left: bytes
    source_right: bytes
    target_distinguishable: bool


@dataclass(frozen=True)
class ExecutedPreprocessingReceipt:
    """Digests calculated from the actual inputs and a preprocessor's results.

    The digests bind *this execution*, not the deployed preprocessor version,
    source capture, or any hidden ambient state the callback may consult.
    """

    source_left_sha256: str
    source_right_sha256: str
    output_left_sha256: str
    output_right_sha256: str
    replay_stable: bool


@dataclass(frozen=True)
class ExecutedPreprocessingAudit:
    disposition: AuditDisposition
    receipts: tuple[ExecutedPreprocessingReceipt, ...]


def audit_executed_preprocessing(
    witnesses: Iterable[SourcePayloadPair],
    preprocess: Callable[[bytes], bytes],
) -> ExecutedPreprocessingAudit:
    """Execute and replay a byte-to-byte transform instead of trusting output IDs.

    A distinction is falsified if independently supplied source payloads differ
    in a declared target-relevant way yet produce *identical actual bytes*.
    Replaying each input detects common nondeterminism/state contamination;
    unstable replay blocks even a narrow non-collision result. Determinism of
    two replays is not a proof of purity, reproducibility, or source provenance.

    ``preprocess`` must be the actual deployed transform (with a fixed seed if
    applicable). It receives no target labels from this interface, but may
    consult external privileged state: that requires separate provenance audit.
    """

    if not callable(preprocess):
        raise TypeError("preprocess must be a callable taking and returning bytes")

    receipts: list[ExecutedPreprocessingReceipt] = []
    destructive_indices: list[int] = []
    unstable_indices: list[int] = []
    tested_relevant = False
    for index, witness in enumerate(witnesses):
        if not isinstance(witness.source_left, bytes) or not isinstance(
            witness.source_right, bytes
        ):
            raise TypeError("source payloads must be immutable bytes")
        if not isinstance(witness.target_distinguishable, bool):
            raise TypeError("target_distinguishable must be a boolean")
        if witness.target_distinguishable and witness.source_left == witness.source_right:
            raise ValueError("a target-distinguishing pair must differ at the source")

        left_output = preprocess(witness.source_left)
        right_output = preprocess(witness.source_right)
        left_replay = preprocess(witness.source_left)
        right_replay = preprocess(witness.source_right)
        if not all(
            isinstance(output, bytes)
            for output in (left_output, right_output, left_replay, right_replay)
        ):
            raise TypeError("preprocessor output must be immutable bytes")

        replay_stable = left_output == left_replay and right_output == right_replay
        receipts.append(
            ExecutedPreprocessingReceipt(
                sha256(witness.source_left).hexdigest(),
                sha256(witness.source_right).hexdigest(),
                sha256(left_output).hexdigest(),
                sha256(right_output).hexdigest(),
                replay_stable,
            )
        )
        if not replay_stable:
            unstable_indices.append(index)
        if witness.target_distinguishable:
            tested_relevant = True
            if left_output == right_output:
                destructive_indices.append(index)

    if unstable_indices:
        disposition = AuditDisposition("PREPROCESSING_REPLAY_UNSTABLE", tuple(unstable_indices))
    elif destructive_indices:
        disposition = AuditDisposition(
            "PREPROCESSING_DESTRUCTIVE_QUOTIENT_DETECTED", tuple(destructive_indices)
        )
    elif tested_relevant:
        disposition = AuditDisposition("NO_DESTRUCTIVE_QUOTIENT_WITNESSED_IN_SCOPE")
    else:
        disposition = AuditDisposition("PREPROCESSING_PRESERVATION_UNKNOWN")
    return ExecutedPreprocessingAudit(disposition, tuple(receipts))


@dataclass(frozen=True)
class MatchedAblation:
    """World/capture held fixed while adjudication bookkeeping is permuted.

    The pair is informative only if the independently provided before/after
    world and capture digests match. Identical digests here are claims
    by the data producer, not cryptographic evidence of causal identity.
    """

    world_left: str | None
    world_right: str | None
    capture_left: str | None
    capture_right: str | None
    adjudication_left: str
    adjudication_right: str
    exposed_left: str
    exposed_right: str


def audit_matched_ablation(pairs: Iterable[MatchedAblation]) -> AuditDisposition:
    """Detect raw-scene oracle symptoms in matched bookkeeping permutations."""

    counterexamples: list[int] = []
    informative = False
    for index, pair in enumerate(pairs):
        if (
            not pair.world_left
            or pair.world_left != pair.world_right
            or not pair.capture_left
            or pair.capture_left != pair.capture_right
        ):
            continue
        if pair.adjudication_left == pair.adjudication_right:
            continue
        informative = True
        if pair.exposed_left != pair.exposed_right:
            counterexamples.append(index)

    if counterexamples:
        return AuditDisposition("RAW_SCENE_ORACLE_DETECTED", tuple(counterexamples))
    if informative:
        return AuditDisposition("NO_RAW_SCENE_ORACLE_WITNESSED_IN_SCOPE")
    return AuditDisposition("GENERATIVE_PROVENANCE_UNVERIFIED")


@dataclass(frozen=True)
class ExposurePath:
    """Auditor-described provenance path ending at a possible learner exposure.

    ``declared_world_process`` means the causal route is part of ordinary
    declared world generation, not a privileged instrumentation shortcut. It
    must be independently inspected; asserting it here does not verify it.
    """

    origin: str
    path: tuple[str, ...]
    learner_visible: bool
    declared_world_process: bool


def audit_exposure_paths(paths: Iterable[ExposurePath]) -> AuditDisposition:
    """Catch extra simulator/evaluator-to-learner paths, including watermarks.

    The test does not rely on a target semantic partition: a watermark encoding
    *all* latent simulator state can be forbidden even if labels are shuffled.
    """

    privileged = {"EVALUATOR_ONLY", "SIMULATOR_LATENT"}
    counterexamples: list[int] = []
    for index, path in enumerate(paths):
        if not path.path:
            raise ValueError("exposure path must identify at least one transform")
        if path.origin in privileged and path.learner_visible and not path.declared_world_process:
            counterexamples.append(index)

    if counterexamples:
        return AuditDisposition(
            "FORBIDDEN_LEARNER_EXPOSURE_PATH_DETECTED", tuple(counterexamples)
        )
    return AuditDisposition("GENERATIVE_PROVENANCE_UNVERIFIED")


@dataclass(frozen=True)
class SemanticClaimEvidence:
    """Claim/freeze declarations supplied by an evaluator, never by the learner.

    The holdout's mere existence does not show that its rival-discriminating
    design, independence, measurement, or results were actually verified.
    """

    target_frozen_before_candidate: bool
    rival_family_frozen_before_candidate: bool
    new_evidence_ids: tuple[str, ...]
    claim_discriminating_against_structured_rivals: bool
    selection_evidence_ids: tuple[str, ...] = ()
    interpretation_frozen_before_holdout: bool = False
    rivals_frozen_before_holdout: bool = False
    holdout_result: str | None = None


@dataclass(frozen=True)
class SemanticConfirmationDisposition:
    hypothesis_status: str
    holdout_status: str
    claim_ceiling: str


def audit_semantic_confirmation(
    evidence: SemanticClaimEvidence,
) -> SemanticConfirmationDisposition:
    """Prevent post-hoc naming or fresh IID confounds from claiming semantics.

    A `SUPPORTED_AMONG...` result is a *ceiling* conditional on declarations,
    not a certificate that the hypothesis or learner succeeded on the data.
    """

    if evidence.holdout_result not in (None, "SUPPORTED", "FALSIFIED"):
        raise ValueError("holdout_result must be SUPPORTED, FALSIFIED or None")

    originally_frozen = (
        evidence.target_frozen_before_candidate
        and evidence.rival_family_frozen_before_candidate
    )
    fresh_ids = set(evidence.new_evidence_ids)
    if not fresh_ids or fresh_ids.intersection(evidence.selection_evidence_ids):
        holdout_status = "NO_FRESH_EVIDENCE"
    elif not originally_frozen and not evidence.selection_evidence_ids:
        holdout_status = "FRESHNESS_UNVERIFIED"
    elif evidence.claim_discriminating_against_structured_rivals:
        holdout_status = "CLAIM_DISCRIMINATING_HOLDOUT"
    else:
        holdout_status = "FRESH_BUT_NONDISCRIMINATING_EVIDENCE"

    retest_frozen = (
        evidence.interpretation_frozen_before_holdout
        and evidence.rivals_frozen_before_holdout
    )
    eligible = holdout_status == "CLAIM_DISCRIMINATING_HOLDOUT" and (
        originally_frozen or retest_frozen
    )
    if originally_frozen:
        hypothesis_status = "CONFIRMATORY_TARGET_CLAIM"
    elif eligible:
        hypothesis_status = "POST_HOC_INTERPRETATION_RETESTED"
    else:
        hypothesis_status = "EXPLORATORY_POST_HOC_INTERPRETATION"

    if not eligible:
        ceiling = "SEMANTIC_INTERPRETATION_STILL_CONFOUNDED"
    elif evidence.holdout_result == "SUPPORTED":
        ceiling = "SUPPORTED_AMONG_DECLARED_RIVALS_WITHIN_TESTED_SCOPE"
    elif evidence.holdout_result == "FALSIFIED":
        ceiling = "SEMANTIC_INTERPRETATION_NOT_SUPPORTED_IN_TESTED_SCOPE"
    else:
        ceiling = "SEMANTIC_CONFIRMATION_NOT_ESTABLISHED"
    return SemanticConfirmationDisposition(hypothesis_status, holdout_status, ceiling)
