# External reference-evidence boundary V1

Status: `PUBLIC_GENERIC_CONTRACT / AUTHOR_REFERENCE_ONLY / NO_GROUNDING_CREDIT`

This receiver accepts a language provider's source-authored translation or
lexical lookup as **reference evidence**. It does not discover an unknown
language, calibrate its signal channel, or learn a semantic correspondence.
Grounded evidence and author-supplied strings are distinct classes.

## JSONL transport

One complete UTF-8 JSON object per line, using
`schema: "unvtrslr-reference-evidence-v1"`. Every record has exactly:

```json
{
  "schema": "unvtrslr-reference-evidence-v1",
  "origin": {
    "repo": "example/lab-fixtures",
    "commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "source_group": "single-test-author",
    "source_document": "Synthetic exercise C",
    "source_sha256": "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
    "record_id": "synthetic-17"
  },
  "direction": "lab-en",
  "evidence_class": "AUTHOR_ATTESTED_CORPUS",
  "source_text": "[test indicator]",
  "target_text": "Control panel indicator active.",
  "alternatives": [],
  "register": null,
  "taboo": null,
  "semantic_atoms": null,
  "qualification_eligible": false,
  "learner_visible": false,
  "source_independence": "SINGLE_AUTHOR_REFERENCE",
  "withheld": false,
  "warnings": []
}
```

This is a **synthetic interoperability fixture**, not an attested utterance.
The `repo` + 40-character `commit` + `source_document` + `record_id` and
optional original-case `source_sha256` identify **claimed** lineage and must
be independently checked against the named sources if authenticity matters.
A content hash is not a proof of authorship, source independence, or permission.
`source_group` is inert author-supplied metadata, **not** a counted independent
speaker. Every row must explicitly identify
`source_independence: "SINGLE_AUTHOR_REFERENCE"`.

Evidence class is one of:

- `AUTHOR_ATTESTED_CORPUS`: `target_text` is a literal recorded translation
  for a unique attested match, or null with typed `corpus` alternatives when
  multiple attested matches remain. This is an attestation **by the author**,
  not independently grounded meaning.
- `AUTHOR_LEXICON_GLOSS`: `target_text` must be null. Candidate lexical glosses
  may appear in typed `lexeme` or `lexical_segmentation` provenance objects;
  none is a fluent sentence or grammatical parse.
- `AUTHOR_PARTIAL_LEXICAL`: some lexical matches exist but unknown tokens
  remain; candidate alternatives and an explicit warning are both required.
- `UNKNOWN`: `target_text` null, `alternatives` empty.

Where a source contains non-vocalizable or protected signal material, the
provider sets `withheld:true`, omits **both** `source_text` and `target_text`,
supplies no alternatives, and records the reason in `warnings`. Ordinary
non-withheld records require source text. A withheld reference cannot silently
become an emission-ready target.

`semantic_atoms` must be null; `qualification_eligible:false`,
`learner_visible:false` and `source_independence:"SINGLE_AUTHOR_REFERENCE"`
are mandatory. The receiver independently enforces those values and assigns
the claim ceiling `AUTHOR_SUPPLIED_REFERENCE_ONLY_NOT_GROUNDED`.

Consumers call `parse_reference_evidence_json`, `parse_reference_evidence`, or
`read_reference_evidence_jsonl` from `unvtrslr.reference_evidence`. Live
producer envelopes are `{ "ok":true, "request_id":string|null, "record":<evidence> }`
or `{ "ok":false, "request_id":string|null, "error":{ "code":string, "message":string } }`.
`parse_reference_envelope_json` checks the envelope and rejects confusing an
error with a successful evidence record. These entry points
validate bounded data in memory and never dereference paths or execute source
content. Source text is preserved byte-for-byte after UTF-8 decoding; the
receiver does not normalize accents or punctuation. Display clients must
handle terminal-control escaping separately.

The command `python -m unvtrslr.reference_evidence_cli` validates envelope
JSONL from stdin and prints only aggregated evidence-class counts; `--bare`
accepts pure records. A malformed record exits 2, producer error envelopes
yield exit 1, and all-valid records exit 0. The report never quotes or writes
raw reference content. Inputs are capped at 64 KiB per record and 10,000
records per invocation.

## Forbidden promotion

Do **not** convert these rows directly into `BridgeLearner` observation
episodes, `TargetGroundingEpisode`, `TargetConstructionEpisode`, an R2 positive
control, or real-corpus qualification. That would give the learner the bridge
from a human-authored bilingual corpus and then credit it with discovering
the bridge. Grounding must use separately collected observation and
intervention evidence with frozen splits, independent speakers/sources where
applicable, causal probes, and documented non-equivalence tests.

Private or rights-restricted language corpora and lexical data should remain
private. The public receiver and its tests contain only synthetic fixtures;
no provider dataset, utterance, or lexicon is vendored here.

## Unverified beyond this boundary

This contract establishes only loss-aware transport and validation of
author-supplied source/reference distinctions. It does not prove correctness
of the provider's labels or any semantic fit between continuous acoustic
signals and discrete target orthography. A future governed signal layer must
bind resonance features and claimed meaning to independent observations.
