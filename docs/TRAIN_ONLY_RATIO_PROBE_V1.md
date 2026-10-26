# Train-only two-tone ratio probe V1

Status: `SYNTHETIC_SUPERVISED_INVARIANCE_CONTROL / NOT_SEMANTICS`.

The evaluator creates labeled, independent two-tone observations and withholds
holdout answers from the learner's `FrozenRatioModel.predict(payload)` method.
Training uses evaluator-private opaque class labels, computes a two-tone FFT
frequency ratio, and freezes the median ratio per class in an immutable model.
The model carries a SHA-256 commitment to the sorted *labeled training rows*
and an explicit `oracle_supervision_used=True`; inference accepts only the
strict four-field waveform observation, not a class, trial/family identity,
source corpus, generation seed, or English gloss.

The exercised fixture changes phases, amplitudes, background noise, and the
absolute carrier frequencies (global pitch transposition ×1.6) without
changing the class-specific frequency ratios. It further **swaps arbitrary
opaque class labels in training**, verifying that the frozen classifier's
outputs follow the actual training labels rather than hardcoded carrier IDs.
Changing only the evaluator holdout answer key after training must score zero.
The pre-existing absolute peak-frequency supervised baseline is run on the
same fixture as a shortcut comparator.

```bash
PYTHONPATH=src python -m pytest -q tests/test_train_only_ratio_learner.py
```

## Evidence ceiling and falsifiers

- This is a hand-engineered two-tone invariant plus **supervised** lookup,
  not a discovered semantic structure. Oracle labels enter fitting.
- Both sender and receiver still share a deliberately authored synthetic
  acoustic pattern, and the evaluation is in-process on one machine.
- The provenance digest is evidence of what training inputs the fixture used,
  not cryptographic proof of process isolation or absence of all leakage.
- No natural acoustic corpus, compositional grammar, causal referents,
  grounded action, arbitrary real-world noise, novel class emergence, or
  independent models are exercised.
- Near-duplicate train/holdout waveforms may evade the base exact-replay
  validator; family disjointness depends on the evaluator's truthful IDs.
- The two strongest FFT peaks can be manipulated by sidebands/harmonics.
  A deterministic third-tone interference negative control now adds a 700 Hz
  source only to the pitch-shifted holdout (amplitudes 0.4 and 0.6) and
  checks that accuracy falls to one-third or below, despite the clean
  pitch-shifted holdout scoring 100%. This is an explicit failure of
  robustness under unseen source mixtures, not an achievement metric.
  More distortions and recombination remain outside this narrow test.

The proper conclusion from high accuracy is **generalization of an engineered
relative-pitch feature under the tested transposition**, never that Universal
Translator understands or has learned Num'ta'reen.
