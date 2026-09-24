# Pragmatics and Communicative Function

Status: RESEARCH DESIGN / R3 INPUT / NOT A UNIVERSAL PRAGMATICS ONTOLOGY

## Purpose

UNVTRSLR already distinguishes signalhood, grounding, semantic hypotheses, context, convention, and rendering. This document adds a deliberately cautious interactional layer for a question that denotation alone cannot answer:

> **What is this candidate signal doing in this interaction, to whom, under what conditions, and what evidence supports that interpretation?**

This layer is not a catalog of human speech acts. It represents competing hypotheses about interactional function without presuming words, sentences, human intentions, shared mental architecture, cooperation, or even that the observed behavior is communicative.

The layer is downstream of acquisition and segmentation, overlaps with signalhood and grounding, and feeds convention, experimental selection, and rendering. Its objects are hypotheses, not privileged truths.

## Core separation

A candidate communicative event may carry several distinct structures:

- what environmental or internal distinction it appears related to;
- what relation or prediction it conveys;
- whether it is directed at anyone;
- what response it appears designed or selected to elicit;
- what the sender may assume about the receiver;
- whether the signal is cooperative, strategic, deceptive, ritualized, exploratory, or unknown;
- whether absence, timing, modality, or audience changes the interpretation.

None of those should be collapsed into a single `meaning` label when the evidence permits them to diverge.

For example, two signals may have the same referential target but different interactional consequences; two different forms may serve the same tested communicative function; one signal may simultaneously identify a referent and request attention; a behavior may predict the sender’s next action without having been intentionally produced to communicate it.

## Relationship to signalhood

Communicative function does not presuppose signalhood.

Every candidate function must carry a live alternative such as:

`H0: behavior is noncommunicative / incidental / mechanically coupled`

until the signalhood evidence is strong enough to lower that alternative.

Evidence that can strengthen a communicative-function hypothesis includes, where applicable:

- audience-contingent production;
- response-contingent repetition or modification;
- role-sensitive production;
- recipient behavior changing after direct signal intervention;
- repair after a demonstrable mismatch;
- selective withholding under conditions where production otherwise occurs;
- transfer of the signal to novel instances;
- sender/receiver role reversal;
- partner acquisition;
- counterfactual predictions that distinguish the proposed function from a simpler reactive policy.

No single item is sufficient in every system.

## Required hypothesis objects

A candidate implementation should be able to represent the following objects regardless of whether they are encoded as nodes, constraints, predictive state, distributions, or another substrate.

### `communicative_function_hypothesis`

A hypothesis about the interactional role of a candidate signal.

Suggested fields:

- hypothesis identity;
- candidate signal/segment reference;
- hypothesized function structure;
- triggering context;
- hypothesized target/addressee;
- hypothesized expected receiver change;
- hypothesized sender-side consequence, if any;
- evidence supporting and contradicting;
- alternative function hypotheses;
- noncommunicative null hypothesis;
- confidence/calibration;
- provenance;
- scope;
- last validation.

The function structure should not require an English verb such as `REQUEST` or `WARN`. A neutral representation may instead encode something like:

`production of S under condition C predicts an attempt to increase probability that receiver R attends to region X before event E`.

A renderer may later gloss that as warning-like or attention-directing if the evidence warrants it.

### `addressee_hypothesis`

A hypothesis about the intended or functionally targeted recipient of the signal.

Fields should allow:

- no addressee;
- one or more candidate addressees;
- broadcast/audience-wide target;
- uncertain target;
- apparent target distinct from actual responder;
- evidence from orientation, timing, channel selection, interaction history, or recipient-specific modulation.

Do not infer addressee merely from who happened to observe the signal.

### `audience_hypothesis`

A representation of who may be monitoring the interaction and whether their presence changes production or interpretation.

This matters because:

- a signal may target one agent but be available to others;
- sender behavior can change in the presence of observers;
- an overhearer may learn a convention without being the intended recipient;
- deception may be aimed at one audience while cooperation is aimed at another.

### `ostension_or_attention_hypothesis`

A hypothesis that a behavior is functioning to make some signal, object, relation, event, or interaction itself salient to another agent.

This must remain separate from semantic salience inside the learner. A sender’s apparent attention-directing act is an inferred communicative function; the receiver’s internal priority allocation is a different variable.

### `epistemic_state_hypothesis`

A bounded hypothesis about what another agent may know, expect, discriminate, attend to, or remain uncertain about.

Required discipline:

- infer from observable behavior and interaction history;
- preserve alternatives;
- distinguish `COUNTERPART_SIGNALLED` from `MODEL_INFERRED`;
- do not rewrite an epistemic hypothesis as evaluator truth;
- permit asymmetric models: A’s model of B may differ from B’s demonstrable state.

This object is useful for teaching, repair, deception, audience design, and convention maintenance without presuming human-like theory of mind.

### `expected_response_hypothesis`

A hypothesis about what receiver-side change would count as the signal functioning successfully.

The response need not be a motor action. It might be:

- attention shift;
- prediction update;
- selection among alternatives;
- delayed action;
- production of another signal;
- withholding an action;
- repair/confirmation;
- formation or revision of a convention.

Task reward is not automatically the expected semantic response.

### `repair_state`

A representation of an interactional mismatch and the attempts to resolve it.

Suggested fields:

- trouble source hypothesis;
- who detected the mismatch;
- evidence of mismatch;
- repair initiation signal;
- repair candidate;
- whether the repair changed form, context, segmentation, referent, function, or modality;
- receiver response;
- resolution status;
- remaining alternatives.

A canned repeat-after-failure policy must be representable without being mislabeled as semantic repair.

### `strategic_or_deceptive_hypothesis`

A hypothesis that sender incentives or behavior make literal/referential interpretation insufficient.

Possible structures include:

- selective disclosure;
- withholding;
- exaggeration;
- false signaling;
- audience-specific signaling;
- strategic ambiguity;
- truthful signal used to induce a misleading inference.

The system should not require a moralized label such as `lie`; it should represent the observable mismatch among sender evidence, signal content/function, receiver inference, and outcome.

### `interaction_history_reference`

A reference to prior interactions relevant to current interpretation.

History may include:

- prior conventions;
- recent successful/failed references;
- repair episodes;
- partner-specific terminology or signal patterns;
- known drift;
- role changes;
- prior deception/reliability evidence.

Interaction history must be explicit and bounded. Hidden recurrent-model state should not be the only place partner-specific semantic history exists if the evaluator is expected to audit it.

## Human-derived function families

The following are **experimental families**, not universal primitives. They are useful because human communication provides rich controls and counterexamples.

### Assertion-like

Operational sketch:

A signal appears to make a world-state or relation available for receiver uptake without primarily attempting to select a receiver action.

Evidence may include:

- receiver predictions update;
- signal varies with world state while receiver action affordances remain fixed;
- the same content transfers across tasks with different optimal actions.

Failure mode: a task-action code masquerading as assertion.

### Request-like

Operational sketch:

A signal appears selected to increase the probability of a receiver action or state transition beneficial/relevant to the sender or joint interaction.

Evidence may include:

- form/function changes when requested action changes while referent stays fixed;
- receiver can accept, reject, defer, or repair;
- role reversal works.

Failure mode: receiver learned a fixed action lookup from signal token.

### Warning-like

Operational sketch:

A signal appears to communicate a predicted adverse or high-cost condition in a way that enables receiver adaptation.

Evidence may include:

- receiver generalizes to novel hazards;
- signal maps to the hazard distinction rather than one memorized avoidance action;
- altered timing changes usefulness but not underlying referent.

Failure mode: alarm token = flee action, with no reusable hazard semantics.

### Query-like

Operational sketch:

A signal appears designed to reduce sender uncertainty by eliciting discriminating information from the receiver.

Evidence may include:

- next action depends on receiver reply;
- query choice tracks which hypothesis distinction is unresolved;
- useless/redundant replies produce repair or another query.

Failure mode: a learned two-turn task script.

### Correction-like

Operational sketch:

A signal appears to mark a prior interpretation, claim, convention, or action as mismatched and propose or elicit a replacement.

Evidence may include:

- targeted response to a specific prior error;
- corrected behavior persists on a novel recurrence;
- irrelevant previous turns do not trigger the same correction.

### Acknowledgment-like

Operational sketch:

A signal appears to provide evidence that a prior contribution has been received or understood sufficiently for current purposes.

Evidence may include:

- omission triggers repetition/repair;
- acknowledgment form depends on degree/type of understanding;
- incorrect acknowledgments can be exposed by subsequent tests.

Failure mode: automatic heartbeat/turn token.

### Rejection-like

Operational sketch:

A signal appears to decline a proposed mapping, action, interpretation, or convention.

Evidence should distinguish rejection from channel failure or nonresponse.

### Attention-directing-like

Operational sketch:

A signal appears designed to align receiver observation/attention with a region, entity, event, relation, or channel.

Deictic human controls are useful, but unknown systems may use movement, environmental modification, timing, vibration, emission direction, or other modalities.

### Teaching/demonstration-like

Operational sketch:

A signal/action sequence appears selected to modify the partner’s future mapping or predictive ability rather than merely solve the immediate episode.

Evidence may include faster partner acquisition, explicit contrast demonstrations, or behavior targeted to the learner’s current uncertainty.

### Repair-like

Operational sketch:

A signal/action responds to evidence of misunderstanding or transmission failure in a way that discriminates the trouble source and changes the interaction to restore coordination/understanding.

Repair-like behavior is stronger evidence when it is specific, novel, role-reversible, and successful under unseen error types.

## Literal/denotational content versus interactional function

The architecture must permit these cases:

1. same referent, different function;
2. same function, different referent;
3. same apparent proposition, different addressee;
4. same proposition, different epistemic/evidential stance;
5. same proposition, cooperative versus deceptive use;
6. same function achieved by radically different modality/form;
7. no stable proposition-like content, but stable interactional function;
8. stable referential content with no evidence of deliberate communication.

A renderer should not silently convert one into another.

## Indirect communication and inference

Human pragmatics demonstrates that conventional/literal form can underdetermine communicated meaning. UNVTRSLR should therefore permit an `inferred_communicative_content` layer, but with strict provenance.

Each inferred pragmatic claim should record:

- source signal and literal/grounded structures if any;
- context dependencies;
- interaction history used;
- counterpart-state hypotheses used;
- inference rule/model;
- live alternatives;
- confidence;
- counterfactual test that could distinguish the inference.

The renderer must mark inferred content as `INFERRED` rather than `PRESERVED` unless the source system itself has established the inferred structure as conventional content.

## Presupposition-like background dependence

Some communications depend on assumptions treated as already shared or available.

Represent this neutrally as:

`background_dependency_hypothesis`

with:

- required background proposition/distinction;
- evidence that sender relies on it;
- evidence receiver possesses or can reconstruct it;
- accommodation behavior, if any;
- mismatch/repair result;
- whether the background assumption is actually true, unknown, or evaluator-only.

This prevents the translator from treating assumed background as asserted content.

## Silence, withholding, timing, and omission

Absence can become a candidate signal only when the system has evidence for an expected event whose nonoccurrence is contingent and behaviorally relevant.

Minimum evidence bundle for a strong absence/withholding hypothesis:

1. a baseline expectation that event/signal `S` would occur under matched conditions;
2. nonoccurrence covaries with a candidate world, audience, or interaction state;
3. receiver behavior changes contingent on nonoccurrence;
4. random loss, latency, sensor failure, inactivity, and physical inability are tested as alternatives;
5. direct intervention on availability/withholding changes the predicted outcome.

Silence without an established expectation remains `UNRESOLVED`, not automatically meaningful.

## Cooperative, strategic, deceptive, and adversarial senders

The bootstrap protocol must not assume a benevolent teacher.

Candidate sender models may include:

- cooperative/aligned;
- partially aligned;
- indifferent;
- competitive;
- strategically informative;
- strategically ambiguous;
- selectively deceptive;
- unknown/nonstationary.

These are hypotheses over observed incentive/behavior structure, not personality labels.

A communication bridge should retain **reliability by scope**. One sender may be reliable about spatial vectors and unreliable about resource quality. One signal family may be honest under one audience and strategic under another.

## Audience and overhearer effects

A robust translator should distinguish:

- intended addressee;
- actual recipient;
- incidental observer;
- eavesdropper;
- broadcast audience;
- evaluator observer.

Tests should vary audience presence while holding world state fixed. If production changes, audience is a candidate causal context variable.

An overhearer’s ability to infer a convention does not retroactively make them the intended addressee.

## Perspective and deixis

Reference may depend on an indexical ground such as:

- producer position;
- receiver position;
- shared landmark;
- orientation;
- time of production/reception;
- current focus/attention;
- socially or procedurally defined frame.

Do not reduce deictic meaning to absolute coordinates unless tests show the source system itself does so.

A role-reversal test should change perspective while preserving the target relation. A system that memorizes absolute locations should fail when the deictic ground moves.

## Pragmatic uncertainty

Pragmatic uncertainty should remain separable from referential uncertainty.

Example:

- referent = object X, p=.96;
- candidate function = request receiver move X, p=.44;
- alternative = warn receiver about X, p=.39;
- alternative = direct attention to X, p=.17.

A fluent renderer must not convert this state into an unqualified imperative.

## Minimal adversarial pairs

### Same denotation / different function

World state and referent remain constant. Sender emits one of two forms. One reliably precedes receiver selection; the other reliably precedes receiver avoidance. Then change the receiver’s available actions. A true function model should preserve the distinction beyond the original action mapping.

### Same signal / different addressee

Same form is emitted while orientation/channel targeting alternates between two agents. Only the targeted agent’s response matters. A system that binds meaning to whichever agent reacts fastest should fail.

### Same content / cooperative versus deceptive use

Signal has an established world mapping. Change sender incentive so that production becomes strategically unreliable while the vocabulary remains fixed. The translator should retain lexical/semantic convention while lowering reliability of the current claim.

### Explicit signal versus meaningful withholding

Establish an expectation of signal production under a condition. Then test deliberate withholding against random channel loss. The system should treat absence as meaningful only where the evidence distinguishes the processes.

### Repair versus reflex

Create two agents:

- one diagnoses which distinction the receiver misunderstood and produces targeted clarification;
- one repeats or changes form after any failure.

Both can improve average reward. Only the first should receive strong `repair_like` evidence.

## Representation invariants

Regardless of R1 substrate, pragmatic hypotheses should preserve:

- evidence/provenance;
- scope;
- alternatives;
- noncommunicative null hypothesis;
- addressee/audience uncertainty;
- context dependencies;
- interaction history links;
- predicted discriminating outcomes;
- calibration;
- distinction between observed response and inferred intention.

## What R3 may certify

A future R3 evaluator may eventually support a status like:

`PRAGMATICALLY_GROUNDED_WITHIN_TESTED_SCOPE`

only when the candidate demonstrates the required distinctions across adversarial function, context, repair, partner, role, and strategic tests.

It must **not** certify:

- human-like intention;
- consciousness;
- theory of mind as a metaphysical fact;
- universal speech-act categories;
- cooperative disposition;
- uniquely correct interpretation of all sender motives.

## Research consequence

Human pragmatics is valuable to UNVTRSLR because it provides difficult cases where surface content, shared reference, interaction history, participant perspective, and communicative function diverge. The correct use of that literature is adversarial: force the semantic bridge to preserve distinctions without assuming the human categories are the architecture of communication itself.
