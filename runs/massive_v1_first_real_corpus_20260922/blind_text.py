"""Sealed-reference multilingual TEXT stress; no gold intent/slot labels at inference.

MASSIVE utterances share content IDs across language editions. The evaluator
controls test targets; only source text, language pair and ID reach predictors.
This is not automatically a blind pretrained-model holdout, nor a language
acquisition claim. External translation responses are explicitly untrusted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from io import BytesIO
import json
from pathlib import Path
import tarfile
import unicodedata

from unvtrslr.archive_integrity import load_verified_archive
from unvtrslr.multilingual_qualification import _levenshtein
from runs.massive_v1_first_real_corpus_20260922.run import (
    DATASET_BYTES, DATASET_SHA256, LOCALES, canonical_tokens,
    read_locale_rows, stable_holdout_key, write_json, write_jsonl,
)

EXPOSURE_PERCENTS = (0, 1, 10, 100)
TARGET_LOCALES = ("fr-FR", "de-DE", "sw-KE", "tr-TR")
CLAIM_CEILING = "SOURCE_TEXT_ONLY_MASSIVE_PAIRED_TRANSLATION_DIAGNOSTIC"


def _index(rows: list[dict], locale: str, partition: str) -> dict[str, dict]:
    if not rows:
        raise ValueError("cannot align empty parallel partition")
    output: dict[str, dict] = {}
    for row in rows:
        if row.get("partition") != partition:
            raise ValueError("partition mismatch")
        if row.get("locale") != locale:
            raise ValueError("locale mismatch")
        raw = row.get("id")
        if type(raw) not in (str, int) or not str(raw):
            raise ValueError("invalid record id")
        key = str(raw)
        if key in output:
            raise ValueError("duplicate record id")
        if type(row.get("utt")) is not str or not row["utt"].strip():
            raise ValueError("empty corpus utterance")
        output[key] = row
    return output


def make_parallel_pairs(
    source_rows: list[dict], target_rows: list[dict],
    source_locale: str, target_locale: str, partition: str,
) -> list[dict]:
    if source_locale == target_locale or source_locale not in LOCALES or target_locale not in LOCALES:
        raise ValueError("unsupported or same-language pair")
    if partition not in ("train", "test"):
        raise ValueError("unsupported partition")
    src = _index(source_rows, source_locale, partition)
    tgt = _index(target_rows, target_locale, partition)
    if src.keys() != tgt.keys():
        raise ValueError("parallel corpus has unaligned content IDs")
    result = []
    for rid, row in src.items():
        if row.get("intent") != tgt[rid].get("intent"):
            raise ValueError("intent mismatch in parallel corpus alignment")
        result.append({
            "id": rid,
            "source_language": source_locale.split("-", 1)[0],
            "target_language": target_locale.split("-", 1)[0],
            "source_text": row["utt"],
            "target_text": tgt[rid]["utt"],
        })
    return result


def public_requests(pairs: list[dict]) -> list[dict]:
    """Immutable view boundary: no gold target, intent, slots, or worker ID."""
    return [{
        "id": pair["id"],
        "source_language": pair["source_language"],
        "target_language": pair["target_language"],
        "source_text": pair["source_text"],
    } for pair in pairs]


def select_pairs(pairs: list[dict], source_locale: str, percent: int) -> list[dict]:
    if type(percent) is not int or percent not in EXPOSURE_PERCENTS:
        raise ValueError("unsupported exposure percent")
    if source_locale not in LOCALES:
        raise ValueError("unsupported source language")
    ids = [p["id"] for p in pairs]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate pair ID")
    ordered = sorted(ids, key=lambda i: (stable_holdout_key(source_locale, str(i)), str(i)))
    selected = set(ordered[:len(ordered) * percent // 100])
    return [p for p in pairs if p["id"] in selected]


def _normalized(text: str) -> str:
    return unicodedata.normalize("NFC", text).strip()


def fit_exact_phrasebook(training: list[dict]) -> dict[tuple[str, str, str], str | None]:
    """Negative control, not a translator: ambiguity forces abstention."""
    lexicon: dict[tuple[str, str, str], str | None] = {}
    for pair in training:
        key = (pair["source_language"], pair["target_language"], _normalized(pair["source_text"]))
        target = _normalized(pair["target_text"])
        if key not in lexicon:
            lexicon[key] = target
        elif lexicon[key] != target:
            lexicon[key] = None
    return lexicon


def predict_phrasebook(
    requests: list[dict], lexicon: dict[tuple[str, str, str], str | None],
) -> list[dict]:
    output = []
    for row in requests:
        if set(row) != {"id", "source_language", "target_language", "source_text"}:
            raise ValueError("request must be source-only")
        key = (row["source_language"], row["target_language"], _normalized(row["source_text"]))
        text = lexicon.get(key)
        output.append({
            "id": row["id"], "status": "OK" if text is not None else "ABSTAIN",
            "text": text,
        })
    return output


def predict_copy_control(requests: list[dict]) -> list[dict]:
    """Hostile negative control: copying source has 100% coverage, little fidelity."""
    return [
        {"id": row["id"], "status": "OK", "text": row["source_text"]}
        for row in requests
    ]


def score_predictions(pairs: list[dict], predictions: list[dict]) -> dict:
    """Evaluator-private target comparison; fail closed on inconsistent outputs."""
    if not pairs or len({row["id"] for row in pairs}) != len(pairs):
        raise ValueError("nonempty uniquely identified paired test data required")
    expected = {row["id"]: row for row in pairs}
    got: dict[str, dict] = {}
    for row in predictions:
        if type(row) is not dict or set(row) != {"id", "status", "text"}:
            raise ValueError("prediction schema mismatch")
        rid = row["id"]
        if type(rid) is not str or rid not in expected or rid in got:
            raise ValueError("duplicate or unknown predicted record ID")
        status, text = row["status"], row["text"]
        if status not in ("OK", "ABSTAIN", "ERROR"):
            raise ValueError("invalid prediction status")
        if status == "OK":
            if type(text) is not str or not text.strip() or len(text) > 8192:
                raise ValueError("OK requires bounded nonempty translation")
            if len(canonical_tokens(text)) > 256:
                raise ValueError("OK translation token count exceeds bound")
        elif text is not None:
            raise ValueError("abstain/error cannot supply candidate text")
        got[rid] = row
    if got.keys() != expected.keys():
        raise ValueError("incomplete prediction set")
    exact, covered, similarity = 0, 0, 0.0
    statuses: Counter[str] = Counter()
    for rid, pair in expected.items():
        prediction = got[rid]
        statuses[prediction["status"]] += 1
        if prediction["status"] != "OK":
            continue
        covered += 1
        candidate = canonical_tokens(_normalized(prediction["text"]))
        reference = canonical_tokens(_normalized(pair["target_text"]))
        exact += int(candidate == reference)
        denominator = max(1, len(candidate), len(reference))
        similarity += 1.0 - _levenshtein(candidate, reference) / denominator
    n = len(pairs)
    return {
        "status": "DIAGNOSTIC_ONLY_NOT_SEMANTIC_QUALIFICATION",
        "records": n,
        "coverage": covered / n,
        "exact_match": exact / n,
        "token_similarity": similarity / n,
        "abstentions": statuses["ABSTAIN"],
        "errors": statuses["ERROR"],
        "status_counts": dict(sorted(statuses.items())),
    }


def _external_json_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key in external prediction")
        result[key] = value
    return result


def load_external_predictions(path: Path, *, expected_count: int = 200) -> list[dict]:
    """Bound untrusted JSONL size, structure and count before scoring."""
    if type(expected_count) is not int or not 1 <= expected_count <= 200:
        raise ValueError("bad expected record count")
    if not path.is_file() or path.stat().st_size > 4_000_000:
        raise ValueError("oversized or missing predictions file")
    predictions = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if len(line.encode("utf-8")) > 32768 or not line.strip():
                raise ValueError("oversized or blank prediction line")
            if len(predictions) >= expected_count:
                raise ValueError("too many prediction records")
            row = json.loads(
                line, object_pairs_hook=_external_json_object,
                parse_constant=lambda _value: (_ for _ in ()).throw(
                    ValueError("nonfinite JSON prediction")
                ),
            )
            predictions.append(row)
    if len(predictions) != expected_count:
        raise ValueError("incomplete prediction records")
    return predictions


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-tar", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--predictions-dir",
                        help="optional offline JSONL predictions per target; no network calls")
    args = parser.parse_args()
    data, digest = load_verified_archive(
        Path(args.dataset_tar), expected_sha256=DATASET_SHA256, expected_bytes=DATASET_BYTES
    )
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    # Reconstruct all references from a pinned archive, never from model output.
    results = []
    with tarfile.open(fileobj=BytesIO(data), mode="r:gz") as tar:
        rows = {lang: read_locale_rows(tar, lang) for lang in ("en-US", *TARGET_LOCALES)}
    for target in TARGET_LOCALES:
        source_train = [r for r in rows["en-US"] if r["partition"] == "train"]
        source_test = [r for r in rows["en-US"] if r["partition"] == "test"]
        target_train = [r for r in rows[target] if r["partition"] == "train"]
        target_test = [r for r in rows[target] if r["partition"] == "test"]
        train = make_parallel_pairs(source_train, target_train, "en-US", target, "train")
        test_all = make_parallel_pairs(source_test, target_test, "en-US", target, "test")
        by_id = {p["id"]: p for p in test_all}
        holdout_ids = [
            r["id"] for r in sorted(source_test, key=lambda row: stable_holdout_key("en-US", str(row["id"])))[:200]
        ]
        holdout = [by_id[str(i)] for i in holdout_ids]
        if len(train) != 11514 or len(holdout) != 200:
            raise ValueError("unexpected MASSIVE split size")
        if {x["id"] for x in train} & {x["id"] for x in holdout}:
            raise ValueError("train/holdout ID overlap")
        req_path = output / f"requests_en_to_{target}.jsonl"
        source_only = public_requests(holdout)
        write_jsonl(req_path, source_only)
        # 100% coverage by itself is meaningless: a copy-the-input system is
        # scored without any target hints as a required hostile control.
        copied = score_predictions(holdout, predict_copy_control(source_only))
        results.append({"target_locale": target, "engine": "COPY_SOURCE_NEGATIVE_CONTROL", **copied})
        for percent in EXPOSURE_PERCENTS:
            learned = fit_exact_phrasebook(select_pairs(train, "en-US", percent))
            result = score_predictions(holdout, predict_phrasebook(public_requests(holdout), learned))
            results.append({"target_locale": target, "exposure_percent": percent,
                            "engine": "TRAIN_ONLY_EXACT_PHRASEBOOK_CONTROL", **result})
        if args.predictions_dir:
            prediction_file = Path(args.predictions_dir) / f"predictions_en_to_{target}.jsonl"
            predictions = load_external_predictions(prediction_file, expected_count=len(holdout))
            external = score_predictions(holdout, predictions)
            results.append({"target_locale": target, "engine": "EXTERNALLY_SUPPLIED_NOT_ATTESTED", **external})
    write_json(output / "blind_text_report.json", {
        "schema": "MASSIVE_PAIRED_TEXT_EVALUATION_V1",
        "claim_ceiling": CLAIM_CEILING,
        "dataset_sha256": digest,
        "test_records_per_target": 200,
        "gold_labels_visible_to_inference": False,
        "reference_text_visible_to_inference": False,
        "holdout_description": "published test content IDs, same 200 for every target",
        "results": results,
    })
    for row in results:
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
