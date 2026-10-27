# Supervised synthetic compositional learning — first executable baseline (2026-10-27)

**Claim ceiling:** `SUPERVISED_FIXED_LENGTH_POSITIONAL_COMPOSITION_SYNTHETIC_ONLY`. This is neither unsupervised language discovery nor Num’ta’reen/real-world fluent translation.

## What is genuinely learned

`src/unvtrslr/compositional_probe.py` fits a reusable position-to-semantic-slot hypothesis from labeled *training only*. It is **not** given the five token-position mappings or an author-supplied vocabulary map. For each semantic field, it estimates which input position predicts that field, requires repeated consistent token evidence and a 0.15 predictive-margin over other positions, then abstains if support is absent or ambiguous. The training examples include structured semantics; supervision is explicit.

The private evaluator constructs an opaque five-token surface for **actor, action, patient, tense, polarity** with four noun values, three actions, two tenses and two polarity values. There are 192 unique combinations per seed. A seeded shuffle fixes 96 training and 96 held-out **unseen combinations**. Vocabulary mappings differ over seeds 17, 23, 47 and 61; learner code has no generator dictionary or test labels. Train and inference run in a separate child interpreter from evaluator scoring, with requests containing only `id` and `source_text`. This is **not** restricted OS/filesystem security; evaluator source and data remain accessible to the same user. Full source files and model remain on local temporary directories during evaluation; only per-seed JSON reports are versioned.

## Observations

| Labeled train rows per seed | Held-out exact accuracy (seeds 17 / 23 / 47 / 61) |
| --- | --- |
| 8 | 0% / 22.92% / 33.33% / 0% |
| 16 | 100% / 100% / 100% / 76.04% |
| 32 | 100% / 100% / 100% / 100% |
| 48 | 100% / 100% / 100% / 100% |
| 64 | 100% / 100% / 100% / 100% |
| 96 | 100% / 100% / 100% / 100% |

At 96 examples per seed, **384/384 held-out tuples** were recovered exactly. Exact whole-sentence memorization was **0/384 coverage**; random shuffling of whole training labels produced **0/384 coverage** at the learner’s abstention gate. Unknown lexical tokens and changed token counts produce `ABSTAIN`.

These scores are intentionally narrow: the task is **fixed-length and positional**; the model has **not learned negation scope, embedded syntax, free word order, unknown vocabulary semantics, acoustic interpretation or natural-language translation**. Its high synthetic score must not be used as evidence of those capabilities. The author-controlled generator is transparent and this is a laboratory unit benchmark, not independent human validation.

Reproduction from repository root: `python runs/composition_20261027/run.py --seed 17 --out /tmp/composition-17.json`; repeat for 23/47/61 using a fresh path. Each evaluator invokes a **separate worker process** for fitting and source-only prediction. Compare JSON receipts in `research/COMPOSITION_SEED*_20261027.json`. The four sha-bound splits cannot be modified after inspecting results without disclosing a new benchmark version.

## Independent published comparator

The official <https://github.com/brendenlake/SCAN> add-primitive **jump** split was fetched at Git commit `c4b756cbc010d75c912f16c42c8f15dc6b7e6c8f`. Frozen train SHA-256 `15c82c6bd4222a1f44d28aea6e56f23a52002c9a8b05f77497544114055a62b7`; test SHA-256 `14ea0560537282a343141d324a278ee4d7337a1744f740dc811307ab6f162450`. There are **14,670 training records / 7,706 test records**. Exact phrasebook coverage and source-text copy exact-match on the official test are both **0%**, recorded in `research/SCAN_NEGATIVE_CONTROL_20261027.json`. The constrained positional learner has **no scored SCAN sequence-to-sequence result**. This must be addressed with a genuine variable-length learner rather than rebranding exact memorization. Research: Lake and Baroni, ICML 2018, <https://proceedings.mlr.press/v80/lake18a.html>.

FLORES-200 is a complementary real-world multilingual evaluation with **access terms** at <https://huggingface.co/datasets/facebook/flores> (CC BY-SA 4.0), and the official repository advises more recently maintained alternatives: <https://github.com/openlanguagedata/flores>. No gated corpus was downloaded, translated or scored in this run. To avoid evaluation leakage, require a separately prepared reference-held evaluator and no use of test references for model selection. Human bilingual adequacy review on natural utterances is outstanding.

## Num’ta’reen boundary and cross-repository rule

The actual `thebrazenbeard/num-ta-reen` author's 30-utterance corpus and 500-word dictionary are **not** synthetic data. Its 27 eligible leave-one-out author-IGT probes achieved 112/127 correct morphemes, 2 wrong and 13 abstained (source-verified; only 26 training utterances per fold); 15 correct factorized morphemes were unseen as whole tokens. These independent Num’ta’reen measurements were reproduced with `python -m research.heldout_morpheme_probe --repo-root <num-repo>`. The five-token generated experiment is **not** Num’ta’reen syntax, language canon, phonology or communication. No dictionary, corpus, or translation output in that repository was modified.

An actual integration should wait for a common typed JSONL interface and show **better** author-heldout morpheme/semantic accuracy without target-IGT leakage, scope confusion, or loss of abstention. SemanticAtlas and Semiotics are candidate *interfaces*, not assumed accuracy improvements. Future author-only contrastive tests should target agent/patient inversion, scope of negation, question focus, and new morphological combinations; do not score invented Num’ta’reen answers before author approval.

## Qualification backlog

1. Fit/test a variable-length learner against official SCAN's fixed add-primitive split, document exact zero-shot results against train-only phrasebook/copy and at least one real method; freezing split is mandatory.
2. Evaluate novel grammar rules and variable word order separately. The current positional model will not generalize them, and this must remain visible.
3. Acquire permitted natural-language reference data (FLORES/updated fork), add human blinded bilingual evaluation and versioned BLEU/chrF++, including adequacy failures.
4. Prove strict filesystem/process custody (restricted access to evaluator gold and model data) rather than confusing separate processes with a sandbox.
5. Obtain an independent architecture/security/linguistics review and qualify specific integrations only when scored improvement exceeds controls.

No new native ChatGPT subagents are attested for this session; local assistant/tool orchestration and any later external LLM review are separate evidence classes.
