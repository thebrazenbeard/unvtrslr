from unvtrslr.bridge import BridgeLearner, Episode
from unvtrslr.translator import (
    AcousticContextEpisode,
    fit_reference_translator,
    freeze_operational_relations,
    reference_translator_model_from_dict,
    translate_source_evidence,
)
from unvtrslr.unit_registry import LocalUnitEvidence


def evidence(recording, source, vector):
    return LocalUnitEvidence(
        recording_id=recording,
        source_id=source,
        local_unit_id="u0",
        vector=tuple(vector),
    )


def training_episodes():
    rows = []

    # Source 1: three acoustic contrasts.
    s1_low = (-2.0, -1.0)
    s1_mid = (0.0, 0.0)
    s1_high = (2.0, 1.0)

    # Source 2: affine-shifted/scaled realization of the same three contrasts.
    s2_low = (80.0, -34.0)
    s2_mid = (100.0, -30.0)
    s2_high = (120.0, -26.0)

    contexts = [
        ("s1-low-a", "s1", s1_low, {"ctx:red", "shape:circle"}),
        ("s1-low-b", "s1", s1_low, {"ctx:red", "shape:triangle"}),
        ("s2-low-a", "s2", s2_low, {"ctx:red", "shape:star"}),
        ("s2-low-b", "s2", s2_low, {"ctx:red", "shape:hex"}),
        ("s1-high-a", "s1", s1_high, {"ctx:blue", "shape:square"}),
        ("s1-high-b", "s1", s1_high, {"ctx:green", "shape:square"}),
        ("s2-high-a", "s2", s2_high, {"ctx:yellow", "shape:square"}),
        ("s2-high-b", "s2", s2_high, {"ctx:purple", "shape:square"}),
        ("s1-mid-a", "s1", s1_mid, {"mid:a"}),
        ("s1-mid-b", "s1", s1_mid, {"mid:b"}),
        ("s2-mid-a", "s2", s2_mid, {"mid:c"}),
        ("s2-mid-b", "s2", s2_mid, {"mid:d"}),
    ]

    for recording, source, vector, context in contexts:
        rows.append(
            AcousticContextEpisode.build(
                recording,
                source,
                context,
                [evidence(recording, source, vector)],
            )
        )

    return rows


def fit_model():
    return fit_reference_translator(
        training_episodes(),
        cluster_distance=0.30,
        match_threshold=0.30,
    )[0]


def new_source_three_contrasts():
    return [
        evidence("s3-low", "s3", (980.0, 40.0)),
        evidence("s3-mid", "s3", (1000.0, 50.0)),
        evidence("s3-high", "s3", (1020.0, 60.0)),
    ]


def test_end_to_end_prepared_evidence_translates_cross_source_relations():
    model = fit_model()
    rows = new_source_three_contrasts()

    result = translate_source_evidence(
        model,
        rows,
        query_keys=[
            ("s3-low", "s3", "u0"),
            ("s3-high", "s3", "u0"),
        ],
        renderer={
            "ctx:red": "red",
            "shape:square": "square",
        },
    )

    assert result.status == "REFERENCE_TRANSLATION_SUPPORTED"
    assert result.relations == ("red", "square")
    assert result.unresolved_local_units == ()
    assert all(unit is not None for unit in result.global_units)


def test_same_local_id_strings_do_not_create_identity():
    model = fit_model()
    rows = new_source_three_contrasts()

    result = translate_source_evidence(
        model,
        rows,
        query_keys=[
            ("s3-low", "s3", "u0"),
            ("s3-high", "s3", "u0"),
        ],
    )

    assert len(set(result.global_units)) == 2


def test_one_unit_new_source_fails_closed_instead_of_translating():
    model = fit_model()
    row = evidence("single", "s3", (999.0, 999.0))

    result = translate_source_evidence(model, [row])

    assert result.status == "UNRESOLVED"
    assert result.global_units == (None,)
    assert result.unresolved_local_units == ("single:u0",)


def test_two_point_source_normalization_is_rejected_for_end_to_end_fit():
    try:
        fit_reference_translator(
            training_episodes(),
            min_units_per_source=2,
        )
    except ValueError as exc:
        assert "at least three acoustic contrasts" in str(exc)
    else:
        raise AssertionError("two-point source normalization should fail closed")


def test_cross_source_semantic_gate_rejects_one_source_positive_relation():
    episodes = []

    # Token g has enough statistical support for "ctx:red", but all positive
    # red evidence is from source s1. Source s2 observes g without red.
    for i in range(6):
        episodes.append(
            Episode.build(
                ["g"],
                ["ctx:red", f"s1-noise:{i}"],
                source="s1",
            )
        )
    for i in range(2):
        episodes.append(
            Episode.build(
                ["g"],
                [f"s2-other:{i}"],
                source="s2",
            )
        )

    # A contrasting token supplies negative evidence for red.
    for source in ("s1", "s2"):
        for i in range(4):
            episodes.append(
                Episode.build(
                    ["h"],
                    ["ctx:neutral", f"h-noise:{source}:{i}"],
                    source=source,
                )
            )

    bridge = BridgeLearner().fit(episodes)
    assert bridge.infer("g").status == "OPERATIONAL_RELATION_SUPPORTED"

    frozen = freeze_operational_relations(
        bridge,
        min_sources=2,
    )

    assert all(row.token != "g" for row in frozen)


def test_translator_model_roundtrip_preserves_inference_and_identity():
    model = fit_model()
    restored = reference_translator_model_from_dict(model.to_dict())
    rows = new_source_three_contrasts()

    original = translate_source_evidence(
        model,
        rows,
        query_keys=[
            ("s3-low", "s3", "u0"),
            ("s3-high", "s3", "u0"),
        ],
    )
    reloaded = translate_source_evidence(
        restored,
        rows,
        query_keys=[
            ("s3-low", "s3", "u0"),
            ("s3-high", "s3", "u0"),
        ],
    )

    assert restored.model_id == model.model_id
    assert reloaded == original


def test_translator_model_rejects_tampered_semantic_relation():
    model = fit_model()
    payload = model.to_dict()
    payload["semantic_relations"][0]["atom"] = "ctx:tampered"

    try:
        reference_translator_model_from_dict(payload)
    except ValueError as exc:
        assert "integrity" in str(exc)
    else:
        raise AssertionError("tampered translator model should fail")


def test_translator_model_rejects_tampered_claim_ceiling():
    model = fit_model()
    payload = model.to_dict()
    payload["claim_ceiling"] = "UNBOUNDED_TRANSLATION"

    try:
        reference_translator_model_from_dict(payload)
    except ValueError as exc:
        assert "claim ceiling" in str(exc)
    else:
        raise AssertionError("tampered claim ceiling should fail")


def test_translator_model_rejects_duplicate_token_relations():
    model = fit_model()
    payload = model.to_dict()
    payload["semantic_relations"] = (
        list(payload["semantic_relations"])
        + [dict(payload["semantic_relations"][0])]
    )

    try:
        reference_translator_model_from_dict(payload)
    except ValueError as exc:
        assert "duplicate token" in str(exc)
    else:
        raise AssertionError("duplicate token relation should fail")
