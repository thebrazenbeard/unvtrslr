# Pragmatics and Interaction Research Notes — First Adversarial Synthesis

Status: FIRST-CYCLE SYNTHESIS / NOT ARCHITECTURE CANON
Evidence ledger: `research/PRAGMATICS_REFERENCES.md`
Historical crosswalk: `research/VERA_SEMANTIC_HISTORY_CROSSWALK.md`

## Executive result

The first external challenge pass does **not** justify importing a human pragmatics ontology into UNVTRSLR. It does justify strengthening the evaluator around context, addressee, repair, convention, pragmatic inference, deception, multimodality, and causal use of messages.

The largest correction is to the predecessor slogan:

> `translate functions, not words`

That slogan is useful as a rejection of dictionary substitution, but too strong as architecture. Form can itself carry meaning through iconicity, timing, order, prosody, gesture, and conventional contrast. The stronger UNVTRSLR rule is:

> **Preserve the tested semantic and communicative invariants that matter within scope. Lexical/surface identity is neither necessary nor sufficient. Functional similarity is also neither necessary nor sufficient by itself. Form must be conserved when form is one of the demonstrated invariants.**

That is a real narrowing of predecessor doctrine, not ratification.

## Theme 1 — Grounding is more than symbol-to-symbol mapping

### SOURCE-DERIVED FINDING

Harnad’s symbol-grounding formulation is a strong warning against treating formal symbol relations as self-grounding. Clark and Brennan use “grounding” differently: human interlocutors collaboratively seek evidence that a contribution has been understood well enough for the current purpose. These are distinct uses of the word *grounding*—one about semantic attachment to non-symbolic structure, the other about interactional evidence of understanding.

### WHAT IT DOES NOT ESTABLISH

Neither literature establishes that UNVTRSLR can prove a uniquely correct ontology. Harnad does not solve pragmatic convention; Clark and Brennan do not show that mutual belief can be directly observed or that all communication requires human-style collaborative grounding.

### UNVTRSLR CONSEQUENCE

Keep at least three separate notions:

1. `world_grounding` — evidence linking a semantic distinction to observations, interventions, relations, or predictions;
2. `interaction_grounding` — evidence that participants can use/repair a convention sufficiently for a declared purpose;
3. `evaluator_ground_truth` — withheld test facts that neither participant is allowed to treat as its own epistemic state.

Never let success on (2) substitute automatically for (1).

### ADVERSARIAL CHALLENGE

Construct a pair that coordinates flawlessly through a partner-specific lookup code but cannot identify the same distinction after a world-factor intervention. It has interactional coordination without demonstrated reusable world grounding.

**Crosswalk effect:** supports and sharpens `VSH-008`, `VSH-012`; leaves any claim of unique semantic grounding explicitly out of scope.

---

## Theme 2 — Function matters, but form sometimes is the function-bearing evidence

### SOURCE-DERIVED FINDING

The predecessor “translate functions, not words” principle correctly attacks lexical substitution. Grice and relevance-theory traditions likewise show that human communicated content can exceed sentence-level conventional content. However, iconicity research shows that linguistic form is not uniformly arbitrary: form can systematically/iconically contribute to processing and meaning. Gesture and deixis add stronger multimodal cases where orientation, timing, location, and movement are part of what is communicated.

### WHAT IT DOES NOT ESTABLISH

There is no evidence that “function” is a species-neutral master representation. Nor is there evidence that form is always semantically dispensable after its function is inferred. A translation that discards form may destroy distinctions carried by rhythm, iconicity, timing, spatial layout, or modality.

### UNVTRSLR CONSEQUENCE

Replace function-first translation with **typed invariant conservation**. Ask separately whether the tested invariant is referential, relational, predictive, pragmatic, formal/iconic, temporal, social, epistemic, evidential, or task-functional. A target may preserve one while losing another.

`FUNCTIONALLY_EQUIVALENT` should therefore remain a typed, scoped equivalence class—not a synonym for `same meaning`.

### ADVERSARIAL CHALLENGE

Give two source signals that induce the same receiver action but differ in an iconic spatial relation that predicts a novel-world property. A task-only translator will call them equivalent; a semantic-conservation system should not.

**Crosswalk effect:** `VSH-001` survives only in narrowed form. Status recommendation: `SUPPORTED`, with explicit narrowing.

---

## Theme 3 — Common ground should not be modeled as magical symmetric mind-reading

### SOURCE-DERIVED FINDING

Clark/Brennan and Brennan/Clark provide strong human evidence that communication is history-sensitive and that partners establish working shared conceptualizations. Stalnaker’s tradition analyzes presupposition using common ground. But formal work on convention explicitly debates whether infinite-order common knowledge is necessary for ordinary conventions.

### WHAT IT DOES NOT ESTABLISH

Behavioral success does not let an evaluator conclude that both agents literally possess symmetric nested beliefs. Human common-ground theories are explanatory models, not direct access to participant minds, and the common-knowledge requirement is contested even inside game-theoretic convention theory.

### UNVTRSLR CONSEQUENCE

Represent three different things:

- `interactionally_supported_common_ground`: what repeated behavior/repair licenses the system to treat as jointly usable within scope;
- `counterpart_epistemic_hypothesis`: uncertain inference about what another agent knows/expects;
- `evaluator_mutual_state`: hidden truth used only for scoring when a synthetic experiment provides it.

This permits asymmetric, partial, mistaken, or partner-specific common ground without logical contradiction.

### ADVERSARIAL CHALLENGE

Agent A believes convention X is established; Agent B succeeds only by reading a side channel. Both coordinate. Then remove the side channel. If A’s model says “shared semantic convention” merely from prior success, it has inferred false common ground.

**Crosswalk effect:** supports `VSH-004`, `VSH-010`; motivates a new explicit common-ground document.

---

## Theme 4 — Repair is evidence of interaction structure, not proof of intention or understanding

### SOURCE-DERIVED FINDING

Conversation analysis shows organized repair practices in human dialogue. Dingemanse et al. find striking cross-linguistic similarities in other-initiated repair across a broad 12-language sample, making repair one of the better candidates for a human pragmatic regularity.

### WHAT IT DOES NOT ESTABLISH

The studies do not establish repair as an extraterrestrial universal. More importantly for UNVTRSLR, a policy can imitate repair behavior without representing misunderstanding: repeat after failure, alter output after low reward, or copy a learned repair token.

### UNVTRSLR CONSEQUENCE

Treat repair as a **candidate communicative function** whose evidence comes from discriminatory behavior: Does the response target the actual locus of misunderstanding? Does repair improve interpretation under novel error types? Can roles reverse? Can a false repair cue be rejected?

### ADVERSARIAL CHALLENGE

Create `repair_reflex`: whenever reward drops, emit the previous signal more slowly/loudly or choose a canned alternative. It can look cooperative while lacking a model of what failed. R3 must reject this as evidence of grounded repair.

**Crosswalk effect:** reinforces `VSH-008` and adds a strong R3 negative control.

---

## Theme 5 — Successful coordination does not prove shared semantics

### SOURCE-DERIVED FINDING

Kottur et al. show multi-agent languages with near-perfect task reward that are not human-interpretable or compositional. Lowe et al. show even stronger metric failure: messages can correlate with subsequent action while having no causal effect on the partner/environment. Chaabouni et al. show that compositionality and generalization need not correlate in a simple way, although compositionality can aid transmission to new learners.

### WHAT IT DOES NOT ESTABLISH

Human interpretability is not the criterion for alien semantics. Noncompositionality is not automatically failure. Likewise, causal influence is necessary for some communication claims but is not by itself enough to establish a stable semantic distinction.

### UNVTRSLR CONSEQUENCE

Retain the current R2 insistence on communication ablation and direct message intervention. Add R3 tests that distinguish:

- causal influence;
- task coordination;
- stable referential/relational invariants;
- cross-task reuse;
- partner transfer;
- pragmatic-function discrimination.

A system can pass one and fail another.

### ADVERSARIAL CHALLENGE

Build a sender whose message is a perfect index into the receiver’s action table for one task. Change the optimal action while preserving the world distinction. If the mapping collapses, it learned action coordination, not reusable semantics.

**Crosswalk effect:** strongly supports `VSH-001` (narrowed), `VSH-008`, `VSH-012`.

---

## Theme 6 — Compositionality must earn its exact role

### SOURCE-DERIVED FINDING

Emergent-communication research does not support a simplistic “compositionality ⇒ generalization” rule. Chaabouni et al. found no correlation between measured compositionality and generalization in their setup, though compositionality improved transmission to new learners. Kharitonov/Baroni similarly warn that desired properties can be loosely related to compositionality depending on task.

### WHAT IT DOES NOT ESTABLISH

This does not refute compositionality as important in natural language, nor does it imply that arbitrary holistic codes can scale to UNVTRSLR’s target. It only blocks using compositionality as a magic proxy for grounding, generalization, or human-like syntax.

### UNVTRSLR CONSEQUENCE

R2/R3 should score **novel recombination**, **systematic transfer**, and **partner acquisition** directly. Structural compositionality is one possible mechanism and a useful diagnostic, but not the certificate itself.

### ADVERSARIAL CHALLENGE

Compare a holistic code and a compositionally structured code on held-out combinations, new partners, changed tasks, and ontology mismatch. If the holistic code genuinely matches the required transfer behavior, do not fail it merely for not resembling human syntax.

**Crosswalk effect:** supports the anti-universal boundary in `VSH-009` and simplicity discipline in `VSH-012`.

---

## Theme 7 — Context is structured and intervention-sensitive, not a flat bag of features

### SOURCE-DERIVED FINDING

Deixis demonstrates that interpretation can be anchored to speaker, addressee, time, place, attention, and social/perceptual access. Conceptual-pact work demonstrates partner-history effects. Presupposition theory demonstrates dependence on background assumptions. Gesture research demonstrates cross-modal integration and culturally variable conventionalization.

### WHAT IT DOES NOT ESTABLISH

It does not follow that every available contextual variable belongs in semantic state. A flat “context vector” can confound causal context with nuisance information, leak evaluator state, or memorize episode identities.

### UNVTRSLR CONSEQUENCE

Context references should be **typed and testable**: participant-role, spatial/deictic, temporal, interaction-history, modality/channel, environmental, epistemic-hypothesis, convention-state, and unknown/domain-specific. Each claimed context dependency must survive interventions that vary the candidate factor while holding plausible confounds fixed.

### ADVERSARIAL CHALLENGE

Give every episode a unique background texture correlated with speaker role. A learner can appear context-sensitive by memorizing texture. Then swap textures independently of speaker role. The correct semantic route should follow the role evidence, not the nuisance cue.

**Crosswalk effect:** strongly supports `VSH-003`, `VSH-004`, `VSH-005`.

---

## Theme 8 — Human pragmatic categories are experimental families, not universal primitives

### SOURCE-DERIVED FINDING

Human pragmatics provides productive distinctions—saying/implicating, assertion-like versus request-like behavior, deixis, presupposition, repair, addressee modeling, audience effects. Cross-linguistic work also shows that structural universals are much rarer than many theories assumed, while some interactional repair patterns appear much more stable across sampled languages.

### WHAT IT DOES NOT ESTABLISH

No reviewed source justifies hard-coding English speech-act categories, pronoun systems, tense, sentence mood, or Gricean maxims into an alien semantic ontology. Even a widespread human interactional pattern is evidence about humans, not arbitrary intelligence.

### UNVTRSLR CONSEQUENCE

Use labels such as `request_like`, `assertion_like`, `warning_like`, `query_like`, `repair_like`, or `attention_directing_like` only as **evaluator families in human/synthetic controls**. The substrate should store a more neutral candidate function: conditions of production, target/addressee, predicted receiver response, world-state dependence, expected consequences, evidence, alternatives, and uncertainty.

### ADVERSARIAL CHALLENGE

Construct a signaling system whose “warning-like” signal changes receiver behavior but has no proposition-like asserted content, and another system whose declarative-looking form is strategically used as a request. An English speech-act classifier should fail; a functional hypothesis system should retain the observed structure without forcing a human label.

**Crosswalk effect:** supports `VSH-010` only in a species-neutralized form.

---

## Theme 9 — Silence, withholding, and absence can be signals, but only counterfactually

### SOURCE-DERIVED FINDING

Animal signaling literature documents information withholding/deception in competitive interaction. Human pragmatics also routinely recognizes meaning carried by omission, delayed response, and expected-but-absent contributions.

### WHAT IT DOES NOT ESTABLISH

Absence is not intrinsically communicative. A non-event can result from sensor failure, latency, inattention, physical inability, noise, or no action at all. Calling every omission a signal would create an unlimited hallucination surface.

### UNVTRSLR CONSEQUENCE

A `withholding_or_absence_signal_hypothesis` requires evidence of an expectation relation: the event would predictably have occurred under a matched condition; its absence covaries with audience/context/state; recipients alter behavior contingent on the absence; and alternative physical explanations are tested.

### ADVERSARIAL CHALLENGE

Drop packets randomly at the same rate as a strategic withholding policy. A learner must not infer meaning from missing packets unless the missingness tracks a causal/interactional variable beyond channel noise.

**Crosswalk effect:** extends `VSH-003` and `VSH-010` into a concrete R3 test family.

---

## Theme 10 — A universal translator needs an anti-universalism discipline

### SOURCE-DERIVED FINDING

Evans and Levinson document substantial structural diversity across human languages. Gesture and deixis work add cultural and modality variation. Conversely, Dingemanse et al. provide evidence that some interactional repair organization may be relatively stable across a diverse human sample.

### WHAT IT DOES NOT ESTABLISH

Neither “humans are radically diverse” nor “some human pragmatic systems look recurrent” tells us what extraterrestrial cognition must share. Universal claims remain hypotheses requiring wider controls.

### UNVTRSLR CONSEQUENCE

Treat every proposed universal as one of:

- `PHYSICAL_CANDIDATE_INVARIANT`
- `INTERACTIONAL_CANDIDATE_INVARIANT`
- `HUMAN_CROSS_LINGUISTIC_REGULARITY`
- `SPECIES_OR_MODALITY_SPECIFIC_PATTERN`
- `UNRESOLVED`

These are evidence scopes, not ontology classes.

### ADVERSARIAL CHALLENGE

Any R3 feature that is necessary to pass must be tested against a synthetic positive oracle that communicates successfully **without** that human-specific feature. If the oracle fails solely because it lacks a human convention, the evaluator has leaked anthropology into the definition of communication.

**Crosswalk effect:** strengthens every `DO_NOT_INHERIT` field, especially `VSH-009` and `VSH-010`.

## Crosswalk disposition after first literature pass

This table is the research disposition for Task 2. The source crosswalk retains its original hypothesis records as the historical intake layer; later promotion edits should point back to this table rather than erase the original uncertainty.

| ID | First-pass status | Disposition |
| --- | --- | --- |
| `VSH-001` | `SUPPORTED` | Narrow: preserve tested invariants; function does not automatically outrank meaningful form. |
| `VSH-002` | `SUPPORTED` | Keep meaning/priority separation, but do not require the predecessor five-stage runtime architecture. |
| `VSH-003` | `SUPPORTED` | Strong fit with no-assumed-tokenization target; test continuous/multimodal segmentation. |
| `VSH-004` | `SUPPORTED` | Context dependence is well-supported; require typed context and causal/nuisance discrimination. |
| `VSH-005` | `SUPPORTED` | Preserve alternatives; representation format remains open to R1 competition. |
| `VSH-006` | `SUPPORTED` | Preserve epistemic/provenance distinctions; import permission/authority only for tasks where they exist. |
| `VSH-007` | `SUPPORTED` | Ambiguity is information when alternatives are materially distinct; scoped decision policies may choose while recording collapse. |
| `VSH-008` | `SUPPORTED` | Causal interventions/ablations and minimal pairs directly address misleading success metrics. |
| `VSH-009` | `SUPPORTED` | One-to-one lexical ontology is unsafe; richer mapping must not invent ambiguity in genuinely one-to-one codes. |
| `VSH-010` | `SUPPORTED` | Denotation/pragmatic function distinction is strong in human evidence; universal pragmatic labels remain prohibited. |
| `VSH-011` | `SUPPORTED` | Keep learned/embedding representations eligible, but similarity alone cannot certify grounding/equivalence. |
| `VSH-012` | `SUPPORTED` | Negative controls and simpler explanations are strongly justified by emergent-communication failures. |

`SUPPORTED` here means **supported as a scoped UNVTRSLR design/evaluation proposition**, not established universal truth.

## Rejected overclaims generated by this cycle

The first cycle already produced negative results worth preserving:

1. **REJECTED:** `FUNCTION_IS_MORE_UNIVERSAL_THAN_FORM` — unsupported. Function is a useful comparison dimension; form may carry meaning and may itself be the invariant.
2. **REJECTED:** `COMMON_GROUND_REQUIRES_PROVABLE_SYMMETRIC_MUTUAL_BELIEF` — too strong for an operational evaluator and contested even in convention theory.
3. **REJECTED:** `REPAIR_BEHAVIOR_PROVES_INTENTIONAL_COMMUNICATION` — a reflex policy can imitate repair.
4. **REJECTED:** `TASK_SUCCESS_PROVES_SHARED_SEMANTICS` — directly contradicted by emergent-communication results and causal-ablation failures.
5. **REJECTED:** `COMPOSITIONALITY_PROVES_GENERALIZATION_OR_HUMAN_LIKE_SYNTAX` — empirical relation is task-dependent; direct transfer metrics are required.
6. **REJECTED:** `CONTEXT_IS_ONE_FLAT_FEATURE_BUNDLE` — encourages leakage/confounding; typed dependencies and interventions are preferable.
7. **REJECTED:** `HUMAN_SPEECH_ACT_LABELS_ARE_SPECIES_NEUTRAL_PRIMITIVES` — no evidence supports this promotion.

These rejections are important: this lane is already changing predecessor ideas rather than decorating them.

## Next architecture frontier

The literature now supports writing four architecture-neutral documents without touching R1/R2 canon:

1. pragmatic/communicative-function hypotheses;
2. common ground and convention evidence;
3. semantic routing and segmentation;
4. typed functional/invariant translation.

Those documents should then generate R3 adversarial tests. R3 must evaluate pragmatic robustness without turning human pragmatics into the definition of communication.
