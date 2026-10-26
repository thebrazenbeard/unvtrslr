# BT2 three-host model opinions — 2026-10-26

Evidence class: `MODEL_REVIEW`, not runtime qualification, source test, or
independently reconstructed semantics. Frozen subject for all three prompts:
UNVTRSLR `main@a102009f25998395f1d737a009c7ee079033230e`, tree
`6551f5912f69e9c10b0ecb2013c68f97c58982e7`. The models saw **brief
descriptions**, not the actual full source tree or hidden experimental data.
All three calls were observed through genuine local inference endpoints on
three physically distinct devices. None is credited with independently
verifying a code defect.

## VN1 — Gemma

- Host/runtime: `VERA-NODE-1`, Ollama HTTP `/api/generate` on localhost:11434.
- Model: `gemma3:1b`, Ollama digest
  `97558784bdc9175075a72655bf360b15da17df6b3b9e5182af9f8c0c8e58ba7c`,
  model size 806,067,407 bytes; deterministic request `temperature=0`,
  `num_predict=64`, `stream=false`.
- Exact prompt:

  > Hostile review: UNVTRSLR tries to infer meaning without a common language. In a toy test the sender gets true binary factor and receiver gets sign plus task. What independent observation could falsify learned semantics? Answer in under 60 words.

- Observed response (Windows console replaced some apostrophes with U+FFFD):

  > A consistent, repeatable failure to accurately interpret the toy test�s results across multiple trials, regardless of the sender�s or receiver�s actions, would falsify the learned semantics. It demonstrates the system isn�t truly understanding the task�s nuances.

- Assessment: general suggestion about repeatability; no specific novel
  falsifier or source-grounded mechanism. `MODEL_REVIEW_ONLY`.

## VN2 — IBM Granite

- Host/runtime: `VN2`, local `llama.cpp` OpenAI-compatible HTTP service
  `127.0.0.1:11435/v1/chat/completions`, declared owner `llamacpp`.
- Model file: `ibm-granite_granite-3.3-2b-instruct-Q4_K_M.gguf`,
  2,533,539,840 parameters, 2048 context, model file 1,543,556,592 bytes;
  independently read model-file SHA-256
  `555b91485955bc96eb445b57dd4bbf8809aa7d8cce7c313f4f8bc5b2340896b4`.
  `temperature=0`, `max_tokens=64`, `stream=false`; returned 57 completion tokens.
- Exact prompt:

  > You are a hostile reviewer. UNVTRSLR aims to infer meanings without shared language. In a toy test, sender sees true binary factor, receiver sees message and task; evaluator scores message swap and reward. Name the most decisive missing test for learned semantics. Keep under 60 words.

- Observed response:

  > The most decisive missing test for learned semantics in UNVTRSLR would be a "Cross-Cultural Semantic Alignment Test," evaluating how well a system interprets and conveys meaning across diverse linguistic and cultural contexts, ensuring robust semantic understanding.

- Assessment: abstract suggestion; assumes human culture, which is not
  an adequate test for communication with no shared ontology. No concrete
  experimental counterexample. `MODEL_REVIEW_ONLY`.

## Lappy — Qwen

- Host/runtime: `Lappy`, Ollama HTTP `/api/generate` on localhost:11434.
- Model: `qwen3:4b-instruct`, Ollama digest
  `0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0`,
  model size 2,497,293,803 bytes; `temperature=0`, `num_predict=76`,
  `stream=false`.
- Exact prompt:

  > Hostile review: UNVTRSLR tries to infer meaning without shared language. A toy sender sees evaluator true binary factor and receiver sees sign plus task. What decisive counterexample would reveal task-only code rather than learned meaning? Reply under 65 words.

- Observed response (console character replacement retained):

  > A receiver consistently outputs the same sign regardless of input variation, yet the task outcome changes�proving the code depends only on task, not learned meaning.

- Assessment: plausibly points toward an input-ignoring receiver but reverses
  the receiver/action-sign terminology. Negative controls already cover
  input-ignoring and task-bound behavior; no new verified defect.
  `MODEL_REVIEW_ONLY`.

## Hostile synthesis and exclusions

> None of the three local model outputs verifies or falsifies the actual
> repository implementation. They are prompt-conditioned critiques of
> a description, with no blind code execution, held-out experiment, or
> independent semantics reconstruction.

The stronger source/test findings this round came from native specialist
agents plus direct reproductions: silent acoustic modulation, typed-evidence
coercion, R2 reference monkeypatching, CI checkout evasion, shared-host-file
collusion, and cross-factor message collision. Those claims require the actual
regression tests and GitHub CI bound to the proposed source tree.

### Next valid experiment

Freeze a sender/receiver/evaluator protocol with independent host/VM privilege
boundaries; train a new convention from raw interaction rather than handing
over a binary world factor or pretrained codebook. Blind the counterfactual
task and factor interventions, switch roles/partners and tasks, and score
held-out compositional transfer with honest abstention and non-equivalence.
External model agreement should not affect certificate thresholds.
