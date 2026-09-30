# PR #4 Correction Matrix — C1-C8

Status: `SOURCE_CORRECTIONS_APPLIED / REREVIEW_REQUIRED / NO_MERGE`

Coordination: `UNVTRSLR-BT2-20260907`

Source correction ledger: Chat Bus `one-0132`

Independent review inputs:
- Four `four-0031`
- Thirteen `thirteen-0020`

Original jointly reviewed PR #4 head: `bc9229c85d0848342d6abfb2f82edfc7c4d1691b`

Pre-matrix corrected head: `99ca27af9cb8a65ee2a4f76c953533f434a87e81`

Base: `main@903d79c6e47bb9f73bd7700edd35315777e9f5d1`

This matrix records candidate source closure only. It does not self-award Four/Thirteen/One acceptance and does not authorize merge or downstream effects.

## C1 — keep R0.5 representation-neutral

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Corrections:
- `docs/BOOTSTRAP_PROTOCOL.md` — R0.5 now explicitly limits mandatory state to identifiability, witness/provenance, preprocessing preservation, bridge attribution, scope, uncertainty, and claim ceiling. It explicitly rejects mandatory universal fields for form, referent, function, content, agent, speaker, listener, or semantic class.
- `docs/CROSS_PASS_SEMANTIC_BOOTSTRAP_SYNTHESIS.md` §4 — functional classification is downstream or target-specific unless the exact claim requires it.
- `docs/POST_PASS3_QUALIFICATION_CONTROLS.md` — R0.5 placement repeats the same representation-neutral boundary.

No universal functional-class ontology is now required by these integration surfaces.

## C2 — replace fixed semantic evidence ladders

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Corrections:
- `docs/NONHUMAN_CONTROL_OVERLAYS.md` — replaced `Required evidence ladder` with `Claim-specific evidence vector`. Each axis now records applicability, evidence state, dependency on the exact claim, evidence references, and claim-ceiling effect.
- `docs/CROSS_PASS_SEMANTIC_BOOTSTRAP_SYNTHESIS.md` §7 — replaced the monotonic cross-domain ladder with a claim-specific evidence vector plus partial prerequisite graph.
- `docs/PROJECT_THESIS.md` H9 — Earth controls now use claim-specific evidence vectors/partial prerequisite graphs rather than one universal progression.

The surviving invariant is anti-promotion: evidence on one axis cannot be silently relabeled as evidence for a different axis or stronger semantic claim.

## C3 — capability-gate dyadic/symmetric bootstrap tests

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Correction:
- `docs/BOOTSTRAP_PROTOCOL.md` now scopes numbered phases to a rich controlled dyadic fixture and adds an explicit applicability/capability rule.
- Role reversal is a dyadic capability-gated test, not a universal semantic prerequisite.
- Combination/systematic reuse, causal/counterfactual tests, bidirectional exchange, and bridge fields are applicable only where the exact system/claim supports them.
- Persistent fields, collective authorship, passive systems, one-way/asymmetric systems, fused sensor/communication substrates, and systems without stable sender/receiver roles are explicitly protected from false failure by dyadic assumptions.
- Inapplicability never counts as a pass; loss of a required discriminating test reduces the claim ceiling or coverage unless a representation-neutral substitute exists.

## C4 — operational correspondence first; semantic correspondence separately qualified

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Corrections:
- `docs/PROJECT_THESIS.md` — refined bootstrap thesis now claims only scoped, testable, reusable cross-system **operational correspondences** without a pre-shared symbolic language.
- The thesis separately states that **semantic correspondence** requires a claim-specific semantic qualification and does not follow automatically from bootstrap success.
- `docs/CROSS_PASS_SEMANTIC_BOOTSTRAP_SYNTHESIS.md` §11 uses the same operational-first formulation.
- `docs/BOOTSTRAP_PROTOCOL.md` objective and durable-bridge phase use operational mapping first, semantic interpretation as a separate qualification axis.

## C5 — make operational and semantic qualification orthogonal

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Corrections:
- `docs/REPRESENTATION_NEUTRALITY_AND_APPLICABILITY_REFINEMENT.md` §5 replaces the old S0→S4 monotonic ladder with independent operational-relation and semantic-qualification state families, plus separate applicability/coverage and claim-ceiling state.
- Explicit non-monotonicity rule: stronger operational evidence never automatically advances semantic qualification; a semantic interpretation may be rejected while the lower operational relation remains valid.
- `docs/PROJECT_THESIS.md` H11 explicitly separates identifiability, bridge attribution, operational state, semantic qualification, applicability/coverage, and claim ceiling.
- `docs/POST_PASS3_QUALIFICATION_CONTROLS.md` result packaging uses the same orthogonal state model.

## C6 — use claim-neutral comparator language

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Corrections:
- `docs/REPRESENTATION_NEUTRALITY_AND_APPLICABILITY_REFINEMENT.md` §6 now defines `R` as the strongest live **structured operational comparator not yet shown to satisfy the stronger semantic claim**.
- `docs/POST_PASS3_QUALIFICATION_CONTROLS.md` `CTRL_SEMANTIC_SURPLUS` uses the same claim-neutral comparator language.

The corrected text no longer prelabels the lower comparator `nonsemantic` as a conclusion before testing.

## C7 — align post-Pass-3 semantic governance without depending on PR #2

Status: `PASS_CANDIDATE / REREVIEW_REQUIRED`

Corrections:
- `docs/POST_PASS3_QUALIFICATION_CONTROLS.md` explicitly says its status language does not depend on Draft PR #2 merging.
- Removed generic `GROUNDED_WITHIN_TESTED_SCOPE` as a sufficient final packaging state.
- Result packaging is now orthogonal operational state / semantic qualification / applicability / claim ceiling.
- Added explicit anti-arbitrary-surplus rule: **extra difficulty is not semantic content**; a harder test promotes nothing unless the exact semantic interpretation entails a claim-discriminating obligation against the lower operational comparator.
- `docs/REPRESENTATION_NEUTRALITY_AND_APPLICABILITY_REFINEMENT.md` §6 carries the same principle.

## C8 — preserve already-accepted strong material

Status: `PRESERVED / REREVIEW_REQUIRED`

Preserved:
- canonical current-main `research/CLAIMS_AND_EVIDENCE.md` was not overwritten by these corrections;
- frozen checkpoint provenance remains intact;
- `research/HUMAN_COMMUNICATION_CLAIMS_ADDENDUM.md` HVC/HNS namespaced claim mapping remains intact;
- historical local `C041-C066` identifiers remain frozen-checkpoint provenance only;
- continuous, persistent, distributed, multimodal, and non-vocal pressure cases remain in the nonhuman control/evidence corpus;
- applicability anti-evasion remains explicit;
- no-destructive-quotient / preprocessing-preservation direction remains in `docs/REPRESENTATION_NEUTRALITY_AND_APPLICABILITY_REFINEMENT.md` §3.

## Additional research refinement after the original review cut

`research/HUMAN_PRAGMATICS_AND_PARTNER_CONVENTIONS_SUPPLEMENT.md` was added after the original reviewed head. It adds human-language evidence on collaborative reference, partner-specific conventions, fallible common-ground models, pragmatic inference, partner-transfer scope, and a new false-success class:

`DYADIC_SEMANTIC_OVERFIT`

This supplement is not used to substitute for C1-C8. It is an additional evidence refinement that should be reviewed on its own merits.

## Rereview target

Four should rereview representation neutrality/minimality against the exact PR #4 head containing this matrix.

Thirteen should rereview false-success, provenance, semantic-claim ceilings, and scope against the same exact head.

One should reconcile those rereviews and independently inspect the changed passages before changing disposition.

Until then:

`PR4 = SOURCE_CORRECTIONS_APPLIED / REREVIEW_REQUIRED / NO_MERGE`
