# Control Suite

## Purpose

The control suite is designed to test UNVTRSLR against communication systems whose semantics are at least partially known to the evaluator while progressively removing assumptions that make ordinary translation easy.

Controls are not training truth unless a specific experiment says so.

## Control class 1 — Human natural languages

Use natural languages as **positive controls** because humans already know substantial translation relationships among them.

The test should withhold dictionaries and parallel text from the participating agents while retaining evaluator access to known translations.

### Selection criteria

Choose languages that differ along multiple dimensions:

- word order;
- morphology;
- grammatical gender/classification;
- tense/aspect systems;
- evidentiality;
- pronoun systems;
- spatial encoding;
- lexicalization patterns;
- cultural categories;
- resource level.

Candidate sets should include languages from unrelated families rather than only closely related Indo-European pairs.

Uniform Meaning Representation research is useful here because UMR explicitly targets commonalities and variations across diverse languages, including Arapaho, Chinese, English, Kukama, Navajo, and Sanapaná in its first released multilingual dataset.

### Evaluation

Measure:

- recovered referential mappings;
- recovered predicate/argument structure;
- temporal/modality preservation;
- one-to-many and many-to-one mappings;
- untranslatable or paraphrase-required distinctions;
- conservation ledger accuracy.

## Control class 2 — Signed and spatial human language

Include at least one signed-language or sign-inspired control.

Purpose:

- break the assumption that language is acoustic/textual;
- test spatial grammar;
- test simultaneity versus sequential tokenization;
- test embodiment and viewpoint effects.

Do not flatten signed communication into English glosses before it reaches the learner, because that would remove the modality challenge.

## Control class 3 — Natural Semantic Metalanguage as a hypothesis baseline

Natural Semantic Metalanguage (NSM) research proposes a stable set of 65 semantic primes shared across human languages, along with combinatorial properties.

UNVTRSLR should treat these as:

- a strong human-language hypothesis;
- a useful benchmark for semantic recovery;
- a source of candidate low-complexity human concepts;

but **not** as proof of universal concepts across nonhuman or extraterrestrial intelligence.

Experiments can ask:

- which NSM primes are independently recoverable from grounded interaction?
- which require specifically human social/cognitive assumptions?
- do agents invent different decompositions that support the same behavior?

## Control class 4 — Synthetic languages with exact evaluator truth

Generate languages whose semantics and grammar are entirely known to the evaluator.

Vary:

- compositionality;
- word order;
- morphology;
- synonymy;
- polysemy;
- context dependence;
- irregularity;
- optional information;
- semantic underspecification.

Synthetic languages provide the cleanest test of whether a system reconstructs meaning rather than matching familiar human-language statistics.

### Required variants

1. Fully compositional language.
2. Partially compositional language.
3. Holistic codebook language.
4. Context-sensitive language.
5. Language with deliberately non-English category boundaries.
6. Language with lossy source-to-target mapping.
7. Language with concepts absent from target inventory.

## Control class 5 — Private-code traps

Create agents that can solve a referential task with arbitrary IDs or positional shortcuts.

These controls should obtain high task reward while failing semantic-transfer tests.

The evaluator must reject them as semantic success.

This addresses a known emergent-communication problem: successful agents can align representations and coordinate without learning evaluator-recognizable conceptual structure.

## Control class 6 — Honeybee-inspired vector communication

Use a synthetic channel inspired by the honeybee waggle dance.

Example mapping:

- orientation -> direction;
- duration -> distance;
- repetition/precision -> reliability or audience-dependent effects.

Do not tell the learner which dimensions are semantically relevant.

Test whether it can discover:

- that the behavior is communicative;
- which dimensions carry information;
- what environmental variables they map to;
- that signal precision can itself vary with social context.

The point is not to claim the synthetic agent is a bee. The point is to test continuous embodied encoding.

## Control class 7 — Context-dependent alarm communication

Use a synthetic system inspired by vervet-monkey alarm research.

Create signal forms whose meaning depends on environmental/social context.

The same signal may correspond to different receiver-relevant interpretations under different contextual conditions.

A one-to-one dictionary learner should fail.

Measure whether UNVTRSLR learns a conditional semantic mapping and preserves context dependence in translation.

## Control class 8 — Whale-like sequence modeling

Use synthetic acoustic sequence systems inspired by sperm-whale coda research.

Separate tasks carefully:

- acoustic structure prediction;
- individual/social-unit classification;
- turn-taking prediction;
- contextual association;
- demonstrated semantic mapping.

A system that predicts plausible vocal sequences has not thereby translated them.

Project CETI and its WhAM work are useful related research, but semantic qualification requires behavioral/contextual evidence beyond acoustic generation.

## Control class 9 — Continuous arbitrary channels

Construct communication systems where meanings are encoded in:

- frequency;
- amplitude;
- duration;
- phase-like relationships;
- trajectories;
- acceleration;
- orientation;
- timing intervals;
- combinations of continuous dimensions.

This prevents the architecture from treating discrete tokenization as universal.

## Control class 10 — Environmental modification

Do not provide a dedicated communication channel.

Agents communicate only by modifying shared space:

- object placement;
- path construction;
- resource arrangement;
- temporary marks;
- repeated motion traces.

The system must infer when action functions as signal rather than merely as world manipulation.

## Control class 11 — Asymmetric sensors

Use the same latent world with different sensory projections.

Examples:

- RGB vs depth;
- optical flow vs object detections;
- acoustic spectrum vs event labels;
- allocentric vs egocentric space;
- coarse temporal/high spatial vs high temporal/coarse spatial.

The evaluator must ensure there is no hidden common latent vector available to both agents.

## Control class 12 — Different ontology partitions

Give the agents intentionally different category boundaries.

Examples:

- continuous color vs categorical color;
- two source states collapsed into one target state;
- different object segmentation;
- relation-first vs object-first representation;
- one side has a sensory feature unavailable to the other.

Success includes identifying partial or absent equivalence.

## Control class 13 — Unknown communication channel

Provide many observable behaviors, only some of which carry communicative information.

The learner does not receive a `message` field.

Evaluate signalhood discovery independently from semantic decoding.

## Control class 14 — No communication control

Include worlds where no communicative behavior exists.

UNVTRSLR should conclude that there is insufficient evidence for signalhood.

If it invents a language anyway, the signalhood detector is overfitting.

## Control class 15 — Deceptive or unreliable communicator

The counterpart sometimes emits:

- false signals;
- accidental signals;
- stale conventions;
- strategic deception;
- inconsistent mappings.

The translator should preserve provenance and learn reliability conditional on context rather than converting received signals into truth.

## Control class 16 — Semantic drift

Change a convention after it has been established.

Measure:

- drift detection;
- confidence reduction;
- repair negotiation;
- convention versioning;
- whether old and new mappings are contextually separated.

## Control class 17 — Shared-language leakage controls

Deliberately insert prohibited shortcuts to verify the evaluator catches them:

- shared class IDs;
- shared object IDs;
- identical embeddings;
- synchronized private indices;
- hidden natural-language metadata;
- evaluator truth copied into learner state.

The qualification harness is not trustworthy unless these controls are detected or explicitly excluded.

## Control class 18 — Human zero-shared-language interaction

Later-stage human experiments can test whether the protocol helps people construct communication under channel restrictions.

Possible restrictions:

- no speech;
- no writing;
- novel arbitrary signal interface;
- shared manipulable environment;
- limited feedback;
- asymmetric observations.

These experiments require ethical review and should follow, not precede, synthetic validation.

## Control class 19 — “Alien” synthetic agents

Construct agents whose internal representations are intentionally unlike common human semantics.

Examples:

- no persistent object identity;
- field/flow-centered world model;
- radically different time discretization;
- high-dimensional sensory categories;
- goal structures unlike human reward tasks;
- communication optimized around state transitions rather than referents.

The objective is not to model actual aliens. It is to attack anthropocentric assumptions.

## Control class 20 — Self-describing bootstrap control

Give a receiver an unknown protocol whose first task is to explain enough of its own framing and semantics to support later interpretation.

Compare:

- predeclared framing;
- partially self-describing framing;
- fully opaque stream with repeated curriculum structure.

This is the closest terrestrial control for the broadcast form of interstellar UNVTRSLR.

## Required reporting

Every control run should record:

- what information each agent had;
- what they did not share;
- sensory interfaces;
- action interfaces;
- channel definition or absence of one;
- evaluator-only truth;
- semantic challenges attempted;
- calibration;
- conservation ledger;
- negative-control performance;
- alternative shortcut explanations.

Without that disclosure, cross-experiment “universality” comparisons are meaningless.

---

## Human verbal-language Pass 1 control overlays

These overlays apply to human spoken/verbal controls and to synthetic controls motivated by them. They do not replace the later signed/nonverbal or nonhuman passes.

### HVC-1 — typological/semantic distance matrix

Human-language positive controls should not be dominated by closely related high-resource languages.

Select pairs or small sets that vary materially in:

- morphology and word order;
- obligatoriness of tense/aspect/modal marking;
- evidential/source-of-information marking;
- spatial frame systems;
- pronoun/participant distinctions;
- lexical category boundaries;
- polysemy and lexicalization patterns;
- resource level and pretraining exposure.

Report what distinctions are obligatorily encoded, optionally encoded, lexicalized differently, or absent as one-to-one lexical equivalents.

**Failure caught:** English-centric translation success presented as general semantic mediation.

### HVC-2 — discovery versus convention-invention split

Run two materially different human conditions:

1. **pre-existing-language recovery:** agents encounter a convention that existed before the experiment and must infer its use without a dictionary;
2. **novel-convention formation:** participants are allowed to invent a new code during the experiment.

The resulting bridge entries must preserve `DISCOVERED_CORRESPONDENCE` versus `NEGOTIATED_CONVENTION` provenance.

**Failure caught:** a system that invents an effective task code being reported as having decoded a language.

### HVC-3 — iconicity ladder

For matched semantic challenges compare:

- high human-perceived iconicity;
- low/moderate iconicity;
- intentionally arbitrary mappings;
- misleading iconic cues that correlate with a nuisance variable rather than the target distinction.

**Failure caught:** a system that relies on human-motivated resemblance while being credited with arbitrary zero-shared-symbol grounding.

### HVC-4 — repair availability matrix

Compare:

- natural repair available;
- repair channel available but unlabeled;
- repair disabled;
- repair delayed;
- repair corrupted/noisy;
- evaluator-tagged `REPAIR` events as a deliberately invalid leakage condition.

Measure not only task success but interactions-to-stable-mapping, calibration, error recovery, and whether conventions remain transferable.

**Failure caught:** repair semantics smuggled through the interface instead of inferred from interaction.

### HVC-5 — joint-attention subsidy controls

Human experiments must declare whether they provide:

- shared gaze target;
- pointing;
- highlighted referent;
- shared scene segmentation;
- experimenter-directed salience;
- synchronized object IDs;
- common display coordinates.

Run matched conditions where at least some of these are removed or made asymmetric.

**Failure caught:** the experimenter performing the referential grounding while the learner receives credit.

### HVC-6 — task/pragmatics scaffold audit

Audit instructions, UI, feedback, timing, and task rules for semantic information.

Deliberately construct a control where a participant can infer the intended meaning primarily from:

- task objective;
- allowed action set;
- reward structure;
- menu position;
- turn timing;
- tutorial examples;
- experimenter behavior.

The semantic evaluator should detect that the scaffold, not the counterpart signal, carries the decisive information.

### HVC-7 — pretrained human-prior matrix

For model-based agents distinguish:

- scratch/scratch;
- pretrained/scratch;
- scratch/pretrained;
- pretrained/pretrained;
- materially different pretrained model families;
- synthetic semantic categories absent from public corpora.

Where possible record training-provenance overlap with the human languages or cultural facts used in the control.

**Failure caught:** recovery from memorized linguistic/world priors being reported as bootstrap from the current shared environment.

### HVC-8 — semantic partition mismatch

Use human-language-inspired worlds where source and target category boundaries differ.

Examples should include:

- one source term spanning several target terms;
- several source terms collapsing into one target category;
- a grammatically obligatory information-source distinction on one side but not the other;
- context-dependent lexicalization where a direct dictionary is misleading.

Success requires preservation of partial overlap, paraphrase, uncertainty, or scoped non-equivalence rather than forced one-to-one mapping.

### HVC-9 — third-party acquisition

After a dyad stabilizes a convention, introduce an independently initialized third participant that did not share the dyad's training history.

The third participant may learn from the permitted environment and interaction but receives no hidden codebook.

**Failure caught:** co-trained private coordination that cannot be reconstructed from grounded interaction.

Third-party acquisition is strong anti-shortcut evidence, not by itself proof of uniquely correct semantics.

### HVC-10 — identifiability null

Construct at least one case where the evaluator knows two latent distinctions but the agents' allowed observations/interventions make them exactly indistinguishable.

The expected system result is `UNDERDETERMINED_IN_SCOPE` or `UNIDENTIFIABLE_WITHIN_INTERACTION_SURFACE`, not a forced semantic answer.

**Failure caught:** evaluator truth being laundered into a claim that the learner discovered an empirically inaccessible distinction.

### HVC-11 — turn-structure ablation

Compare ordinary turn-like interaction against continuous, overlapping, asynchronous, or delayed signaling variants.

**Failure caught:** treating human conversational turn-taking as an undeclared universal framing layer.

### HVC-12 — self-description staging

Replace Control 20's binary notion of self-description with a staged comparison:

1. `SELF_DEMONSTRATING_ONLY` — repeated structure/contrast without meta-language;
2. `CONVENTION_FORMING` — negotiated mappings and repair can emerge;
3. `RECURSIVELY_SELF_DESCRIBING` — the system attempts to communicate about its own forms/uncertainty after prior grounding;
4. `PREDECLARED_META_LANGUAGE` — invalid/easier comparator in which meta-semantic functions are supplied.

**Failure caught:** circular claims that a zero-semantics protocol explained itself using concepts that were already presupposed.

## Human verbal control reporting additions

In addition to the general required reporting, record:

- whether the target behavior was pre-existing or negotiated during the experiment;
- joint-attention/ostension support available;
- repair affordances and whether they were labeled;
- iconicity condition;
- pretrained language/world priors;
- experiment/task instructions visible to each side;
- category/ontology partitions supplied by the interface;
- whether the tested distinction was identifiable from learner-visible evidence at all;
- whether a third party could reconstruct the convention;
- whether success depended on specifically human perceptual/pragmatic common ground.
