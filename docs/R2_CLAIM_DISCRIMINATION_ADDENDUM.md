# R2 — Claim-Discriminating Semantic Qualification Addendum

Status: `PROVISIONAL / RESEARCH-DERIVED / NOT_IMPLEMENTED`

## Purpose

R0.5 can establish that learner evidence is admissible and that an operational relation is empirically distinguishable and properly attributed.

That is not yet enough for a strong semantic claim.

R2 must test whether the proposed interpretation makes predictions that differ from serious alternatives and survives evidence capable of breaking the confounds that made the interpretation attractive.

## Fresh evidence is not automatically confirmatory

A genuinely new IID holdout from the same environment family may preserve the same nuisance/semantic correlation as training data.

Therefore:

`FRESH_EVIDENCE != CLAIM_DISCRIMINATING_EVIDENCE`

Suggested statuses:

- `FRESH_BUT_NONDISCRIMINATING_EVIDENCE`
- `CLAIM_DISCRIMINATING_HOLDOUT`
- `COUNTERFACTUAL_OR_SHIFT_TESTED`
- `SEMANTIC_INTERPRETATION_STILL_CONFOUNDED`

A semantic interpretation should not receive strong promotion merely because it generalizes to unseen samples drawn from the same confounded regime.

## Required control — `CTRL_IID_HOLDOUT_ILLUSION`

Construct a case where:

1. the learner discovers a real transferable operational relation;
2. a candidate semantic interpretation fits training data;
3. the interpretation is frozen;
4. a fresh IID holdout from the same regime confirms it;
5. a preregistered intervention or domain shift breaks the nuisance/semantic correlation while preserving the narrower operational relation;
6. the candidate continues tracking the nuisance or narrower invariant rather than the claimed semantic content.

Expected result:

- operational relation may remain verified;
- fresh-IID success may remain recorded;
- strong semantic promotion must fail or narrow;
- the certificate should identify the interpretation as confounded or best-supported only within the narrower regime.

## Structured alternatives matter

An open/null rival such as `NONE_OF_DECLARED_RIVALS` is useful because it prevents forced choice among named labels.

It is not a substitute for serious structured model criticism.

R2 should distinguish:

- rejection escape exists;
- structured alternatives were generated or nominated;
- structured alternatives were materially tested;
- misspecification was detected;
- only declared rivals were compared.

A losing null bucket does not eliminate omitted structured explanations.

## Confirmatory versus exploratory semantic naming

If a semantic interpretation is proposed only after inspecting a learned relation, the same data cannot both select and confirm that interpretation.

Required workflow:

`discover operational relation -> freeze proposed interpretation -> collect independent claim-discriminating evidence -> test interpretation`

Suggested statuses:

- `CONFIRMATORY_TARGET_CLAIM`
- `EXPLORATORY_POST_HOC_INTERPRETATION`
- `POST_HOC_INTERPRETATION_RETESTED_ON_FRESH_EVIDENCE`
- `OPERATIONAL_RELATION_VERIFIED_SEMANTIC_NAMING_UNRESOLVED`

Even after fresh retesting, the evidence must be claim-discriminating rather than merely new.

## Informational relation versus communicative function

A receiver may exploit a cue to predict a state without the source using that cue communicatively.

R2 should keep separate statuses such as:

- `INFORMATIONAL_RELATION_SUPPORTED`
- `RECEIVER_USE_SUPPORTED`
- `COMMUNICATIVE_FUNCTION_SUPPORTED_IN_SCOPE`
- `COMMUNICATIVE_FUNCTION_UNRESOLVED`
- `NONCOMMUNICATIVE_CUE_SUPPORTED`

Receiver exploitation alone must not promote a producer-side communicative or intentionality claim.

## Non-monotonic claim ladder

R2 must permit outcomes where earlier successes survive while stronger claims fail.

Examples:

- operational relation verified / semantic label unresolved;
- clean learner attribution / semantic interpretation confounded;
- fresh holdout passed / claim-discriminating shift failed;
- best among declared rivals / structured-rival adequacy not established;
- communicative use unresolved / informational relation supported.

No earlier success automatically upgrades a later claim.

## Conservative claim ceiling

Where structured alternatives remain incomplete, prefer:

`BEST_SUPPORTED_INTERPRETATION_AMONG_DECLARED_RIVALS_WITHIN_TESTED_SCOPE`

Where the operational relation is strong but semantic naming is not independently confirmed, prefer:

`OPERATIONAL_RELATION_VERIFIED / SEMANTIC_NAMING_UNRESOLVED`

The evaluator should not emit `TRUE_MEANING_RECOVERED` as a consequence of closed-family success, fresh IID generalization, or post-hoc interpretability.

## Open research frontier

A remaining falsification target is whether the adjective `semantic` adds any independently testable obligation beyond a robust, reusable, transferable predictive/coordination relation once:

- evidence provenance is clean;
- privileged instrumentation is absent;
- the interpretation is preregistered or independently retested;
- claim-discriminating evidence is used;
- structured alternatives are materially stressed;
- learner attribution is clean;
- transfer is robust.

If no additional observable obligation can be identified, UNVTRSLR should lower the claim ceiling rather than define semantic success by fiat.
