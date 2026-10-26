# Empirical signal baselines V1 — supervised lookup falsifier

Status: `EXECUTABLE_NEGATIVE_CONTROL / ORACLE_SUPERVISED / SYNTHETIC_ONLY`.

`src/unvtrslr/empirical_signal_baselines.py` measures a deliberately trivial
nearest-frequency codebook lookup. It establishes how much apparent success
can arise from **prearranged carriers plus evaluator-provided opaque labels**.
It is not an emergent-language learner or a zero-shared-ontology candidate.

## Input and trust boundary

The trusted evaluator constructs `LabeledAcousticTrial` rows. Every row holds
an opaque nonnegative class ID, trial ID and family ID alongside the strict
four-field `UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1` waveform packet. Only the
waveform packet would be permissible as learner input. The class IDs and
`PeakLookupScore.class_carriers_hz` are **evaluator-private**. No Num’ta’reen
lexicon, generator seed, English gloss or author-approved frequency mapping
is imported, exposed, or assumed.

The scorer deliberately **uses class IDs in training**. That is *oracle
supervision*, giving the baseline privileges that a genuine blind learner
would not have. Its score is therefore a shortcut reference, not evidence
of discovering meaning. It does not provide process or host isolation.

`score_supervised_peak_lookup(train, holdout)`:

1. Verifies a nonempty, disjoint train/holdout split with unique trial IDs and
   nonoverlapping family IDs; rejects byte-identical waveform replay.
2. Enforces one shared public sample-rate/shape signature across both splits
   to remove those particular metadata confounds. It does **not** control
   waveform-level intensity, duration, pitch or capture artifacts.
3. Uses a Hann-windowed FFT to extract the dominant non-DC frequency of each
   mono recording, then fits one median carrier per oracle class label.
4. Reports holdout nearest-carrier accuracy, per-class accuracy and the fitted
   carrier table under a permanent claim ceiling:
   `SUPERVISED_SPECTRAL_LOOKUP_NEGATIVE_CONTROL_ONLY`.

For now it rejects multi-channel audio, silence and recordings shorter than
64 frames. These are declared **baseline scope limits**, not general acoustic
limitations of UNVTRSLR.

## Executable falsifier

The regression fixture uses two arbitrary frequency classes (400 and 600 Hz),
16 kHz / 1,600-frame mono signals, independently seeded phases, amplitudes and
small noise. Both holdouts use fresh trial and family IDs.

| Holdout condition | Oracle-supervised lookup accuracy |
| --- | ---: |
| Nuisance-matched frequencies, new phase/gain/noise | 100% |
| Frequencies globally shifted by ×1.5, same public metadata | 50% |

The shifted results are deterministic: 400→600 Hz is classified as the
600-Hz class; 600→900 Hz remains nearest the 600-Hz class. Accuracy is 50%
because the holdout is class balanced, **not** because the model has learned
an invariant relationship. The test would catch any claim that 100% ordinary
accuracy establishes robust acoustic semantics.

Run the focused suite:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_empirical_signal_baselines.py
```

This is an in-process synthetic control. Future work must demonstrate a
strictly separated, frozen learner with inaccessible evaluator labels and
codebooks, independently authenticated signals, stronger nuisance shifts,
partner swaps and randomized causal interventions before considering a
positive semantic claim. A supervised spectral negative control cannot by
itself establish that any such learner passed those tests.
