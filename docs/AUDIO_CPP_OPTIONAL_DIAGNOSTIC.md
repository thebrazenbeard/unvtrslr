# Optional audio.cpp ASR diagnostic boundary

Status: `HUMAN_ASR_DIAGNOSTIC_UNQUALIFIED` — opt-in, no deployment and no semantic claim.

`src/unvtrslr/audio_cpp_adapter.py` invokes a **trusted, explicitly selected**
audio.cpp CLI offline with `--task asr --family nemotron_asr|parakeet_tdt`,
`--backend cpu|cuda|vulkan`, `--mode offline` and `--audio <temporary WAV>`.
The engine is not downloaded or started automatically.

The input must be bounded PCM RIFF/WAV; its original bytes are written
unchanged to the temporary file. Num’ta’reen spectral analysis must consume
the original waveform separately, not this ASR output.

Example, supplying already installed and approved local assets:

```python
from unvtrslr.audio_cpp_adapter import AudioCppConfig, transcribe_diagnostic

config = AudioCppConfig(
    command=(r"C:\absolute\path\audiocpp_cli.exe",),
    model_path=r"C:\absolute\path\parakeet-tdt-0.6b-v3-q8.gguf",
    family="parakeet_tdt",
    backend="cpu",
)
diagnostic = transcribe_diagnostic(wav_file.read_bytes(), config)
assert not diagnostic.semantic_qualification
```

The API returns raw bounded stdout **as an untrusted diagnostic**. The CLI's
text/log presentation can vary by version: it is not parsed as an English
translation, word alignment, ground truth, or Num’ta’reen gloss.

Controls: no shell, fixed CLI flags, bounded input/output sizes, bounded
runtime, non-inherited user environment, file SHA-256 provenance for the
executable, model GGUF, and absolute helper files in the command tuple,
change-detection on those files during each invocation, and source WAV
integrity readback. An output flood is killed without buffering unbounded
stdout. POSIX ordinary descendants are killed with the process group;
**Windows detached descendants and deliberate process-group escapes remain
uncontained**. This is not a sandbox for untrusted programs. Dependencies
can still change between the hash read and process launch (TOCTOU).

This first adapter accepts a **single GGUF file**, not multi-file model
packages. It also does not authenticate the upstream release signature or
validate model-license compliance; those require separate review.

The VN1 host previously fetched the official Windows CPU portable archive
for audio.cpp `v0.9.2-drama3-base-small`, release SHA-256
`9654c8f66f87bda768196d934059be896399b43703b06e5f2b857430775bec3b`,
and `--list-devices` reported one CPU. That proves neither ASR inference
nor numerical/spectral suitability.

Executable unit tests use local Python fake workers:
`python -m pytest -q tests/test_audio_cpp_adapter.py`.

Success at this transport boundary **never** sets
`semantic_qualification=True`. A future benchmark needs pinned real
NVIDIA model files, independent transcriptions, genuine multilingual audio,
word-error rates, latency/RAM measurements, and a separate raw-resonance
fidelity test with unmodified Num’ta’reen measurements.
