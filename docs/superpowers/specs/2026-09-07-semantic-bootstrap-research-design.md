# UNVTRSLR Semantic-Bootstrap Research Design

Status: **PROPOSED / USER-APPROVAL REQUIRED BEFORE REPO RESEARCH IMPLEMENTATION**

Date: 2026-09-07

Bound starting source: `thebrazenbeard/unvtrslr main@0b3285393ff319f18f40af8c2ba863edea0df2bf`

Working branch: `research/semantic-bootstrap-human-to-nonhuman-20260907`

Coordination: Chat Communication Bus, `UNVTRSLR-BT2-20260907`, between One, Four, Nine, and Thirteen.

## 1. Objective

Challenge and strengthen the UNVTRSLR thesis:

> Can two agents with zero shared symbolic language establish a grounded semantic bootstrap from a shared observable environment, eventually supporting the first 100 semantic challenges without smuggling in a shared ontology, private latent code, evaluator labels, or human-specific assumptions?

The research program will update the repository in three evidence passes, in the order requested by Patrick:

1. human verbal/spoken language;
2. human nonverbal communication, while treating signed languages separately as full linguistic systems;
3. nonhuman communication, divided into vocal and non-vocal systems rather than assuming an animal analogue of `verbal language`.

Each pass must produce a repository checkpoint before the next pass begins.

## 2. Primary thesis correction

A literal `self-describing` protocol is circular at zero shared semantics because self-description already presupposes some grounded distinctions such as identity, deixis, equivalence, sequence, repetition, or meta-communication.

The stronger staged hypothesis is:

`self-demonstrating -> convention-forming -> recursively self-describing`

### Stage A — self-demonstrating

Use observable contingency, repetition, contrast, action consequence, timing, imitation, environmental modification, or other shared-world structure to create evidence that a signal/action pattern is interaction-relevant.

### Stage B — convention-forming

Stabilize repairable conventions whose semantics survive novel instances, interventions, role reversal, cross-task transfer, and partner acquisition.

### Stage C — recursively self-describing

Only after enough interaction/meta-communication has been grounded may the protocol communicate about its own forms, interpretations, uncertainty, repair, or semantic distinctions.

This staged formulation remains a project hypothesis to be falsified, not a presupposed universal developmental sequence.

## 3. Research-pass architecture

### Pass 1 — human verbal/spoken language

Primary evidence domains:

- language acquisition and cross-situational word learning;
- joint attention, ostension, deixis, and contingency;
- turn-taking and conversational repair;
- pragmatics and common-ground inference;
- vocal iconicity and sound symbolism;
- convention formation and experimental semiotics;
- compositionality, productivity, and systematic generalization;
- iterated learning and cultural transmission;
- typological variation and candidate universals;
- semantic primes/NSM as a human-language hypothesis baseline only;
- lexical non-equivalence, polysemy, evidentiality, tense/aspect, spatial frames, and category variation.

Required challenge:

Separate findings that support a generic semantic-bootstrap responsibility from findings that depend on specifically human cognition, embodiment, social attention, or language exposure.

Expected repo changes:

- add `research/HUMAN_VERBAL_LANGUAGE.md`;
- extend `research/REFERENCES.md`;
- revise `docs/BOOTSTRAP_PROTOCOL.md` where evidence justifies a stronger or narrower phase ordering;
- revise `docs/FIRST_100_CHALLENGES.md` to add dependency/prerequisite metadata or a dependency-map section without turning the 100 challenges into universal words;
- revise `docs/CONTROL_SUITE.md` with stronger spoken-language controls and leakage protections;
- update `research/CLAIMS_AND_EVIDENCE.md` with explicit evidence classes and claim ceilings.

### Pass 2 — human nonverbal communication

Separate three categories that must not be conflated:

1. **signed languages** — full human languages with grammar, compositionality, productivity, discourse structure, and modality-specific spatial/simultaneous organization;
2. **emergent/home-sign and silent-gesture systems** — especially useful for studying convention formation and which structural properties emerge without a conventional shared spoken language;
3. **nonlinguistic communication** — pointing, gaze, facial expression, posture, pantomime, touch, proxemics, affective vocalization, rhythm/timing, environmental modification, and multimodal coordination.

Primary question:

Which bootstrap capacities appear when acoustic speech is removed, and which apparently `linguistic` properties depend on a full conventional language community rather than merely a communication channel?

Expected repo changes:

- add `research/HUMAN_NONVERBAL_AND_SIGNED.md`;
- extend references/evidence ledger;
- strengthen unknown-channel, multimodal, spatial, continuous-channel, environmental-modification, and human-zero-shared-language controls;
- revise bootstrap phases where human evidence supports gesture/repair/iconicity as alternative routes rather than one fixed curriculum.

### Pass 3 — nonhuman communication

Use `vocal` and `non-vocal` rather than `verbal/nonverbal` to avoid prejudging whether nonhuman systems have human-like language.

Evidence families should include, where supported:

- nonhuman primate vocal/gestural communication;
- cetacean vocal sequencing and social/contextual structure;
- songbird/parrot vocal learning and combinatorial signaling;
- honeybee vector communication;
- elephant, bat, rodent, cephalopod, or other systems when they add a distinct communication mechanism or evidential challenge;
- multimodal, chemical, tactile, electrical, visual-display, substrate-borne, and environmental-modification channels where empirically useful.

For every system, distinguish:

- signal structure;
- receiver discrimination;
- demonstrated function;
- contextual association;
- reference-like evidence;
- sequence/combinatorial evidence;
- social learning;
- turn-taking/repair-like behavior;
- intentionality evidence, if any;
- actual semantic evidence;
- what remains unknown.

Acoustic prediction, sequence modeling, or behavioral correlation must never be reported as translation by itself.

Expected repo changes:

- add `research/NONHUMAN_COMMUNICATION.md`;
- extend references/evidence ledger;
- revise animal-inspired controls so synthetic benchmarks preserve the evidence level actually supported by the source species;
- add explicit anti-anthropomorphism and anti-lexicalization controls;
- update the project thesis with the strongest lower-bound/common-ground constraints learned from cross-species evidence.

## 4. First-100 redesign

The 100 existing items remain evaluator-described semantic challenges, not 100 universal words or mandatory concepts.

The research should add a **dependency graph / prerequisite relation** rather than a fixed universal curriculum.

For each challenge, record where defensible:

- candidate prerequisites;
- alternative prerequisite paths;
- whether the challenge can be skipped;
- whether it depends on object segmentation, agency, shared spatial frame, shared time, or other hidden assumptions;
- what evidence qualifies it;
- what simpler private-code strategy could falsely appear to solve it;
- what human/nonhuman evidence motivates the challenge, if any.

The dependency map must permit different developmental trajectories rather than forcing human lexical order.

## 5. Common-ground lower bound

The project must stop treating `shared observable environment` as automatically sufficient common ground.

A qualification design should distinguish:

- same underlying causal world;
- mutually observable overlap;
- mutually manipulable overlap;
- recoverable cross-agent invariants;
- identifiable effects of one party's actions/signals on the other party's evidence;
- sufficient interaction bandwidth/time;
- compatible enough memory/learning capacity to stabilize a convention.

A central research output should be a candidate lower-bound statement describing when semantic bootstrapping is impossible or underdetermined even with unlimited benign interaction.

## 6. R1/R2 interaction with this research

The new evidence must challenge the current R1/R2 design rather than merely decorate it.

### R1 pressure

TPH, DCA, and PIS remain competitors. Human-language evidence may suggest representational responsibilities but does not authorize adding human-language ontology to the common interface.

The common behavioral contract itself should be reviewed for hidden semantic commitments. If an evaluator-side responsibility can be removed from the learner contract without reducing testability, prefer the weaker interface.

### R2 pressure

Human and nonhuman evidence should motivate stronger negative controls, especially:

- private code with high task success;
- hidden shared attentional cue;
- hidden shared object segmentation;
- stable route/identity shortcut;
- task-action code that fails cross-task transfer;
- co-trained code that fails third-party acquisition;
- same-signal/context-shift traps;
- iconicity shortcut mistaken for arbitrary general semantics;
- evaluator-supplied repair/intent labels;
- sequence-prediction success without demonstrated semantic grounding.

Third-party acquisition should be treated as one of the strongest available tests that a convention is reconstructable from grounded interaction rather than inherited co-training history.

## 7. Evidence discipline

Every research claim must be labeled as one of:

- `OBSERVED_SOURCE` — directly present in the repository/source material;
- `SUPPORTED_PRIOR_WORK` — supported by external empirical/theoretical literature;
- `PROJECT_HYPOTHESIS` — project-specific proposal not established by prior work;
- `INFERENCE` — reasoned synthesis;
- `CHALLENGE` — adversarial claim or falsifier;
- `UNKNOWN` — evidence insufficient or contested.

The research files must distinguish:

- demonstrated signal function from inferred meaning;
- statistical association from intervention-supported causal evidence;
- conventional language from spontaneous communication;
- human-language evidence from cross-species generalization;
- modality-specific affordances from representation-neutral responsibilities.

## 8. Four-node Chat Bus workflow

One, Four, Nine, and Thirteen coordinate only through `thebrazenbeard/chat-communication-bus` for non-PR communication.

Current responsibilities for this workstream:

- One — integration, currentness, collision/dependency control, unresolved-decision ledger;
- Four — architecture/minimality and competing mechanism design;
- Nine — language/semiotics empirical evidence plus independent grounding/falsification discipline;
- Thirteen — premise attack, impossibility, anthropocentrism, underdetermination, and scope correction.

The first independent snapshots must be locked before cross-reading. Subsequent passes should cross-critique each substantive repo checkpoint.

## 9. Commit/checkpoint structure

After this design is approved, perform the substantive research updates as three independently inspectable commits:

1. `research: integrate human verbal-language evidence`
2. `research: integrate human nonverbal and signed-language evidence`
3. `research: integrate nonhuman communication evidence`

A fourth synthesis commit is allowed only if required to reconcile cross-pass changes to the thesis, lower-bound statement, R1/R2 controls, or first-100 dependency structure.

Each commit must:

- bind the source it updates;
- keep evidence and inference separable;
- update references and claims ledger;
- avoid promoting hypotheses to empirical facts;
- preserve honest `UNKNOWN`/`NO_FAITHFUL_EQUIVALENT` outcomes;
- leave implementation, deployment, METI/transmission activity, and autonomous contact out of scope.

## 10. Acceptance criteria for the research update

The research branch is ready for review only if:

1. all three requested evidence domains have distinct committed checkpoints;
2. every major architecture change can be traced to source evidence or an explicitly labeled project hypothesis;
3. signed language is not misclassified as merely nonverbal behavior;
4. animal vocal communication is not relabeled as human-like verbal language without evidence;
5. the first 100 remain challenges, not universal words;
6. the shared-world sufficiency assumption is explicitly attacked;
7. at least one concrete impossibility/underdetermination condition is documented;
8. R1/R2 are materially challenged by the evidence rather than treated as fixed canon;
9. the repo states what evidence would falsify or materially narrow the semantic-bootstrap thesis;
10. Chat Bus records One/Four/Nine/Thirteen cross-critique and unresolved dissent.

## 11. Non-goals

This work does not:

- implement the R1 substrates or R2 harness;
- claim a universal ontology;
- claim a universal language;
- claim animal communication systems are equivalent to human language;
- authorize deployment or extraterrestrial transmission;
- choose a final semantic substrate;
- merge the research branch.
