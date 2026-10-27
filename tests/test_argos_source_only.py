"""Hostile source-only boundary tests; no model inference needed."""
import json
from pathlib import Path
from zipfile import ZipFile
import pytest
from runs.massive_v1_first_real_corpus_20260922.argos_source_only import read_requests, percentile, strict_object
from runs.massive_v1_first_real_corpus_20260922.argos_install_locked import validate_model

def item(i=1, **kwargs):
    value = {"id": str(i), "source_language": "en", "target_language": "sw", "source_text": "turn off the light"}
    value.update(kwargs)
    return value

def to_file(tmp_path, lines):
    p = tmp_path / "requests.jsonl"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p

def test_accepts_valid_source_only(tmp_path):
    assert read_requests(to_file(tmp_path, [json.dumps(item())]), "sw", 1) == [item()]

@pytest.mark.parametrize("mutant", [
    item(target_text="secret reference"),
    item(intent="gold intent"),
    item(source_language="fr"),
    item(target_language="de"),
    item(source_text=""),
    item(id=""),
])
def test_rejects_reference_and_invalid_language(tmp_path, mutant):
    with pytest.raises(ValueError):
        read_requests(to_file(tmp_path, [json.dumps(mutant)]), "sw", 1)

def test_rejects_duplicate_keys_even_when_json_parser_would_keep_last(tmp_path):
    raw = '{"id":"1","source_language":"en","target_language":"sw","source_text":"first","source_text":"secret"}'
    with pytest.raises(ValueError, match="duplicate JSON key"):
        read_requests(to_file(tmp_path, [raw]), "sw", 1)

def test_rejects_duplicate_ids_and_count_mismatch(tmp_path):
    p = to_file(tmp_path, [json.dumps(item()), json.dumps(item())])
    with pytest.raises(ValueError, match="duplicate ID"):
        read_requests(p, "sw", 2)
    with pytest.raises(ValueError, match="unexpected request count"):
        read_requests(to_file(tmp_path, [json.dumps(item())]), "sw", 2)

def test_rejects_nonfinite_json(tmp_path):
    with pytest.raises(ValueError, match="nonfinite"):
        read_requests(to_file(tmp_path, ['{"id":"1","source_language":"en","target_language":"sw","source_text":NaN}']), "sw", 1)

def test_percentiles_exact():
    assert percentile([5, 1, 2, 3, 4], .95) == 5
    assert percentile([], .95) is None

def test_model_hash_mismatch_fails_before_loading(tmp_path):
    archive = tmp_path / "synthetic.argosmodel"
    with ZipFile(archive, "w") as z:
        z.writestr("translate-en_sw/metadata.json", '{"from_code":"en","to_code":"sw","package_version":"1.11"}')
    with pytest.raises(ValueError, match="archive hash mismatch"):
        validate_model(archive, {"target":"sw","package_version":"1.11","bytes":archive.stat().st_size,"sha256":"0"*64})

def test_model_symlink_rejected_even_with_pinned_hash(tmp_path):
    import hashlib
    from zipfile import ZipInfo
    archive = tmp_path / "symlink.argosmodel"
    with ZipFile(archive, "w") as z:
        z.writestr("pkg/metadata.json", '{"from_code":"en","to_code":"sw","package_version":"1.11"}')
        link = ZipInfo("pkg/model.bin")
        link.create_system = 3
        link.external_attr = (0o120777 << 16)
        z.writestr(link, "C:/Windows/System32")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    with pytest.raises(ValueError, match="symlink"):
        validate_model(archive, {"target":"sw","package_version":"1.11","bytes":archive.stat().st_size,"sha256":digest})
