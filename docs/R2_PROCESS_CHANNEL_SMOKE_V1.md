# R2 process-channel reference smoke test — V1

Status: `REFERENCE_PROCESS_SCREEN_EXECUTABLE / NO_OS_SANDBOX / NO_SEMANTIC_QUALIFICATION`

`src/unvtrslr/r2_process_probe.py` supplies a narrow, executable step toward
the four-zone R2 design. Unlike `r2_controls.probe_controls`, its sender and
receiver never share a Python object or interpreter. Each call launches a
fresh process. The sender receives **only** `{"factor": 0|1}`; the receiver
receives **only** `{"message": string|null, "task": "align"|"invert"}`.
Evaluator episode IDs and expected actions never enter the receiver payload.

Adapters read exactly one JSON request from stdin and return one JSON object:

- sender: `{"message": "opaque-symbol"}` (1–256 UTF-8 bytes);
- receiver: `{"action": 0|1}` (integer, not boolean).

Call `screen_process_channel(ProcessEndpoint(sender_argv),
ProcessEndpoint(receiver_argv), episodes)` from a trusted research driver.
Commands are passed as argument arrays to subprocesses without a shell, with
a minimal environment and fresh working directory. They are not downloaded,
installed, or executed automatically by the package. **Review the adapter
programs before running them; subprocesses are not a security sandbox.**

The screen tests:

1. balanced toy-factor baseline accuracy;
2. same-world receiver message removal;
3. alternative-factor message insertion with receiver task fixed;
4. repeat intervention consistency across fresh receiver processes and
   a hidden, randomly shuffled order of five probes per episode;
5. inversion of the receiver's task using the same message.

The receiver-side surface deliberately contains no episode ID, so cross-ID
leakage is *excluded by API* rather than measured as a separate success score.
Tests provide a transparent reference oracle, a constant receiver, and a
sender environment-variable side channel that cannot traverse an ordinary
child-to-child environment. A hostile shared-host-file pair also proves that
process boundaries alone do not prevent inter-process collusion. Even the
reference fixture's numerically perfect result emits `COUNTERFACTUAL_UNQUALIFIED`
and an explicit `numerical_gates_met=True`, **never**
`GROUNDED_WITHIN_TESTED_SCOPE` or a trusted positive certificate. Identical
opposite-factor messages invalidate the reported causal flip rate (`None`).

## Sharp boundaries

This screen does **not** solve or certify the intended translation problem:

- The known positive adapters begin with a **pre-agreed two-symbol codebook**.
  No convention is learned without a shared language or ontology.
- The evaluator gives the sender a perfectly identified binary factor and the
  receiver a human-authored task. The scenario already shares semantics.
- Host filesystem, network, clock, binary contents, OS-wide state, timing, and
  covert channels are not isolated. A malicious candidate can still collude;
  shuffling the intervention order only removes an easy fixed-order attack.
- Program stdout is spooled to a temporary file before a size check, avoiding
  unbounded **RAM** capture. This does not impose an OS output quota or bound
  the amount a malicious program could write to disk before timeout.
- Fresh process invocations prevent within-Python-object leaks, not shared
  storage or pretraining leakage. The actual outputs are not independently
  source-authenticated or randomized under a sealed external evaluator.
- No real corpus, animal interaction, novel partner, role reversal,
  compositional transfer, non-equivalence or third-party acquisition is tested.
- No controlled statistical confidence bound has been calibrated.

## Next qualification gates

1. Run separately permissioned sender/receiver/evaluator containers or
   VMs with closed file/network surfaces and frozen, independently audited
   prompts/artifacts; rerun deliberate shared-state adversaries.
2. Replace the privileged binary factor input with separately rendered raw
   observations and use interaction feedback to learn conventions.
3. Blind and preregister held-out causal interventions, composition,
   modality/partner transfer, and rival hypotheses before candidate evaluation.
4. Compare against no-message and task-specific-code baselines, with uncertainty
   and non-equivalence as legitimate outcomes.

The metric distinction follows Lowe et al., *On the Pitfalls of Measuring
Emergent Communication* (AAMAS 2019,
https://www.ifaamas.org/Proceedings/aamas2019/pdfs/p693.pdf): correlation
between messages and behavior is not causal listening. Compositionality and
novel recombination must be tested separately (Chaabouni et al., ACL 2020,
https://aclanthology.org/2020.acl-main.407/).

Reference-free coherence or shuffled-context metrics are also potentially
useful diagnostics, but fluent/human-plausible content alone is not semantic
evidence (Paradise, Gruber & Kalai, *On Non-interactive Evaluation of Animal
Communication Translators*, https://openreview.net/forum?id=EJ3uh7XPgJ).
