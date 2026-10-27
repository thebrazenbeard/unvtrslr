"""Tests for train-only fit, source-only transport and synthetic holdout."""
from __future__ import annotations
import json
import pytest
from unvtrslr.compositional_probe import fit, predict, load_jsonl, tokens
from runs.composition_20261027.run import cases, score

def sample():
    train,holdout=cases(17)
    return train,holdout

def test_disjoint_frozen_synthetic_holdout_and_coverage():
    train,test=sample()
    assert len(train)==len(test)==96
    assert not {r["source_text"] for r in train}&{r["source_text"] for r in test}
    model=fit(train)
    assert set(model["hypotheses"])=={"actor","action","patient","tense","polarity"}
    predictions=[predict(model,row["source_text"]) for row in test]
    assert score(predictions,test)["exact_accuracy"]==1.0

@pytest.mark.parametrize("seed", [17,23,47,61])
def test_four_vocab_permutations_zero_phrase_memorization(seed):
    train,test=cases(seed)
    model=fit(train)
    assert all(x["source_text"] not in {r["source_text"] for r in train} for x in test)
    assert all(predict(model,x["source_text"])["meaning"]==x["meaning"] for x in test)

def test_unknown_token_abstains_not_hallucinates():
    train,test=sample()
    model=fit(train)
    original=test[0]["source_text"].split()
    original[0]="v_unknown"
    result=predict(model," ".join(original))
    assert result["status"]=="ABSTAIN"
    assert "actor" in result["unresolved"]

def test_unseen_shape_abstains():
    model=fit(sample()[0])
    assert predict(model,"single")["status"]=="ABSTAIN"

def test_corrupted_labels_do_not_qualify():
    import random
    train,test=sample()
    meanings=[r["meaning"] for r in train]
    random.Random(17+104729).shuffle(meanings)
    corrupted=[{**r,"meaning":meanings[i]} for i,r in enumerate(train)]
    model=fit(corrupted)
    assert sum(predict(model,r["source_text"])["status"]=="OK" for r in test)==0

def test_training_schema_no_answer_extraneous_field():
    train,_=sample()
    altered=[dict(row) for row in train]
    altered[0]["reference"]="leak"
    with pytest.raises(ValueError, match="schema"):
        fit(altered)

def test_prediction_transport_rejects_reference_and_duplicates(tmp_path):
    p=tmp_path/"requests.jsonl"
    p.write_text('{"id":"1","source_text":"a b","meaning":{"actor":"leak"}}\n')
    with pytest.raises(ValueError,match="reference"):
        load_jsonl(p,{"id","source_text"})
    p.write_text('{"id":"1","id":"2","source_text":"a b"}\n')
    with pytest.raises(ValueError,match="duplicate"):
        load_jsonl(p,{"id","source_text"})

def test_reject_malformed_training():
    train,_=sample()
    with pytest.raises(ValueError,match="duplicate"):
        fit(train+[train[0]])
    with pytest.raises(ValueError):
        tokens("")

def test_synthetic_scope_is_explicit():
    model=fit(sample()[0])
    assert model["claim_ceiling"]=="SUPERVISED_FIXED_LENGTH_POSITIONAL_COMPOSITION_SYNTHETIC_ONLY"
