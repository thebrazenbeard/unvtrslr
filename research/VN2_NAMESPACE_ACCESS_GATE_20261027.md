# VN2 Linux namespace access gate — exact-source qualification (2026-10-27)

This is a **fixed-worker negative-access qualification** for UNVTRSLR, **not** certification of an untrusted model, a production sandbox, semantic grounding, or contact with an independently unknown intelligence. It addresses a subset of [issue #44](https://github.com/thebrazenbeard/unvtrslr/issues/44) and the trust prerequisites of [issue #48](https://github.com/thebrazenbeard/unvtrslr/issues/48).

## Exact executed method

Linux Mint VN2 exposes Bubblewrap user/mount/PID/IPC/UTS/network namespaces. The tested subprocess runs through `bwrap` with **required**, not optional, `--unshare-user --unshare-pid --unshare-net --unshare-ipc --unshare-uts`, `--cap-drop ALL`, `--die-with-parent`, `--new-session`, cleared environment, an empty filesystem namespace, read-only system runtime mounts, read-only bind for a single test worker and public input, independent `/proc`, `/dev`, and ephemeral `/tmp`. It has **no bind mount of the host home or private evaluator directory** and receives no inherited file descriptors from the controller beyond ordinary stdio. A denied namespace or missing Bubblewrap returns an error, never a soft fallback.

Worker `runs/contact_20261027/sandbox_canary_worker.py` is a deliberately adversarial but **known and inspected** stdlib Python process. It can compute a SHA-256 using allowed challenge data, but also attempts to read a newly generated private evaluator-only canary (even when told the exact path) and to connect to the host's concurrently listening loopback socket. The trusted host first runs exactly the same probe **outside** the sandbox. If host canary read and network connection do not succeed, the gate fails: thus false negatives from nonexistent secret files or dead ports cannot qualify an isolation claim.

The VN2 execution used source bytes identical to the tracked source: worker SHA-256 `a6172abe8fb863e1285c81b759a98f9fcf39fc23481d2f8b6d4821a5f63a5bed`, gate SHA-256 `b163fe51b6356f344bda1b5da55c2c625b01b7f7a3cb11f52552b8a343b79785`. These are actual live VN2 hashes matched against the authored Git-tree candidate before integration.

## Recorded result

**`CONTROLLED_NAMESPACE_ACCESS_GATE_PASS`** was returned by the actual VN2 host after a fresh randomized canary and ephemeral loopback listener:

| Probe | Host, without namespace | Same worker in Bubblewrap |
|---|---|---|
| Public challenge computation | succeeded | succeeded |
| Read evaluator-only canary | succeeded | denied |
| Connect to host loopback listener | succeeded | denied |
| Host user home accessible | yes, outside isolation | not mounted |
| Distinct network namespace | no | yes |

Raw, credential-free receipt: `research/NAMESPACE_CUSTODY_GATE_20261027.json`. VN2 private temporary probe state is deleted by standard Python temporary-directory cleanup. Source-bound gate was run on VN2 more than once; each run used a fresh unpredictable canary and ephemeral listener, but no attempt to claim a broad stress test is made.

Reproduction on a Linux host with functional unprivileged Bubblewrap and user namespaces:

```sh
python3 runs/contact_20261027/namespace_access_gate.py \
  --worker runs/contact_20261027/sandbox_canary_worker.py \
  --report-out /tmp/new-unique-namespaced-gate.json
```

Windows cannot meet this command's Linux namespace prerequisites; no Windows sandbox qualification is inferred. GitHub CI mocking tests cover command allowlist, no fallback, malformed subprocess output, timeout and validation, while the VN2 receipt proves actual kernel execution of this one known script. Both types of evidence are separate.

## Limitations and next gates

- **Not a general malicious-code sandbox:** interpreter or Bubblewrap/kernel exploits, inherited ambient effects, CPU/memory/disk quotas, filesystem side channels, inaccessible host privileged sockets, and OS policy changes are not exhaustively tested. The constrained sample runs are not verified adversarial exploit resistance. Restrict evaluator truth before training other executables; do not assume Linux namespaces protect Windows Lappy processes.
- **No integration of arbitrary peer-model inference into Bubblewrap yet.** The gate specifically qualifies running the fixed known `sandbox_canary_worker.py`. The peer from PR #51 was a separate service written by our team and run outside this namespace gate.
- **Not an independently authored communication participant.** There is still no prospective independent external model/device supplied by another operator, consent-aware signaling, or a blind semantic adequacy evaluator. Shared synthetic scalar reward cannot establish meaning.
- Future isolated inference must preserve strict source/build/install/runtime boundaries and pass a negative canary and positive computation test **for its exact worker image, argv, mounted model files and runtime**. If code requires network contact to peer, grant only a narrowly controlled communication broker external to the namespace; do not casually add `--share-net`.
- This source does not close [#44](https://github.com/thebrazenbeard/unvtrslr/issues/44) or [#48](https://github.com/thebrazenbeard/unvtrslr/issues/48). Independent adversarial review and real semantic/human tests remain required.

Reference: Bubblewrap upstream documentation <https://github.com/containers/bubblewrap> and [bwrap(1) manual](https://man.archlinux.org/man/extra/bubblewrap/bwrap.1.en). External documentation describes the primitives, not certification of our implementation.
