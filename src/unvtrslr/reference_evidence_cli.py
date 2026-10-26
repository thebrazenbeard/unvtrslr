"""Offline JSONL contract validator, emitting only non-sensitive aggregates."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import sys

from .reference_evidence import (
    CLAIM_CEILING,
    MAX_RECORDS,
    ReferenceEvidenceError,
    parse_reference_envelope_json,
    parse_reference_evidence_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate external author-reference JSONL; never grant semantic credit")
    parser.add_argument("--bare", action="store_true", help="validate pure evidence objects rather than transport envelopes")
    args = parser.parse_args(argv)
    counts: Counter[str] = Counter()
    error_envelopes = 0
    seen = 0
    try:
        for line_number, line in enumerate(sys.stdin.buffer, start=1):
            if not line.strip():
                continue
            seen += 1
            if seen > MAX_RECORDS:
                raise ReferenceEvidenceError("record-count limit exceeded")
            try:
                if args.bare:
                    record = parse_reference_evidence_json(line)
                else:
                    envelope = parse_reference_envelope_json(line)
                    record = envelope.record
                    if record is None:
                        error_envelopes += 1
                        continue
                counts[record.evidence_class] += 1
            except ReferenceEvidenceError as exc:
                raise ReferenceEvidenceError(f"JSONL line {line_number}: {exc}") from exc
    except ReferenceEvidenceError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "REFERENCE_VALIDATION_COMPLETE_NOT_GROUNDED",
        "claim_ceiling": CLAIM_CEILING,
        "validated_records": sum(counts.values()),
        "error_envelopes": error_envelopes,
        "evidence_classes": dict(sorted(counts.items())),
        "qualification_eligible": False,
    }, sort_keys=True))
    return 1 if error_envelopes else 0


if __name__ == "__main__":
    raise SystemExit(main())
