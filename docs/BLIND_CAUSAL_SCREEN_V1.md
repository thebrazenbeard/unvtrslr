# Blind causal screen V1 — evaluator-only, in-process diagnostic

Status: `EXECUTABLE_SYNTHETIC_CONTROL / IN_PROCESS / COUNTERFACTUAL_UNQUALIFIED`

`src/unvtrslr/blind_causal_screen.py` is an optional narrow evaluation seam
for candidate acoustic communication. It does **not** implement acquisition,
remote transport, isolated local models, or semantics. Its sole useful claim is
that a trusted *in-process evaluator* can measure several simple channel
interventions while keeping private trial labels out of learner **arguments**.

## Boundary and interface

`freeze_evaluation(train, holdout)` takes evaluator-only `PrivateTrial` rows:
`trial_id`, `group_id`, `observation_payload`, and `correct_action`. Trial and
group IDs are not included in learner-visible callbacks. Groups must be
disjoint across train/holdout, and holdout must represent both binary actions.
Within **each** split, every public `(sample_rate_hz, shape)` stratum must
contain equal numbers of both actions. Otherwise even an identical all-zero
waveform could reveal the evaluator answer through the audio header or length.
This strict balance rejects suspicious fixtures but does **not** eliminate
signal-level nuisance confounds embedded in amplitudes/frequencies.
Exact canonical waveform observations may not be reused between training and
holdout, even under fresh trial IDs or group labels. That blocks literal
lookup/replay but not transformed near-duplicates or memorized codebooks;
those still demand independently authenticated captures and nuisance-shift
controls.
The private manifest commitment is salted; neither it nor the private trial
objects should be disclosed before holdout evaluation. Input dictionaries are
validated and copied into immutable serialized records at freeze time.

The sender gets *exactly* the four keys from the separately planned blind
acoustic bridge:

```json
{
  "schema": "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1",
  "sample_rate_hz": 16000,
  "shape": [1600, 1],
  "float64_le_b64": "<canonical base64-encoded little-endian float64 samples>"
}
```

The `float64_le_b64` example above is a **schema placeholder**, not a real
encoded recording. Unknown keys (including any English gloss, hidden target,
source ID, trial ID, nuisance tag, timing metadata or seed) are rejected.
The public payload must encode finite samples and respect explicit shape/
channel/total sample bounds (at most 64 channels, 262,144 scalar values,
`sample_rate_hz` at most 2³¹−1, absolute sample magnitude at most 1e100).
The expected encoded text length is verified **before** base64 decoding to
avoid a large allocation from a tiny falsely declared shape. These match the
blind acoustic bridge's declared numeric limits. A waveform itself can leak
answers via intensity, duration, modulation, or deterministic generation.

The receiver gets `ReceiverView(message: bytes|None,
available_actions=(0,1))` and returns integer `0` or `1`. A sender message
is 1–256 opaque bytes. The receiver gets no evaluator factor, task label,
source reference, trial ID, or partner identity in its callback arguments.

## Four nonqualifying diagnostics

`screen_frozen_holdout()` measures:

1. Original-message holdout accuracy.
2. No-message accuracy on the same evaluator rows.
3. Deterministically rotated-message accuracy.
4. Optional partner receiver accuracy, plus same-callback replay consistency.

All outputs are labelled:
`IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED`.
If the messages are constant or the requested rotation leaves the sequence
unchanged, the shuffle is not an intervention at all: report
`message_shuffle_changes_payload=False` and `shuffled_accuracy=None` rather than a
misleading score. A malicious receiver can still use fixed call order to
manufacture apparently favorable original/replay/absent scores; those are
**not** positive causal gates. Conversely,
`message_shuffle_changes_payload=True` means only a syntactic byte change,
not necessarily a between-class intervention. A phase-counting receiver can
ignore every message while achieving original=1, absent=.5, shuffled=0 and
stable replay. Therefore `state_isolation_verified=False` and
`causal_listening_qualified=False` are unconditional, even for impressive
numeric metrics.
Even a perfect original score and poor controls are not a causal-listening
certificate: callbacks can share globals/files or branch on call order, and
the receiver is not genuinely reset to matched frozen state between probes.
More seriously, the four-key sender argument is **not a Python security
boundary**. An untrusted sender callback can use `inspect.stack()` to find
the evaluator's enclosing comprehension frame and read its private
`_SealedTrial.correct_action` directly, then encode that answer in its
message. A deterministic regression reproduces original accuracy 1.0,
no-message accuracy 0.5, shuffled accuracy 0.0, and consistent replay using
only this stack oracle. The qualification flags correctly remain `False`.
This makes in-process answer secrecy against an adversarial callback a
**NO-GO** even when arguments contain no private fields. Only an independently
isolated evaluator and learner execution boundary can test that claim.
The fixed rotation is a smoke negative control, not a preregistered randomized
intervention. The training split is *sealed and validated* but this module
does not train any participant or deliver post-action scalar consequences.

For actual qualification, physically separate and attest the Lappy evaluator,
VN1 sender and VN2 receiver; freeze state, randomize interventions and probe
cross-host covert channels, nuisance-matched generalization, partner swaps,
novel composition, response uncertainty and alternative code hypotheses.
See `docs/R2_THREE_HOST_CAUSAL_ACQUISITION_GATE.md`.

Keep a declared **prearranged-frequency-codebook baseline**. A separate
security probe reported 8/8 synthetic Num'ta'reen state recovery using only
FFT-peak nearest-frequency lookup against `250 + 92 * state` Hz. This is a
*reported adversarial observation*, not a reproduction by this module. Such
decoding is compatible with memorizing an author-specified codebook; it
cannot show the learner discovered semantics. Blind the codebook and test
novel combinations and nuisance shifts against the declared lookup baseline.

## Reproduction

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_blind_causal_screen.py
```

Passing synthetic tests here demonstrates argument-level separation and
repeatable control math, not any real-world language learning.
