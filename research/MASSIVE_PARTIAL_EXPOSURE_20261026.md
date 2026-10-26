# MASSIVE 1.0 Partial-Exposure Stress, 2026-10-26

**Result:** `MULTILINGUAL_HOLDOUT_THRESHOLD_NOT_MET` at **every** exposure level.
**Claim ceiling:** `SUPERVISED_MASSIVE_PARTIAL_EXPOSURE_TARGET_CONSTRUCTION_NOT_TRANSLATION`.

## Empirical subject and provenance

- Run code: `runs/massive_v1_first_real_corpus_20260922/partial_exposure.py`.
- Evaluator and target-construction code from the exact current UNVTRSLR source branch.
- Public dataset: Amazon MASSIVE 1.0, `39,500,415` compressed bytes; SHA-256 `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`; freshly downloaded from the official URL and hash checked before parsing.
- Training: published `train` partition, 11,514 utterances per language at 100%; strict nested subsets at 1% (115) and 10% (1,151), chosen by SHA-256 on (locale, record ID); 0% explicit no-model abstention. 100% preserves upstream training order.
- Evaluation: 200 fixed published `test` utterances per language, the same deterministic SHA-256 holdout as the earlier baseline. Evaluation remains held-out at all exposure levels.
- Locales: `en-US`, `fr-FR`, `de-DE`, `sw-KE`, `tr-TR`. Exactly 1,000 held-out evaluations per level.
- Model: the existing UNVTRSLR `TargetConstructionEpisode` / `fit_target_construction_model` / `render_semantic_sequence` implementation; minimum two source/worker identities per accepted target construction. No imported code or models from the four proposed external projects.
- Frozen qualification thresholds: coverage >= 0.10; exact-match >= 0.05; token similarity >= 0.10; ambiguity <= 0.25, in every 200-item language slice. The thresholds were not lowered after observing failures.
- Computed JSON report on Lappy: SHA-256 `5bb6c71ff6b3c27e274c3ecabd85b27a1eed48ab7e6d32384f5225015f3196a2`, 18,004 bytes. Generated report kept outside the source tree; source plus dataset hash reconstructs it. No dataset/model artifacts committed.

## Real-corpus results

| Exposure | Train rows per language | Macro coverage | Macro exact match | Macro token similarity | Qualification |
|---|---:|---:|---:|---:|---|
| 0% | 0 | 0% | 0% | 0% | no training; abstain |
| 1% | 115 | 0% | 0% | 0% | fail |
| 10% | 1,151 | 0.4% | 0.1% | 0.24% | fail |
| 100% | 11,514 | 29.3% | 1.0% | 7.2349% | fail |

At 10%, English and German provided no eligible outputs; French and Swahili had 0.5% coverage, Turkish had 1%. One exact-match example occurred in Swahili. At 100%, the results reproduce the prior repository's published **29.3% coverage / 1% exact match** and its five per-locale slices.

Zero exposure deliberately skips a qualification API that rejects empty training: it reports `NO_TRAINING_EXPOSURE`, no candidates, and no possibility of a PASS. For every other level, the existing holdout evaluator checks source/record leakage and scores successful renderings; no overlap violations were reported.

## What this does NOT show

This is **not** direct unknown-language translation. The system receives the held-out reference's *gold intent and ordered slot-type annotations* as its source-side semantic input. The experiment measures how well it can construct target-side text from that privileged representation. A real translator must additionally infer that representation from raw text or speech without oracle metadata.

The 0/1/10/100 comparison tests training scarcity **within known MASSIVE locales**, not truly unseen language families, speaker noise, discourse, novel grammatical systems, Num’ta’reen semantics, or multiword productive grammar. Those need separate frozen evaluations.

## External reference repositories (reviewed, not integrated)

| Project | Potential role | Boundaries |
|---|---|---|
| [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) | Conventional, self-hosted Argos text-translation baseline on permitted known-language pairs | AGPL-3.0; benchmark through an isolated API rather than copy code; needs installed supported language packages |
| [NextAI Translator](https://github.com/nextai-translator/nextai-translator) | Human-facing streaming text translation and TTS UX comparisons | LLM/API-dependent configuration, AGPL-3.0 per GitHub; not a ground-truth semantic oracle |
| [Babel Fish speech-to-speech](https://github.com/ibro45/Speech-to-Speech-Translator) | Historical language-ID -> Google STT/translation/TTS pipeline reference | Only Croatian, French, Spanish in its README; cloud dependence; GPL-3.0; last published push in 2020 |
| [Real-Time Speech Translator](https://github.com/TobyM-engineering/Real-Time-Speech-Translator) | Bounded audio buffering, watchdog, wearable IO reference | Real-time OpenAI cloud API dependency; Raspberry Pi hardware assumptions; MIT |

No audio benchmark, cross-model performance comparison, code copy, license determination for a combined distribution, or installed service is claimed. The next meaningful engineering advance is **slot/value-compositional target realization with frozen novel recombinations**, then a separate real speech-to-text-to-target translation benchmark against a local text baseline.

## Repeat locally

```powershell
$env:PYTHONPATH = "$PWD\src;$PWD"
python -m pytest -q tests/test_massive_partial_exposure.py
python -m runs.massive_v1_first_real_corpus_20260922.partial_exposure --dataset-tar <the-verified-MASSIVE-archive.tar.gz> --out <isolated-output-dir>
```

Run requires the exact pinned archive bytes. It does not download automatically.
