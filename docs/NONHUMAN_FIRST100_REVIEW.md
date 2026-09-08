# Nonhuman Review of the First 100 Semantic Challenges

Status: `PASS_3_FIRST100_REVIEW / CROSS_SPECIES_SCOPE`

This document pressure-tests `docs/FIRST_100_CHALLENGES.md` against the Pass 3 nonhuman communication evidence. It does **not** replace the 100-item inventory. It classifies hidden assumptions and identifies which challenges are plausible cross-system probes versus human-heavy stress tests.

## Core correction

The first 100 are evaluator challenges, not a universal developmental ladder, not 100 universal concepts, and not requirements that every communication system must satisfy.

Pass 3 adds a new allowed outcome:

`NOT_APPLICABLE_TO_OBSERVED_COMMUNICATION_SYSTEM`

Use it only when the challenge itself presupposes an unsupported ontology/function for the tested system. Do not use it to excuse an ordinary failure on a challenge whose prerequisites are actually present.

## Cross-species pressure by family

### Family A — recurrence, identity, discrimination

Generally useful, but several challenges assume stable object/event segmentation.

Cross-species evidence supports recurrent pattern discrimination and individual-specific signal relations, but identity can be encoded through emitter cues, copied addressee signals, learned labels, or persistent environmental traces.

Required audit:
- what constitutes a stable unit?
- is identity attached to an object, individual, trajectory, signal source, location, or distributed trace?
- does the evaluator supply the segmentation?

Challenges 3-7 should therefore be marked `SEGMENTATION_DEPENDENT` rather than treated as primitive.

### Family B — quantity and magnitude

Potentially broad but unitization is a hidden prerequisite. `one`, `many`, exact count, and ratio only make sense after a system has some stable aggregation scheme.

Honeybee-inspired evidence also warns that a physical magnitude such as distance may be represented through a species-specific perceptual metric.

Required audit:
- evaluator metric versus sender metric versus receiver metric;
- aggregation window;
- countable-unit assumption.

### Family C — similarity, category, feature

Useful as a bridge stress test, not evidence that all communicators possess human-like categories.

The evaluator must permit:
- continuous rather than categorical organization;
- overlapping partitions;
- relation-first representations;
- population-specific signal repertoires;
- categories induced by sensor ecology rather than evaluator labels.

### Family D — space and geometry

Strong candidate family for many embodied systems, but coordinate frames and perceptual metrics cannot be assumed shared.

Honeybee route communication makes challenge 38 especially important: success should be possible through a negotiated or learned transform between incompatible distance metrics rather than requiring common meters.

Left/right, front/back, or vertical relations should remain alternatives rather than mandatory universal axes.

### Family E — time, sequence, recurrence

Broadly useful but temporal grain can differ radically.

Persistent chemical trails and asynchronous collective signaling show that:
- producer and receiver need not be co-present;
- message start/end may not exist;
- overlapping traces can accumulate;
- relevant timescale may be much longer than one dyadic exchange.

Challenge 42's `same-time` and challenge 49's sequence representation therefore need tolerance for asynchronous/persistent systems.

### Family F — change, action, control

Materially anthropocentric if `agent` and `action` are preinstalled.

Use the weaker framing `locally attributable change/influence` unless the tested system independently supports agent/action decomposition.

Challenges 52, 57, 59, and 60 should be tagged `AGENCY_MODEL_DEPENDENT`.

### Family G — causality, prediction, counterfactuals

Prediction and intervention are valuable scientific probes, but not every system exposes controllable interventions or counterfactual signaling.

Allow:
- passive discriminating histories;
- exogenous natural variation;
- playback/replay manipulations;
- environmental perturbations;
- controlled interventions where ethically/ecologically appropriate.

Challenges 62, 65, and 69 are therefore high-value research stress tests, not universal prerequisites for communication.

### Family H — communication about communication

Passes 1-2 already moved repair earlier. Pass 3 reinforces the distinction between flexible intentional systems and systems with no evidence of meta-communication.

Great-ape persistence/elaboration supports some repair-like functions, but chemical trails, bee dances, or many vocal systems need not expose explicit `repeat`, `clarify`, or `I do not understand` functions.

Challenges 71-80 should be scored only when the observed system supplies evidence that such interaction management is possible. Absence is not automatically failure of communication.

### Family I — agency, knowledge, goal, social perspective

This is the most human-heavy family.

Challenges 81-90 remain extremely useful for testing a mediator that claims broad human or agentic competence, but they must not define the universal bootstrap kernel.

Required labels:
- `HUMAN_CONTROL_RELEVANT`;
- `AGENTIC_SYSTEM_RELEVANT`;
- or `NOT_APPLICABLE_TO_OBSERVED_COMMUNICATION_SYSTEM`.

Specific caution:
- `goal`, `belief`, `known`, `unknown`, `assertion`, `question`, and `warning` are evaluator interpretations until operationally grounded.

### Family J — composition, abstraction, non-equivalence

This family remains central, but `composition` must not mean concatenated symbolic syntax.

Cross-species evidence supports several possibilities:
- ordered vocal combinations;
- simultaneous multidimensional displays;
- continuous vector signals;
- spatially persistent traces;
- population-specific repertoires.

Qualification should therefore ask whether independently recoverable components/features combine predictably, not whether the system looks sentence-like.

Challenge 100 remains scope-bounded:

`NO_FAITHFUL_EQUIVALENT_FOUND_WITHIN_TESTED_SCOPE`

unless formal impossibility is established.

## New cross-species difficulty dimensions

Add these dimensions to challenge generation:

- discrete event -> persistent field;
- single producer -> collective authorship;
- co-present receiver -> delayed/asynchronous receiver;
- dedicated channel -> sensor/channel overlap;
- evaluator physical metric -> species-specific perceptual metric;
- fixed signal function -> context-dependent mixed function;
- individual learning -> socially transmitted convention;
- dyadic exchange -> population/network communication;
- observable intention -> no intentionality evidence;
- corpus association -> causal/playback receiver evidence;
- single modality -> multimodal redundancy/conflict;
- symbolic combination -> continuous/simultaneous composition.

## New false-success modes

1. A classifier predicts world context from a signal and the evaluator calls that `meaning` without receiver evidence.
2. Individual identity information is mislabeled as a proper name.
3. A nonrandom sequence is mislabeled as syntax/compositional semantics.
4. A rich acoustic model is mislabeled as translation.
5. Evaluator Euclidean variables are treated as the organism's internal semantic quantities.
6. A persistent collective trail is forcibly segmented into sender-message-receiver triples.
7. Audience-insensitive ecological behavior is mislabeled communication.
8. Human intentionality tests are required for systems that do not depend on flexible intentional production.
9. A socially transmitted repertoire is treated as species-wide innate semantics.
10. A human-readable ontology wins because the evaluator cannot score a nonhuman-like representation.

## Recommended evaluator metadata for every challenge

Add or derive:

- `ontology_dependencies[]`;
- `segmentation_dependencies[]`;
- `agentivity_dependencies[]`;
- `timescale_dependencies[]`;
- `channel_dependencies[]`;
- `modality_assumptions[]`;
- `receiver_evidence_required`;
- `claim_ceiling`;
- `not_applicable_conditions[]`;
- `cross_species_variant_available`;
- `anthropomorphic_label_risk`.

## Result

The first 100 survive Pass 3 as a **broad adversarial challenge inventory**, but not as a universal concept list or fixed curriculum.

The strongest cross-species kernel is earlier and thinner: detect repeatable structure, distinguish context/contingency, identify whether behavior affects a receiver or shared process, test competing relations when the surface permits, preserve uncertainty/provenance, and avoid claiming a semantic relation stronger than the evidence.
