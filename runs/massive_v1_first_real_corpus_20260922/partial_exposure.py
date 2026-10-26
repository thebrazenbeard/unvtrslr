"""Frozen exposure-fraction stress against the existing MASSIVE 1.0 adapter.

This measures supervised target construction conditioned on gold intent/slots.
It does NOT demonstrate translation from unknown input or grounded semantics.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from io import BytesIO
import json
from pathlib import Path
import tarfile

from unvtrslr.archive_integrity import load_verified_archive
from unvtrslr.target_constructions import (
    TargetConstructionEpisode,
    fit_target_construction_model,
    render_semantic_sequence,
)
from unvtrslr.multilingual_qualification import (
    EvaluationRecord, QualificationThresholds, TrainingExposure,
    evaluate_multilingual_holdout,
)
from runs.massive_v1_first_real_corpus_20260922.run import (
    DATASET_SHA256, DATASET_BYTES, LOCALES, MODEL_LINEAGE, ADAPTER_ID,
    canonical_tokens, read_locale_rows, semantic_pattern, stable_holdout_key,
    write_json, write_jsonl,
)

EXPOSURE_PERCENTS = (0, 1, 10, 100)
PROFILE_CLAIM = "SUPERVISED_MASSIVE_PARTIAL_EXPOSURE_TARGET_CONSTRUCTION_NOT_TRANSLATION"
THRESHOLDS = QualificationThresholds(
    min_corpora=1, min_languages=5, min_records_per_slice=200,
    min_coverage=.10, min_exact_match=.05, min_token_similarity=.10,
    max_ambiguity_rate=.25,
)


def _validate_rows(rows: list[dict], locale: str, partition: str) -> None:
    ids: set[str] = set()
    for row in rows:
        if row.get("partition") != partition:
            raise ValueError(f"expected {partition} partition")
        if row.get("locale") != locale:
            raise ValueError("unexpected locale")
        rowid = str(row["id"])
        if rowid in ids:
            raise ValueError("duplicate record id")
        ids.add(rowid)


def choose_training(rows: list[dict], locale: str, percent: int) -> list[dict]:
    if type(percent) is not int or percent not in EXPOSURE_PERCENTS:
        raise ValueError("unsupported exposure percent")
    _validate_rows(rows, locale, "train")
    ordered = sorted(rows, key=lambda r: (stable_holdout_key(locale, str(r["id"])), str(r["id"])))
    selected_ids = {str(r['id']) for r in ordered[:len(ordered) * percent // 100]}
    # Preserve published train order when fitting, including the 100% baseline.
    return [r for r in rows if str(r['id']) in selected_ids]


def choose_holdout(rows: list[dict], locale: str, limit: int = 200) -> list[dict]:
    if type(limit) is not int or limit < 1:
        raise ValueError("holdout limit must be positive")
    _validate_rows(rows, locale, "test")
    return sorted(rows, key=lambda r: (stable_holdout_key(locale, str(r["id"])), str(r["id"])))[:limit]


def evaluate_locale_profile(
    locale: str, training: list[dict], holdout: list[dict], percent: int,
) -> dict:
    if type(percent) is not int or percent not in EXPOSURE_PERCENTS:
        raise ValueError("unsupported exposure percent")
    _validate_rows(training, locale, "train")
    _validate_rows(holdout, locale, "test")
    if {str(r["id"]) for r in training} & {str(r["id"]) for r in holdout}:
        raise ValueError("training/holdout record ID overlap")
    if percent == 0 and training:
        raise ValueError("zero exposure cannot contain training")
    namespace = sorted({atom for r in training for atom in semantic_pattern(r)})
    model = None
    model_error = None
    if not training:
        model_error = "NO_TRAINING_EXPOSURE"
    else:
        try:
            episodes = [
                TargetConstructionEpisode.build(
                    episode_id=f"{locale}:train:{r['id']}",
                    source_id=f"{locale}:worker:{r['worker_id']}",
                    semantic_atoms=semantic_pattern(r),
                    target_tokens=canonical_tokens(r["utt"]),
                ) for r in training
            ]
            model = fit_target_construction_model(
                episodes, target_language_id=locale,
                semantic_atoms=namespace,
                upstream_model_ids={MODEL_LINEAGE["target_construction_pr18_head"], ADAPTER_ID},
                min_sources=2, min_positive_per_source=1,
            )
        except ValueError as exc:
            model_error = str(exc)
    candidates = []
    statuses = Counter()
    prediction_ids = []
    for row in holdout:
        if model is None:
            rendered = ()
            status = model_error or "NO_CONSTRUCTION_MODEL"
        else:
            result = render_semantic_sequence(model, semantic_pattern(row))
            rendered = result.realizations
            status = result.status
        statuses[status] += 1
        if rendered:
            prediction_ids.append(str(row["id"]))
        candidates.append(EvaluationRecord.build(
            "massive", "1.0", f"{locale}:test:{row['id']}",
            locale, str(row["id"]), locale,
            [canonical_tokens(row["utt"])], rendered,
            source_id=f"{locale}:worker:{row['worker_id']}",
            system_status=status,
        ))
    # Per-locale scoring under a declared single-slice gate; overall five
    # languages are independently required by the aggregate runner below.
    exposure = [
        TrainingExposure.build(
            "massive", "1.0", f"{locale}:train:{r['id']}",
            locale, str(r["id"]), f"{locale}:worker:{r['worker_id']}",
        ) for r in training
    ]
    local_gate = QualificationThresholds(
        min_corpora=1, min_languages=1, min_records_per_slice=max(1, len(holdout)),
        min_coverage=THRESHOLDS.min_coverage,
        min_exact_match=THRESHOLDS.min_exact_match,
        min_token_similarity=THRESHOLDS.min_token_similarity,
        max_ambiguity_rate=THRESHOLDS.max_ambiguity_rate,
    )
    # The existing evaluator deliberately refuses empty training exposure.
    # A zero-shot diagnostic is an explicit all-abstain condition, not a
    # fabricated nonempty training set or a qualification pass.
    report = evaluate_multilingual_holdout(
        exposure, candidates, regime="HELD_OUT_CONTENT", thresholds=local_gate
    ) if holdout and exposure else None
    stats = asdict(report.slices[0]) if report and report.slices else {}
    return {
        "locale": locale, "exposure_percent": percent,
        "training_record_count": len(training), "evaluation_count": len(holdout),
        "model_error": model_error,
        "statuses": dict(sorted(statuses.items())),
        "predicted_content_ids": prediction_ids,
        "coverage": stats.get("coverage", 0.0),
        "exact_match": stats.get("exact_match", 0.0),
        "token_similarity": stats.get("mean_token_similarity", 0.0),
        "ambiguity": stats.get("ambiguity_rate", 0.0),
        "local_status": report.status if report else "ZERO_EXPOSURE_ABSTENTION_NOT_QUALIFIED",
        "leakage_violations": list(report.leakage_violations) if report else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-tar", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--locales", nargs="+", choices=LOCALES, default=list(LOCALES))
    args = parser.parse_args()
    path = Path(args.dataset_tar)
    archive, digest = load_verified_archive(
        path, expected_sha256=DATASET_SHA256, expected_bytes=DATASET_BYTES
    )
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with tarfile.open(fileobj=BytesIO(archive), mode="r:gz") as tar:
        for locale in args.locales:
            rows = read_locale_rows(tar, locale)
            train = [r for r in rows if r["partition"] == "train"]
            test = [r for r in rows if r["partition"] == "test"]
            if len(train) != 11514 or len(test) != 2974:
                raise ValueError("published MASSIVE 1.0 split size mismatch")
            holdout = choose_holdout(test, locale)
            if len(holdout) != 200:
                raise ValueError("holdout count mismatch")
            for percent in EXPOSURE_PERCENTS:
                selected = choose_training(train, locale, percent)
                result = evaluate_locale_profile(locale, selected, holdout, percent)
                results.append(result)
                print(json.dumps({
                    k: v for k, v in result.items() if k != "predicted_content_ids"
                }, sort_keys=True, ensure_ascii=False), flush=True)
    summaries = []
    for percent in EXPOSURE_PERCENTS:
        group = [r for r in results if r["exposure_percent"] == percent]
        summaries.append({
            "exposure_percent": percent,
            "languages": len(group),
            "macro_coverage": sum(r["coverage"] for r in group) / len(group),
            "macro_exact_match": sum(r["exact_match"] for r in group) / len(group),
            "macro_token_similarity": sum(r["token_similarity"] for r in group) / len(group),
            "qualified_all_slices": len(group) == len(LOCALES) and all(
                r["local_status"] == "QUALIFIED_WITHIN_DECLARED_MULTILINGUAL_HOLDOUT"
                for r in group
            ),
        })
    payload = {
        "schema": "UNVTRSLR_MASSIVE_PARTIAL_EXPOSURE_V1",
        "status": "DIAGNOSTIC_ONLY_NOT_SEMANTIC_QUALIFICATION",
        "claim_ceiling": PROFILE_CLAIM,
        "dataset_sha256": digest,
        "language_set": list(args.locales),
        "exposure_percents": list(EXPOSURE_PERCENTS),
        "split_algorithm": "SHA256(locale + ':' + record_id), independently per partition",
        "gold_semantic_adapter": "intent and ordered slot types from held-out annotation",
        "frozen_gate": asdict(THRESHOLDS),
        "summaries": summaries,
        "slices": results,
    }
    write_json(out / "partial_exposure_report.json", payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
