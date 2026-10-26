# Blind subprocess adapter V1 — executable seam, not isolation qualification

Status: `EXECUTABLE_SUBPROCESS_TRANSPORT / HOST_ISOLATION_UNVERIFIED`.

`src/unvtrslr/subprocess_blind_adapter.py` provides callable
`SubprocessBlindSender` and `SubprocessBlindReceiver` for the existing
`screen_frozen_holdout` synthetic diagnostic. Both invoke an **explicitly
configured executable** with `shell=False`. Every callback starts a fresh
child process, transmits one UTF-8 JSON document via stdin, reads a bounded
JSON response on stdout, and terminates the child. There is no runtime
connection to Num’ta’reen canon, lexicon, English glosses or target labels.

## Wire contracts

**Sender request:** exactly the existing four-key
`UNVTRSLR_BLIND_ACOUSTIC_OBSERVATION_V1` payload (`schema`,
`sample_rate_hz`, `shape`, `float64_le_b64`). Sample count, base64,
finiteness and amplitude are validated before launch.

**Sender response:**

```json
{"schema":"UNVTRSLR_SUBPROCESS_SENDER_RESPONSE_V1","message_b64":"QQ=="}
```

**Receiver request:**

```json
{"schema":"UNVTRSLR_SUBPROCESS_RECEIVER_REQUEST_V1","message_b64":"QQ==","available_actions":[0,1]}
```

`message_b64` is `null` in the no-message intervention. The receiver
response is exactly `{"schema":"UNVTRSLR_SUBPROCESS_RECEIVER_RESPONSE_V1","action":0}`
or `action:1`. The sender message must decode to 1–256 bytes and both
response objects reject extra keys, booleans masquerading as actions,
noncanonical base64 and oversized output.

## Usage

```python
from unvtrslr.subprocess_blind_adapter import (
    SubprocessBlindSender, SubprocessBlindReceiver,
)
from unvtrslr.blind_causal_screen import screen_frozen_holdout

# Paths must be absolute, and worker programs are explicitly trusted.
sender = SubprocessBlindSender(("/absolute/path/to/sender-worker",))
receiver = SubprocessBlindReceiver(("/absolute/path/to/receiver-worker",))
result = screen_frozen_holdout(frozen_evaluation, sender, receiver)
assert result.state_isolation_verified is False
assert result.causal_listening_qualified is False
```

Use a Windows absolute executable path on Windows. Workers read one JSON
document from standard input and write one JSON object to stdout. Worker
stderr is intentionally discarded so it is not treated as evaluation data.
Do not send training examples, evaluator labels, nonce, manifest commitment,
trial ordering, source IDs, codebooks or target-language strings to workers.

## Evidence and security ceiling

Executable regression `tests/test_subprocess_blind_adapter.py` uses real
Python child processes. A child can inspect **its own** stack but does not
see the parent's `_SealedTrial` frame; private test environment variables
are not inherited. It exercises timeouts, bounded stdout, strict JSON and
full sender → receiver synthetic counterfactual screening.

This closes **one specific in-process stack-inspection channel**. It does
**not** establish sealed holdout security or isolated learning. A worker
running under the same operating-system principal can still read shared
files, invoke services, contact networks, inspect clocks/process details,
or use a prearranged codebook. The adapter is **not a sandbox for untrusted
executables**: despite time and output limits, worker CPU, memory, spawned
descendants, disk and external effects are not reliably contained.
The same unprivileged OS user is not an independent trust domain.

Each call starts a fresh process, so there is no persistent learned neural
state in this transport by itself. A worker that reaches a persistent model
service could reintroduce sharing, and must be audited separately.
The existing evaluator continues to report
`IN_PROCESS_SYNTHETIC_COUNTERFACTUAL_UNQUALIFIED` and unconditional
`state_isolation_verified=False`, `causal_listening_qualified=False`.

Before any learned-grounding claim: split evaluator, sender, and receiver
across independently audited Lappy/VN1/VN2 boundaries; freeze executable,
weights, prompts and network permissions; test OS-level access to hidden
labels and cross-host side channels; randomize interventions; compare naive
frequency lookup and no-message baselines. See
`R2_THREE_HOST_CAUSAL_ACQUISITION_GATE.md`.
