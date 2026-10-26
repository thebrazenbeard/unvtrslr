"""Exposure-fraction tests for the separately qualified MASSIVE real-corpus packet."""
from __future__ import annotations

import pytest

from runs.massive_v1_first_real_corpus_20260922.partial_exposure import (
    EXPOSURE_PERCENTS,
    choose_training,
    choose_holdout,
    evaluate_locale_profile,
)


def _row(row_id, partition, locale="en-US", worker="worker1"):
    return {
        "id": row_id,
        "partition": partition,
        "locale": locale,
        "worker_id": worker,
        "intent": "qa",
        "annot_utt": "ask [temperature: hot]",
        "utt": f"example {row_id}",
    }


def test_exposure_selection_is_stable_and_strictly_nested():
    rows = [_row(str(i), "train") for i in range(1000)]
    rows = list(reversed(rows))
    results = [choose_training(rows, "en-US", p) for p in EXPOSURE_PERCENTS]
    ids = [set(str(r["id"]) for r in result) for result in results]
    assert [len(x) for x in ids] == [0, 10, 100, 1000]
    assert ids[0] < ids[1] < ids[2] < ids[3]
    assert [set(str(r["id"]) for r in choose_training(list(reversed(rows)), "en-US", p))
            for p in EXPOSURE_PERCENTS] == ids


@pytest.mark.parametrize("percent", [-1, 2, 12, 101, 1.0, True, "10"])
def test_unfrozen_fraction_cannot_be_supplied(percent):
    with pytest.raises(ValueError):
        choose_training([_row("one", "train")], "en-US", percent)


def test_training_provenance_must_be_unambiguous():
    rows = [_row("one", "train"), _row("one", "train")]
    with pytest.raises(ValueError, match="duplicate"):
        choose_training(rows, "en-US", 100)
    with pytest.raises(ValueError, match="train"):
        choose_training([_row("bad", "test")], "en-US", 100)
    with pytest.raises(ValueError, match="locale"):
        choose_training([_row("bad", "train", locale="de-DE")], "en-US", 100)


def test_holdout_selects_test_only_with_independent_stable_identity():
    rows = [_row(str(i), "test") for i in range(250)]
    holdout = choose_holdout(rows, "en-US", limit=20)
    assert len(holdout) == 20
    assert {r["id"] for r in holdout} == {r["id"] for r in choose_holdout(rows[::-1], "en-US", 20)}
    assert all(r["partition"] == "test" for r in holdout)
    with pytest.raises(ValueError, match="test"):
        choose_holdout([_row("bad", "train")], "en-US", 1)


def test_zero_exposure_produces_only_abstentions():
    holdout = [_row("new-a", "test"), _row("new-b", "test")]
    record = evaluate_locale_profile("en-US", [], holdout, 0)
    assert record["training_record_count"] == 0
    assert record["coverage"] == 0
    assert record["exact_match"] == 0
    assert record["model_error"] == "NO_TRAINING_EXPOSURE"
    assert record["local_status"] == "ZERO_EXPOSURE_ABSTENTION_NOT_QUALIFIED"
    assert record["statuses"] == {"NO_TRAINING_EXPOSURE": 2}
    assert record["predicted_content_ids"] == []
    assert record["evaluation_count"] == 2


def test_no_train_test_id_overlap_even_across_prefixes():
    rows = [_row(str(i), "train") for i in range(40)]
    test = [_row("0", "test")]
    with pytest.raises(ValueError, match="overlap"):
        evaluate_locale_profile("en-US", rows, test, 100)
