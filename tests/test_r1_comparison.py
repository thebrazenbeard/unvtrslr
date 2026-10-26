"""The R1 screening gate must not manufacture a substrate winner."""

import unittest
from dataclasses import replace

from unvtrslr.r1_comparison import (
    CandidateEvaluation,
    ComplexitySpec,
    ComparisonProfile,
    MetricSpec,
    compare_substrates,
)


PROFILE_DIGEST = "a" * 64
SUITE_DIGEST = "b" * 64
CODE_DIGEST = "c" * 64
SURFACE_DIGEST = "d" * 64
EPISODE_DIGEST = "e" * 64


def profile():
    return ComparisonProfile(
        profile_digest=PROFILE_DIGEST,
        suite_digest=SUITE_DIGEST,
        episode_batch_digest=EPISODE_DIGEST,
        learner_surface_digest=SURFACE_DIGEST,
        critical_tests=("E01", "E08"),
        metrics=(
            MetricSpec("transfer_accuracy", "HIGHER", 0.03),
            MetricSpec("calibration_loss", "LOWER", 0.03),
        ),
        complexity=(
            ComplexitySpec("serialized_representation_bytes", "bytes", 0),
            ComplexitySpec("fixed_primitive_count", "count", 0),
            ComplexitySpec("learned_primitive_count", "count", 0),
            ComplexitySpec("candidate_specific_trainable_parameters", "count", 0),
            ComplexitySpec("peak_memory_bytes", "bytes", 0),
            ComplexitySpec("compute_per_interaction", "operations", 0),
            ComplexitySpec("interactions_to_qualification", "interactions", 0),
            ComplexitySpec("adapter_complexity", "source_lines", 0),
            ComplexitySpec("human_authored_ontology_bytes", "bytes", 0),
        ),
        min_independent_runs=3,
    )


def candidate(name, *, passed=None, metrics=None, complexity=None, **overrides):
    counts = {spec.name: 10 for spec in profile().complexity}
    counts["serialized_representation_bytes"] = 100 if name == "TPH" else 50
    counts.update(complexity or {})
    values = dict(
        substrate_id=name,
        profile_digest=PROFILE_DIGEST,
        suite_digest=SUITE_DIGEST,
        episode_batch_digest=EPISODE_DIGEST,
        learner_surface_digest=SURFACE_DIGEST,
        learner_code_digest=CODE_DIGEST,
        independent_run_count=3,
        critical_test_passes={"E01": True, "E08": True},
        metric_intervals={"transfer_accuracy": (0.80, 0.82), "calibration_loss": (0.10, 0.12)},
        complexity=counts,
    )
    if passed is not None:
        values["critical_test_passes"] = passed
    if metrics is not None:
        values["metric_intervals"] = metrics
    values.update(overrides)
    return CandidateEvaluation(**values)


class R1ComparisonTests(unittest.TestCase):
    def test_simpler_equivalent_candidate_dominates_without_selecting_substrate(self):
        result = compare_substrates(profile(), [candidate("TPH"), candidate("PIS")])
        self.assertEqual(result.dominated_by, {"TPH": ("PIS",), "PIS": ()})
        self.assertEqual(result.nondominated, ("PIS",))
        self.assertEqual(result.status, "COMPARATIVE_SCREEN_ONLY")

    def test_semantic_advantage_blocks_complexity_only_win(self):
        better = candidate("TPH", metrics={
            "transfer_accuracy": (0.90, 0.92), "calibration_loss": (0.10, 0.12)
        })
        result = compare_substrates(profile(), [better, candidate("PIS")])
        self.assertEqual(result.nondominated, ("PIS", "TPH"))

    def test_critical_test_gain_blocks_false_dominance(self):
        shortcut = candidate("PIS", passed={"E01": True, "E08": False})
        result = compare_substrates(profile(), [candidate("TPH"), shortcut])
        self.assertEqual(result.nondominated, ("PIS", "TPH"))

    def test_all_failed_candidates_cannot_be_eliminated_solely_for_complexity(self):
        failure = {"E01": False, "E08": False}
        result = compare_substrates(profile(), [
            candidate("TPH", passed=failure), candidate("PIS", passed=failure)
        ])
        self.assertEqual(result.dominated_by, {"TPH": (), "PIS": ()})
        self.assertEqual(result.nondominated, ("PIS", "TPH"))

    def test_tolerated_cost_regressions_can_form_three_candidate_dominance_cycle(self):
        # Margins are symmetric and nontransitive: each cheaper system is
        # allowed two nonmaterial losses, so pairwise elimination cycles.
        dims = (
            "serialized_representation_bytes",
            "peak_memory_bytes",
            "adapter_complexity",
        )
        loosened = replace(
            profile(),
            complexity=tuple(
                replace(spec, materiality_margin=2.0) if spec.name in dims else spec
                for spec in profile().complexity
            ),
        )
        results = compare_substrates(loosened, [
            candidate("TPH", complexity=dict(zip(dims, (0, 2, 4)))),
            candidate("DCA", complexity=dict(zip(dims, (4, 0, 2)))),
            candidate("PIS", complexity=dict(zip(dims, (2, 4, 0)))),
        ])
        self.assertEqual(results.dominated_by, {
            "TPH": ("PIS",), "DCA": ("TPH",), "PIS": ("DCA",)
        })
        self.assertEqual(results.nondominated, ())  # mathematically no root
        self.assertEqual(results.status, "INTRANSITIVE_DOMINANCE_HOLD")
        self.assertEqual(results.dominance_cycles, (("DCA", "PIS", "TPH"),))
        self.assertEqual(results.retained_candidates, ("DCA", "PIS", "TPH"))

    def test_acyclic_ordinary_screen_retains_only_its_true_nondominated_candidate(self):
        results = compare_substrates(profile(), [candidate("TPH"), candidate("PIS")])
        self.assertEqual(results.status, "COMPARATIVE_SCREEN_ONLY")
        self.assertEqual(results.dominance_cycles, ())
        self.assertEqual(results.retained_candidates, results.nondominated)

    def test_screen_discloses_claimed_critical_test_subset_and_unverified_provenance(self):
        result = compare_substrates(profile(), [candidate("TPH"), candidate("PIS")])
        self.assertEqual(result.declared_critical_tests, ("E01", "E08"))
        self.assertEqual(result.provenance_status, "CALLER_ASSERTED_UNVERIFIED")
        self.assertEqual(result.declared_metric_names, ("transfer_accuracy", "calibration_loss"))

    def test_material_regression_in_another_complexity_field_blocks_dominance(self):
        high_memory = candidate("PIS", complexity={"peak_memory_bytes": 1000})
        result = compare_substrates(profile(), [candidate("TPH"), high_memory])
        self.assertEqual(result.nondominated, ("PIS", "TPH"))

    def test_uncertain_intervals_do_not_count_as_noninferiority(self):
        low_bound = candidate("PIS", metrics={
            "transfer_accuracy": (0.75, 0.85), "calibration_loss": (0.10, 0.12)
        })
        result = compare_substrates(profile(), [candidate("TPH"), low_bound])
        self.assertEqual(result.nondominated, ("PIS", "TPH"))

    def test_lower_is_better_metrics_use_opposite_bounds(self):
        worse_loss = candidate("PIS", metrics={
            "transfer_accuracy": (0.80, 0.82), "calibration_loss": (0.10, 0.17)
        })
        result = compare_substrates(profile(), [candidate("TPH"), worse_loss])
        self.assertEqual(result.nondominated, ("PIS", "TPH"))

    def test_mixed_profile_or_holdout_is_rejected(self):
        for field in ("profile_digest", "suite_digest", "episode_batch_digest", "learner_surface_digest"):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                compare_substrates(profile(), [candidate("TPH"), candidate("PIS", **{field: "f" * 64})])

    def test_missing_tests_or_metrics_cannot_silently_pass(self):
        for field, value in (("critical_test_passes", {"E01": True}),
                             ("metric_intervals", {"transfer_accuracy": (0.8, 0.9)})):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                compare_substrates(profile(), [candidate("TPH"), candidate("PIS", **{field: value})])

    def test_inadequate_runs_and_nonfinite_metrics_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "independent_run_count"):
            compare_substrates(profile(), [candidate("TPH"), candidate("PIS", independent_run_count=1)])
        with self.assertRaisesRegex(ValueError, "metric_intervals"):
            compare_substrates(profile(), [candidate("TPH"), candidate("PIS", metrics={
                "transfer_accuracy": (float("nan"), 0.9), "calibration_loss": (0.1, 0.12)
            })])

    def test_unbounded_integers_fail_closed_instead_of_overflowing(self):
        huge = 10 ** 1000
        for value in (huge, -huge):
            with self.subTest(kind="metric", value_sign=value > 0), self.assertRaisesRegex(ValueError, "metric_intervals"):
                compare_substrates(profile(), [candidate("TPH"), candidate("PIS", metrics={
                    "transfer_accuracy": (value, value), "calibration_loss": (0.1, 0.12)
                })])
            with self.subTest(kind="cost", value_sign=value > 0), self.assertRaisesRegex(ValueError, "complexity"):
                compare_substrates(profile(), [candidate("TPH"), candidate("PIS", complexity={
                    "peak_memory_bytes": value
                })])

    def test_unbalanced_repetitions_cannot_enter_paired_screen(self):
        with self.assertRaisesRegex(ValueError, "independent_run_count must match"):
            compare_substrates(profile(), [candidate("TPH"), candidate("PIS", independent_run_count=4)])

    def test_profile_cannot_omit_adapter_or_ontology_costs(self):
        full = profile()
        with self.assertRaisesRegex(ValueError, "complexity"):
            ComparisonProfile(
                profile_digest=full.profile_digest,
                suite_digest=full.suite_digest,
                episode_batch_digest=full.episode_batch_digest,
                learner_surface_digest=full.learner_surface_digest,
                critical_tests=full.critical_tests,
                metrics=full.metrics,
                complexity=full.complexity[:-2],
                min_independent_runs=full.min_independent_runs,
            )


if __name__ == "__main__":
    unittest.main()
