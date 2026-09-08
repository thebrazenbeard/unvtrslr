# UNVTRSLR

**Universal semantic mediation for communication without a shared language.**

UNVTRSLR began from a simple idea: if humanity wants to communicate with an unknown intelligence, especially an extraterrestrial one, sending a static message may be the wrong abstraction. A better artifact may be a system that can **discover how the other party communicates, establish shared reference where possible, negotiate a semantic bridge, and then translate through that bridge**.

The original shorthand was:

> any language -> math -> English

The research program in this repository uses a stronger formulation:

> **meaning-bearing observations -> grounded formal semantic hypotheses -> tested scoped correspondences -> target rendering**

Mathematics is therefore not assumed to *be* universal meaning. It is used as a formal carrier for structures that have been grounded, tested, and assigned explicit uncertainty and provenance.

## Core research question

The first controlled experiment asks:

Can two agents with:

- zero shared symbols,
- no assumed linguistic communication channel,
- potentially different sensory systems,
- potentially different internal ontologies,
- and only a partially shared observable interaction surface,

**discover signalhood, establish grounded semantic invariants, create reusable/compositional communication, and identify both translatable and genuinely non-equivalent concepts?**

The broader theory is deliberately weaker than `two agents exchanging messages`. Cross-species evidence motivates a more general question:

> Can initially unaligned adaptive systems or coupled processes with partially overlapping observables and influence surfaces construct scoped, testable, reusable cross-system semantic correspondences without a pre-shared symbolic language?

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
- a single sender and receiver,
- synchronous message events,
- a communication channel separate from ordinary sensing,
- or even that a behavior is intended as communication.

The system must be able to consider continuous signals, timing, motion, geometry, environmental modification, multimodal behavior, persistent traces, distributed authorship, and contextual meaning.

## Foundational design commitments

1. **Ground before translating.** Formal symbols do not become meaningful merely by referring to other symbols.
2. **Do not assume language.** Linguistic communication is one possible channel, not the architecture.
3. **The environment is candidate common ground, not a guaranteed Rosetta Stone.** Shared physics does not imply shared segmentation, perceptual metric, timescale, or semantic variable.
4. **Signalhood is a hypothesis.** The system must distinguish behavior from communication rather than receiving a pre-labeled message stream.
5. **Channel is a hypothesis.** Communication may be acoustic, signed, spatial, chemical, electrical, tactile, substrate-borne, persistent, multimodal, or fused with ordinary sensing.
6. **Meaning is contextual.** Pattern + environment + history + participant state + receiver effect may be required to infer function.
7. **Uncertainty is part of meaning.** Ambiguity must not be silently collapsed.
8. **Provenance is part of meaning.** Observation, supplied claim, inference, prediction, evaluator truth, negotiated convention, and pre-existing correspondence must remain distinct.
9. **Translation may be lossy or impossible.** `NO_FAITHFUL_EQUIVALENT_FOUND_WITHIN_TESTED_SCOPE` is a valid result.
10. **Communication success is not enough.** Agents can invent private codes or exploit task artifacts without learning reusable grounded distinctions.
11. **Rich signal structure is not enough.** Tokenization, clustering, prediction, synthesis, sequence structure, identity cues, and classifier-readable context remain below semantic qualification unless stronger receiver/world evidence supports the claim.
12. **Arbitrary notation is not failure.** A convention may use arbitrary signs; the failure is hidden common ground or task-bound code that does not survive grounding tests.
13. **Meaning must survive appropriate tests.** Novel instances, context changes, receiver effects, role reversal where applicable, composition/systematic reuse, intervention or other discriminating histories, cross-task transfer, partner transfer, and counterfactual prediction are stronger evidence than agreement on a symbol.
14. **English is a renderer, not the semantic center.** Other natural languages, signed forms, diagrams, equations, actions, or other modalities are equally valid target realizations.
15. **A universal ontology is not assumed.** The universal layer should be a framework for representing hypotheses, relationships, uncertainty, provenance, evidence, transforms, and claim ceilings—not an encyclopedia of human concepts.
16. **Grounding claims are scoped.** No finite evaluator proves a uniquely correct ontology or universal meaning; certificates bind the exact worlds, interaction surfaces, strategies, controls, and threats survived.
17. **Identifiability precedes semantic promotion.** If rival mappings are indistinguishable through all allowed learner-visible histories in scope, the system must not force a semantic answer.
18. **Identifiability is not learner credit.** If evaluator/adapter/mediator infrastructure already performs the cross-system normalization, downstream success does not establish that the learner discovered the bridge.
19. **Human categories are controls, not universal law.** `name`, `word`, `syntax`, `belief`, `goal`, `question`, `warning`, `object`, and `agent` must be operationally earned for the tested system.
20. **Honest non-applicability is allowed.** A challenge whose prerequisites are absent may receive `NOT_APPLICABLE_TO_OBSERVED_COMMUNICATION_SYSTEM` rather than being mis-scored as a failure of communication itself.

## Current R1/R2 architecture challenge

The project now has three deliberately competing minimal semantic substrates:

- **TPH — Typed Probabilistic Hypergraph:** explicit structured relational hypotheses;
- **DCA — Denotational Constraint Algebra:** executable constraints/operators over compatible situations and trajectories;
- **PIS — Predictive-Intervention State:** action-conditioned predictions and signal-induced predictive changes.

No substrate is architecture canon. The richer candidates must empirically earn their additional commitments.

The R2 evaluator is designed to distinguish grounded convention from private shortcut code using causal message interventions where applicable, world-factor interventions, nuisance shifts, role reversal, cross-task transfer, partner swap, sensor shifts, counterfactual tests, ontology mismatch, conservation audits, and intentionally deceptive negative controls.

Pass 3 adds pressure that R1/R2 must also handle continuous, simultaneous, persistent, multimodal, sensor/channel-overlapping, collectively authored, and non-anthropomorphic communication without hidden adapters doing the semantic work.

A passing result may eventually receive `GROUNDED_WITHIN_TESTED_SCOPE`; there is intentionally no `UNIVERSALLY_GROUNDED` status.

## Repository map

- [`docs/PROJECT_THESIS.md`](docs/PROJECT_THESIS.md) — the refined concept and hypotheses.
- [`docs/CROSS_PASS_SEMANTIC_BOOTSTRAP_SYNTHESIS.md`](docs/CROSS_PASS_SEMANTIC_BOOTSTRAP_SYNTHESIS.md) — synthesis of the human verbal, human signed/nonverbal, and nonhuman evidence passes.
- [`docs/DESIGN_PRINCIPLES.md`](docs/DESIGN_PRINCIPLES.md) — architecture-level constraints.
- [`docs/SEMANTIC_SUBSTRATE.md`](docs/SEMANTIC_SUBSTRATE.md) — proposed semantic responsibilities before R1 competition.
- [`docs/R1_SUBSTRATE_COMPETITION.md`](docs/R1_SUBSTRATE_COMPETITION.md) — three genuinely competing minimal semantic substrates and the fair competition rule.
- [`docs/R2_ADVERSARIAL_EVALUATOR.md`](docs/R2_ADVERSARIAL_EVALUATOR.md) — adversarial semantic-grounding evaluator and scoped certificate.
- [`docs/R2_NEGATIVE_CONTROLS.md`](docs/R2_NEGATIVE_CONTROLS.md) — 25 shortcut systems plus positive oracles the harness must classify correctly.
- [`specs/R1R2_EVALUATION_CONTRACT_V1.yaml`](specs/R1R2_EVALUATION_CONTRACT_V1.yaml) — machine-readable R1/R2 evaluation contract.
- [`docs/BOOTSTRAP_PROTOCOL.md`](docs/BOOTSTRAP_PROTOCOL.md) — how communication could be established from zero shared symbols.
- [`docs/NONHUMAN_BOOTSTRAP_CONSTRAINTS.md`](docs/NONHUMAN_BOOTSTRAP_CONSTRAINTS.md) — cross-species constraints on channel, signalhood, sender/receiver, perception, and claim ceilings.
- [`docs/SEMANTIC_CONSERVATION.md`](docs/SEMANTIC_CONSERVATION.md) — what it means to preserve meaning.
- [`docs/EXPERIMENTAL_PROGRAM.md`](docs/EXPERIMENTAL_PROGRAM.md) — staged falsification program.
- [`docs/FIRST_100_CHALLENGES.md`](docs/FIRST_100_CHALLENGES.md) — 100 semantic challenges, not 100 presumed universal words.
- [`docs/NONHUMAN_FIRST100_REVIEW.md`](docs/NONHUMAN_FIRST100_REVIEW.md) — Pass 3 cross-species pressure test of the first 100.
- [`docs/CONTROL_SUITE.md`](docs/CONTROL_SUITE.md) — Earth-language, synthetic, nonlinguistic, asymmetric, and negative controls.
- [`docs/NONHUMAN_CONTROL_OVERLAYS.md`](docs/NONHUMAN_CONTROL_OVERLAYS.md) — Pass 3 controls for nonhuman-inspired channels and false-success modes.
- [`docs/INTERSTELLAR_DEPLOYMENT.md`](docs/INTERSTELLAR_DEPLOYMENT.md) — probe, broadcast, and hybrid architectures.
- [`docs/FAILURE_MODES.md`](docs/FAILURE_MODES.md) — ways the project can fool itself.
- [`docs/RESEARCH_LANDSCAPE.md`](docs/RESEARCH_LANDSCAPE.md) — relationship to prior research.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — ordered research phases and gates.
- [`research/CLAIMS_AND_EVIDENCE.md`](research/CLAIMS_AND_EVIDENCE.md) — main evidence-status ledger.
- [`research/NONHUMAN_CLAIMS.md`](research/NONHUMAN_CLAIMS.md) — Pass 3 cross-species claims supplement and claim ceilings.
- [`research/HUMAN_VERBAL_LANGUAGE.md`](research/HUMAN_VERBAL_LANGUAGE.md) — Pass 1 human spoken/verbal evidence review.
- [`research/HUMAN_NONVERBAL_AND_SIGNED.md`](research/HUMAN_NONVERBAL_AND_SIGNED.md) — Pass 2 signed-language and human nonverbal evidence review.
- [`research/NONHUMAN_COMMUNICATION.md`](research/NONHUMAN_COMMUNICATION.md) — Pass 3 nonhuman vocal/non-vocal evidence matrix.
- [`research/REFERENCES.md`](research/REFERENCES.md) — base literature and source notes.
- [`research/NONHUMAN_COMMUNICATION_REFERENCES.md`](research/NONHUMAN_COMMUNICATION_REFERENCES.md) — Pass 3 source supplement.

## The key experimental standard

A semantic mapping is not counted as established merely because the receiver performs correctly once.

A candidate distinction should survive, where applicable:

1. communication ablation;
2. direct signal intervention/playback;
3. world-factor intervention or other discriminating environmental variation;
4. nuisance transformations;
5. novel instances;
6. novel contexts;
7. role reversal where the observed system supports it;
8. recombination/systematic reuse;
9. transfer to a task or ecological context with different downstream demands;
10. acquisition/use by an independently initialized partner or population member where appropriate;
11. changed perceptual presentation;
12. counterfactual or predictive tests where appropriate;
13. ontology-mismatch/non-equivalence traps;
14. independent evaluator reconstruction;
15. provenance and semantic-conservation audit;
16. automated search for simpler shortcut explanations;
17. mediation-trust audit showing the bridge was not precomputed by privileged infrastructure;
18. claim-ceiling audit showing the evidence rung actually supports the wording used.

The system must also be rewarded for correctly saying that two conceptual structures are only partially overlapping, non-equivalent in the tested representation, empirically underdetermined, or not applicable to the observed communication system.

## Interstellar motivation

Historical interstellar messages such as the Pioneer plaques, Arecibo transmission, Voyager Golden Record, and the Lincos project attempt to construct content that a radically unfamiliar recipient might decode. UNVTRSLR asks a different question:

> **What if the transmitted artifact is not primarily the message, but the machinery for constructing a shared semantics?**

For an embodied probe, that machinery could interact locally with a recipient and a shared environment. For a broadcast, it could use a progressively staged curriculum. The project no longer treats literal self-description as the first zero-semantics move; the stronger working hypothesis is:

`self-demonstrating -> convention-forming -> recursively self-describing`

A hybrid architecture could use both local interaction and predesigned structure.

## Status

`PASS_1_2_3_RESEARCH_INTEGRATED / R1_R2_DESIGN_BASELINED / IMPLEMENTATION_NOT_STARTED / NO_SEMANTIC_QUALIFICATION`

The repository currently defines a research program and an adversarial qualification design, not a proven universal language, universal ontology, animal translator, or extraterrestrial communication solution. The strongest claims here are intentionally written so they can fail.
