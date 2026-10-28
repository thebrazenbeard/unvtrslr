# Linux namespaced UNVTRSLR learner + bounded evaluator broker (2026-10-27)

**Claim ceiling: source-controlled actual UNVTRSLR negotiation inside Bubblewrap against an experimenter-authored, synthetic process broker. No independently unknown intelligence, emergent universal semantics or arbitrary-code containment.**

This closes one technical gap after [PR #52](https://github.com/thebrazenbeard/unvtrslr/pull/52), which demonstrated isolation only with a known canary probe, and after [PR #51](https://github.com/thebrazenbeard/unvtrslr/pull/51), which demonstrated a cross-host *unsandboxed* learner against an authored peer.

The worker `runs/contact_20261027/isolated_learner_worker.py` now executes the **existing** `src/unvtrslr/contact_negotiation.py` learner and `signal_discovery.py` under a Linux Bubblewrap read-only allowlist. It does *not* import the full NumPy-dependent `unvtrslr/__init__.py`: its `/app` namespace contains only the two actual unchanged source modules and one approved worker. No private evaluator code, private seed/mode, canary file, or hidden holdout input is mounted in the child.

`runs/contact_20261027/isolated_exchange.py` owns the synthetic private partner, trains through explicit `observe` / `offer` / `outcome` JSONL exchanges on stdin/stdout, validates all actions and numerical samples, bounds each output line and total requests, reads worker stdout with a nonblocking deadline to avoid partial-line deadlocks, and performs independent withheld-context wrong-signal evaluation **only after** a learner result has been frozen. The worker reports its namespace identifier and attempts forbidden canary-path/network access; the broker denies qualification unless its attestation differs from the host and both probes fail. This is a **known trusted Python worker**, not an adversarial-code resistance certificate.

**Actual VN2 execution:** source `f33094d442cbc68395bf4f32fc6c899d184b3483` on Linux Mint VN2, Python 3.12 and Bubblewrap 0.9; four seeds 17, 41, 73, 107; seven partner modes per seed. All **28/28 expected control classifications** and **28/28 namespace attestations** matched. Within the 28 classifications, **8 were held-out successes, 4 were held-out failures, 16 were ineligible**. A correctly classified failure is NOT a successful communication event. Private synthetic modes include responsive, slow-adapting, silent, fixed, independently random, uninformative constant-reward, and changed-rule drift. The positive cases demonstrate acquisition of a bounded two-feature operational convention through the real learner, not discovery of arbitrary intelligence.

The credential-free bound receipt is `research/ISOLATED_LEARNER_VN2_20261027.json` (SHA-256 `7ee887adfe0f0fbaa32081cf118f46396010085b07e842a5561d3a4517d76d44`). It stores the exact source SHA and four individual per-seed receipt digests; detailed receipts reside on VN2 and can be independently read back. No private canary bytes or live token were committed. Each session creates a new private canary, starts a fresh namespaced worker and closes the broker on success/failure.

**Source-based future reproducibility (Linux and functional unprivileged bwrap):**

```sh
python3 runs/contact_20261027/isolated_exchange.py \
  --repo . --seed 73 --report-out /tmp/unv-isolated-new.json
```

The output is deterministic in its synthetic partner seeds except for fresh canary/namespace details; do not overwrite earlier evidence. The repo CI tests mock or statically qualify argument boundaries; only the live VN2 result establishes actual namespace execution.

**Still not proved:** an independently authored or operated interlocutor, open-ended sensing without predefined 2-D scenes, a natural language, identification of communicative intent, observational invariants outside engineered rewards, authenticated source-independent outcome adjudication, sandbox escape resistance for untrusted arbitrary binaries/models, or *any actual extraterrestrial contact*. Python builtins, broker semantics, environment interventions, and reward/ablation conventions are still given by the test designer; this is not a real-world deployment. Keep [mission issue #48](https://github.com/thebrazenbeard/unvtrslr/issues/48) and [security/human adequacy issue #44](https://github.com/thebrazenbeard/unvtrslr/issues/44) OPEN.

**Fresh specialist review boundary:** Native ChatGPT subagent dispatch was unavailable. A fresh local VN1 qwen3:1.7b read-only model critique correctly noticed the ambiguous original `matched` key; it was changed to `matched_expected_control`. A separate Lappy qwen3:4b review request timed out without substantive output. Neither qualifies as independent human/security review. Further hostile tests must read exact final head, not a local-model opinion.
