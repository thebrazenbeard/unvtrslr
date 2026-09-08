# R0.5 — Evidence Admissibility and Claim-Control Gate

Status: `PROVISIONAL / RESEARCH-DERIVED / NOT_IMPLEMENTED`

## Purpose

R0.5 is a pre-R1 audit. It does **not** decide what meaning is, select a semantic substrate, or certify that a relation is genuinely semantic.

Its job is narrower:

> determine whether the learner-visible evidence is admissible, whether the declared target distinction is empirically distinguishable within scope, and whether the apparent bridge can be attributed to the learner/counterpart interaction rather than to privileged experiment machinery.

R0.5 exists because later representation or semantic evaluation is uninterpretable if the experiment has already written the answer into the learner's evidence, destroyed target-relevant distinctions, or defined the rival family so narrowly that success is guaranteed by construction.

## Non-goals

R0.5 does not establish:

- a universal ontology;
- a universal decomposition into objects, agents, messages, referents, functions, or semantic content;
- that a winning interpretation is uniquely true;
- that a verified operational relation is communicative;
- that a communicative relation has a warranted human semantic label;
- that a semantic claim survives serious structured alternatives;
- that fresh IID evidence is claim-discriminating evidence.

Those stronger claims remain downstream responsibilities.

## Audit subject

A provisional audit subject is:

`R05_AUDIT(`
`  interaction_surface,`
`  target_claim_spec,`
`  rival_hypothesis_family,`
`  admissible_strategy_family,`
`  budget,`
`  statistical_resolution,`
`  mediation_trust_partition,`
`  hypothesis_family_provenance,`
`  boundary_model`
`)`

The fields are experiment declarations, not claims that nature comes pre-segmented into these categories.

## Required outputs

R0.5 should expose at least:

- `EMPIRICAL_IDENTIFIABILITY`
- `TARGET_RELATION_STATUS`
- `BRIDGE_ATTRIBUTION`
- `HYPOTHESIS_FAMILY_STATUS`
- `HYPOTHESIS_FAMILY_PROVENANCE`
- `WITNESS_PROVENANCE`
- `PREPROCESSING_PRESERVATION_STATUS`
- `INSTRUMENTATION_PROVENANCE_STATUS`
- `BOUNDARY_MODEL`
- `CLAIM_CEILING`
- `SCOPE`

No passing field silently promotes another.

## 1. Empirical identifiability is claim-relative

Two rival hypotheses are empirically equivalent within an interaction surface, strategy family, budget, and statistical resolution when every admissible strategy produces learner-visible evidence that is indistinguishable at that resolution.

R0.5 may therefore return outcomes such as:

- `DISTINGUISHABLE_IN_SCOPE`
- `UNIDENTIFIABLE_WITHIN_INTERACTION_SURFACE`
- `INSUFFICIENT_EVIDENCE_OR_BUDGET`
- `OPEN_OR_MISSPECIFIED_RIVAL_FAMILY`

`DISTINGUISHABLE_IN_SCOPE` means only that the declared evidence can separate relevant rivals. It does not mean that the learner has grounded the distinction or that the evaluator's ontology is privileged.

## 2. Witness provenance and bridge attribution

Every discriminating witness should carry an auditable path from origin to learner exposure.

A generic provenance description may include, where applicable:

`world/generator -> dynamics/scene construction -> production/actuation -> propagation -> sensor/render/capture -> preprocessing -> learner exposure`

The exact stages are experiment-specific.

The audit must identify whether a distinguishing witness is attributable to:

- declared participant/world causal dynamics;
- learner/counterpart interaction;
- negotiated convention;
- interaction-surface infrastructure;
- privileged mediator;
- observer/instrumentation telemetry;
- mixed or unresolved provenance.

A learner may receive genuinely discriminating information while still failing learner-grounding attribution because the experiment supplied the cross-system normalization.

## 3. Mediation and instrumentation trust boundary

Target-specific semantic leakage is not the only threat.

R0.5 must audit both:

- target-conditioned semantic writing, such as evaluator labels or challenge identity altering learner-visible evidence; and
- target-agnostic privileged telemetry, such as a renderer or diagnostic layer exposing an invertible encoding of simulator latent state.

A learner-visible feature derived directly from evaluator/simulator latent state outside the declared participant-accessible generative path is presumptive subsidy until ablation shows that the claimed bridge does not materially depend on it.

Target-independence alone does not make telemetry neutral.

## 4. Claim-relative no-destructive-quotient rule

A learner-boundary transform must not collapse two native learner-accessible observation histories or states into one representation when their distinction is required to discriminate a currently admissible target-claim rival, unless:

1. the loss is explicitly declared; and
2. the affected claim is correspondingly downgraded or marked unidentifiable.

This rule does not require:

- a global clock;
- discrete events;
- messages;
- channels;
- objects;
- raw-modality storage;
- concurrency as a universal primitive.

Serialization, compression, quantization, feature extraction, or tokenization are allowed when they preserve the distinctions required by the tested claim.

If preservation cannot be established, use a fail-closed state such as `PREPROCESSING_PRESERVATION_UNKNOWN` rather than presuming neutrality.

## 5. Hypothesis-family provenance

The evaluator authorship surface must be explicit.

For each target/rival family record, where material:

- who proposed it;
- when it was frozen relative to candidate evidence;
- whether candidate traces/results were inspected before selection;
- the source and size of any searched interpretation library;
- adjudication rule and threshold version;
- whether the claim is confirmatory or exploratory;
- the identity of fresh evidence used for later confirmation.

Suggested statuses include:

- `CONFIRMATORY_TARGET_CLAIM`
- `EXPLORATORY_POST_HOC_INTERPRETATION`
- `OPERATIONAL_RELATION_VERIFIED_SEMANTIC_NAMING_UNRESOLVED`
- `FROZEN_CONFIRMATORY`
- `POST_HOC_EXPLORATORY`
- `KNOWN_INCOMPLETE`
- `MISSPECIFICATION_DETECTED`

A post-hoc semantic label does not become confirmatory because it fits the same evidence extremely well.

## 6. Open rival is necessary but not sufficient

An explicit option such as:

`NONE_OF_DECLARED_RIVALS / UNMODELED_RELATION`

prevents forced choice among named evaluator labels.

It does **not** establish that the declared family contains the strongest relevant structured alternative.

R0.5 should therefore distinguish:

- `REJECTION_ESCAPE_PRESENT`
- `STRUCTURED_ALTERNATIVE_STRESS_NOT_ESTABLISHED`
- `STRUCTURED_ALTERNATIVE_STRESS_TESTED`
- `RIVAL_FAMILY_MISSPECIFICATION_DETECTED`
- `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`

Strong semantic promotion remains downstream and must respect this ceiling.

## 7. Boundary model is provenance

UNVTRSLR must not silently assume that arbitrary systems naturally decompose into exactly two agents.

Use the weaker operational abstraction:

`EXPOSURE_CONTROL_LOCUS`

A locus is an experiment-declared boundary through which some process receives state and/or can influence the coupled system. It may correspond to one agent, many agents, a distributed process, overlapping processes, or another bounded experimental locus.

Suggested boundary states:

- `EXPERIMENTER_DECLARED`
- `LEARNER_DISCOVERED`
- `MIXED`
- `UNRESOLVED`

Any claim that materially depends on a particular individuation must bind that dependency.

## Stable adversarial control IDs

Cross-document coordination should use semantic IDs rather than overloaded local ordinals.

### `CTRL_PRIVATE_ALIAS`

Rival meanings are observationally/interventionally aliased through the learner surface. The system must report scoped unidentifiability rather than inventing a distinction.

### `CTRL_MINIMAL_SEPARABLE`

A minimal positive case in which one learner-accessible consequence separates the declared rivals without privileged mediation.

### `CTRL_BRIDGE_ORACLE`

A privileged mediator performs the cross-system normalization while downstream evidence remains genuinely useful. Empirical distinguishability may pass; learner bridge attribution must fail.

### `CTRL_RAW_SCENE_ORACLE`

Evaluator adjudication variables or target partition write a robust cue into the world/scene/sensor path upstream of neutral preprocessing. Permuting adjudication bookkeeping while holding the declared physical episode fixed must expose the subsidy where feasible.

### `CTRL_GLOBAL_STATE_WATERMARK`

Target-agnostic privileged telemetry exposes simulator/evaluator latent state to the learner. Remove, randomize, mask, or decorrelate the telemetry while preserving declared participant/world evidence. If bridge performance collapses only when privileged telemetry disappears, the stronger grounding claim fails.

### `CTRL_DESTRUCTIVE_QUOTIENT`

A learner-boundary transform erases a target-relevant distinction while the evaluator retains access to the richer pre-transform state. The evaluator must not credit the learner with evidence it never received.

### `CTRL_POSTHOC_SEMANTIC_NAMING`

A learner discovers a real operational partition; the evaluator selects a human semantic label only after inspecting that partition. The operational result may stand, but the semantic label is exploratory until frozen and tested on independent claim-discriminating evidence.

## Relationship to R1 and R2

### R0.5 owns

- learner-evidence admissibility;
- empirical identifiability relative to declared rivals;
- witness provenance;
- bridge attribution;
- mediation and instrumentation provenance;
- no-destructive-quotient preservation;
- hypothesis-family provenance and limitations;
- boundary-model provenance.

### R1 owns

- fair competition among candidate representation/substrate systems;
- no automatic semantic promotion from representational success.

### R2 owns

- communicative-function/content claims;
- confirmatory versus exploratory semantic naming;
- claim-discriminating interventions/domain shifts;
- structured-alternative stress where strong semantic wording depends on it;
- the final scoped semantic claim ceiling.

## Claim discipline

The project must permit non-monotonic outcomes such as:

- operational relation verified, semantic label unresolved;
- learner bridge attribution clean, semantic interpretation confounded;
- fresh evidence obtained, but not claim-discriminating;
- open/null rival present, but structured-rival adequacy not established;
- interpretation best among declared rivals, broader ontology unresolved.

A conservative certificate should prefer wording such as:

`SUPPORTED_AMONG_DECLARED_RIVALS_WITHIN_TESTED_SCOPE`

or:

`OPERATIONAL_RELATION_VERIFIED / SEMANTIC_QUALIFICATION_PENDING`

rather than `TRUE_MEANING_RECOVERED`.

## Current research ceiling

At this stage, R0.5 is best understood as a provenance-aware identifiability and evidence-admissibility gate.

It should make later semantic claims harder to fake, but it does not itself prove that the surviving cross-system relation deserves the adjective `semantic`.

That question remains deliberately falsifiable downstream.
