# UNVTRSLR

**An experimental toolkit for discovering, testing, and rendering communication across systems that do not start with a shared language.**

UNVTRSLR explores a question more basic than conventional translation: when two systems do not agree on words, symbols, message boundaries, or even what counts as a signal, can they establish reusable distinctions from observable interaction?

This repository contains a Python reference package, command-line tools, synthetic experiments, qualification harnesses, and an adversarial research program. It is **not** a working universal translator or a demonstrated way to communicate with extraterrestrial intelligence.

> **License:** Source-available proprietary software, **not open source**. The [LICENSE](LICENSE) permits limited private noncommercial evaluation, research, education, security review, and interoperability assessment. Commercial use, redistribution, hosted use, and public deployment of modified versions require separate permission. See [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md); third-party components retain their own terms.

## What the package does today

The Python package (Python 3.11+, NumPy, SciPy) exposes reference tools for:

| Component | Implemented interface | Scope |
| --- | --- | --- |
| Acoustic fingerprints | `unvtrslr-fingerprint` | Measures PCM WAV recordings without assuming their sounds are words. |
| Candidate acoustic events and recurring units | `unvtrslr-register-units`, `unvtrslr-unit-model` | Builds and checks recording-local observations and cross-recording acoustic identities. |
| Reference translation | `unvtrslr-translate` | Fits operational acoustic/context correspondences, freezes a new source's calibration separately, and renders a later query with an optional label map. |
| Order and target construction probes | `unvtrslr-order`, `unvtrslr-target`, `unvtrslr-construct` | Tests order-sensitive relations and target-language realizations in constrained demonstrations. |
| Qualification utilities | `unvtrslr-qualify-calibration`, `unvtrslr-qualify-multilingual` | Reports held-out results under declared calibration/corpus conditions; does not certify universal meaning. |

The package also includes research modules for signal discovery, interaction contingency, rival hypotheses, R0.5 information-integrity controls, and R1/R2 adversarial evaluation. The cross-process and cross-host scripted-peer studies are **opt-in research experiments**, not production networking, safe execution of arbitrary untrusted models, or evidence of independently initiated communication.

Source: [`pyproject.toml`](pyproject.toml), [`src/unvtrslr/`](src/unvtrslr/), [`tests/`](tests/), and the [claims/evidence ledger](research/CLAIMS_AND_EVIDENCE.md).

## Install and try a local measurement

In a Python 3.11+ environment, from a checkout:

```bash
python -m pip install .
unvtrslr-fingerprint recording.wav
```

`recording.wav` is a **user-provided PCM WAV**. The command outputs a JSON acoustic fingerprint; it does not recognize speech or assign meaning. The current WAV reader supports 8-, 16-, and 32-bit integer PCM and preserves multichannel samples instead of averaging away channel differences. Run `unvtrslr-fingerprint --help` for CLI options.

To explore the source-calibrated reference translator, inspect the real CLI contract:

```bash
unvtrslr-translate --help
unvtrslr-translate prepare-wav recording.wav \
  --recording-id observation-001 \
  --source-id source-a > observation.jsonl
```

The latter step only prepares recording-local evidence. Fitting a translator requires a **separate, adequately replicated training-episode JSONL dataset** with acoustic evidence and declared context; the system does not infer that context from audio. Before query translation, a new source requires independent calibration evidence, frozen into a profile. The query cannot calibrate itself:

```bash
unvtrslr-translate fit training-episodes.jsonl > translator.json
unvtrslr-translate calibrate translator.json source-a-calibration.jsonl > source-a-profile.json
unvtrslr-translate translate translator.json source-a-profile.json source-a-query.jsonl
```

Those filenames are illustrative inputs the caller must supply, **not files bundled with the repository**. Training data must satisfy the source/contrast and semantic replication gates; missing evidence or unresolved relations can legitimately fail or abstain. For schemas, optional rendering, constraints, and examples see [Reference Translator V2](docs/REFERENCE_TRANSLATOR_V2.md).

## How the research works

The proposed progression is:

1. **Observe:** preserve raw measurements and detect candidate regularities without prelabeling communication.
2. **Audit:** check whether the observations could identify the claimed distinction; detect leaked labels, destructive preprocessing, hidden bridges, and evaluator-authored shortcuts.
3. **Hypothesize:** compare minimal candidate structures such as typed probabilistic hypergraphs (TPH), denotational constraint algebra (DCA), and predictive-intervention states (PIS).
4. **Intervene:** test changes in message, world, context, partner, sensor, and task against rival explanations and negative controls.
5. **Render cautiously:** emit a target-language representation only where relations have been tested, retaining uncertainty, provenance, and scoped non-equivalence.

The design does **not** assume speech, text, two individuals, discrete symbols, a universal ontology, or mathematical notation that magically supplies meaning. English is only one optional renderer. Task success alone can arise from private shortcut codes; it is not proof of grounded semantics.

Key documents:

- [Project thesis](docs/PROJECT_THESIS.md) and [design principles](docs/DESIGN_PRINCIPLES.md)
- [Bootstrap protocol](docs/BOOTSTRAP_PROTOCOL.md), [semantic conservation](docs/SEMANTIC_CONSERVATION.md), and [failure modes](docs/FAILURE_MODES.md)
- [R0.5 information-integrity audit](docs/R0_5_INFORMATION_INTEGRITY_AUDIT.md)
- [R1 substrate competition](docs/R1_SUBSTRATE_COMPETITION.md) and [R2 adversarial evaluator](docs/R2_ADVERSARIAL_EVALUATOR.md)
- [R2 semantic-claim controls](docs/R2_SEMANTIC_CLAIM_CONTROLS.md) and [evaluation contract](specs/R1R2_EVALUATION_CONTRACT_V1.yaml)
- [Research roadmap](docs/ROADMAP.md) and [claims/evidence ledger](research/CLAIMS_AND_EVIDENCE.md)

## Evidence and maturity

**Status: research/reference implementation; no universal-translation, unknown-intelligence-contact, or production-deployment qualification.**

- The package includes tested synthetic/reference tools for acoustic evidence, cross-source recurring units, operational correspondences, order-sensitive relations, target construction, and some multilingual evaluation regimes. These do not establish a uniquely correct ontology or universal grounding.
- A [synthetic namespaced learner study](research/ISOLATED_LEARNER_RUNTIME_V1_20261027.md), a [fixed-worker namespace custody diagnostic](research/VN2_NAMESPACE_ACCESS_GATE_20261027.md), and a [scripted two-host peer trial](research/CROSSHOST_SCRIPTED_PEER_20261027.md) have recorded bounded outcomes. Their named historical hosts are **experiment provenance**, not installation requirements or generalizable security certification.
- The [synthetic contact/interaction study](research/AUTONOMOUS_CANDIDATES_AND_INTERACTIVE_CONTACT_20261027.md) does not demonstrate independently discovered communicative intent. The [bootstrap contingency study](research/BOOTSTRAP_CONTINGENCY_20261027.md) does not demonstrate negotiated semantics.
- The [first MASSIVE 1.0 real-corpus run](evidence/real_corpus/massive_v1_20260922/RESULT.md) **failed** its preregistered multilingual holdout gate: 1,000 held-out records over five languages produced 29.3% macro coverage, **1.0% macro exact match**, and 7.235% macro token similarity. The [multilingual qualification contract](docs/MULTILINGUAL_HELDOUT_QUALIFICATION_V1.md) explains the declared regimes; no real-corpus qualification pass is claimed.
- Source-calibration profiles isolate queries from their own normalization data; they do **not** authenticate external preregistration, independent source identity, or the validity of all semantic labels. See [Reference Translator V2](docs/REFERENCE_TRANSLATOR_V2.md).

The [R2 process-channel smoke screen](docs/R2_PROCESS_CHANNEL_SMOKE_V1.md) separates Python processes and applies synthetic controls but is **not a sandbox**. A namespace diagnostic for a fixed worker is not containment for adversarial arbitrary code. Source-level startup regressions address a known editor-task loader vector; they cannot attest to the security of a user's installed machine or other revisions. See [startup safety tests](tests/test_workspace_startup_safety.py).

## Testing and contribution

From a development checkout with test dependencies installed:

```bash
python -m pip install -e . pytest
python -m pytest -q
```

Tests cover the implemented reference interfaces, negative controls, and known integrity regressions; passing them is not independent scientific validation. Reproduce experiments only in an isolated environment with data and host access you are authorized to use. Do not treat experiment metadata, a learner's claimed identity, a model's opinion, or a mutable wrapper as host-granted consent or authority.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CLA.md](CLA.md) before proposing changes. Proprietary license boundaries apply even to publicly readable code.
