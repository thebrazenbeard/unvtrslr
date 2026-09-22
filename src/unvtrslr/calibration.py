from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Iterable, Mapping, Sequence

import numpy as np

from .information import conditional_mutual_information, mutual_information


@dataclass(frozen=True)
class FingerprintObservation:
    observation_id: str
    system_id: str
    source_id: str
    fingerprint: Mapping
    content_id: str | None = None
    family_id: str | None = None


@dataclass(frozen=True)
class FeatureAssociation:
    feature: str
    observations: int
    raw_mutual_information_bits: float
    conditional_mutual_information_bits: float
    normalized_conditional_information: float
    null_mean_bits: float
    null_std_bits: float
    null_z: float | None
    status: str


@dataclass(frozen=True)
class CalibrationReport:
    schema: str
    claim_ceiling: str
    target: str
    nuisance_fields: tuple[str, ...]
    observation_count: int
    system_count: int
    source_count: int
    identifiability_status: str
    features: tuple[FeatureAssociation, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def _nested(mapping: Mapping, *path: str):
    cur = mapping
    for part in path:
        if not isinstance(cur, Mapping) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _numeric(value) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if np.isfinite(out) else None


def fingerprint_scalars(fingerprint: Mapping) -> dict[str, float]:
    """Flatten auditable scalar measurements from Acoustic Fingerprint V1.

    Raw absolute pitch is retained as a calibration feature rather than silently
    discarded. Source-relative pitch is kept separately so nuisance conditioning
    can reveal which view generalizes better in a particular corpus.
    """
    ch = fingerprint.get("channels", {}) if isinstance(fingerprint, Mapping) else {}
    result: dict[str, float] = {}

    paths = {
        "voiced_frame_fraction": ("__root__", "voiced_frame_fraction"),
        "pitch_raw_median_hz": ("pitch_raw_hz", "median"),
        "pitch_raw_iqr_hz": ("pitch_raw_hz", "iqr"),
        "pitch_relative_iqr_st": ("pitch_relative_semitones", "iqr"),
        "pitch_relative_std_st": ("pitch_relative_semitones", "std"),
        "pitch_relative_slope": ("pitch_relative_semitones", "slope"),
        "pitch_relative_curvature": ("pitch_relative_semitones", "curvature"),
        "pitch_relative_range_st": ("pitch_relative_semitones", "range"),
        "intensity_median_db": ("intensity_db", "median"),
        "intensity_iqr_db": ("intensity_db", "iqr"),
        "intensity_std_db": ("intensity_db", "std"),
        "intensity_slope": ("intensity_db", "slope"),
        "intensity_range_db": ("intensity_db", "range"),
        "periodicity_median": ("periodicity", "median"),
        "periodicity_iqr": ("periodicity", "iqr"),
        "spectral_centroid_median_hz": ("spectral_centroid_hz", "median"),
        "spectral_centroid_iqr_hz": ("spectral_centroid_hz", "iqr"),
        "spectral_bandwidth_median_hz": ("spectral_bandwidth_hz", "median"),
        "spectral_bandwidth_iqr_hz": ("spectral_bandwidth_hz", "iqr"),
        "spectral_flatness_median": ("spectral_flatness", "median"),
        "spectral_flatness_iqr": ("spectral_flatness", "iqr"),
        "spectral_rolloff_median_hz": ("spectral_rolloff_hz", "median"),
        "spectral_slope_median_db_octave": ("spectral_slope_db_octave", "median"),
        "h1_h2_median_db": ("h1_h2_db", "median"),
        "h1_h2_iqr_db": ("h1_h2_db", "iqr"),
        "envelope_modulation_peak_hz": ("__channel_scalar__", "envelope_modulation_peak_hz"),
    }

    for name, path in paths.items():
        if path[0] == "__root__":
            value = fingerprint.get(path[1])
        elif path[0] == "__channel_scalar__":
            value = ch.get(path[1]) if isinstance(ch, Mapping) else None
        else:
            value = _nested(ch, path[0], path[1])
        number = _numeric(value)
        if number is not None:
            result[name] = number

    mfcc = ch.get("mfcc", []) if isinstance(ch, Mapping) else []
    if isinstance(mfcc, Sequence):
        for row in mfcc:
            if not isinstance(row, Mapping):
                continue
            idx = row.get("index")
            if not isinstance(idx, int):
                continue
            for stat in ("median", "iqr", "std"):
                number = _numeric(row.get(stat))
                if number is not None:
                    result[f"mfcc_{idx}_{stat}"] = number

    return result


def _quantile_bins(values: Sequence[float], max_bins: int = 4) -> list[int]:
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        return []
    unique = np.unique(arr)
    if len(unique) <= 1:
        return [0] * len(arr)
    bins = min(max_bins, len(unique), max(2, int(round(np.sqrt(len(arr))))))
    edges = np.unique(np.quantile(arr, np.linspace(0.0, 1.0, bins + 1)[1:-1]))
    if len(edges) == 0:
        return [0] * len(arr)
    return np.digitize(arr, edges, right=False).astype(int).tolist()


def _attr(obs: FingerprintObservation, name: str) -> str | None:
    if name not in {"system_id", "source_id", "content_id", "family_id"}:
        raise ValueError(f"unsupported observation field: {name}")
    return getattr(obs, name)


def _identifiability(observations: Sequence[FingerprintObservation], target: str, nuisances: Sequence[str]) -> str:
    target_values = [_attr(obs, target) for obs in observations]
    if any(value is None for value in target_values):
        return "TARGET_FIELD_INCOMPLETE"
    if len(set(target_values)) < 2:
        return "TARGET_HAS_SINGLE_CLASS"

    nuisance_tuples = [tuple(_attr(obs, field) for field in nuisances) for obs in observations]
    if any(any(value is None for value in z) for z in nuisance_tuples):
        return "NUISANCE_FIELD_INCOMPLETE"

    by_nuisance: dict[tuple, set[str]] = {}
    for y, z in zip(target_values, nuisance_tuples):
        by_nuisance.setdefault(z, set()).add(str(y))
    if all(len(values) < 2 for values in by_nuisance.values()):
        return "TARGET_CONFOUNDED_WITH_NUISANCE"
    return "IDENTIFIABLE_WITHIN_OBSERVED_STRATA"


def _permuted_targets_within_strata(
    targets: Sequence[str],
    strata: Sequence[tuple],
    *,
    rng: np.random.Generator,
) -> list[str]:
    out = list(targets)
    groups: dict[tuple, list[int]] = {}
    for i, z in enumerate(strata):
        groups.setdefault(z, []).append(i)
    for idxs in groups.values():
        shuffled = [targets[i] for i in idxs]
        rng.shuffle(shuffled)
        for i, value in zip(idxs, shuffled):
            out[i] = value
    return out


def calibrate_feature_information(
    observations: Iterable[FingerprintObservation],
    *,
    target: str = "system_id",
    nuisance_fields: Sequence[str] = ("source_id",),
    max_bins: int = 4,
    permutations: int = 128,
    seed: int = 0,
    min_observations: int = 8,
) -> CalibrationReport:
    """Rank acoustic dimensions by nuisance-conditioned target information."""
    obs = sorted(list(observations), key=lambda o: o.observation_id)
    if not obs:
        raise ValueError("at least one observation is required")
    if permutations < 0:
        raise ValueError("permutations must be >= 0")

    ident = _identifiability(obs, target, nuisance_fields)
    targets = [str(_attr(o, target)) for o in obs]
    strata = [tuple(_attr(o, field) for field in nuisance_fields) for o in obs]

    flattened = [fingerprint_scalars(o.fingerprint) for o in obs]
    feature_names = sorted({name for row in flattened for name in row})
    associations: list[FeatureAssociation] = []
    rng = np.random.default_rng(seed)

    for feature in feature_names:
        selected = [(i, row[feature]) for i, row in enumerate(flattened) if feature in row]
        if len(selected) < min_observations:
            associations.append(
                FeatureAssociation(feature, len(selected), 0.0, 0.0, 0.0, 0.0, 0.0, None, "INSUFFICIENT_OBSERVATIONS")
            )
            continue

        idxs = [i for i, _ in selected]
        values = [value for _, value in selected]
        x = _quantile_bins(values, max_bins=max_bins)
        y = [targets[i] for i in idxs]
        z = [strata[i] for i in idxs]

        if len(set(x)) < 2:
            associations.append(
                FeatureAssociation(feature, len(selected), 0.0, 0.0, 0.0, 0.0, 0.0, None, "CONSTANT_AFTER_BINNING")
            )
            continue

        raw_mi = mutual_information(x, y)
        cmi = conditional_mutual_information(x, y, z)
        target_entropy_within = conditional_mutual_information(y, y, z)
        normalized = cmi / target_entropy_within if target_entropy_within > 0 else 0.0

        null = []
        for _ in range(permutations):
            perm_y = _permuted_targets_within_strata(y, z, rng=rng)
            null.append(conditional_mutual_information(x, perm_y, z))
        null_mean = float(np.mean(null)) if null else 0.0
        null_std = float(np.std(null)) if null else 0.0
        null_z = None if null_std <= 1e-12 else float((cmi - null_mean) / null_std)

        if ident != "IDENTIFIABLE_WITHIN_OBSERVED_STRATA":
            status = ident
        elif cmi <= null_mean + max(1e-9, 2.0 * null_std):
            status = "NO_CLEAR_INFORMATION_ABOVE_NULL"
        else:
            status = "CONDITIONAL_INFORMATION_SUPPORTED"

        associations.append(
            FeatureAssociation(
                feature=feature,
                observations=len(selected),
                raw_mutual_information_bits=float(raw_mi),
                conditional_mutual_information_bits=float(cmi),
                normalized_conditional_information=float(normalized),
                null_mean_bits=null_mean,
                null_std_bits=null_std,
                null_z=null_z,
                status=status,
            )
        )

    associations.sort(
        key=lambda row: (
            row.conditional_mutual_information_bits - row.null_mean_bits,
            row.normalized_conditional_information,
            row.feature,
        ),
        reverse=True,
    )

    return CalibrationReport(
        schema="UNVTRSLR_CROSSLINGUISTIC_CALIBRATION_V1",
        claim_ceiling="KNOWN_SYSTEM_MEASUREMENT_PRIOR_ONLY_NO_UNKNOWN_SEMANTIC_DECODING",
        target=target,
        nuisance_fields=tuple(nuisance_fields),
        observation_count=len(obs),
        system_count=len({o.system_id for o in obs}),
        source_count=len({o.source_id for o in obs}),
        identifiability_status=ident,
        features=tuple(associations),
    )


@dataclass(frozen=True)
class FeatureInteraction:
    feature_a: str
    feature_b: str
    observations: int
    joint_conditional_information_bits: float
    best_individual_information_bits: float
    joint_gain_over_best_bits: float
    null_mean_bits: float
    null_std_bits: float
    null_z: float | None
    status: str


def calibrate_pairwise_interactions(
    observations: Iterable[FingerprintObservation],
    *,
    target: str = "system_id",
    nuisance_fields: Sequence[str] = ("source_id",),
    feature_names: Sequence[str] | None = None,
    max_bins: int = 3,
    permutations: int = 128,
    seed: int = 0,
    min_observations: int = 12,
    min_joint_gain_bits: float = 0.05,
    min_joint_state_count: int = 2,
    max_pairs: int | None = None,
) -> tuple[FeatureInteraction, ...]:
    """Find feature pairs whose joint information exceeds either feature alone.

    This is deliberately a joint-gain diagnostic, not a claim of unique
    information-theoretic synergy. It catches simple combinatorial/XOR-like codes
    while avoiding that stronger decomposition claim.
    """
    obs = sorted(list(observations), key=lambda o: o.observation_id)
    if not obs:
        raise ValueError("at least one observation is required")
    if permutations < 0:
        raise ValueError("permutations must be >= 0")

    ident = _identifiability(obs, target, nuisance_fields)
    targets = [str(_attr(o, target)) for o in obs]
    strata = [tuple(_attr(o, field) for field in nuisance_fields) for o in obs]
    flattened = [fingerprint_scalars(o.fingerprint) for o in obs]

    available = sorted({name for row in flattened for name in row})
    if feature_names is not None:
        requested = set(feature_names)
        available = [name for name in available if name in requested]

    pairs = [
        (available[i], available[j])
        for i in range(len(available))
        for j in range(i + 1, len(available))
    ]
    if max_pairs is not None:
        pairs = pairs[: max(0, int(max_pairs))]

    rng = np.random.default_rng(seed)
    results: list[FeatureInteraction] = []

    for feature_a, feature_b in pairs:
        selected = [
            (i, row[feature_a], row[feature_b])
            for i, row in enumerate(flattened)
            if feature_a in row and feature_b in row
        ]
        if len(selected) < min_observations:
            continue

        idxs = [i for i, _, _ in selected]
        xa = _quantile_bins([a for _, a, _ in selected], max_bins=max_bins)
        xb = _quantile_bins([b for _, _, b in selected], max_bins=max_bins)
        if len(set(xa)) < 2 or len(set(xb)) < 2:
            continue

        joint = list(zip(xa, xb))
        y = [targets[i] for i in idxs]
        z = [strata[i] for i in idxs]

        cell_counts: dict[tuple, int] = {}
        for joint_state, nuisance_state in zip(joint, z):
            key = (nuisance_state, joint_state)
            cell_counts[key] = cell_counts.get(key, 0) + 1
        sparse_joint = bool(cell_counts) and min(cell_counts.values()) < min_joint_state_count

        ia = conditional_mutual_information(xa, y, z)
        ib = conditional_mutual_information(xb, y, z)
        ij = conditional_mutual_information(joint, y, z)
        best = max(ia, ib)
        gain = max(0.0, ij - best)

        null = []
        for _ in range(permutations):
            perm_y = _permuted_targets_within_strata(y, z, rng=rng)
            null.append(conditional_mutual_information(joint, perm_y, z))
        null_mean = float(np.mean(null)) if null else 0.0
        null_std = float(np.std(null)) if null else 0.0
        null_z = None if null_std <= 1e-12 else float((ij - null_mean) / null_std)

        if ident != "IDENTIFIABLE_WITHIN_OBSERVED_STRATA":
            status = ident
        elif sparse_joint:
            status = "SPARSE_JOINT_STATE_UNIDENTIFIABLE"
        elif ij <= null_mean + max(1e-9, 2.0 * null_std):
            status = "NO_CLEAR_JOINT_INFORMATION_ABOVE_NULL"
        elif gain < min_joint_gain_bits:
            status = "JOINT_INFORMATION_REDUNDANT_WITH_BEST_INDIVIDUAL"
        else:
            status = "JOINT_GAIN_SUPPORTED"

        results.append(
            FeatureInteraction(
                feature_a=feature_a,
                feature_b=feature_b,
                observations=len(selected),
                joint_conditional_information_bits=float(ij),
                best_individual_information_bits=float(best),
                joint_gain_over_best_bits=float(gain),
                null_mean_bits=null_mean,
                null_std_bits=null_std,
                null_z=null_z,
                status=status,
            )
        )

    results.sort(
        key=lambda row: (
            row.joint_gain_over_best_bits,
            row.joint_conditional_information_bits - row.null_mean_bits,
            row.feature_a,
            row.feature_b,
        ),
        reverse=True,
    )
    return tuple(results)
