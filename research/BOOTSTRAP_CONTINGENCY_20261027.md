# UNVTRSLR Phase-0 active-probe contingency gate (2026-10-27)

**Primary mission restored:** communication bootstrap with zero shared symbols is the core, **not** translation between pairs of already-known human languages. Source: `README.md` and `docs/BOOTSTRAP_PROTOCOL.md`, as of `main@25146d41fa6cdb5a67a5658a271bba9d741edc19`.

The first executable slice is `src/unvtrslr/bootstrap_contingency.py`. It accepts bounded, numeric 16-sample receiver-response traces collected under *deliberately applied candidate probes*. It does not inspect words, messages, translations, meanings, shared object IDs, sender intentions or author-dictionary tokens. A trial records only the chosen probe (`sham`, `probe_a`, `probe_b`), randomized within-block order, experimenter-declared setting/block identity, and a continuous measured response. Both candidate probes are arbitrary lab actions, **not inferred messages from an unrecognized intelligence**.

The trained screen estimates *sham-adjusted* delayed-minus-baseline effects for both probe choices within balanced, matched intervention triples. It selects only if one candidate has a stable, direction-consistent effect above an a-priori lab threshold in **every** training setting, dominates the other candidate, and has no equally strong immediate-window response. It checks a frozen choice on disjoint, unseen settings and can produce either `NO_DISCRIMINATING_RESPONSE_CONTINGENCY`, `HELDOUT_CONTINGENCY_NOT_REPLICATED`, `HELDOUT_RESPONSE_AMBIGUOUS`, or `RESPONSE_CONTINGENCY_REPLICATED_IN_HELDOUT_SETTINGS`. This is *contingent environmental responsiveness only*.

## Executed evaluator controls

`runs/bootstrap_20261027/run.py` generates 21 synthetic cases (3 seeds x 7 interventions) with 108 training and 108 held-out continuous response observations each. For each seed, the learner detects the deliberately contingent later response to `probe_b` and refuses to call five negative-control families a stable response (no response, context-only apparent signals, immediate-only artifact, ambiguous two-probe response, order-linked artifact); a sixth (`training_only`) explicitly fails fresh-setting replication. The evaluator truth and generator remain in the same user-accessible repository and can be inspected. Reproduce with `python runs/bootstrap_20261027/run.py --out <new-report.json>`; source run report `research/BOOTSTRAP_CAUSAL_CONTROLS_20261027.json`. Thresholds are lab heuristics fixed in code, **not** calibration from independently acquired data or a formal causal identification proof.

**What this corrects:** the recently merged Argos/MASSIVE and SCAN efforts improved a limited translation/linguistic branch, but measured neither detection of communicative intention nor the possible absence of a language channel. The controlled probe gate makes a small, falsifiable contribution toward Phase 0/1 without elevating translated strings to semantic evidence.

## Non-negotiable limitations

- The controller supplied probe boundaries, source of intervention, sensing schedule, temporal segments, target measured response channel, and matched setting labels. Hence **not** signalhood discovery from a continuous, unsegmented stream.
- Matched effects do not prove communication (physical reflex, involuntary response, environmental interference, private model coding, or instrument artifact remain alternatives); there is no inferred referent, ontology, joint attention, or negotiated convention.
- Randomization arises in a synthetic generator; there is **no independent live partner, no hardware experiment, no OS-enforced evaluator isolation, and no external causal experiment attestation**.
- No score proves unknown intelligence, extraterrestrial communication, language acquisition, or universality. Consent, cautious intervention, and non-coercive safety rules matter before interacting with a real partner.
- Shared mathematics can encode the evidence, hypotheses, uncertainty and provenance, but **does not instantiate universal meaning by fiat**.
- English must stay an optional *renderer*. Many-to-many human-language translation, nonverbal modalities, hypothetical unknown languages, and shared-concept comparison are separate future empirical pathways.
- Source/build/CI, lab scenario effect, genuine external interaction, grounding, verified bidirectional negotiation, bilingual human adequacy and deployment are different states. No current qualification transfers between them.

## Repair and research backlog

1. **Next bootstrap gate:** infer candidate communication channel and signal segmentation from raw, continuous multi-channel observations with no experimenter-authored communication intervals or known partner; compare noncommunicative periodic/nuisance traces, replay vs altered timing, and null/unknown rivals.
2. **Bidirectional negotiation:** implement active closed-loop partner adaptation with correction, refusal, acknowledgments, and role reversal, with tests on new contexts, partners, sensors and tasks. Require prospective interventions rather than simply fitting evaluator-labeled classes.
3. **Semantics:** compete TPH/DCA/PIS with intervened referents, novelty, cross-situation transfer, non-equivalent meanings and withheld counterfactual truth; demonstrate extra falsifiable obligations beyond operational task reward.
4. **Multilingual plus nonverbal:** source-agnostic language/motion/audio/environment adapters should target learned relations and non-equivalence, not route everything through English. No automatic Num’ta’reen canon modifications.
5. **Existing issue #44:** complete genuine OS-level worker isolation with denied evaluator-gold access and independent bilingual reviewers on Argos packets; the existing 80 tasks have zero real human ratings and must not be rebranded as human adequacy. Existing issue #46 retains variable-length SCAN/real-multilingual learning and author-heldout Num'ta’reen acceptance tests.

No native ChatGPT subagent dispatch capability was exposed in this conversation. No fabricated dispatch receipts, other agent qualification, contact with nonhuman intelligence, or human semantic reviews are reported.
