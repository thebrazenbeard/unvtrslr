"""Adversarial regression tests for claims and supply-chain boundaries."""
import copy
import json
from pathlib import Path
from zipfile import ZipFile
import pytest
from runs.massive_v1_first_real_corpus_20260922.argos_install_locked import (
    validate_lock, validate_model,
)
from runs.massive_v1_first_real_corpus_20260922.argos_source_only import (
    validate_complete_predictions,
)

LOCK = Path(__file__).resolve().parents[1] / "research" / "ARGOS_MODEL_LOCK_20261027.json"

@pytest.mark.parametrize("mutator", [
    lambda x: x["models"].pop(),
    lambda x: x["models"].append(copy.deepcopy(x["models"][0])),
    lambda x: x["models"][0].update(target="../foreign"),
    lambda x: x.update(engine_package="argostranslate==0.0.1"),
    lambda x: x.update(source_corpus_sha256="0" * 64),
    lambda x: x["models"][0].update(sha256="wrong"),
])
def test_model_lock_invalid_shapes_fail_closed(mutator):
    obj = json.loads(LOCK.read_text(encoding="utf-8"))
    mutator(obj)
    with pytest.raises(ValueError):
        validate_lock(obj)

def test_repo_model_lock_valid():
    validate_lock(json.loads(LOCK.read_text(encoding="utf-8")))

def test_windows_drive_member_blocked(tmp_path):
    import hashlib
    path = tmp_path / "bad.argosmodel"
    with ZipFile(path, "w") as z:
        z.writestr("pkg/metadata.json", '{"from_code":"en","to_code":"sw","package_version":"1.11"}')
        z.writestr("C:/Windows/System32/drill.txt", "x")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    spec = {"target":"sw", "package_version":"1.11","bytes":path.stat().st_size,"sha256":digest}
    with pytest.raises(ValueError, match="unsafe"):
        validate_model(path, spec)

def test_partial_success_is_a_failed_benchmark():
    candidates = [
        {"id": "1", "status": "OK", "text": "bonjour"},
        {"id": "2", "status": "ERROR", "text": None},
    ]
    with pytest.raises(ValueError, match="incomplete"):
        validate_complete_predictions(candidates, ["1", "2"])

def test_only_complete_unique_ok_set_succeeds():
    records = [{"id":str(i), "status":"OK", "text":"text"} for i in range(2)]
    validate_complete_predictions(records, ["0", "1"])
    with pytest.raises(ValueError):
        validate_complete_predictions(records + [records[0]], ["0", "1"])
    with pytest.raises(ValueError):
        validate_complete_predictions(records, ["0", "missing"])


def test_worker_requires_requests_only_directory(tmp_path):
    from runs.massive_v1_first_real_corpus_20260922.argos_source_only import (
        validate_worker_input_directory
    )
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    for locale in ("fr-FR", "de-DE", "sw-KE", "tr-TR"):
        (input_dir / f"requests_en_to_{locale}.jsonl").write_text("{}\n")
    other = tmp_path / "outputs"
    models = tmp_path / "models"
    models.mkdir()
    validate_worker_input_directory(input_dir, other, models)
    (input_dir / "gold_references.jsonl").write_text('{"target":"leak"}\n')
    with pytest.raises(ValueError, match="request-only"):
        validate_worker_input_directory(input_dir, other, models)
    (input_dir / "gold_references.jsonl").unlink()
    with pytest.raises(ValueError, match="overlap"):
        validate_worker_input_directory(input_dir, input_dir, models)

def test_worker_rejects_existing_predicted_files(tmp_path):
    from runs.massive_v1_first_real_corpus_20260922.argos_source_only import validate_worker_input_directory
    input_dir = tmp_path / "source"
    input_dir.mkdir()
    for locale in ("fr-FR", "de-DE", "sw-KE", "tr-TR"):
        (input_dir / f"requests_en_to_{locale}.jsonl").write_text("{}\n")
    destination = tmp_path / "pred"
    destination.mkdir()
    (destination / "predictions_en_to_fr-FR.jsonl").write_text('{"status":"OK"}')
    models = tmp_path / "models"
    models.mkdir()
    with pytest.raises(ValueError, match="stale"):
        validate_worker_input_directory(input_dir, destination, models)

def test_rejects_conflicting_model_metadata_even_with_matching_archive_hash(tmp_path):
    import hashlib
    archive = tmp_path / "metadata-mismatch.argosmodel"
    with ZipFile(archive, "w") as z:
        z.writestr("pkg/metadata.json", json.dumps({
            "from_code": "en", "to_code": "sw",
            "package_version": "1.11", "argos_version": "1.0"
        }))
    spec = {
        "target": "sw", "package_version": "1.11", "argos_version": "1.5",
        "bytes": archive.stat().st_size,
        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()
    }
    with pytest.raises(ValueError, match="identity"):
        validate_model(archive, spec)
