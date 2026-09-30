# Post-Pass-3 Methodological Analogues — Supplement 1

Status: `FOLLOWUP_METHOD_RESEARCH / PROVISIONAL / NOT_CANON`

Predecessor checkpoint: `POST_PASS3_QUALIFICATION_REFINEMENT_1@5d38ea3f2a5e3f5108d12f91cba6e331050ca3c9`.

This supplement extends `research/POST_PASS3_METHOD_ANALOGUES.md`. The cited work is used as methodological analogy only. None of these papers demonstrates UNVTRSLR's zero-shared-symbol semantic bootstrap or licenses stronger semantic claims by itself.

## 1. IID success can coexist with shortcut dependence

### Tu, Lalwani, Gella & He (2020)

*An Empirical Study on Robustness to Spurious Correlations using Pre-trained Language Models*. Transactions of the Association for Computational Linguistics 8:621-633. DOI `10.1162/tacl_a_00335`.

Source: https://aclanthology.org/2020.tacl-1.40/

The paper explicitly distinguishes ordinary IID evaluation from challenging datasets where known spurious correlations no longer hold. Models can perform strongly in-distribution and then collapse when those correlations are broken.

**UNVTRSLR analogue:** a fresh sample from the same environment family does not establish that a learned bridge tracks the intended semantic relation. A qualification set must contain examples or interventions that separate the intended claim from live shortcut alternatives.

**Control pressure:** strengthens `CTRL_CLAIM_DISCRIMINATING_HOLDOUT` and the distinction between `FRESH_BUT_NONDISCRIMINATING_EVIDENCE` and `CLAIM_DISCRIMINATING_HOLDOUT`.

## 2. Invariance across environments is stronger evidence than single-regime prediction

### Peters, Bühlmann & Meinshausen (2016)

*Causal Inference by using Invariant Prediction: Identification and Confidence Intervals*. Journal of the Royal Statistical Society Series B 78(5):947-1012. DOI `10.1111/rssb.12167`.

Source: https://doi.org/10.1111/rssb.12167

The method exploits predictive relations that remain invariant across different experimental settings/interventions. The paper also emphasizes that causal predictors may be unidentifiable in a given set of environments, in which case the procedure should not make false causal discoveries.

**UNVTRSLR analogue:** semantic qualification should prefer tests that alter nuisance structure or environmental regime while preserving the claimed relation, and should retain an honest underdetermination state when no available regime separates rival explanations.

**Claim ceiling:** invariant prediction is a causal-inference framework, not a theory of meaning. UNVTRSLR borrows the methodological principle that robustness across discriminating environments is stronger evidence than repeated prediction inside one confounded regime.

## 3. Dataset/instrumentation provenance can itself create shortcuts

### Compton, Zhang, Puli & Ranganath (2023)

*When More is Less: Incorporating Additional Datasets Can Hurt Performance By Introducing Spurious Correlations*. Proceedings of Machine Learning Research 219:110-127.

Source: https://proceedings.mlr.press/v219/compton23a.html

The study shows that hospital/source-specific artifacts can induce spurious disease correlations and degrade worst-group performance even when more data are added.

**UNVTRSLR analogue:** acquisition/site/render/sensor provenance can carry target-relevant information independently of the intended participant relation. A learner may exploit that information without any explicit target-conditioned watermark.

**Control pressure:** supports the broader instrumentation threat model behind `CTRL_GLOBAL_STATE_WATERMARK`: target-independence does not imply semantic neutrality. Learner-visible features derived from privileged simulator/evaluator state require provenance classification and ablation where they could support the claimed bridge.

## 4. A null/open option does not establish model-family adequacy

### Aho et al. / model misspecification literature

Representative open-access discussion: *Errors in Statistical Inference Under Model Misspecification: Evidence, Hypothesis Testing, and AIC* (Ecology and Evolution, 2021; PMCID `PMC8293863`).

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC8293863/

A central misspecification problem is that neither the null nor the tested alternative need adequately describe the data. Selecting one member of a restricted family does not establish that the family contains the right explanation.

**UNVTRSLR analogue:** `NONE_OF_DECLARED_RIVALS` is only a rejection escape. It does not generate a missing structured alternative, and its loss to a named human semantic label does not prove that the named label is adequate.

**Control pressure:** retain separate statuses for `REJECTION_ESCAPE_PRESENT` and `STRUCTURED_ALTERNATIVE_STRESS_TESTED`; otherwise the strongest honest wording remains `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`.

## 5. Human-language / animal-communication comparison itself has measurement bias

### *Overcoming bias in the comparison of human language and animal communication* (2023)

Open-access source: https://pmc.ncbi.nlm.nih.gov/articles/PMC10666095/

The paper argues that standard animal-communication methods often privilege isolated signals with predictable immediate behavioral responses, while human language routinely conveys content without immediate overt action. This creates a methodological bias in what researchers are able to call meaningful.

**UNVTRSLR analogue:** human-style response criteria cannot become hidden universal applicability rules. A persistent field, delayed receiver effect, internal-state update, or distributed interaction may support a communication hypothesis even when no immediate discrete response exists.

**Control pressure:** strengthens `CTRL_NOT_APPLICABLE_EVASION` in both directions:

1. do not mark a hard challenge `NOT_APPLICABLE` merely because the tested system lacks a human-style response;
2. do not mark a challenge `APPLICABLE` merely because the evaluator can force the system into a human response ontology.

Applicability must be tied to the operational capability being tested, not the human surface form of the test.

## 6. Representation-neutrality consequence: prefer relations over partitions

The current coordination language sometimes says `operational partition`. That phrase is useful for discrete classification examples but is too strong as a general primitive.

Nonhuman and multimodal evidence permits stable relations that are:

- continuous rather than partitioned;
- graded or probabilistic;
- field-like;
- trajectory-based;
- temporally persistent;
- many-to-many;
- context-indexed;
- collective rather than attributable to one participant.

The weaker project term should be:

`VERIFIED_OPERATIONAL_RELATION`

A partition is one special case.

For a candidate relation `R`, record the native mathematical/empirical form actually supported: partition, metric, ordering, conditional dependence, dynamical coupling, transform, field relation, response function, or `OTHER/UNRESOLVED`.

Do not coerce a continuous or relational result into categories solely to make semantic scoring convenient.

## 7. Boundary-neutrality consequence: `locus` is bookkeeping, not ontology

`EXPOSURE_CONTROL_LOCUS` is safer than `agent`, but `locus` can still sound spatially localized and stable. The strongest interpretation is explicitly administrative:

`ACCESS_INFLUENCE_SCOPE`

An access/influence scope is an experiment-defined record of where observations can enter a process and where actions/state changes can influence the tested coupled system. It may be spatially distributed, overlapping, time-varying, collective, or unresolved.

Recommended provenance fields:

- `scope_id`;
- `scope_definition`;
- `scope_author = EXPERIMENTER | LEARNER | MIXED | UNRESOLVED`;
- `exposure_paths[]`;
- `influence_paths[]`;
- `overlaps_with[]`;
- `time_variation`;
- `individuation_dependency`;
- `claim_effect_if_boundary_changes`.

This is not a claim that nature contains discrete scopes. It is a way to audit what the experiment assumed.

## 8. Stronger anti-evasion rule for `NOT_APPLICABLE`

`STRUCTURALLY_INAPPLICABLE_IN_SCOPE` should require all of the following where feasible:

1. the challenge's operational capability and prerequisites are stated without human surface-form dependence;
2. evidence that a required prerequisite is absent is independent of the candidate's failure on the challenge;
3. the evaluator attempts a representation-neutral/cross-system variant before exclusion when such a variant is coherent;
4. applicability is frozen before candidate scoring or independently audited afterward;
5. `APPLICABILITY_UNRESOLVED` remains distinct and cannot count as pass or exclusion;
6. exclusions reduce coverage and any universality claim;
7. evidence that later establishes the prerequisite automatically reopens the challenge;
8. the reason for exclusion is testable enough that an adversary could falsify it.

A candidate's statement `I cannot do this` is not evidence of inapplicability. Failure behavior cannot be used circularly to shrink the applicable set.

## 9. Current synthesis

The follow-up research strengthens a conservative sequence:

`discover/verify an operational relation`
`-> classify learner-visible evidence provenance`
`-> challenge shortcuts under non-IID or intervention-like conditions`
`-> keep model-family adequacy separate from winner selection`
`-> keep applicability independent of candidate failure`
`-> only then test whether a semantic rendering adds claim-discriminating obligations`.

The research does not establish that this sequence is sufficient for semantics. It establishes why weaker evaluation patterns are vulnerable to known classes of false success.
