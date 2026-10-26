"""Quarantined, source-authored reference evidence from external language tools.

This is a transport/validation boundary, *not* a grounded semantic learner.
Author-attested text and lexical glosses never become BridgeLearner episodes,
target-grounding episodes, or qualification observations by parsing them.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from types import MappingProxyType
from typing import Iterable, Mapping


SCHEMA = "unvtrslr-reference-evidence-v1"
CLAIM_CEILING = "AUTHOR_SUPPLIED_REFERENCE_ONLY_NOT_GROUNDED"
MAX_LINE_BYTES = 65_536
MAX_TEXT_CHARS = 4096
MAX_RECORDS = 10_000
_TOP_KEYS = frozenset({
    "schema", "origin", "direction", "evidence_class", "source_text",
    "target_text", "alternatives", "semantic_atoms", "qualification_eligible",
    "warnings", "register", "taboo", "source_independence", "learner_visible",
    "withheld",
})
_ORIGIN_KEYS = frozenset({
    "repo", "commit", "source_group", "source_document", "source_sha256", "record_id",
})
_CLASSES = frozenset({
    "AUTHOR_ATTESTED_CORPUS", "AUTHOR_LEXICON_GLOSS", "AUTHOR_PARTIAL_LEXICAL", "UNKNOWN",
})
_LEXEME_KEYS = frozenset({
    "kind", "token", "value", "headword", "gloss", "category",
    "register", "taboo", "ipa", "source_line", "note",
})
_SEGMENT_KEYS = frozenset({"kind", "token", "segmentation", "value", "note"})
_CORPUS_KEYS = frozenset({"kind", "record_id", "value"})
_LEXEME_REQUIRED = frozenset({"kind", "token", "value", "headword", "gloss", "source_line"})
_SEGMENT_LEXEME_REQUIRED = frozenset({"headword", "gloss", "source_line"})
_DIRECTION = re.compile(r"[a-z][a-z0-9-]*-[a-z][a-z0-9-]*\Z")
_REPO = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
_COMMIT = re.compile(r"[0-9a-f]{40}\Z")


class ReferenceEvidenceError(ValueError):
    """Malformed reference data, or an attempt to cross its evidence boundary."""


@dataclass(frozen=True)
class ReferenceEvidence:
    origin_repo: str
    origin_commit: str
    source_group: str
    source_document: str | None
    source_sha256: str | None
    record_id: str | None
    direction: str
    evidence_class: str
    source_text: str | None
    target_text: str | None
    alternatives: tuple[Mapping[str, object], ...]
    register: str | None
    taboo: str | None
    withheld: bool
    warnings: tuple[str, ...]
    schema: str = SCHEMA
    claim_ceiling: str = CLAIM_CEILING
    qualification_eligible: bool = False
    learner_visible: bool = False
    source_independence: str = "SINGLE_AUTHOR_REFERENCE"
    semantic_atoms: None = None


def _exact_keys(value: object, expected: frozenset[str], name: str) -> Mapping[str, object]:
    if not isinstance(value, dict) or set(value) != expected:
        raise ReferenceEvidenceError(f"{name} must have exactly the V1 fields")
    return value


def _string(value: object, name: str, *, maximum: int = MAX_TEXT_CHARS) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ReferenceEvidenceError(f"{name} must be a nonempty bounded string")
    # The parser does not normalize/strip: every source form is preserved.
    return value


def _nullable_string(value: object, name: str, *, maximum: int = 512) -> str | None:
    return None if value is None else _string(value, name, maximum=maximum)


def _strings(value: object, name: str, *, maximum: int) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) > maximum:
        raise ReferenceEvidenceError(f"{name} must be a bounded string list")
    return tuple(_string(item, f"{name} item") for item in value)


def _freeze_provenance(value: object) -> object:
    """Detach validated nested evidence from caller-owned mutable JSON data.

    A frozen outer dataclass is insufficient when alternatives contain dicts
    and lists: post-validation mutation must not rewrite the evidence snapshot.
    """
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze_provenance(member)
                                 for key, member in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_provenance(member) for member in value)
    return value


def _alternatives(value: object) -> tuple[Mapping[str, object], ...]:
    if not isinstance(value, list) or len(value) > 64:
        raise ReferenceEvidenceError("alternatives must be a bounded list of provenance objects")
    checked = []
    for alternative in value:
        if not isinstance(alternative, dict) or not alternative:
            raise ReferenceEvidenceError("unsupported alternative provenance fields")
        kind = alternative.get("kind")
        if kind == "lexeme" and set(alternative) <= _LEXEME_KEYS:
            _validate_lexeme(alternative, required=_LEXEME_REQUIRED)
        elif kind == "lexical_segmentation" and set(alternative) == _SEGMENT_KEYS:
            _string(alternative["token"], "segmentation token")
            _string(alternative["note"], "segmentation note")
            if alternative["value"] is not None:
                raise ReferenceEvidenceError("segmentation cannot claim fluent target value")
            segments = alternative["segmentation"]
            if not isinstance(segments, list) or not 1 <= len(segments) <= 16:
                raise ReferenceEvidenceError("segmentation must be a bounded lexeme list")
            for segment in segments:
                if not isinstance(segment, dict) or not set(segment) <= _LEXEME_KEYS:
                    raise ReferenceEvidenceError("malformed segmentation lexeme")
                if segment.get("kind") not in (None, "lexeme"):
                    raise ReferenceEvidenceError("segmentation may contain lexemes only")
                _validate_lexeme(segment, required=_SEGMENT_LEXEME_REQUIRED)
        elif kind == "corpus" and set(alternative) == _CORPUS_KEYS:
            _string(alternative["record_id"], "corpus record ID")
            _string(alternative["value"], "corpus candidate value")
        else:
            raise ReferenceEvidenceError("unsupported alternative provenance fields")
        checked.append(_freeze_provenance(alternative))
    return tuple(checked)


def _validate_lexeme(lexeme: Mapping[str, object], *, required: frozenset[str]) -> None:
    if not required <= lexeme.keys():
        raise ReferenceEvidenceError("lexeme must include identifying text and source_line")
    for key, member in lexeme.items():
        if key == "source_line":
            if type(member) is not int or member < 1:
                raise ReferenceEvidenceError("source_line must be a positive integer")
        elif key == "kind":
            if member != "lexeme":
                raise ReferenceEvidenceError("unsupported lexeme kind")
        elif key in required:
            _string(member, f"lexeme {key}")
        elif member is not None:
            _string(member, f"lexeme {key}")


def parse_reference_evidence(value: object) -> ReferenceEvidence:
    """Accept a tightly bounded source-authored fixture, never semantic credit.

    No file paths are dereferenced. `source_document` is inert metadata.
    """
    entry = _exact_keys(value, _TOP_KEYS, "reference record")
    if entry["schema"] != SCHEMA:
        raise ReferenceEvidenceError("unsupported reference schema")
    if (entry["qualification_eligible"] is not False
            or entry["semantic_atoms"] is not None
            or entry["learner_visible"] is not False
            or entry["source_independence"] != "SINGLE_AUTHOR_REFERENCE"):
        raise ReferenceEvidenceError("author-supplied references cannot claim grounded qualification")
    origin = _exact_keys(entry["origin"], _ORIGIN_KEYS, "origin")
    repo = _string(origin["repo"], "origin repo", maximum=256)
    if not _REPO.fullmatch(repo):
        raise ReferenceEvidenceError("origin repo must be owner/name")
    commit = _string(origin["commit"], "origin commit", maximum=40)
    if not _COMMIT.fullmatch(commit):
        raise ReferenceEvidenceError("origin commit must be a lowercase 40-character SHA")
    source_group = _string(origin["source_group"], "source_group", maximum=256)
    source_sha256 = _nullable_string(origin["source_sha256"], "source_sha256", maximum=64)
    if source_sha256 is not None and not re.fullmatch(r"[0-9A-Fa-f]{64}", source_sha256):
        raise ReferenceEvidenceError("source_sha256 must be a 64-character hex digest")
    direction = _string(entry["direction"], "direction", maximum=48)
    if not _DIRECTION.fullmatch(direction):
        raise ReferenceEvidenceError("direction must be a pair of language identifiers")
    grade = entry["evidence_class"]
    if not isinstance(grade, str) or grade not in _CLASSES:
        raise ReferenceEvidenceError("unsupported evidence_class")
    source = _nullable_string(entry["source_text"], "source_text", maximum=MAX_TEXT_CHARS)
    target = _nullable_string(entry["target_text"], "target_text", maximum=MAX_TEXT_CHARS)
    alternatives = _alternatives(entry["alternatives"])
    warnings = _strings(entry["warnings"], "warnings", maximum=32)
    withheld = entry["withheld"]
    if type(withheld) is not bool:
        raise ReferenceEvidenceError("withheld must be a boolean")
    if withheld and (source is not None or target is not None or alternatives or not warnings):
        raise ReferenceEvidenceError("withheld reference must not expose source, target, alternatives")
    if not withheld and source is None:
        raise ReferenceEvidenceError("source_text is required unless withheld")
    if grade == "AUTHOR_ATTESTED_CORPUS" and not withheld and target is None and not alternatives:
        raise ReferenceEvidenceError("attested reference requires target or alternatives")
    if grade != "AUTHOR_ATTESTED_CORPUS" and target is not None:
        raise ReferenceEvidenceError("non-attested references cannot assert a fluent target")
    if grade == "AUTHOR_PARTIAL_LEXICAL" and (not alternatives or not warnings):
        raise ReferenceEvidenceError("partial lexical evidence needs candidates and explicit warning")
    if grade == "UNKNOWN" and alternatives:
        raise ReferenceEvidenceError("unknown reference cannot assert alternatives")
    return ReferenceEvidence(
        origin_repo=repo,
        origin_commit=commit,
        source_group=source_group,
        source_document=_nullable_string(origin["source_document"], "source_document"),
        source_sha256=source_sha256,
        record_id=_nullable_string(origin["record_id"], "record_id"),
        direction=direction,
        evidence_class=grade,
        source_text=source,
        target_text=target,
        alternatives=alternatives,
        register=_nullable_string(entry["register"], "register"),
        taboo=_nullable_string(entry["taboo"], "taboo"),
        withheld=withheld,
        warnings=warnings,
    )


def _no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, member in pairs:
        if key in value:
            raise ReferenceEvidenceError("duplicate JSON member")
        value[key] = member
    return value


def _reject_constant(value: str) -> None:
    raise ReferenceEvidenceError(f"non-JSON numeric constant: {value}")


def parse_reference_evidence_json(line: str | bytes) -> ReferenceEvidence:
    if isinstance(line, bytes):
        try:
            line = line.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ReferenceEvidenceError("reference must be UTF-8") from exc
    if not isinstance(line, str) or len(line.encode("utf-8")) > MAX_LINE_BYTES:
        raise ReferenceEvidenceError("reference line exceeds byte limit")
    try:
        obj = json.loads(line, object_pairs_hook=_no_duplicate_keys, parse_constant=_reject_constant)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ReferenceEvidenceError("invalid reference JSON") from exc
    return parse_reference_evidence(obj)


def read_reference_evidence_jsonl(lines: Iterable[str | bytes]) -> tuple[ReferenceEvidence, ...]:
    rows = []
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if len(rows) >= MAX_RECORDS:
            raise ReferenceEvidenceError("reference JSONL record count exceeds limit")
        try:
            rows.append(parse_reference_evidence_json(line))
        except ReferenceEvidenceError as exc:
            raise ReferenceEvidenceError(f"reference JSONL line {number}: {exc}") from exc
    return tuple(rows)


@dataclass(frozen=True)
class ReferenceEnvelope:
    """Transport framing only; errors do not become reference observations."""

    request_id: str | None
    record: ReferenceEvidence | None
    error_code: str | None


def parse_reference_envelope(value: object) -> ReferenceEnvelope:
    if not isinstance(value, dict) or type(value.get("ok")) is not bool:
        raise ReferenceEvidenceError("reference envelope requires boolean ok")
    request_id = _nullable_string(value.get("request_id"), "request_id", maximum=128)
    if value["ok"]:
        if set(value) != {"ok", "request_id", "record"}:
            raise ReferenceEvidenceError("successful envelope has unexpected fields")
        return ReferenceEnvelope(request_id, parse_reference_evidence(value["record"]), None)
    if set(value) != {"ok", "request_id", "error"}:
        raise ReferenceEvidenceError("error envelope has unexpected fields")
    error = _exact_keys(value["error"], frozenset({"code", "message"}), "error")
    code = _string(error["code"], "error code", maximum=80)
    _string(error["message"], "error message", maximum=1000)
    if not re.fullmatch(r"[A-Z][A-Z0-9_]*", code):
        raise ReferenceEvidenceError("error code must be an identifier")
    return ReferenceEnvelope(request_id, None, code)


def parse_reference_envelope_json(line: str | bytes) -> ReferenceEnvelope:
    if isinstance(line, bytes):
        try:
            line = line.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ReferenceEvidenceError("reference envelope must be UTF-8") from exc
    if not isinstance(line, str) or len(line.encode("utf-8")) > MAX_LINE_BYTES:
        raise ReferenceEvidenceError("reference envelope line exceeds byte limit")
    try:
        obj = json.loads(line, object_pairs_hook=_no_duplicate_keys, parse_constant=_reject_constant)
    except (ValueError, TypeError, RecursionError) as exc:
        raise ReferenceEvidenceError("invalid reference envelope JSON") from exc
    return parse_reference_envelope(obj)
