"""Frozen-split *synthetic* screen of target construction recall and abstention.

This evaluator deliberately fits on training rows only. Neither the source IDs
nor the caller-supplied frozen digest authenticate external collection, and a
successful screen is not evidence of productive grammar or grounded language.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import re
from typing import Iterable

from .target_constructions import (
    TargetConstructionEpisode,
    fit_target_construction_model,
    render_semantic_sequence,
)


@dataclass(frozen=True)
class TargetHoldoutRow:
    episode_id: str
    slice: str
    source_unseen_in_training: bool
    target_status: str
    single_reference_match: bool | None


@dataclass(frozen=True)
class TargetConstructionHoldoutReport:
    status: str
    provenance_status: str
    split_sha256: str
    fitted_model_id: str
    training_episode_count: int
    heldout_episode_count: int
    known_pattern_count: int
    known_single_prediction_count: int
    known_single_reference_matches: int
    novel_pattern_count: int
    novel_pattern_abstentions: int
    outside_namespace_count: int
    novel_atom_count: int
    unseen_source_probe_count: int
    ambiguous_rendering_count: int
    rows: tuple[TargetHoldoutRow, ...]


def _checked_rows(
    episodes: Iterable[TargetConstructionEpisode], label: str
) -> tuple[TargetConstructionEpisode, ...]:
    checked = []
    for row in episodes:
        if not isinstance(row, TargetConstructionEpisode):
            raise TypeError(f"{label} must contain TargetConstructionEpisode values")
        if not isinstance(row.episode_id, str) or not row.episode_id.strip():
            raise ValueError(f"{label} episode_id must not be empty")
        if not isinstance(row.source_id, str) or not row.source_id.strip():
            raise ValueError(f"{label} source_id must not be empty")
        # A direct dataclass constructor can bypass TargetConstructionEpisode
        # annotations. Rebuilding it via .build() would stringify arbitrary
        # objects and erase the distinction between a raw witness and its
        # textual representation before either hashing or fitting.
        if any(not isinstance(atom, str) for atom in row.semantic_atoms):
            raise ValueError(f"{label} semantic atom must be a string")
        if any(not isinstance(token, str) for token in row.target_tokens):
            raise ValueError(f"{label} target token must be a string")
        checked.append(
            TargetConstructionEpisode.build(
                row.episode_id, row.source_id, row.semantic_atoms, row.target_tokens
            )
        )
    return tuple(checked)


def _canonical_scope(
    *,
    target_language_id: str,
    semantic_atoms: Iterable[str],
    upstream_model_ids: Iterable[str],
    min_sources: int,
    min_positive_per_source: int,
) -> dict:
    if not isinstance(target_language_id, str) or not target_language_id.strip():
        raise ValueError("target_language_id must not be empty")
    if min_sources < 2 or min_positive_per_source < 1:
        raise ValueError("replication thresholds must be positive and min_sources >= 2")
    raw_namespace = tuple(semantic_atoms)
    raw_upstream = tuple(upstream_model_ids)
    if any(not isinstance(atom, str) for atom in raw_namespace):
        raise ValueError("semantic atom identifier must be a string")
    if any(not isinstance(model, str) for model in raw_upstream):
        raise ValueError("upstream model ID must be a string")
    namespace = sorted(set(raw_namespace))
    upstream = sorted(set(raw_upstream))
    if not namespace or any(not atom for atom in namespace):
        raise ValueError("semantic namespace must contain nonempty atoms")
    if not upstream or any(not model for model in upstream):
        raise ValueError("upstream_model_ids must contain nonempty IDs")
    return {
        "target_language_id": target_language_id,
        "semantic_atoms": namespace,
        "upstream_model_ids": upstream,
        "min_sources": min_sources,
        "min_positive_per_source": min_positive_per_source,
    }


def target_holdout_split_sha256(
    training: Iterable[TargetConstructionEpisode],
    heldout: Iterable[TargetConstructionEpisode],
    *,
    target_language_id: str,
    semantic_atoms: Iterable[str],
    upstream_model_ids: Iterable[str],
    min_sources: int = 2,
    min_positive_per_source: int = 2,
) -> str:
    """Content-bind the caller's train/test split, references and fit scope.

    The digest must be frozen externally before fitting. Generating a matching
    digest after seeing outcomes would be circular; this function cannot know
    whether the caller complied with that pre-registration requirement.
    """
    train = _checked_rows(training, "training")
    test = _checked_rows(heldout, "heldout")
    scope = _canonical_scope(
        target_language_id=target_language_id,
        semantic_atoms=semantic_atoms,
        upstream_model_ids=upstream_model_ids,
        min_sources=min_sources,
        min_positive_per_source=min_positive_per_source,
    )
    payload = {
        "schema": "UNVTRSLR_TARGET_HOLDOUT_SPLIT_V1",
        "fit_scope": scope,
        "training": [asdict(row) for row in sorted(train, key=lambda r: r.episode_id)],
        "heldout": [asdict(row) for row in sorted(test, key=lambda r: r.episode_id)],
    }
    return sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        .encode("utf-8")
    ).hexdigest()


def evaluate_target_construction_holdout(
    training: Iterable[TargetConstructionEpisode],
    heldout: Iterable[TargetConstructionEpisode],
    *,
    expected_split_sha256: str,
    target_language_id: str,
    semantic_atoms: Iterable[str],
    upstream_model_ids: Iterable[str],
    min_sources: int = 2,
    min_positive_per_source: int = 2,
) -> TargetConstructionHoldoutReport:
    """Measure exact recall and unknown abstention without training on holdout.

    Unknown combinations are an *abstention control* here, not generalization
    success. Only a single learned realization is scored for reference-token
    agreement; multiple realizations are recorded but never scored as a guess.
    """
    train = _checked_rows(training, "training")
    test = _checked_rows(heldout, "heldout")
    if not train or not test:
        raise ValueError("training and heldout must both be nonempty")
    scope = _canonical_scope(
        target_language_id=target_language_id,
        semantic_atoms=semantic_atoms,
        upstream_model_ids=upstream_model_ids,
        min_sources=min_sources,
        min_positive_per_source=min_positive_per_source,
    )
    actual_split_sha256 = target_holdout_split_sha256(train, test, **scope)
    if not isinstance(expected_split_sha256, str) or not re.fullmatch(
        "[0-9a-f]{64}", expected_split_sha256
    ) or actual_split_sha256 != expected_split_sha256:
        raise ValueError("frozen split SHA-256 mismatch; evaluation is blocked")

    train_ids = [row.episode_id for row in train]
    test_ids = [row.episode_id for row in test]
    if len(set(train_ids)) != len(train_ids) or len(set(test_ids)) != len(test_ids):
        raise ValueError("duplicate episode IDs within training or heldout")
    if set(train_ids).intersection(test_ids):
        raise ValueError("episode_id overlap between training and heldout")

    model = fit_target_construction_model(train, **scope)
    train_patterns = {row.semantic_atoms for row in train}
    train_lengths = {len(row.semantic_atoms) for row in train}
    train_atoms = {atom for row in train for atom in row.semantic_atoms}
    train_sources = {row.source_id for row in train}
    namespace = set(model.semantic_atoms)

    rows: list[TargetHoldoutRow] = []
    known_count = known_predicted = known_matched = novel_count = novel_abstained = 0
    outside_count = novel_atom_count = unseen_source = ambiguous_count = 0
    for episode in test:
        pattern = episode.semantic_atoms
        if any(atom not in namespace for atom in pattern):
            slice_name = "OUTSIDE_SEMANTIC_NAMESPACE"
            outside_count += 1
        elif any(atom not in train_atoms for atom in pattern):
            slice_name = "NOVEL_ATOM_WITHIN_NAMESPACE"
            novel_atom_count += 1
        elif pattern in train_patterns:
            slice_name = "KNOWN_EXACT_PATTERN"
            known_count += 1
        elif len(pattern) not in train_lengths:
            slice_name = "NOVEL_LENGTH_WITHIN_NAMESPACE"
            novel_count += 1
        else:
            slice_name = "NOVEL_COMBINATION_WITHIN_NAMESPACE"
            novel_count += 1

        observed = render_semantic_sequence(model, pattern)
        is_single = (
            observed.status == "TARGET_CONSTRUCTION_SUPPORTED"
            and len(observed.realizations) == 1
        )
        match = (observed.realizations[0] == episode.target_tokens) if is_single else None
        if slice_name == "KNOWN_EXACT_PATTERN" and is_single:
            known_predicted += 1
            known_matched += bool(match)
        if slice_name in ("NOVEL_COMBINATION_WITHIN_NAMESPACE", "NOVEL_LENGTH_WITHIN_NAMESPACE"):
            novel_abstained += observed.status == "UNKNOWN_TARGET_CONSTRUCTION"
        if observed.status == "MULTIPLE_TARGET_CONSTRUCTIONS_SUPPORTED":
            ambiguous_count += 1
        shifted = episode.source_id not in train_sources
        unseen_source += shifted
        rows.append(
            TargetHoldoutRow(
                episode_id=episode.episode_id,
                slice=slice_name,
                source_unseen_in_training=shifted,
                target_status=observed.status,
                single_reference_match=match,
            )
        )

    return TargetConstructionHoldoutReport(
        status="REFERENCE_HOLDOUT_SCREEN_ONLY",
        provenance_status="CALLER_ASSERTED_SPLIT_AND_SOURCE_IDENTITIES",
        split_sha256=actual_split_sha256,
        fitted_model_id=model.model_id,
        training_episode_count=len(train),
        heldout_episode_count=len(test),
        known_pattern_count=known_count,
        known_single_prediction_count=known_predicted,
        known_single_reference_matches=known_matched,
        novel_pattern_count=novel_count,
        novel_pattern_abstentions=novel_abstained,
        outside_namespace_count=outside_count,
        novel_atom_count=novel_atom_count,
        unseen_source_probe_count=unseen_source,
        ambiguous_rendering_count=ambiguous_count,
        rows=tuple(rows),
    )
