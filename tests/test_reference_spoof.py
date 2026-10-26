"""Hostile synthetic checks for the author-reference/learned-evidence boundary.

This test deliberately does not import Num'ta'reen sources or corpus data.
It is meant to be staged in the public UNVTRSLR test suite once its
reference_evidence-v1 contract is finalized.
"""

from copy import deepcopy
import unittest

from unvtrslr.reference_evidence import (
    ReferenceEvidenceError,
    parse_reference_evidence,
)


def synthetic_reference() -> dict:
    return {
        "schema": "unvtrslr-reference-evidence-v1",
        "origin": {
            "repo": "example/synthetic-author-data",
            "commit": "a" * 40,
            "source_document": "Synthetic experiment A",
            "record_id": "synthetic-001",
            "source_group": "example/synthetic-author-data",
            "source_sha256": None,
        },
        "direction": "lab-en",
        "evidence_class": "AUTHOR_ATTESTED_CORPUS",
        "source_text": "[s:x s:y]",
        "target_text": "A synthetic sample.",
        "alternatives": [],
        "semantic_atoms": None,
        "qualification_eligible": False,
        "learner_visible": False,
        "source_independence": "SINGLE_AUTHOR_REFERENCE",
        "register": None,
        "taboo": None,
        "withheld": False,
        "warnings": [],
    }


class SourceIdentitySpoofTests(unittest.TestCase):
    def test_single_author_records_cannot_claim_independent_semantic_evidence(self):
        # Different row IDs do not constitute independent observational sources.
        left = synthetic_reference()
        right = deepcopy(left)
        right["origin"]["record_id"] = "synthetic-002"
        for row in (left, right):
            result = parse_reference_evidence(row)
            self.assertEqual(result.source_independence, "SINGLE_AUTHOR_REFERENCE")
            self.assertIs(result.qualification_eligible, False)
            self.assertIs(result.learner_visible, False)
            self.assertIsNone(result.semantic_atoms)

    def test_false_qualification_and_learner_visibility_rejected(self):
        for key, forged in (
            ("qualification_eligible", True),
            ("learner_visible", True),
            ("source_independence", "INDEPENDENT_OBSERVATIONS"),
            ("semantic_atoms", ["ctx:red"]),
        ):
            with self.subTest(key=key):
                row = synthetic_reference()
                row[key] = forged
                with self.assertRaises(ReferenceEvidenceError):
                    parse_reference_evidence(row)

    def test_forged_source_group_cannot_promote_claim(self):
        # The parser cannot authenticate source_group; callers must not use
        # distinct metadata labels as evidence of independent collection.
        left = synthetic_reference()
        right = deepcopy(left)
        right["origin"]["source_group"] = "invented-second-lab"
        for row in (left, right):
            result = parse_reference_evidence(row)
            self.assertEqual(result.claim_ceiling, "AUTHOR_SUPPLIED_REFERENCE_ONLY_NOT_GROUNDED")
            self.assertIs(result.qualification_eligible, False)
            self.assertEqual(result.source_independence, "SINGLE_AUTHOR_REFERENCE")

    def test_alias_and_language_spoof_fields_not_accepted(self):
        for key, forged in (
            ("source_id", "fake-independent-lab"),
            ("target_language_id", "fictional-language"),
            ("grounded", True),
        ):
            with self.subTest(key=key):
                row = synthetic_reference()
                row[key] = forged
                with self.assertRaises(ReferenceEvidenceError):
                    parse_reference_evidence(row)


if __name__ == "__main__":
    unittest.main()
