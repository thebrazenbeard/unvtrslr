# Semantic Routing and Segmentation

Status: RESEARCH DESIGN / R3 INPUT / REPRESENTATION-NEUTRAL

## Purpose

Earlier VSNS/Semantic Atlas work used vocabulary such as entry node, propagation path, destination node, semantic routing, and salience. Those terms were useful inside that project, but UNVTRSLR must not inherit the graph metaphor or the project-specific node taxonomy as if it were universal.

The transferable result is narrower:

> **Before a signal can be translated, the system may need to infer where its boundaries are, which interpretation families are relevant, which context variables matter, and which competing semantic hypotheses survive. Those choices must remain testable and provenance-bearing.**

This document specifies those responsibilities without choosing TPH, DCA, PIS, or another R1 substrate.

## Segmentation is not semantics

A `segmentation_hypothesis` proposes which part of the observation stream should be treated as a candidate unit or coordinated structure.

A segment can be:

- temporally bounded;
- spatially bounded;
- continuous;
- recurring;
- multimodal;
- overlapping with another segment;
- hierarchical;
- distributed over time;
- partly defined by absence or timing;
- an environmental modification rather than an emitted symbol.

Segmentation may be supported by regularity without any known meaning.

Therefore:

`regular boundary != semantic unit`

and:

`semantic hypothesis != proof that the chosen segmentation is correct`

A later semantic failure may require reopening segmentation rather than merely remapping the same assumed tokens.

## Required segmentation record

A candidate implementation should be able to retain:

- observation span/reference;
- channel(s)/modality;
- proposed boundaries;
- segmentation mechanism;
- evidence for the boundaries;
- alternative segmentations;
- relation among overlapping/hierarchical candidates;
- confidence;
- provenance;
- downstream hypotheses currently depending on the segmentation;
- tests that would discriminate competing segmentations.

If the environment supplies packet boundaries, those are acquisition facts, not automatically semantic boundaries.

## Boundary leakage control

R1/R2/R3 evaluators should include cases where semantic units do not align with implementation conveniences such as:

- file boundaries;
- packets;
- frame boundaries;
- whitespace;
- words;
- speaker turns;
- fixed time windows;
- sensor polling cycles.

A candidate that relies on evaluator-provided segmentation without demonstrating that the boundary is available to the learner should fail the relevant no-hidden-common-ground control.

## Plural segmentation

When several parses remain plausible, preserve them.

Example abstract structure:

```text
S1: [a b] [c]
S2: [a] [b c]
S3: [a b c]
S4: cross-modal unit = [a + gesture_g] [b c]
```

The system should be able to attach semantic hypotheses to each candidate rather than force a single segmentation first.

A segmentation may become favored because it predicts:

- recurrence;
- receiver responses;
- world-state contrasts;
- compositional reuse;
- partner imitation;
- repair boundaries;
- counterfactual consequences.

## Segmentation and multimodality

A candidate unit may span several modalities.

Do not assume that speech-like channel A is the “message” and gesture-like channel B is metadata. Possible relationships include:

- redundant;
- complementary;
- disambiguating;
- conflicting;
- temporally interlocked;
- one channel indicating addressee while another carries referential structure;
- one channel altering pragmatic function of another.

R3 should include channel-conflict cases where each modality separately suggests a different interpretation.

## Semantic routing as hypothesis competition

“Routing” is used here only as an analytic shorthand:

> determining which semantic/pragmatic hypothesis families an observation currently supports and how evidence shifts among them.

It does **not** require literal nodes, a neural router, or a fixed graph.

Candidate route families may include:

- referential/entity;
- relational;
- event/process;
- quantitative;
- temporal;
- spatial/deictic;
- causal/predictive;
- communicative-function/pragmatic;
- epistemic/evidential;
- affective/motivational;
- social-role;
- convention/meta-communication;
- unknown/domain-specific.

These labels are bookkeeping families for research. They are not a claim that every agent decomposes meaning this way.

## One observation, multiple routes

A signal can simultaneously support several structures.

Example:

- refers to region X;
- predicts event E near X;
- directs receiver attention toward X;
- indicates sender uncertainty about E.

A one-label classifier would collapse four potentially independent invariants.

The substrate should permit these structures to coexist and should record whether they are:

- jointly supported;
- mutually exclusive;
- causally linked;
- alternatives;
- nested;
- unresolved.

## Route selection and provenance

Every material route decision should retain:

- observations supporting it;
- context facts used;
- model-derived features used;
- counterpart-supplied claims used;
- interventions that strengthened/weakened it;
- alternative routes discarded or retained;
- confidence/calibration;
- scope.

A renderer should be able to explain why a route was selected without treating hidden evaluator labels as learner evidence.

## Context is typed

A flat context vector is dangerous because it can mix causally meaningful context with nuisance features and answer-key leakage.

Suggested context families:

### Participant context

- candidate sender;
- candidate addressee;
- audience/overhearer;
- current role configuration.

### Spatial/deictic context

- positions;
- orientations;
- frames of reference;
- shared landmarks;
- perceptual access.

### Temporal context

- production time;
- reception time;
- ordering;
- latency;
- phase/periodicity;
- interaction-relative timing.

### Interaction-history context

- previous convention;
- prior reference;
- repair episode;
- recent success/failure;
- partner-specific pact;
- drift evidence.

### Modality/channel context

- channel availability;
- noise;
- cross-modal alignment;
- sensor transformation;
- emission direction.

### Environmental context

- world state;
- local affordances;
- relevant physical relationships;
- intervention history.

### Epistemic-hypothesis context

- inferred receiver uncertainty;
- inferred shared distinction;
- inferred expectation.

These remain hypotheses/provenance-bearing records where not directly observed.

## Context-sensitive rerouting

A robust system should be tested with four-way contrasts:

1. **same form, relevant context changed** — interpretation should change if the context variable is truly semantic/pragmatic;
2. **same form, nuisance context changed** — interpretation should remain invariant where appropriate;
3. **different form, relevant invariant preserved** — translation may remain equivalent if form is not material;
4. **different form, form-linked invariant changed** — equivalence should fail when form itself carries the demonstrated distinction.

This design directly prevents two opposite errors:

- ignoring context;
- treating every context change as meaning change.

## Speaker/addressee rerouting

Perspective-sensitive systems require explicit role tests.

Hold world state fixed while swapping sender and receiver positions/roles. A deictic or participant-relative mapping should update with the relevant frame. An absolute-coordinate shortcut should not receive credit for perspective-sensitive semantics.

## Timing and prosody as candidate structure

For human controls, timing/prosody can affect segmentation, emphasis, pragmatic function, information structure, or affective/social interpretation.

For arbitrary systems, generalize only the measurable principle:

> **Temporal and intensity structure may be semantically active and therefore must be experimentally varied rather than discarded as channel noise by default.**

Candidate features include:

- relative duration;
- onset/offset relation;
- repetition interval;
- amplitude/intensity modulation;
- frequency contour;
- phase relation;
- synchrony across modalities.

No human prosodic category is presumed.

## Interpretation versus salience

The strongest transferable VSNS correction is a separation, not a mandatory processing sequence.

A candidate system may compute interpretation and priority jointly. What it must not do is silently equate them.

Represent separately:

- semantic hypothesis confidence;
- estimated relevance/importance/urgency;
- action value;
- attentional priority;
- risk/cost;
- truth/evidence status.

High urgency cannot certify a semantic interpretation.

Example failure:

A loud signal reliably causes immediate avoidance. A learner labels its meaning `DANGER` solely because avoidance has high reward. When the same signal later means `STOP CURRENT ACTION` in both dangerous and harmless contexts, the task-policy shortcut is exposed.

## Post-interpretive salience rule

The predecessor phrase “meaning before salience” should be implemented as an audit rule:

> **Any salience/priority assignment used downstream must reference the semantic or perceptual evidence from which it was derived, and semantic confidence must be independently inspectable.**

This allows architectures with joint inference while preventing salience from becoming semantic ground truth.

## Truth, provenance, permission, and priority

Semantic routing must remain orthogonal to other governance/epistemic axes.

These are distinct:

- `X` was observed;
- sender claims `X`;
- learner predicts `X`;
- receiver should attend to `X`;
- receiver is requested to act on `X`;
- receiver is authorized/permitted to act on `X`;
- `X` is high priority;
- evaluator says `X` is true.

UNVTRSLR does not need a universal permission ontology, but when a task includes authorization/constraint semantics, the bridge must not treat request as permission or claim as truth.

## Ambiguity conservation

If several materially different route/segmentation combinations remain live, the target should preserve the uncertainty.

A mapping may render:

```text
H1: region X is the referent; function attention-directing, p=.48
H2: event E is the referent; function warning-like, p=.37
H3: signal is noncommunicative, p=.15
```

The renderer may choose one only under a declared decision policy, and the conservation ledger must record `AMBIGUITY_COLLAPSED` unless the alternatives are irrelevant to the declared scope.

## Reopening earlier layers

Later evidence can invalidate earlier processing assumptions.

Examples:

- pragmatic repair reveals that segmentation was wrong;
- role reversal reveals that a referent was encoded from sender-relative perspective;
- partner swap reveals a route depended on private history;
- multimodal conflict reveals that the “secondary” channel carried the discriminating information;
- counterfactual test reveals that a causal route was merely temporal association.

Therefore the architecture must permit backward revision. The planes are audit boundaries, not an irreversible waterfall.

## Candidate route tests

### Polysemy/context test

In human-language controls, use a form with multiple plausible interpretations and manipulate context independently. Test whether the learner tracks the relevant distinction rather than a dominant dictionary gloss.

### Segmentation ambiguity test

Present identical continuous observations with later interactions that discriminate two boundary hypotheses. Credit systems that revise segmentation without erasing prior evidence.

### Prosodic/timing contrast test

Hold nominal symbol identity fixed while changing a temporal/intensity feature shown to affect receiver behavior. Then create a nuisance timing change that should not matter.

### Speaker-role test

Swap sender/addressee or coordinate frames. Distinguish participant-relative interpretation from memorized absolute mappings.

### Cross-modal conflict test

Train channels as mutually consistent, then create a case where they disagree. Require the system to expose conflict rather than average them into a false single interpretation.

### Salience decoupling test

Make two interpretations equally likely but attach different action costs; then reverse costs while holding semantic evidence constant. Semantic confidence should not follow reward salience.

## Shortcut explanations to retain

For every routing result, search for:

- episode ID memorization;
- speaker ID memorization;
- lexical prior dominance;
- fixed tokenization;
- reward/action policy substitution;
- hidden evaluator labels;
- channel-specific shortcut;
- absolute-coordinate substitution for deixis;
- recency/frequency masquerading as semantics;
- embedding similarity treated as ground truth.

## R1 neutrality

TPH may represent route competition as weighted typed edges/hyperedges.

DCA may represent it as competing constraint sets over situations/trajectories.

PIS may represent it as distinct predictive/interventional state partitions.

None receives credit for matching the metaphors in this document. They receive credit only for performing the required distinctions and tests.

## Research consequence

The Semantic Atlas/VSNS history contributes a useful experimental stance to UNVTRSLR:

- do not assume the unit;
- do not assume the route;
- do not let urgency define meaning;
- vary one suspected distinction at a time;
- preserve alternatives;
- make later evidence capable of reopening earlier interpretation choices.

That is the portable content. The old node names and Vera-specific salience architecture are not.
