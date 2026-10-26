# Local-model hostile review: Lappy / VN1 / VN2 (2026-10-26)

Status: `THREE_REAL_INFERENCES / INTERNAL_MODEL_REVIEW / NOT_INDEPENDENT_QUALIFICATION`

## Exact subject and method

- GitHub `main`: `97a0326136527303f5eafac430d46772e0b68c53`.
- Exact source tree: `db878120ae12cb4557a8870ac3d2f34750369713`.
- One orchestrating ChatGPT session sent the **same written excerpt** below to
  three separate model inference runtimes on three named devices. The models
  were **not** given a local repository checkout or tools, and could not
  inspect independent raw recordings or evaluate live source code.
- Each request set temperature `0`. Lappy and VN1 used Ollama `/api/generate`
  with `num_predict=380` (Gemma retry `420`); VN2 used llama.cpp
  `/v1/chat/completions` with `max_tokens=420`. These API differences and
  small model sizes prevent treating scores as a controlled model comparison.

| Host | Inference provider/runtime | Exact model label observed | Outcome |
| --- | --- | --- | --- |
| Lappy | Ollama, local Windows | `qwen3:4b-instruct`, Ollama listed ID `0edcdef34593` | Substantive but partly overstated hostile review |
| VERA-NODE-1 / VN1 | Ollama, local Windows | `lfm2.5-thinking:1.2b`, listed ID `95bd9d45385f` | Request completed with empty `.response`; **not counted as usable review** |
| VERA-NODE-1 / VN1 | Ollama, local Windows | `gemma3:1b`, listed ID `97558784bdc9` | Returned criticism, but proposed an irrelevant text-creativity test |
| VN2 | llama.cpp `llama-server`, Linux localhost port `11435` | `ibm-granite_granite-3.3-2b-instruct-Q4_K_M.gguf`, observed `system_fingerprint=b11827-970b51ce7` | Returned criticism containing a demonstrably false code inference |

Model names/short runtime IDs are local tool readbacks, **not verified weight
hashes or provenance attestations**. Distinct computers/models do not imply
independent information channels: the coordinator supplied a common summary.

## Exact prompt material supplied to each counted model

> UNVTRSLR HOSTILE REVIEW. Subject: GitHub main 97a0326136527303f5eafac430d46772e0b68c53, exact tree db878120ae12cb4557a8870ac3d2f34750369713. Evidence excerpt only (you do NOT have direct repo access): (1) Acoustic extractor chooses highest RMS input channel, marks exact silence and constant-DC AC spectrum invalid, and keeps numeric compatibility placeholders plus validity flags. (2) Candidate event novelty thresholds require finite positive values. Cross-recording registry clusters source-normalized vectors; recording_id and source_id are caller-supplied, a recording ID has one asserted source owner. (3) Synthetic R2 process channel sends sender a known binary factor, sends receiver an opaque message and explicit align/invert task; toy successful pair has prearranged symbols. (4) On POSIX adapter starts a process session, driver kills its process group on timeout/return; Windows kills only direct child. Task: identify two concrete paths to CONVINCING BUT FALSE evidence of language-free generalized semantic grounding, and propose one falsifiable control experiment that would distinguish a learned convention from shortcut behavior. Be adversarial, concise, under 230 words. Label observed excerpt facts separately from inferences. State what evidence is still missing.

## Results and critical adjudication

1. **Lappy / Qwen:** objected that silence/shape invariance can be mislabeled
   semantic identity, and that the R2 prearranged codebook could be passed off
   as emergent shared meaning. Suggested randomly permuting symbols. The
   challenge is material, but a permutation without an explicit fresh
   *learning* phase is not sufficient to distinguish acquisition from failure
   to decode an intentionally broken codebook.
2. **VN1 / Gemma:** treated finite-positive novelty thresholds as an inherent
   flaw and proposed randomized textual creativity prompts. That does not
   identify a reproducible defect in this acoustic/causal-listening API. Its
   review is retained as **low-specificity model criticism**, not accepted as
   a test design. The preceding LFM attempt produced no usable answer.
3. **VN2 / Granite:** raised cross-modality/human-comparison and pitch-feature
   ablation ideas, but falsely asserted that choosing the highest-RMS channel
   prioritizes silence. The supplied excerpt states the opposite. Human
   benchmark mismatch and pitch removal alone cannot demonstrate causal
   meaning; this review contains an explicit **model misreading**.

> **Hostile challenge retained:** The evaluator revealing the binary factor
> and a toy symbol convention can produce excellent observed task accuracy
> without agents ever learning semantics from unlabelled experience.

> **Review reliability challenge:** Agreement among models is not validation;
> two of these small-model outputs were partly off-target, and none had access
> to independent source or runtime evidence.

## Actionable next gate

Use `docs/R2_THREE_HOST_CAUSAL_ACQUISITION_GATE.md` for a separate trial with
VN1 observing raw nuisance-varied stimuli, VN2 acting on messages and delayed
scalar feedback, and Lappy holding sealed randomized intervention keys.
Freeze learner state, controls and holdouts; compare matched trials with
original/replaced/shuffled/absent messages. Audit shared filesystem, model
preload, clock, network and orchestration leakage **before** scoring. Test
partner swaps, novel composition and legitimate non-equivalence. Require
source evidence and executable tests for any subsequent code change.

No real three-host causal acquisition or confinement experiment was run in
this review. No universal-translation, grounded-semantic or OS-sandbox claim
is earned by these local model answers.
