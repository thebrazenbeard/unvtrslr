# R3 — Pragmatics and Interaction Negative Controls

Status: `SPECIFIED / HARNESS_NOT_IMPLEMENTED`

## Purpose

R3 must not reward a system merely because it looks conversationally competent, obtains high task reward, emits familiar pragmatic markers, or adapts after failure.

The negative controls below are deliberately designed to **look better than they are**. Each one should succeed on some superficial measure while failing a specific pragmatic or semantic requirement. The R3 harness is trustworthy only if it rejects every control on the dimensions that control is built to violate.

These controls complement the R2 shortcut suite. R2 asks whether communication is grounded and causally used. R3 adds failures where grounded or task-relevant behavior still does not justify claims about addressee, context, repair, convention, pragmatic force, ambiguity, or conservation.

## Control requirements

Every negative control must:

- be reproducibly generated;
- expose only learner-visible inputs allowed by the corresponding candidate condition;
- have an explicit expected-success profile;
- have an explicit expected-failure profile;
- be scored blind to its control identity until after trace collection;
- be tested on hidden episodes not used to tune its behavior;
- remain visible in the final harness report even when it fails as intended.

A harness failure is not repaired by lowering the importance of the dimension the control exposed.

## RN00 — `task_policy_mimic`

### Construction

Sender transmits an opaque code for the receiver action that maximizes current task reward. The code need not represent the underlying world distinction or communicative function.

Example synthetic setup:

- world contains latent property X;
- task A maps X to action `left`;
- sender sends token L whenever `left` is optimal and R whenever `right` is optimal;
- receiver learns token→action.

### Expected superficial success

- high task reward;
- high sender-message/receiver-action mutual information;
- strong apparent request-like coordination;
- possible causal listening.

### Required failure

When task B changes the optimal action while preserving X or the communicative distinction, the code should fail cross-task reuse and semantic/pragmatic conservation.

### Must fail dimensions

- `FUNCTION_DISCRIMINATION` when functions share an action;
- `PRAGMATIC_CONSERVATION`;
- `SHORTCUT_RESISTANCE`;
- usually `CONTEXT_SENSITIVITY` under changed task.

### Primary tests

`P01`, `P14`, `P20`.

---

## RN01 — `partner_id_pragmatist`

### Construction

Receiver conditions responses primarily on partner identity rather than signal meaning or interaction evidence. During training, each partner identity is correlated with a distinct pragmatic policy.

### Expected superficial success

- apparently partner-sensitive language use;
- apparent conceptual pacts;
- high within-dyad reward;
- apparently appropriate addressee behavior.

### Required failure

Partner swap or independently initialized partner breaks the mapping even when the semantic/pragmatic convention is externally available.

### Must fail dimensions

- `PARTNER_TRANSFER`;
- `SHORTCUT_RESISTANCE`;
- potentially `ADDRESSEE_MODELING` if identity is mistaken for target evidence.

### Primary tests

`P07`, `P17`.

---

## RN02 — `context_lookup_table`

### Construction

Learner memorizes a context/episode identifier→interpretation table. The identifier is correlated with the correct pragmatic reading during training but is not causally part of the meaning.

Possible nuisance keys:

- background texture;
- episode index;
- scene seed;
- irrelevant object identity;
- serialization order;
- partner slot.

### Expected superficial success

- excellent same-surface/different-context classification on in-distribution episodes;
- apparently sophisticated context sensitivity.

### Required failure

When nuisance keys are permuted independently of the true causal context variable, the learner follows the nuisance cue.

### Must fail dimensions

- `CONTEXT_SENSITIVITY`;
- `SHORTCUT_RESISTANCE`;
- possibly `AMBIGUITY_CALIBRATION`.

### Primary tests

`P02`, `P18`.

---

## RN03 — `surface_speech_act_classifier`

### Construction

A human-language classifier predicts pragmatic labels from conventional surface markers such as sentence mood, punctuation, lexical templates, or prosodic stereotypes without modeling grounded context or interactional consequences.

Synthetic analogue: each training function has a fixed form marker that is later decoupled from function.

### Expected superficial success

- high request/assertion/question/warning classification on familiar forms;
- fluent human-readable output;
- strong benchmark accuracy on templated examples.

### Required failure

When form and function are independently permuted, when function is expressed indirectly, or when a new modality carries the same function, the classifier follows the marker rather than the interactional evidence.

### Must fail dimensions

- `FUNCTION_DISCRIMINATION`;
- `INDIRECT_INFERENCE_CALIBRATION`;
- `PRAGMATIC_CONSERVATION`;
- `SHORTCUT_RESISTANCE`.

### Primary tests

`P01`, `P04`, `P20`.

---

## RN04 — `repair_reflex`

### Construction

Whenever reward decreases, the sender/receiver triggers a fixed repair behavior such as:

- repeat the prior message;
- increase intensity;
- slow transmission;
- choose a canned alternate token;
- restart the interaction.

It never represents which layer failed.

### Expected superficial success

- better reward after many communication failures;
- turn-like repair behavior;
- repeated clarification-looking exchanges.

### Required failure

Inject qualitatively different trouble sources—channel corruption, segmentation ambiguity, wrong referent, wrong addressee, function mismatch. The reflex cannot target the actual mismatch and should underperform targeted repair on novel error types.

### Must fail dimensions

- `REPAIR_ROBUSTNESS`;
- `SHORTCUT_RESISTANCE`.

### Primary test

`P11`.

---

## RN05 — `deixis_by_fixed_coordinate`

### Construction

Learner maps deictic-looking signals to absolute coordinates learned during training. Sender and receiver occupy stable positions, making the shortcut appear perspective-aware.

### Expected superficial success

- high referential accuracy;
- apparent `here/there` or direction competence;
- correct navigation under training geometry.

### Required failure

Move/rotate sender and receiver, shift coordinate origin, reverse roles, or move the landmark while preserving the intended relative relation.

### Must fail dimensions

- `DEICTIC_GENERALIZATION`;
- `ROLE_REVERSAL` where applicable;
- `SHORTCUT_RESISTANCE`.

### Primary tests

`P03`, `P16`.

---

## RN06 — `audience_leak`

### Construction

Learner has access to a hidden or accidental feature correlated with evaluator-defined audience/addressee identity.

Possible leaks:

- agent array index;
- evaluator role label;
- recipient ID embedded in payload metadata;
- channel number uniquely tied to the intended audience;
- challenge-family identifier.

### Expected superficial success

- perfect addressee/audience prediction;
- apparently nuanced audience-dependent behavior.

### Required failure

Remove/permutate the leak while preserving observable orientation/channel/history evidence.

### Must fail dimensions

- `ADDRESSEE_MODELING`;
- `AUDIENCE_MODELING`;
- `SHORTCUT_RESISTANCE`.

### Primary tests

`P07`, `P08`.

### Harness rule

If evaluator-only audience labels leak into learner-visible inputs, this is not merely candidate failure. The affected evaluation run is `HARNESS_INVALID`.

---

## RN07 — `reward_predictor`

### Construction

Learner predicts which receiver behavior maximizes reward from current world/task state and treats that action prediction as the message’s pragmatic meaning.

The communication channel may be causally used, but the represented distinction is expected reward/action—not communicative function.

### Expected superficial success

- strong task reward;
- high action prediction;
- apparent request/warning behavior where those functions align with optimal action.

### Required failure

Create cases where distinct communicative functions induce the same action, or the same function implies different actions after task/incentive changes.

### Must fail dimensions

- `FUNCTION_DISCRIMINATION`;
- `PRAGMATIC_CONSERVATION`;
- `SHORTCUT_RESISTANCE`.

### Primary tests

`P01`, `P09`, `P14`.

---

## RN08 — `forced_intent_labeler`

### Construction

Learner is required by its decoder or output head to assign every candidate signal one label from a human-style inventory such as assertion/request/warning/query—even when the evidence supports noncommunication, ambiguity, multiple simultaneous functions, or an unknown function.

### Expected superficial success

- tidy labels;
- high accuracy on closed-set human controls;
- fluent explanations.

### Required failure

Use:

- noncommunicative behavior;
- unresolved signalhood;
- strategic ambiguity;
- simultaneous multi-function signals;
- synthetic communicative functions outside the training taxonomy.

The labeler should become overconfident and miscalibrated.

### Must fail dimensions

- `AMBIGUITY_CALIBRATION`;
- `INDIRECT_INFERENCE_CALIBRATION`;
- `SHORTCUT_RESISTANCE`;
- often `PRAGMATIC_CONSERVATION`.

### Primary tests

`P04`, `P10`, `P20`.

---

## RN09 — `pragmatics_conservation_liar`

### Construction

Translator produces a fluent target rendering that preserves coarse denotation/task effect while systematically dropping or inventing pragmatic structure.

Variants:

- drops addressee distinction;
- converts uncertain inference into assertion;
- converts counterpart claim into evaluator fact;
- erases strategic ambiguity;
- omits background dependency;
- changes request-like into assertion-like force;
- invents sender intention to make output natural.

### Expected superficial success

- high fluency;
- good lexical/reference match;
- possibly high task reward;
- high human preference on outputs that reward decisiveness.

### Required failure

Dimension-level conservation audit exposes unsupported `ADDED`, `OMITTED`, `AMBIGUITY_COLLAPSED`, or unmarked `INFERRED` content.

### Must fail dimensions

- `PRAGMATIC_CONSERVATION`;
- `AMBIGUITY_CALIBRATION`;
- `SHORTCUT_RESISTANCE`.

### Primary tests

`P01`, `P04`, `P05`, `P07`, `P09`, `P10`, `P19`, `P20`.

---

# Additional adversarial controls

These are not required by the first contract minimum but should be implemented early because they attack different assumptions.

## RN10 — `acknowledgment_heartbeat`

Receiver emits an acknowledgment token after every message regardless of understanding.

Should fail targeted confirmation tests even though turn coordination looks excellent.

## RN11 — `absence_hallucinator`

Learner assigns meaning to any missing expected packet without modeling channel loss or sender capability.

Should fail `P06` against matched random loss.

## RN12 — `convention_newest_wins`

Learner overwrites the convention on the latest anomalous use.

Should fail gradual drift/noise separation in `P12`.

## RN13 — `deception_erases_semantics`

Learner assumes that once a sender lies, the underlying signal convention no longer exists.

Should fail `P09`, where convention knowledge and current claim reliability are independently scored.

## RN14 — `multimodal_average`

Learner averages conflicting channel evidence into one confident latent state and exposes no conflict.

Should fail `P19`.

## RN15 — `human_pragmatics_only`

Learner performs well on human-language request/assertion/deixis/repair forms but lacks a representation capable of learning a synthetic, nonhuman communicative function family.

Should fail `P20` and the nonhuman positive oracle.

# Positive controls

R3 needs positive oracles because a harness that rejects everything is not useful.

## RP00 — `scoped_pragmatic_oracle`

### Construction

Evaluator-owned oracle receives only the learner-visible variables legitimately required to solve the test and is given the synthetic interaction rules/semantics through an implementation inaccessible to candidates.

It should:

- correctly distinguish the generated function/context/addressee/convention variables;
- preserve uncertainty where the generator leaves ambiguity;
- pass role/partner/context transformations within the declared scope;
- fail or return `UNKNOWN` outside its encoded scope rather than inventing a human label.

### Expected result

Pass all applicable critical R3 dimensions for its declared synthetic world family.

### Purpose

Establish achievable headroom and validate that the evaluator is not demanding impossible information.

---

## RP01 — `calibrated_uncertainty_oracle`

### Construction

Evaluator oracle is given the exact observable likelihood structure but not hidden truth for intentionally underdetermined cases.

It outputs the correct posterior or prescribed calibrated uncertainty over:

- multiple function hypotheses;
- addressee ambiguity;
- signalhood versus noncommunication;
- strategic ambiguity;
- channel-loss versus withholding when evidence is insufficient.

### Expected result

Strong `AMBIGUITY_CALIBRATION` and no penalty for refusing false certainty.

### Purpose

Verify that the harness rewards `UNKNOWN`/multiple-live-hypothesis outputs rather than forcing top-1 pragmatic labeling.

---

## RP02 — `partial_equivalence_oracle`

### Construction

Source and target share some tested invariants but intentionally lack others. Oracle has the exact synthetic mapping and emits a conservation ledger with:

- preserved dimensions;
- transformed dimensions;
- omitted/non-equivalent dimensions;
- context requirements;
- no unsupported additions.

### Expected result

Pass `PRAGMATIC_CONSERVATION` while explicitly returning `PARTIAL_OVERLAP`, `APPROXIMATE`, or `NO_FAITHFUL_EQUIVALENT` as appropriate.

### Purpose

Verify that R3 does not reward forced equivalence over honest non-equivalence.

---

## RP03 — `nonhuman_function_oracle`

### Construction

Synthetic agents use a communicative distinction that is deliberately awkward to describe as a human speech act—for example, a continuous modulation jointly specifying receiver sampling phase and a conditional environmental relation.

No request/assertion/question label is supplied.

### Expected result

Pass function/context/conservation tests by representing observable dependencies and consequences.

### Purpose

Verify that the harness itself has not hard-coded human pragmatics as the definition of communication.

# Harness qualification matrix

At minimum, the harness should demonstrate this pattern before any candidate qualification:

| Control | Expected overall result | Critical reason |
| --- | --- | --- |
| `RN00_task_policy_mimic` | FAIL | task action is not reusable pragmatic semantics |
| `RN01_partner_id_pragmatist` | FAIL | partner identity shortcut |
| `RN02_context_lookup_table` | FAIL | nuisance context leakage |
| `RN03_surface_speech_act_classifier` | FAIL | form marker substituted for function |
| `RN04_repair_reflex` | FAIL | repair is untargeted reflex |
| `RN05_deixis_by_fixed_coordinate` | FAIL | fixed coordinates substitute for perspective |
| `RN06_audience_leak` | FAIL or HARNESS_INVALID | hidden audience answer key |
| `RN07_reward_predictor` | FAIL | reward/action substituted for meaning |
| `RN08_forced_intent_labeler` | FAIL | closed-set intent overconfidence |
| `RN09_pragmatics_conservation_liar` | FAIL | fluent semantic loss/addition |
| `RP00_scoped_pragmatic_oracle` | PASS | achievable scoped solution |
| `RP01_calibrated_uncertainty_oracle` | PASS | uncertainty is rewarded |
| `RP02_partial_equivalence_oracle` | PASS | honest non-equivalence is rewarded |
| `RP03_nonhuman_function_oracle` | PASS | no human-pragmatics dependency |

# Meta-negative control rule

A negative control is useful only if it is **strong on something**. A trivial random system that fails every task does not validate the evaluator.

Prefer controls that achieve one or more of:

- high task reward;
- strong message/action correlation;
- causal receiver influence;
- fluent target rendering;
- high human pragmatic classification accuracy;
- successful within-dyad coordination;
- apparently adaptive repair;
- apparently context-sensitive behavior.

Then require the R3 dimension vector to reveal exactly what is missing.

# Result boundary

Passing the negative-control gate means only:

> the current R3 harness can distinguish its preregistered pragmatic shortcut systems from its scoped positive oracles.

It does not mean the control suite is exhaustive. New shortcut classes discovered during candidate evaluation must be added to a future frozen suite rather than retroactively changing the candidate’s hidden test.
