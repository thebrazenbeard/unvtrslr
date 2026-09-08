# R1 Interface Generalization V2

Status: `PROVISIONAL_SUCCESSOR_CORRECTION / NOT_IMPLEMENTED`

## Purpose

The original R1 common behavioral contract is useful for agent/message/action fixtures, but its interface vocabulary can accidentally turn those fixture properties into universal assumptions.

UNVTRSLR must also be able to test systems involving:

- persistent fields rather than discrete messages;
- passive or asynchronous exposure;
- distributed or collective processes;
- overlapping sensor/channel boundaries;
- environmental modification without an explicit signal object;
- systems where active intervention is unavailable, unsafe, or not part of the declared interaction surface.

Therefore V2 treats `signal`, `action`, `message`, and `intervention` as **capabilities that may be required by a fixture or claim**, not universal primitives that every candidate must expose.

## Minimal universal interface

A candidate substrate used under V2 must support the weakest common operations needed to compare representations without prescribing a particular communication ontology:

1. `ingest_learner_visible_exposure_by_opaque_reference`
2. `update_candidate_state`
3. `preserve_competing_interpretations`
4. `explicit_uncertainty`
5. `explicit_provenance`
6. `condition_on_declared_exposure_or_interaction_feature`
7. `predict_or_constrain_under_admissible_regime`
8. `scoped_equivalence_or_non_equivalence`
9. `expose_support_and_contradiction`
10. `evaluator_query_adapter_without_truth_labels`
11. `conservation_ledger_support`
12. `UNKNOWN_outcome`
13. `NO_FAITHFUL_EQUIVALENT_FOUND_WITHIN_DECLARED_SCOPE_outcome`

`predict_or_constrain_under_admissible_regime` is intentionally broad but not unconstrained. The exact admissible regime must be frozen by the experiment contract and may contain observational queries, natural perturbations, active interventions, policy-conditioned predictions, or another declared query family.

The evaluator may not silently expand that regime after seeing candidate behavior.

## Capability/applicability manifest

Each fixture and candidate evaluation must bind a capability/applicability manifest covering at least:

- `DISCRETE_SIGNAL_CONDITIONING`
- `MESSAGE_BOUNDARY`
- `ACTIVE_INTERVENTION`
- `ACTION_SELECTION`
- `ROLE_REVERSAL`
- `BIDIRECTIONAL_EXCHANGE`
- `GLOBAL_TEMPORAL_ORDERING`
- `DISCRETE_TOKENIZATION`

Each capability receives one of:

- `REQUIRED_BY_FIXTURE`
- `SUPPORTED_OPTIONAL`
- `NOT_APPLICABLE_JUSTIFIED`
- `UNRESOLVED`

A fixture may add additional capabilities.

## Anti-evasion rule

`NOT_APPLICABLE_JUSTIFIED` is not a pass token.

For every critical test or claimed property, the evaluator must record whether the capability is:

- genuinely irrelevant to the exact claim;
- unavailable because of the declared system/fixture;
- or omitted in a way that weakens the claim.

If a stronger claim materially depends on a capability that is marked `NOT_APPLICABLE_JUSTIFIED` or `UNRESOLVED`, the claim ceiling must be lowered rather than treating the missing test as passed.

Example:

- a passive field-coupled system need not support an `ACTION_SELECTION` API;
- but a claim of counterfactual causal control cannot receive credit from an unperformed active-control test merely because action selection is absent.

The evaluator must use another genuinely discriminating route or retain the weaker claim.

## Active intervention remains high-value, not universal

Active intervention is often one of the strongest ways to distinguish causal/semantic rivals. V2 does not demote it scientifically.

Instead:

- use active intervention when the declared interaction surface supports it;
- otherwise use admissible natural perturbations, environmental shifts, temporal discontinuities, partner changes, sensor changes, or other claim-discriminating evidence;
- if no available evidence separates the rivals, return underdetermination rather than manufacturing intervention capability.

## No hidden evaluator ontology through generalization

The generalized interface must not become so abstract that the evaluator can smuggle arbitrary structure through the query object.

Therefore every `admissible_regime` and evaluator query family must be:

- declared before candidate hidden evaluation;
- provenance-bound;
- free of evaluator semantic labels or hidden truth variables in learner-visible form;
- limited to operations physically or procedurally available under the declared fixture;
- auditable under R0.5 mediation and generative provenance.

An opaque query ID is not automatically safe. Its causal effect and information content still belong in the provenance graph.

## Relation to R1/R2

This document is a bounded V2 correction to the common candidate interface. It does not replace the existing R1 substrate definitions or remove intervention-based R2 tests where applicable.

Its purpose is narrower:

> Do not make agent/message/action ontology a prerequisite for entering the substrate competition.

V2 certificates must bind the exact capability/applicability manifest used for the run.
