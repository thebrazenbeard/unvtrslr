# Claims and Evidence Ledger

This file separates prior evidence from UNVTRSLR hypotheses and speculation.

Status vocabulary:

- `SUPPORTED_PRIOR_WORK` — directly supported by cited research.
- `SUPPORTED_LIMITED_SCOPE` — supported only under narrower conditions than the project target.
- `PROJECT_HYPOTHESIS` — plausible but not demonstrated for UNVTRSLR.
- `DESIGN_REQUIREMENT` — chosen constraint, not empirical fact.
- `OPEN_QUESTION` — unresolved.
- `SPECULATIVE_INTERSTELLAR` — extrapolation beyond validated Earth evidence.

## C001 — Formal symbols do not automatically provide grounded meaning

**Status:** `SUPPORTED_PRIOR_WORK`

Harnad's symbol-grounding problem directly motivates this claim.

**Project consequence:** mathematics may carry formal structure but cannot simply be declared universally meaningful.

## C002 — Shared environmental interaction can bootstrap communication conventions

**Status:** `SUPPORTED_LIMITED_SCOPE`

Grounded language-game and robot experiments show shared lexicons and simple compositional structures emerging under situated interaction.

**Limit:** those systems generally assume more shared perceptual/task structure than the strongest UNVTRSLR target.

## C003 — Successful emergent communication can lack evaluator-recognizable conceptual semantics

**Status:** `SUPPORTED_PRIOR_WORK`

Bouchacourt & Baroni (2018) show successful communication despite visual representations that do not capture the conceptual properties humans might assume.

**Project consequence:** task reward alone cannot qualify semantic grounding.

## C004 — Richer/generalization-oriented games can improve emergent communication structure

**Status:** `SUPPORTED_LIMITED_SCOPE`

Mu & Goodman and related work support this under controlled artificial-agent tasks.

**Project consequence:** first experiments should require generalizations and relationships, not only single-object reference.

## C005 — Compositionality and generalization are not identical

**Status:** `SUPPORTED_PRIOR_WORK`

Emergent-language research finds they can dissociate depending on task and metric.

**Project consequence:** use multiple compositionality/generalization measures and behavioral tests.

## C006 — Humans can create new nonlinguistic conventions using common ground

**Status:** `SUPPORTED_PRIOR_WORK`

Human experiments on instantaneous conventions show minimal signals can acquire context-dependent communicative functions.

**Project consequence:** nonlinguistic bootstrap is empirically plausible at least for humans.

## C007 — A cross-linguistic human semantic core may exist

**Status:** `SUPPORTED_LIMITED_SCOPE`

NSM researchers propose 65 semantic primes shared across human languages and provide extensive cross-linguistic evidence.

**Limit:** the claim remains a linguistic theory about humans; it is not evidence of species-independent universality.

## C008 — Cross-lingual formal meaning representations are feasible

**Status:** `SUPPORTED_LIMITED_SCOPE`

UMR demonstrates a graph formalism representing shared semantic structures across multiple diverse human languages.

**Limit:** UMR categories remain human-linguistic and do not prove modality- or species-neutrality.

## C009 — Nonhuman communication can encode quantitative/spatial structure in non-word-like behavior

**Status:** `SUPPORTED_PRIOR_WORK`

Honeybee waggle dances encode direction and distance through motion parameters.

**Project consequence:** discrete symbols cannot be an ingress requirement.

## C010 — Animal signals can require context for interpretation

**Status:** `SUPPORTED_PRIOR_WORK`

Later vervet-monkey work shows context dependence and overlap beyond simple predator-word mappings.

**Project consequence:** use conditional semantic hypotheses rather than fixed dictionaries.

## C011 — Predictive acoustic modeling is not equivalent to demonstrated semantic translation

**Status:** `DESIGN_REQUIREMENT`

This is a methodological distinction supported by the gap between acoustic-generation objectives and behavioral semantic evidence.

**Project consequence:** animal-inspired controls must separate acoustic structure from meaning claims.

## C012 — Progressive mathematical/scientific teaching has historical precedent in interstellar messaging

**Status:** `SUPPORTED_PRIOR_WORK`

Lincos is the strongest direct example; Voyager/Arecibo and later message designs also use mathematics/physics as bootstrap material.

## C013 — Lincos assumes a mentally humanlike receiver

**Status:** `SUPPORTED_PRIOR_WORK`

Freudenthal states this assumption explicitly.

**Project consequence:** UNVTRSLR should test synthetic receivers that violate it.

## C014 — Shared physics may offer interstellar common ground

**Status:** `PROJECT_HYPOTHESIS`

Interstellar-message literature commonly treats physics and mathematics as promising shared structure, but exosemiotic critiques warn that representations and concepts need not be interpreted identically.

**Project consequence:** use physics as a candidate anchor to be demonstrated, not an assumed language.

## C015 — A translator may be a better interstellar payload than a static message

**Status:** `SPECULATIVE_INTERSTELLAR`

This is the founding UNVTRSLR proposition.

**Supporting reasoning:** an adaptive system can test mappings after contact rather than requiring all semantics to be anticipated before launch.

**Major limitation:** embodied probes have extreme travel-time and autonomy constraints; broadcasts lack local shared interaction.

## C016 — Signalhood can be inferred without a pre-labeled communication channel

**Status:** `PROJECT_HYPOTHESIS`

Human and animal research suggests audience effects, contingency, coordination, and interaction patterns can reveal communicative function.

**Not yet shown:** a general artificial system that can reliably discover signalhood under the full UNVTRSLR conditions.

## C017 — Shared semantics can emerge despite different sensory encodings

**Status:** `PROJECT_HYPOTHESIS`

Grounded and multimodal research makes this plausible, but the strongest condition—materially different perceptual ontologies with no shared latent representation—requires direct testing.

## C018 — Active interventions can distinguish semantic hypotheses better than passive association

**Status:** `PROJECT_HYPOTHESIS`

The principle follows standard experimental-design reasoning, but its benefit and safety tradeoffs in semantic bootstrap must be measured.

## C019 — Semantic non-equivalence can be detected operationally

**Status:** `PROJECT_HYPOTHESIS`

Human translation already contains many partial/one-to-many mappings, but a system that discovers rather than receives non-equivalence requires experimental validation.

## C020 — A universal representation grammar may be possible without a universal ontology

**Status:** `PROJECT_HYPOTHESIS`

Candidate structural responsibilities include event, relation, quantity, time, space, provenance, uncertainty, and alternatives.

**Falsifier:** if successful systems require domain-specific or species-specific primitives so extensively that the common kernel contributes no transferable value.

## C021 — Semantic conservation can be evaluated independently of target-text similarity

**Status:** `PROJECT_HYPOTHESIS`

The proposed method uses tested invariants, interventions, and independent semantic reconstruction.

**Open:** how to discover important invariants without human annotation at scale.

## C022 — Role reversal is stronger evidence of shared semantics than one-way response success

**Status:** `DESIGN_REQUIREMENT`

This is adopted as a qualification pressure rather than claimed as a universal psychological law.

## C023 — `NO_FAITHFUL_EQUIVALENT` should be rewarded

**Status:** `DESIGN_REQUIREMENT`

Without this outcome, evaluation incentivizes forced translation and anthropocentric category collapse.

## C024 — English should not be the internal semantic substrate

**Status:** `DESIGN_REQUIREMENT`

English is one renderer among many. Internal English would silently privilege English categories.

## C025 — A self-describing semantic broadcast is possible

**Status:** `OPEN_QUESTION / SPECULATIVE_INTERSTELLAR`

Lincos and interstellar-decoding literature suggest progressive teaching can convey increasingly rich structure, but a receiver with radically different priors may fail to reconstruct framing or intended semantics.

## C026 — A self-describing protocol can be tested on Earth

**Status:** `PROJECT_HYPOTHESIS`

Receivers can be denied protocol documentation and evaluated on how much framing/semantics they reconstruct from controlled streams.

## C027 — Probe and broadcast architectures should share a semantic core but different bootstrap regimes

**Status:** `DESIGN_REQUIREMENT`

Local interaction changes the problem enough that one curriculum should not be assumed optimal for both.

## C028 — Communication understanding must remain separate from permission to act

**Status:** `DESIGN_REQUIREMENT`

Especially important for embodied probe or machine-control settings.

## C029 — No current evidence proves a truly universal translator is feasible

**Status:** `SUPPORTED_PRIOR_WORK / PROJECT_BOUNDARY`

Existing work demonstrates partial responsibilities under constrained assumptions. The combined zero-language, unknown-channel, asymmetric-ontology target remains unproven.

## C030 — The project is scientifically useful even if universality fails

**Status:** `PROJECT_HYPOTHESIS`

A staged failure can identify which assumptions—shared perception, common context, cooperation, compositionality, interaction, or humanlike concepts—are actually necessary for communication.

## R1/R2 additions

## C031 — A semantic substrate need not be an explicit symbolic ontology

**Status:** `SUPPORTED_LIMITED_SCOPE / PROJECT_HYPOTHESIS`

Predictive-state-representation research shows that dynamical state can be represented using action-conditioned predictions of future observations rather than hidden-state labels.

**Project consequence:** PIS is a serious non-symbolic R1 rival.

**Limit:** prior PSR work does not establish semantic communication or translation.

## C032 — Message/action correlation does not establish communication

**Status:** `SUPPORTED_PRIOR_WORK`

Lowe et al. demonstrate settings where messages contain information about subsequent actions but do not causally affect the environment or other agent.

**Project consequence:** direct message intervention and ablation are critical R2 tests.

## C033 — Causal listening is necessary but not sufficient for grounded semantics

**Status:** `DESIGN_REQUIREMENT / PROJECT_HYPOTHESIS`

Counterfactual social-influence research supports causal influence as a stronger communication signal than correlation alone.

However, an action-plan code may causally control a receiver while remaining task-bound.

**Project consequence:** causal listening must be combined with world-factor interventions, cross-task transfer, role reversal, and partner transfer.

## C034 — Arbitrary notation is not evidence against grounding

**Status:** `DESIGN_REQUIREMENT`

A convention may use arbitrary signs while remaining externally grounded.

**Project consequence:** R2 ignores consequence-preserving symbol permutations. It targets hidden common ground and task-private shortcuts rather than human unreadability.

## C035 — Unique unsupervised semantic ontology recovery cannot be assumed

**Status:** `SUPPORTED_LIMITED_SCOPE / PROJECT_BOUNDARY`

Locatello et al. show that unsupervised disentangled representation learning is not identifiable without inductive biases.

**Project consequence:** UNVTRSLR must record substrate inductive biases and avoid claiming a unique true internal ontology from observation alone.

## C036 — Grounding qualification must be explicitly scope-bounded

**Status:** `DESIGN_REQUIREMENT`

No finite evaluator can distinguish hypotheses that make identical predictions over every tested observation and intervention but diverge only outside the tested family.

**Project consequence:** use `GROUNDED_WITHIN_TESTED_SCOPE`, bind certificates to exact world/intervention families, and retain surviving alternative explanations.

## C037 — Cross-task and third-party transfer are key tests against private task code

**Status:** `PROJECT_HYPOTHESIS / DESIGN_REQUIREMENT`

If a signal tracks a reusable world invariant, it should often remain useful when the optimal downstream action changes and should be re-groundable by an independently initialized partner.

**Falsifier:** if genuinely grounded conventions systematically fail these tests while known private task codes pass them under a trustworthy harness.

## C038 — A richer semantic substrate should not win by interpretability alone

**Status:** `DESIGN_REQUIREMENT`

Human-readable graphs can create false confidence.

**Project consequence:** R1 uses empirical semantic qualification plus explicit complexity accounting. A richer substrate must earn complexity through transfer, calibration, non-equivalence, conservation, or efficiency.

## C039 — No single scalar should certify grounded meaning

**Status:** `DESIGN_REQUIREMENT`

Task reward, mutual information, compositionality, causal influence, reconstruction accuracy, and language similarity each capture only part of the target.

**Project consequence:** R2 emits a conjunctive operational-grounding vector with critical failure gates.

## C040 — A semantic evaluator must be able to reject strong intentionally broken systems

**Status:** `DESIGN_REQUIREMENT`

An evaluator that only recognizes obvious random failure has not demonstrated shortcut resistance.

**Project consequence:** R2 requires a suite of adversarial negative controls designed to perform well on naive task metrics.

## Human verbal-language Pass 1 additions

## C041 — Humans can reduce referential ambiguity across repeated ambiguous contexts

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Smith & Yu (2008) show infant cross-situational accumulation of word-referent evidence across ambiguous trials.

**Project consequence:** maintain competing mapping hypotheses across encounters; do not require one-shot ostension.

**Claim ceiling:** this does not establish arbitrary-agent grounding, unknown signalhood, or sufficiency of passive co-occurrence.

## C042 — Conventionally defined joint attention is not necessary or sufficient for human word learning

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Akhtar & Gernsbacher (2007) review evidence for word learning without conventional joint-attention markers and joint attention without commensurate vocabulary learning.

**Project consequence:** gaze, pointing, and shared visual fixation cannot be mandatory bootstrap primitives.

**Open:** what weaker cross-party evidence relation is actually necessary.

## C043 — Human turn-taking is strongly structured across languages but must not become universal framing canon

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Stivers et al. (2009) find broad commonalities in minimizing gaps/overlap across ten languages with cultural timing variation.

**Project consequence:** turn-like alternation is legitimate signalhood evidence, not a required discrete-message architecture.

## C044 — Repair is a robust human conversational mechanism for resolving communication problems

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Dingemanse et al. (2015) find broad cross-linguistic commonalities in other-initiated repair.

**Project consequence:** test repair early and compare repair-rich/disabled/corrupted conditions.

**Constraint:** repair functions must be inferred from interaction; evaluator labels such as `REPAIR` or `CORRECTION` are leakage.

## C045 — Humans can rapidly invent communication conventions in unfamiliar restricted channels

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Galantucci (2005) demonstrates rapid emergence of novel graphic communication systems under task restrictions.

**Project consequence:** negotiated convention is empirically plausible for humans.

**Claim ceiling:** convention invention is not evidence of decoding pre-existing counterpart semantics.

## C046 — Human vocal iconicity can bootstrap some novel mappings

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Perlman & Lupyan (2018) and Ćwiek et al. (2021) show above-chance human comprehension of novel iconic vocalizations, including cross-cultural tests.

**Project consequence:** iconicity is an accelerator/control condition.

**Claim ceiling:** no species-neutral or arbitrary-channel universality follows.

## C047 — Cultural transmission can increase regularity/structure after a signaling system exists

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Kirby, Cornish & Smith (2008) show artificial human languages become more learnable/structured across transmission chains.

**Project consequence:** separate initial grounding, convention stabilization, and later systematization/compositional emergence.

**Claim ceiling:** the experiment prespecifies meanings and channels; it is not zero-shared-semantics evidence.

## C048 — Human languages partition semantic domains differently

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Semantic typology documents substantial cross-linguistic variation in category boundaries across domains such as color, kinship, number, folk biology, and space.

**Project consequence:** one-to-one lexical mapping cannot be assumed even for human controls; partial overlap and one-to-many/many-to-one mappings must be first-class.

## C049 — Information-source/provenance distinctions can themselves be linguistic meaning

**Status:** `SUPPORTED_PRIOR_WORK / HUMAN_SCOPE`

Typological work on evidentiality shows that some languages grammaticalize source-of-information distinctions that others express differently or optionally.

**Project consequence:** provenance is not only audit metadata. A faithful mediator may need to conserve observed/reported/inferred distinctions as semantic content.

## C050 — Strong human structural universals should not be assumed without explicit burden

**Status:** `SUPPORTED_LIMITED_SCOPE / CONTESTED_THEORETICAL_INTERPRETATION`

Evans & Levinson (2009) synthesize typological evidence to argue for deep structural diversity and against simplistic strong universals. The theoretical debate is not closed.

**Project consequence:** noun/verb, subject, word order, tense, recursion, or other familiar categories may be human-language controls or candidate structures but not generic bootstrap primitives by default.

## C051 — Literal self-description from zero shared semantics is circular unless prerequisite distinctions are independently grounded

**Status:** `PROJECT_HYPOTHESIS / LOGICAL_CHALLENGE`

A protocol cannot rely on an instruction like `this signal means repeat` if `this`, `signal`, `means`, and `repeat` are themselves ungrounded.

**Project consequence:** test the staged hypothesis `self-demonstrating -> convention-forming -> recursively self-describing` instead of treating self-description as the initial primitive.

## C052 — Discovery and invention are separate semantic achievements

**Status:** `DESIGN_REQUIREMENT`

A system may create a useful convention without recovering a counterpart's pre-existing semantic practice.

**Project consequence:** bridge provenance must distinguish `DISCOVERED_CORRESPONDENCE`, `NEGOTIATED_CONVENTION`, `MIXED_OR_ADAPTED_CONVENTION`, `INFERRED_EQUIVALENCE`, and `EVALUATOR_DEFINED_RELATION`.

## C053 — A shared physical world does not guarantee an identifiable shared semantic distinction

**Status:** `PROJECT_BOUNDARY / INFERENCE`

If two candidate mappings induce the same learner-observable interaction distribution under every mutually available intervention, no bootstrap restricted to that surface can identify which mapping is true.

**Project consequence:** add R0.5 interaction-identifiability/common-ground auditing and permit `UNDERDETERMINED_IN_SCOPE` before semantic qualification.

## C054 — Human-language evidence is a graded control family, not proof of the full target

**Status:** `DESIGN_REQUIREMENT / PROJECT_BOUNDARY`

Human communication experiments begin with large shared biological, perceptual, developmental, social, and cultural priors.

**Project consequence:** every human-derived mechanism must be retested as those shared priors are removed in later signed/nonverbal, nonhuman, asymmetric, synthetic-alien, and from-scratch conditions.

## Open research gaps to investigate next

1. Formal literature on signalhood/intention detection without labeled communication channels.
2. Active-learning methods optimized for semantic hypothesis discrimination.
3. Semiotic models that do not assume discrete symbols.
4. Cross-modal semantic equivalence metrics.
5. Formal methods for detecting ontology mismatch.
6. Self-describing file/protocol formats and bootstrapping under unknown instruction sets.
7. Robust physical-layer/framing inference for interstellar channels.
8. Information-theoretic measures that preserve semantic distinctions rather than only mutual information.
9. Independent receiver architectures for contamination-resistant bootstrap tests.
10. Governance literature for METI and autonomous-contact systems.
11. Formal conditions under which cross-task transfer should be expected from a grounded convention.
12. Methods for constructing adversarial world generators that do not reveal evaluator ontology.
13. Lower bounds on the intervention set needed to distinguish competing semantic hypotheses.
14. Complexity measures that fairly compare symbolic, denotational, and predictive substrates.
15. Whether repair-like function can be discovered without assuming discrete turns or agent boundaries.
16. Human signed-language and homesign evidence for which structures survive removal of speech.
17. How nonhuman systems challenge the human-derived distinction between reference, function, and intention.
18. Formal identifiability results for semantic mappings under asymmetric observation/intervention surfaces.
19. Methods for separating pretrained human semantic priors from in-session grounding evidence.
20. Whether third-party acquisition is necessary, merely useful, or sometimes inappropriate for genuinely grounded conventions.

## Promotion rule

No `PROJECT_HYPOTHESIS` should be relabeled as supported UNVTRSLR capability without:

- exact experiment/version provenance;
- preregistered acceptance criteria;
- negative controls;
- simpler rivals;
- contamination/leakage audit;
- uncertainty and failure reporting;
- independent reproduction where practical.
