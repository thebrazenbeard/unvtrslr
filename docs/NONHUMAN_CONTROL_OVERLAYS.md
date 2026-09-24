# Nonhuman Communication Control Overlays

Status: `PASS_3_CONTROL_OVERLAY / CROSS_SPECIES_SCOPE`

Predecessor checkpoint: `HUMAN_NONVERBAL_SIGNED_PASS_2@390e533abc85682177327af6bbfa56c9719a0019`

Evidence basis:
- `research/NONHUMAN_COMMUNICATION.md`
- `research/NONHUMAN_COMMUNICATION_REFERENCES.md`
- `research/NONHUMAN_CLAIMS.md`
- `docs/NONHUMAN_BOOTSTRAP_CONSTRAINTS.md`

These overlays extend `docs/CONTROL_SUITE.md`. They do not assert that any reviewed animal system is equivalent to human language.

## NHCTRL-1 — structure without semantics

Construct an acoustic or multimodal system with rich clustering, sequence regularity, individual/style variation, and high predictive accuracy but with no evaluator-demonstrated signal-to-world semantic relation.

Expected result:
- `STRUCTURE_DISCOVERED = YES`
- `SEMANTICS_GROUNDED = NO`

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

## NHCTRL-9 — operational intentionality ladder

For a gesture-like system independently manipulate:
- recipient presence;
- recipient orientation/attention;
- response success;
- opportunity to persist;
- opportunity to elaborate or switch modality.

Intentionality evidence may raise a signalhood/function score when behavior changes appropriately, but its absence must not invalidate communication systems whose operation does not require flexible intentional production. If the exact intentionality probe is not supported in scope, report the separate applicability state (`STRUCTURALLY_INAPPLICABLE_IN_SCOPE` or `APPLICABILITY_UNRESOLVED`) rather than treating inapplicability as a pass.

Failure caught: either assuming intention from structured behavior or making human-like intention a universal prerequisite.

## NHCTRL-10 — social-learning/culture transfer

Matched populations should differ in transmission history while sharing basic sensorimotor capacity.

Test whether:
- signal forms differ by population;
- naive individuals acquire local forms socially;
- mediator separates species/biological constraint from population convention and individual idiosyncrasy.

Failure caught: treating culturally inherited variants as universal species semantics.

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

Every nonhuman-inspired control should record only the evidence axes that are relevant to the exact claim under test. Candidate axes include:

- observable structure;
- receiver discrimination;
- communicative function;
- context association;
- reference-like evidence;
- combination/systematic reuse;
- social learning/culture;
- intentionality evidence;
- semantic-qualification evidence.

For each relevant axis record:

- applicability: `APPLICABLE_TESTED | STRUCTURALLY_INAPPLICABLE_IN_SCOPE | APPLICABILITY_UNRESOLVED`;
- evidence state and exact evidence references;
- whether the axis is a prerequisite for the exact claim;
- the resulting effect on coverage and claim ceiling.

These axes form a partial prerequisite graph, not one universal monotonic ladder. Evidence on one axis must never be silently relabeled as evidence for a different axis or stronger semantic claim.

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
- social-learning history;
- evaluator-only labels and world variables;
- strongest claim the run is allowed to make.
