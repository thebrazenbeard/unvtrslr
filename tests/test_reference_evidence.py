"""Synthetic fixtures only: never load external/proprietary language data."""

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from itertools import repeat

from unvtrslr.reference_evidence import (
    CLAIM_CEILING,
    MAX_LINE_BYTES,
    MAX_RECORDS,
    ReferenceEvidenceError,
    parse_reference_evidence,
    parse_reference_envelope_json,
    parse_reference_evidence_json,
    read_reference_evidence_jsonl,
)


def fixture():
    return {
        "schema": "unvtrslr-reference-evidence-v1",
        "origin": {
            "repo": "example/lab-fixtures",
            "commit": "a" * 40,
            "source_group": "one-author-test-group",
            "source_document": "Synthetic exercise C",
            "source_sha256": "B" * 64,
            "record_id": "synthetic-17",
        },
        "direction": "lab-en",
        "evidence_class": "AUTHOR_ATTESTED_CORPUS",
        "source_text": "⟦β 𐐀⟧",
        "target_text": "Control panel indicator active.",
        "alternatives": [],
        "register": None,
        "taboo": None,
        "semantic_atoms": None,
        "qualification_eligible": False,
        "learner_visible": False,
        "source_independence": "SINGLE_AUTHOR_REFERENCE",
        "withheld": False,
        "warnings": [],
    }


class ReferenceEvidenceTests(unittest.TestCase):
    def test_attested_is_not_semantic_qualification(self):
        row = parse_reference_evidence(fixture())
        self.assertEqual(row.evidence_class, "AUTHOR_ATTESTED_CORPUS")
        self.assertEqual(row.claim_ceiling, CLAIM_CEILING)
        self.assertIs(row.qualification_eligible, False)
        self.assertIsNone(row.semantic_atoms)
        self.assertIn("𐐀", row.source_text)
        self.assertEqual(row.target_text, "Control panel indicator active.")

    def test_lexical_alternatives_are_never_fluent_targets(self):
        row = fixture()
        row.update(evidence_class="AUTHOR_LEXICON_GLOSS", target_text=None,
                   alternatives=[{"kind": "lexeme", "token": "s1", "value": "marker",
                                  "headword": "s1", "gloss": "marker", "source_line": 11},
                                 {"kind": "lexeme", "token": "s2", "value": "indicator",
                                  "headword": "s2", "gloss": "indicator", "source_line": 12}])
        result = parse_reference_evidence(row)
        self.assertIsNone(result.target_text)
        self.assertEqual(result.alternatives[0]["gloss"], "marker")

    def test_validated_alternatives_are_deeply_immutable_and_unaliased(self):
        row = fixture()
        row.update(evidence_class="AUTHOR_LEXICON_GLOSS", target_text=None,
                   alternatives=[{"kind": "lexeme", "token": "s1", "value": "marker",
                                  "headword": "s1", "gloss": "marker", "source_line": 1},
                                 {"kind": "lexical_segmentation", "token": "s2=x",
                                  "segmentation": [{"headword": "s2", "gloss": "indicator",
                                                    "source_line": 2}], "value": None,
                                  "note": "Source-only segmentation"}])
        parsed = parse_reference_evidence(row)
        row["alternatives"][0]["gloss"] = "tampered by caller"
        row["alternatives"][1]["segmentation"][0]["gloss"] = "tampered nested"
        self.assertEqual(parsed.alternatives[0]["gloss"], "marker")
        self.assertEqual(parsed.alternatives[1]["segmentation"][0]["gloss"], "indicator")
        with self.assertRaises(TypeError):
            parsed.alternatives[0]["gloss"] = "tampered after parse"
        with self.assertRaises(TypeError):
            parsed.alternatives[1]["segmentation"][0]["gloss"] = "tampered nested after parse"

    def test_unknown_has_no_implicit_answer(self):
        row = fixture()
        row.update(evidence_class="UNKNOWN", target_text=None)
        self.assertIsNone(parse_reference_evidence(row).target_text)

    def test_mixed_known_and_unknown_preserves_partial_without_fluency(self):
        row = fixture()
        row.update(evidence_class="AUTHOR_PARTIAL_LEXICAL", target_text=None,
                   alternatives=[{"kind": "lexeme", "token": "sample", "value": "known",
                                  "headword": "sample", "gloss": "known", "source_line": 7}],
                   warnings=["UNKNOWN_SEGMENTS_PRESENT"])
        result = parse_reference_evidence(row)
        self.assertIsNone(result.target_text)
        self.assertEqual(result.evidence_class, "AUTHOR_PARTIAL_LEXICAL")

    def test_lexical_claim_requires_identifying_fields_and_source_line(self):
        base = fixture()
        base.update(evidence_class="AUTHOR_LEXICON_GLOSS", target_text=None)
        good = {"kind": "lexeme", "token": "s1", "value": "marker",
                "headword": "s1", "gloss": "marker", "source_line": 7}
        for missing in ("token", "value", "headword", "gloss", "source_line"):
            with self.subTest(missing=missing):
                row = dict(base, alternatives=[{key: val for key, val in good.items() if key != missing}])
                with self.assertRaisesRegex(ReferenceEvidenceError, "lexeme must include"):
                    parse_reference_evidence(row)
        row = dict(base, alternatives=[{"kind": "lexeme"}])
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)

    def test_reject_fabricated_grounding_and_extra_fields(self):
        for key, value in [("qualification_eligible", True), ("semantic_atoms", ["ctx:active"]),
                           ("claim_ceiling", "GROUNDED")]:
            with self.subTest(key=key):
                row = fixture()
                row[key] = value
                with self.assertRaises(ReferenceEvidenceError):
                    parse_reference_evidence(row)

    def test_reject_nonattested_fluent_text(self):
        row = fixture()
        row["evidence_class"] = "AUTHOR_LEXICON_GLOSS"
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)

    def test_reject_unknown_alternatives(self):
        row = fixture()
        row.update(evidence_class="UNKNOWN", target_text=None, alternatives=[{"gloss": "guess"}])
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)

    def test_reject_duplicate_json_keys(self):
        data = json.dumps(fixture())
        altered = data.replace('"schema":', '"schema": "bogus", "schema":', 1)
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence_json(altered)

    def test_reject_invalid_utf8_and_unbounded_text(self):
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence_json(b"\xff")
        row = fixture()
        row["source_text"] = "x" * 4097
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)

    def test_json_entrypoints_reject_lone_surrogates_as_reference_errors(self):
        # Malformed Python str inputs must fail closed just like invalid UTF-8
        # bytes, not leak a raw UnicodeEncodeError from the byte cap check.
        for parse in (parse_reference_evidence_json, parse_reference_envelope_json):
            for value in ("\ud800", "\udfff", "{}\ud800"):
                with self.subTest(parser=parse.__name__, value=repr(value)):
                    with self.assertRaisesRegex(ReferenceEvidenceError, "UTF-8"):
                        parse(value)
        with self.assertRaisesRegex(ReferenceEvidenceError, "line 2"):
            read_reference_evidence_jsonl([json.dumps(fixture()), "\ud800"])

    def test_escaped_surrogates_cannot_survive_validated_reference_fields(self):
        # json.dumps emits ASCII '\\ud800'. Input byte decoding therefore
        # succeeds; the validator must reject the invalid Unicode scalar
        # after JSON decoding, including inside nested provenance.
        bad = chr(0xD800)
        for path in (
            ("source_text",), ("target_text",), ("register",), ("taboo",),
            ("origin", "source_group"), ("origin", "source_document"),
            ("origin", "record_id"), ("warnings", 0),
        ):
            with self.subTest(path=path):
                row = fixture()
                if path == ("warnings", 0):
                    row["warnings"] = [bad]
                elif len(path) == 1:
                    row[path[0]] = bad
                else:
                    row[path[0]][path[1]] = bad
                with self.assertRaisesRegex(ReferenceEvidenceError, "Unicode scalar"):
                    parse_reference_evidence_json(json.dumps(row).encode("ascii"))

        lexeme = {"kind": "lexeme", "token": "s1", "value": "marker",
                  "headword": "s1", "gloss": "marker", "source_line": 11}
        for key in ("token", "value", "headword", "gloss", "category", "ipa"):
            with self.subTest(lexeme=key):
                row = fixture()
                row.update(evidence_class="AUTHOR_LEXICON_GLOSS", target_text=None,
                           alternatives=[dict(lexeme, **{key: bad})])
                with self.assertRaisesRegex(ReferenceEvidenceError, "Unicode scalar"):
                    parse_reference_evidence_json(json.dumps(row))

        row = fixture()
        row.update(evidence_class="AUTHOR_LEXICON_GLOSS", target_text=None,
                   alternatives=[{"kind": "lexical_segmentation", "token": "s1=x",
                                  "note": bad, "value": None,
                                  "segmentation": [{"headword": "s1",
                                                    "gloss": "marker",
                                                    "source_line": 11}]}])
        with self.assertRaisesRegex(ReferenceEvidenceError, "Unicode scalar"):
            parse_reference_evidence_json(json.dumps(row))

        for envelope in (
            {"ok": True, "request_id": bad, "record": fixture()},
            {"ok": False, "request_id": bad,
             "error": {"code": "INVALID_REQUEST", "message": "synthetic"}},
            {"ok": False, "request_id": "synthetic",
             "error": {"code": "INVALID_REQUEST", "message": bad}},
        ):
            with self.subTest(envelope=envelope["ok"], request_id=repr(envelope["request_id"])):
                with self.assertRaisesRegex(ReferenceEvidenceError, "Unicode scalar"):
                    parse_reference_envelope_json(json.dumps(envelope).encode("ascii"))

    def test_json_entrypoints_keep_valid_unicode_and_existing_byte_bounds(self):
        good_record = json.dumps(fixture(), ensure_ascii=False)
        good_envelope = json.dumps({"ok": True, "request_id": "synthetic",
                                    "record": fixture()}, ensure_ascii=False)
        self.assertIn("𐐀", parse_reference_evidence_json(good_record).source_text)
        self.assertIn("𐐀", parse_reference_envelope_json(good_envelope).record.source_text)
        for parse in (parse_reference_evidence_json, parse_reference_envelope_json):
            with self.subTest(parser=parse.__name__, case="bad utf8"):
                with self.assertRaisesRegex(ReferenceEvidenceError, "UTF-8"):
                    parse(b"\xff")
            with self.subTest(parser=parse.__name__, case="byte cap"):
                with self.assertRaisesRegex(ReferenceEvidenceError, "exceeds byte limit"):
                    parse(" " * (MAX_LINE_BYTES + 1))

    def test_reject_absolute_origin_source_repo_and_bad_commit(self):
        row = fixture()
        row["origin"]["repo"] = "../../private"
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)
        row = fixture()
        row["origin"]["commit"] = "not-an-immutable-sha"
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)

    def test_origin_repo_rejects_dot_path_components(self):
        for repo in ("../unsafe", "owner/..", "./repo", "owner/."):
            with self.subTest(repo=repo):
                row = fixture()
                row["origin"]["repo"] = repo
                with self.assertRaisesRegex(ReferenceEvidenceError, "origin repo must be owner/name"):
                    parse_reference_evidence(row)
        for repo in ("owner-name/repo.name", "owner_name/repo-name"):
            with self.subTest(repo=repo):
                row = fixture()
                row["origin"]["repo"] = repo
                self.assertEqual(parse_reference_evidence(row).origin_repo, repo)

    def test_jsonl_records_are_bounded_source_authored_objects(self):
        row = json.dumps(fixture(), ensure_ascii=False)
        parsed = read_reference_evidence_jsonl(["\n", row + "\n"])
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0].record_id, "synthetic-17")

    def test_jsonl_line_errors_report_position(self):
        with self.assertRaisesRegex(ReferenceEvidenceError, "line 2"):
            read_reference_evidence_jsonl([json.dumps(fixture()), "not-json"])

    def test_excessively_nested_json_is_a_bounded_validation_error(self):
        # Under the byte cap but beyond the decoder's recursion budget.
        # A malformed external reference must never crash the validator.
        deeply_nested = "[" * 12000 + "0" + "]" * 12000
        self.assertLess(len(deeply_nested.encode("utf-8")), 65536)
        with self.assertRaisesRegex(ReferenceEvidenceError, "invalid reference JSON"):
            parse_reference_evidence_json(deeply_nested)
        with self.assertRaisesRegex(ReferenceEvidenceError, "invalid reference envelope JSON"):
            parse_reference_envelope_json(deeply_nested)

        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
        result = subprocess.run(
            [sys.executable, "-m", "unvtrslr.reference_evidence_cli"],
            input=deeply_nested + "\n",
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid reference envelope JSON", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_reference_jsonl_has_aggregate_record_limit(self):
        row = json.dumps(fixture(), ensure_ascii=False) + "\n"
        with self.assertRaisesRegex(ReferenceEvidenceError, "record count exceeds limit"):
            read_reference_evidence_jsonl(repeat(row, MAX_RECORDS + 1))

    def test_success_and_error_envelopes_are_distinct(self):
        good = {"ok": True, "request_id": "one", "record": fixture()}
        parsed = parse_reference_envelope_json(json.dumps(good, ensure_ascii=False))
        self.assertIsNotNone(parsed.record)
        self.assertIsNone(parsed.error_code)
        error = {"ok": False, "request_id": "two", "error": {
            "code": "BAD_REQUEST", "message": "Unusable input"}}
        failed = parse_reference_envelope_json(json.dumps(error))
        self.assertIsNone(failed.record)
        self.assertEqual(failed.error_code, "BAD_REQUEST")

    def test_cli_reports_only_aggregate_without_echoing_content(self):
        env = os.environ.copy()
        source_dir = str(Path(__file__).resolve().parents[1] / "src")
        env["PYTHONPATH"] = source_dir + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            [sys.executable, "-m", "unvtrslr.reference_evidence_cli"],
            input=json.dumps({"ok": True, "request_id": "one", "record": fixture()},
                             ensure_ascii=False) + "\n",
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["validated_records"], 1)
        self.assertIs(summary["qualification_eligible"], False)
        self.assertNotIn("Control panel", result.stdout)
        self.assertNotIn("𐐀", result.stdout)

    def test_cli_rejects_failed_producer_envelope(self):
        env = os.environ.copy()
        source_dir = str(Path(__file__).resolve().parents[1] / "src")
        env["PYTHONPATH"] = source_dir + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(
            [sys.executable, "-m", "unvtrslr.reference_evidence_cli"],
            input=json.dumps({"ok": False, "request_id": None,
                              "error": {"code": "BAD_REQUEST", "message": "private failure detail"}}) + "\n",
            text=True, capture_output=True, env=env, check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["error_envelopes"], 1)
        self.assertNotIn("private failure detail", result.stdout)

    def test_withheld_record_never_exposes_source_or_target(self):
        row = fixture()
        row.update(source_text=None, target_text=None, withheld=True, warnings=["NONVOCAL_REFERENCE"])
        result = parse_reference_evidence(row)
        self.assertTrue(result.withheld)
        self.assertIsNone(result.source_text)
        self.assertIsNone(result.target_text)
        row["target_text"] = "should not emerge"
        with self.assertRaises(ReferenceEvidenceError):
            parse_reference_evidence(row)

    def test_reference_cannot_forge_independent_speaker(self):
        for key, value in [("source_independence", "INDEPENDENT_SPEAKERS"),
                           ("learner_visible", True), ("source_id", "synthetic-other-speaker")]:
            with self.subTest(key=key):
                row = fixture()
                row[key] = value
                with self.assertRaises(ReferenceEvidenceError):
                    parse_reference_evidence(row)

    def test_source_sha_case_is_not_rewritten(self):
        row = fixture()
        result = parse_reference_evidence(row)
        self.assertEqual(result.source_sha256, "B" * 64)


if __name__ == "__main__":
    unittest.main()
