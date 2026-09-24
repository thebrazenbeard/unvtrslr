# Human Verbal-Language Research Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate human spoken/verbal-language evidence into UNVTRSLR without promoting human-specific linguistic machinery into universal semantic-bootstrap canon.

**Architecture:** Add one evidence-focused research file, then revise the bootstrap protocol, first-100 challenge framing, control suite, references, and claims ledger only where the evidence changes a project obligation or claim ceiling. Keep external evidence, project hypotheses, and adversarial inferences explicitly separable.

**Tech Stack:** Markdown research corpus; Git/GitHub provenance; peer-reviewed primary/review literature; Chat Communication Bus coordination.

**Spec:** `docs/superpowers/specs/2026-09-07-semantic-bootstrap-research-design.md`

## Global Constraints

- Bound starting source: `thebrazenbeard/unvtrslr main@0b3285393ff319f18f40af8c2ba863edea0df2bf`.
- Working branch: `research/semantic-bootstrap-human-to-nonhuman-20260907`.
- This pass is human verbal/spoken language only; signed/nonverbal and nonhuman evidence remain later distinct passes.
- Signed languages must not be treated as merely nonverbal behavior.
- Human evidence is not species-independent universality evidence.
- `FIRST_100_CHALLENGES.md` remains 100 evaluator-described challenges, not 100 universal words.
- No implementation, deployment, METI/transmission, autonomous-contact action, or merge is in scope.
- Non-PR coordination among One, Four, Nine, and Thirteen stays on Chat Communication Bus under `UNVTRSLR-BT2-20260907`.

---

### Task 1: Lock the human verbal-language evidence review

**Files:**
- Create: `research/HUMAN_VERBAL_LANGUAGE.md`
- Modify: `research/REFERENCES.md`

**Interfaces:**
- Consumes: current thesis, bootstrap phases, R1/R2 contracts, existing bibliography.
- Produces: evidence classes and architecture implications used by Tasks 2-5.

- [ ] **Step 1:** Verify primary/review sources for cross-situational learning, joint attention limits, turn-taking, repair, experimental semiotics, vocal iconicity, cultural transmission, semantic typology, evidentiality, and cross-linguistic diversity.
- [ ] **Step 2:** Write `research/HUMAN_VERBAL_LANGUAGE.md` with separate sections for observed result, claim ceiling, UNVTRSLR implication, and non-generalization warning.
- [ ] **Step 3:** Add exact source records/DOIs to `research/REFERENCES.md`, avoiding duplicate records already present.
- [ ] **Step 4:** Re-read every empirical sentence against its cited source and downgrade any claim whose source supports only a narrower condition.

**Acceptance:** No project architecture claim is presented as established human evidence; no human finding is silently generalized to arbitrary agents.

### Task 2: Revise the bootstrap protocol from the evidence

**Files:**
- Modify: `docs/BOOTSTRAP_PROTOCOL.md`

**Interfaces:**
- Consumes: Task 1 evidence review.
- Produces: evidence-constrained bootstrap ordering used by later human/nonhuman passes.

- [ ] **Step 1:** Add the `self-demonstrating -> convention-forming -> recursively self-describing` distinction as a project hypothesis, not a law.
- [ ] **Step 2:** Add an identifiability/common-ground precondition before semantic promotion.
- [ ] **Step 3:** Recast joint attention/ostension as useful human routes, not mandatory primitives.
- [ ] **Step 4:** Strengthen repair/clarification as an early functional target while forbidding preinstalled semantic labels for repair acts.
- [ ] **Step 5:** Distinguish discovered pre-existing correspondences from negotiated conventions and adapted/mixed conventions.

**Acceptance:** The protocol can explicitly conclude `UNDERDETERMINED_IN_SCOPE` before attempting a semantic mapping.

### Task 3: Turn the first 100 into a dependency-aware challenge system

**Files:**
- Modify: `docs/FIRST_100_CHALLENGES.md`

**Interfaces:**
- Consumes: human acquisition/interaction evidence and R0.5 identifiability constraint.
- Produces: dependency metadata framing without changing the 100 evaluator challenge identities.

- [ ] **Step 1:** Add a dependency-map section separating physical/interaction prerequisites from evaluator semantic labels.
- [ ] **Step 2:** Define alternative paths so attention, reference, repair, quantity, action, and composition are not forced into one human developmental order.
- [ ] **Step 3:** Add hidden-assumption annotations for object segmentation, agency, shared time, perspective, and observability.
- [ ] **Step 4:** Add explicit false-success patterns such as shared task structure, hidden attention cues, co-trained private code, and evaluator-defined category recovery.

**Acceptance:** The 100 remain challenge families; the document does not claim that their labels or order are universal concepts.

### Task 4: Strengthen human-language controls

**Files:**
- Modify: `docs/CONTROL_SUITE.md`

**Interfaces:**
- Consumes: Task 1 evidence and Task 2 protocol changes.
- Produces: human-language positive/negative controls that pressure R1/R2 without leaking semantic truth.

- [ ] **Step 1:** Add spoken-language controls spanning typological/semantic variation rather than mostly related high-resource languages.
- [ ] **Step 2:** Add convention-invention controls separate from pre-existing-language recovery controls.
- [ ] **Step 3:** Add iconicity/no-iconicity paired controls.
- [ ] **Step 4:** Add repair-present/repair-disabled or repair-corrupted conditions.
- [ ] **Step 5:** Add human-pragmatics leakage controls for gaze, task instructions, shared coordinate conventions, experimenter cues, pretrained world knowledge, and evaluator segmentation.

**Acceptance:** A system cannot receive credit for language recovery merely by exploiting a human experiment's shared task scaffolding.

### Task 5: Update the claims ledger and challenge R1/R2

**Files:**
- Modify: `research/CLAIMS_AND_EVIDENCE.md`

**Interfaces:**
- Consumes: Tasks 1-4.
- Produces: explicit claim ceilings and new open questions for later passes.

- [ ] **Step 1:** Add claims for cross-situational ambiguity reduction, joint-attention non-necessity, interaction repair robustness, convention invention, iconicity, cultural transmission, semantic-category diversity, and evidentiality.
- [ ] **Step 2:** Add an identifiability/underdetermination project boundary.
- [ ] **Step 3:** Mark `jointly testable contingency`, R0.5, predictive-state minimality, and the staged self-description sequence as `PROJECT_HYPOTHESIS` unless independently supported.
- [ ] **Step 4:** Add discovery-vs-invention provenance as a design requirement.

**Acceptance:** The ledger makes clear what human evidence supports, what it merely motivates, and what remains an UNVTRSLR-specific hypothesis.

### Task 6: Verify and checkpoint the pass

**Files:**
- Review all files changed in Tasks 1-5.
- Chat Bus: append one Nine checkpoint/review request on `bus/nine-v2`.

**Interfaces:**
- Consumes: completed pass.
- Produces: independently inspectable human-verbal checkpoint for Four/Thirteen/One cross-critique.

- [ ] **Step 1:** Compare the branch against its pre-pass head and confirm only intended research/docs paths changed.
- [ ] **Step 2:** Search changed files for overclaims including `universal`, `proves`, `necessary`, `sufficient`, and `self-describing`; inspect each occurrence contextually.
- [ ] **Step 3:** Confirm source records/DOIs and evidence labels are internally consistent.
- [ ] **Step 4:** Post the exact branch head and changed-file set to Chat Bus for One/Four/Thirteen cross-critique.
- [ ] **Step 5:** Do not begin the human nonverbal/signed pass until this human-verbal repository checkpoint exists.

**Acceptance:** The branch has one auditable human-verbal research checkpoint, with external evidence separated from project inference and a Chat Bus cross-review request bound to the exact commit.
