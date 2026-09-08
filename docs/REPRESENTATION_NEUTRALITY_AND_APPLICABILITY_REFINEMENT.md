# Representation Neutrality and Applicability Refinement

Status: `POST_PASS3_DESIGN_REFINEMENT / PROVISIONAL / NOT_CANON / NOT_MERGED`

Predecessor checkpoint: `POST_PASS3_QUALIFICATION_REFINEMENT_1@5d38ea3f2a5e3f5108d12f91cba6e331050ca3c9`.

This document answers the current One/Four/Nine/Thirteen pressure on hidden representation primitives after the nonhuman communication pass. It is a design refinement, not a qualification result.

## 1. Replace `operational partition` as the default primitive

`operational partition` is too discrete for a general semantic bootstrap.

Use:

`VERIFIED_OPERATIONAL_RELATION`

A relation can instantiate any empirically supported structure, including:

- discrete partition;
- ordering;
- metric or pseudometric;
- continuous transform;
- conditional dependence;
- response function;
- dynamical coupling;
- field relation;
- trajectory relation;
- many-to-many correspondence;
- probabilistic relation;
- unresolved/other structure.

A partition is therefore one possible relation form, not the architecture's default ontology.

### Required metadata

For every verified operational relation, record:

- `relation_id`;
- `relation_form`;
- `learner_accessible_evidence`;
- `distinguishing_controls`;
- `scope`;
- `uncertainty`;
- `transfer_regimes[]`;
- `known_failures[]`;
- `human_rendering` if any;
- `rendering_status`.

## 2. Replace ontological `agent` assumptions with auditable access/influence scopes

The project may continue using `agent` in the controlled dyadic fixture, but the general evaluator should use the weaker provenance handle:

`ACCESS_INFLUENCE_SCOPE`

Definition:

> an experiment-defined record of the learner-accessible exposure paths and influence paths relevant to a claim.

A scope may be:

- one organism/process;
- several coordinated processes;
- distributed in space;
- overlapping another scope;
- time-varying;
- collectively authored;
- experimenter-declared;
- learner-discovered;
- mixed;
- unresolved.

The scope exists in the audit because the experiment needs an information-flow boundary. It is not automatically a natural cognitive individual.

### Required fields

- `scope_id`;
- `scope_definition`;
- `scope_author`;
- `exposure_paths[]`;
- `influence_paths[]`;
- `overlaps_with[]`;
- `time_variation`;
- `boundary_model_status`;
- `claim_dependency_on_individuation`.

### Claim rule

If changing the scope decomposition changes whether a semantic claim passes, the claim must state that dependency. Do not silently promote one experimenter individuation into a universal fact.

## 3. No-destructive-quotient rule without a stable source-side history primitive

Earlier formulations referred to `source-side histories`. Persistent fields, asynchronous traces, distributed state, or coupled sensing/communication can make `history` itself unnecessarily strong.

Use a more operational condition.

Let `E` be the learner-accessible exposure state/process under the declared experiment and `F(E)` the learner-bound representation after preprocessing.

For target claim family `H`, preprocessing is admissible only if the evaluator has no demonstrated pair/set of learner-accessible exposure conditions `E1...En` such that:

1. the conditions are distinguishable under the native experiment at the learner boundary before `F`;
2. that distinction is required to discriminate live rivals in `H`;
3. `F` collapses the conditions so the distinction is no longer recoverable within declared tolerance/budget;
4. the evaluator nevertheless credits the learner with recovering the lost distinction.

This avoids assuming discrete events, total time order, messages, channels, or stable object histories.

### Required status

`PREPROCESSING_PRESERVATION_STATUS = PRESERVED_FOR_CLAIM | LOSS_DECLARED_CLAIM_NARROWED | DESTRUCTIVE_QUOTIENT_DETECTED | UNKNOWN`

`UNKNOWN` cannot be treated as neutral.

## 4. Applicability is a separate scientific claim

For each First-100 challenge, applicability must be adjudicated independently from performance.

Required states:

- `APPLICABLE_TESTED`;
- `STRUCTURALLY_INAPPLICABLE_IN_SCOPE`;
- `APPLICABILITY_UNRESOLVED`.

### Anti-evasion requirements

`STRUCTURALLY_INAPPLICABLE_IN_SCOPE` requires, where feasible:

1. a representation-neutral statement of the capability/prerequisite;
2. positive evidence that a necessary prerequisite is absent or structurally unavailable;
3. evidence not derived solely from the candidate failing the challenge;
4. an attempted cross-system variant if one can test the same operational capability without the disputed human ontology;
5. preregistered applicability rules or independent blind audit;
6. a falsifiable re-entry condition;
7. explicit coverage reduction.

A failure cannot be retroactively relabeled `NOT_APPLICABLE` simply because the candidate did poorly.

### Coverage reporting

Report:

`passed / applicable / total`

and separately:

`inapplicable / unresolved / total`.

No excluded challenge increases the pass numerator.

## 5. Semantic-status ladder

To keep semantic language from outrunning evidence, use explicit claim levels.

### S0 — `OBSERVABLE_REGULARITY`

Repeatable structure exists in learner-accessible evidence.

### S1 — `VERIFIED_OPERATIONAL_RELATION`

A reusable relation survives declared controls, transfer, or intervention-like tests within scope.

### S2 — `CROSS_SYSTEM_CORRESPONDENCE`

The relation links distinguishable structures across two or more access/influence scopes or representations and survives bridge-attribution/provenance controls.

This level does not yet require a human semantic label.

### S3 — `SEMANTIC_CORRESPONDENCE_CANDIDATE`

A proposed semantic interpretation is frozen and entails at least one claim-discriminating obligation beyond the strongest live nonsemantic operational rival.

### S4 — `SEMANTIC_CORRESPONDENCE_SUPPORTED_IN_SCOPE`

The candidate interpretation survives independent claim-discriminating evidence, structured-rival pressure, instrumentation/shortcut controls, and the stated semantic-surplus obligation.

### S5 — no universal level

The architecture must not silently promote S4 to `TRUE_MEANING` or universal semantics. S4 remains scoped to tested systems, environments, interventions, rival families, and budgets.

## 6. Semantic surplus as an empirical burden, not a definition by fiat

The word `semantic` should add a test burden.

Let `R` be the strongest verified nonsemantic relation and `S` the proposed semantic interpretation.

`S` is not promoted merely because humans find it intuitive, compressive, or predictive.

It must add at least one preregistered obligation that `R` does not already entail, such as a novel-context transfer, substitution, counterfactual, conservation, role-reversal where appropriate, intervention, or non-equivalence prediction.

If no such obligation can be identified, retain:

`VERIFIED_OPERATIONAL_RELATION / HUMAN_RENDERING_ONLY`.

This rule does not claim to solve philosophy of meaning. It makes the project's use of semantic terminology falsifiable inside an experimental program.

## 7. Instrumentation neutrality is never assumed from target-independence

A target-agnostic latent-state watermark can still provide privileged supervision.

For every learner-visible feature derived directly or indirectly from simulator/evaluator latent state outside the declared participant/world causal path, record:

- provenance source;
- transform chain;
- whether participants could access an equivalent physical variable through the declared world;
- whether feature removal/randomization materially changes bridge performance;
- whether the feature is necessary for ordinary rendering/physics or only instrumentation/evaluation convenience.

Target-partition permutation remains useful but is insufficient alone.

## 8. Fresh evidence versus discriminating evidence

Keep four independent properties:

- `DATA_FRESHNESS`;
- `DISTRIBUTION_RELATION_TO_TRAINING`;
- `RIVAL_DISCRIMINATION_POWER`;
- `INTERVENTION_OR_SHIFT_STATUS`.

Fresh IID data may have low rival-discrimination power.

A semantic claim requiring discrimination between `S` and a structured rival `R` cannot be confirmed on a holdout where `S` and `R` make the same predictions.

## 9. Rival-family adequacy remains open by default

Use:

- `REJECTION_ESCAPE_PRESENT`;
- `STRUCTURED_ALTERNATIVE_STRESS_NOT_ESTABLISHED`;
- `STRUCTURED_ALTERNATIVE_STRESS_TESTED`;
- `RIVAL_FAMILY_MISSPECIFICATION_DETECTED`;
- `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`.

A null/open alternative prevents forced choice. It does not prove that all relevant structured alternatives have been represented.

## 10. Relationship to the First 100

The First 100 remain a broad adversarial challenge inventory.

They are not:

- 100 universal concepts;
- a fixed developmental sequence;
- a requirement that every observed communication system instantiate human agency, objecthood, speech acts, explicit repair, or symbolic composition.

Each challenge should eventually bind:

- a representation-neutral operational capability;
- applicability prerequisites;
- cross-system variants;
- claim ceiling;
- false-success controls;
- semantic-status level reached.

## 11. Current falsifiable core

The strongest current bootstrap claim should be expressed conservatively:

> Under declared conditions where learner-accessible exposure contains recoverable distinguishing structure, preprocessing preserves claim-relevant distinctions, privileged instrumentation does not supply the cross-system bridge, and rival hypotheses can be discriminated within scope, initially unaligned systems may be able to construct reusable cross-system operational correspondences without a pre-shared symbolic language.

Whether a correspondence deserves the stronger label `semantic` is a separate qualification question, not something the bootstrap receives by definition.

This separation is intentional. If the project cannot state an empirical obligation added by the semantic interpretation beyond the operational relation, the correct scientific result is still valuable but should remain below the semantic claim ceiling.
