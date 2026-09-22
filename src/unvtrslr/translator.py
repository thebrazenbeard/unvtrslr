from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Iterable, Mapping, Sequence

from .bridge import BridgeLearner, Episode
from .event_evidence import evidence_from_audio_event_result
from .events import discover_candidate_units
from .unit_model import (
    FrozenUnitModel,
    OutOfSampleUnitAssignment,
    assign_source_units,
    fit_frozen_unit_model,
    frozen_unit_model_from_dict,
)
from .unit_registry import LocalUnitEvidence, UnitRegistryResult


@dataclass(frozen=True)
class AcousticContextEpisode:
    episode_id: str
    source_id: str
    context: frozenset[str]
    evidence: tuple[LocalUnitEvidence, ...]

    @classmethod
    def build(
        cls,
        episode_id: str,
        source_id: str,
        context: Iterable[str],
        evidence: Iterable[LocalUnitEvidence],
    ) -> "AcousticContextEpisode":
        rows = tuple(evidence)
        if not rows:
            raise ValueError("episode must contain acoustic evidence")
        if any(row.source_id != source_id for row in rows):
            raise ValueError("episode source_id must match every evidence row")
        return cls(
            episode_id=str(episode_id),
            source_id=str(source_id),
            context=frozenset(str(item) for item in context),
            evidence=rows,
        )


@dataclass(frozen=True)
class FrozenSemanticRelation:
    token: str
    atom: str
    support: int
    positive_source_coverage: int
    p_atom_given_token: float
    p_atom_without_token: float
    effect: float
    information_bits: float


@dataclass(frozen=True)
class ReferenceTranslatorModel:
    schema: str
    model_id: str
    claim_ceiling: str
    acoustic_model: FrozenUnitModel
    semantic_min_sources: int
    semantic_relations: tuple[FrozenSemanticRelation, ...]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class ReferenceTranslation:
    status: str
    model_id: str
    acoustic_model_id: str
    global_units: tuple[str | None, ...]
    relations: tuple[str, ...]
    unresolved_local_units: tuple[str, ...]
    assignments: tuple[OutOfSampleUnitAssignment, ...]


def _relation_positive_sources(
    episodes: Sequence[Episode],
    token: str,
    atom: str,
) -> set[str]:
    return {
        str(episode.source)
        for episode in episodes
        if episode.source is not None
        and token in episode.signal
        and atom in episode.context
    }


def freeze_operational_relations(
    bridge: BridgeLearner,
    *,
    min_sources: int = 2,
) -> tuple[FrozenSemanticRelation, ...]:
    """Freeze only bridge relations with cross-source positive evidence."""
    if min_sources < 2:
        raise ValueError("min_sources must be >= 2")

    tokens = sorted(
        {
            token
            for episode in bridge.episodes
            for token in episode.signal
        }
    )
    relations: list[FrozenSemanticRelation] = []

    for token in tokens:
        inference = bridge.infer(token)
        if inference.status != "OPERATIONAL_RELATION_SUPPORTED":
            continue

        top = inference.candidates[0]
        positive_sources = _relation_positive_sources(
            bridge.episodes,
            token,
            top.atom,
        )
        if len(positive_sources) < min_sources:
            continue

        relations.append(
            FrozenSemanticRelation(
                token=token,
                atom=top.atom,
                support=top.support,
                positive_source_coverage=len(positive_sources),
                p_atom_given_token=top.p_atom_given_token,
                p_atom_without_token=top.p_atom_without_token,
                effect=top.effect,
                information_bits=top.information_bits,
            )
        )

    return tuple(relations)


def _translator_model_id(
    acoustic_model_id: str,
    semantic_min_sources: int,
    relations: Sequence[FrozenSemanticRelation],
) -> str:
    rows = [
        acoustic_model_id,
        str(int(semantic_min_sources)),
    ]
    for relation in sorted(
        relations,
        key=lambda row: (row.token, row.atom),
    ):
        rows.append(
            "|".join(
                [
                    relation.token,
                    relation.atom,
                    str(relation.support),
                    str(relation.positive_source_coverage),
                    repr(relation.p_atom_given_token),
                    repr(relation.p_atom_without_token),
                    repr(relation.effect),
                    repr(relation.information_bits),
                ]
            )
        )
    return "urt_" + sha256(
        "\n".join(rows).encode("utf-8")
    ).hexdigest()[:12]


def fit_reference_translator(
    episodes: Iterable[AcousticContextEpisode],
    *,
    semantic_min_sources: int = 2,
    min_sources: int = 2,
    min_units_per_source: int = 3,
    cluster_distance: float = 0.65,
    scale_floor: float = 0.25,
    match_threshold: float | None = None,
    acoustic_ambiguity_margin: float = 0.15,
    bridge_alpha: float = 0.5,
    bridge_min_support: int = 2,
    bridge_min_probability: float = 0.70,
    bridge_min_effect: float = 0.35,
    bridge_min_information_bits: float = 0.05,
    bridge_ambiguity_margin: float = 0.08,
) -> tuple[ReferenceTranslatorModel, UnitRegistryResult]:
    """Fit acoustic identity first, then ground only frozen global unit IDs."""
    materialized = list(episodes)
    if not materialized:
        raise ValueError("at least one acoustic/context episode is required")
    if semantic_min_sources < 2:
        raise ValueError("semantic_min_sources must be >= 2")
    if min_units_per_source < 3:
        raise ValueError(
            "end-to-end translation requires at least three "
            "acoustic contrasts per source"
        )

    evidence = [
        row
        for episode in materialized
        for row in episode.evidence
    ]
    acoustic_model, registry = fit_frozen_unit_model(
        evidence,
        min_sources=min_sources,
        min_units_per_source=min_units_per_source,
        cluster_distance=cluster_distance,
        scale_floor=scale_floor,
        match_threshold=match_threshold,
        ambiguity_margin=acoustic_ambiguity_margin,
    )

    assignment_by_key = {
        (
            assignment.recording_id,
            assignment.source_id,
            assignment.local_unit_id,
        ): assignment
        for assignment in registry.assignments
    }

    bridge_episodes: list[Episode] = []
    for episode in materialized:
        tokens: list[str] = []
        for row in episode.evidence:
            key = (
                row.recording_id,
                row.source_id,
                row.local_unit_id,
            )
            assignment = assignment_by_key.get(key)
            if assignment is None:
                raise ValueError("training evidence is missing from acoustic registry")
            if (
                assignment.status != "CROSS_SOURCE_UNIT_SUPPORTED"
                or assignment.global_unit_id is None
            ):
                raise ValueError(
                    "training episode contains an acoustic unit that did not "
                    "survive cross-source recurrence qualification"
                )
            tokens.append(assignment.global_unit_id)

        bridge_episodes.append(
            Episode.build(
                tokens,
                episode.context,
                source=episode.source_id,
            )
        )

    bridge = BridgeLearner(
        alpha=bridge_alpha,
        min_support=bridge_min_support,
        min_probability=bridge_min_probability,
        min_effect=bridge_min_effect,
        min_information_bits=bridge_min_information_bits,
        ambiguity_margin=bridge_ambiguity_margin,
    ).fit(bridge_episodes)

    semantic_relations = freeze_operational_relations(
        bridge,
        min_sources=semantic_min_sources,
    )
    if not semantic_relations:
        raise ValueError(
            "no operational relation survived the cross-source semantic gate"
        )

    model_id = _translator_model_id(
        acoustic_model.model_id,
        semantic_min_sources,
        semantic_relations,
    )
    model = ReferenceTranslatorModel(
        schema="UNVTRSLR_REFERENCE_TRANSLATOR_MODEL_V1",
        model_id=model_id,
        claim_ceiling=(
            "OUT_OF_SAMPLE_ACOUSTIC_MATCH_TO_CROSS_SOURCE_"
            "OPERATIONAL_RELATION_WITHIN_REFERENCE_FIXTURES"
        ),
        acoustic_model=acoustic_model,
        semantic_min_sources=semantic_min_sources,
        semantic_relations=semantic_relations,
    )
    return model, registry


def _evidence_key(row: LocalUnitEvidence) -> tuple[str, str, str]:
    return (row.recording_id, row.source_id, row.local_unit_id)


def translate_source_evidence(
    model: ReferenceTranslatorModel,
    evidence: Iterable[LocalUnitEvidence],
    *,
    query_keys: Sequence[tuple[str, str, str]] | None = None,
    renderer: Mapping[str, str] | None = None,
) -> ReferenceTranslation:
    """Translate selected local units after classifying a source as a batch."""
    rows = list(evidence)
    if not rows:
        raise ValueError("at least one local unit is required")

    sources = {row.source_id for row in rows}
    if len(sources) != 1:
        raise ValueError("translation batch must contain exactly one source")

    assignments = assign_source_units(
        model.acoustic_model,
        rows,
    )
    assignment_by_key = {
        (
            assignment.recording_id,
            assignment.source_id,
            assignment.local_unit_id,
        ): assignment
        for assignment in assignments
    }
    evidence_by_key = {_evidence_key(row): row for row in rows}

    selected_keys = (
        list(query_keys)
        if query_keys is not None
        else [_evidence_key(row) for row in rows]
    )
    if any(key not in evidence_by_key for key in selected_keys):
        raise ValueError("query key is not present in the translation batch")

    relation_by_token = {
        relation.token: relation
        for relation in model.semantic_relations
    }

    global_units: list[str | None] = []
    relations: list[str] = []
    unresolved: list[str] = []

    for key in selected_keys:
        assignment = assignment_by_key.get(key)
        label = f"{key[0]}:{key[2]}"

        if (
            assignment is None
            or assignment.status != "FROZEN_MATCH_SUPPORTED"
            or assignment.global_unit_id is None
        ):
            global_units.append(None)
            unresolved.append(label)
            continue

        global_units.append(assignment.global_unit_id)
        relation = relation_by_token.get(assignment.global_unit_id)
        if relation is None:
            unresolved.append(label)
            continue

        rendered = (
            renderer.get(relation.atom, relation.atom)
            if renderer is not None
            else relation.atom
        )
        if rendered not in relations:
            relations.append(rendered)

    if relations and not unresolved:
        status = "REFERENCE_TRANSLATION_SUPPORTED"
    elif relations:
        status = "PARTIAL_REFERENCE_TRANSLATION"
    else:
        status = "UNRESOLVED"

    return ReferenceTranslation(
        status=status,
        model_id=model.model_id,
        acoustic_model_id=model.acoustic_model.model_id,
        global_units=tuple(global_units),
        relations=tuple(relations),
        unresolved_local_units=tuple(unresolved),
        assignments=tuple(assignments),
    )


def reference_translator_model_from_dict(
    obj: Mapping,
) -> ReferenceTranslatorModel:
    acoustic_model = frozen_unit_model_from_dict(dict(obj["acoustic_model"]))
    relations = tuple(
        FrozenSemanticRelation(
            token=str(row["token"]),
            atom=str(row["atom"]),
            support=int(row["support"]),
            positive_source_coverage=int(row["positive_source_coverage"]),
            p_atom_given_token=float(row["p_atom_given_token"]),
            p_atom_without_token=float(row["p_atom_without_token"]),
            effect=float(row["effect"]),
            information_bits=float(row["information_bits"]),
        )
        for row in obj["semantic_relations"]
    )
    model = ReferenceTranslatorModel(
        schema=str(obj["schema"]),
        model_id=str(obj["model_id"]),
        claim_ceiling=str(obj["claim_ceiling"]),
        acoustic_model=acoustic_model,
        semantic_min_sources=int(obj["semantic_min_sources"]),
        semantic_relations=relations,
    )
    if model.schema != "UNVTRSLR_REFERENCE_TRANSLATOR_MODEL_V1":
        raise ValueError("unsupported reference translator model schema")
    if any(
        relation.positive_source_coverage < model.semantic_min_sources
        for relation in model.semantic_relations
    ):
        raise ValueError("persisted semantic relation violates source-coverage gate")
    expected = _translator_model_id(
        model.acoustic_model.model_id,
        model.semantic_min_sources,
        model.semantic_relations,
    )
    if expected != model.model_id:
        raise ValueError("reference translator model integrity check failed")
    return model


def prepare_audio_evidence(
    recording_id: str,
    source_id: str,
    samples,
    sample_rate: int,
    **event_kwargs,
) -> tuple[LocalUnitEvidence, ...]:
    """Raw-audio adapter using the exact acoustic/event stages in this lineage."""
    events = discover_candidate_units(
        samples,
        sample_rate,
        **event_kwargs,
    )
    return evidence_from_audio_event_result(
        recording_id,
        source_id,
        samples,
        sample_rate,
        events,
    )
