"""Human-review infrastructure regressions; ratings here are TEST FIXTURES, not assessments."""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path

import pytest
from runs.massive_v1_first_real_corpus_20260922.human_blind_packet import (
    make_tasks,write_new,
)
from runs.massive_v1_first_real_corpus_20260922.human_blind_scoring import (
    aggregate,load_packet,validate_rating,
)

def write_jsonl(path,rows):
    path.write_text("".join(json.dumps(row,sort_keys=True)+"\n" for row in rows),
                    encoding="utf-8")
    return path

def sample_tasks():
    requests=[{"id":str(i),"source_language":"en","target_language":"fr",
        "source_text":f"say hello {i}", "reference":"never show the gold"} for i in range(200)]
    predictions=[{"id":str(i),"status":"OK","text":f"bonjour {i}"} for i in range(200)]
    return requests,predictions

def packet_fixture(tmp_path):
    tasks=[{"task_id":f"{i:020x}","source_language":"en",
            "target_locale":("fr-FR","de-DE","sw-KE","tr-TR")[i%4],
            "source_text":f"source sentence {i}","candidate_text":f"candidate {i}"}
           for i in range(8)]
    return write_jsonl(tmp_path/"packet.jsonl",tasks),tasks

def ratings_fixture(tasks):
    return [{"task_id":task["task_id"],"reviewer_id":rid,
             "status":"RATED","adequacy":4 if i%2==0 else 3,
             "fluency":3,"errors":[],"comment":""}
            for i,task in enumerate(tasks) for rid in ("rater-a","rater-b")]

def test_blind_packet_hides_gold_and_backend():
    reqs,preds=sample_tasks()
    public,private=make_tasks(reqs,preds,"fr-FR",count=20)
    assert len(public)==len(private)==20
    assert len({item["task_id"] for item in public})==20
    assert all(set(x)=={"task_id","source_language","target_locale",
             "source_text","candidate_text"} for x in public)
    assert "reference" not in json.dumps(public)
    assert "argostranslate" not in json.dumps(public)
    assert all(x["private_source_id"] for x in private)
    assert make_tasks(reqs,preds,"fr-FR",count=20)==(public,private)

def test_packet_rejects_partial_output():
    reqs,preds=sample_tasks()
    preds[5]["status"]="ERROR"
    preds[5]["text"]=None
    with pytest.raises(ValueError,match="unusable"):
        make_tasks(reqs,preds,"fr-FR",count=20)

def test_packet_rejects_duplicate_predictions():
    reqs,preds=sample_tasks()
    preds[10]=preds[9]
    with pytest.raises(ValueError,match="identities"):
        make_tasks(reqs,preds,"fr-FR",count=20)

def test_packet_write_no_overwrite(tmp_path):
    path=tmp_path/"packet.jsonl"
    write_new(path,[{"a":1}])
    with pytest.raises(ValueError,match="overwrite"):
        write_new(path,[{"a":2}])

def test_complete_two_rater_report_is_explicitly_unverified(tmp_path):
    path,tasks=packet_fixture(tmp_path)
    rating_path=write_jsonl(tmp_path/"ratings.jsonl",ratings_fixture(tasks))
    report=aggregate(path,rating_path,"rater-a","rater-b")
    assert report["tasks_supplied"]==8 and report["reviews_supplied"]==16
    assert report["human_provenance_verified"] is False
    assert report["independence_proven"] is False
    assert set(report["languages"])=={"fr-FR","de-DE","sw-KE","tr-TR"}
    assert all(x["exact_pair_agreement"]==1.0 for x in report["languages"].values())
    assert all(x["cohen_unweighted_kappa"] is None for x in report["languages"].values())  # all labels constant per locale

def test_no_rating_file_means_no_report(tmp_path):
    path,_=packet_fixture(tmp_path)
    with pytest.raises(ValueError,match="missing"):
        aggregate(path,tmp_path/"no-such-file","rater-a","rater-b")

def test_refuse_duplicate_or_missing_rating(tmp_path):
    path,tasks=packet_fixture(tmp_path)
    ratings=ratings_fixture(tasks)
    write_jsonl(tmp_path/"ratings.jsonl",ratings[:-1])
    with pytest.raises(ValueError,match="missing"):
        aggregate(path,tmp_path/"ratings.jsonl","rater-a","rater-b")
    write_jsonl(tmp_path/"ratings.jsonl",ratings+[ratings[0]])
    with pytest.raises(ValueError,match="duplicate"):
        aggregate(path,tmp_path/"ratings.jsonl","rater-a","rater-b")

@pytest.mark.parametrize("mutation",["unknown","boolean","score","errors","extra","nonfinite"])
def test_refuse_malformed_rating(tmp_path,mutation):
    path,tasks=packet_fixture(tmp_path)
    ratings=ratings_fixture(tasks)
    if mutation=="unknown":ratings[0]["task_id"]="f"*20
    elif mutation=="boolean":ratings[0]["adequacy"]=True
    elif mutation=="score":ratings[0]["fluency"]=5
    elif mutation=="errors":ratings[0]["errors"]=["NOT_A_CATEGORY"]
    elif mutation=="extra":ratings[0]["gold_reference"]="leak"
    elif mutation=="nonfinite":ratings[0]["adequacy"]=float("nan")
    write_jsonl(tmp_path/"ratings.jsonl",ratings)
    with pytest.raises(ValueError):
        aggregate(path,tmp_path/"ratings.jsonl","rater-a","rater-b")

def test_unratable_with_nonnull_scores_rejected():
    row=ratings_fixture([{"task_id":"a"*20}])[0]
    row["status"]="UNRATABLE"
    with pytest.raises(ValueError,match="null"):
        validate_rating(row,{"rater-a","rater-b"})

def test_unratable_pairs_excluded_without_invented_accuracy(tmp_path):
    path,tasks=packet_fixture(tmp_path)
    ratings=ratings_fixture(tasks)
    for row in ratings:
        if row["task_id"]==tasks[0]["task_id"]:
            row["status"]="UNRATABLE"
            row["adequacy"]=row["fluency"]=None
    write_jsonl(tmp_path/"ratings.jsonl",ratings)
    result=aggregate(path,tmp_path/"ratings.jsonl","rater-a","rater-b")
    assert result["languages"]["fr-FR"]["any_unratable"]==1
    assert result["languages"]["fr-FR"]["both_rated"]==1

def test_rating_import_duplicate_json_keys_fail(tmp_path):
    path,tasks=packet_fixture(tmp_path)
    malicious='{"task_id":"'+tasks[0]["task_id"]+'","task_id":"override"}\n'
    (tmp_path/"ratings.jsonl").write_text(malicious,encoding="utf-8")
    with pytest.raises(ValueError,match="duplicate JSON"):
        aggregate(path,tmp_path/"ratings.jsonl","rater-a","rater-b")

def test_packet_import_rejects_target_field(tmp_path):
    path,tasks=packet_fixture(tmp_path)
    tasks[0]["target_text"]="gold leaked"
    write_jsonl(path,tasks)
    with pytest.raises(ValueError,match="malformed"):
        load_packet(path)


def test_aggregator_cli_requires_matching_packet_digest(tmp_path, monkeypatch):
    import sys
    from runs.massive_v1_first_real_corpus_20260922.human_blind_scoring import main
    packet,tasks=packet_fixture(tmp_path)
    scores=write_jsonl(tmp_path/"ratings.jsonl",ratings_fixture(tasks))
    out=tmp_path/"summary.json"
    argv=["score","--packet",str(packet),"--ratings",str(scores),
          "--reviewer-a","rater-a","--reviewer-b","rater-b",
          "--expected-packet-sha256","0"*64,"--out",str(out)]
    monkeypatch.setattr(sys,"argv",argv)
    with pytest.raises(ValueError,match="digest mismatch"):
        main()
    assert not out.exists()
