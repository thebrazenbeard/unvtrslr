"""Fail-closed external JSONL ingestion, independent of model execution."""
import json
from pathlib import Path
import pytest
from runs.massive_v1_first_real_corpus_20260922.blind_text import load_external_predictions

def rows(tmp_path, lines):
    p = tmp_path / "pred.jsonl"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p

def test_valid_predicted_rows(tmp_path):
    inputs = [json.dumps({"id": "1", "status": "OK", "text": "bonjour"}),
              json.dumps({"id": "2", "status": "ABSTAIN", "text": None})]
    got = load_external_predictions(rows(tmp_path, inputs), expected_count=2)
    assert len(got) == 2

def test_duplicate_json_key_rejected(tmp_path):
    evil = '{"id":"1","status":"OK","text":"hello","text":"override"}'
    with pytest.raises(ValueError, match="duplicate"):
        load_external_predictions(rows(tmp_path, [evil]), expected_count=1)

def test_nonfinite_json_rejected(tmp_path):
    evil = '{"id":"1","status":"OK","text":NaN}'
    with pytest.raises(ValueError, match="nonfinite"):
        load_external_predictions(rows(tmp_path, [evil]), expected_count=1)

def test_record_limit_rejected(tmp_path):
    s = json.dumps({"id": "x", "status": "ABSTAIN", "text": None})
    with pytest.raises(ValueError, match="records"):
        load_external_predictions(rows(tmp_path, [s] * 201), expected_count=200)

def test_line_limit_rejected(tmp_path):
    too_big = '{"id":"1","status":"OK","text":"' + ("x" * 40000) + '"}'
    with pytest.raises(ValueError, match="line"):
        load_external_predictions(rows(tmp_path, [too_big]), expected_count=1)

def test_incomplete_rejected(tmp_path):
    p = rows(tmp_path, [json.dumps({"id": "1", "status": "ABSTAIN", "text": None})])
    with pytest.raises(ValueError, match="records"):
        load_external_predictions(p, expected_count=2)
