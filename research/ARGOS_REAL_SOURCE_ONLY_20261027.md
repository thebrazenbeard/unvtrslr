# Offline Argos source-only MASSIVE 1.0 benchmark — 2026-10-27

**Evidence class:** real Lappy neural CPU inference, source-only request boundary, privately sealed evaluation. **Claim:** DIAGNOSTIC_ONLY_NOT_SEMANTIC_QUALIFICATION. Event `linguistics_live_coordination`.

## Source and model provenance

- UNVTRSLR baseline: `main@bd8176371b1eaf1bd4c2f76494959a3c0b5f5576`, Git tree `a569cf8103dee0f3df4632f93e5ed1038e3c2c1e`.
- Amazon MASSIVE 1.0 archived bytes 39,500,415; SHA-256 `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`. Source: `https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.0.tar.gz`.
- Argos Translate **1.11.0** installed in separate Python 3.11 venv. Wheel SHA-256 `a89b42d82f40843900338f9ac60d4c82fda590b6898247f5d0c15d46731ca7df` (downloaded and independently hashed on Lappy). Argos git tag ref `v1.11.0 = 7a13fbc509f28c5987d032ad7708b709dd0ddd7e`, package index main observed `ff90de60728f7c1338ff6b75974e4c89b2442d22`.
- Exact transitive Python dependency versions: `research/ARGOS_PY311_LOCK_20261027.txt`.
- Offline direct packages from the official Argos package index (not pivots):

| Pair | Argos package version | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| en→fr | 1.9 | 65,472,327 | `3a65ed83364f4e7b06e30f9dd823db1934899ed3ce839e63f46dc7b09dc797b4` |
| en→de | 1.3 | 150,508,297 | `6cd847f0c06c9c66013e6b0932e07fd54a6d90894659c02bf6c5247b72fb25b1` |
| en→sw | 1.11 | 75,782,172 | `994bf9e19f00dd1566ad59e95879a7ea24de19f7b4fc89ab0dcce860580353f2` |
| en→tr | 1.5 | 124,742,526 | `2d553a00880a0c21dea5b1c375535659e6bf18c9bf2ce9847c2a2fd2ff50316a` |

Model URLs, required sizes, identities and hashes are machine-readable in `research/ARGOS_MODEL_LOCK_20261027.json`. Model archives passed hash and metadata checks *before* installation; vendor signatures and end-to-end supply-chain signatures were not established. No model binaries are to be committed.

## Frozen benchmark results (real independent source-only process)

The inference worker was supplied only `{id, source_language, target_language, source_text}` for the same 200 frozen published-test IDs per target. It was not passed target texts, intents, or slots as request fields. The worker still ran under the Lappy user's OS access rights; this is a process-level input discipline, **not** filesystem isolation or proof against reading other accessible files. The result JSONL was separately passed to `blind_text.py` using `--predictions-dir`. Source-only process is not an OS-enforced secrecy proof; training-corpus overlap with upstream Argos remains unmeasured.

| Target | Predicted / 200 | Exact | Token similarity | SacreBLEU | chrF++ |
| --- | --- | ---: | ---: | ---: | ---: |
| French | 200 | 6.5% | 49.86% | 37.16 | 59.65 |
| German | 200 | 0.5% | 23.96% | 12.38 | 43.12 |
| Swahili | 200 | 0% | 25.45% | 13.85 | 39.24 |
| Turkish | 200 | 1% | 25.53% | 10.53 | 40.34 |

No inference errors, 800 / 800 predictions. BLEU signature: `nrefs:1|case:mixed|eff:yes|tok:13a|smooth:exp|version:2.5.1`; chrF++: `nrefs:1|case:mixed|eff:yes|nc:6|nw:2|space:no|version:2.5.1`. These diagnostics compare to one published reference, not an adequacy judgment. The earlier train-only phrasebook (<=10% coverage zero; 100% train exposure 4 predictions/800, one match) and source-copy control (800 predictions, four exact reference matches) remain negative controls. Earlier UNVTRSLR oracle-intent target-construction scores are a distinct, **not source-only** task. It has no complete native comparable text-source translation model at this baseline.

A visible failure example: MASSIVE ID `3785`, source `turn off the bathroom light please`. The target Swahili reference is `zima taa ya bafu tafadhali`, while this Argos package generated `Download mchezo Mwanga wa jua tafadhali`. This is an obvious content mismatch, not an unknown-language success. By contrast German output `Bitte das Badezimmerlicht ausschalten` is semantically plausible despite differing from the published German reference `bitte ausmachen vom badezimmer licht`.

## Runtime and repeatability

Host Lappy Windows, Intel i5-11400H 6 cores / 12 threads, 31.73 GiB RAM. CPU-only `ARGOS_DEVICE_TYPE=cpu`, `ARGOS_CHUNK_TYPE=MINISBD`, `ARGOS_INTER_THREADS=1`, `ARGOS_INTRA_THREADS=4`. Benchmarks were sequential target batches, 200 requests each, not concurrency/streaming. First-per-target latency includes lazy initialization and is **not full process cold start**. Process peak working-set is cumulative, not per-model isolated.

| Target | Run 1 p50/p95 warm ms | Run 1 requests/sec | Run 2 p50/p95 warm ms | Run 2 peak working set MiB |
| --- | --- | ---: | --- | ---: |
| fr | 42.46 / 93.70 | 20.18 | 44.88 / 88.65 | 403.74 |
| de | 45.64 / 110.89 | 18.09 | 44.57 / 93.94 | 689.66 |
| sw | 31.78 / 74.71 | 17.36 | 30.20 / 63.47 | 703.20 |
| tr | 32.78 / 86.03 | 19.45 | 32.24 / 77.53 | 850.36 |

**Repeatability:** independent process invocation twice, each 800/800 OK and every per-language prediction file SHA-256 identical:

- fr: `3d2dc8ae73c39320addddfa0f4d2392a4ec0d15c2c48fe06216351d927dffb1c`
- de: `f42419d68d8c79be168e91d55572a1a90b62f0a4245c2860e1503719725c2dd3`
- sw: `49ccda3669c77a28311e942fbef57f7b29ab665a4836cabdd1ba2283926f1c43`
- tr: `977c16f2e12a2cb4a8b43b6893d9f083508948da208544d2a2384462e22e5654`

Original raw predictions, archived models, corpus, performance receipts and scored reports remain in isolated Lappy scratch `C:\Temp\bt2-unvtrslr-20261027-one\_run` / `_models`, **not in Git**. This document and scripts are source-controlled reconstruction instructions, not raw model binary redistribution.

## Reconstruction (PowerShell, checkout as working directory)

1. Create Python 3.11 venv, install from pinned `research/ARGOS_PY311_LOCK_20261027.txt` and verify Argos version. Download the MASSIVE archive and four model URLs named in the lock, then verify SHA-256 and size.
2. Set `ARGOS_PACKAGES_DIR`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_CONFIG_HOME` to fresh, private folders; set `ARGOS_DEVICE_TYPE=cpu`, `ARGOS_CHUNK_TYPE=MINISBD`, `ARGOS_INTER_THREADS=1`, `ARGOS_INTRA_THREADS=4`, `PYTHONIOENCODING=utf-8`.
3. Run `python runs/massive_v1_first_real_corpus_20260922/argos_install_locked.py --lock research/ARGOS_MODEL_LOCK_20261027.json --download-dir <model-archives>`. Install fails closed on missing/changed/unsafe models.
4. Set `PYTHONPATH=src;.`, then run `python -m runs.massive_v1_first_real_corpus_20260922.blind_text --dataset-tar <archive> --out <sealed>`. Copy ONLY the four `requests_en_to_*.jsonl` files to a standalone input folder, outside the evaluator directory. Where an OS sandbox/ACL is separately available, deny worker access to `<sealed>` and the archive; this Lappy test did **not** demonstrate that OS isolation.
5. Invoke `python runs/massive_v1_first_real_corpus_20260922/argos_source_only.py --requests-dir <source-only> --predictions-dir <fresh-empty-predictions> --model-dir <model-archives> --lock research/ARGOS_MODEL_LOCK_20261027.json`. The worker rejects missing/extra input-directory entries, overlapping input/model/output paths, nonempty output directories and incomplete translation runs. `--limit` is only for diagnostics; a partial run is **not** an 800-item benchmark.
6. In a **separate post-inference evaluator process**, score `python -m runs.massive_v1_first_real_corpus_20260922.blind_text --dataset-tar <archive> --out <evaluation> --predictions-dir <predictions>`. Optional `argos_quality_metrics.py` with `--dataset-tar`, `--predictions-dir`, `--out` computes BLEU/chrF++ using separately installed SacreBLEU.
7. Run `python -m pytest -q tests`; verify the sample response IDs, prediction SHA values and per-language score ranges above. Keep thresholds unchanged.

## Limitations and threat model

The source-only adapter rejects unknown language, wrong language pair, missing/extra fields, duplicate source IDs, excessive lengths, duplicate JSON keys, nonfinite input, missing record counts, contaminated request directories, path overlap, stale destination files, partial successful inference and incomplete model-lock declarations. The companion BLEU/chrF evaluator now reuses the bounded untrusted-JSONL import validator rather than reading raw predictions without size and record limits. External evaluator import now rejects oversized files, extra records, duplicates and nonfinite JSON before private scoring; caller must use unmodified published heldout IDs. Argos model archive validation checks ZIP traversal, duplicate names, archive expansion cap and symlink entries, but installing third-party ONNX/CTranslate2 models still executes a trusted translation runtime: **not an OS sandbox**.

There is no calibrated confidence estimate, COMET, human semantic judgment, cross-host replication, streaming benchmark, unknown-language translation success, CPU utilization trace, GPU qualification, or independently observed developer subagent dispatch in this session. A different run/host/Argos release must be classified separately. No integration into VeraOS, Num'ta’reen canon changes, or backend state writes took place.

## Hardening regression round (same frozen subjects, 2026-10-27)

Source-only input directory now requires **exactly four** request JSONL files and rejects unexpected entries, symlinks, output/model overlap and any nonempty output destination to prevent stale predictions being reused. Every attempted sentence in a benchmark run must succeed, or the worker fails instead of reporting a misleading partial success. The model lock requires exactly four direct language packages, a pinned engine wheel and MASSIVE source digest; ZIP validation additionally rejects Windows-drive member paths. The optional BLEU evaluator now uses the same bounded JSONL reader as the built-in evaluator. These are *process-input protections*, not an OS sandbox or proof of model/corpus separation under shared Windows user permissions.

A complete additional Lappy CPU execution from `C:\Temp\bt2-argos-input-stage-20261027\requests` made **800/800** actual predictions with the four request files in a standalone directory; its four prediction SHA-256 values matched the first two runs exactly. Both separate post-inference scoring paths reproduced the same exact-match, token-similarity, BLEU and chrF++ results. All execution effects remained local until source-only PR publication. Independent external reviewer approval and formal host isolation are still unqualified.
