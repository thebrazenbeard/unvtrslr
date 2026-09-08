# Nonhuman Communication Control Overlays

Status: `PASS_3_CONTROL_OVERLAY / CROSS_SPECIES_SCOPE`

Predecessor checkpoint: `HUMAN_NONVERBAL_SIGNED_PASS_2@390e533abc85682177327af6bbfa56c9719a0019`

Evidence basis:
- `research/NONHUMAN_COMMUNICATION.md`
- `research/NONHUMAN_COMMUNICATION_REFERENCES.md`
- `research/NONHUMAN_CLAIMS.md`
- `docs/NONHUMAN_BOOTSTRAP_CONSTRAINTS.md`

These overlays extend `docs/CONTROL_SUITE.md`. They do not assert that any reviewed animal system is equivalent to human language.

## NHCTRL-1 — structure without a qualified semantic claim

Construct an acoustic or multimodal system with rich clustering, sequence regularity, individual/style variation, and high predictive accuracy but with no evaluator-demonstrated signal-to-world semantic relation.

Expected result:
- `STRUCTURE_DISCOVERED = YES`
- `SEMANTIC_CLAIM_SUPPORTED = NO`

Failure caught: treating tokenization, prediction, embeddings, compression, synthesis, or a recovered "alphabet" as translation.

Sperm-whale coda structure is the motivating positive example for rich structure with a deliberately lower semantic claim ceiling.

## NHCTRL-2 — identity cue versus individual address

Matched conditions:

1. signal varies with emitter identity only;
2. receiver recognizes emitter;
3. sender copies a receiver-associated signal to address that receiver;
4. sender uses a learned receiver-specific signal not reducible to simple copying.

The evaluator must not collapse all four into `NAME`.

Failure caught: anthropomorphic promotion from identity information to naming.

## NHCTRL-3 — context association versus reference-like evidence

Use an alarm-like system in which a signal covaries with an external class.

Compare:
- passive corpus correlation;
- matched-arousal context swap;
- playback with the external stimulus absent;
- playback after nuisance/acoustic equalization;
- receiver behavior under held-out contexts.

Failure caught: calling a context classifier semantic reference without causal receiver evidence.

## NHCTRL-4 — sequence structure versus compositional function

Provide reusable signal components with nonrandom ordering.

Run:
- intact natural-like order;
- reversed order;
- component shuffle;
- unfamiliar matched components;
- novel recombination with preregistered predicted receiver response.

Report separately:
- `FORM_COMBINATION`;
- `RECEIVER_COMBINATION_SENSITIVITY`;
- `PREDICTABLE_FUNCTION_COMBINATION`;
- `COMPOSITIONAL_SEMANTIC_GENERALIZATION`.

Failure caught: distributional syntax being promoted to compositional meaning.

## NHCTRL-5 — continuous spatial-vector signaling

Use a honeybee-inspired continuous movement/timing channel. Do not supply labels for direction, distance, route, or coordinate frame.

Include a condition where the sender's encoded quantity is based on a perceptual metric that differs systematically from evaluator Euclidean distance.

Failure caught: laundering evaluator physical variables into sender/receiver semantics.

## NHCTRL-6 — persistent chemical field

Use signals that:
- diffuse;
- decay;
- superpose;
- are reinforced by multiple producers;
- may be sampled after the original producer has departed.

Do not provide sender/message IDs.

Failure caught: assuming a discrete, synchronous one-sender/one-receiver message event.

## NHCTRL-7 — sensor/channel overlap

Use a physical substrate that carries both ordinary environmental sensing and socially contingent modulation, inspired by electrocommunication/electrolocation.

The learner must infer when variation is environmental, self-generated sensing, or communicative.

Failure caught: requiring `sensor_stream` and `communication_channel` to be disjoint architecture objects.

## NHCTRL-8 — shared actuator, mixed function

Use the same observable pattern family for:
- camouflage/background matching;
- defensive response;
- courtship/social display;
- communicative audience-targeted use.

Keep low-level visual structure similar enough that form alone is insufficient.

Failure caught: permanently labeling a pattern as communicative independent of audience, history, context, and receiver response.

## NHCTRL-9 — operational intentionality probes

For a gesture-like system independently manipulate, when those manipulations are applicable:
- recipient presence;
- recipient orientation/attention;
- response success;
- opportunity to persist;
- opportunity to elaborate or switch modality.

Intentionality evidence may raise a signalhood/function score when behavior changes appropriately, but its absence must not invalidate communication systems whose operation does not require flexible intentional production. `NOT_APPLICABLE` is not positive evidence and must reduce the coverage of any claim that would otherwise depend on the omitted probe.

Failure caught: either assuming intention from structured behavior or making human-like intention a universal prerequisite.

## NHCTRL-10 — social-learning/culture transfer

Matched populations should differ in transmission history while sharing basic sensorimotor capacity.

Test whether, where applicable:
- signal forms differ by population;
- naive individuals acquire local forms socially;
- mediator separates species/biological constraint from population convention and individual idiosyncrasy.

Failure caught: treating culturally inherited variants as universal species semantics. Systems without a meaningful social-learning axis are not failed by this control; the axis is simply inapplicable and cannot be credited.

## NHCTRL-11 — multimodal redundancy and conflict

Provide acoustic, movement, posture, chemical/electrical, or contextual cues with conditions where modalities:
- agree;
- one is absent;
- one is noisy;
- two conflict.

Measure whether the learner identifies which modality carries which function rather than concatenating all features into a hidden shared code.

## NHCTRL-12 — no-communication ecological correlation

Provide a richly structured behavior that correlates with world state but has no demonstrated receiver-directed function. Add an audience manipulation that leaves the behavior unchanged and a receiver-ablation condition where downstream ecology is unchanged.

Expected result: `COMMUNICATION_NOT_ESTABLISHED` or equivalent.

Failure caught: confusing ecological predictability with communication.

## NHCTRL-13 — anthropomorphic label trap

Evaluator metadata contains tempting labels such as `name`, `word`, `syntax`, `question`, `warning`, or `meaning`, while learner-visible evidence only supports narrower operational relations.

The mediator must report the operational relation and claim ceiling, not copy evaluator terminology.

## NHCTRL-14 — asynchronous collective authorship

A communication trace is produced by many contributors, persists, and is read by later participants. Remove any privileged single-sender identity.

Expected competence: represent collective provenance, temporal decay, and distributed update without fabricating a single author.

## NHCTRL-15 — cross-species perceptual mismatch

Construct one physical environmental variable with different sender and receiver perceptual transforms. A mediator succeeds only if it learns a cross-system relation among the transforms rather than assuming either side represents evaluator truth directly.

Expected reporting should distinguish:
- evaluator physical variable;
- sender perceptual quantity;
- receiver perceptual quantity;
- empirically supported bridge among them.

## Claim-specific evidence vector

There is no universal semantic evidence ladder for these controls. Every exact claim instead declares the evidence axes it actually entails and the prerequisite edges among those axes.

Candidate axes include:

- `STRUCTURE`;
- `RECEIVER_OR_COUPLED_PROCESS_DISCRIMINATION`;
- `COMMUNICATIVE_OR_COORDINATIVE_FUNCTION`;
- `CONTEXT_ASSOCIATION`;
- `EXTERNALLY_TESTABLE_OR_REFERENCE_LIKE_RELATION`;
- `FORM_OR_FUNCTION_COMBINATION`;
- `SYSTEMATIC_REUSE`;
- `TRANSFER_OR_REGROUNDING`;
- `SOCIAL_LEARNING_OR_CULTURE`;
- `INTENTIONALITY_EVIDENCE`;
- `UNCERTAINTY_AND_PROVENANCE`;
- `SEMANTIC_QUALIFICATION`.

For each axis record:

- `applicability = APPLICABLE | STRUCTURALLY_INAPPLICABLE_IN_SCOPE | UNRESOLVED`;
- `evidence_state = NOT_TESTED | NEGATIVE | MIXED | POSITIVE | UNKNOWN`;
- `claim_dependency = REQUIRED_FOR_THIS_CLAIM | SUPPORTING_ONLY | IRRELEVANT_TO_THIS_CLAIM`;
- `evidence_refs[]`;
- `claim_ceiling_effect`.

Only prerequisite edges entailed by the exact claim are mandatory. For example, a claim of learned cultural transmission requires evidence for a social-learning axis; a bounded receiver-discrimination claim does not. An inapplicable axis never counts as a pass, but an irrelevant axis cannot become a universal blocker. Missing material evidence lowers or withholds the exact claim rather than forcing every communication system through a human-derived sequence.

The universal anti-promotion rule is narrower:

> Evidence for one axis must not be silently relabeled as evidence for another axis or for a stronger semantic claim.

## Required provenance fields

Record:
- source species/system inspiration;
- which facts are empirical and which are synthetic extrapolation;
- channel physics;
- persistence/latency;
- sender/receiver assumptions, if any;
- whether the channel overlaps ordinary sensing;
- whether behavior pre-existed or was negotiated;
- receiver evidence type: observation, playback, intervention, navigation, social response, other;
- social-learning history where applicable;
- evaluator-only labels and world variables;
- evidence-vector applicability/status for the exact claim;
- strongest operational claim supported;
- semantic-qualification state, if separately tested;
- overall claim ceiling.
