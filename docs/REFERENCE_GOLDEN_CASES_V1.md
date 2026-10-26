# Synthetic reference-evidence golden cases

Status: `PUBLIC_WIRE_FIXTURE / SINGLE_AUTHOR_ONLY / NO_SEMANTIC_CREDIT`

`tests/fixtures/reference_evidence_golden.jsonl` is a small, intentionally
fabricated provider stream for the `reference_evidence-v1` receiver. It does
**not** contain Num’ta’reen vocabulary, author corpus, a resonance codebook,
or an attested alien utterance. `example/synthetic-reference` and its all-`a`
commit ID are fixture identities, **not independently verified provenance**.

The golden stream covers three distinct cases:

1. An author-attested *synthetic* sample containing NFC `é`, a glottal-stop
   character, and a supplementary-plane character.
2. An NFD `e` plus combining-acute lexical gloss. The receiver must preserve
   its original bytes/Unicode scalar sequence, **not normalize it to case 1**;
   a lexical gloss never becomes a fluent target sentence.
3. A withheld synthetic placeholder with no source text, target text, or
   alternatives. No display or signal material may be inferred from it.

Run the contract checks in a checkout of the public translator:

```sh
PYTHONPATH=src python -m unittest discover -s tests -p 'test_reference_golden_contract.py' -v
PYTHONPATH=src python -m unvtrslr.reference_evidence_cli < tests/fixtures/reference_evidence_golden.jsonl
```

The second command should exit zero and report three validated references,
one each in `AUTHOR_ATTESTED_CORPUS`, `AUTHOR_LEXICON_GLOSS`, and `UNKNOWN`,
with `qualification_eligible:false`. It reports aggregates only, without
reprinting reference text.

## Windows / provider boundary

The actual Num’ta’reen producer is an **opt-in separate process** in its
private repository (`python -m numtareen.interop`). Its request accepts
`direction`, `text` or Base64-encoded UTF-8 `text_base64`, and `unknown`; its
response carries the same V1 envelope. The Num’ta’reen PowerShell translator
is separately documented in that repository. These golden fixtures qualify
neither its Windows launcher nor the live cross-process producer, because the
private data source and Windows hosts are not present in this public test.

Source/reference separation is mandatory: do not feed author reference rows
to causal discovery episodes, bridge training, or semantic qualification.
