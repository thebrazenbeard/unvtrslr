"""Supervised spectral lookup is a shortcut control, never semantic evidence."""

import numpy as np
import pytest

from unvtrslr.blind_audio_observation import project_audio_observation
from unvtrslr.empirical_signal_baselines import (
    LabeledAcousticTrial,
    score_supervised_peak_lookup,
)


RATE = 16_000
FRAMES = 1_600


def trial(split, index, label, carrier_hz, *, gain=1.0, phase=0.0, noise_seed=0):
    t = np.arange(FRAMES, dtype=np.float64) / RATE
    rng = np.random.default_rng(noise_seed)
    samples = gain * np.sin(2 * np.pi * carrier_hz * t + phase)
    samples += rng.normal(0.0, 0.002, FRAMES)
    return LabeledAcousticTrial(
        trial_id=f"{split}-{index}",
        family_id=f"{split}-family-{index}",
        payload=project_audio_observation(samples, RATE),
        opaque_class_id=label,
    )


def training_trials():
    return [
        trial("train", 0, 0, 400, phase=0.1, noise_seed=1),
        trial("train", 1, 1, 600, phase=0.2, noise_seed=2),
        trial("train", 2, 0, 400, gain=0.6, phase=1.0, noise_seed=3),
        trial("train", 3, 1, 600, gain=0.6, phase=1.2, noise_seed=4),
    ]


def holdout_trials(pitch_scale=1.0):
    return [
        trial("holdout", 0, 0, 400 * pitch_scale, gain=0.8, phase=0.5, noise_seed=91),
        trial("holdout", 1, 1, 600 * pitch_scale, gain=0.7, phase=0.8, noise_seed=92),
        trial("holdout", 2, 0, 400 * pitch_scale, gain=0.4, phase=1.1, noise_seed=93),
        trial("holdout", 3, 1, 600 * pitch_scale, gain=0.3, phase=1.3, noise_seed=94),
    ]


def test_frequency_codebook_lookup_works_on_seen_nuisance_but_fails_pitch_shift():
    control = score_supervised_peak_lookup(training_trials(), holdout_trials())
    shifted = score_supervised_peak_lookup(training_trials(), holdout_trials(1.5))
    assert control.accuracy == 1.0
    assert shifted.accuracy == 0.5
    assert control.class_carriers_hz == ((0, 400.0), (1, 600.0))
    assert control.oracle_supervision_used is True
    assert control.semantic_qualification is False
    assert shifted.semantic_qualification is False
    assert shifted.claim_ceiling == "SUPERVISED_SPECTRAL_LOOKUP_NEGATIVE_CONTROL_ONLY"


def test_scores_are_deterministic_for_identical_frozen_fixtures():
    first = score_supervised_peak_lookup(training_trials(), holdout_trials())
    second = score_supervised_peak_lookup(training_trials(), holdout_trials())
    assert first == second


def test_rejects_exact_waveform_replay_between_train_and_holdout():
    train = training_trials()
    holdout = holdout_trials()
    holdout[0] = LabeledAcousticTrial("different-id", "new-family", train[0].payload, 0)
    with pytest.raises(ValueError, match="replay"):
        score_supervised_peak_lookup(train, holdout)


def test_rejects_public_sample_rate_metadata_confounds():
    train = training_trials()
    confounded = holdout_trials()
    confounded[0] = LabeledAcousticTrial(
        "bad-rate", "new-family", project_audio_observation(np.zeros(FRAMES), 8_000), 0
    )
    with pytest.raises(ValueError, match="metadata"):
        score_supervised_peak_lookup(train, confounded)


def test_rejects_shared_family_and_unseen_holdout_class():
    train = training_trials()
    holdout = holdout_trials()
    holdout[0] = LabeledAcousticTrial("h-new", train[0].family_id, holdout[0].payload, 0)
    with pytest.raises(ValueError, match="family"):
        score_supervised_peak_lookup(train, holdout)
    holdout[0] = LabeledAcousticTrial("h-new", "new-family", holdout[0].payload, 2)
    with pytest.raises(ValueError, match="class"):
        score_supervised_peak_lookup(train, holdout)


@pytest.mark.parametrize("label", [True, -1, 1.5, "zero"])
def test_rejects_nonopaque_positive_class_ids(label):
    train = training_trials()
    train[0] = LabeledAcousticTrial("bad", "new-family", train[0].payload, label)
    with pytest.raises(ValueError, match="opaque_class_id"):
        score_supervised_peak_lookup(train, holdout_trials())


def test_rejects_silent_waveforms_without_peak():
    train = training_trials()
    train[0] = LabeledAcousticTrial(
        "silence", "silence-family", project_audio_observation(np.zeros(FRAMES), RATE), 0
    )
    with pytest.raises(ValueError, match="spectral peak"):
        score_supervised_peak_lookup(train, holdout_trials())
