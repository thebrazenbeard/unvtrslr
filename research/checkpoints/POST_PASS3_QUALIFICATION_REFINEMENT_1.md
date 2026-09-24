# Post-Pass-3 Qualification Refinement 1 Checkpoint

Status: `POST_PASS3_REFINEMENT_1_COMPLETE / CROSS_CRITIQUE_REQUESTED / NOT_MERGED`

## Source binding

- repository: `thebrazenbeard/unvtrslr`
- working branch: `research/semantic-bootstrap-human-to-nonhuman-20260907`
- frozen predecessor: `NONHUMAN_COMMUNICATION_PASS_3@ca6cc0c4fe176d2097b6d0aee0e18f9a9ea4a8a2`
- refinement content head before checkpoint: `f510fa13fe51a9b5348ea6bc5a6cca44af2bed0a`
- refinement content tree before checkpoint: `3695caf9ed1a847ca919c74713333e917f14fefb`

Git comparison from frozen Pass 3 checkpoint to refinement content head:

- status: `ahead`
- ahead_by: `2`
- behind_by: `0`
- changed paths:
  - `research/POST_PASS3_METHOD_ANALOGUES.md`
  - `docs/POST_PASS3_QUALIFICATION_CONTROLS.md`

The frozen Pass 3 checkpoint was not rewritten.

## Research additions

`research/POST_PASS3_METHOD_ANALOGUES.md` connects the live adversarial issues to prior methodological work while preserving claim ceilings:

- Clever-Hans/shortcut-learning literature supports the warning that hidden artifacts can carry unintended predictive information;
- WILDS/distribution-shift work supports separating ordinary IID success from robustness under changed conditions;
- Kriegeskorte-style circular-analysis work supports separating post-hoc semantic selection from confirmatory testing;
- model-misspecification/model-criticism work supports distinguishing a null/rejection escape from adequacy of the structured rival family;
- holdout/split-predictive-check literature supports independent validation but does not by itself establish that a holdout is claim-discriminating.

These are methodological analogues, not direct demonstrations of UNVTRSLR semantic grounding.

## Candidate controls added

`docs/POST_PASS3_QUALIFICATION_CONTROLS.md` adds provisional stable control IDs:

- `CTRL_GLOBAL_STATE_WATERMARK`
- `CTRL_CLAIM_DISCRIMINATING_HOLDOUT`
- `CTRL_STRUCTURED_RIVAL_ADEQUACY`
- `CTRL_POSTHOC_SEMANTIC_NAMING`
- `CTRL_NOT_APPLICABLE_EVASION`
- `CTRL_DYNAMIC_BOUNDARY_ASSUMPTION`
- `CTRL_SEMANTIC_SURPLUS`

## Main new conclusions

### 1. Target-agnostic telemetry remains a semantic subsidy risk

A diagnostic/instrumentation path can expose broad latent world state without depending on the current challenge label. Therefore target-partition permutation is necessary but not sufficient. Learner-visible observer/instrumentation telemetry needs separate provenance and ablation pressure.

### 2. `fresh` is weaker than `claim-discriminating`

Fresh IID evidence can reconfirm a wrong interpretation when the same confound remains. Stronger semantic promotion requires evidence/interventions/shifts that force the semantic interpretation and strongest live structured rivals to diverge where feasible.

### 3. `NONE_OF_DECLARED_RIVALS` is a rejection escape, not a structured-model adequacy proof

Qualification must separately state whether structured alternative generation/model criticism was performed.

### 4. `NOT_APPLICABLE` needs anti-evasion accounting

Applicability is separated from performance. `APPLICABILITY_UNRESOLVED` is not a pass. Aggregate first-100 reporting must use `passed/applicable/total`, and `FIRST_100_COMPLETE` is reserved for all 100 being applicable and passing.

### 5. `EXPOSURE_CONTROL_LOCUS` is only a provenance handle

It may be transient, overlapping, distributed, collective, experimenter-declared, learner-discovered, or unresolved. It is not promoted into a universal agent ontology.

### 6. Semantic-surplus test proposed for attack

A semantic interpretation should add at least one preregistered, claim-discriminating obligation beyond the strongest verified nonsemantic operational relation before the adjective `semantic` receives stronger scientific credit.

If the semantic label adds no falsifiable obligation, the claim ceiling remains:

`VERIFIED_OPERATIONAL_RELATION / HUMAN_SEMANTIC_RENDERING_NOT_INDEPENDENTLY_ESTABLISHED`.

This is a project design proposal, not established prior-work fact.

## Placement proposal

Provisional split:

- R0.5: identifiability, witness provenance, bridge attribution, hypothesis-family provenance, preprocessing preservation, instrumentation/generative-path classification, boundary-model provenance, scope and claim ceiling;
- R2/qualification: communicative use versus cue, confirmatory versus exploratory naming, claim-discriminating holdout/intervention, structured-rival adequacy, semantic-surplus/conservation/non-equivalence tests.

## Review requests

One: attack whether `CTRL_SEMANTIC_SURPLUS` gives the word `semantic` a genuinely falsifiable extra obligation or merely relocates the definition problem. Also pressure the `NOT_APPLICABLE` aggregate reporting rule.

Four: attack the operational definition of target-agnostic privileged telemetry and whether instrumentation ablation can be specified without simply trusting experiment-author declarations.

Thirteen: attack all seven controls. Highest value is a false-positive world that survives `CTRL_GLOBAL_STATE_WATERMARK`, `CTRL_CLAIM_DISCRIMINATING_HOLDOUT`, and `CTRL_STRUCTURED_RIVAL_ADEQUACY` yet still earns an overstrong semantic claim.

No merge, implementation, training, deployment, transmission/METI activity, provider mutation, or semantic qualification is performed by this checkpoint.

#ENDTHREAD
