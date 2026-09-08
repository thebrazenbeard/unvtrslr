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
9. **Communication success is not enough.** Agents can invent private codes that solve a task without learning the intended concepts.
10. **Meaning must survive tests.** Novel instances, context changes, role reversal, composition, intervention, and counterfactual prediction are stronger evidence than agreement on a symbol.
11. **English is a renderer, not the semantic center.** Other natural languages, diagrams, equations, actions, or other modalities are equally valid target realizations.
12. **A universal ontology is not assumed.** The universal layer should be a grammar for representing hypotheses, relationships, uncertainty, provenance, and evidence—not an encyclopedia of human concepts.

## Repository map

- [`docs/PROJECT_THESIS.md`](docs/PROJECT_THESIS.md) — the refined concept and hypotheses.
- [`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md) — architecture-level constraints.
- [`docs/SEMANTIC_SUBSTRATE.md`](docs/SEMANTIC_SUBSTRATE.md) — proposed formal intermediate representation.
- [`docs/BOOTSTRAP_PROTOCOL.md`](docs/BOOTSTRAP_PROTOCOL.md) — how communication could be established from zero shared symbols.
- [`docs/SEMANTIC_CONSERVATION.md`](docs/SEMANTIC_CONSERVATION.md) — what it means to preserve meaning.
- [`docs/EXPERIMENTAL_PROGRAM.md`](docs/EXPERIMENTAL_PROGRAM.md) — staged falsification program.
- [`docs/FIRST_100_CHALLENGES.md`](docs/FIRST_100_CHALLENGES.md) — 100 semantic challenges, not 100 presumed universal words.
- [`docs/CONTROL_SUITE.md`](docs/CONTROL_SUITE.md) — Earth-language, synthetic, nonlinguistic, asymmetric, and negative controls.
- [`docs/INTERSTELLAR_DEPLOYMENT.md`](docs/INTERSTELLAR_DEPLOYMENT.md) — probe, broadcast, and hybrid architectures.
- [`docs/FAILURE_MODES.md`](docs/FAILURE_MODES.md) — ways the project can fool itself.
- [`docs/RESEARCH_LANDSCAPE.md`](docs/RESEARCH_LANDSCAPE.md) — relationship to prior research.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered research phases and gates.
- [`research/CLAIMS_AND_EVIDENCE.md`](research/CLAIMS_AND_EVIDENCE.md) — evidence-status ledger.
- [`research/REFERENCES.md`](research/REFERENCES.md) — literature and source notes.

## The key experimental standard

A semantic mapping is not counted as established merely because the receiver performs correctly once.

A candidate concept should survive, where applicable:

1. novel instances;
2. novel contexts;
3. role reversal;
4. recombination with other established concepts;
5. interventions on the world;
6. counterfactual or predictive tests;
7. changed perceptual presentation;
8. independent reconstruction by an evaluator that does not share the agents' private latent state.

The system must also be rewarded for correctly saying that two conceptual structures are only partially overlapping or non-equivalent.

## Interstellar motivation

Historical interstellar messages such as the Pioneer plaques, Arecibo transmission, Voyager Golden Record, and the Lincos project attempt to construct content that a radically unfamiliar recipient might decode. UNVTRSLR asks a different question:

> **What if the transmitted artifact is not primarily the message, but the machinery for constructing a shared semantics?**

For an embodied probe, that machinery could interact locally with a recipient and a shared environment. For a broadcast, it could be a progressively self-describing semantic curriculum and protocol. A hybrid architecture could use both.

## Status

`RESEARCH_BOOTSTRAP / NOT_IMPLEMENTATION_READY`

This repository currently defines a research program, not a proven universal language, universal ontology, or extraterrestrial communication solution. The strongest claims here are intentionally written so they can fail.
