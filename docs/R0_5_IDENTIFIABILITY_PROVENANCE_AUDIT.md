# R0.5 Identifiability and Provenance Audit

Status: PROVISIONAL / REVIEWED DESIGN PRESSURE / NOT YET CANONICAL MAIN

## Purpose

R0.5 is a pre-R1 gate that asks a narrower question than semantic qualification:

> Does the learner-accessible interaction surface contain enough trustworthy, non-subsidized structure to distinguish the declared claim from its declared rivals, and can that structure be attributed to the coupled system rather than to evaluator or instrumentation leakage?

R0.5 exists to prevent later representation or semantic tests from receiving a contaminated problem formulation and then reporting a sophisticated false positive.

It is intentionally claim-neutral. It does not define a universal ontology of meaning, language, agents, messages, referents, functions, or intentions.

## Non-goals

R0.5 does not establish:

- true meaning;
- communicative intent;
- producer-side communicative function;
- a universal semantic representation;
- completeness of the evaluator's hypothesis family;
- absence of every possible hidden dependency in inaccessible machinery;
- metaphysical identity between two systems' concepts.

Those claims require later, scoped qualification and may remain underdetermined.

## Required audit inputs

`R05_AUDIT` should bind at least:

- `interaction_surface`
- `target_claim_spec`
- `rival_hypothesis_family`
- `admissible_strategy_family`
- `budget`
- `statistical_resolution`
- `mediation_trust_partition`
- `hypothesis_family_provenance`
- `boundary_model`

`interaction_surface` must include the earliest generative boundary capable of altering learner-visible evidence when that boundary is material to the experiment.

The audit should avoid assuming exactly two individuated agents. Use experiment-declared exposure/control loci where necessary.

## Required outputs

A machine contract should expose semantic field names rather than globally overloading ordinal labels.

Minimum outputs:

- `EMPIRICAL_IDENTIFIABILITY`
- `BRIDGE_ATTRIBUTION`
- `HYPOTHESIS_FAMILY_STATUS`
- `HYPOTHESIS_FAMILY_PROVENANCE`
- `WITNESS_PROVENANCE`
- `PREPROCESSING_PRESERVATION_STATUS`
- `GENERATIVE_PROVENANCE_STATUS`
- `BOUNDARY_MODEL`
- `CLAIM_CEILING`
- `SCOPE`

`TARGET_RELATION_STATUS` may be used later as an evaluator annotation where a bounded test genuinely needs categories such as report, referent, cue, function, communicative use, or intent. It is not required as a universal pre-R1 primitive.

## Claim-relative no-destructive-quotient rule

A learner-bound transform may compress, serialize, tokenize, quantize, feature-extract, sample, or otherwise transform the native exposure surface.

It must not collapse two source-side learner-accessible states or histories into one learner representation when their distinction is required to discriminate a currently admissible target-claim rival, unless the loss is explicitly declared and the affected claim is correspondingly downgraded or marked unidentifiable.

This rule does not require:

- raw modality retention;
- a global clock;
- event objects;
- discrete messages;
- concurrency as a universal primitive.

The relevant requirement is preservation of distinctions needed by the claim under test.

If preservation cannot be established, use:

`PREPROCESSING_PRESERVATION_UNKNOWN`

rather than assuming neutrality.

## Generative and witness provenance

Witness provenance must extend far enough upstream to detect semantic writing into the evidence surface.

An experiment-specific provenance path may include:

`world/generator -> dynamics/scene construction -> participant/actuator production -> propagation/channel physics -> sensor/render/capture -> preprocessing -> learner exposure`

Each learner-visible causal path should be classified where possible as one of:

- `DECLARED_WORLD_DYNAMICS`
- `PARTICIPANT_PRODUCED`
- `DECLARED_PHYSICAL_OR_CHANNEL_PROPAGATION`
- `DECLARED_SENSOR_MODEL`
- `LEARNER_PREPROCESSING`
- `INSTRUMENTATION_OR_TELEMETRY`
- `EVALUATOR_OR_ADJUDICATION`
- `UNKNOWN_OR_UNVERIFIED`

These are experiment-responsibility labels, not universal natural kinds.

If the generator, renderer, sensor, evaluator, or instrumentation can affect learner-visible evidence but cannot be independently inspected or reproduced, strong claims must fail closed to a bounded provenance status such as:

`GENERATIVE_PROVENANCE_UNVERIFIED`

UNVTRSLR can audit declared and inspectable machinery. It cannot infer the honesty of inaccessible machinery from learner traces alone.

## Stable adversarial controls

### `CTRL_PRIVATE_ALIAS`

High task reward achieved through a task-bound arbitrary code without transferable grounded correspondence.

Expected result: operational coordination may pass; semantic promotion fails.

### `CTRL_BRIDGE_ORACLE`

A privileged mediator performs the target normalization before the learner sees the evidence.

Expected result: downstream identifiability may remain high, but `BRIDGE_ATTRIBUTION` must report mediation subsidy.

### `CTRL_RAW_SCENE_ORACLE`

Evaluator target bookkeeping directly changes learner-visible scene or sensor evidence while the physical/generative episode is otherwise held fixed.

Expected result: target-partition permutation exposes evaluator-written evidence.

### `CTRL_GLOBAL_STATE_WATERMARK`

A target-agnostic instrumentation channel writes an invertible or highly informative encoding of privileged simulator state into learner-visible raw evidence.

The watermark is always present and does not depend on the currently selected target claim, so target-partition permutation alone does not expose it.

Required matched comparison:

1. same declared episode and participant behavior with privileged telemetry visible;
2. same declared episode and participant behavior with telemetry removed, randomized, masked, encrypted, or otherwise decorrelated while preserving the declared interaction path.

If the bridge collapses only when the telemetry disappears, the stronger grounding claim fails.

Target-independence is not evidence of neutrality.

### `CTRL_DESTRUCTIVE_QUOTIENT`

A preprocessing transform erases a native learner-accessible distinction that the evaluator later credits the learner with recovering.

Expected result: qualification fails or the claim ceiling narrows.

### `CTRL_POSTHOC_SEMANTIC_NAMING`

The learner discovers a genuine, transferable operational partition. The evaluator inspects the partition afterward, searches a human semantic label library, selects the best-fitting label, and then reports that the learner recovered that meaning.

Required distinction:

- `CONFIRMATORY_TARGET_CLAIM`
- `EXPLORATORY_POST_HOC_INTERPRETATION`
- `OPERATIONAL_RELATION_VERIFIED_SEMANTIC_NAMING_UNRESOLVED`
- `POST_HOC_INTERPRETATION_RETESTED_ON_FRESH_EVIDENCE`

Same-data post-selection never becomes confirmatory semantic recovery merely because fit is high.

### `CTRL_IID_HOLDOUT_ILLUSION`

A post-hoc semantic interpretation is frozen and then perfectly reconfirmed on fresh IID data from the same confounded regime.

A claim-discriminating intervention or domain shift later reveals that the learner tracks a different invariant than the semantic label asserts while the narrower operational relation survives.

Required statuses include:

- `FRESH_BUT_NONDISCRIMINATING_EVIDENCE`
- `CLAIM_DISCRIMINATING_HOLDOUT`
- `COUNTERFACTUAL_OR_SHIFT_TESTED`
- `SEMANTIC_INTERPRETATION_STILL_CONFOUNDED`

Fresh evidence is necessary for post-hoc confirmation but is not sufficient unless it separates the strongest live alternatives relevant to the promoted claim.

### Structured-rival adequacy control

`NONE_OF_DECLARED_RIVALS` is a rejection escape hatch, not proof that the rival family is adequate.

Required status separation:

- `REJECTION_ESCAPE_PRESENT`
- `REJECTION_ESCAPE_ABSENT`
- `STRUCTURED_ALTERNATIVE_STRESS_NOT_ESTABLISHED`
- `STRUCTURED_ALTERNATIVE_STRESS_TESTED`
- `RIVAL_FAMILY_MISSPECIFICATION_DETECTED`
- `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`

A null bucket losing to a named label does not eliminate omitted structured explanations.

Hypothesis-family adequacy is normally an ongoing criticism obligation, not a binary property achieved once.

## Informational cue is not communicative function

A source feature can be:

- a real informational relation;
- causally useful to a receiver;
- robust across contexts;
- transferable;

without being used communicatively by the producer.

Receiver exploitation alone must not promote a producer-side claim.

Downstream semantic qualification should distinguish statuses such as:

- `INFORMATIONAL_RELATION_SUPPORTED`
- `RECEIVER_USE_SUPPORTED`
- `COMMUNICATIVE_FUNCTION_SUPPORTED_IN_SCOPE`
- `COMMUNICATIVE_FUNCTION_UNRESOLVED`
- `NONCOMMUNICATIVE_CUE_SUPPORTED`

No single marker should be treated as metaphysical proof of intention.

## Semantic null-content test

A robust operational relation does not become scientifically stronger merely by being renamed semantic.

For every proposed promotion from an operational relation to a semantic relation, require an explicit semantic delta:

> What additional observable prediction, intervention outcome, conservation obligation, rendering constraint, transfer requirement, or qualification failure becomes possible specifically because this is a semantic correspondence rather than merely an operational correspondence?

If the answer is `none`, semantic promotion fails.

Stable control:

`CTRL_SEMANTIC_NULL_CONTENT`

Compare two claim objects over the same evidence:

- `OPERATIONAL_CORRESPONDENCE`
- `SEMANTIC_CORRESPONDENCE`

The stronger claim must declare at least one predeclared condition under which the operational claim can remain true while the semantic claim becomes false.

If no such condition exists, the semantic label adds no falsifiable content within scope.

Suggested statuses:

- `OPERATIONAL_CORRESPONDENCE_ESTABLISHED`
- `SEMANTIC_DELTA_SPECIFIED`
- `SEMANTIC_DELTA_TESTED`
- `SEMANTIC_DELTA_NOT_ESTABLISHED`
- `SEMANTIC_INTERPRETATION_UNDERDETERMINED_IN_SCOPE`
- `SEMANTIC_LABEL_ADDS_NO_FALSIFIABLE_CONTENT`

Do not solve this by defining semantics as whatever passes the current evaluator. That is circular unless the evaluator contains independently justified semantic-specific obligations.

## Semantic-surplus discipline

A semantic qualification stage may require a `SEMANTIC_SURPLUS_OBLIGATION`, but arbitrary extra difficulty is not enough.

Candidate obligations may include, depending on the exact claim:

- cross-context conservation under task changes;
- systematic recombination or generalization;
- bidirectional or role-reversed use;
- counterfactual substitution;
- rendering constraints with explicit loss accounting;
- transfer into independently constructed tasks whose scoring was not derived from the original operational partition;
- novel interaction predictions not used to fit the relation.

No single item is a universal definition of semantics.

A valid surplus obligation must create a principled, predeclared falsifiable difference between the lower operational claim and the stronger semantic claim. If an arbitrary non-semantic code can satisfy the burden for the same reason, the obligation has not earned the promotion.

## Responsibility boundary

### R0.5 owns

- empirical identifiability relative to a declared family;
- hypothesis-family provenance and family-status exposure;
- witness provenance;
- generative/instrumentation provenance;
- no-destructive-quotient preservation;
- bridge attribution;
- exposure/control boundary provenance;
- evidence-admissibility controls.

### R1 owns

- competing representation/substrate systems over claims that survive R0.5;
- no automatic semantic promotion from representational success.

### R2 owns

- communicative-function/content claims where applicable;
- confirmatory versus exploratory semantic naming;
- claim-discriminating intervention/domain-shift evidence;
- structured alternative generation and stress where strong wording depends on it;
- semantic-surplus obligations;
- semantic claim ceiling.

## Claim ceiling

The ladder is deliberately non-monotonic.

The system must permit states such as:

- operational relation verified, semantic label unresolved;
- learner bridge attribution clean, semantic interpretation confounded;
- fresh evidence obtained, but not claim-discriminating;
- null/open rival present, but structured-rival adequacy not established;
- semantic interpretation best among declared rivals, with broader ontology unresolved;
- semantic label empirically vacuous relative to the lower operational claim.

No earlier success automatically upgrades a later claim.

Safe intermediate wording includes:

`OPERATIONAL_CORRESPONDENCE / GROUNDED RELATION / INTERPRETATION UNDER TEST`

Reserve stronger semantic wording for claims carrying explicit additional falsifiable obligations.
