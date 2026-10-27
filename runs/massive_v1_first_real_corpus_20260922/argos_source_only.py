"""Offline, source-only Argos inference. Never reads MASSIVE targets or annotations."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import statistics
import time
from runs.massive_v1_first_real_corpus_20260922.argos_install_locked import validate_lock

def strict_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key")
        out[key] = value
    return out

def read_requests(path: Path, target: str, expected: int) -> list[dict]:
    if path.stat().st_size > 4_000_000:
        raise ValueError("oversized source-only request file")
    rows, ids = [], set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or len(raw) > 16384:
            raise ValueError("empty or oversized request")
        row = json.loads(raw, object_pairs_hook=strict_object,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
        if type(row) is not dict or set(row) != {"id", "source_language", "target_language", "source_text"}:
            raise ValueError("reference/annotation or malformed request boundary")
        if not isinstance(row["id"], str) or not row["id"] or row["id"] in ids:
            raise ValueError("bad/duplicate ID")
        if row["source_language"] != "en" or row["target_language"] != target:
            raise ValueError("language mismatch")
        if type(row["source_text"]) is not str or not row["source_text"].strip() or len(row["source_text"]) > 8192:
            raise ValueError("invalid source")
        ids.add(row["id"])
        rows.append(row)
    if len(rows) != expected:
        raise ValueError(f"unexpected request count {len(rows)}")
    return rows

def percentile(values: list[float], fraction: float) -> float | None:
    return sorted(values)[math.ceil(fraction * len(values)) - 1] if values else None

def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

def validate_complete_predictions(rows: list[dict], expected_ids: list[str]) -> None:
    """A benchmark run must not silently pass when any item failed."""
    if (len(rows) != len(expected_ids)
            or len(set(expected_ids)) != len(expected_ids)
            or [row.get("id") for row in rows] != expected_ids):
        raise ValueError("incomplete or reordered benchmark predictions")
    for row in rows:
        if type(row) is not dict or set(row) != {"id", "status", "text"}:
            raise ValueError("invalid benchmark prediction schema")
        if row["status"] != "OK" or type(row["text"]) is not str or not row["text"].strip():
            raise ValueError("incomplete benchmark inference; record diagnostics and fail")


def validate_worker_input_directory(requests_dir: Path, predictions_dir: Path, models_dir: Path) -> None:
    """Detect accidental answer-file co-location; not an OS sandbox."""
    src = requests_dir.resolve(strict=True)
    models = models_dir.resolve(strict=True)
    output = predictions_dir.resolve(strict=False)
    if not src.is_dir() or not models.is_dir():
        raise ValueError("request/model directories missing")
    if (src == output or src.is_relative_to(output) or output.is_relative_to(src)
            or src == models or src.is_relative_to(models)
            or models.is_relative_to(src) or output == models
            or output.is_relative_to(models) or models.is_relative_to(output)):
        raise ValueError("input/model/output path overlap")
    expected = {f"requests_en_to_{locale}.jsonl" for locale in
                ("fr-FR", "de-DE", "sw-KE", "tr-TR")}
    actual = {entry.name for entry in src.iterdir()}
    if actual != expected:
        raise ValueError("not a request-only inference directory")
    if any(entry.is_symlink() or not entry.is_file() for entry in src.iterdir()):
        raise ValueError("request-only directory contains unsafe link or entry")
    if predictions_dir.exists() and any(predictions_dir.iterdir()):
        raise ValueError("nonempty prediction destination risks stale benchmark outputs")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--requests-dir", type=Path, required=True)
    p.add_argument("--predictions-dir", type=Path, required=True)
    p.add_argument("--model-dir", type=Path, required=True)
    p.add_argument("--lock", type=Path, required=True)
    p.add_argument("--limit", type=int, default=200)
    a = p.parse_args()
    validate_worker_input_directory(a.requests_dir, a.predictions_dir, a.model_dir)
    if not 1 <= a.limit <= 200:
        raise ValueError("bad limit")
    if importlib.metadata.version("argostranslate") != "1.11.0":
        raise ValueError("unqualified Argos engine")
    lock = json.loads(a.lock.read_text(encoding="utf-8"))
    validate_lock(lock)
    for spec in lock["models"]:
        package_path = a.model_dir / f'en_{spec["target"]}.argosmodel'
        if package_path.stat().st_size != spec["bytes"] or sha(package_path) != spec["sha256"]:
            raise ValueError(f'model archive changed: {spec["target"]}')
    import psutil  # inference-only resource metrics; unit imports need no Argos extras
    startup_begin = time.perf_counter()
    import argostranslate.translate as tr
    installed = {x.code: x for x in tr.get_installed_languages()}
    startup_load_s = time.perf_counter() - startup_begin
    proc = psutil.Process()
    if "en" not in installed:
        raise ValueError("English source model missing")
    a.predictions_dir.mkdir(parents=True, exist_ok=True)
    report = {"engine": "argostranslate", "version": "1.11.0",
              "device": os.environ.get("ARGOS_DEVICE_TYPE", "cpu"),
              "startup_load_s": startup_load_s, "targets": []}
    for spec in lock["models"]:
        target = spec["target"]
        locale = {'fr': 'fr-FR', 'de': 'de-DE', 'sw': 'sw-KE', 'tr': 'tr-TR'}[target]
        path = a.requests_dir / f"requests_en_to_{locale}.jsonl"
        rows = read_requests(path, target, 200)[:a.limit]
        if target not in installed:
            raise ValueError(f"direct model missing for {target}")
        translator = installed["en"].get_translation(installed[target])
        latencies, predictions = [], []
        started = time.perf_counter()
        cpu_started = time.process_time()
        for i, row in enumerate(rows):
            before = time.perf_counter()
            try:
                candidate = translator.translate(row["source_text"])
                if type(candidate) is not str or not candidate.strip() or len(candidate) > 8192:
                    raise ValueError("invalid translation output")
                pred = {"id": row["id"], "status": "OK", "text": candidate}
            except Exception as exc:
                print('INFERENCE_ERROR', target, i, type(exc).__name__, str(exc)[:240], flush=True)
                pred = {"id": row["id"], "status": "ERROR", "text": None}
            elapsed = time.perf_counter() - before
            latencies.append(elapsed)
            predictions.append(pred)
        wall = time.perf_counter() - started
        cpu = time.process_time() - cpu_started
        validate_complete_predictions(predictions, [row["id"] for row in rows])
        predpath = a.predictions_dir / f"predictions_en_to_{locale}.jsonl"
        with predpath.open("w", encoding="utf-8", newline="\n") as out:
            for rec in predictions:
                out.write(json.dumps(rec, ensure_ascii=False, allow_nan=False) + "\n")
        mem = proc.memory_info()
        perf = {"target": target, "records": len(rows), "ok": sum(r["status"] == "OK" for r in predictions),
                "cold_first_s": latencies[0], "warm_p50_s": statistics.median(latencies[1:]) if len(latencies)>1 else None,
                "warm_p95_s": percentile(latencies[1:], .95), "wall_s": wall,
                "process_cpu_s": cpu, "throughput_rps": len(rows)/wall,
                "post_batch_rss_mib": mem.rss / 1048576,
                "process_peak_working_set_mib": getattr(mem, "peak_wset", mem.rss) / 1048576,
                "requests_sha256": sha(path), "predictions_sha256": sha(predpath),
                "archive_sha256": spec["sha256"], "first_prediction": predictions[0]}
        report["targets"].append(perf)
        print(json.dumps(perf, ensure_ascii=True), flush=True)
    (a.predictions_dir/"argos_runtime_metrics.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

if __name__ == "__main__":
    main()
