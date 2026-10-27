# Frozen Argos bilingual translation-adequacy review packet

**Status 2026-10-27:** 80 target-language candidate translations selected from the already frozen 800-item real Argos MASSIVE inference. **Human scores: NOT COLLECTED.** This packet is *ready for independent bilingual reviewers*, not proof of translation accuracy, reviewer authenticity, blind test independence, or OS security.

## Evidence, scope, custody

- Source: UNVTRSLR `main@75f9388e2ad6f6e3cee027ec42235e3e51ef28de`, published MASSIVE 1.0 test split, 200 frozen IDs per en→fr/de/sw/tr; source archive SHA-256 `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`.
- Source-only request SHA-256 and actual Argos prediction SHA-256 are pinned **per language** by `human_blind_packet.py`. Sampling was chosen after model outcomes were observed and is diagnostic, not preregistered. Sampling is deterministic by seed `UNV_BILINGUAL_QA_SHA_SAMPLE_V1`, 20 items per locale, not accuracy-stratified or population-representative.
- **Public reviewer packet** fields: `task_id`, `source_language`, `target_locale`, `source_text`, `candidate_text`. No gold reference, model name, original MASSIVE ID, intent or slots.
- **Private crosswalk** maps task IDs to original IDs and candidate engine, and is kept in a separate directory. Reviewers must never receive it or the sealed dataset. This split is a procedural control; the same Windows user can still access both locations. Deterministic IDs are opaque, **not cryptographic anonymization**.
- Generated on Lappy: packet SHA-256 `eb6f85271d4022e4597b0c192c63cfde29d290fb83656b74789a5d33652044d4`; private manifest SHA-256 `1a8009546947efb99324780170d118c516229737dd4ee4a22e3a1ce0f7b94acd`. Both contain uncommitted dataset-derived content at `C:\Temp\bt2-human-qa-reviews-20261027\public\packet.jsonl` and `C:\Temp\bt2-human-qa-reviews-20261027\private\manifest.jsonl`. **Do not commit or redistribute the raw task sheets without establishing dataset rights.**

## Evaluator procedure

1. Recruit two **actual fluent bilingual** reviewers per language, ideally from distinct sources, with conflict disclosure and documented consent. This step has not occurred. Do not use an LLM score and call it human-verified.
2. Provide only the public JSONL and the rubric below. Record reviewer IDs separately and independently. Randomized task order is already fixed; do not show either reviewer gold translations or the other's judgments.
3. For each task, rate **meaning preservation (adequacy)** and **target fluency** independently from 0 to 4, or mark UNRATABLE. In case of uncertainty choose UNRATABLE rather than fabricate meaning. Errors can include OMISSION, ADDITION, ROLE_SWAP, NEGATION, TIME, ENTITY, UNINTELLIGIBLE or OTHER. Record a short reason for a nonperfect score.
4. Input schema (one JSON object per line per reviewer, 2 per task): `{"task_id":"<20-hex>","reviewer_id":"rater-a","status":"RATED","adequacy":3,"fluency":4,"errors":["OMISSION"],"comment":"Minor missing qualifier"}`. For `UNRATABLE`, use null adequacy and fluency with `errors: []`.
5. Seal the **complete 160-row input** with a checksum; never alter it post-scoring. The CLI requires the frozen public packet digest and refuses missing, duplicate, altered, impossible or partial records. A code-generated fixture is **not a review**.
6. Aggregate only after both submissions, using `human_blind_scoring.py --packet <public> --ratings <ratings.jsonl> --reviewer-a rater-a --reviewer-b rater-b --expected-packet-sha256 eb6f85271d4022e4597b0c192c63cfde29d290fb83656b74789a5d33652044d4 --out <fresh-report>`. The result explicitly marks `human_provenance_verified: false` and `independence_proven: false` until documented audit external to this CLI.
7. Review disagreement and adjudicate major semantic failures **without retraining or selecting thresholds against these 80 published-test items**. Report by language, error classes, unratable counts and reviewer agreement; distinguish adequacy from automatic BLEU/chrF.

## Ordinal review rubric

Adequacy 0 = source meaning unrelated or reversed; 1 = substantial meaning missing/wrong; 2 = partially correct with important errors; 3 = mostly faithful with minor errors; 4 = fully faithful in context. Fluency 0 = unintelligible target; 1 = severely broken; 2 = understandable but awkward; 3 = natural with minor flaws; 4 = fluent natural target. For explicit NEGATION, ENTITY and ROLE_SWAP, report the category even if fluent.

These 80 items are a **diagnostic convenience sample**, not a new statistically independent held-out set. Unweighted Cohen kappa is only descriptive for two raters and may be undefined when all ratings are identical; report the denominator and pair agreement. No human adequacy result exists as of this document.

The earlier Argos BLEU and chrF++ measurements remain unchanged and explicitly diagnostic. Num'ta’reen authored data/canon and other systems are not modified.
