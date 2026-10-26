"""Public synthetic golden wire cases, never private Num'ta'reen corpus.

These cases qualify UTF-8 framing and reference-evidence provenance only,
not phonology, natural-language translation, or acoustic meaning.
"""

from pathlib import Path
import json
import os
import subprocess
import sys
import unicodedata
import unittest

from unvtrslr.reference_evidence import (
    CLAIM_CEILING,
    parse_reference_envelope_json,
)


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "reference_evidence_golden.jsonl"


class GoldenReferenceBoundaryTests(unittest.TestCase):
    def test_utf8_unicode_forms_and_withheld_reference_are_not_promoted(self):
        records = [parse_reference_envelope_json(line).record
                   for line in FIXTURE.read_bytes().splitlines()]
        self.assertEqual(len(records), 3)
        nfc, nfd, withheld = records
        self.assertEqual(nfc.source_text, "é ʔ 𐐀")
        self.assertEqual(nfd.source_text, "e\N{COMBINING ACUTE ACCENT} ʔ 𐐀")
        self.assertNotEqual(nfc.source_text, nfd.source_text)
        self.assertEqual(unicodedata.normalize("NFC", nfc.source_text),
                         unicodedata.normalize("NFC", nfd.source_text))
        self.assertEqual(nfd.evidence_class, "AUTHOR_LEXICON_GLOSS")
        self.assertIsNone(nfd.target_text)
        self.assertEqual(nfd.alternatives[0]["token"], "e\N{COMBINING ACUTE ACCENT}")
        self.assertTrue(withheld.withheld)
        self.assertIsNone(withheld.source_text)
        self.assertIsNone(withheld.target_text)
        for record in records:
            self.assertEqual(record.claim_ceiling, CLAIM_CEILING)
            self.assertEqual(record.source_independence, "SINGLE_AUTHOR_REFERENCE")
            self.assertIs(record.qualification_eligible, False)
            self.assertIs(record.learner_visible, False)
            self.assertIsNone(record.semantic_atoms)

    def test_cli_accepts_exact_utf8_jsonl_and_emits_no_reference_text(self):
        env = os.environ.copy()
        source_dir = str(Path(__file__).resolve().parents[1] / "src")
        env["PYTHONPATH"] = source_dir + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            [sys.executable, "-m", "unvtrslr.reference_evidence_cli"],
            input=FIXTURE.read_bytes(),
            capture_output=True,
            env=env,
            timeout=10,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, b"")
        summary = json.loads(result.stdout)
        self.assertEqual(summary["validated_records"], 3)
        self.assertEqual(summary["evidence_classes"], {
            "AUTHOR_ATTESTED_CORPUS": 1,
            "AUTHOR_LEXICON_GLOSS": 1,
            "UNKNOWN": 1,
        })
        self.assertIs(summary["qualification_eligible"], False)
        self.assertNotIn("é".encode("utf-8"), result.stdout)
        self.assertNotIn("marker".encode("utf-8"), result.stdout)


if __name__ == "__main__":
    unittest.main()
