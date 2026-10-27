"""Evaluator-only BLEU and chrF; run after sealed source-only inference ends."""
from __future__ import annotations
import argparse
from io import BytesIO
import importlib.metadata
import json
from pathlib import Path
import tarfile
from sacrebleu.metrics import BLEU, CHRF
from unvtrslr.archive_integrity import load_verified_archive
from runs.massive_v1_first_real_corpus_20260922.blind_text import (
    TARGET_LOCALES, make_parallel_pairs, score_predictions
)
from runs.massive_v1_first_real_corpus_20260922.run import (
    DATASET_BYTES, DATASET_SHA256, read_locale_rows, stable_holdout_key
)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-tar", required=True, type=Path)
    ap.add_argument("--predictions-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    if importlib.metadata.version("sacrebleu") != "2.5.1":
        raise ValueError("unqualified sacrebleu release")
    archive, digest = load_verified_archive(a.dataset_tar, expected_sha256=DATASET_SHA256, expected_bytes=DATASET_BYTES)
    with tarfile.open(fileobj=BytesIO(archive), mode="r:gz") as tar:
        corpora = {lc: read_locale_rows(tar, lc) for lc in ("en-US", *TARGET_LOCALES)}
    source = [r for r in corpora["en-US"] if r["partition"] == "test"]
    ids = [str(r["id"]) for r in sorted(source, key=lambda r: stable_holdout_key("en-US", str(r["id"])))[:200]]
    bleu = BLEU(tokenize="13a", effective_order=True)
    chrf = CHRF(word_order=2)
    report = {"schema": "UNV_ARGOS_POST_INFERENCE_QUALITY_V1", "dataset_sha256": digest,
              "sacrebleu_version": "2.5.1", "languages": []}
    for locale in TARGET_LOCALES:
        target = [r for r in corpora[locale] if r["partition"] == "test"]
        aligned = make_parallel_pairs(source, target, "en-US", locale, "test")
        by_id = {x["id"]: x for x in aligned}
        holdout = [by_id[i] for i in ids]
        predfile = a.predictions_dir / f"predictions_en_to_{locale}.jsonl"
        predictions = [json.loads(line) for line in predfile.read_text(encoding="utf-8").splitlines()]
        native_score = score_predictions(holdout, predictions)
        out_by_id = {p["id"]: p for p in predictions}
        hypotheses = [out_by_id[rid]["text"] or "" for rid in ids]
        references = [by_id[rid]["target_text"] for rid in ids]
        b = bleu.corpus_score(hypotheses, [references])
        c = chrf.corpus_score(hypotheses, [references])
        examples = []
        for idx in (0, 1, 2):
            examples.append({"id": ids[idx], "source": by_id[ids[idx]]["source_text"],
                             "reference": references[idx], "prediction": hypotheses[idx]})
        item = {"target_locale": locale, "records": len(ids),
                "native_exact_match": native_score["exact_match"],
                "native_token_similarity": native_score["token_similarity"],
                "bleu": b.score, "chrf2": c.score,
                "bleu_signature": str(bleu.get_signature()),
                "chrf_signature": str(chrf.get_signature()),
                "examples": examples}
        report["languages"].append(item)
        print(json.dumps({k: v for k, v in item.items() if k != "examples"}, ensure_ascii=True), flush=True)
    a.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
