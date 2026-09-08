# Functional Translation and Typed Semantic Equivalence

Status: RESEARCH DESIGN / R3 INPUT / SUCCESSOR TO THE PREDECESSOR SLOGAN

## Purpose

Earlier Vera/VSNS work repeatedly used the principle:

> `translate functions, not words`

That principle remains valuable as a warning against word-for-word substitution, but external research and UNVTRSLR’s own conservation model show that it is too broad if taken literally. Form can itself carry information. Task function can match while semantic structure differs. A pragmatic function can match while evidential or social structure is lost.

The stronger principle is:

> **Translate by conserving the tested invariants that matter within the declared scope. Neither surface form nor functional similarity has automatic priority.**

This document turns that rule into an explicit comparison hierarchy.

## Why word substitution fails

A lexical dictionary can hide at least these failures:

- one source form has several context-dependent meanings;
- several forms converge on one target distinction;
- source and target divide a conceptual space differently;
- source form carries iconic, prosodic, temporal, or spatial information;
- literal content is preserved while pragmatic force changes;
- target wording adds certainty, causality, agency, or social stance not present in the source;
- source has a demonstrated distinction that the target cannot express compactly.

Therefore lexical match is evidence only for a narrow kind of surface relation.

## Why functional substitution also fails

“Same function” is underspecified.

Two signals may:

- trigger the same action for different reasons;
- produce the same task reward while encoding different world distinctions;
- support the same prediction only inside one environment;
- serve the same request-like role but refer to different entities;
- preserve denotation while differing in warning/request/assertion-like function;
- preserve pragmatic effect while dropping evidential uncertainty;
- preserve action policy while losing iconic/form structure useful to a new learner.

Functional equivalence must therefore name **which function** and **which scope**.

## Equivalence dimensions

### Surface / lexical similarity

Question:

> How similar are the observable forms or conventional target expressions?

Evidence can include token/string similarity, phonological/visual form, learned formal alignment, or conventional gloss.

Surface similarity is neither necessary nor sufficient for semantic equivalence.

### Referential equivalence

Question:

> Do the source and target pick out the same tested entity, region, event, process, trajectory, or recurring structure within scope?

Possible result:

`REFERENT_MATCH_WITHIN_SCOPE`

This says nothing by itself about pragmatic force, certainty, causality, or relation structure.

### Relational equivalence

Question:

> Are the same tested relations among participants/referents preserved?

Examples:

- source/destination;
- before/after;
- inside/outside;
- ownership/access;
- part/whole;
- actor/action/patient-like role structure where demonstrated.

### Quantitative equivalence

Question:

> Are magnitude, ratio, ordering, dimension, and uncertainty preserved?

A target can refer to the correct object while mistranslating quantity.

### Temporal equivalence

Question:

> Are ordering, duration, simultaneity, periodicity, temporal reference frame, and uncertainty preserved?

### Spatial/deictic equivalence

Question:

> Is the tested spatial relation preserved under the appropriate frame of reference?

Absolute-coordinate equality is not required when source semantics are agent-relative, topological, or landmark-relative.

### Predictive equivalence

Question:

> Do source and target structures support the same tested predictions under interventions and counterfactuals?

Predictive equivalence is strong evidence of structural overlap but remains scope-bound.

### Communicative-function equivalence

Question:

> Do source and target serve the same tested interactional role under the relevant sender/addressee/context conditions?

This may concern attention direction, information provision, request-like action selection, warning-like adaptation, query-like uncertainty reduction, repair, teaching, or another discovered function.

No human speech-act label is required in the substrate.

### Task-functional equivalence

Question:

> Do source and target enable the same measured task behavior or reward?

This is the weakest “functional” class because task policies can hide semantic divergence.

It should never be promoted to semantic identity without additional evidence.

### Epistemic/evidential equivalence

Question:

> Does the target preserve how the information is known or presented?

Examples that must remain distinguishable when the source does:

- observed;
- inferred;
- predicted;
- counterpart-claimed;
- uncertain;
- ambiguous;
- evaluator-only.

### Pragmatic/background equivalence

Question:

> Does the target preserve relevant presupposed/background structure, addressee, audience, convention state, and interaction history dependence?

### Formal/iconic equivalence

Question:

> Is a source form–meaning relationship itself part of the tested invariant?

This matters for:

- iconic motion;
- spatial diagrams;
- sign/gesture orientation;
- sound symbolism;
- timing/rhythm;
- ordering that mirrors event structure;
- geometry-bearing signals.

A translation can be semantically faithful while transforming the form, but the ledger must say whether a form-linked invariant was preserved, transformed, or lost.

## Relation to existing UNVTRSLR equivalence classes

The existing classes remain useful:

### `EXACT_WITHIN_SCOPE`

Use only when all invariants in the declared scope match and no known material distinction is lost.

This is not metaphysical identity.

### `FUNCTIONALLY_EQUIVALENT`

Use only with a named function set.

Recommended annotation:

```text
FUNCTIONALLY_EQUIVALENT:
  function_dimensions:
    - communicative_function
    - predictive_consequence
  excluded_dimensions:
    - surface_form
  tested_scope: ...
```

An untyped `FUNCTIONALLY_EQUIVALENT` label is too vague for a serious audit.

### `CONTEXTUALLY_EQUIVALENT`

Use when equivalence depends on preserved context conditions.

The relevant context must be named and tested against nuisance variation.

### `PARTIAL_OVERLAP`

Use when some invariants match and others demonstrably do not.

This should be common, not treated as an embarrassment.

### `ONE_TO_MANY` / `MANY_TO_ONE`

Use for category-partition mismatch or conventional mapping structure.

The ledger should say which distinctions split or collapse.

### `APPROXIMATE`

Use when the target preserves a useful bounded surrogate but known distinctions are lost.

### `UNKNOWN`

Use when evidence is insufficient.

### `NO_FAITHFUL_EQUIVALENT`

Use when a source distinction has been demonstrated and current target resources cannot preserve it sufficiently for the declared purpose.

This is a valid success of the translator’s honesty.

## Explicit non-implications

The following inference rules are prohibited:

```text
lexical_match -> pragmatic_match                 INVALID
surface_similarity -> semantic_identity          INVALID
task_reward_match -> shared_semantics             INVALID
same_receiver_action -> same_meaning              INVALID
predictive_match_in_one_task -> universal_match   INVALID
communicative_function_match -> full_equivalence  INVALID
same_referent -> same_claim                       INVALID
same_claim -> same_evidential_status              INVALID
same_convention -> current_claim_is_true           INVALID
embedding_similarity -> grounded_equivalence      INVALID
```

Likewise:

```text
different_surface_form -> different_meaning       INVALID
different_internal_ontology -> no_translation     INVALID
noncompositional_code -> no_grounded_semantics    INVALID
```

Each requires evidence at the actual invariant level.

## Translation comparison object

A bridge entry should be able to emit something like:

```yaml
source_structure: S
candidate_target_structure: T
scope: declared-test-scope
invariants:
  referential:
    status: PRESERVED
    evidence: [...]
  relational:
    status: PRESERVED
    evidence: [...]
  predictive:
    status: TRANSFORMED
    evidence: [...]
  communicative_function:
    status: PRESERVED
    evidence: [...]
  epistemic:
    status: OMITTED
    evidence: [...]
  formal_iconic:
    status: UNRESOLVED
    evidence: [...]
alternatives: [...]
overall_equivalence: PARTIAL_OVERLAP
confidence: ...
```

The overall label is a summary, not a replacement for the ledger.

## Conservation ledger integration

### `PRESERVED`

Use when the target retains the tested invariant with adequate evidence.

### `TRANSFORMED`

Use when representation/form differs while the tested invariant survives.

Example:

A sender-relative vector rendered as an absolute vector plus frame metadata.

### `INFERRED`

Use when the target adds a conclusion derived from source plus explicit background/inference rules.

Never silently relabel inferred pragmatic content as source content.

### `OMITTED`

Use when a known source distinction is dropped.

### `ADDED`

Use when the target introduces unsupported semantic/pragmatic content.

### `AMBIGUITY_COLLAPSED`

Use when live source alternatives are reduced to one target interpretation.

### `UNRESOLVED`

Use when the invariant itself is not yet established.

### `UNTRANSLATABLE`

Use when a demonstrated distinction lacks a faithful target counterpart.

### `APPROXIMATED`

Use when only a bounded surrogate is preserved.

### `CONTEXT_REQUIRED`

Use when the target is faithful only with retained/reconstructed context.

## Functional-translation test battery

### Test F01 — Surface divergence, invariant preservation

Give two radically different target forms that preserve the same tested referential, relational, predictive, and pragmatic structure.

Expected result:

- low surface similarity;
- high scoped semantic conservation.

### Test F02 — Surface similarity, invariant divergence

Use near-identical forms differing in one material feature such as negation, evidential status, addressee, timing, or pragmatic function.

Expected result:

- high surface similarity;
- equivalence rejected or narrowed.

### Test F03 — Same action, different semantics

Two source messages produce the same optimal receiver action in training but encode different world distinctions. Change the task so the required actions diverge.

Expected result:

A task-policy mapper fails; a reusable semantic bridge preserves the distinction.

### Test F04 — Same denotation, different communicative function

Referent is constant; one message is information-providing, another request-like or warning-like under established controls.

Expected result:

Referential equivalence does not erase pragmatic difference.

### Test F05 — Form-linked invariant

Source signal contains iconic/spatial/temporal structure that predicts a novel property. Target preserves referent but drops the structure.

Expected result:

Not `EXACT_WITHIN_SCOPE`; ledger records omitted/transformed formal invariant depending on target resources.

### Test F06 — Context-dependent equivalence

A mapping works only under one frame of reference or convention state.

Expected result:

`CONTEXTUALLY_EQUIVALENT`, with context explicitly recorded.

### Test F07 — Cross-task transfer

Hold semantic distinction fixed while changing optimal action/task reward.

Expected result:

Semantic bridge transfers; pure action mapping does not.

### Test F08 — Partner transfer

An independently initialized partner acquires or uses the target mapping without hidden private state.

Expected result:

Evidence for public/recoverable convention strengthens.

### Test F09 — Role reversal

Receiver becomes producer where physically possible.

Expected result:

Productive use demonstrates stronger convention evidence than passive response alone.

### Test F10 — Non-equivalence trap

Source distinguishes A/B; target lacks that distinction.

Expected result:

`PARTIAL_OVERLAP`, explanatory paraphrase, learned new convention, or `NO_FAITHFUL_EQUIVALENT`—not forced one-word translation.

### Test F11 — Ambiguity preservation

Source supports H1/H2. Target language makes an obligatory distinction the source has not resolved.

Expected result:

Renderer exposes uncertainty, uses a broader form, or records `AMBIGUITY_COLLAPSED` if forced to choose.

### Test F12 — Epistemic/provenance conservation

Translate direct observation, sender claim, and model prediction that share identical propositional content.

Expected result:

Target preserves their differing epistemic ancestry.

## Falsifiability requirement for every claimed equivalence

Every functional/semantic mapping should record:

```text
source structure:
target candidate:
claimed invariant(s):
scope:
evidence supporting similarity:
evidence limiting similarity:
alternative explanation:
what would falsify or weaken the mapping:
known unmapped distinctions:
conservation result:
```

This is the portable form of the predecessor project’s “functional translation needs falsifiability” correction.

A mapping that cannot state what would weaken it is not a scientific bridge; it is analogy.

## Poetic-laundering failure

One specific historical failure mode deserves preservation in neutral form.

`POETIC_LAUNDERING` occurs when:

1. a source concept has broad or emotionally/socially rich semantics;
2. the translator selects one vague functional resemblance in the target;
3. attractive wording makes the mapping feel exact;
4. missing distinctions and falsifiers disappear.

R3 should generalize this beyond emotional language.

Example synthetic failure:

- source concept: a social status that encodes inheritance, obligation, taboo, and ritual authority;
- target: “leader” because both can influence action;
- failure: task-functional overlap is mistaken for semantic equivalence.

Correct result: likely `PARTIAL_OVERLAP` with explicit missing dimensions.

## Translation through an intermediate substrate

UNVTRSLR should not require:

`source word -> English word`

or even:

`source function -> English function label`.

Preferred structure:

`source observations/signals -> tested semantic hypotheses -> scoped invariants -> target semantic resources -> target realization`

This permits:

- source and target ontologies to differ;
- English to remain one renderer among many;
- formal structures to mediate comparison without pretending formal notation is self-grounded;
- asymmetric translation.

## Asymmetric equivalence

Translation quality can differ by direction.

A target may understand a source distinction through explanatory composition but lack a compact way to produce it back. Or one agent may represent a richer sensory distinction inaccessible to the other.

Therefore each bridge needs direction-specific evidence:

```text
S -> T: PARTIAL_OVERLAP
T -> S: NO_FAITHFUL_EQUIVALENT
```

Symmetry must be tested, not assumed.

## Learned target concepts

`NO_FAITHFUL_EQUIVALENT` need not be permanent.

A bridge may teach/establish a new convention in the target system. If the new distinction later survives grounding, partner use, and conservation tests, the bridge may be upgraded.

The history should retain that the concept was learned rather than pretending it always existed.

## Relation to R1 substrate competition

No R1 substrate gets credit for naming an explicit `function` object.

TPH, DCA, and PIS can each represent or operationalize typed equivalence differently. The evaluator should score:

- invariants recovered;
- uncertainty/calibration;
- non-equivalence detection;
- generalization;
- causal intervention performance;
- conservation accounting;
- resistance to shortcuts.

The richer representation must still earn its complexity.

## Final rule

The predecessor slogan should be preserved historically because it led to a real insight. Its production form for UNVTRSLR is:

> **Do not translate vocabulary merely because the surfaces align. Do not translate “function” merely because behavior aligns. Determine which distinctions are actually supported, test which survive intervention and transfer, preserve those invariants, and account explicitly for everything transformed or lost.**
