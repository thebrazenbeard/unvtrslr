"""Conservative R1 substrate comparison, *not* an R2 grounding evaluator.

Inputs are independently generated candidate evidence summaries. This module
checks comparability and screens Pareto dominance; it cannot authenticate a
holdout, compute R2 metrics, verify provenance, or select a grounded substrate.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Mapping


_SUBSTRATES = frozenset(("TPH", "DCA", "PIS"))
_REQUIRED_COMPLEXITY = frozenset((
    "serialized_representation_bytes",
    "fixed_primitive_count",
    "learned_primitive_count",
    "candidate_specific_trainable_parameters",
    "peak_memory_bytes",
    "compute_per_interaction",
    "interactions_to_qualification",
    "adapter_complexity",
    "human_authored_ontology_bytes",
))


def _digest(value: str, field: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError(f"{field} must be a lowercase SHA-256 hex digest")


def _finite_number(value: object) -> bool:
    """Handle arbitrarily large integers without leaking an OverflowError."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return isfinite(value)
    except OverflowError:
        return False


def _nonnegative(value: float, field: str) -> None:
    if not _finite_number(value) or value < 0:
        raise ValueError(f"{field} must be a finite nonnegative number")


def _unique_nonempty(values: tuple[str, ...], field: str) -> None:
    if not values or any(not isinstance(value, str) or not value for value in values):
        raise ValueError(f"{field} requires nonempty names")
    if len(values) != len(set(values)):
        raise ValueError(f"{field} contains duplicates")


@dataclass(frozen=True)
class MetricSpec:
    name: str
    direction: str  # HIGHER or LOWER; all candidates must share the same rule.
    noninferiority_margin: float

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("metric name is required")
        if self.direction not in ("HIGHER", "LOWER"):
            raise ValueError("metric direction must be HIGHER or LOWER")
        _nonnegative(self.noninferiority_margin, "noninferiority_margin")


@dataclass(frozen=True)
class ComplexitySpec:
    name: str
    unit: str
    materiality_margin: float

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("complexity name is required")
        if not isinstance(self.unit, str) or not self.unit:
            raise ValueError("complexity accounting requires explicit units")
        _nonnegative(self.materiality_margin, "materiality_margin")


@dataclass(frozen=True)
class ComparisonProfile:
    profile_digest: str  # Frozen preregistration artifact, not computed here.
    suite_digest: str  # Exact common challenge suite artifact.
    episode_batch_digest: str  # Exact evaluation-world membership/seed-set artifact.
    learner_surface_digest: str  # E1/E2 inputs, affordances, channel, feedback, budget.
    critical_tests: tuple[str, ...]
    metrics: tuple[MetricSpec, ...]
    complexity: tuple[ComplexitySpec, ...]
    min_independent_runs: int

    def __post_init__(self) -> None:
        for field in ("critical_tests", "metrics", "complexity"):
            object.__setattr__(self, field, tuple(getattr(self, field)))
        _digest(self.profile_digest, "profile_digest")
        _digest(self.suite_digest, "suite_digest")
        _digest(self.episode_batch_digest, "episode_batch_digest")
        _digest(self.learner_surface_digest, "learner_surface_digest")
        _unique_nonempty(self.critical_tests, "critical_tests")
        _unique_nonempty(tuple(m.name for m in self.metrics), "metrics")
        names = tuple(c.name for c in self.complexity)
        _unique_nonempty(names, "complexity")
        missing = _REQUIRED_COMPLEXITY - set(names)
        if missing:
            raise ValueError(f"complexity missing required accounting: {sorted(missing)}")
        if type(self.min_independent_runs) is not int or self.min_independent_runs < 2:
            raise ValueError("min_independent_runs must be at least two")


@dataclass(frozen=True)
class CandidateEvaluation:
    substrate_id: str
    profile_digest: str
    suite_digest: str
    episode_batch_digest: str
    learner_surface_digest: str
    learner_code_digest: str
    independent_run_count: int
    critical_test_passes: Mapping[str, bool]
    metric_intervals: Mapping[str, tuple[float, float]]
    complexity: Mapping[str, float]

    def __post_init__(self) -> None:
        if self.substrate_id not in _SUBSTRATES:
            raise ValueError("substrate_id must be TPH, DCA, or PIS")
        for field in ("profile_digest", "suite_digest", "episode_batch_digest", "learner_surface_digest", "learner_code_digest"):
            _digest(getattr(self, field), field)
        if type(self.independent_run_count) is not int or self.independent_run_count < 1:
            raise ValueError("independent_run_count must be a positive integer")
        # Copy to disallow post-validation changes to a supplied mutable mapping.
        for field in ("critical_test_passes", "metric_intervals", "complexity"):
            supplied = getattr(self, field)
            if not isinstance(supplied, Mapping):
                raise ValueError(f"{field} must be a mapping")
            copied = dict(supplied)
            if field == "metric_intervals":
                copied = {
                    name: tuple(interval) if isinstance(interval, (tuple, list)) else interval
                    for name, interval in copied.items()
                }
            object.__setattr__(self, field, MappingProxyType(copied))


@dataclass(frozen=True)
class R1ScreeningReport:
    status: str
    provenance_status: str
    profile_digest: str
    suite_digest: str
    episode_batch_digest: str
    learner_surface_digest: str
    declared_critical_tests: tuple[str, ...]
    declared_metric_names: tuple[str, ...]
    dominated_by: Mapping[str, tuple[str, ...]]
    # Strict graph roots; these can be empty if tolerance-relaxed pairwise
    # comparisons have a cycle, even when no candidate may be eliminated.
    nondominated: tuple[str, ...]
    # Preserve whole top strongly connected components in a cycle; unlike
    # nondominated, this is the safe set to advance to later controls.
    retained_candidates: tuple[str, ...]
    dominance_cycles: tuple[tuple[str, ...], ...]


def _validate_candidate(profile: ComparisonProfile, candidate: CandidateEvaluation) -> None:
    if candidate.profile_digest != profile.profile_digest:
        raise ValueError(f"{candidate.substrate_id}: profile_digest mismatch")
    if candidate.suite_digest != profile.suite_digest:
        raise ValueError(f"{candidate.substrate_id}: suite_digest mismatch")
    if candidate.episode_batch_digest != profile.episode_batch_digest:
        raise ValueError(f"{candidate.substrate_id}: episode_batch_digest mismatch")
    if candidate.learner_surface_digest != profile.learner_surface_digest:
        raise ValueError(f"{candidate.substrate_id}: learner_surface_digest mismatch")
    if candidate.independent_run_count < profile.min_independent_runs:
        raise ValueError(f"{candidate.substrate_id}: independent_run_count below frozen minimum")

    expected = set(profile.critical_tests)
    if set(candidate.critical_test_passes) != expected or any(type(v) is not bool for v in candidate.critical_test_passes.values()):
        raise ValueError(f"{candidate.substrate_id}: critical_test_passes incomplete or invalid")

    metric_names = {metric.name for metric in profile.metrics}
    if set(candidate.metric_intervals) != metric_names:
        raise ValueError(f"{candidate.substrate_id}: metric_intervals incomplete or unexpected")
    for name, interval in candidate.metric_intervals.items():
        if not isinstance(interval, (tuple, list)) or len(interval) != 2:
            raise ValueError(f"{candidate.substrate_id}: metric_intervals {name} requires [lower, upper]")
        lower, upper = interval
        if (any(not _finite_number(x) for x in (lower, upper))
                or lower > upper):
            raise ValueError(f"{candidate.substrate_id}: metric_intervals {name} invalid")

    complexity_names = {spec.name for spec in profile.complexity}
    if set(candidate.complexity) != complexity_names:
        raise ValueError(f"{candidate.substrate_id}: complexity incomplete or unexpected")
    for name, value in candidate.complexity.items():
        _nonnegative(value, f"complexity {name}")


def _dominates(profile: ComparisonProfile, challenger: CandidateEvaluation, contender: CandidateEvaluation) -> bool:
    # Vacuous pass coverage is not evidence of semantic non-inferiority: a
    # cheaper learner that fails every named critical test cannot eliminate
    # another equally unqualified learner on cost alone.
    if not any(challenger.critical_test_passes[test] for test in profile.critical_tests):
        return False

    # A challenger may not lose a critical test that the contender passed.
    if any(contender.critical_test_passes[test] and not challenger.critical_test_passes[test]
           for test in profile.critical_tests):
        return False

    # Use opposing confidence bounds to avoid calling uncertain results non-inferior.
    for metric in profile.metrics:
        challenger_low, challenger_high = challenger.metric_intervals[metric.name]
        contender_low, contender_high = contender.metric_intervals[metric.name]
        if metric.direction == "HIGHER":
            if challenger_low < contender_high - metric.noninferiority_margin:
                return False
        elif challenger_high > contender_low + metric.noninferiority_margin:
            return False

    strictly_simpler = False
    for spec in profile.complexity:
        challenger_cost = challenger.complexity[spec.name]
        contender_cost = contender.complexity[spec.name]
        if challenger_cost > contender_cost + spec.materiality_margin:
            return False
        if challenger_cost < contender_cost - spec.materiality_margin:
            strictly_simpler = True
    return strictly_simpler


def _cycle_aware_retention(
    dominated_by: Mapping[str, tuple[str, ...]],
) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    """Retain undominated SCCs when relaxed pairwise costs are nontransitive.

    `dominated_by` points to direct dominators. It is not guaranteed to be a
    partial order: nonmaterial losses may accumulate into A > B > C > A.
    This graph has at most three nodes, but compute reachability explicitly
    so no input order or edge orientation can manufacture a survivor.
    """
    reach: dict[str, set[str]] = {}
    for name in dominated_by:
        seen: set[str] = set()
        pending = list(dominated_by[name])
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            pending.extend(dominated_by[current])
        reach[name] = seen

    def same_component(left: str, right: str) -> bool:
        return left == right or left in reach[right] and right in reach[left]

    groups = {
        tuple(sorted(other for other in dominated_by if same_component(name, other)))
        for name in dominated_by
    }
    cycles = tuple(sorted(group for group in groups if len(group) > 1))
    retained = tuple(sorted(
        name for name, direct_dominators in dominated_by.items()
        if all(same_component(name, other) for other in direct_dominators)
    ))
    return retained, cycles


def compare_substrates(profile: ComparisonProfile, candidates: list[CandidateEvaluation]) -> R1ScreeningReport:
    """Return a conservative pairwise Pareto screen, never a qualification.

    `profile_digest` and `suite_digest` are only caller assertions. No result
    from this function grants `R1_SUBSTRATE_SELECTED` or an R2 certificate.
    """
    if len(candidates) < 2 or len(candidates) > len(_SUBSTRATES):
        raise ValueError("comparison requires two or three candidate evaluations")
    names = [candidate.substrate_id for candidate in candidates]
    if len(names) != len(set(names)):
        raise ValueError("duplicate substrate_id in candidate evaluations")
    for candidate in candidates:
        _validate_candidate(profile, candidate)
    if len({candidate.independent_run_count for candidate in candidates}) != 1:
        raise ValueError("independent_run_count must match across candidates")

    dominated_by = {
        contender.substrate_id: tuple(sorted(
            challenger.substrate_id for challenger in candidates
            if challenger is not contender and _dominates(profile, challenger, contender)
        ))
        for contender in candidates
    }
    nondominated = tuple(sorted(name for name, dominators in dominated_by.items() if not dominators))
    retained_candidates, dominance_cycles = _cycle_aware_retention(dominated_by)
    return R1ScreeningReport(
        status=("INTRANSITIVE_DOMINANCE_HOLD" if dominance_cycles else "COMPARATIVE_SCREEN_ONLY"),
        provenance_status="CALLER_ASSERTED_UNVERIFIED",
        profile_digest=profile.profile_digest,
        suite_digest=profile.suite_digest,
        episode_batch_digest=profile.episode_batch_digest,
        learner_surface_digest=profile.learner_surface_digest,
        declared_critical_tests=profile.critical_tests,
        declared_metric_names=tuple(metric.name for metric in profile.metrics),
        dominated_by=MappingProxyType(dominated_by),
        nondominated=nondominated,
        retained_candidates=retained_candidates,
        dominance_cycles=dominance_cycles,
    )
