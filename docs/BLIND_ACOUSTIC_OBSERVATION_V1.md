# Blind acoustic observation projection V1

Status: `OPT_IN_REFERENCE_WIRE_FORMAT / UNLABELLED_RAW_ACOUSTIC_INPUT_ONLY`

Purpose: allow a synthetic acoustic producer, including a deliberately
**noncanonical** Num'ta'reen resonance fixture, to hand acoustic evidence to
an UNVTRSLR learner without *also* sending its private generator symbols,
English or other reference translations, morphology/lexicon, provenance
strings, evaluator answers, source names, or trial identifiers.

`src/unvtrslr/blind_audio_observation.py` provides two pure functions:

```python
project_audio_observation(samples, sample_rate) -> dict
decode_audio_observation(payload) -> (samples, sample_rate)
```

The **entire learner-visible projection** is the exact four-key JSON shape:

```json
{
  "schema": "UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1",
  "sample_rate_hz": 16000,
  "shape": [3200, 1],
  "float64_le_b64": "<base64-encoded IEEE-754 float64 little-endian waveform>"
}
```

Waveform samples are copied into a frame-by-channel little-endian float64
array and encoded without quantization, amplitude normalization, channel
averaging, or segmentation. The decoder checks exactly those four keys,
positive integer sampling rate, shape, canonical base64 length and alphabet,
finite amplitudes and analysis numeric range before returning an immutable
waveform. At most 262,144 scalar samples and 64 channels are admitted by
this reference transport; those bounds are a resource policy, **not** a
perceptual or biological frequency limit. Sampling rate is also bounded to
the positive signed-32-bit integer range to avoid downstream numeric/runtime
pathologies; this is a wire-engineering bound, not a claim about admissible
alien frequencies. The existing acoustic/event APIs
can consume the decoded data unchanged.

## Critical information barriers

The generator's symbols, language rules, source/corpus identifiers, hidden
truth, action targets, prompt text, seed, nuisance factors, and trial IDs
remain *evaluator-private*. The projection API accepts only waveform and
rate. Neither the Num'ta'reen translator nor its lexicon/corpus may be
loaded into the learner environment. The evaluator should seal and hash its
private manifest **outside** the learner channel, freeze a holdout split,
and prove absence of shared file, network, clock, model-cache or orchestration
side channels before any semantic qualification.

The strict wire format does **not** sanitize the waveform's *information
content*. A generator can encode an answer through duration, leading
silence, number of pulses, recording noise, sample count, sample rate or a
deliberate frequency watermark. All these remain visible and must be
challenged with matched nuisance, intervention and message-ablation controls.
Raw waveform preservation protects evidence integrity; it does not prove
signalhood, semantic learning, equivalence or universal translation.

## Format and provenance limits

- The `float64_le_b64` key defines byte order. A conflicting extra `dtype`
  or `endianness` field is rejected. However arbitrary big-endian *sample
  bytes* can decode as finite little-endian values; such a mislabel cannot
  always be detected from raw bits without independent format provenance.
- A schema-valid input can still carry a hidden code in the audio; an
  evaluator must test it rather than assuming the interface proves blindness.
- The implementation provides no transport authentication, network security,
  process sandbox, or per-host model-state isolation.
- The known Num'ta'reen language project must not be treated as having an
  author-approved phonetic-to-Hz or waveform algorithm without independently
  confirmed canonical source material.

The maximum claim established by the reference tests is exact, bounded,
unlabelled waveform transfer into the UNVTRSLR acoustic/event pipeline.
