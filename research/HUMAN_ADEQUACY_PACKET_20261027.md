# Blinded bilingual adequacy packet — source-only Argos benchmark

**Status:** SOURCE/PACKET PRODUCED, HUMAN_ANNOTATION_NOT_COLLECTED, SEMANTIC_QUALIFICATION_UNKNOWN. This is an extension of merged PR #43 and unresolved [issue #44](https://github.com/thebrazenbeard/unvtrslr/issues/44).

This script pairs the frozen published MASSIVE English **source-only requests** with previously SHA-verified Argos `OK` predictions, with **no** published target/reference annotations in the reviewer-facing file. For each of four target locales (fr-FR, de-DE, sw-KE, tr-TR), it selects the first 20 items under a deterministic fixed SHA-256 ordering of corpus IDs and locale. It produces 80 `source_text/candidate_text` tasks under opaque review identifiers and a separately located, evaluator-private ID/model manifest. It refuses changed input prediction hashes, missing predictions, non-OK outputs, duplicate IDs, or overwriting old results. Sampling was decided *after* initial model results were known; it is a **diagnostic convenience sample**, not a preregistered unbiased benchmark or statistical population estimate.

Observed Lappy packet:
- Reviewer-only file: `C:\Temp\bt2-humanqa-reviewer-20261027\packet.jsonl` (80 items), SHA-256 `eb6f85271d4022e4597b0c192c63cfde29d290fb83656b74789a5d33652044d4`.
- Evaluator-private manifest: `C:\Temp\bt2-humanqa-private-20261027\manifest.jsonl` (80 items), SHA-256 `1a8009546947efb99324780170d118c516229737dd4ee4a22e3a1ce0f7b94acd`.
- No raw packet or manifest are committed. Separate paths **do not** enforce ACL isolation if the same user can read both; grant reviewers access to the public packet alone through an externally controlled share and never give them the manifest.

Reproduce with `python runs/massive_v1_first_real_corpus_20260922/human_blind_packet.py --requests-dir <verified-request-dir> --predictions-dir <verified-predictions-dir> --reviewer-out <new-reviewer-directory>/packet.jsonl --private-out <different-private-directory>/manifest.jsonl`. The source-only prediction SHA-256 pins are identical to the published PR #43 record. Use fresh paths; scripts reject overwriting evidence.

## Human evaluation protocol (not yet executed)

Recruit **at least two fluent bilingual raters per target language** who do not see model identity, engine attribution, reference translations, or one another's ratings. A bilingual rater sees only `task_id`, English source, and candidate target. For each item independently record:
- **Meaning adequacy** 0 = unrelated/wrong; 1 = serious semantic error; 2 = minor omission or nuance change; 3 = all essential meaning preserved.
- **Target fluency** 0 = unintelligible; 1 = heavily ungrammatical; 2 = understandable awkward; 3 = natural and grammatical.
- **Error flags**, independently: actor/patient reversal, negation, tense/aspect, entity/number, omission, added meaning/hallucination, register/politeness, other (brief free-text justification).
- **Uncertainty** 0/1/2 for confident/uncertain/cannot judge; allow `ABSTAIN_RATER` rather than forced ratings.

Store each rater's independent signed/dated scores in a private audit trail. Predefine adjudication for serious rater disagreements and report per-language disagreement/coverage, not only aggregated mean. Keep human review separate from automatic BLEU/chrF exact match. Rejoin the evaluator manifest only **after** annotation submission freezes; only then compare with the reference if needed. No claim of blinded evaluation, adequacy, or human certification is justified before those actual ratings exist.

This packet measures the external Argos model only. It **does not** prove UNVTRSLR learned real natural language, translate Num’ta’reen canon, or enforce a strong OS-level evaluator boundary.
