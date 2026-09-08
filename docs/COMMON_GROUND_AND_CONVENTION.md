# Common Ground and Convention

Status: RESEARCH DESIGN / R3 INPUT / NOT A THEORY OF MIND CLAIM

## Purpose

UNVTRSLR needs a way to represent when two agents have established enough shared semantic structure to use a convention productively—without pretending the evaluator can inspect or prove perfectly symmetric beliefs.

Human communication research uses notions such as common ground, grounding, conceptual pacts, mutual belief, and convention. These are valuable sources of experimental structure. They should not be imported as metaphysical requirements for arbitrary intelligence.

This document therefore separates **observable interactional evidence**, **counterpart-state hypotheses**, and **evaluator-only truth**.

## Three constructs that must not collapse

### `interactionally_supported_common_ground`

A scoped record that a distinction, reference, convention, or procedure has enough mutual behavioral support to be treated as jointly usable for the present interaction.

It answers:

> What can the system responsibly rely on as jointly established **for this purpose, with these participants, under these tested conditions**?

Suggested fields:

- common-ground record ID;
- participants;
- semantic/conventional structure referenced;
- establishment evidence;
- confirmation evidence;
- repair history;
- tested contexts;
- tested roles;
- partner-transfer status;
- counterexamples;
- confidence/calibration;
- last-confirmed interaction;
- expiration/drift policy;
- provenance.

It is an operational evidence object, not a claim that the participants possess identical internal representations.

### `counterpart_epistemic_hypothesis`

A participant’s or learner’s uncertain model of what another agent may know, distinguish, expect, attend to, or misunderstand.

It answers:

> What do I currently predict about the other participant’s usable information state?

This object must remain explicitly inferential and may conflict with `interactionally_supported_common_ground`.

Example:

- convention X has repeatedly succeeded;
- learner A predicts B knows X with p=.82;
- evaluator hidden truth shows B was using an unrelated side channel;
- therefore prior interactional evidence was misleading and must be revised.

### `evaluator_mutual_state`

Ground truth available only in synthetic/controlled experiments about what each agent actually received, represented, or could discriminate.

It exists to score false-common-ground cases.

Learners must not receive this object directly unless the experiment explicitly makes it part of the observable world.

## Why this separation matters

Without it, a system can perform the following invalid promotion:

`both agents acted successfully -> both understood the same thing -> they share the same concept -> the concept is grounded`

Each arrow requires additional evidence.

UNVTRSLR should instead preserve the chain:

`observed coordination -> candidate shared convention -> tests of causality/reuse/repair/transfer -> scoped common-ground evidence`

with competing explanations retained.

## Establishment evidence

A convention becomes stronger when several independent evidence classes converge.

Candidate evidence includes:

- repeated successful use on novel instances;
- direct message intervention causing predicted receiver changes;
- contrastive failure when the convention is intentionally perturbed;
- explicit or behaviorally demonstrated acknowledgment;
- role reversal;
- targeted repair after mismatch;
- successful recombination with other established distinctions;
- transfer to a different task requiring the same semantic distinction but a different action;
- acquisition by an independently initialized partner;
- successful use after modality/presentation changes;
- counterfactual prediction;
- resistance to simpler shortcut explanations.

No fixed subset is universally required. The certificate should state which evidence the convention survived.

## Convention lifecycle

A convention is not a permanent dictionary entry.

### `CANDIDATE`

A recurring mapping or interactional regularity has been detected but lacks sufficient evidence for stable use.

### `ESTABLISHING`

Participants are converging; successful use exists, but alternatives remain materially plausible.

### `ESTABLISHED_WITHIN_SCOPE`

The mapping has survived the declared establishment tests for specified participants/context.

### `WEAKENED`

Counterevidence, errors, or drift reduce confidence without yet invalidating the convention.

### `DRIFTING`

The form, function, context bounds, or interpretation is changing over interaction history.

### `UNDER_REPAIR`

Participants have detected or behaved as if there is a mismatch and are renegotiating.

### `REPLACED`

A successor convention has superseded the prior mapping for some or all scope.

### `ABANDONED`

Participants no longer rely on the mapping, or evidence shows it was never semantically stable.

### `UNKNOWN_CURRENTNESS`

The convention was once established but has not been revalidated in conditions where drift is plausible.

Lifecycle state must be participant- and scope-qualified. A convention can be established for A↔B while unknown for A↔C.

## Partner-specific conceptual pacts

Human experiments show that conversational partners can establish persistent, partner-specific ways of conceptualizing/referencing an object.

UNVTRSLR should generalize the experimental lesson, not the lexical mechanism:

> Interaction history can create partner-specific semantic shortcuts or conventions that are real within a dyad yet fail to transfer.

Therefore every convention should record:

- participant set;
- whether it emerged through direct interaction;
- whether a new partner can infer/acquire it;
- whether it depends on shared history inaccessible to outsiders;
- whether a simpler, more general bridge exists.

A partner-specific pact is not failure. It becomes a failure only when the system incorrectly promotes it as a general semantic mapping.

## Asymmetric common ground

Participants need not possess symmetric evidence or representations.

Examples:

- A can produce a signal reliably; B can interpret it but cannot produce it.
- B understands a coarse distinction; A represents a finer one.
- A knows how a convention was established; B learned it indirectly.
- A believes a mapping is stable; B remains uncertain.

Represent asymmetry explicitly.

Possible record:

```text
convention: K
A_production: strong
A_interpretation: strong
B_production: unknown
B_interpretation: strong
A_model_of_B: strong
B_model_of_A: weak
role_reversal: not_tested
```

Do not force symmetric status for convenience.

## False common ground

A critical R3 failure class is **apparent shared understanding produced by different mechanisms**.

### Side-channel false common ground

A sender emits arbitrary message M. Receiver ignores M and acts from a leaked scene identifier. Coordination succeeds.

Required outcome:

- message intervention/ablation exposes no causal semantic role;
- common-ground claim is rejected or weakened.

### Partner-identity lookup

Receiver memorizes partner-specific output policies rather than learning the semantic mapping.

Required test:

- partner swap while preserving semantic task;
- independently initialized partner.

### Shared-task-policy illusion

Both agents independently infer the same optimal action from world state; the signal adds nothing.

Required test:

- communication ablation;
- hide complementary information so coordination actually requires message content.

### Overestimated background

Sender assumes receiver shares a reference/history that receiver lacks. Receiver guesses successfully on training distributions.

Required test:

- novel case where the missing background distinction matters;
- targeted repair should diagnose the mismatch.

### Semantic-alignment illusion

Agents use the same signal for different internal distinctions that happen to prescribe the same action in the current task.

Required test:

- change optimal action or introduce a world where the distinctions diverge.

## Common-ground scope

Every record should declare dimensions such as:

- participants;
- channel/modality;
- environment class;
- task family;
- temporal window;
- referential domain;
- pragmatic function;
- ontology assumptions;
- perceptual presentation;
- role configuration.

A convention that passes in one scope must not silently inherit validity in another.

## Confirmation and acknowledgment

Evidence of acknowledgment may strengthen interactional grounding, but a fixed acknowledgment token is vulnerable to shortcut behavior.

Strong confirmation tests include:

- receiver must demonstrate the distinction under a novel instance;
- acknowledgment can be challenged by a minimal pair;
- incorrect acknowledgment is followed by behavior exposing the mismatch;
- acknowledgment semantics survives role reversal.

A heartbeat token or turn-taking marker may coordinate the exchange without certifying understanding.

## Repair and renegotiation

When evidence indicates mismatch, the system should be able to identify what layer may have failed:

- acquisition/channel;
- segmentation;
- signalhood;
- referent;
- relation;
- context;
- communicative function;
- addressee;
- convention currentness;
- epistemic assumption.

Repair should update only the affected hypotheses when possible.

Example:

A known symbol still refers to the same object, but its interactional use has drifted from `attention-directing-like` to a more specific `hazard-alert-like` function. The referential mapping need not be discarded merely because the pragmatic convention changed.

## Convention drift

Drift is expected in adaptive systems.

Detect candidate drift when:

- the same form’s predictive consequences change over time;
- context bounds tighten or broaden;
- participant-specific use diverges;
- old mappings require increasing repair;
- a new form progressively replaces an old form;
- role reversal begins to fail despite receiver-side success.

Drift requires temporal evidence. One anomalous interaction should update uncertainty but not automatically rewrite the convention.

## Abandonment

A mapping should be abandoned when evidence supports that:

- prior success was caused by a shortcut;
- participants no longer use the distinction consistently;
- the semantic interpretation was materially wrong;
- a replacement convention has become established;
- current evidence is insufficient and retaining the convention would create unsafe overconfidence.

Abandonment preserves historical evidence; it does not delete the record of what once worked.

## Partner transfer

Partner transfer tests whether a convention is recoverable beyond the original dyad.

Levels of evidence:

1. **same partner, novel instance** — weakest transfer;
2. **role reversal within dyad**;
3. **new partner with access to prior public interaction history**;
4. **new partner without private dyadic state**;
5. **independently initialized partner acquires mapping through the same grounding process**.

Failure at a higher level does not invalidate dyadic semantics; it limits scope.

## Role reversal

Role reversal tests productive versus merely reactive competence.

A mapping is stronger when a previous receiver can:

- produce a signal based on a novel world state;
- guide the previous sender;
- repair misuse;
- preserve the same tested invariant under reversed perspective.

But role reversal is not mandatory for every asymmetric communication system. Some channels or organisms may physically support only one-way signaling. In those cases the certificate should record the asymmetry rather than force an impossible test.

## Independently initialized partner test

This is a particularly strong anti-private-code test.

The new partner must not inherit:

- hidden sender-specific lookup tables;
- shared random seeds encoding semantics;
- evaluator labels;
- private training embeddings;
- inaccessible interaction memory.

Success should come from observable grounding/teaching/convention evidence available in the declared protocol.

## Convention versus semantic identity

A stable convention can be arbitrary.

Two agents may agree that signal `K7` tracks a semantic distinction with no intrinsic resemblance between form and referent. That arbitrariness is not failure.

The evaluator should ask:

- Is the mapping stable?
- Is the distinction grounded?
- Does it generalize within scope?
- Is it causally used?
- Can alternatives/ambiguity be represented?
- Is provenance preserved?

It should not ask whether the signal “looks like” its meaning.

## Conventionalization versus grounding

These are related but separable.

- A grounded distinction can exist without an established communicative convention.
- A convention can exist around a task-action code with weak semantic grounding.
- A grounded convention has both a tested distinction and a stable signal-mediated mapping to it.

This yields a useful matrix:

| | Weak convention | Strong convention |
| --- | --- | --- |
| Weak grounding | unstable/private behavior | stable shortcut code |
| Strong grounding | understood but not conventionally communicated | strongest candidate grounded convention |

R2/R3 should include all four cells.

## Common ground and deception

Agents may share a convention while disagreeing about truth or incentives.

Example structure:

- both know signal S conventionally maps to quality Q;
- sender sometimes produces S deceptively;
- receiver understands the convention but discounts current reliability.

The correct update is **not** “semantic mapping lost.” It is:

- convention remains established;
- current claim reliability decreases;
- strategic/deceptive hypothesis increases;
- receiver epistemic state updates.

This is why convention, claim truth, sender reliability, and pragmatic function must remain separate.

## Stopping rule for establishment

Do not define common ground by one confidence threshold alone.

A convention may be labeled `ESTABLISHED_WITHIN_SCOPE` only when:

- declared critical evidence bundle is satisfied;
- no known simpler shortcut explains success;
- uncertainty is calibrated on withheld cases;
- unresolved asymmetries are recorded;
- scope is explicit;
- latest validation is recent enough for the environment’s drift rate.

## R3 implications

R3 should directly test:

- false common ground;
- partner-specific pacts;
- role reversal;
- partner swap;
- independently initialized partner acquisition;
- drift;
- repair;
- asymmetric competence;
- deceptive use of an intact convention;
- stable task coordination without reusable semantic structure.

## Claims boundary

Evidence under this model may justify:

`INTERACTIONALLY_SHARED_WITHIN_TESTED_SCOPE`

or, after sufficient grounding evidence:

`GROUNDED_CONVENTION_WITHIN_TESTED_SCOPE`

It does not establish:

- identical internal concepts;
- literal mutual belief at arbitrary recursive depth;
- consciousness;
- human-like social cognition;
- universal convention structure;
- truth of any current claim merely because its convention is shared.
