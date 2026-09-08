# First 100 Semantic Challenges

## Important framing

These are **100 semantic challenges**, not 100 asserted universal concepts.

The experiment should not force the agents to invent human words corresponding to these labels. The evaluator uses the labels only to describe the capability being tested.

A successful pair may solve a challenge with a representation that does not map one-to-one onto the evaluator's vocabulary.

The objective is to test whether reusable semantic distinctions can be established, generalized, composed, and audited.

## Family A — recurrence, identity, and discrimination

1. Detect that two observations are repetitions of the same event pattern.
2. Distinguish repeated pattern from a novel pattern.
3. Establish a stable referent across small perceptual changes.
4. Distinguish two persistent referents of the same type.
5. Re-identify a referent after temporary occlusion/absence.
6. Establish a convention for selecting one referent among distractors.
7. Distinguish same-category from same-individual.
8. Detect that two signals are variants of one convention.
9. Detect that one signal form is being used for two different functions.
10. Communicate that identity is uncertain rather than forcing a match.

## Family B — quantity and magnitude

11. Distinguish none from some.
12. Distinguish one instance from repeated/multiple instances.
13. Distinguish fewer from more.
14. Establish exact small-number distinctions without shared numeral symbols.
15. Establish equality of quantity.
16. Establish inequality of quantity.
17. Communicate increase.
18. Communicate decrease.
19. Communicate approximate magnitude rather than exact count.
20. Discover a stable dimensionless ratio shared across sensory encodings.

## Family C — similarity, category, and feature

21. Establish that two observations share a property despite differing in others.
22. Establish that two observations differ along one property while matching others.
23. Learn a category from multiple positive examples without receiving the category label.
24. Reject an out-of-category instance.
25. Generalize a category to a novel instance.
26. Learn that one category is nested within another.
27. Learn overlapping categories.
28. Discover that the counterpart's category boundary differs from its own.
29. Communicate partial category membership/uncertainty.
30. Detect that no exact target category matches the source category.

## Family D — space and geometry

31. Establish near vs far relationally.
32. Establish left/right or an alternative directional distinction relative to a frame.
33. Establish above/below or an alternative vertical relation.
34. Establish inside/outside.
35. Establish between.
36. Establish in-front/behind or another ordered spatial relation.
37. Communicate direction independent of absolute coordinate notation.
38. Communicate distance using a negotiated scale or ratio.
39. Transfer a spatial relation across a viewpoint change.
40. Navigate to a novel target using only established spatial semantics.

## Family E — time, sequence, and recurrence

41. Establish before vs after.
42. Establish same-time/overlap where observable.
43. Establish duration comparisons.
44. Establish repeated periodic structure.
45. Distinguish event order from clock representation.
46. Communicate that an event happened previously.
47. Communicate that an event is expected later.
48. Recognize a recurring state after an intervening different state.
49. Communicate a sequence of three or more events.
50. Distinguish causal order from mere temporal order.

## Family F — change, action, and control

51. Establish that a state changed.
52. Distinguish spontaneous change from apparent agent-driven change.
53. Establish an action convention through demonstration.
54. Communicate approach vs withdraw.
55. Communicate start vs stop.
56. Communicate continuation/repetition of an action.
57. Request a choice among available actions.
58. Communicate completion vs interruption.
59. Transfer an action convention to a novel object.
60. Distinguish an observed action from a request to perform that action.

## Family G — causality, prediction, and counterfactuals

61. Discover that one event reliably predicts another.
62. Distinguish predictive correlation from intervention-supported causal influence.
63. Communicate a likely consequence of an action.
64. Communicate uncertainty about a consequence.
65. Use an intervention to distinguish two competing causal hypotheses.
66. Communicate a conditional relation: if X, then Y.
67. Communicate a condition under which the relation fails.
68. Transfer a learned causal relation to a novel configuration.
69. Communicate a counterfactual outcome for an action not taken.
70. Correct a previously inferred causal relation after contradictory evidence.

## Family H — communication about communication

71. Establish an attention-getting convention.
72. Establish acknowledgement/receipt.
73. Establish rejection or correction.
74. Establish repeat-again.
75. Establish slower/simpler or otherwise modified repetition.
76. Establish same-meaning/different-form.
77. Establish different-meaning/same-form depending on context.
78. Communicate uncertainty or lack of understanding.
79. Negotiate a new convention when the old one fails.
80. Explicitly retire or revise a convention after semantic drift.

## Family I — agency, knowledge, goal, and social perspective

81. Distinguish an agent-like responsive source from a nonresponsive process.
82. Establish self vs other perspective or an equivalent participant distinction.
83. Communicate which agent performed an action.
84. Communicate which agent is expected to act next.
85. Infer and communicate an apparent goal from repeated behavior, with uncertainty.
86. Distinguish a counterpart's supplied goal claim from the translator's inferred goal.
87. Establish that one agent has access to information another lacks.
88. Communicate known vs unknown information.
89. Detect a mistaken counterpart belief through behavior.
90. Preserve the distinction between an assertion, request, question-like probe, and warning-like signal if such functions emerge.

## Family J — composition, abstraction, and non-equivalence

91. Combine two established semantic distinctions in a novel message.
92. Combine three or more distinctions in a novel configuration.
93. Communicate a relation between two novel categories.
94. Communicate a rule/generalization rather than one example.
95. Transfer an established semantic structure to a new task.
96. Explain a source distinction using a compound target construction when no single target convention exists.
97. Detect a one-to-many mapping between source and target concepts.
98. Detect a many-to-one collapse in the target system.
99. Correctly return `UNKNOWN` when evidence is insufficient.
100. Correctly return `NO_FAITHFUL_EQUIVALENT` for a demonstrated source distinction that the target system cannot yet express.

## Qualification pattern

The challenge number itself is not a pass/fail test. Each challenge receives a preregistered evaluator contract.

Where applicable, qualification should require:

- withheld examples;
- novel contexts;
- role reversal;
- contrastive minimal pairs;
- composition;
- intervention;
- calibration;
- semantic conservation accounting;
- a negative control that can succeed at the surface task while lacking the intended semantic capability.

## Difficulty dimensions

Each challenge can be independently hardened along these axes:

- shared sensors -> asymmetric sensors;
- discrete channel -> continuous channel;
- known channel -> unknown signalhood;
- aligned object segmentation -> different segmentation;
- cooperative partner -> noisy/noncooperative partner;
- immediate feedback -> delayed feedback;
- shared coordinate frame -> different frames;
- static semantics -> drifting semantics;
- exact target equivalent -> partial/non-equivalent target;
- single task -> cross-task transfer.

This allows the first 100 challenges to generate a much larger test space without pretending that 100 evaluator labels are the fundamental alphabet of intelligence.

---

## Dependency-aware interpretation — human verbal-language Pass 1

Human-language evidence does not justify treating the numeric order above as a universal developmental curriculum. The challenge inventory should instead be interpreted as a **dependency graph with alternative routes**.

### Rule 1 — identifiability precedes prerequisite claims

For every challenge, first ask whether the target distinction is actually identifiable through the available interaction surface.

If two candidate mappings cannot be distinguished by any learner-observable history or mutually available intervention, the correct outcome is not `FAILED_TO_LEARN`; it is `UNDERDETERMINED_IN_SCOPE` or `UNIDENTIFIABLE_WITHIN_INTERACTION_SURFACE`.

### Rule 2 — prerequisites are hypotheses, not evaluator gifts

A challenge may depend on capabilities such as recurrence detection, contrast, stable segmentation, temporal ordering, participant distinction, or repair. Those dependencies must be declared and tested rather than silently supplied.

A prerequisite record should include:

- `challenge_id`;
- `candidate_prerequisites[]`;
- `alternative_paths[]`;
- `hidden_assumptions[]`;
- `can_skip`;
- `qualification_evidence[]`;
- `false_success_modes[]`;
- `human_evidence_basis[]` where applicable.

### Rule 3 — multiple bootstrap routes must remain legal

Human evidence supports several useful routes but no single mandatory sequence:

- repeated cross-situational evidence can reduce referential ambiguity without perfect one-shot joint attention;
- repair can expose misunderstanding before a rich lexicon exists;
- iconicity can accelerate some form/meaning mappings;
- negotiated conventions can arise through restricted unfamiliar channels;
- later cultural transmission can increase regularity/compositionality after a system already exists.

Therefore the harness must permit, for example:

- repair before stable noun-like reference;
- action conventions before object categories;
- quantity/recurrence distinctions before participant identity;
- spatial relations without left/right if another coordinate system is negotiated;
- composition through non-concatenative or continuous signaling;
- no explicit `self/other` distinction if the successful representation uses a different participant structure.

### Rule 4 — Family H is not merely a late family

Items 71-80 are numbered late for organization, not because meta-communication must wait until challenges 1-70 are complete.

Human conversational repair suggests that limited communication-about-communication can be useful very early. An experiment may therefore attempt 72-75 or 78 before many referential challenges, provided those functions emerge from observable behavior rather than evaluator-supplied semantic labels.

### Rule 5 — hidden assumptions by family

The following are common hidden subsidies to declare explicitly:

- **A (identity):** stable object/event segmentation, persistence model, temporal grain;
- **B (quantity):** countable-unit segmentation, recurrence detection, aggregation window;
- **C (category):** feature comparability, positive-example selection, evaluator category boundaries;
- **D (space):** coordinate frame, viewpoint relation, dimensionality, shared geometry;
- **E (time):** comparable timescale, event boundaries, ordering observability;
- **F (action):** identifiable agent/action boundary, controllability, action-effect latency;
- **G (causality):** intervention availability, causal sufficiency, stable mechanism window;
- **H (meta-communication):** interaction failure must itself become observable without evaluator labels;
- **I (agency/knowledge):** agent decomposition, information-access model, goal/belief concepts;
- **J (composition/non-equivalence):** stable lower-level distinctions, target search space, composition budget.

### Rule 6 — human-language false-success modes

Human verbal-language experiments must include or audit against these shortcuts:

1. shared gaze or experimenter-directed attention acting as the real label;
2. shared object IDs/segmentation supplied through the task interface;
3. pretrained linguistic/world knowledge reconstructing the intended category without grounding it in the counterpart interaction;
4. task instructions supplying the pragmatic frame the system is later credited with discovering;
5. negotiated task code reported as recovery of a pre-existing counterpart language;
6. iconic form/meaning resemblance acting as an undeclared answer key;
7. repair events explicitly tagged by the evaluator;
8. co-trained private codes that fail third-party acquisition;
9. one-to-one evaluator category recovery in a domain where human languages actually partition meanings differently.

### Rule 7 — `NO_FAITHFUL_EQUIVALENT` is scope-bounded

Challenge 100 should be interpreted operationally as:

`NO_FAITHFUL_EQUIVALENT_FOUND_WITHIN_TESTED_SCOPE`

unless a formal impossibility result justifies a stronger statement.

The result must bind the searched target representation family, permitted composition depth/complexity, tested contexts/interventions, and material computational/search budget.

### Candidate dependency clusters, not fixed order

A useful evaluator may group challenges into provisional clusters:

- **interaction stability:** 1-2, 8-10, 71-79;
- **referential/category stability:** 3-7, 21-30;
- **magnitude/structure:** 11-20, 31-50;
- **action/prediction:** 51-70;
- **participant/social perspective:** 81-90;
- **composition/translation limits:** 91-100.

These clusters are evaluator conveniences, not claims that cognition or language develops in that sequence.

The later human nonverbal/signed and nonhuman passes should attack this dependency structure again rather than inherit it as canon.

---

## Dependency refinements — human signed/nonverbal Pass 2

Pass 2 does not replace the 100 challenges. It changes what may count as a valid path through them.

### Rule 8 — composition is not synonymous with sequence

Challenges 91-94 must allow simultaneous or overlapping composition. A system should not fail merely because it combines distinctions through:

- two hands at once;
- manual plus facial/head movement;
- a persistent spatial locus plus a simultaneous motion;
- timing/synchrony rather than concatenation.

A test harness that serializes all evidence into evaluator-created gloss tokens has changed the challenge.

### Rule 9 — shared spatial frame is itself a candidate dependency

Challenges 31-40, 82-84, and some referential tasks must declare whether the agents share:

- origin and orientation;
- viewpoint;
- scale;
- persistent landmark identity;
- object segmentation;
- correspondence between physical and discourse space.

If those are supplied, record them as common-ground subsidies. Alternative qualification paths should allow agents to negotiate a frame or succeed using another relational scheme.

### Rule 10 — deixis and participant reference need functional disambiguation

Challenges 6, 71, 82-84, and related tasks must not treat a point/gaze direction as a pre-labeled referential act.

A valid control should make the same physical form plausibly serve:

- selection;
- location;
- participant marking;
- direction;
- command;
- attention management;
- or noncommunicative behavior.

Credit requires recovering the demonstrated functional pattern in context.

### Rule 11 — meta-communication may be layered onto content

Challenges 71-80 need not occupy separate turns or separate tokens. Repair, uncertainty, question-like force, discourse management, or emphasis may be distributed across a simultaneous nonmanual channel while another channel carries referential content.

The dependency graph therefore permits `meta-communication + content` as one interaction complex.

### Rule 12 — dyadic competence and community language are different qualification targets

A successful pair may solve challenges 1-100 without developing the systematicity of a mature community language. Conversely, structures observed after community/cohort transmission cannot be credited retroactively to an isolated pair.

Each result should record one of:

- `ISOLATED_OR_DYADIC`;
- `MULTI_USER_COMMUNITY`;
- `TRANSMITTED_ACROSS_COHORTS`.

This matters especially for challenges 8-9, 76-80, and 91-95, where conventionalization/systematization can grow over social transmission.

### Rule 13 — object-centered paths must have rivals

Families A, C, D, F, and I often read naturally in object/agent terms. At least some qualification worlds should provide alternative segmentation in which:

- trajectories or fields are more stable than objects;
- participant boundaries are ambiguous;
- relations are primary and object identity is secondary;
- persistent spatial loci do not map one-to-one to physical objects.

The challenge is to establish a reusable distinction, not to force the evaluator's object ontology.

### Rule 14 — attention-getting does not mean gaze/pointing

Challenge 71 must accept any empirically established interaction-management convention that reliably changes counterpart uptake/availability in scope. Gaze, pointing, touch, sound, motion, environmental change, or another channel may serve in human controls, but none is the semantic definition.

### Rule 15 — iconicity changes difficulty, not correctness

For challenges involving shape, motion, space, action, or affect, record whether the signal is:

- strongly iconic/motivated;
- weakly iconic;
- arbitrary;
- misleadingly iconic.

A mapping does not receive more semantic credit because its form resembles the evaluator's target. Iconicity is a difficulty/modality condition.

### Rule 16 — functional category uncertainty can remain after state discrimination succeeds

A form may reliably covary with a world state while its communicative function remains ambiguous. For example, a facial movement may be grammatical, affective, interactional, or incidental.

Therefore R0.5-style `state distinguishability` must not automatically satisfy challenges that require a communicative-function distinction.

### Pass 2 false-success additions

Add these to the evaluator's shortcut search:

1. English gloss or sign annotation supplied before learning;
2. pose/vision preprocessing that normalizes semantic spatial loci using evaluator truth;
3. sequentialization that deletes meaning-bearing simultaneity while retaining labels in metadata;
4. pretrained sign-language recognition mapping directly to known glosses;
5. pointing/gaze treated as a referent label by the harness;
6. universal-emotion classifier supplying facial semantics;
7. community-produced regularity credited to the initial dyad;
8. pantomime/iconicity success reported as arbitrary convention grounding;
9. visual preprocessing serving as Thirteen's semantic relay / bridge oracle.

The nonhuman Pass 3 must attack these human manual assumptions again rather than inheriting them as cross-species canon.
