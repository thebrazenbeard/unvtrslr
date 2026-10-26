from types import SimpleNamespace

import pytest

from unvtrslr.unit_registry import (
    LocalUnitEvidence,
    build_unit_registry,
    evidence_from_event_result,
)


def rows_two_sources():
    # Same two relative acoustic states under large source offset/scale changes.
    return [
        LocalUnitEvidence("r1", "s1", "u0", (-1.0, -0.5)),
        LocalUnitEvidence("r1", "s1", "u1", (1.0, 0.5)),
        LocalUnitEvidence("r2", "s2", "u0", (90.0, -32.0)),
        LocalUnitEvidence("r2", "s2", "u1", (110.0, -28.0)),
    ]


def test_cross_source_relative_states_receive_shared_registry_ids():
    result = build_unit_registry(
        rows_two_sources(),
        cluster_distance=0.25,
    )
    by_local = {
        (a.source_id, a.local_unit_id): a
        for a in result.assignments
    }

    assert (
        by_local[("s1", "u0")].global_unit_id
        == by_local[("s2", "u0")].global_unit_id
    )
    assert (
        by_local[("s1", "u1")].global_unit_id
        == by_local[("s2", "u1")].global_unit_id
    )
    assert (
        by_local[("s1", "u0")].global_unit_id
        != by_local[("s1", "u1")].global_unit_id
    )
    assert all(
        a.status == "CROSS_SOURCE_UNIT_SUPPORTED"
        for a in result.assignments
    )


def test_input_order_does_not_change_assignments():
    a = build_unit_registry(
        rows_two_sources(),
        cluster_distance=0.25,
    ).to_dict()
    b = build_unit_registry(
        list(reversed(rows_two_sources())),
        cluster_distance=0.25,
    ).to_dict()

    assert a == b


def test_source_local_extra_unit_is_not_promoted_globally():
    rows = rows_two_sources() + [
        LocalUnitEvidence(
            "r1",
            "s1",
            "u2",
            (8.0, 8.0),
        ),
    ]
    result = build_unit_registry(
        rows,
        cluster_distance=0.25,
    )
    extra = next(
        a
        for a in result.assignments
        if a.source_id == "s1"
        and a.local_unit_id == "u2"
    )

    assert extra.global_unit_id is None
    assert extra.status == "SOURCE_LOCAL_ONLY"
    assert extra.source_coverage == 1


def test_single_unit_source_fails_closed_instead_of_zero_center_matching():
    rows = rows_two_sources() + [
        LocalUnitEvidence(
            "r3",
            "s3",
            "u0",
            (999.0, 999.0),
        ),
    ]
    result = build_unit_registry(
        rows,
        cluster_distance=0.25,
    )
    row = next(
        a
        for a in result.assignments
        if a.source_id == "s3"
    )

    assert (
        row.status
        == "INSUFFICIENT_SOURCE_CONTRAST"
    )
    assert row.global_unit_id is None


def test_event_adapter_aggregates_repeated_local_unit_events():
    events = [
        SimpleNamespace(vector=(0.0, 0.0)),
        SimpleNamespace(vector=(0.2, 0.2)),
        SimpleNamespace(vector=(3.0, 4.0)),
    ]
    units = [
        SimpleNamespace(
            event_index=0,
            unit_id="u0",
        ),
        SimpleNamespace(
            event_index=1,
            unit_id="u0",
        ),
        SimpleNamespace(
            event_index=2,
            unit_id="u1",
        ),
    ]
    result = SimpleNamespace(
        events=events,
        units=units,
    )

    evidence = evidence_from_event_result(
        "rec",
        "speaker",
        result,
    )
    by_id = {
        row.local_unit_id: row
        for row in evidence
    }

    assert by_id["u0"].vector == (0.1, 0.1)
    assert by_id["u1"].vector == (3.0, 4.0)


def test_global_ids_are_registry_local_evidence_ids_not_semantic_labels():
    result = build_unit_registry(
        rows_two_sources(),
        cluster_distance=0.25,
    )

    assert result.claim_ceiling == (
        "CROSS_RECORDING_ACOUSTIC_"
        "RECURRENCE_ONLY_NO_SEMANTIC_IDENTITY"
    )
    assert all(
        a.global_unit_id is None
        or a.global_unit_id.startswith("g_")
        for a in result.assignments
    )


def test_two_distinct_unit_ids_with_identical_measurements_are_not_source_contrast():
    """Source diversity is not established by arbitrary local-unit labels."""
    rows = [
        LocalUnitEvidence("r1", "source-1", "u0", (0.0, 0.0)),
        LocalUnitEvidence("r1", "source-1", "u1", (0.0, 0.0)),
        LocalUnitEvidence("r2", "source-2", "u0", (10.0, 20.0)),
        LocalUnitEvidence("r2", "source-2", "u1", (10.0, 20.0)),
    ]

    result = build_unit_registry(rows)

    assert result.eligible_source_count == 0
    assert result.excluded_source_count == 2
    assert all(a.global_unit_id is None for a in result.assignments)
    assert {a.status for a in result.assignments} == {"INSUFFICIENT_SOURCE_CONTRAST"}


def test_subscale_nuisance_jitter_does_not_fabricate_independent_source_contrast():
    rows = [
        LocalUnitEvidence("r1", "source-1", "u0", (0.0, 0.0)),
        LocalUnitEvidence("r1", "source-1", "u1", (1e-8, -1e-8)),
        LocalUnitEvidence("r2", "source-2", "u0", (0.0, 0.0)),
        LocalUnitEvidence("r2", "source-2", "u1", (3.0, 3.0)),
    ]

    result = build_unit_registry(rows, scale_floor=0.25)

    assert result.eligible_source_count == 1
    assert result.excluded_source_count == 1
    assert all(a.global_unit_id is None for a in result.assignments)
    assert all(a.status == "INSUFFICIENT_SOURCE_CONTRAST"
               for a in result.assignments if a.source_id == "source-1")


@pytest.mark.parametrize("invalid_id", ["", " ", "\t"])
def test_unnamed_source_cannot_supply_independent_cross_source_coverage(invalid_id):
    rows = [
        LocalUnitEvidence("r1", "source-1", "u0", (0.0,)),
        LocalUnitEvidence("r1", "source-1", "u1", (1.0,)),
        LocalUnitEvidence("r2", invalid_id, "u0", (0.0,)),
        LocalUnitEvidence("r2", invalid_id, "u1", (1.0,)),
    ]
    with pytest.raises(ValueError, match="source_id"):
        build_unit_registry(rows)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_source_vectors_are_rejected_before_normalization(bad):
    rows = rows_two_sources()
    rows[0] = LocalUnitEvidence("r1", "s1", "u0", (bad, 0.0))
    with pytest.raises(ValueError, match="finite"):
        build_unit_registry(rows)
