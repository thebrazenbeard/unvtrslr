# Research Roadmap

## Status

`RESEARCH_BOOTSTRAP / NOT_IMPLEMENTATION_READY`

The roadmap is intentionally gated. Later phases do not inherit qualification merely because earlier phases succeeded.

## R0 — Research corpus and assumptions ledger

### Objective

Establish the conceptual and evidentiary baseline.

### Deliverables

- project thesis;
- research landscape;
- references;
- claims/evidence ledger;
- explicit assumptions;
- failure-mode inventory;
- competing architecture list.

### Gate

`R0_RESEARCH_BASELINED`

Pass when a reviewer can distinguish:

- established prior work;
- current project hypothesis;
- speculation;
- untested assumption.

## R1 — Minimal semantic substrate competition

### Objective

Define and compare the smallest formal representations capable of supporting the first experiments.

### Candidate rivals

1. typed probabilistic graph;
2. relation-tuple substrate;
3. latent-cluster + provenance + intervention log;
4. event-sourced hypothesis store;
5. hybrid symbolic/probabilistic representation.

### Required tests

- same control tasks;
- same evaluator;
- no hidden English ontology;
- semantic conservation support;
- uncertainty/provenance support;
- complexity accounting.

### Gate

No substrate becomes architecture canon unless it earns complexity over a simpler rival.

## R2 — Trustworthy experiment harness

### Objective

Build the evaluator before claiming semantic learning.

### Required capabilities

- deterministic world generation/replay;
- learner/evaluator separation;
- configuration and seed binding;
- independent metric recomputation;
- sensory asymmetry;
- pluggable channels;
- no-communication controls;
- label-leak controls;
- private-code controls;
- interaction logs;
- conservation ledger evaluation.

### Gate

`HARNESS_TRUSTWORTHY`

The harness must fail intentionally broken semantic systems.

## R3 — Human-language and synthetic-language controls

### Objective

Prove that the protocol can recover known semantic relationships without direct dictionaries.

### Work

- multiple unrelated natural-language controls;
- at least one signed/spatial control;
- synthetic compositional language;
- synthetic context-dependent language;
- synthetic non-equivalent categories.

### Gate

The system must recover known mappings, preserve uncertainty, and correctly identify at least some non-equivalences.

## R4 — Zero-shared-vocabulary grounded communication

### Objective

Agents invent communication from scratch in a shared world.

### Work

- referential grounding;
- relation grounding;
- role reversal;
- compositional recombination;
- transfer to a new task.

### Adversaries

- private-code agent;
- memorizer;
- shared-latent shortcut.

### Gate

Task success must survive semantic probes and cross-task transfer.

## R5 — Unknown and nonlinguistic communication channels

### Objective

Remove message segmentation and linguistic assumptions.

### Work

- continuous signals;
- timing;
- motion;
- orientation;
- environmental modification;
- multimodal channels;
- no-communication worlds.

### Gate

The system must discover signalhood with controlled false positives and ground at least some continuous/nonlinguistic mappings.

## R6 — Context, asymmetry, and ontology mismatch

### Objective

Attack the assumption that both parties experience or categorize the world the same way.

### Work

- context-dependent signals;
- asymmetric sensors;
- different coordinate frames;
- different object segmentation;
- unavailable sensory dimensions;
- many-to-one/one-to-many mappings;
- semantic drift.

### Gate

The system must preserve partial mappings and return `NO_FAITHFUL_EQUIVALENT` when appropriate.

## R7 — Active semantic science

### Objective

Move from passive association to discriminating experiment design.

### Work

- competing semantic hypotheses;
- information-gain baseline;
- safe intervention policy;
- causal vs predictive distinction;
- counterfactual tests;
- repair and clarification.

### Gate

Active testing must improve hypothesis discrimination over passive baselines without self-confirming bias.

## R8 — Meta-communication and self-description

### Objective

Teach communication about communication itself.

### Work

- repeat/repair;
- uncertainty;
- questions/probes;
- convention revision;
- explaining mappings;
- self-describing protocol fragments.

### Gate

A receiver not pretrained on the protocol must recover enough of the protocol to participate in further bootstrap.

## R9 — Cross-architecture receiver qualification

### Objective

Eliminate success tied to one learner implementation.

### Work

- independently implemented sender/receiver systems;
- different model families;
- from-scratch agents;
- pretrained agents with contamination controls;
- cross-partner convention transfer.

### Gate

At least two materially different receiver architectures independently reconstruct equivalent semantic invariants from the same bootstrap curriculum.

## R10 — Interstellar broadcast simulation

### Objective

Simulate an uncoordinated receiver receiving a self-describing signal over an impaired channel.

### Work

- signal detection;
- framing inference;
- redundancy/error corruption;
- number/ratio/physics curriculum;
- semantic substrate teaching;
- reply protocol reconstruction.

### Gate

Receiver must recover meaning without access to human language, source code, hidden metadata, or shared framing configuration.

## R11 — Embodied probe simulation

### Objective

Evaluate the interactive translator-probe concept.

### Work

- unknown agent detection;
- safe signalhood experiments;
- grounded semantic negotiation;
- action/permission separation;
- long-lived convention memory;
- counterpart change/drift;
- multiple agents/groups.

### Gate

The probe must demonstrate useful semantic bridge construction while staying inside strict action-authority bounds.

## R12 — Human and animal-research interfaces

### Objective

Evaluate whether the architecture transfers beyond synthetic agents.

### Candidate work

- human zero-shared-language experiments;
- collaboration with linguists/sign-language researchers;
- animal-communication datasets with behavioral context;
- Project CETI-like multimodal data interfaces;
- archival Earth communication systems.

### Boundary

Do not claim animal translation from acoustic prediction alone.

Human/animal work requires appropriate ethical and domain expertise.

## R13 — Interstellar package candidate

### Objective

Only after prior gates: define a bounded candidate package for a broadcast, probe, or hybrid system.

### Required artifacts

- physical-layer assumptions;
- self-description curriculum;
- semantic protocol;
- human knowledge corpus;
- conservation/provenance rules;
- receiver tests;
- failure behavior;
- governance boundaries;
- versioning and longevity strategy.

### Gate

`INTERSTELLAR_PACKAGE_RESEARCH_CANDIDATE`

This status does not authorize transmission or deployment.

## Parallel workstreams

Some research can proceed in parallel once R0 exists:

- literature review;
- representation alternatives;
- synthetic-language generator design;
- nonlinguistic channel taxonomy;
- semantic conservation metrics;
- physical-layer/bootstrap research;
- safety/governance research.

But experimental claims remain ordered by the qualification gates above.

## Near-term next steps

1. Convert the first 100 challenge families into machine-readable evaluator specifications.
2. Define the smallest three rival semantic substrates.
3. Design the negative-control suite before the learner.
4. Select a minimal world simulator supporting sensor asymmetry and interventions.
5. Define exact signalhood-discovery metrics.
6. Build one synthetic language with deliberately non-English semantics.
7. Build one continuous nonlinguistic channel.
8. Preregister R2/R3 pass/fail criteria before model training.
9. Expand literature review around self-describing protocols, semiotics, active learning, and cross-modal grounding.
10. Preserve every promoted claim in the evidence ledger with exact experimental provenance.
