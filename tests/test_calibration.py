from unvtrslr.calibration import (
    FingerprintObservation,
    calibrate_feature_information,
    fingerprint_scalars,
)


def fp(*, slope=0.0, raw_pitch=200.0, centroid=1000.0):
    return {
        "voiced_frame_fraction": 1.0,
        "channels": {
            "pitch_raw_hz": {"median": raw_pitch, "iqr": 10.0, "mean": raw_pitch, "std": 4.0},
            "pitch_relative_semitones": {
                "median": 0.0, "iqr": 2.0, "mean": 0.0, "std": 1.0,
                "slope": slope, "curvature": 0.0, "range": 5.0,
            },
            "intensity_db": {
                "median": -12.0, "iqr": 2.0, "mean": -12.0, "std": 1.0,
                "slope": 0.0, "curvature": 0.0, "range": 3.0,
            },
            "periodicity": {"median": 0.9, "iqr": 0.02, "mean": 0.9, "std": 0.01},
            "spectral_centroid_hz": {"median": centroid, "iqr": 50.0, "mean": centroid, "std": 20.0},
            "spectral_bandwidth_hz": {"median": 500.0, "iqr": 20.0, "mean": 500.0, "std": 10.0},
            "spectral_flatness": {"median": 0.1, "iqr": 0.01, "mean": 0.1, "std": 0.01},
            "spectral_rolloff_hz": {"median": 2200.0, "iqr": 50.0, "mean": 2200.0, "std": 25.0},
            "spectral_slope_db_octave": {"median": -8.0, "iqr": 0.5, "mean": -8.0, "std": 0.2},
            "h1_h2_db": {"median": 4.0, "iqr": 0.5, "mean": 4.0, "std": 0.2},
            "mfcc": [{"index": 0, "median": 1.0, "iqr": 0.2, "mean": 1.0, "std": 0.1}],
            "envelope_modulation_peak_hz": 4.0,
        },
    }


def build_identifiable():
    rows = []
    for source_index in range(4):
        source = f"s{source_index}"
        base_pitch = 120 + 40 * source_index
        for repeat in range(2):
            rows.append(
                FingerprintObservation(
                    f"a-{source}-{repeat}", "A", source,
                    fp(
                        slope=-2.0 - 0.1 * source_index - 0.03 * repeat,
                        raw_pitch=base_pitch,
                    ),
                )
            )
            rows.append(
                FingerprintObservation(
                    f"b-{source}-{repeat}", "B", source,
                    fp(
                        slope=+2.0 + 0.1 * source_index + 0.03 * repeat,
                        raw_pitch=base_pitch,
                    ),
                )
            )
    return rows


def test_fingerprint_scalars_keeps_raw_and_relative_pitch_separate():
    row = fingerprint_scalars(fp(slope=1.5, raw_pitch=245.0))
    assert row["pitch_raw_median_hz"] == 245.0
    assert row["pitch_relative_slope"] == 1.5


def test_conditional_information_recovers_system_feature_across_sources():
    report = calibrate_feature_information(build_identifiable(), permutations=64, seed=7)
    by_name = {row.feature: row for row in report.features}
    slope = by_name["pitch_relative_slope"]
    assert report.identifiability_status == "IDENTIFIABLE_WITHIN_OBSERVED_STRATA"
    assert slope.conditional_mutual_information_bits > 0.9
    assert slope.status == "CONDITIONAL_INFORMATION_SUPPORTED"


def test_source_only_raw_pitch_loses_credit_after_conditioning():
    report = calibrate_feature_information(build_identifiable(), permutations=32, seed=3)
    by_name = {row.feature: row for row in report.features}
    raw = by_name["pitch_raw_median_hz"]
    assert raw.raw_mutual_information_bits < 0.2
    assert raw.conditional_mutual_information_bits == 0.0


def test_target_source_confound_is_reported_not_misread_as_zero_information():
    rows = [
        FingerprintObservation("a1", "A", "speaker-a", fp(slope=-2.0)),
        FingerprintObservation("a2", "A", "speaker-a", fp(slope=-2.1)),
        FingerprintObservation("b1", "B", "speaker-b", fp(slope=2.0)),
        FingerprintObservation("b2", "B", "speaker-b", fp(slope=2.1)),
        FingerprintObservation("a3", "A", "speaker-a", fp(slope=-1.9)),
        FingerprintObservation("b3", "B", "speaker-b", fp(slope=1.9)),
        FingerprintObservation("a4", "A", "speaker-a", fp(slope=-2.2)),
        FingerprintObservation("b4", "B", "speaker-b", fp(slope=2.2)),
    ]
    report = calibrate_feature_information(rows, permutations=16)
    assert report.identifiability_status == "TARGET_CONFOUNDED_WITH_NUISANCE"
    assert all(
        row.status != "CONDITIONAL_INFORMATION_SUPPORTED"
        for row in report.features
    )


def test_report_order_is_deterministic_for_same_seed():
    rows = build_identifiable()
    a = calibrate_feature_information(rows, permutations=32, seed=11).to_dict()
    b = calibrate_feature_information(list(reversed(rows)), permutations=32, seed=11).to_dict()
    assert a == b
