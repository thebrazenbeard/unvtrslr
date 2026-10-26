"""A supervised, frozen waveform-only inference probe; not semantic qualification."""

from dataclasses import replace

import numpy as np
import pytest

from unvtrslr.blind_audio_observation import decode_audio_observation, project_audio_observation
from unvtrslr.empirical_signal_baselines import LabeledAcousticTrial, score_supervised_peak_lookup
from unvtrslr.train_only_ratio_learner import fit_and_score_ratio_probe


RATE = 8192
FRAMES = 4096


def _trial(split, index, label, ratio, pitch_scale=1.0):
    t = np.arange(FRAMES) / RATE
    f0 = 180.0 * pitch_scale
    rng = np.random.default_rng(index + (0 if split == "train" else 1000))
    phases = rng.uniform(-np.pi, np.pi, 2)
    gains = rng.uniform(0.32, 0.54, 2)
    samples = gains[0] * np.sin(2 * np.pi * f0 * t + phases[0])
    samples += gains[1] * np.sin(2 * np.pi * f0 * ratio * t + phases[1])
    samples += rng.normal(0, 0.001, FRAMES)
    return LabeledAcousticTrial(
        f"{split}-{index}", f"{split}-family-{index}",
        project_audio_observation(samples, RATE), label,
    )


def _split(permutation=(7, 41), pitch_scale=1.0):
    ratios = (1.35, 1.85)
    train = [_trial("train", i, permutation[i % 2], ratios[i % 2]) for i in range(12)]
    holdout = [
        _trial("holdout", i, permutation[i % 2], ratios[i % 2], pitch_scale)
        for i in range(12)
    ]
    return train, holdout


def test_train_only_model_generalizes_pitch_shift_where_carrier_lookup_fails():
    train, holdout = _split(pitch_scale=1.6)
    result = fit_and_score_ratio_probe(train, holdout)
    shortcut = score_supervised_peak_lookup(train, holdout)
    assert result.accuracy == 1.0
    assert shortcut.accuracy < result.accuracy
    assert result.model.provenance_sha256 == fit_and_score_ratio_probe(train, holdout).model.provenance_sha256
    assert len(result.model.provenance_sha256) == 64
    assert result.model.oracle_supervision_used is True
    assert result.semantic_qualification is False
    assert result.model.semantic_qualification is False
    assert result.model.predict(holdout[0].payload) == holdout[0].opaque_class_id


def test_model_learns_arbitrarily_permuted_labels_from_training_not_hardcoded():
    train_a, holdout_a = _split(permutation=(7, 41), pitch_scale=1.6)
    train_b, holdout_b = _split(permutation=(41, 7), pitch_scale=1.6)
    first = fit_and_score_ratio_probe(train_a, holdout_a)
    second = fit_and_score_ratio_probe(train_b, holdout_b)
    assert first.accuracy == second.accuracy == 1.0
    assert first.model.predict(holdout_a[0].payload) != second.model.predict(holdout_a[0].payload)
    assert first.model.provenance_sha256 != second.model.provenance_sha256
    # Withheld private answer keys deliberately inverted after fitting.
    wrong_answers = [replace(row, opaque_class_id=41 if row.opaque_class_id == 7 else 7) for row in holdout_a]
    assert fit_and_score_ratio_probe(train_a, wrong_answers).accuracy == 0.0


def test_split_replay_and_metadata_confounds_rejected():
    train, holdout = _split()
    holdout[0] = replace(holdout[0], payload=train[0].payload)
    with pytest.raises(ValueError, match="replay"):
        fit_and_score_ratio_probe(train, holdout)
    _, holdout = _split()
    holdout[0] = replace(holdout[0], family_id=train[0].family_id)
    with pytest.raises(ValueError, match="family"):
        fit_and_score_ratio_probe(train, holdout)
    _, holdout = _split()
    holdout[0] = replace(holdout[0], payload=project_audio_observation(np.zeros(2048), RATE))
    with pytest.raises(ValueError, match="metadata"):
        fit_and_score_ratio_probe(train, holdout)


def test_prediction_does_not_take_expected_label_or_trial_identity():
    train, holdout = _split()
    model = fit_and_score_ratio_probe(train, holdout).model
    assert model.predict(holdout[0].payload) == holdout[0].opaque_class_id
    with pytest.raises(TypeError):
        model.predict(holdout[0].payload, holdout[0].opaque_class_id)
    with pytest.raises(ValueError, match="spectral"):
        model.predict(project_audio_observation(np.zeros(FRAMES), RATE))


@pytest.mark.parametrize("interferer_amplitude", [0.0, 0.4, 0.6])
def test_unseen_third_tone_is_a_negative_robustness_control(interferer_amplitude):
    """An engineered two-peak feature must not imply arbitrary-source robustness.

    Keep the fitted supervised model and held-out labels fixed; only the
    learner-visible acoustic signal receives an untrained 700 Hz source.
    This deliberately records model failure, not a translation success.
    """
    train, holdout = _split(pitch_scale=1.6)
    baseline = fit_and_score_ratio_probe(train, holdout)
    contaminated = []
    for row in holdout:
        samples, sample_rate = decode_audio_observation(row.payload)
        time = np.arange(samples.shape[0]) / sample_rate
        altered = samples[:, 0] + interferer_amplitude * np.sin(2 * np.pi * 700.0 * time)
        contaminated.append(replace(row, payload=project_audio_observation(altered, sample_rate)))

    score = fit_and_score_ratio_probe(train, contaminated)
    assert score.model.provenance_sha256 == baseline.model.provenance_sha256
    assert score.semantic_qualification is False
    if interferer_amplitude == 0.0:
        assert score.accuracy == 1.0
    else:
        assert score.accuracy <= 1.0 / 3.0
