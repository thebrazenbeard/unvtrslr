# R3 — Adversarial Pragmatics and Interaction Evaluator

Status: `DESIGN_SPECIFIED / HARNESS_NOT_IMPLEMENTED / NO_PRAGMATIC_QUALIFICATION`

## Purpose

R2 asks whether a communication system has grounded, reusable semantic distinctions rather than a private shortcut code and whether stronger semantic names have earned their additional claim burden.

R3 asks a different question:

> **Can that grounded bridge preserve and use interactional meaning when denotation alone is insufficient?**

R3 targets context, addressee, communicative function, repair, convention state, pragmatic inference, strategic/deceptive use, multimodal conflict, and function-preserving translation.

R3 is additive. It does not rewrite R0.5 experiment-integrity requirements, R1 substrate competition, or R2 grounding/semantic-claim qualification.

## Prerequisite boundary

A candidate should enter a given R3 test only when the semantic structures required by that test are sufficiently available to make the test meaningful.

For example:

- a deictic role-shift test requires a candidate spatial/referential distinction;
- convention-drift testing requires an established candidate convention;
- same-denotation/different-function testing requires the relevant denotation to be separately grounded;
- pragmatic conservation requires source structures that the evaluator can score.

R3 inherits an upstream integrity ceiling from R0.5 and R2:

1. the target distinction must be empirically identifiable within the declared interaction surface or explicitly marked underdetermined;
2. preprocessing must not have destroyed the distinction later credited to the learner;
3. a hidden bridge, adapter, simulator state, instrumentation path, or evaluator label must not have supplied the distinction outside the declared generative path;
4. target claim/rival-family provenance must be explicit, including whether the interpretation is confirmatory or post-hoc;
5. post-hoc semantic or pragmatic interpretations require fresh **claim-discriminating** evidence rather than merely fresh IID evidence;
6. strongest live structured alternatives must be materially stressed or the claim must remain `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`/otherwise bounded;
7. any pragmatic label stronger than a verified operational relation must carry an explicit falsifiable semantic/pragmatic surplus obligation;
8. the final R3 certificate cannot exceed the R0.5/R2 claim ceiling.

R3 may run diagnostic probes before full R0.5/R2 qualification, but **R3 PASS cannot compensate for R0.5 integrity failure, R2 grounding failure, or an unresolved stronger semantic claim**.

## Claims boundary

Passing R3 may support:

`PRAGMATICALLY_GROUNDED_WITHIN_TESTED_SCOPE`

only when the upstream R0.5/R2 claim ceiling permits that wording.

This means only that the candidate discriminated and conserved the preregistered interactional distinctions while the defined shortcut controls failed and the stronger pragmatic interpretation survived its declared surplus obligations.

It does not establish:

- consciousness;
- human-like intention;
- theory of mind as an internal fact;
- benevolence/cooperation;
- universal speech-act categories;
- uniquely correct private mental-state attribution;
- extraterrestrial compatibility outside the tested scope.

Where the operational relation is strong but the pragmatic name remains underdetermined, valid outcomes include weaker statements such as:

- `OPERATIONAL_RELATION_VERIFIED_SEMANTIC_NAMING_UNRESOLVED`;
- `SUPPORTED_AMONG_DECLARED_RIVALS_WITHIN_TESTED_SCOPE`;
- `BEST_SUPPORTED_AMONG_DECLARED_RIVALS_ONLY`;
- `SEMANTIC_INTERPRETATION_STILL_CONFOUNDED`.

## Trust zones

R3 inherits the R0.5/R2 trust-zone logic.

### P0 — Evaluator-only interaction truth

May include:

- intended synthetic function label where a generated world defines one;
- actual addressee/audience assignment;
- hidden sender incentive state;
- whether a signal is intentionally withheld by the generator;
- actual channel-drop/noise events;
- convention version/drift schedule;
- latent source pragmatic structure;
- shortcut-control identity.

Learners must not access P0 except where the declared physical/generative process itself legitimately causes learner-visible evidence. R0.5 must audit extra causal dependencies from evaluator/adjudication state into learner exposure.

### P1 — Learner-visible observations

Only the declared sensory, interaction, communication, task, and public-history information is exposed.

No hidden pragmatic label may leak through filenames, IDs, serialization order, timing artifacts, reward labels, partner identifiers, simulator watermarks, or semantic bridge adapters.

### P2 — Interaction

Participants communicate and act under the frozen challenge protocol.

### P3 — Blind pragmatic adjudication

The evaluator scores immutable traces and substrate/bridge exports after the interaction. The target claim, rival family, thresholds, and semantic/pragmatic surplus obligation must obey the R0.5/R2 confirmatory-versus-exploratory rules.

## Harness qualification before candidate qualification

The R3 harness must first prove that it rejects intentionally deceptive shortcut systems.

Required sequence:

1. applicable R0.5 audit fixtures are qualified for the interaction surface;
2. deterministic replay works;
3. positive pragmatic oracles pass;
4. every required R3 negative control runs;
5. each negative control fails the dimensions it is designed to violate;
6. threshold/margin procedures are calibrated without candidate hidden-test data;
7. challenge generators, target/rival families, semantic/pragmatic surplus obligations, and held-out rules are frozen;
8. only then may an R1/R2 candidate receive a final R3 qualification attempt.

If a shortcut control passes, status is `HARNESS_INVALID`, not “candidate impressive.” If R0.5 provenance or preprocessing/generative integrity remains unresolved, final pragmatic qualification is blocked or claim-limited even if R3 task metrics are high.

## Critical tests

### P01 — Same denotation, different communicative function

**Question:** Can the candidate distinguish interactional function while referential content is held fixed?

**Construction:** Ground referent/world distinction X. Establish two signal families that both concern X but have different experimentally defined consequences, such as information-providing versus request-like, or attention-directing versus warning-like.

**Intervention:** Change receiver action affordances and task incentives while preserving X and the function distinction.

**Pass evidence:** Candidate retains the function distinction beyond the training action mapping and conservation ledger does not collapse them as identical.

**Failure catches:** task-action code; lexical mood classifier; same-referent = same-meaning assumption.

### P02 — Same surface, different context

**Question:** Can context change the supported interpretation without a surface-form change?

**Construction:** Reuse identical signal form under contexts where different meanings/functions are causally established.

**Intervention:** Independently vary relevant context and nuisance context.

**Pass evidence:** Interpretation follows the causal context variable and remains invariant to nuisance shifts.

**Failure catches:** dominant-gloss mapping; episode-ID lookup; flat context memorization.

### P03 — Deictic role shift

**Question:** Does perspective-sensitive meaning track the current indexical ground rather than fixed coordinates?

**Construction:** Establish sender-relative/receiver-relative/landmark-relative reference in a synthetic world.

**Intervention:** swap roles, positions, orientation, and coordinate frame while preserving the relational target.

**Pass evidence:** Candidate updates reference appropriately and records the frame dependency.

**Failure catches:** absolute-coordinate shortcut; fixed speaker-ID rule.

### P04 — Indirect function

**Question:** Can the candidate infer an interactional function not directly encoded by the literal/denotational structure, while preserving inference provenance?

**Construction:** Human controls may use indirect requests/implicature; synthetic controls should define an interaction where literal structure underdetermines the intended function but context/history disambiguates it.

**Pass evidence:** Function is inferred only under supporting context, marked `INFERRED` where appropriate, and rejected under counter-contexts.

**Failure catches:** phrase-template classifier; always-infer-intention bias.

### P05 — Presupposition mismatch

**Question:** Can the system detect when a signal relies on background structure that the receiver does not actually share?

**Construction:** Sender behaves as though background B is established; receiver condition alternates among B-known, B-unknown, and B-false.

**Pass evidence:** candidate distinguishes asserted/current content from background dependency and triggers uncertainty/repair rather than silently injecting B.

**Failure catches:** presupposition-as-fact; shared-context hallucination.

### P06 — Silence or withholding

**Question:** Can absence become a signal only when counterfactual evidence supports an expectation?

**Construction:** Compare strategic withholding against matched random packet loss, latency, sender inactivity, and channel failure.

**Pass evidence:** semantic/pragmatic meaning is assigned to nonoccurrence only in the condition where absence tracks an established causal/interactional variable.

**Failure catches:** absence hallucination; channel-noise semantics.

### P07 — Intended addressee versus overhearer

**Question:** Can the system distinguish who a signal is for from who can observe it?

**Construction:** Signal is visible to multiple agents but targeted to one via orientation/channel/history cues.

**Intervention:** swap addressee while holding form/world state fixed.

**Pass evidence:** addressee hypothesis follows the discriminating cues; overhearer learning does not rewrite intended-target evidence.

**Failure catches:** fastest-responder heuristic; audience = addressee assumption.

### P08 — Audience-dependent behavior

**Question:** Does sender behavior depend causally on who is present or monitoring?

**Construction:** Hold sender information/world state fixed while manipulating audience composition.

**Pass evidence:** candidate identifies and scopes audience-conditioned production without attributing unsupported private motives.

**Failure catches:** partner-ID memorization; untested mental-state narrative.

### P09 — Deceptive sender

**Question:** Can the bridge preserve an established convention while detecting that current use is strategically unreliable?

**Construction:** Establish an honest mapping, then alter sender incentives so some uses become deceptive/misleading.

**Pass evidence:** convention remains identifiable; current claim reliability/strategic hypothesis changes; receiver does not erase semantics merely because truthfulness drops.

**Failure catches:** convention = truth; sender always cooperative assumption.

### P10 — Strategic ambiguity

**Question:** Can the candidate retain several plausible interpretations when sender incentives favor ambiguity?

**Construction:** Sender benefits from receiver choosing one of several interpretations without committing to one.

**Pass evidence:** unresolved alternatives and sender-strategy evidence remain explicit; renderer does not falsely choose certainty.

**Failure catches:** top-1 pragmatic labeler; fluency-driven collapse.

### P11 — Repair after misunderstanding

**Question:** Is repair targeted to the actual mismatch?

**Construction:** Inject distinct failures at channel, segmentation, referent, context, and function layers.

**Pass evidence:** repair behavior discriminates trouble source better than a generic repeat/change policy and improves novel-error performance.

**Failure catches:** `RN04_repair_reflex`.

### P12 — Convention drift

**Question:** Can the system detect and localize gradual change in a once-established mapping?

**Construction:** Alter form, context bounds, function, or referential mapping on a controlled schedule.

**Pass evidence:** candidate weakens/updates the affected convention while preserving unaffected dimensions/history.

**Failure catches:** permanent dictionary; newest-event overwrite; catastrophic full remap.

### P13 — Private shortcut code

**Question:** Can R3 reject a high-performing dyadic code with no transferable pragmatic structure?

**Construction:** Co-trained partners receive a private function/action code unavailable to new partners.

**Pass condition for evaluator:** negative control fails partner transfer, role reversal where applicable, or function-discrimination under changed task.

### P14 — Coordination without reusable semantics

**Question:** Does apparent pragmatic success survive when optimal action changes?

**Construction:** Train messages as direct action selectors; then preserve world/function distinction but alter action policy.

**Pass evidence:** genuine semantic/pragmatic bridge transfers; action code fails.

### P15 — Stable reference, wrong ontology

**Question:** Can a system succeed referentially while representing the wrong distinction?

**Construction:** Training worlds make two latent factors perfectly correlated; communication can ground either. Holdout breaks the correlation.

**Pass evidence:** candidate exposes uncertainty before disambiguation or updates to the factor actually supported by intervention.

**Failure catches:** stable word-object correlation misreported as correct ontology.

### P16 — Role reversal

**Question:** Can pragmatic/conventional structure be used productively in the opposite participant role where the channel permits it?

**Pass evidence:** previous receiver can produce/use/repair the convention under novel cases without a fresh dictionary.

**Scope rule:** physically asymmetric channels may mark `NOT_APPLICABLE_WITH_JUSTIFICATION`; they must not receive false symmetry credit.

### P17 — Partner swap

**Question:** Can a new partner use or acquire the pragmatic convention without private shared state?

**Pass evidence:** transfer or grounded reacquisition succeeds under the preregistered partner condition.

### P18 — Context transfer

**Question:** Does the function mapping survive irrelevant context changes and fail appropriately when relevant context changes?

**Pass evidence:** calibrated selective invariance, not blanket context sensitivity or context blindness.

### P19 — Multimodal channel conflict

**Question:** Can the bridge represent disagreement between channels instead of averaging them into false certainty?

**Construction:** Train mutually consistent modalities, then conflict them on held-out cases.

**Pass evidence:** conflict/provenance is exposed, alternate interpretations remain live, and downstream decisions use declared policy.

### P20 — Function preserved across form and ontology

**Question:** Can two agents preserve a tested interactional function despite radically different surface forms and representational partitions?

**Construction:** Source and target have different sensory/ontological encodings but can establish a common operational invariant.

**Pass evidence:** conserved function survives novel instances, context change, and transfer; ledger records non-equivalent dimensions rather than claiming full identity.

## Operational pragmatic vector

R3 reports at least:

- `FUNCTION_DISCRIMINATION`;
- `CONTEXT_SENSITIVITY`;
- `DEICTIC_GENERALIZATION`;
- `ADDRESSEE_MODELING`;
- `AUDIENCE_MODELING`;
- `INDIRECT_INFERENCE_CALIBRATION`;
- `BACKGROUND_DEPENDENCY_HANDLING`;
- `REPAIR_ROBUSTNESS`;
- `CONVENTION_STABILITY_AND_DRIFT`;
- `PARTNER_TRANSFER`;
- `ROLE_REVERSAL`;
- `STRATEGIC_OR_DECEPTIVE_ROBUSTNESS`;
- `AMBIGUITY_CALIBRATION`;
- `MULTIMODAL_CONFLICT_HANDLING`;
- `PRAGMATIC_CONSERVATION`;
- `SHORTCUT_RESISTANCE`.

Task reward remains separate.

## Threshold policy

R3 follows R2’s candidate-independent threshold discipline.

For each metric `M`, preregister:

- critical versus diagnostic status;
- null/chance distribution;
- positive-oracle distribution;
- strongest relevant negative-control distribution;
- minimum normalized oracle headroom;
- minimum negative-control margin;
- confidence interval method;
- episode/seed requirements;
- applicability conditions.

Do not tune thresholds after viewing candidate hidden-test results. R0.5/R2 target-claim and rival-family freeze rules also apply: hidden candidate behavior may not be used to choose the semantic/pragmatic interpretation later scored as confirmatory.

## Conjunctive critical gates

A high aggregate score cannot compensate for catastrophic failure on an applicable critical distinction.

Examples:

- perfect task reward does not compensate for zero function discrimination;
- good repair does not compensate for evaluator-label leakage;
- partner transfer does not compensate for total pragmatic-conservation failure;
- fluent indirect inference does not compensate for forced intent labels on `UNKNOWN` cases;
- strong R3 metrics do not compensate for `GENERATIVE_PROVENANCE_UNVERIFIED`, destructive preprocessing, or an upstream claim ceiling too weak for the requested pragmatic label.

## Pragmatic conservation audit

For each tested source→target interaction, audit at least:

- denotational/referential structure;
- communicative function;
- addressee/audience;
- context dependence;
- epistemic/evidential status;
- background dependency;
- strategic/reliability status;
- ambiguity;
- form-linked invariant where applicable;
- provenance.

Unsupported target additions are `ADDED`. Hidden collapse is `AMBIGUITY_COLLAPSED`. Context-dependent mappings require `CONTEXT_REQUIRED`.

The audit must also retain the upstream distinction between the verified operational relation and any stronger semantic/pragmatic naming. Conservation of an evaluator-authored label is not evidence that the label was validly grounded.

## R3 harness falsifiers

The R3 harness is invalid if any of these occur:

- a fixed surface speech-act classifier passes cross-form/function tests;
- a repair reflex receives the same repair score as targeted repair;
- partner-ID lookup passes partner swap;
- absolute coordinates pass deictic role shift;
- random packet loss is scored as meaningful withholding;
- a reward predictor passes pragmatic-function discrimination;
- evaluator pragmatic labels leak to the learner;
- an always-intentional labeler is not penalized on noncommunicative/unknown controls;
- pragmatic conservation can drop addressee, uncertainty, or provenance without penalty;
- a synthetic nonhuman positive oracle fails merely because it lacks human sentence/speech-act structure;
- a hidden bridge or simulator/instrumentation feature supplies the distinction and the harness credits the learner;
- a post-hoc pragmatic label is promoted using the same evidence that selected it;
- fresh IID evidence is treated as confirmation despite an unchanged confound;
- a generic `NONE` rival is treated as proof that the structured rival family is adequate.

## R3 certificate

A passing evaluation may emit:

`OPERATIONAL_PRAGMATIC_GROUNDING_CERTIFICATE_V1`

Required fields:

- candidate/substrate version;
- R0.5 audit status and exact claim ceiling;
- R0.5 boundary model, generative-provenance status, and preprocessing-preservation status;
- R2 prerequisite status and scope;
- semantic/pragmatic target claim and rival-family identity;
- semantic/pragmatic interpretation mode: confirmatory versus exploratory/post-hoc;
- claim-discriminating holdout/intervention identity;
- structured-rival adequacy status;
- explicit semantic/pragmatic surplus obligation;
- learner digest;
- evaluator digest;
- R3 contract/profile digest;
- interaction-generator digest;
- sensor/channel configuration;
- partner configuration;
- challenge suite version;
- negative/positive control suite version;
- held-out rule digest;
- seed sets/generation rule;
- operational pragmatic vector with confidence intervals;
- applicable/not-applicable critical tests and justifications;
- surviving alternative explanations;
- conservation audit summary;
- known limitations;
- exact status.

Possible statuses:

- `FAIL`;
- `HARNESS_INVALID`;
- `INDETERMINATE`;
- `PARTIALLY_PRAGMATICALLY_GROUNDED`;
- `PRAGMATICALLY_GROUNDED_WITHIN_TESTED_SCOPE`.

There is intentionally no `UNIVERSAL_PRAGMATICS` status.

If the interactional operational relation passes but the stronger pragmatic naming does not meet its upstream claim/provenance obligations, the R3 report should emit the strongest weaker claim supported rather than force one of the pragmatic-grounding success statuses.

## Relationship to R0.5 and R2

R0.5, R2, and R3 answer different failure questions.

- **R0.5:** Was the distinction actually available, preserved, and attributable to the learner/counterpart interaction under a valid hypothesis-family provenance and boundary model?
- **R2:** Is the operational relation grounded/reusable rather than a shortcut, and does any stronger semantic name survive its additional falsifiable claim burden?
- **R3:** Given those prerequisites, are interactional/pragmatic distinctions preserved, discriminated, transferred, and conserved under adversarial conditions?

A candidate can therefore be:

- R0.5 FAIL/UNRESOLVED with high downstream metrics: no final semantic/pragmatic qualification;
- R2 FAIL / R3 diagnostic high: good at human-like interaction patterns without grounded semantics;
- R2 PASS at operational level / stronger semantic name unresolved: R3 may diagnose function-like structure but cannot silently promote the stronger label;
- R2 PASS / R3 FAIL: grounded denotational bridge that loses context/function;
- R0.5 + R2 + R3 PASS within the same bound scope: strongest current candidate for grounded semantic mediation with interactional robustness;
- any prerequisite INDETERMINATE: final claim remains bounded accordingly.

R3 never retroactively changes the meaning of an R0.5 or R2 result and cannot exceed their claim ceiling.

## Research standard

The objective is not to make UNVTRSLR imitate human conversation.

The objective is to make it difficult for a translator to claim semantic success while silently losing the kinds of distinctions that human pragmatics, multimodal communication, strategic signaling, and interaction research show can matter—and to do so without assuming those human manifestations are universal or allowing experiment infrastructure/post-hoc labeling to manufacture the distinction being credited.
