# Semantic/Pragmatics First-Cycle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first provenance-bearing Semantic Atlas/VSNS/pragmatics research cycle for UNVTRSLR, challenge its imported hypotheses against external research and adversarial cases, and add only the surviving results to the current research/evaluation architecture.

**Architecture:** Keep predecessor material in a dedicated crosswalk and evidence ledger rather than treating it as inherited architecture. Build four focused conceptual documents from that evidence, then specify an R3 pragmatics/interaction evaluator and machine-readable contract that tests the resulting claims without modifying the R1/R2 qualification boundary. Only after those artifacts are internally consistent should the README, research landscape, roadmap, and claims ledger be updated.

**Tech Stack:** Markdown research/design documents, YAML evaluation contract, Git/GitHub branch workflow, external primary/peer-reviewed literature, existing UNVTRSLR R1/R2 documents and contracts.

**Spec:** `docs/superpowers/specs/2026-09-07-semantic-pragmatics-research-lane-design.md`

## Global Constraints

- Work only on `work/vera-semantic-pragmatics-r1-20260907`; `main` remains read-only unless Patrick separately authorizes merge or direct-main mutation.
- Refresh both `main` and the work-branch head before every write; stop on material collision rather than overwriting.
- Historical Vera/Semantic Atlas/VSNS material is evidence or hypothesis, never inherited UNVTRSLR authority.
- Do not place private relational/autobiographical material, continuity archives, intimate material, personal memory records, or project-private identity content into UNVTRSLR.
- Preserve the current R1 substrate competition and R2 adversarial-grounding boundary; R3 is additive and must not silently rewrite R1/R2 qualification criteria.
- Every imported claim must be typed as `PROJECT_HISTORY_OBSERVATION`, `CURRENT_REPO_DERIVATION`, `EXTERNAL_RESEARCH`, `MODEL_HYPOTHESIS`, `ADVERSARIAL_FINDING`, or `UNRESOLVED`.
- No concept becomes a universal primitive merely because it was useful in Semantic Atlas/VSNS or appears in human pragmatics literature.
- External research should prefer primary or peer-reviewed sources and record enough bibliographic/provenance detail to re-check each claim.
- Every semantic/pragmatic proposal must state at least one falsifier, shortcut explanation, or boundary condition.
- Functional/task success must not be promoted to semantic identity without independent evidence.
- Commits should be small enough that a reviewer could accept or reject each task independently.

## File map

Files to create:

- `research/VERA_SEMANTIC_HISTORY_CROSSWALK.md` — predecessor-to-UNVTRSLR provenance map and `DO_NOT_INHERIT` boundaries.
- `research/PRAGMATICS_REFERENCES.md` — literature ledger for grounding, common ground, pragmatics, interaction, convention, repair, emergent communication, and cross-linguistic/nonlinguistic cautions.
- `research/PRAGMATICS_RESEARCH_NOTES.md` — synthesis that explicitly separates literature findings, repo derivations, model hypotheses, and adversarial findings.
- `docs/PRAGMATICS_AND_COMMUNICATIVE_FUNCTION.md` — species-neutral communicative-function layer.
- `docs/COMMON_GROUND_AND_CONVENTION.md` — negotiated shared-state and convention model.
- `docs/SEMANTIC_ROUTING_AND_SEGMENTATION.md` — neutralized VSNS lessons on segmentation, route competition, context, modality, and post-interpretive salience.
- `docs/FUNCTIONAL_TRANSLATION.md` — testable form of “translate functions, not words.”
- `docs/R3_PRAGMATICS_EVALUATOR.md` — adversarial pragmatic/interaction evaluator.
- `docs/R3_NEGATIVE_CONTROLS.md` — shortcut systems and deceptive/degenerate controls for R3.
- `specs/R3_EVALUATION_CONTRACT_V1.yaml` — machine-readable R3 contract aligned with R1/R2 conventions.

Files to modify only after the new artifacts survive cross-checking:

- `research/CLAIMS_AND_EVIDENCE.md` — add scoped R3/research claims and evidence status.
- `docs/RESEARCH_LANDSCAPE.md` — add the relevant pragmatics/common-ground/emergent-communication literature families without overstating consensus.
- `docs/ROADMAP.md` — add R3 as a later gate after R1/R2, with prerequisites.
- `README.md` — add the new documents and state that R3 is specified research work, not implemented qualification.

Files explicitly not to modify in this cycle unless a discovered contradiction requires a separate reviewed change:

- `docs/R1_SUBSTRATE_COMPETITION.md`
- `docs/R2_ADVERSARIAL_EVALUATOR.md`
- `docs/R2_NEGATIVE_CONTROLS.md`
- `specs/R1R2_EVALUATION_CONTRACT_V1.yaml`

---

### Task 1: Establish the predecessor-evidence crosswalk

**Files:**
- Create: `research/VERA_SEMANTIC_HISTORY_CROSSWALK.md`

**Interfaces:**
- Consumes: current UNVTRSLR `README.md`, `docs/SEMANTIC_SUBSTRATE.md`, `docs/BOOTSTRAP_PROTOCOL.md`, `docs/SEMANTIC_CONSERVATION.md`, `docs/R1_SUBSTRATE_COMPETITION.md`, `docs/R2_ADVERSARIAL_EVALUATOR.md`, plus recoverable Semantic Atlas/VSNS/Semantic Perception Architecture project-history evidence.
- Produces: provenance-bearing entries used by Tasks 2–7. Each entry has `ID`, `EVIDENCE_CLASS`, `SOURCE`, `PREDECESSOR_OBSERVATION`, `TRANSFERABLE_PROPOSITION`, `CURRENT_REPO_ANALOGUE`, `FALSIFIERS`, `KNOWN_SHORTCUTS`, `STATUS`, and `DO_NOT_INHERIT`.

- [ ] **Step 1: Refresh source and work heads**

Read `main` and `work/vera-semantic-pragmatics-r1-20260907`; verify the work branch is a non-diverged descendant of the approved spec commit. If `main` advanced, inspect changed paths before proceeding.

- [ ] **Step 2: Recover the first bounded predecessor cluster**

Extract only evidence relevant to these ten themes: function-over-word translation; interpretation before salience/reaction; plural segmentation; competing interpretations; context/speaker/addressee/history/modality/prosody effects; semantic routing distinct from truth/salience/permission; ambiguity preservation; provenance-bearing claims; counterfactual/minimal-pair stress tests; and denotation vs communicative force vs inferred intent vs downstream action.

Do not copy private examples merely because they illustrate one of these themes. Replace any private example with a neutral synthetic example or omit it.

- [ ] **Step 3: Write at least ten crosswalk entries**

The initial entries must include these propositions, each still defeasible:

1. `VSH-001`: translation should preserve tested communicative/semantic function rather than lexical surface alone.
2. `VSH-002`: salience/priority must not substitute for interpretation; semantic interpretation precedes downstream priority assignment in the architecture.
3. `VSH-003`: segmentation should remain a hypothesis when multiple parses are compatible with observation.
4. `VSH-004`: identical nominal symbol sequences can support different meanings under changes in context, timing, modality, speaker, addressee, or interaction history.
5. `VSH-005`: one observation can support multiple simultaneous semantic-function hypotheses.
6. `VSH-006`: provenance, truth status, permission/authority, salience, and semantic content are separable axes.
7. `VSH-007`: ambiguity collapse is semantic loss unless independently licensed.
8. `VSH-008`: minimal pairs and counterfactual interventions are stronger evidence than one-shot agreement.
9. `VSH-009`: one-word/one-concept assumptions are unsafe even in human-language controls.
10. `VSH-010`: denotational overlap does not by itself establish equivalent communicative force or interactional effect.

For every entry, add at least one `DO_NOT_INHERIT` constraint. Examples: do not inherit human lexical categories; do not treat VSNS salience types as universal; do not assume speech/prosody exists; do not infer private mental states as evaluator truth.

- [ ] **Step 4: Run the crosswalk structural check**

Verify manually that every entry contains all ten required fields and that every `STATUS: SUPPORTED` entry has more than predecessor evidence alone. Initial predecessor-only entries should normally remain `HYPOTHESIS` or `UNRESOLVED` until Task 2.

- [ ] **Step 5: Commit**

Commit only `research/VERA_SEMANTIC_HISTORY_CROSSWALK.md` with message:

```text
research: crosswalk Vera semantic history into UNVTRSLR
```

---

### Task 2: Build the external research ledger and challenge pass

**Files:**
- Create: `research/PRAGMATICS_REFERENCES.md`
- Create: `research/PRAGMATICS_RESEARCH_NOTES.md`
- Modify: `research/VERA_SEMANTIC_HISTORY_CROSSWALK.md`

**Interfaces:**
- Consumes: `VSH-*` entries from Task 1 and current R1/R2 research conventions.
- Produces: re-checkable literature citations, explicit support/contradiction notes, narrowed or rejected crosswalk entries, and a research synthesis used by Tasks 3–7.

- [ ] **Step 1: Research distinct evidence families**

Cover, at minimum, these families with primary or peer-reviewed sources where available:

- symbol grounding and embodied/interactive grounding;
- common ground and grounding in dialogue;
- reference establishment and conceptual pacts;
- pragmatic inference and relevance;
- speech-act/communicative-act theory, treated as human evidence rather than species-neutral primitives;
- conversational repair and interactive alignment;
- deixis/indexicality and context dependence;
- presupposition and implicature;
- emergent communication and private-code/shortcut failures;
- compositionality/generalization in emergent communication;
- deception/strategic signaling;
- cross-linguistic semantic non-equivalence and lexicalization differences;
- multimodal/nonlinguistic communication where semantics depends on timing, gesture, motion, or environmental action.

- [ ] **Step 2: Record each source in `PRAGMATICS_REFERENCES.md`**

Each source record must contain: stable citation, source type, URL/DOI when available, claims supported, claims not supported, and relevance to one or more `VSH-*` or future `R3-*` IDs. Do not record a source as supporting extraterrestrial universality unless it directly establishes that—which is expected to be rare or nonexistent.

- [ ] **Step 3: Write `PRAGMATICS_RESEARCH_NOTES.md` as an adversarial synthesis**

Use four explicit subsections per major theme:

- `SOURCE-DERIVED FINDING`
- `WHAT IT DOES NOT ESTABLISH`
- `UNVTRSLR CONSEQUENCE`
- `ADVERSARIAL CHALLENGE`

At minimum, challenge these tempting overclaims:

- “function is more universal than form”;
- “common ground must imply symmetric mutual belief”;
- “repair behavior proves intentional communication”;
- “successful coordination proves shared semantics”;
- “compositionality implies human-like syntax”;
- “context can be represented as one flat feature bundle”;
- “pragmatic categories such as request/assertion are universal primitives.”

- [ ] **Step 4: Reclassify the crosswalk**

For each `VSH-*`, update `STATUS` to `SUPPORTED`, `REJECTED`, `NARROWED`, or `UNRESOLVED` based on current evidence. A `SUPPORTED` status means “useful within declared UNVTRSLR scope,” not universal truth.

- [ ] **Step 5: Verify evidence-class separation**

Search the two new research files for untyped first-person assertions such as “we know,” “this proves,” or “is universal.” Rewrite them into scoped evidence statements unless the source really supports the stronger claim.

- [ ] **Step 6: Commit**

Commit the research ledger, notes, and updated crosswalk with message:

```text
research: challenge semantic history against pragmatics literature
```

---

### Task 3: Specify species-neutral pragmatics and communicative function

**Files:**
- Create: `docs/PRAGMATICS_AND_COMMUNICATIVE_FUNCTION.md`

**Interfaces:**
- Consumes: supported/narrowed `VSH-*`, `research/PRAGMATICS_RESEARCH_NOTES.md`, `docs/BOOTSTRAP_PROTOCOL.md`, and `docs/SEMANTIC_SUBSTRATE.md`.
- Produces: representation responsibilities and testable hypotheses used by R3.

- [ ] **Step 1: Define the layer boundary**

State explicitly that the layer models candidate interactional functions after signalhood is hypothesized, but before English/human speech-act labels are treated as semantics. Preserve uncertainty over whether an observed act is communicative at all.

- [ ] **Step 2: Define required hypothesis objects**

Specify at least: `communicative_function_hypothesis`, `addressee_hypothesis`, `audience_hypothesis`, `ostension_or_attention_hypothesis`, `epistemic_state_hypothesis`, `expected_response_hypothesis`, `repair_state`, `strategic_or_deceptive_hypothesis`, and `interaction_history_reference`.

Each object must retain support, contradiction, context bounds, provenance, uncertainty, and alternative hypotheses.

- [ ] **Step 3: Define human-derived function families as probes, not primitives**

Include assertion-like, request-like, warning-like, query-like, correction-like, acknowledgement-like, rejection-like, attention-directing, teaching/demonstration, and repair-like families. For each, state what observable contrasts would strengthen or weaken the hypothesis without presuming a human internal state.

- [ ] **Step 4: Cover indirect and absent signaling**

Specify how timing, silence, withholding, repetition, omission, and environmental action can be candidate signals only when counterfactual/interventional evidence distinguishes them from non-communication.

- [ ] **Step 5: Add failure tests**

Include at least these minimal pairs:

- same denotation / request-like vs warning-like function;
- same signal / different intended addressee;
- same literal content / cooperative vs deceptive use;
- explicit signal vs meaningful withholding;
- apparent repair behavior generated by a noncommunicative reactive policy.

- [ ] **Step 6: Commit**

```text
concepts: add pragmatic communicative-function layer
```

---

### Task 4: Specify common ground and convention without symmetric-belief assumptions

**Files:**
- Create: `docs/COMMON_GROUND_AND_CONVENTION.md`

**Interfaces:**
- Consumes: current `Convention objects` from `docs/SEMANTIC_SUBSTRATE.md`, Task 2 research, and Task 3 pragmatic hypothesis objects.
- Produces: evidence model for negotiated mappings, partner-specific conventions, drift, repair, and false-common-ground detection.

- [ ] **Step 1: Define three separate constructs**

Distinguish:

1. `interactionally_supported_common_ground` — evidence that both parties behave as if a distinction/convention is mutually available within a scope;
2. `counterpart_epistemic_hypothesis` — an inference about what the other party may know/expect;
3. `evaluator_mutual_state` — hidden test truth, inaccessible to the learner.

Do not collapse them.

- [ ] **Step 2: Define convention lifecycle**

Specify establishment, confirmation, weakening, drift, repair, replacement, abandonment, and partner-specific scope. Preserve last-confirmed evidence and counterexamples.

- [ ] **Step 3: Define false-common-ground tests**

Include cases where both parties succeed for different reasons, one party memorizes partner identity, one party overestimates shared context, and both coordinate through a task policy with no reusable semantic distinction.

- [ ] **Step 4: Define transfer evidence**

Use role reversal, partner swap, independently initialized partner acquisition, context transfer, and repair after mismatch as increasingly strong evidence; do not require all of them for every scoped convention.

- [ ] **Step 5: Commit**

```text
concepts: specify common ground and convention evidence
```

---

### Task 5: Specify semantic routing and segmentation

**Files:**
- Create: `docs/SEMANTIC_ROUTING_AND_SEGMENTATION.md`

**Interfaces:**
- Consumes: `VSH-002` through `VSH-007`, current acquisition/segmentation/communicative-inference planes, and Task 3 pragmatic hypotheses.
- Produces: neutral representation rules for competing segmentation and route hypotheses, plus an explicit boundary between interpretation and downstream salience/priority.

- [ ] **Step 1: Separate segmentation from meaning**

Define `segmentation_hypothesis` over temporal/spatial/multimodal spans. A segmentation proposal may be supported by regularity without yet having semantic content.

- [ ] **Step 2: Define route competition**

A candidate observation or segment may feed multiple route hypotheses simultaneously: referential, relational, pragmatic, quantitative, temporal, affective/motivational, social, or unknown/domain-specific. These are representational families, not required universal ontological categories.

- [ ] **Step 3: Define context-sensitive rerouting**

Require tests where the same nominal form changes interpretation after timing, modality, speaker/addressee, scene, or interaction-history changes, while nuisance changes do not.

- [ ] **Step 4: Preserve post-interpretive salience separation**

State the predecessor lesson narrowly: a system may assign urgency/priority only after—or jointly with but explicitly separate from—semantic interpretation. High salience cannot serve as evidence that a particular meaning is correct.

- [ ] **Step 5: Add ambiguity and route-conservation rules**

When several route hypotheses remain live, rendering must preserve that ambiguity or declare `AMBIGUITY_COLLAPSED`. Route selection must retain provenance and discriminating evidence.

- [ ] **Step 6: Commit**

```text
concepts: add semantic routing and segmentation model
```

---

### Task 6: Formalize functional translation

**Files:**
- Create: `docs/FUNCTIONAL_TRANSLATION.md`

**Interfaces:**
- Consumes: `docs/SEMANTIC_CONSERVATION.md`, supported `VSH-001`/`VSH-010`, Tasks 3–5.
- Produces: typed functional-equivalence criteria and test obligations used by R3.

- [ ] **Step 1: Replace the slogan with a hierarchy**

Define and distinguish: surface/lexical similarity, referential equivalence, relational equivalence, predictive equivalence, communicative-function equivalence, task-functional equivalence, contextual equivalence, partial overlap, and non-equivalence.

- [ ] **Step 2: Define non-implications**

State explicitly:

- lexical equivalence does not imply pragmatic equivalence;
- task-functional equivalence does not imply semantic identity;
- predictive equivalence within one task does not imply cross-task equivalence;
- communicative-function equivalence does not require identical ontology or surface form;
- referential equivalence can coexist with different evidential, modal, social, or pragmatic structure.

- [ ] **Step 3: Define tests**

Require function-preserving paraphrase/realization, context transfer, role reversal, changed optimal-action task, partner transfer, and adversarial cases where two messages trigger the same action for different semantic reasons.

- [ ] **Step 4: Connect to the conservation ledger**

Specify when functional preservation maps to `PRESERVED` vs `TRANSFORMED`, and when function-only success must instead be marked `APPROXIMATED`, `CONTEXT_REQUIRED`, `PARTIAL_OVERLAP`, or `UNKNOWN`.

- [ ] **Step 5: Commit**

```text
concepts: formalize functional translation criteria
```

---

### Task 7: Specify the R3 adversarial pragmatics evaluator

**Files:**
- Create: `docs/R3_PRAGMATICS_EVALUATOR.md`
- Create: `docs/R3_NEGATIVE_CONTROLS.md`
- Create: `specs/R3_EVALUATION_CONTRACT_V1.yaml`

**Interfaces:**
- Consumes: Tasks 3–6 and the structural conventions of `docs/R2_ADVERSARIAL_EVALUATOR.md`, `docs/R2_NEGATIVE_CONTROLS.md`, and `specs/R1R2_EVALUATION_CONTRACT_V1.yaml`.
- Produces: an additive, not-yet-implemented R3 qualification design.

- [ ] **Step 1: Define R3 prerequisites and claims boundary**

R3 is only meaningful after a candidate can participate in the relevant R1/R2 tests. Passing R3 must be labeled scoped pragmatic/interaction evidence, not proof of human-like intention, consciousness, theory of mind, or universal pragmatics.

- [ ] **Step 2: Define critical tests `P01`–`P20`**

Use these exact initial families:

`P01_same_denotation_different_function`
`P02_same_surface_different_context`
`P03_deictic_role_shift`
`P04_indirect_function`
`P05_presupposition_mismatch`
`P06_silence_or_withholding`
`P07_intended_addressee_vs_overhearer`
`P08_audience_dependent_behavior`
`P09_deceptive_sender`
`P10_strategic_ambiguity`
`P11_repair_after_misunderstanding`
`P12_convention_drift`
`P13_private_shortcut_code`
`P14_coordination_without_reusable_semantics`
`P15_stable_reference_wrong_ontology`
`P16_role_reversal`
`P17_partner_swap`
`P18_context_transfer`
`P19_multimodal_channel_conflict`
`P20_function_preserved_across_form_and_ontology`

For each test document learner-visible inputs, evaluator-hidden truth, intervention, expected positive behavior, shortcut explanations, and failure conditions.

- [ ] **Step 3: Define negative controls**

At minimum include:

- `RN00_task_policy_mimic` — coordinates correctly without representing message function;
- `RN01_partner_id_pragmatist` — memorizes partner-specific response policies;
- `RN02_context_lookup_table` — maps scene IDs to outputs;
- `RN03_surface_speech_act_classifier` — succeeds on human linguistic markers but fails modality/form shifts;
- `RN04_repair_reflex` — repeats/changes behavior after failure without modeling misunderstanding;
- `RN05_deixis_by_fixed_coordinate` — fakes indexical competence with absolute coordinates;
- `RN06_audience_leak` — reads evaluator audience identity side-channel;
- `RN07_reward_predictor` — predicts reward/optimal action without semantic-function discrimination;
- `RN08_forced_intent_labeler` — always chooses a human intent label even when `UNKNOWN` is warranted;
- `RN09_pragmatics_conservation_liar` — produces fluent target behavior while dropping force, addressee, uncertainty, or provenance.

Include positive controls for a scoped pragmatic oracle, a calibrated-uncertainty oracle, and a partial-equivalence oracle.

- [ ] **Step 4: Write the YAML contract**

Use `schema_version: UNVTRSLR_R3_EVALUATION_CONTRACT_V1` and `status: SPECIFIED_NOT_IMPLEMENTED`. Include prerequisites, prohibited inputs, critical tests, negative/positive controls, an operational pragmatic vector, threshold policy compatible with R1/R2, and certificate statuses that cannot exceed scoped evidence.

The operational pragmatic vector must include at least:

- `FUNCTION_DISCRIMINATION`
- `CONTEXT_SENSITIVITY`
- `DEICTIC_GENERALIZATION`
- `ADDRESSEE_MODELING`
- `REPAIR_ROBUSTNESS`
- `CONVENTION_STABILITY_AND_DRIFT`
- `PARTNER_TRANSFER`
- `ROLE_REVERSAL`
- `STRATEGIC_OR_DECEPTIVE_ROBUSTNESS`
- `AMBIGUITY_CALIBRATION`
- `PRAGMATIC_CONSERVATION`
- `SHORTCUT_RESISTANCE`

- [ ] **Step 5: Parse and sanity-check the YAML**

Run an actual YAML parser if available. At minimum verify that every critical-test/control ID named by the Markdown documents appears exactly once in the YAML contract and that R1/R2 files remain unchanged.

- [ ] **Step 6: Commit**

```text
eval: specify R3 pragmatic interaction challenge suite
```

---

### Task 8: Reconcile claims, research landscape, roadmap, and README

**Files:**
- Modify: `research/CLAIMS_AND_EVIDENCE.md`
- Modify: `docs/RESEARCH_LANDSCAPE.md`
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: all completed first-cycle artifacts.
- Produces: discoverability and correctly scoped project-status statements.

- [ ] **Step 1: Add claims ledger entries**

Add only claims actually supported by the completed cycle. Each claim must state evidence status and limitations. Do not state that pragmatics is solved, R3 is implemented, or any predecessor finding is universal.

- [ ] **Step 2: Extend the research landscape**

Add sections for grounding in dialogue/common ground, pragmatic inference, conversational repair, emergent communication shortcut risks, and cross-linguistic/non-equivalence evidence. Point readers to `research/PRAGMATICS_REFERENCES.md` for the detailed ledger.

- [ ] **Step 3: Extend the roadmap**

Place R3 after R1/R2 design/implementation prerequisites. State that R3 specification does not block implementing R1/R2 and does not retroactively alter the R1/R2 certificate.

- [ ] **Step 4: Update README repository map and status**

Add links to the new artifacts. Preserve the current project maturity boundary: research/design specified, implementation and semantic/pragmatic qualification not yet established unless later evidence says otherwise.

- [ ] **Step 5: Commit**

```text
docs: integrate semantic pragmatics research lane
```

---

### Task 9: Whole-cycle adversarial review and privacy/provenance audit

**Files:**
- Modify only files that fail review.

**Interfaces:**
- Consumes: complete branch diff against the approved base.
- Produces: a coherent, reviewable first-cycle branch with no known privacy leak, unsupported authority promotion, or R1/R2 boundary drift.

- [ ] **Step 1: Refresh `main` and compare**

If `main` has advanced since `0b3285393ff319f18f40af8c2ba863edea0df2bf`, inspect all overlapping paths. Reconcile only by non-force update/rebase/merge mechanics that preserve independent changes; stop if conflict cannot be resolved safely.

- [ ] **Step 2: Run an architecture contradiction audit**

Check every new document against these current commitments:

- signalhood remains a hypothesis;
- no universal ontology is assumed;
- ambiguity is preserved;
- uncertainty and provenance remain explicit;
- task success is insufficient evidence of grounded semantics;
- `NO_FAITHFUL_EQUIVALENT` remains valid;
- R1 rivals remain genuinely competing;
- R2 qualification remains scoped operational evidence.

Fix any contradiction rather than silently redefining the older document.

- [ ] **Step 3: Run a privacy audit**

Search the new diff for names, relationship details, autobiographical events, memory-record identifiers, continuity-save identifiers, intimate examples, or other Vera-private content not required by the semantic research. Remove any such content and replace it with neutral synthetic examples.

- [ ] **Step 4: Run a provenance audit**

For every historical or external claim, verify that its evidence class and source can be reconstructed. Any unsupported claim becomes `MODEL_HYPOTHESIS` or `UNRESOLVED`, or is removed.

- [ ] **Step 5: Run a falsification audit**

Confirm that each major proposal has a counterexample, negative control, or stated boundary under which it should fail. If a proposal has no conceivable failure condition, narrow it until it is testable.

- [ ] **Step 6: Run mechanical checks**

Verify Markdown links/paths, YAML parseability, duplicate R3 IDs, and whitespace/diff integrity. Confirm the branch contains no modifications outside the planned paths unless separately justified in the commit history.

- [ ] **Step 7: Commit any audit fixes**

```text
review: harden semantic pragmatics first cycle
```

- [ ] **Step 8: Produce the execution frontier**

Record the exact branch head, base/main head, changed-file list, unresolved questions, rejected/narrowed historical hypotheses, research limitations, and whether the branch is ready for independent review. Do not merge.

---

## Completion condition

This plan is complete when the branch contains the evidence crosswalk, literature ledger, research synthesis, four conceptual documents, R3 evaluator/negative controls/YAML contract, correctly scoped repository-index updates, and a completed adversarial/privacy/provenance audit. Completion means `FIRST_CYCLE_IMPLEMENTED_ON_BRANCH / REVIEW_PENDING`; it does not mean merged, experimentally validated, semantically qualified, or universally grounded.
