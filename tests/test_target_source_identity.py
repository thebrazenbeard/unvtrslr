"""Identity controls for independent target-side evidence replication."""

from dataclasses import replace

import pytest

from unvtrslr.target_constructions import (
    TargetConstructionEpisode,
    fit_target_construction_model,
)
from unvtrslr.target_grounding import (
    NonEquivalenceObservation,
    TargetGroundingEpisode,
    fit_target_grounding_model,
)


def test_target_grounding_builder_rejects_missing_independent_source_id():
    with pytest.raises(ValueError, match="source_id"):
        TargetGroundingEpisode.build("demo-1", "", ["red"], ["ctx:red"])


def test_non_equivalence_builder_rejects_missing_independent_source_id():
    with pytest.raises(ValueError, match="source_id"):
        NonEquivalenceObservation.build("neq-1", "", "ctx:red", "single-token")


def test_target_construction_builder_rejects_missing_independent_source_id():
    with pytest.raises(ValueError, match="source_id"):
        TargetConstructionEpisode.build("demo-1", " ", ["ctx:red"], ["red"])


def test_target_grounding_fit_rechecks_direct_dataclass_source_ids():
    rows = [
        TargetGroundingEpisode.build(
            f"speaker-{index}", "speaker-1", ["red"], ["ctx:red"]
        )
        for index in (1, 2)
    ]
    # Public dataclass construction bypasses the build() entry point.
    rows.extend(
        replace(row, episode_id=f"missing-{index}", source_id="")
        for index, row in enumerate(tuple(rows), start=1)
    )
    with pytest.raises(ValueError, match="source_id"):
        fit_target_grounding_model(
            rows,
            target_language_id="opaque-target",
            semantic_atoms=["ctx:red"],
            upstream_model_ids=["translator-1"],
        )


def test_target_grounding_fit_rechecks_non_equivalence_source_ids():
    rows = [
        TargetGroundingEpisode.build("demo-1", "speaker-1", ["red"], ["ctx:red"]),
    ]
    observations = [
        NonEquivalenceObservation.build(
            f"noeq-{index}", "speaker-1", "ctx:red", "single-token"
        )
        for index in (1, 2)
    ]
    observations.extend(
        replace(row, observation_id=f"missing-{index}", source_id="")
        for index, row in enumerate(tuple(observations), start=1)
    )
    with pytest.raises(ValueError, match="source_id"):
        fit_target_grounding_model(
            rows,
            target_language_id="opaque-target",
            semantic_atoms=["ctx:red"],
            upstream_model_ids=["translator-1"],
            non_equivalence_observations=observations,
        )


def test_target_construction_fit_rechecks_direct_dataclass_source_ids():
    rows = [
        TargetConstructionEpisode.build(
            f"speaker-{index}", "speaker-1", ["ctx:red"], ["red"]
        )
        for index in (1, 2)
    ]
    rows.extend(
        replace(row, episode_id=f"missing-{index}", source_id="")
        for index, row in enumerate(tuple(rows), start=1)
    )
    with pytest.raises(ValueError, match="source_id"):
        fit_target_construction_model(
            rows,
            target_language_id="opaque-target",
            semantic_atoms=["ctx:red"],
            upstream_model_ids=["translator-1"],
        )
