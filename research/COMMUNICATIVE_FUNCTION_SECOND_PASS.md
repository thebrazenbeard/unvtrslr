# Communicative Function — Second Research / Challenge Pass

Status: `SECOND_PASS_RESEARCH_SYNTHESIS / EXTENSION_CANDIDATES_ONLY / R3_V1_UNCHANGED`

## Purpose

The first pragmatics cycle deliberately avoided hard-coding human speech-act categories. This second pass asks a narrower question:

> **What can UNVTRSLR responsibly mean by “communicative function” when the observed system may be nonhuman, nonlinguistic, strategic, multi-party, self-directed, or only partially communicative?**

This pass does not modify the frozen first-cycle R3 V1 contract. It identifies extension candidates and new falsifiers for a later version.

## Sources reviewed in this pass

### S01 — Scott-Phillips (2008), “Defining biological communication”

Journal of Evolutionary Biology. DOI: `10.1111/j.1420-9101.2007.01497.x`.

Relevant result: biological communication lacks one universally agreed definition. Scott-Phillips argues for an adaptation-based account in which both the signal and corresponding response must be adaptive, and distinguishes signal, cue, coercion, and response.

Important boundary for UNVTRSLR: this is an evolutionary definition. It is not directly applicable to arbitrary synthetic or extraterrestrial systems when evolutionary history is unavailable.

### S02 — Maynard Smith & Harper (2003), *Animal Signals*

Oxford University Press. DOI: `10.1093/oso/9780198526841.001.0001`.

Relevant result: signal reliability is central in evolutionary signaling theory. Signals can be deceptive, and receiver behavior depends on the incentive/reliability structure of the signaling system.

Important boundary: adaptation/history is part of the biological definition, not a species-neutral observable primitive.

### S03 — Seyfarth et al. / animal signaler–receiver review tradition

Annual Review of Psychology (2003), “Signalers and Receivers in Animal Communication.” DOI: `10.1146/annurev.psych.54.101601.145121`.

Relevant result: a signal can both influence receiver behavior and provide receiver-usable information; sender production mechanisms do not uniquely determine receiver-extracted content. The review also argues that nonhuman signaling need not involve human-style intention to inform.

Important boundary: lack of demonstrated human-like intention does not imply lack of communication.

### S04 — Owren, Rendall & Ryan (2010), “Redefining animal signaling: influence versus information in communication”

Biology & Philosophy 25:755–780. DOI: `10.1007/s10539-010-9224-4`.

Relevant result: the authors challenge information-transfer metaphors and propose influence as a more concrete organizing concept for animal signaling.

Important boundary: influence alone is not enough for UNVTRSLR semantic qualification because coercion, cues, task policy, and self-regulation can all alter behavior.

### S05 — Skyrms (2010), signaling-game information

“The flow of information in signaling games,” Philosophical Studies 147:155–165. DOI: `10.1007/s11098-009-9452-0`.

Relevant result: initially arbitrary signals can acquire informational content under learning/evolution in signaling games; content can be characterized without lexical resemblance.

Important boundary: game-theoretic informational content remains conditional on the game/environment structure. It is not sufficient evidence for pragmatic interpretation, common ground, or unique real-world ontology.

### S06 — Fried et al. (2022), “Pragmatics in Language Grounding: Phenomena, Tasks, and Modeling Approaches”

arXiv:2211.08371.

Relevant result: grounded pragmatics depends on task goals, environmental context, communicative affordances, convention, and shared state.

Important boundary: the survey is about human-language grounding. It motivates test families but not species-neutral pragmatic primitives.

### S07 — higher-order animal-communication network work

Recent higher-order-network work on animal communication emphasizes that signals may have multiple simultaneous receivers and that receivers may integrate multiple signallers.

Important boundary: a dyadic sender→receiver abstraction can be too narrow even before considering alien communication.

### S08 — Nunley (2026), “Self-Regulation through Communication in Evolved Neural Agents”

Recent arXiv preprint, not treated as peer-reviewed authority in this pass.

Relevant result: in one evolved-agent setup, some vocalizations functioned partly through self-hearing to sustain the caller’s own behavior rather than only through transfer to another agent.

Important boundary: this is a model-specific preprint. Its value here is as an adversarial construction showing that an externally observable “communication” channel can participate in sender self-regulation.

## Challenge 1 — “Communicative function” cannot simply mean receiver effect

A behavior may alter another system because it is:

- a deliberate/selected signal;
- a cue exploited by the receiver;
- coercive physical influence;
- incidental correlation;
- a task-policy command;
- a shared side-channel artifact;
- a self-regulatory act that another agent merely overhears.

Therefore this rule is rejected:

`receiver_behavior_changes_after_signal -> communicative_function_established`

Direct causal effect is useful evidence, but it must be typed by competing mechanism hypotheses.

### Extension candidate

Add an architecture-neutral `interaction_effect_hypothesis` below `communicative_function_hypothesis`.

Suggested fields:

- source event/behavior;
- affected locus/loci;
- measurable effect;
- causal-intervention evidence;
- timing;
- context dependence;
- alternative mechanisms;
- whether the effect is sufficient for any higher communication claim;
- provenance and scope.

A communicative-function claim may build on interaction effects, but interaction effect itself is a lower claim.

## Challenge 2 — Information and influence are independent axes

A signal can be highly informative but behaviorally irrelevant in the current task. A signal can strongly influence behavior while conveying little reusable world information. A signal can influence the sender itself. A receiver can extract information from a cue whose producer did not evolve/act to communicate it.

Therefore the R3 representation should preserve at least:

- statistical/informational association;
- causal influence;
- reusable semantic distinction;
- interactional function;
- reliability/strategic status;
- producer-side function;
- receiver-side extracted information.

These should not be compressed into a single `communication_strength` scalar.

### New falsifier

Construct two channels:

1. high mutual information, zero receiver causal dependence;
2. strong receiver causal dependence, zero cross-task semantic reuse.

A system that calls both “same communicative function” fails the distinction.

## Challenge 3 — Producer function and receiver interpretation can diverge

Animal-communication theory supplies a useful asymmetry:

- why/when a producer emits a signal;
- what a receiver extracts from it;
- what effect it has on the receiver;

need not be identical descriptions.

UNVTRSLR should therefore avoid a single unqualified “meaning” slot where possible.

### Extension candidate

Split function evidence into:

- `producer_function_hypothesis` — what production appears to accomplish for the producer/system;
- `receiver_use_hypothesis` — what distinction/effect the receiver appears to derive;
- `interaction_level_function_hypothesis` — what stable relation exists across the coupled interaction.

These may converge, partially overlap, or conflict.

## Challenge 4 — Self-directed or self-heard signaling breaks a strict other-agent requirement

A channel can be externally observable while also participating in the producer’s own control loop. If UNVTRSLR assumes every candidate communicative signal must target another agent, it can misclassify mixed self/external functions.

The 2026 evolved-agent preprint is not enough to establish a biological universal, but it is enough to motivate a synthetic adversarial case.

### Extension candidate

Permit candidate recipient sets:

- `SELF_ONLY`;
- `OTHER_ONLY`;
- `SELF_AND_OTHER`;
- `MULTIPLE_OTHERS`;
- `BROADCAST_UNKNOWN`;
- `NO_RECIPIENT_ESTABLISHED`.

These are operational recipient hypotheses, not metaphysical identities.

### New negative control candidate — `RN16_self_regulation_masquerading_as_message`

Construction:

- producer emits signal S;
- S causally affects producer through self-hearing;
- receiver can hear S but does not causally use it;
- producer behavior changes strongly after S;
- naive evaluator mistakes coordinated timing for sender→receiver communication.

Required failure:

- receiver causal-use test exposes no external communicative effect;
- system retains producer self-regulation separately from receiver communication.

## Challenge 5 — Dyadic sender/receiver modeling is too narrow

Signals may be broadcast, overheard, coalition-specific, group-coordinating, or produced in environments with multiple simultaneous receivers and multiple contributing signalers.

Existing first-cycle `audience_hypothesis` work anticipated this, but the second pass strengthens the requirement: recipient structure should not be represented as a single optional addressee field when the interaction is genuinely higher-order.

### Extension candidate

Represent a `recipient_structure_hypothesis` capable of:

- one-to-one;
- one-to-many;
- many-to-one;
- many-to-many;
- overhearer/eavesdropper;
- group-state dependence;
- uncertain membership;
- dynamic membership during interaction.

R3 V1 can remain dyadic-plus-audience for the first harness, but a future version should not treat that as architecture canon.

## Challenge 6 — Adaptation-based biological definitions are useful controls, not universal definitions

Scott-Phillips / Maynard Smith & Harper are powerful because they sharply distinguish signal from cue/coercion by evolutionary function. But an alien or artificial system may have:

- no reconstructable evolutionary history;
- deliberate design rather than natural selection;
- online learning;
- temporary conventions;
- emergent coordination inside one episode.

Therefore UNVTRSLR cannot define communication solely by evolutionary adaptation.

### Species-neutral operational fallback

For unknown systems, prefer evidence bundles over a single essence definition:

1. candidate event reproducibly affects another locus or shared interaction;
2. effect depends on event intervention rather than mere correlation;
3. production varies with interaction-relevant state;
4. receiver/system response is contingent and nontrivial;
5. effect survives novel instances or controlled transformation;
6. simpler cue/coercion/task-policy/self-regulation explanations are actively tested;
7. function claim is scoped and may remain `UNRESOLVED`.

This is an operational test bundle, not a claim that communication has been metaphysically defined.

## Challenge 7 — Reliability is a property of use, not lexical convention itself

Signaling theory emphasizes reliability because sender/receiver interests can diverge. This reinforces the first-cycle separation among:

- convention;
- current claim content;
- sender reliability;
- strategic/deceptive hypothesis.

A deceptive use of an established convention should not automatically destroy the convention.

### New test extension candidate

`P21 — reliability transfer under stable convention`

- establish convention K honestly;
- vary sender incentives and reliability by context;
- keep form and world ontology fixed;
- require model to preserve convention while learning context-specific reliability.

Failure modes:

- `deception_erases_semantics`;
- `convention_implies_truth`;
- global distrust after local deception.

## Challenge 8 — Informational content can emerge in arbitrary signaling games without solving translation

Skyrms-style signaling games show that arbitrary signals can acquire informational content under dynamics. That is directly useful against the assumption that meaningful signals must resemble their content.

But it also creates a warning for UNVTRSLR:

> A stable game-relative informational partition is not automatically a cross-task semantic bridge or pragmatic interpretation.

This reinforces R0.5/R2 claim ceilings and R3’s need to preserve lower operational success when higher labels fail.

## Second-pass disposition

### Supported/narrowed

- causal receiver effect is evidence, not communicative-function proof;
- information, influence, semantics, and pragmatic function are distinct axes;
- producer and receiver descriptions may diverge;
- communication need not require demonstrated human-style intention-to-inform;
- recipient structure may be multi-party and dynamic;
- reliability should remain separate from convention identity;
- arbitrary signal form is compatible with stable informational content;
- evolutionary signal definitions are valuable biological controls but not universal operational definitions.

### Newly rejected overclaims

- `COMMUNICATIVE_FUNCTION_EQUALS_RECEIVER_EFFECT` — rejected;
- `COMMUNICATION_REQUIRES_HUMAN_STYLE_INTENTION_TO_INFORM` — rejected as a universal requirement;
- `EVERY_COMMUNICATIVE_SIGNAL_IS_OTHER_DIRECTED` — rejected as an architecture assumption;
- `INFORMATION_CONTENT_EQUALS_PRAGMATIC_FUNCTION` — rejected;
- `DYADIC_SENDER_RECEIVER_IS_A_UNIVERSAL_INTERACTION_SHAPE` — rejected;
- `DECEPTION_INVALIDATES_THE_CONVENTION_IT_USES` — rejected.

## Candidate future changes — do not modify R3 V1 yet

For an R3 V2 or R3.1 design pass, consider:

1. `interaction_effect_hypothesis` below pragmatic function;
2. producer-function / receiver-use / interaction-level-function separation;
3. explicit recipient-structure hypothesis;
4. `RN16_self_regulation_masquerading_as_message`;
5. `P21_reliability_transfer_under_stable_convention`;
6. a synthetic cue-versus-signal-versus-coercion family where evolutionary history is evaluator-defined but withheld from the learner;
7. a many-to-many pragmatic positive oracle;
8. a certificate field stating which operational communication definition/evidence bundle the run actually tested.

## Research boundary

This pass adds adversarial pressure, not capability evidence. No source reviewed here demonstrates a species-neutral universal pragmatics layer, and no current UNVTRSLR implementation has tested these extensions.
