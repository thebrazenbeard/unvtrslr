"""Blinded packet privacy/provenance validation with synthetic fixtures."""
from __future__ import annotations
import pytest
from runs.massive_v1_first_real_corpus_20260922.human_blind_packet import make_tasks

def fixtures():
    req=[{"id":str(i),"source_language":"en","target_language":"fr",
          "source_text":f"source {i}"} for i in range(200)]
    pred=[{"id":str(i),"status":"OK","text":f"translation {i}"} for i in range(200)]
    return req,pred

def test_packet_samples_deterministically_and_leaks_no_labels_or_model():
    req,pred=fixtures()
    pub,private=make_tasks(req,pred,"fr-FR",20)
    assert len(pub)==len(private)==20
    assert len({p["task_id"] for p in pub})==20
    assert pub==make_tasks(req,pred,"fr-FR",20)[0]
    assert all(set(row)=={"task_id","source_language","target_locale",
                          "source_text","candidate_text"} for row in pub)
    assert all("private_source_id" not in row and "reference" not in row
               and "engine" not in row for row in pub)
    assert all("private_source_id" in row for row in private)
    assert all(row["task_id"] not in {str(i) for i in range(200)} for row in pub)

def test_missing_output_record_rejected():
    req,pred=fixtures()
    with pytest.raises(ValueError):
        make_tasks(req,pred[:-1],"fr-FR")

def test_duplicate_source_id_fails_closed():
    req,pred=fixtures()
    pred[-1]["id"]=pred[0]["id"]
    with pytest.raises(ValueError):
        make_tasks(req,pred,"fr-FR")

def test_error_or_abstention_fails_closed():
    req,pred=fixtures()
    pred[0]["status"]="ERROR"
    pred[0]["text"]=None
    with pytest.raises(ValueError):
        make_tasks(req,pred,"fr-FR")

def test_untrusted_prediction_extra_field_fails_closed():
    req,pred=fixtures()
    pred[0]["reference"]="correct answer"
    with pytest.raises(ValueError):
        make_tasks(req,pred,"fr-FR")

def test_sample_count_boundary():
    req,pred=fixtures()
    with pytest.raises(ValueError):
        make_tasks(req,pred,"fr-FR",201)
    with pytest.raises(ValueError):
        make_tasks(req,pred,"fr-FR",0)

def test_private_output_nested_beneath_review_tree_is_rejected(tmp_path):
    from runs.massive_v1_first_real_corpus_20260922.human_blind_packet import check_output_separation
    reviewer=tmp_path/"public"/"packet.jsonl"
    private=tmp_path/"public"/"subdir"/"manifest.jsonl"
    with pytest.raises(ValueError,match="overlap"):
        check_output_separation(reviewer,private)
    check_output_separation(tmp_path/"public"/"packet.jsonl",tmp_path/"private"/"manifest.jsonl")
