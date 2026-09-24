# R3 Extension Candidates V2

Status: `CANDIDATE_EXTENSION_DESIGN / NOT_PART_OF_R3_V1 / NOT_IMPLEMENTED / NOT_QUALIFIED`

Research basis: [`../research/COMMUNICATIVE_FUNCTION_SECOND_PASS.md`](../research/COMMUNICATIVE_FUNCTION_SECOND_PASS.md)

## Purpose

Preserve the first-cycle R3 V1 contract while staging a small set of evidence-driven extensions that emerged from the second communicative-function challenge pass.

These are not automatic changes to `specs/R3_EVALUATION_CONTRACT_V1.yaml`. They are candidates for an explicit R3 V2/R3.1 design review after R3 V1 remains frozen and reproducible.

## Candidate E01 — `interaction_effect_hypothesis`

### Problem

R3 V1 can still tempt an implementation to move too quickly from “signal intervention changed behavior” to “communicative function established.”

Causal influence is lower-level evidence. It can arise from a cue, coercion, task-policy command, self-regulation, or genuine communication.

### Proposed object

```text
interaction_effect_hypothesis:
  source_event
  affected_locus_set
  measurable_effect
  causal_intervention_evidence
  timing
  context_dependencies
  alternative_mechanisms
  provenance
  scope
```

### Promotion rule

`interaction_effect_hypothesis` may support a higher `communicative_function_hypothesis`, but cannot itself certify one.

### Required rival mechanisms

At minimum where applicable:

- incidental correlation;
- cue exploitation;
- coercive physical influence;
- task-policy control;
- self-regulation;
- hidden shared state/side channel;
- genuine signal-mediated interaction.

## Candidate E02 — producer / receiver / interaction function split

### Problem

One unqualified “function” field can collapse three different questions:

1. what production accomplishes for the producer;
2. what the receiver extracts or does;
3. what stable role exists in the coupled interaction.

### Proposed objects

```text
producer_function_hypothesis
receiver_use_hypothesis
interaction_level_function_hypothesis
```

Each object carries its own evidence, alternatives, confidence, provenance, and scope.

### Allowed relations

- `CONVERGENT`
- `PARTIAL_OVERLAP`
- `DIVERGENT`
- `CAUSALLY_LINKED`
- `UNKNOWN`

No requirement says the three must converge.

## Candidate E03 — recipient structure instead of one addressee slot

### Problem

Dyadic sender→receiver modeling is insufficient for broadcast, eavesdropping, coalition signaling, group coordination, many-sender aggregation, and self-heard signaling.

### Proposed object

```text
recipient_structure_hypothesis:
  source_locus_set
  candidate_recipient_set
  recipient_roles
  membership_uncertainty
  self_receipt_status
  audience_or_overhearer_set
  dynamic_membership_history
  evidence
  alternatives
```

### Candidate recipient shapes

- `SELF_ONLY`
- `OTHER_ONLY`
- `SELF_AND_OTHER`
- `ONE_TO_MANY`
- `MANY_TO_ONE`
- `MANY_TO_MANY`
- `BROADCAST_UNKNOWN`
- `NO_RECIPIENT_ESTABLISHED`

These are operational interaction shapes, not universal natural-agent ontology.

## Candidate E04 — information / influence / semantics / pragmatics vector

### Problem

A single communication score can hide qualitatively different successes.

### Proposed vector

- `STATISTICAL_INFORMATION`
- `CAUSAL_INFLUENCE`
- `REUSABLE_SEMANTIC_DISTINCTION`
- `INTERACTIONAL_FUNCTION`
- `PRODUCER_FUNCTION`
- `RECEIVER_USE`
- `RELIABILITY`
- `STRATEGIC_STATUS`

The values need not be scalar probabilities in every substrate, but each dimension must remain independently auditable where the candidate claims it.

### Core non-implications

```text
STATISTICAL_INFORMATION -> COMMUNICATIVE_FUNCTION    INVALID
CAUSAL_INFLUENCE -> SEMANTIC_GROUNDING               INVALID
CAUSAL_INFLUENCE -> PRAGMATIC_FUNCTION               INVALID
PRODUCER_FUNCTION -> RECEIVER_USE                     INVALID
RECEIVER_USE -> PRODUCER_INTENTION                    INVALID
RELIABILITY -> CONVENTION_EXISTS                      INVALID
DECEPTION -> CONVENTION_DOES_NOT_EXIST                INVALID
```

## Candidate E05 — `RN16_self_regulation_masquerading_as_message`

### Construction

- producer emits signal S;
- producer receives S through its own sensory/control channel;
- self-receipt causally stabilizes or changes producer behavior;
- another agent can observe S but does not causally use it;
- temporal coordination makes S look externally communicative to a naive evaluator.

### Naive apparent success

- strong signal/action correlation;
- apparent sender→receiver timing;
- high task reward;
- externally visible signaling behavior.

### Required failure

R3 V2 must detect that external receiver intervention/ablation shows no receiver-side causal use and should preserve self-regulatory function separately.

### Must fail dimensions

- external `CAUSAL_INFLUENCE` claim;
- external `INTERACTIONAL_FUNCTION` claim;
- `SHORTCUT_RESISTANCE` if system collapses self-use into external communication.

## Candidate E06 — `P21_reliability_transfer_under_stable_convention`

### Question

Can the system preserve a semantic convention while learning that current use is contextually unreliable?

### Construction

1. establish convention K under aligned incentives;
2. verify denotational/operational use;
3. alter sender incentives only in selected contexts;
4. preserve signal forms and source ontology;
5. inject honest, deceptive, and unknown-reliability cases;
6. change context distribution in holdout.

### Pass evidence

- convention K remains represented;
- context-specific claim reliability changes;
- deception does not trigger global convention deletion;
- unknown contexts remain calibrated;
- current truth status is not inferred from convention membership.

### Failure controls

- `RN13_deception_erases_semantics`;
- `convention_implies_truth`;
- global-distrust-after-local-deception;
- surface-token-reliability lookup.

## Candidate E07 — cue / signal / coercion synthetic family

### Purpose

Exploit the biological signaling literature as a **synthetic control family**, not a universal definition.

### Evaluator-hidden construction

Create three outwardly similar event families:

1. **cue-like:** producer event is correlated with state and receiver exploits it, but production policy is unaffected by receiver response history;
2. **signal-like:** production and receiver response are jointly selected/trained because of their interaction effect;
3. **coercion-like:** producer action physically forces/perturbs receiver state without a receiver policy adapted/learned to interpret it.

### Learner-visible rule

The learner does not receive the evaluator labels. It must distinguish only the observable/interventional consequences available under the declared interaction surface.

### Claim ceiling

If historical/training provenance required to separate these families is hidden from the learner and not recoverable through interaction, the correct learner result may remain `UNRESOLVED`. The evaluator may score whether the learner avoided an unsupported stronger label.

## Candidate E08 — many-to-many pragmatic positive oracle

### Purpose

Prevent R3 from equating communication with one sender and one receiver.

### Construction

A synthetic group task in which:

- two producer loci each have complementary partial state;
- three receiver loci require different projections of the joint distinction;
- no single message or sender suffices;
- one receiver is an overhearer rather than a target;
- group membership changes on holdout episodes.

### Pass evidence

- correct recipient-structure hypotheses;
- no forced dyadic decomposition that loses information;
- sender contributions remain provenance-bearing;
- overhearer is not silently promoted to addressee;
- group-state changes update recipient structure rather than semantic content where appropriate.

## Candidate E09 — certificate communication-definition binding

### Problem

“Communication” can mean different things across signaling-game, biological, human-pragmatic, and synthetic-agent literature.

### Proposed certificate field

```yaml
communication_evidence_profile:
  operational_definition_version: ...
  required_evidence_dimensions: ...
  excluded_claims: ...
  evolutionary_history_available: true|false
  causal_receiver_use_tested: true|false
  producer_function_tested: true|false
  recipient_structure_tested: ...
  reliability_tested: ...
```

This prevents one R3 result from being read as satisfying every theoretical definition of communication.

## V1 compatibility rule

R3 V1 remains frozen unless a deliberate version transition occurs.

These V2 candidates may be explored in synthetic worlds without changing the V1 qualification contract. If implemented later, they must receive:

- their own contract version;
- new negative/positive controls;
- preregistered thresholds;
- new certificate version or explicit compatible extension fields;
- a migration note explaining what V1 certificates do and do not imply under V2.

## Research consequence

The second pass sharpens the project away from a hidden human-pragmatics ontology and toward a more general causal-interaction account:

> **first establish what changes what; then test whether the effect is signal-mediated, reusable, partner-sensitive, recipient-directed, reliable, semantically grounded, and pragmatically structured. Do not collapse those questions because one familiar communication theory gives them one name.**
