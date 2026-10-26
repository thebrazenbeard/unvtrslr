"""Frozen, deliberately synthetic target-construction holdout falsifiers."""

from dataclasses import replace

import pytest

from unvtrslr.target_constructions import TargetConstructionEpisode
from unvtrslr.target_holdout import (
    evaluate_target_construction_holdout,
    target_holdout_split_sha256,
)


NAMESPACE = ("ctx:red", "ctx:blue", "shape:square", "shape:triangle")
UPSTREAM = ("translator-1", "target-grounder-1")
KW = {
    "target_language_id": "opaque-target",
    "semantic_atoms": NAMESPACE,
    "upstream_model_ids": UPSTREAM,
}


def sample(eid, source, atoms, tokens):
    return TargetConstructionEpisode.build(eid, source, atoms, tokens)


def training():
    rows = []
    for source in ("source-1", "source-2"):
        for index in (1, 2):
            rows.extend(
                [
                    sample(f"{source}-{index}-red-square", source,
                           ("ctx:red", "shape:square"), ("red", "square")),
                    sample(f"{source}-{index}-blue-triangle", source,
                           ("ctx:blue", "shape:triangle"), ("blue", "triangle")),
                ]
            )
    return tuple(rows)


def heldout():
    return (
        sample("h-known", "source-3", ("ctx:red", "shape:square"), ("red", "square")),
        sample("h-combination", "source-3", ("ctx:red", "shape:triangle"), ("red", "triangle")),
        sample("h-length", "source-4", ("ctx:blue", "shape:triangle", "ctx:red"),
               ("blue", "triangle", "red")),
        sample("h-outside", "source-4", ("ctx:green",), ("green",)),
    )


def evaluate(train=None, hold=None):
    train = tuple(training() if train is None else train)
    hold = tuple(heldout() if hold is None else hold)
    sha = target_holdout_split_sha256(train, hold, **KW)
    return evaluate_target_construction_holdout(
        train, hold, expected_split_sha256=sha, **KW
    )


def test_frozen_holdout_separates_recall_composition_length_and_source_shift():
    result = evaluate()
    by_id = {row.episode_id: row for row in result.rows}

    assert result.status == "REFERENCE_HOLDOUT_SCREEN_ONLY"
    assert result.provenance_status == "CALLER_ASSERTED_SPLIT_AND_SOURCE_IDENTITIES"
    assert len(result.split_sha256) == 64
    assert result.known_pattern_count == 1
    assert result.known_single_reference_matches == 1
    assert result.novel_pattern_count == 2
    assert result.novel_pattern_abstentions == 2
    assert result.outside_namespace_count == 1
    assert result.unseen_source_probe_count == 4

    assert by_id["h-known"].slice == "KNOWN_EXACT_PATTERN"
    assert by_id["h-known"].target_status == "TARGET_CONSTRUCTION_SUPPORTED"
    assert by_id["h-known"].single_reference_match is True
    assert by_id["h-known"].source_unseen_in_training is True
    assert by_id["h-combination"].slice == "NOVEL_COMBINATION_WITHIN_NAMESPACE"
    assert by_id["h-combination"].target_status == "UNKNOWN_TARGET_CONSTRUCTION"
    assert by_id["h-combination"].single_reference_match is None
    assert by_id["h-length"].slice == "NOVEL_LENGTH_WITHIN_NAMESPACE"
    assert by_id["h-length"].target_status == "UNKNOWN_TARGET_CONSTRUCTION"
    assert by_id["h-outside"].slice == "OUTSIDE_SEMANTIC_NAMESPACE"
    assert by_id["h-outside"].target_status == "OUTSIDE_TARGET_CONSTRUCTION_NAMESPACE"


def test_frozen_digest_rejects_posthoc_label_or_partition_changes():
    train, hold = training(), heldout()
    frozen = target_holdout_split_sha256(train, hold, **KW)

    altered_labels = (replace(hold[0], target_tokens=("forged",)), *hold[1:])
    with pytest.raises(ValueError, match="frozen split"):
        evaluate_target_construction_holdout(
            train, altered_labels, expected_split_sha256=frozen, **KW
        )
    with pytest.raises(ValueError, match="frozen split"):
        evaluate_target_construction_holdout(
            (*train, hold[0]), hold[1:], expected_split_sha256=frozen, **KW
        )


def test_no_episode_id_overlap_can_enter_holdout_even_with_refrozen_digest():
    train, hold = training(), heldout()
    duplicate = replace(hold[0], episode_id=train[0].episode_id)
    hold = (duplicate, *hold[1:])
    digest = target_holdout_split_sha256(train, hold, **KW)
    with pytest.raises(ValueError, match="overlap"):
        evaluate_target_construction_holdout(
            train, hold, expected_split_sha256=digest, **KW
        )


def test_multiple_realizations_do_not_inflate_single_reference_accuracy():
    train = list(training())
    for source in ("source-1", "source-2"):
        for index in (1, 2):
            train.append(sample(f"{source}-{index}-red-square-alt", source,
                                ("ctx:red", "shape:square"),
                                ("the", "red", "square")))
    result = evaluate(train, (heldout()[0],))
    row = result.rows[0]
    assert row.target_status == "MULTIPLE_TARGET_CONSTRUCTIONS_SUPPORTED"
    assert row.single_reference_match is None
    assert result.ambiguous_rendering_count == 1
    assert result.known_single_prediction_count == 0
    assert result.known_single_reference_matches == 0


def test_holdout_direct_dataclass_bypass_rejected_before_fitting():
    train, hold = training(), heldout()
    tampered = (replace(hold[0], source_id="  "), *hold[1:])
    with pytest.raises(ValueError, match="source_id"):
        target_holdout_split_sha256(train, tampered, **KW)
