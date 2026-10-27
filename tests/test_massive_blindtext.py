"""Cross-language paired-text boundary; fixtures never supply gold semantics to adapter."""
import pytest

from runs.massive_v1_first_real_corpus_20260922.blind_text import (
    make_parallel_pairs, public_requests, fit_exact_phrasebook,
    predict_phrasebook, predict_copy_control, score_predictions, select_pairs,
)


def row(id, lang, partition, text, intent="ask"):
    return {"id": id, "locale": lang, "partition": partition,
            "utt": text, "intent": intent}


def pairs(partition="test"):
    en = [row("1", "en-US", partition, "open door"),
          row("2", "en-US", partition, "turn left")]
    fr = [row("1", "fr-FR", partition, "ouvrir la porte"),
          row("2", "fr-FR", partition, "tournez à gauche")]
    return make_parallel_pairs(en, fr, "en-US", "fr-FR", partition)


def test_source_only_requests_hide_target_and_gold_annotations():
    actual = public_requests(pairs())
    assert actual == [
        {"id": "1", "source_language": "en", "target_language": "fr",
         "source_text": "open door"},
        {"id": "2", "source_language": "en", "target_language": "fr",
         "source_text": "turn left"},
    ]
    assert "ouvrir" not in repr(actual)
    assert "intent" not in repr(actual)


def test_parallel_identity_and_provenance_are_enforced():
    en = [row("1", "en-US", "test", "open")]
    fr = [row("different", "fr-FR", "test", "ouvrir")]
    with pytest.raises(ValueError, match="aligned"):
        make_parallel_pairs(en, fr, "en-US", "fr-FR", "test")
    with pytest.raises(ValueError, match="duplicate"):
        make_parallel_pairs(en + en, [row("1", "fr-FR", "test", "ouvrir")],
                            "en-US", "fr-FR", "test")
    with pytest.raises(ValueError, match="partition"):
        make_parallel_pairs([row("1", "en-US", "train", "open")],
                            [row("1", "fr-FR", "test", "ouvrir")],
                            "en-US", "fr-FR", "test")
    with pytest.raises(ValueError, match="intent"):
        make_parallel_pairs(en, [row("1", "fr-FR", "test", "ouvrir", intent="other")],
                            "en-US", "fr-FR", "test")


def test_phrasebook_only_exact_seen_surface_not_gold_test_reference():
    train = pairs("train")
    lookup = fit_exact_phrasebook(train)
    assert predict_phrasebook(public_requests(train), lookup)[0] == {
        "id": "1", "status": "OK", "text": "ouvrir la porte",
    }
    unknown = [{"id": "3", "source_language": "en",
                "target_language": "fr", "source_text": "unknown words"}]
    assert predict_phrasebook(unknown, lookup) == [
        {"id": "3", "status": "ABSTAIN", "text": None}
    ]


def test_conflicting_translations_abstain_and_never_choose_majority():
    en = [row("1", "en-US", "train", "right"),
          row("2", "en-US", "train", "right")]
    fr = [row("1", "fr-FR", "train", "droit"),
          row("2", "fr-FR", "train", "droite")]
    lookup = fit_exact_phrasebook(
        make_parallel_pairs(en, fr, "en-US", "fr-FR", "train")
    )
    assert predict_phrasebook(
        [{"id": "3", "source_language": "en",
          "target_language": "fr", "source_text": "right"}], lookup
    )[0]["status"] == "ABSTAIN"


def test_sealed_scoring_exact_coverage_and_abstention():
    data = pairs()
    got = score_predictions(data, [
        {"id": "1", "status": "OK", "text": "ouvrir la porte"},
        {"id": "2", "status": "ABSTAIN", "text": None},
    ])
    assert got["records"] == 2
    assert got["coverage"] == .5
    assert got["exact_match"] == .5
    assert got["token_similarity"] == .5
    assert got["abstentions"] == 1
    assert got["status"] == "DIAGNOSTIC_ONLY_NOT_SEMANTIC_QUALIFICATION"


@pytest.mark.parametrize("predictions", [
    [{"id": "1", "status": "OK", "text": "wrong"}],
    [{"id": "1", "status": "OK", "text": "yes"},
     {"id": "1", "status": "OK", "text": "no"}],
    [{"id": "1", "status": "ABSTAIN", "text": "guess"},
     {"id": "2", "status": "ABSTAIN", "text": None}],
    [{"id": "1", "status": "OK", "text": ""},
     {"id": "2", "status": "ABSTAIN", "text": None}],
    [{"id": "1", "status": "ERROR", "text": "hallucinated"},
     {"id": "2", "status": "ABSTAIN", "text": None}],
    [{"id": "1", "status": "OK", "text": "bonjour", "reference": "leak"},
     {"id": "2", "status": "ABSTAIN", "text": None}],
])
def test_malformed_predictions_fail_closed(predictions):
    with pytest.raises(ValueError):
        score_predictions(pairs(), predictions)


def test_training_selection_strict_and_nested():
    data = [{"id": str(i), "source_text": str(i), "target_text": str(i),
             "source_language": "en", "target_language": "fr"}
            for i in range(100)]
    selections = [select_pairs(data, "en-US", p) for p in (0, 1, 10, 100)]
    selected = [{x["id"] for x in group} for group in selections]
    assert [len(x) for x in selected] == [0, 1, 10, 100]
    assert selected[0] < selected[1] < selected[2] < selected[3]
    assert [{x["id"] for x in select_pairs(list(reversed(data)), "en-US", p)}
            for p in (0, 1, 10, 100)] == selected



def test_echo_baseline_is_covered_but_not_a_translation():
    source = public_requests(pairs())
    echoed = predict_copy_control(source)
    assert echoed == [
        {"id": "1", "status": "OK", "text": "open door"},
        {"id": "2", "status": "OK", "text": "turn left"},
    ]
    measured = score_predictions(pairs(), echoed)
    assert measured["coverage"] == 1
    assert measured["exact_match"] == 0


def test_oversized_token_stream_is_rejected_before_edit_distance():
    too_many_tokens = "x " * 300
    with pytest.raises(ValueError, match="token"):
        score_predictions(pairs(), [
            {"id": "1", "status": "OK", "text": too_many_tokens},
            {"id": "2", "status": "ABSTAIN", "text": None},
        ])
