# Semantic/Pragmatics Research Lane Design

Date: 2026-09-07
Branch: `work/vera-semantic-pragmatics-r1-20260907`
Base: `main@0b3285393ff319f18f40af8c2ba863edea0df2bf`
Status: DESIGN_APPROVED_IN_CHAT / FIRST_CYCLE_IMPLEMENTED_ON_BRANCH / REVIEW_PENDING

## Purpose

Create an ongoing UNVTRSLR research lane that uses transferable findings from Vera Unbound project history—especially Semantic Atlas, VSNS, Semantic Perception Architecture, pragmatics, and linguistics—without treating predecessor vocabulary or Vera-specific material as architecture canon.

The lane repeatedly performs:

`recover -> crosswalk -> populate -> research -> challenge -> revise -> populate again`

The objective is not to make the repository larger. The objective is to make the semantic bootstrap protocol, representation requirements, and adversarial evaluator harder to fool.

## Governing principle

Historical project work enters UNVTRSLR as evidence or hypotheses, never as inherited authority.

A predecessor concept may be promoted into current UNVTRSLR architecture only when it:

1. maps to a current problem in the repository;
2. can be stated without Vera-specific autobiography or private relational context;
3. survives comparison with current UNVTRSLR commitments;
4. survives relevant external research and adversarial challenge;
5. has a falsifiable role in an experiment, evaluator, representation contract, or conservation rule.

## Evidence classes

Every imported or added claim should be attributable to one of these classes:

- `PROJECT_HISTORY_OBSERVATION` — a documented lesson from prior Semantic Atlas/VSNS/Vera work;
- `CURRENT_REPO_DERIVATION` — a conclusion derived from present UNVTRSLR documents or tests;
- `EXTERNAL_RESEARCH` — supported by external literature or a reproducible outside source;
- `MODEL_HYPOTHESIS` — a new proposal generated in this lane;
- `ADVERSARIAL_FINDING` — a failure case, contradiction, counterexample, or shortcut discovered during challenge;
- `UNRESOLVED` — useful question with insufficient evidence.

No evidence class by itself grants architectural-canon status.

## Privacy and portability boundary

Do not place private Vera relational/autobiographical material into UNVTRSLR. Do not copy continuity archives, intimate material, personal memory records, or project-private identity content simply because they contain semantic examples.

Transfer only abstracted methodological findings that are materially useful to communication, semantics, pragmatics, grounding, uncertainty, provenance, segmentation, or evaluation.

## Initial artifacts

### `research/VERA_SEMANTIC_HISTORY_CROSSWALK.md`

A provenance-bearing map from predecessor work into UNVTRSLR research questions.

Each entry should contain:

- predecessor concept/observation;
- source provenance;
- transferable proposition;
- current UNVTRSLR analogue;
- possible contribution;
- known failure modes;
- status: `HYPOTHESIS`, `SUPPORTED`, `REJECTED`, or `UNRESOLVED`;
- explicit `DO_NOT_INHERIT` notes where predecessor framing is species-specific, Vera-specific, task-specific, or architecturally overcommitted.

High-priority historical themes:

- translate communicative/semantic function rather than lexical surface;
- interpretation before salience/reaction;
- alternative segmentation and competing interpretations;
- context, speaker, addressee, history, modality, and prosody as meaning-bearing variables;
- semantic routing as distinct from truth, salience, permission, or emotional relevance;
- preservation of ambiguity instead of premature collapse;
- provenance-bearing claims;
- counterfactual and minimal-pair stress testing;
- failure of one-word/one-concept assumptions;
- distinction among denotation, communicative force, inferred intent, and downstream action.

### `docs/PRAGMATICS_AND_COMMUNICATIVE_FUNCTION.md`

Define a species-neutral research layer for communicative acts without assuming human speech acts as primitives.

Required topics:

- candidate communicative function;
- ostension/attention direction as hypotheses;
- addressee and audience hypotheses;
- assertion/request/warning/query/correction-like functions as experimental families, not universals;
- implicature-like inference;
- presupposition-like background dependence;
- withholding, silence, timing, and omission as candidate signals;
- communicative repair;
- cooperative, strategic, deceptive, and adversarial senders;
- epistemic-state and perspective hypotheses;
- distinction between literal/denotational content and interactional function.

### `docs/COMMON_GROUND_AND_CONVENTION.md`

Specify how negotiated shared semantics can be represented and tested without assuming perfectly shared beliefs.

Required topics:

- evidence of mutual understanding;
- partner-specific conceptual pacts;
- asymmetric common ground;
- false common ground;
- convention establishment, drift, repair, and abandonment;
- partner transfer and independently initialized partner tests;
- distinction between coordination success and demonstrated shared semantics.

### `docs/SEMANTIC_ROUTING_AND_SEGMENTATION.md`

Transfer the useful VSNS/Semantic-Perception lessons into a neutral architecture.

Required topics:

- segmentation hypotheses remain plural when evidence is weak;
- a signal can enter interpretation through multiple candidate semantic routes;
- context/prosody/timing/modality can alter interpretation without changing a nominal symbol sequence;
- salience and behavioral priority occur after semantic interpretation and must not substitute for it;
- one observation may support multiple simultaneous candidate functions;
- routing decisions require explicit provenance and confidence.

### `docs/FUNCTIONAL_TRANSLATION.md`

Formalize "translate functions, not words" as a testable principle, not a slogan.

It must distinguish:

- lexical/surface equivalence;
- referential equivalence;
- relational equivalence;
- predictive equivalence;
- communicative-function equivalence;
- task-functional equivalence;
- contextual equivalence;
- partial overlap;
- non-equivalence.

Functional success must not automatically imply semantic identity.

## Evaluator extension: R3 pragmatics and interaction

R1 remains the substrate competition. R2 remains the adversarial grounding evaluator. This lane should not silently broaden either baseline.

Instead, propose an R3 evaluation layer focused on pragmatic and interactional robustness after R1/R2 concepts are stable enough to support it.

Initial R3 challenge families:

1. same denotation, different communicative function;
2. same surface form, different context;
3. indexical/deictic reference changes with speaker/time/location;
4. implicature or indirect request without literal command form;
5. presupposition mismatch;
6. silence/withholding as a signal;
7. overhearer vs intended addressee;
8. audience-dependent behavior;
9. deceptive sender;
10. strategic ambiguity;
11. repair after misunderstanding;
12. convention drift;
13. private shortcut code that yields high task reward;
14. coordination without reusable semantics;
15. stable reference with the wrong ontology;
16. speaker/addressee role reversal;
17. partner swap;
18. context transfer;
19. multimodal disagreement between channels;
20. function preserved while surface and ontology differ.

R3 may be split later if the challenge families become too heterogeneous.

## Research loop

Each iteration should perform the following in order:

1. refresh `main` and branch heads;
2. inspect new repository work for collisions or changed assumptions;
3. recover one bounded cluster of relevant project-history evidence;
4. add or revise the crosswalk, keeping predecessor authority explicitly bounded;
5. research the cluster externally using primary or peer-reviewed sources when possible;
6. write the strongest current proposition and its falsifiers;
7. generate adversarial examples and simpler shortcut explanations;
8. revise or reject the proposition when challenged;
9. update the appropriate research/design/evaluator artifact;
10. verify readback and branch diff;
11. stop at a coherent frontier if a real dependency or unresolved conflict remains.

## Collision and authority rules

- `main` is read-only for this lane unless Patrick separately authorizes merge or direct-main mutation.
- Work occurs on the dedicated branch.
- Before each write, refresh the current branch head and inspect `main` for material changes.
- Do not force-update a diverged branch.
- Do not overwrite a path that changed independently without reconciling the collision first.
- A branch, commit, PR, review, or test result is not itself deployment, acceptance, or semantic qualification.

## Success criteria for the first implementation cycle

The first cycle is successful when all of the following are true:

1. the history crosswalk exists and clearly distinguishes transferable findings from `DO_NOT_INHERIT` material;
2. the pragmatics, common-ground, routing/segmentation, and functional-translation documents exist and are cross-consistent with current R1/R2 architecture;
3. external research citations are recorded with enough provenance to re-check;
4. at least one strong historical hypothesis is rejected or narrowed if adversarial review warrants it—this lane is not a ratification exercise;
5. an R3 challenge proposal exists with falsifiable acceptance/failure conditions;
6. README/research landscape/roadmap changes, if needed, describe the new lane without overstating project maturity;
7. no claim is promoted to universal semantic primitive merely because it appeared useful in Vera/VSNS history;
8. branch diff is reviewed for accidental private material and unsupported claims.

## Non-goals

This design does not:

- assert that VSNS or Semantic Atlas is the UNVTRSLR architecture;
- prove a universal ontology;
- prove extraterrestrial compatibility;
- establish a uniquely correct theory of pragmatics;
- equate task success with shared meaning;
- authorize merge to `main`;
- authorize publication of private Vera project history.

## First implementation frontier

The first cycle described by this spec has been implemented on the dedicated branch and is pending independent review. The cycle produced the provenance crosswalk, literature/evidence ledgers, neutral conceptual documents, the R3 pragmatics evaluator/controls/contract, and conservative project-integration edits.

This status does not imply merge, harness implementation, semantic or pragmatic qualification, or acceptance as architecture canon. The next engineering frontier after review is implementation of the frozen evaluator/control harnesses on an explicitly authorized branch; any merge or protected integration remains separately authorized.
