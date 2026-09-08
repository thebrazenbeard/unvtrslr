# UNVTRSLR

**Universal semantic mediation for communication without a shared language.**

UNVTRSLR began from a simple idea: if humanity wants to communicate with an unknown intelligence, especially an extraterrestrial one, sending a static message may be the wrong abstraction. A better artifact may be a system that can **discover how the other party communicates, establish shared reference, negotiate a semantic bridge, and then translate through that bridge**.

The original shorthand was:

> any language -> math -> English

The research program in this repository uses a stronger formulation:

> **meaning-bearing observations -> grounded formal semantic hypotheses -> tested shared semantics -> target rendering**

Mathematics is therefore not assumed to *be* universal meaning. It is used as a formal carrier for structures that have been grounded, tested, and assigned explicit uncertainty and provenance.

## Core research question

Can two agents with:

- zero shared symbols,
- no assumed linguistic communication channel,
- potentially different sensory systems,
- potentially different internal ontologies,
- and only a shared observable environment,

**discover signalhood, establish grounded semantic invariants, create compositional communication, and identify both translatable and genuinely non-equivalent concepts?**

If that can be demonstrated under increasingly hostile controls, UNVTRSLR becomes more than a translator. It becomes a candidate **semantic bootstrap protocol**.

## Why this is different from ordinary translation

Ordinary machine translation assumes both sides already use human language and that enough semantic overlap exists to map one linguistic surface into another.

UNVTRSLR does not assume:

- words,
- syntax,
- discrete symbols,
- speech,
- text,
- shared sensory categories,
- a shared ontology,
- a shared concept of an object,
- or even that a behavior is intended as communication.

The system must be able to consider continuous signals, timing, motion, geometry, environmental modification, multimodal behavior, and contextual meaning.

## Foundational design commitments

1. **Ground before translating.** Formal symbols do not become meaningful merely by referring to other symbols.
2. **Do not assume language.** Linguistic communication is one possible channel, not the architecture.
3. **The environment is the first Rosetta Stone.** Shared observations and interventions provide candidate common reference.
4. **Signalhood is a hypothesis.** The system must distinguish behavior from communication rather than receiving a pre-labeled message stream.
5. **Meaning is contextual.** Signal + environment + history + sender state + receiver state may be required to infer meaning.
6. **Uncertainty is part of meaning.** Ambiguity must not be silently collapsed.
7. **Provenance is part of meaning.** Observation, supplied claim, inference, prediction, and evaluator truth must remain distinct.
8. **Translation may be lossy or impossible.** `NO_FAITHFUL_EQUIVALENT` is a valid result.
9. **Communication success is not enough.** Agents can invent private codes that solve a task without learning reusable grounded distinctions.
10. **Arbitrary notation is not failure.** A convention may use arbitrary signs; the failure is hidden common ground or task-bound code that does not survive grounding tests.
11. **Meaning must survive tests.** Novel instances, context changes, role reversal, composition, intervention, cross-task transfer, partner transfer, and counterfactual prediction are stronger evidence than agreement on a symbol.
12. **English is a renderer, not the semantic center.** Other natural languages, diagrams, equations, actions, or other modalities are equally valid target realizations.
13. **A universal ontology is not assumed.** The universal layer should be a grammar for representing hypotheses, relationships, uncertainty, provenance, and evidence—not an encyclopedia of human concepts.
14. **Grounding claims are scoped.** No finite evaluator proves a uniquely correct ontology or universal meaning; certificates bind the exact worlds, interventions, controls, and threats survived.
15. **Pragmatic function is also a hypothesis.** Addressee, communicative function, background assumptions, repair, convention state, and sender reliability must be tested rather than inferred from human-looking form.
16. **Preserve tested invariants, not slogans.** Surface identity is neither necessary nor sufficient for faithful translation, but functional similarity is not sufficient either; form must be conserved when form itself carries a demonstrated distinction.

## Current R1/R2 architecture challenge

The project now has three deliberately competing minimal semantic substrates:

- **TPH — Typed Probabilistic Hypergraph:** explicit structured relational hypotheses;
- **DCA — Denotational Constraint Algebra:** executable constraints/operators over compatible situations and trajectories;
- **PIS — Predictive-Intervention State:** action-conditioned predictions and signal-induced predictive changes.

No substrate is architecture canon. The richer candidates must empirically earn their additional commitments.

The R2 evaluator is designed to distinguish grounded convention from private shortcut code using causal message interventions, world-factor interventions, nuisance shifts, role reversal, cross-task transfer, partner swap, sensor shifts, counterfactual tests, ontology mismatch, conservation audits, and a required suite of intentionally deceptive negative controls.

A passing result may eventually receive `GROUNDED_WITHIN_TESTED_SCOPE`; there is intentionally no `UNIVERSALLY_GROUNDED` status.

## R3 pragmatics and interaction challenge

R3 retains the existing human-language and synthetic-language control phase and adds a scoped pragmatics/interaction qualification profile. It asks whether a grounded bridge still preserves meaning when reference alone is insufficient—for example when the same referent is used with a different communicative function, when perspective or addressee changes, when a convention drifts, when the sender is deceptive, when silence rather than an emitted symbol matters, or when modalities conflict.

The R3 design intentionally treats human pragmatic categories as **test families**, not universal ontology. Its positive controls include a synthetic nonhuman communicative-function oracle specifically to catch evaluators that accidentally define communication as human speech acts.

The required negative controls are designed to look competent on naive metrics: task-policy codes, partner-ID policies, context lookup tables, surface speech-act classifiers, canned repair, fixed-coordinate deixis, audience-label leakage, reward predictors, forced intent labeling, and fluent-but-lossy pragmatic rendering.

A future passing result may receive `PRAGMATICALLY_GROUNDED_WITHIN_TESTED_SCOPE`. There is intentionally no `UNIVERSAL_PRAGMATICS` status, and R3 cannot compensate for R2 grounding failure.

## Repository map

- [`docs/PROJECT_THESIS.md`](docs/PROJECT_THESIS.md) — the refined concept and hypotheses.
- [`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md) — architecture-level constraints.
- [`docs/SEMANTIC_SUBSTRATE.md`](docs/SEMANTIC_SUBSTRATE.md) — proposed semantic responsibilities before R1 competition.
- [`docs/R1_SUBSTRATE_COMPETITION.md`](docs/R1_SUBSTRATE_COMPETITION.md) — three genuinely competing minimal semantic substrates and the fair competition rule.
- [`docs/R2_ADVERSARIAL_EVALUATOR.md`](docs/R2_ADVERSARIAL_EVALUATOR.md) — adversarial semantic-grounding evaluator and scoped certificate.
- [`docs/R2_NEGATIVE_CONTROLS.md`](docs/R2_NEGATIVE_CONTROLS.md) — 25 shortcut systems plus positive oracles the harness must classify correctly.
- [`specs/R1R2_EVALUATION_CONTRACT_V1.yaml`](specs/R1R2_EVALUATION_CONTRACT_V1.yaml) — machine-readable R1/R2 evaluation contract.
- [`docs/PRAGMATICS_AND_COMMUNICATIVE_FUNCTION.md`](docs/PRAGMATICS_AND_COMMUNICATIVE_FUNCTION.md) — species-neutral candidate communicative-function layer.
- [`docs/COMMON_GROUND_AND_CONVENTION.md`](docs/COMMON_GROUND_AND_CONVENTION.md) — scoped common-ground evidence, convention lifecycle, false-common-ground tests, and transfer.
- [`docs/SEMANTIC_ROUTING_AND_SEGMENTATION.md`](docs/SEMANTIC_ROUTING_AND_SEGMENTATION.md) — plural segmentation, context-sensitive route competition, multimodality, and the separation of interpretation from salience.
- [`docs/FUNCTIONAL_TRANSLATION.md`](docs/FUNCTIONAL_TRANSLATION.md) — typed invariant-conservation successor to “translate functions, not words.”
- [`docs/R3_PRAGMATICS_EVALUATOR.md`](docs/R3_PRAGMATICS_EVALUATOR.md) — P01–P20 adversarial pragmatic/interaction evaluator.
- [`docs/R3_NEGATIVE_CONTROLS.md`](docs/R3_NEGATIVE_CONTROLS.md) — strong intentionally broken pragmatic systems plus positive oracles.
- [`specs/R3_EVALUATION_CONTRACT_V1.yaml`](specs/R3_EVALUATION_CONTRACT_V1.yaml) — machine-readable R3 evaluation contract.
- [`docs/BOOTSTRAP_PROTOCOL.md`](docs/BOOTSTRAP_PROTOCOL.md) — how communication could be established from zero shared symbols.
- [`docs/SEMANTIC_CONSERVATION.md`](docs/SEMANTIC_CONSERVATION.md) — what it means to preserve meaning.
- [`docs/EXPERIMENTAL_PROGRAM.md`](docs/EXPERIMENTAL_PROGRAM.md) — staged falsification program.
- [`docs/FIRST_100_CHALLENGES.md`](docs/FIRST_100_CHALLENGES.md) — 100 semantic challenges, not 100 presumed universal words.
- [`docs/CONTROL_SUITE.md`](docs/CONTROL_SUITE.md) — Earth-language, synthetic, nonlinguistic, asymmetric, and negative controls.
- [`docs/INTERSTELLAR_DEPLOYMENT.md`](docs/INTERSTELLAR_DEPLOYMENT.md) — probe, broadcast, and hybrid architectures.
- [`docs/FAILURE_MODES.md`](docs/FAILURE_MODES.md) — ways the project can fool itself.
- [`docs/RESEARCH_LANDSCAPE.md`](docs/RESEARCH_LANDSCAPE.md) — relationship to prior research, including pragmatics/common ground/repair/iconicity/emergent-communication cautions.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered research phases and gates.
- [`research/CLAIMS_AND_EVIDENCE.md`](research/CLAIMS_AND_EVIDENCE.md) — evidence-status ledger.
- [`research/REFERENCES.md`](research/REFERENCES.md) — base literature and source notes.
- [`research/R1R2_RESEARCH_NOTES.md`](research/R1R2_RESEARCH_NOTES.md) — representation/evaluator research synthesis.
- [`research/R1R2_REFERENCES.md`](research/R1R2_REFERENCES.md) — sources added specifically for R1/R2.
- [`research/VERA_SEMANTIC_HISTORY_CROSSWALK.md`](research/VERA_SEMANTIC_HISTORY_CROSSWALK.md) — provenance-bearing transfer of predecessor semantic lessons, with explicit `DO_NOT_INHERIT` boundaries.
- [`research/PRAGMATICS_RESEARCH_NOTES.md`](research/PRAGMATICS_RESEARCH_NOTES.md) — adversarial synthesis and rejected overclaims from the first pragmatics research cycle.
- [`research/PRAGMATICS_REFERENCES.md`](research/PRAGMATICS_REFERENCES.md) — re-checkable literature ledger and scope limits.

## The key experimental standard

A semantic mapping is not counted as established merely because the receiver performs correctly once.

A candidate distinction should survive, where applicable:

1. communication ablation;
2. direct message intervention;
3. world-factor intervention;
4. nuisance transformations;
5. novel instances;
6. novel contexts;
7. role reversal;
8. recombination with other established distinctions;
9. transfer to a task with different optimal actions;
10. acquisition/use by an independently initialized partner;
11. changed perceptual presentation;
12. counterfactual or predictive tests;
13. ontology-mismatch/non-equivalence traps;
14. independent evaluator reconstruction;
15. provenance and semantic-conservation audit;
16. automated search for simpler shortcut explanations;
17. pragmatic-function contrast under fixed denotation;
18. addressee/audience and perspective shifts;
19. targeted repair versus reflex repair;
20. pragmatic conservation under ambiguity, deception, and multimodal conflict.

The system must also be rewarded for correctly saying that two conceptual structures are only partially overlapping or non-equivalent.

## Interstellar motivation

Historical interstellar messages such as the Pioneer plaques, Arecibo transmission, Voyager Golden Record, and the Lincos project attempt to construct content that a radically unfamiliar recipient might decode. UNVTRSLR asks a different question:

> **What if the transmitted artifact is not primarily the message, but the machinery for constructing a shared semantics?**

For an embodied probe, that machinery could interact locally with a recipient and a shared environment. For a broadcast, it could be a progressively self-describing semantic curriculum and protocol. A hybrid architecture could use both.

## Status

`R1_R2_DESIGN_BASELINED / R3_PRAGMATICS_DESIGN_SPECIFIED / IMPLEMENTATION_NOT_STARTED / NO_SEMANTIC_OR_PRAGMATIC_QUALIFICATION`

The repository currently defines a research program and adversarial qualification designs, not a proven universal language, universal ontology, universal pragmatics, or extraterrestrial communication solution. The strongest claims here are intentionally written so they can fail.
