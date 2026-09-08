# Research Roadmap

## Status

`R1_R2_DESIGN_BASELINED / IMPLEMENTATION_NOT_STARTED / NOT_IMPLEMENTATION_READY`

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

Current status: `DESIGN_BASELINED`.

Pass meaning: a reviewer can distinguish established prior work, current project hypothesis, speculation, and untested assumption.

## R1 — Minimal semantic substrate competition

### Objective

Define and compare the smallest formal representations capable of supporting the first experiments without silently privileging one human-readable ontology.

### Frozen R1 design rivals

1. **TPH — Typed Probabilistic Hypergraph**: explicit structured relational hypotheses.
2. **DCA — Denotational Constraint Algebra**: executable constraints/operators over compatible situations and trajectories.
3. **PIS — Predictive-Intervention State**: action-conditioned predictions and signal-induced predictive changes.

See [`R1_SUBSTRATE_COMPETITION.md`](R1_SUBSTRATE_COMPETITION.md).

### Required comparison properties

- same control tasks;
- same evaluator;
- no hidden English ontology;
- uncertainty/provenance support;
- semantic-conservation support;
- intervention/prediction support;
- cross-task and partner transfer;
- complexity accounting including adapter complexity;
- multiple seeds and independently generated worlds.

### Gate sequence

`R1_COMPETITION_SPECIFIED` — design complete, common contract and rivals frozen.

`R1_SUBSTRATE_EMPIRICALLY_QUALIFIED` — future status requiring R2-qualified runs.

`R1_SUBSTRATE_SELECTED` — optional later status; a single winner is not required. Pareto-nondominated rivals may continue.

Current status: `R1_COMPETITION_SPECIFIED / NOT_IMPLEMENTED`.

No substrate becomes architecture canon unless it earns complexity over a simpler rival.

## R2 — Trustworthy adversarial experiment harness

### Objective

Build the evaluator before claiming semantic learning and make it capable of rejecting high-performing shortcut systems.

### Design artifacts

- [`R2_ADVERSARIAL_EVALUATOR.md`](R2_ADVERSARIAL_EVALUATOR.md);
- [`R2_NEGATIVE_CONTROLS.md`](R2_NEGATIVE_CONTROLS.md);
- [`../specs/R1R2_EVALUATION_CONTRACT_V1.yaml`](../specs/R1R2_EVALUATION_CONTRACT_V1.yaml);
- [`../research/R1R2_RESEARCH_NOTES.md`](../research/R1R2_RESEARCH_NOTES.md).

### Required capabilities

- deterministic world generation/replay;
- evaluator-only hidden truth zone;
- independently randomized sensor renderers;
- learner/evaluator separation;
- configuration and seed binding;
- independent metric recomputation;
- sensory asymmetry;
- pluggable and unknown channels;
- no-communication controls;
- label/latent leak controls;
- private-code controls;
- causal message interventions;
- world-factor interventions;
- role reversal;
- cross-task transfer;
- partner swap/third-party acquisition;
- ontology-mismatch/non-equivalence tests;
- interaction logs;
- conservation/provenance evaluation;
- automated shortcut search.

### Core methodological rule

Task success is not a semantic certificate. An arbitrary signal convention is not a failure merely because its symbols are opaque. The evaluator targets hidden common ground and task-bound shortcuts: episode IDs, shared latent state, action-plan codes, memorization, reward side channels, co-training artifacts, and other explanations that fail grounded transfer.

### Harness gate

`HARNESS_TRUSTWORTHY`

The harness must reject all preregistered negative controls on the dimensions they violate and pass positive oracles before any R1 candidate hidden evaluation.

Thresholds are calibrated using only chance/null controls, positive oracles, negative controls, and harness-only pilot worlds, then frozen before candidate hidden results are inspected.

Current status: `R2_EVALUATOR_SPECIFIED / HARNESS_NOT_BUILT`.

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

The system must recover known mappings, preserve uncertainty, and correctly identify at least some non-equivalences under the frozen R2 evaluator.

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
- shared-latent shortcut;
- action-plan code;
- episode-ID code.

### Gate

Task success must survive R2 semantic probes, causal interventions, and cross-task/partner transfer.

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

Some research can proceed in parallel:

- literature review;
- synthetic-world generator design;
- synthetic-language generator design;
- nonlinguistic channel taxonomy;
- semantic conservation metrics;
- physical-layer/bootstrap research;
- safety/governance research.

Experimental claims remain ordered by qualification gates.

## Near-term next steps after R1/R2 design

1. Implement the R2 deterministic world/evaluator skeleton before implementing a sophisticated learner.
2. Implement P00-P03 positive controls and N00-N24 negative controls.
3. Freeze the control acceptance matrix and verify `HARNESS_TRUSTWORTHY` on intentionally broken systems.
4. Convert a bounded subset of the first 100 challenge families into machine-readable scenario specifications.
5. Implement the common substrate adapter contract.
6. Implement the smallest credible TPH, DCA, and PIS candidates under matched budgets.
7. Calibrate and freeze the first candidate-independent qualification profile.
8. Run R1 candidates only after the hidden holdout generation rule is frozen.
9. Build one synthetic language with deliberately non-English semantics for R3.
10. Build one continuous nonlinguistic channel for R5-compatible early stress testing.
11. Preserve every run with code/config/world/evaluator digests and immutable metric traces.
12. Treat discovery of any new shortcut as an evaluator-version event requiring a new negative control and requalification.
