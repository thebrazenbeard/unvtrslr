# MASSIVE paired-source-text translation diagnostic — 2026-10-26

**Qualification:** `DIAGNOSTIC_ONLY_NOT_SEMANTIC_QUALIFICATION`.
This run tests text-to-text prediction without gold intent, slot labels, or
correct target sentences in the source-only prediction request.

## Provenance and split

- Canonical upstream corpus: Amazon MASSIVE 1.0, 39,500,415-byte archive, SHA-256
  `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`.
  Archive was freshly read and validated against the frozen version.
- Four independent target locale slices, English `en-US` source into `fr-FR`,
  `de-DE`, `sw-KE`, `tr-TR`. Language editions are aligned by published
  content ID and checked against consistent partition and intent *privately
  during reference construction*.
- The same 200 test content IDs selected using
  `SHA256("en-US:"+id)` are held out in all four target languages. All
  sources are actual corpus utterances, not synthetic sine waves.
- Each `requests_en_to_<locale>.jsonl` contains only:
  `id`, `source_language`, `target_language`, `source_text`.
  Gold target utterances never appear in exported prompts. The evaluator
  retains targets separately in memory.
- This is source-text-only evaluation, **not a proven external host isolation
  boundary**. A system independently given the full MASSIVE test set could
  memorize it. Published training overlap and unknown upstream model training
  contamination remain separate concerns.
- Source and target sentences refer to the same annotation/content ID, but
  can be natural language paraphrases rather than exact word-by-word
  equivalents. Exact match is a demanding diagnostic, **not** a calibrated
  human translation quality score.

## Actual results, 200 held-out items per language

| Control | Train exposure | Total predictions | Coverage | Exact target matches |
| --- | --- | ---: | ---: | ---: |
| Exact parallel phrasebook | 0%, 1%, or 10% | 0 / 800 | 0% | 0 / 800 |
| Exact parallel phrasebook | 100% | 4 / 800 | 0.5% | 1 / 800 |
| Echo English source | No training required | 800 / 800 | 100% | 4 / 800 |

The exact phrasebook uses only paired **train** utterances and abstains on
unseen source strings or conflicting target strings. Its sole exact hit
occurred for German. The echo baseline demonstrates that 100% coverage
does not imply valid translation; even four identical strings appear among
the 800 parallel target references.

**Raw report:** `blind_text_report.json` SHA-256
`bacc1945922a03d4bc172028842619685e9a8fb0965cf75ba2c7f7dba9723d84`
for the first run including 16 phrasebook slices and four echo slices.
The complete generated report and request files stay in an isolated Lappy
scratch folder, not the git repository. The exact dataset and source
reconstruct them.

## External translation engine handoff

Supply results for each language as an UTF-8 JSONL file named
`predictions_en_to_fr-FR.jsonl` (similarly `de-DE`, `sw-KE`, `tr-TR`)
under a local `--predictions-dir`. Every source record requires exactly
one result:

```json
{"id":"123","status":"OK","text":"translated words here"}
{"id":"456","status":"ABSTAIN","text":null}
```

The accepted statuses are `OK`, `ABSTAIN`, and `ERROR`. Anything
else—missing/duplicate/unknown records, status/text contradictions,
extra keys, overlong candidates—fails closed. The evaluator calculates
coverage, exact target match and normalized token edit similarity from
its private references. It does not interpret output as grounded meaning.

For smoke-testing the external file interface, an independent local process
converted the published requests to English-echo predictions (200 results per
target). Reimporting all four files reproduced the echo-control coverage
and exact-match values. **That was not a LibreTranslate or LLM run.**

```powershell
$env:PYTHONPATH = "$PWD\src;$PWD"
python -m pytest -q tests/test_massive_blindtext.py
python -m runs.massive_v1_first_real_corpus_20260922.blind_text --dataset-tar "path/to/pinned-MASSIVE-1.0.tar.gz" --out "scratch/output"
python -m runs.massive_v1_first_real_corpus_20260922.blind_text --dataset-tar "path/to/pinned-MASSIVE-1.0.tar.gz" --out "scratch/evaluated" --predictions-dir "scratch/engine-output"
```

## Next qualification gate

Run an actual independent, pinned translation model (LibreTranslate/Argos
or another known-language baseline) **without exposing evaluation references
or intent metadata**. Record model identity, licenses, output hashes, latency
and resource budgets. Then test domain shift, unseen words, related-language
transfer, truly unfamiliar languages, and Num'ta'reen resonance in their
own separate regimes. No known-language machine translator alone proves
unknown-language acquisition.
