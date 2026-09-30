# Post-Pass-3 Methodological Analogues for Semantic Qualification

Status: `POST_PASS3_METHOD_RESEARCH / PROVISIONAL / NOT_CANON`

Source checkpoint preserved: `NONHUMAN_COMMUNICATION_PASS_3@ca6cc0c4fe176d2097b6d0aee0e18f9a9ea4a8a2`.

This note does **not** modify the frozen Pass 3 research subject. It records methodological analogues from statistics, machine learning, neuroscience, and model criticism that bear on the adversarial controls raised during the One/Four/Nine/Thirteen review round.

The mappings below are analogies. None of these prior works directly implements UNVTRSLR's full zero-shared-symbol semantic bootstrap.

## 1. Hidden target-relevant instrumentation and shortcut learning

### Lapuschkin et al. (2019) — Clever Hans predictors

Lapuschkin, S. et al. *Unmasking Clever Hans predictors and assessing what machines really learn*. Nature Communications 10, 1096 (2019). DOI `10.1038/s41467-019-08987-4`.

The study shows that high benchmark accuracy can be supported by unintended dataset artifacts rather than the intended task structure. A memorable example is an image classifier exploiting a source tag associated with horse images.

**Methodological analogue:** this supports the general warning behind `CTRL_GLOBAL_STATE_WATERMARK`: a learner-visible feature can be highly predictive and stable while being causally irrelevant to the intended semantic relation. Standard task success need not reveal the wrong strategy.

**Claim ceiling:** the paper does not study simulator latent-state watermarks or semantic grounding; it supports the broader shortcut/artifact failure mode.

### Geirhos et al. (2020) — shortcut learning

Geirhos, R. et al. *Shortcut learning in deep neural networks*. Nature Machine Intelligence 2, 665-673 (2020). DOI `10.1038/s42256-020-00257-z`.

The paper frames many ML failures as reliance on decision rules that work on standard benchmarks but fail under more challenging transfer conditions.

**Methodological analogue:** a semantic bootstrap can appear successful under ordinary evaluation while relying on an unintended latent cue. Robust semantic qualification therefore needs strategy-discriminating tests, not only success on an IID benchmark.

### Hidden acquisition/site information in medical imaging

Recent medical-imaging shortcut work shows that models can recover clinical site, scanner/manufacturer, protocol, markers, or other acquisition-related variables from images and use them as shortcuts. This is especially relevant because the information may be diffusely encoded rather than appearing as one obvious label or watermark.

Representative sources:

- *The risk of shortcutting in deep learning algorithms for medical imaging research*. Scientific Reports (2024).
- Ross et al. *Shortcut learning in medical AI hinders generalization: method for estimating AI model generalization without external data*. npj Digital Medicine 7, 124 (2024).

**Methodological analogue:** removing one obvious target-conditioned leak is not sufficient evidence that the observation surface is clean. An entire instrumentation/acquisition pipeline can carry target-relevant side information.

**UNVTRSLR consequence:** distinguish declared participant/world causal evidence from learner-visible observer/instrumentation telemetry, and require ablation or perturbation of privileged telemetry where it could support the tested relation.

## 2. Fresh IID holdout does not prove the intended invariant

### Geirhos et al. (2020)

Shortcut rules can perform well on standard benchmarks and fail only when the testing conditions change in a way that breaks the shortcut.

### WILDS — distribution-shift evaluation

Koh, P. W. et al. *WILDS: A Benchmark of in-the-Wild Distribution Shifts*. Proceedings of ICML 2021, PMLR 139:5637-5664.

WILDS demonstrates large gaps between in-distribution and out-of-distribution performance across multiple real application domains.

**Methodological analogue:** a genuinely fresh sample from the same confounded distribution can preserve the same shortcut. Freshness is therefore weaker than a holdout designed to discriminate the intended claim from live alternative explanations.

**UNVTRSLR consequence:** `FRESH_EVIDENCE` and `CLAIM_DISCRIMINATING_EVIDENCE` must be separate statuses. A semantic interpretation should not be promoted merely because it predicts an IID holdout if a plausible structured rival makes the same predictions there.

## 3. Post-hoc semantic naming and circular selection

### Kriegeskorte et al. (2009) — double dipping

Kriegeskorte, N., Simmons, W. K., Bellgowan, P. S. F. & Baker, C. I. *Circular analysis in systems neuroscience: the dangers of double dipping*. Nature Neuroscience 12, 535-540 (2009). DOI `10.1038/nn.2303`.

The paper shows that selecting data/features based on a criterion and then using the same data for selective inference can produce distorted estimates and spurious significance. It recommends independent data when the selection and test are not inherently independent.

**Methodological analogue:** selecting a human-readable semantic interpretation after inspecting a learned operational partition and then 'confirming' that interpretation on the same evidence is a semantic version of non-independent selection.

**UNVTRSLR consequence:** preserve the split between `EXPLORATORY_POST_HOC_INTERPRETATION` and `CONFIRMATORY_TARGET_CLAIM`; post-hoc labels require a separately frozen follow-up test.

## 4. A null/open rival is not proof that the model family is adequate

### Kruschke (2013) — inference is conditional on the assumed model space

Kruschke, J. K. *Posterior predictive checks can and should be Bayesian*. British Journal of Mathematical and Statistical Psychology 66(1), 45-56 (2013). DOI `10.1111/j.2044-8317.2012.02063.x`.

Kruschke emphasizes that inference over an assumed model space can identify the least-bad available option without establishing that the available model actually fits adequately.

### Model misspecification literature

Representative sources:

- *Bayesian Inference for Misspecified Generative Models*. Annual Review of Statistics and Its Application (2024). DOI `10.1146/annurev-statistics-040522-015915`.
- *Errors in Statistical Inference Under Model Misspecification: Evidence, Hypothesis Testing, and AIC* (2020/2021 literature).

**Methodological analogue:** `NONE_OF_DECLARED_RIVALS` is useful as a rejection escape, but it does not generate a missing structured alternative. A named semantic rival can still win because the relevant competitor was never represented.

**UNVTRSLR consequence:** separate `REJECTION_ESCAPE_PRESENT` from `STRUCTURED_RIVAL_FAMILY_ADEQUACY`. Strong semantic qualification requires explicit alternative-generation/model-criticism pressure or a correspondingly low claim ceiling.

## 5. Holdout/model criticism helps, but the test must target the claim

Holdout predictive checks and split predictive checks address double use of data and improve calibration for model criticism. Recent work includes:

- *Holdout predictive checks for Bayesian model criticism*, Journal of the Royal Statistical Society Series B 86(1), 194-214 (2024 issue / online 2023).
- Li, J. & Huggins, J. H. *Calibrated Model Criticism Using Split Predictive Checks*. Journal of the American Statistical Association (2026). DOI `10.1080/01621459.2026.2649585`.

**Methodological analogue:** independent holdout evidence is valuable for detecting misspecification and circularity.

**Important limit for UNVTRSLR:** independence alone does not ensure that the holdout distinguishes the semantic claim from its strongest live rival. That stronger requirement is a project design inference, not something these papers directly prove.

## 6. Exposure/control loci are provenance handles, not natural entities

The nonhuman pass already showed communication can be collective, persistent, distributed, asynchronous, or fused with sensing. The provisional `EXPOSURE_CONTROL_LOCUS` therefore should be interpreted only as an experiment-level provenance handle over an access/influence boundary.

A locus may be:

- transient;
- overlapping with another locus;
- distributed over several processes;
- time-varying;
- experimenter-declared rather than discovered by the learner.

Any claim requiring stable individuation into `agent A` and `agent B` must bind that assumption explicitly.

## 7. Proposed semantic-surplus criterion

This is a **project hypothesis/design proposal**, not a result established by the cited literature.

A useful way to keep the adjective `semantic` falsifiable is to require a semantic interpretation to add at least one test obligation beyond the strongest verified operational/predictive relation.

Candidate rule:

`SEMANTIC_SURPLUS_TEST`

A proposed semantic interpretation `S` is promotable beyond `VERIFIED_OPERATIONAL_RELATION` only if `S` entails at least one preregistered, claim-discriminating prediction/intervention/transfer/conservation obligation that is **not already entailed** by the strongest nonsemantic operational rival `R`, and `S` survives that test.

If no such discriminating obligation can be stated, the semantic label may remain useful as a human rendering, but it has not added falsifiable scientific content.

This criterion is deliberately defeasible. One/Four/Thirteen should attack whether it is too strict, too weak, or simply relocates the semantic definition problem.

## 8. `NOT_APPLICABLE` anti-evasion requirement

Pass 3 introduced `NOT_APPLICABLE_TO_OBSERVED_COMMUNICATION_SYSTEM` so human-heavy challenges do not become false universal prerequisites. That status needs an anti-evasion gate.

Proposed discipline:

1. applicability is a separate adjudication from performance;
2. the prerequisite/ontology that makes the challenge applicable must be named;
3. the evidence for absence of that prerequisite must be bound;
4. when feasible, applicability rules are frozen before the candidate result is inspected;
5. `APPLICABILITY_UNRESOLVED` is not a pass and must not be silently converted to `NOT_APPLICABLE`;
6. challenge coverage is reported explicitly: `passed/applicable/total`, never as `100 passed` when some challenges were excluded;
7. if later evidence establishes the prerequisite, the challenge re-enters the applicable set;
8. `NOT_APPLICABLE` may lower universality/coverage claims but must not be counted as semantic success.

Strongest allowed aggregate wording should distinguish:

- `FIRST_100_ALL_APPLICABLE_AND_PASSED`;
- `FIRST_100_APPLICABLE_SUBSET_PASSED (k/100 applicable)`;
- `APPLICABILITY_UNRESOLVED`.

This preserves non-anthropocentric evaluation without turning inapplicability into an escape hatch.

## Current methodological synthesis

The strongest cross-disciplinary support is for a conservative evaluation pattern:

`verify operational relation`
`-> audit information provenance / hidden shortcuts`
`-> separate exploratory selection from confirmatory testing`
`-> test under conditions that break plausible confounds`
`-> criticize the rival/model family rather than only choosing its winner`
`-> promote a semantic interpretation only at the claim ceiling the tests actually support`.

This note does not establish that UNVTRSLR is feasible, that any particular representation is canonical, or that a tested relation is semantic merely because it survives these controls.
