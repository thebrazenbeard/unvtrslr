# Post-Pass-3 Qualification Controls

Status: `PROVISIONAL_CONTROL_ADDENDUM / NOT_CANON / NOT_MERGED`

Predecessor frozen evidence checkpoint: `NONHUMAN_COMMUNICATION_PASS_3@ca6cc0c4fe176d2097b6d0aee0e18f9a9ea4a8a2`.

This addendum converts the current One/Four/Nine/Thirteen adversarial round plus post-Pass-3 methodological research into explicit candidate controls. It does not alter the frozen Pass 3 subject and does not replace `docs/R2_ADVERSARIAL_EVALUATOR.md` or `docs/NONHUMAN_CONTROL_OVERLAYS.md` yet.

The status language below is deliberately conservative and does **not** depend on Draft PR #2 merging. It is compatible with an operational-vs-semantic split while current `main` remains authoritative.

Use stable semantic control IDs in cross-worker coordination. Numbered local aliases may exist only inside a frozen suite.

## CTRL_GLOBAL_STATE_WATERMARK

### Failure being tested

A learner-visible raw modality contains target-agnostic privileged telemetry derived from simulator/evaluator latent state. Because the telemetry is not conditioned on the current challenge label, a target-partition permutation can miss it.

### Invalid condition

Let `Z` be privileged simulator/evaluator latent state. An instrumentation/rendering path writes an invertible or highly informative `W(Z)` into learner-visible observations outside the declared participant/world causal path.

The learner may then appear to ground counterpart behavior while actually decoding privileged telemetry.

### Matched control

Hold the declared physical/generative episode and participant behavior fixed while independently:

- removing the privileged telemetry;
- randomizing it;
- encrypting/permuting it independently of the learner;
- or replacing it with matched-noise structure.

### Expected disposition

If bridge/semantic performance materially depends on the telemetry, the stronger learner-grounding claim fails or is narrowed to the augmented instrumentation surface.

Required provenance distinction:

- `DECLARED_PARTICIPANT_WORLD_CAUSAL_PATH`;
- `OBSERVER_INSTRUMENTATION_TELEMETRY`;
- `UNRESOLVED_PATH_CLASS`.

Target-independence is not sufficient evidence of neutrality.

## CTRL_CLAIM_DISCRIMINATING_HOLDOUT

### Failure being tested

A semantic interpretation is frozen and performs well on genuinely fresh IID evidence, but the holdout preserves the same confound that made the interpretation attractive.

### Required design

Identify the strongest live structured operational rival(s) and create a holdout/intervention/domain-shift condition that makes the semantic interpretation and those rivals predict materially different outcomes while preserving the narrower operational relation where possible.

### Required statuses

- `FRESH_BUT_NONDISCRIMINATING_EVIDENCE`;
- `CLAIM_DISCRIMINATING_HOLDOUT`;
- `COUNTERFACTUAL_OR_SHIFT_TESTED`;
- `SEMANTIC_INTERPRETATION_STILL_CONFOUNDED`.

### Qualification rule

Freshness alone cannot promote an exploratory or preregistered semantic interpretation if every strongest live alternative makes the same prediction on the holdout.

## CTRL_STRUCTURED_RIVAL_ADEQUACY

### Failure being tested

The evaluator supplies named rivals plus `NONE_OF_DECLARED_RIVALS`, but an omitted structured alternative remains unrepresented. A named human semantic label wins because the null bucket is too weak, not because the rival family is adequate.

### Required distinction

Keep separate:

- `REJECTION_ESCAPE_PRESENT`;
- `STRUCTURED_ALTERNATIVE_STRESS_NOT_ESTABLISHED`;
- `STRUCTURED_ALTERNATIVE_STRESS_TESTED`;
- `RIVAL_FAMILY_MISSPECIFICATION_DETECTED`;
- `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`.

### Candidate stress methods

Use one or more of:

- alternative generation by an independently initialized evaluator/model family;
- nonparametric/less-committed operational description;
- causal/functional rivals that are not human pragmatic labels;
- model criticism against residual structure;
- adversarial search for a simpler relation explaining the same evidence;
- withheld structured rival injected into synthetic ground truth.

An open/null alternative is useful but is not itself a model-adequacy certificate.

## CTRL_POSTHOC_SEMANTIC_NAMING

### Failure being tested

The evaluator chooses a semantic label after inspecting the learner's discovered operational relation and then treats same-data fit as semantic confirmation.

### Required statuses

- `CONFIRMATORY_TARGET_CLAIM`;
- `EXPLORATORY_POST_HOC_INTERPRETATION`;
- `OPERATIONAL_RELATION_VERIFIED_SEMANTIC_NAMING_UNRESOLVED`;
- `POST_HOC_INTERPRETATION_FROZEN_FOR_FOLLOWUP`;
- `POST_HOC_INTERPRETATION_RETESTED_ON_CLAIM_DISCRIMINATING_FRESH_EVIDENCE`.

### Rule

`discover -> name -> test on same evidence` is exploratory.

`discover -> freeze proposed interpretation -> collect claim-discriminating fresh evidence -> test` may support confirmation within scope.

## CTRL_NOT_APPLICABLE_EVASION

### Failure being tested

`NOT_APPLICABLE_TO_OBSERVED_COMMUNICATION_SYSTEM` is used to convert difficult failures into exclusions, allowing an apparently universal score with weak coverage.

### Required applicability record

For every excluded challenge record:

- `challenge_id`;
- `applicability_prerequisite`;
- `prerequisite_evidence`;
- `applicability_adjudication_time`;
- `candidate_result_seen_before_adjudication`;
- `alternative_cross_species_variant`;
- `reentry_condition`;
- `coverage_effect`.

### Required result states

- `APPLICABLE_TESTED`;
- `STRUCTURALLY_INAPPLICABLE_IN_SCOPE`;
- `APPLICABILITY_UNRESOLVED`.

`APPLICABILITY_UNRESOLVED` is neither pass nor not-applicable.

### Aggregate reporting rule

Always report `passed / applicable / total`.

Do not emit `FIRST_100_COMPLETE` unless all 100 are applicable under the declared target and all 100 pass.

If only `k` challenges are applicable and all `k` pass, the strongest ordinary wording is:

`FIRST_100_APPLICABLE_SUBSET_PASSED (k/100 applicable)`.

`NOT_APPLICABLE` is not semantic success and cannot increase the numerator.

## CTRL_DYNAMIC_BOUNDARY_ASSUMPTION

### Failure being tested

The evaluator silently assumes stable individuated agents, senders, receivers, or channels even though the tested system is distributed, overlapping, collective, transient, or sensor/channel-fused.

### Provisional experiment handle

`EXPOSURE_CONTROL_LOCUS` may be used only as a provenance handle over an operational access/influence boundary.

A locus may be:

- time-varying;
- overlapping;
- distributed;
- collective;
- experimenter-declared;
- learner-discovered;
- unresolved.

### Required field

`BOUNDARY_MODEL = EXPERIMENTER_DECLARED | LEARNER_DISCOVERED | MIXED | UNRESOLVED`

Any claim that depends on stable individuation must state that dependency explicitly.

## CTRL_SEMANTIC_SURPLUS

Status: `PROJECT_HYPOTHESIS / DESIGN PROPOSAL`.

### Problem

A clean, transferable operational relation may survive every provenance and robustness control while the word `semantic` adds no testable content.

### Candidate criterion

Let `R` be the strongest live structured operational comparator not yet shown to satisfy the stronger semantic claim and `S` the proposed semantic interpretation.

`S` earns a stronger semantic qualification only if:

1. the exact interpretation `S` entails at least one preregistered prediction/intervention/transfer/conservation obligation not already entailed by `R`;
2. the obligation is claim-discriminating against the strongest live structured operational rivals;
3. the learner/evaluator passes it on independent evidence;
4. provenance and hypothesis-family controls remain clean.

### Anti-arbitrary-surplus principle

**Extra difficulty is not semantic content.** The evaluator may not promote `S` merely by adding an arbitrary hard test that `R` did not happen to be designed for. The additional obligation must be justified by the content of the exact semantic interpretation and must discriminate `S` from a lower operational account for a reason relevant to that interpretation.

If `S` and `R` make the same predictions on the chosen test, the test does not establish semantic surplus regardless of difficulty.

### Failure disposition

If no claim-grounded discriminating obligation can be stated, preserve the lower operational result. A human semantic rendering may be recorded, but the semantic qualification remains unresolved/not independently established.

### Open attack

This criterion may be too strict, too weak, or circular. It must be challenged before architecture promotion.

## R0.5 versus R2 placement proposal

Keep the pre-R1 gate thin and representation-neutral.

Candidate R0.5 responsibilities:

- `EMPIRICAL_IDENTIFIABILITY`;
- `WITNESS_PROVENANCE`;
- `BRIDGE_ATTRIBUTION`;
- `HYPOTHESIS_FAMILY_PROVENANCE`;
- `PREPROCESSING_PRESERVATION_STATUS`;
- instrumentation/generative-path classification;
- `BOUNDARY_MODEL`;
- `HYPOTHESIS_FAMILY_STATUS` at the level needed to expose open/misspecified rivals;
- `CLAIM_CEILING` and `SCOPE`.

R0.5 does not require a universal functional-class, form/referent, speaker/listener, or content ontology. Target-specific metadata may be carried when an exact claim needs it.

Candidate R2/semantic-qualification responsibilities:

- communicative use versus informational cue where applicable;
- semantic interpretation versus operational relation;
- confirmatory versus exploratory naming;
- claim-discriminating holdouts/interventions;
- structured-rival adequacy/model criticism;
- semantic-surplus test;
- conservation/non-equivalence tests.

This placement is provisional and should remain falsifiable by One/Four/Thirteen critique.

## Current control-chain principle

Do not treat the following as a universal semantic ladder. It is a **claim-construction checklist** whose steps are used only when entailed/applicable to the exact claim:

- establish that a learner-accessible distinction exists;
- verify that the learner boundary preserves the distinctions required by the claim;
- exclude or scope privileged telemetry/bridge oracles;
- establish learner/counterpart attribution as required;
- keep target/rival family provenance clean;
- separate exploratory naming from confirmation;
- require fresh evidence that actually discriminates a semantic claim from live structured operational rivals;
- stress structured alternative adequacy;
- require any claimed semantic surplus to be claim-grounded rather than arbitrary difficulty;
- preserve applicability, coverage, uncertainty, and claim ceiling.

## Result packaging

A completed run reports orthogonal state rather than one ambiguous generic `GROUNDED_WITHIN_TESTED_SCOPE` label:

- **operational relation/grounding state** — what cross-system operational relation is actually supported;
- **semantic interpretation/qualification state** — whether a separately frozen semantic interpretation has survived its claim-specific discriminating tests;
- **applicability/coverage state** — which tests were meaningful and which remain unresolved/inapplicable;
- **claim ceiling** — the strongest wording warranted by the exact evidence and scope.

Research prose may use descriptions such as `operational correspondence supported within tested scope` or `semantic correspondence supported within tested scope`, but only with the corresponding evidence axis stated. No generic status silently licenses semantic interpretation, and no scoped result licenses universal meaning.
