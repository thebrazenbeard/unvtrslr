# VN1 Parakeet real-inference probe — 2026-10-26

Event: `linguistics_live_coordination`. Evidence class: **REAL_SYSTEM_PROBE**, not language-meaning qualification.

## Exact subject

- UNVTRSLR adapter source: `main@0817f7ce5ece0e0757d47935f92f91034fc01009`; adapter Git blob `1caa601349f972d1411f19b948194b327a15ceab`.
- Host: Executor `VERA-NODE-1` (VN1), Windows, Intel Core i7-6770HQ, audio.cpp portable CPU release `v0.9.2-drama3-base-small`.
- Official release ZIP SHA-256: `9654c8f66f87bda768196d934059be896399b43703b06e5f2b857430775bec3b`; verified at the earlier VN1 pilot.
- Model: `audio-cpp/audio.cpp-gguf/Parakeet-TDT-0.6B-v3-GGUF/parakeet-tdt-0.6b-v3-q8_0.gguf`.
- Model file: **915,735,760 bytes**; HF LFS SHA-256 `6fa498f10f8cb606f041aa9512733cfee842a932359b00b0c45b9b723c4f4f4b` (**verified after complete download**).
- CPU: `audiocpp_cli.exe --task asr --family parakeet_tdt --model <file> --backend cpu --audio <file> --text-out <file> --metrics`.
- No credentials, personal microphone audio, or model weights were committed. Test files and downloaded model remained in isolated VN1 TEMP.

## Input control

VN1 Windows System.Speech SAPI generated a 16-kHz, 16-bit, mono PCM WAV speaking:

> The curious orange fox ran past the old blue barn.

Source WAV SHA-256 `65e9f2e91206d0e57622a75cb4a8d1bed6dc04895775a661c58f2436cc492fd4`; length **3.835 seconds**, 61,360 samples.

Two additional controls were constructed deterministically from the same sample count:

1. Original speech plus an additive 700-Hz sinusoid at amplitude 0.2 × full-scale 16-bit PCM, with clipping if needed. WAV SHA-256 `424ff6db0ab1a06c59bc34b52f92df6d041e04dfc9e08d73dfe241fec1e74867`.
2. Pure 434-Hz sine wave at amplitude 0.4 × full-scale PCM. WAV SHA-256 `788083bbee5730bed5cde323abc63735114c133aaa36a34585dabe22d45ff039`.

## Actual observed results

| Invocation | Output | Measured host result |
| --- | --- | --- |
| Direct audio.cpp CLI, clean SAPI speech | Exact original 10 words | exit 0, 8,269.57 ms reported inference wall, 11.081 s overall PowerShell measurement |
| UNVTRSLR `transcribe_diagnostic`, same clean WAV | Exact original 10 words | exit 0, 15.83 s adapter elapsed, 833 UTF-8 output bytes; source SHA and model SHA matched |
| UNVTRSLR adapter, speech + 700-Hz tone | Exact original 10 words | exit 0, 15.84 s adapter elapsed |
| UNVTRSLR adapter, 434-Hz non-speech tone | Empty text result | exit 0, 15.78 s adapter elapsed |

The direct CLI reported **peak RSS 2,540 MB**, **peak Windows committed footprint 6,496 MB**, `metrics.audio_duration_ms=3835`, `metrics.rtf=2.15634`, and `metrics.x_realtime=0.463748`. These are reported CLI measurements for one invocation, not a reproducible performance distribution. In particular, CPU inference was **slower than real time**.

The adapter's source bytes were independently fetched from its exact Git commit and verified against Git blob `1caa601349f972d1411f19b948194b327a15ceab` before invoking a **real** CLI and model. Its output explicitly retained `semantic_qualification=False` in all successful runs. Original input WAV checksums were bound to the adapter diagnostic.

## Limits and negative conclusions

- These samples use one synthetic English voice, not independent natural speakers, microphones, rooms, accents, or other languages. A sample exact match is **not** a general 0% WER estimate.
- A single interfering sinusoid and one empty tone result are not calibrated robustness or anti-hallucination benchmarks.
- `word_timestamps` reported `confidence:0` in this CLI sample; zero here must **not** be interpreted as calibrated uncertainty or strong word confidence.
- There is no Num’ta’reen sound-to-meaning result: the 434-Hz tone was a negative **ASR text** control, not an indigenous resonance interpretation. Num’ta’reen semantic and canon authorities remain separate.
- Windows detached descendant containment remains unverified. Local engine execution was against a downloaded CPU release; provider signature attestation beyond the release archive hash is not established.
- The model is small in file size but not in live RAM/commit consumption. Do not automatically launch or pin it resident on a resource-constrained VeraOS image.

## Architectural decision

VeraOS's current repository describes voice as a replaceable **client/modality**, specialized models behind **`vera-inference`**, and a distinct governed runtime `verad`. The proper future boundary is a **separate, optional, local ASR process/service** with pinned engine/model digests and measured resource limits. It should emit transcription candidates with provenance and uncertainty, not authoritative semantic facts or memory writes. The original audio samples must be preserved for UNVTRSLR / Num’ta’reen spectral inspection.

**Do not add audio.cpp or the 916-MB GGUF to the in-progress Buildroot/QEMU boot image yet.** First qualify service launch, crash cleanup, timeouts, audio fidelity, privacy, multiple real speakers/languages and hardware resource budgets. A hosted boot success is not proof of service safety or semantic grounding.
