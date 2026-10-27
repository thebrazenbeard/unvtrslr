# Cross-host scripted peer — bounded operational interaction trial (2026-10-27)

**Status:** ACTUAL_TWO_HOST_TRANSPORT_PASS; SCRIPTED_PARTNER_ONLY; HIDDEN_RUNTIME_RULE; NO_INDEPENDENT_INTELLIGENCE; NO SEMANTIC QUALIFICATION.

## Exact subjects and execution

This extends UNVTRSLR `main@a10af7930e41d96518f6477d7aa56127d79dda91` (merged PR #50). The learner ran on Windows Lappy, while a separately started Python 3.12 standard-library HTTP service ran on Linux VN2. The service was developed and run privately on VN2 *before* its source was copied into `runs/contact_20261027/reference_peer_service.py` **after** the trial to preserve reconstructible source. The peer's executable file hash was SHA-256 `eecf9bf7779350beaa4c4c2b0ebe559f2cbc63e1d08c3a9aee36a2466513aff4`. The private, generated rule/salt for each session was not shipped to Lappy or source control. Both hosts are operated by the same user/orchestrator: this is **host separation, NOT independent outside authorship**.

Transport: Tailscale-private address-bound HTTP on port 18047, bearer token stored only in private local scratch files (never source or report); request size limits, finite sessions and observation counts, strict JSON API, and explicit GET paths. HTTP has no application-layer TLS; tailnet transport encrypts node-to-node packets subject to Tailscale identity/security. VN2 peer directory mode 0700 and authorization-token file mode 0600. From Lappy, unauthenticated POST returned HTTP 403; a GET requesting private file returned HTTP 404. These are route-denial demonstrations, **not** comprehensive filesystem/OS-level access-control proofs; same VN2 user owning the daemon can read its own files and an authorized client can make finite protocol queries. Service was scoped to this experiment, not installed as a persistent production daemon.

## Interactive protocol

`runs/contact_20261027/crosshost_trial.py` uses the existing `negotiate()` learner through a remote `PartnerPort`. Client sends bounded numeric scene observations and arbitrary waveforms over the network. The peer privately chooses mode, channel-to-feature rule and signal polarity; a session-start hash commits to rule plus random salt. The learner receives no peer-private mode, rule or withheld scene coordinates.

After training, the client submits only a frozen learned sensor axis and outbound motif mapping. VN2, **not Lappy**, generates four fresh held-out feature combinations with random magnitudes and computes both observed outcome and a wrong-signal intervention. Peer qualification is one-shot, private, and recorded on VN2; client receives only outcomes, counts and SHA-256 receipt commitment. A constant-positive-reward partner is explicitly rejected by the wrong-signal contrast. Failed agreement, absent responses or uninterpretable signals do not receive a success claim.

## Actually executed results

Eight distinct unknown-parameter scripted peer sessions, randomized privately in VN2, produced:
- **2 HOLDOUT_PASS**: one responsive and one slow-to-adapt peer. Both required actual waveform exposure; the slow peer needed a second round of proposals. Observed held-out wrong-signal advantage 0.8.
- **1 HOLDOUT_FAIL**: peer whose classification behavior changed before the withheld contexts (ablation advantage 0.0).
- **5 INELIGIBLE**: constant-positive-reward, non-adapting, fixed-channel, independent/random-channel, and silent control partners.

The Lappy result `research/CROSSHOST_SCRIPTED_PEER_20261027.json` is a credential-free source-bound client receipt; SHA-256 `b4d1e78c1b8901f6dd022661185b46d560353e4c97ed461fe1baa800d6532990`. Readback directly from VN2's private JSONL showed exactly the same 8 terminal statuses; **all eight individual private record SHA-256 digests matched the client's receipts**. VN2 runtime source was snapshot into Git without including its `token.txt`, private random salts or hidden session data. The full private raw receipts remain VN2 runtime-only material, separate from the public research summary. Do not use this as evidence of third-party independent review.

## Scientific and security ceiling

This demonstrates that an actual remote computer can act as a peer for the existing learner using a bounded interaction interface while withholding session-specific rules and held-out situations. It is not autonomous discovery of an arbitrary partner, nor proof of language, negotiated human meaning, self-aware intelligence, extraterrestrial existence or a universal ontology. The peer remains a Python program with supplied two-dimensional scene vectors, predeclared observation/offer/outcome actions, known sensor type, familiar pulse-class behavior, and an explicit scalar task feedback signal. Communication-protocol custody is narrower than security against intentionally malicious peer code.

A genuine next gate requires a truly independent third-party participant or device implementation, prospective precommitment of interventions, raw independent observations with no forced 2-channel encoding, nonnumeric/nonlinguistic alternatives, consent-safe active probes, access-restricted evaluator truth with negative canary tests, random partner swaps and transfer, and independently adjudicated semantics. Keep [mission issue #48](https://github.com/thebrazenbeard/unvtrslr/issues/48) OPEN. Separately keep [issue #44](https://github.com/thebrazenbeard/unvtrslr/issues/44) OPEN for strong OS isolation and blinded human adequacy; both remain unqualified by this synthetic peer.

**Reconstruction:** instantiate the posttrial peer source as a separate authorized Linux process with its own new private token, bind only to an allowed Tailscale address, and run `crosshost_trial.py` on a different trusted workstation using `--endpoint`, external `--token-file`, fresh `--report-out`; a new randomized private peer state will generate a *different* receipt and is not an exact replay of this trial. Never commit secrets, infer identity from host separation, or continue exposing the temporary peer listener after testing.
