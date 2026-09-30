# Research Landscape

UNVTRSLR sits at the intersection of several existing research traditions. None is sufficient by itself, but each contributes an important piece.

## 1. Symbol grounding

Stevan Harnad's 1990 “The Symbol Grounding Problem” asks how symbols can acquire meaning that is not merely parasitic on another interpreter's meanings. Harnad argues that symbolic representations ultimately require grounding in nonsymbolic representations, including iconic/perceptual and categorical representations.

**Contribution to UNVTRSLR:** formal semantic structures cannot be treated as meaningful merely because they are internally consistent. Grounding must connect them to perception, action, or other nonsymbolic evidence.

**UNVTRSLR extension:** grounding must be negotiated across systems that may not share perceptual categories.

## 2. Grounded language games and symbol emergence

Luc Steels, Paul Vogt, and related researchers demonstrated that robots or simulated agents can develop shared lexicons and primitive compositional structures through repeated situated language games.

Vogt's work on perceptually grounded language games shows conditions under which semantics and compositional structure can emerge, and Steels' robot experiments emphasize shared environments and social interaction.

**Contribution:** shared context plus feedback can bootstrap conventions without a centrally designed lexicon.

**UNVTRSLR extension:** remove the assumptions that the channel is verbal, that message boundaries are known, and that both parties share similar perceptual organization.

## 3. Emergent communication and referential games

Modern multi-agent emergent-communication research often uses Lewis-style sender/receiver games. Agents develop signaling systems that help solve cooperative tasks.

A major warning comes from Bouchacourt & Baroni (2018): agents can communicate successfully while their aligned visual representations fail to capture the conceptual properties humans assume the symbols denote.

Mu & Goodman (2021) similarly argue that simple single-object referential games encourage uninterpretable task-bound codes; games requiring generalizations improve systematicity and interpretability.

Chaabouni et al. (2020) show that compositionality and generalization are not trivially identical and require careful measurement.

**Contribution:** communication can emerge computationally.

**Warning:** task success is not semantic proof.

**UNVTRSLR requirement:** transfer, role reversal where applicable, intervention or other discriminating histories, semantic minimal pairs, and independent conservation evaluation.

## 4. Coordination, conventions, and experimental semiotics

David Lewis' signaling-game framework treats conventions as solutions to recurring coordination problems. Human experimental-semiotics work shows that people can establish flexible conventions through unfamiliar restricted channels when enough common ground and feedback are available.

Human conversation research adds two important constraints: cross-situational learning can reduce ambiguity over repeated contexts, and repair can expose misunderstanding before a rich lexicon is available. Human turn-taking is highly structured across languages but varies enough that it should be treated as evidence rather than universal framing.

**Contribution:** communication conventions can arise without a fixed prior code, and early interaction management can accelerate grounding.

**Boundary:** these results rely on substantial shared human biology, cognition, pragmatics, task understanding, and perceptual common ground.

**UNVTRSLR extension:** distinguish discovery of a pre-existing convention from invention of a new one, and remove human-specific scaffolds progressively.

## 5. Natural Semantic Metalanguage (NSM)

NSM research by Anna Wierzbicka, Cliff Goddard, and colleagues proposes a small set of cross-linguistically universal semantic primes. The contemporary program identifies 65 primes and argues that their combinatorial grammar provides a human semantic metalanguage.

**Contribution:** decades of cross-linguistic work provide a serious empirical hypothesis about semantic structures shared across human languages.

**Boundary:** this is evidence about humans, not proof of universal concepts for animals, AI systems, or extraterrestrial intelligence.

**UNVTRSLR use:** positive-control benchmark and source of candidate human semantic challenges, never hard-coded alien ontology.

## 6. Abstract and Uniform Meaning Representation

Abstract Meaning Representation (AMR) and newer Uniform Meaning Representation (UMR) seek language-independent or cross-lingual graph representations of meaning.

The 2024 UMR release explicitly represents sentence-level predicate/argument structure plus document-level coreference, temporal, and modal relationships, and was released across six typologically diverse languages.

**Contribution:** practical evidence that semantic representation benefits from explicit events, roles, modality, time, and document-level relations.

**Boundary:** UMR is still a linguistic formalism whose categories are designed around human-language semantics.

**UNVTRSLR use:** architectural inspiration and human-language control, not universal substrate canon.

## 7. Signed languages, homesign, gesture, and modality independence

Human signed languages are full natural languages with phonological, morphological, syntactic, discourse, and pragmatic structure. Their visual-spatial modality shows that language cannot be equated with speech, sound, or a one-dimensional token stream.

Homesign and emerging-sign research is especially important because it shows that structured communicative systems can develop under reduced access to an established conventional language, while community scale, interaction history, and transmission materially affect the resulting system.

Gesture research shows that pointing, gaze, hand movement, facial action, and body orientation can be linguistically integrated, pragmatically meaningful, affective, indexical, or incidental depending on context.

**Contribution:** destroys speech/text as universal ingress assumptions and supports simultaneous/spatial composition, negotiated convention, and functionally ambiguous observable behavior.

**Boundary:** human visual attention, embodiment, social cognition, and cultural interaction remain large shared priors.

## 8. Nonhuman vocal communication

### Vervet alarm calls

Classic playback work shows different alarm-call classes can elicit predator-appropriate receiver behavior in the predator's absence. Later quantitative work complicates any simple `one call = one predator word` interpretation.

**Contribution:** playback can support receiver-relevant external information more strongly than corpus correlation.

**Boundary:** functional/reference-like alarm evidence is not a general animal lexicon or human word system.

### Campbell's monkeys and Japanese great tits

Call-combination work provides bounded evidence that component order or modification can predictably affect receiver behavior.

**Contribution:** nonhuman communication can exhibit combination effects worth testing compositionally.

**Boundary:** distributional sequence structure, human-like syntax, and compositional semantics must remain separate evidence levels.

### Marmosets

Marmosets show extended antiphonal vocal exchange and overlap avoidance. Later modeling work challenged an earlier coupled-oscillator mechanism while preserving the behavioral regularity.

**Contribution:** observed interaction structure and explanatory mechanism must be stored separately.

### Dolphins, parrots, and elephants

Dolphin signature-whistle playback, parrot receiver-directed vocal imitation, and elephant receiver-specific name-like calls provide different mechanisms for individual addressing.

**Contribution:** individual identity/addressing can be communicated through multiple mechanisms.

**Boundary:** `name` is an analogy and cannot be the universal semantic primitive inferred from all identity-bearing signals.

### Sperm whales

Sperm-whale coda research demonstrates rich contextual, social, cultural, and combinatorial acoustic structure. The 2024 Nature Communications study explicitly distinguishes that structural result from established semantics.

**Contribution:** strong contemporary example of why acoustic tokenization, prediction, clustering, embeddings, and synthesis must remain below semantic qualification.

**Boundary:** rich structure is not a translated whale language.

### Bats and information-rich corpora

Large bat vocal corpora contain classifier-readable information about caller, addressee, context, and behavior.

**Contribution:** statistical information can identify useful hypotheses.

**Boundary:** classifier decodability does not establish receiver meaning or signaller intention.

## 9. Nonhuman non-vocal communication

### Honeybee waggle dance

Honeybees communicate resource vectors through dance geometry and timing. Crucially, the distance-related quantity is shaped by optic-flow odometry rather than simply matching an evaluator's observer-independent meters.

**Contribution:** continuous embodied communication can carry displaced spatial information.

**Major lesson:** a shared physical world does not imply a shared physical-variable representation. Evaluator distance, sender perceptual distance, and receiver navigational quantity may be different objects that require a learned transform.

### Great-ape gesture

Great ape gesture shows audience monitoring, response waiting, persistence, elaboration, and recipient-attention sensitivity.

**Contribution:** some of the strongest operational evidence for flexible intentional signaling outside humans.

**Boundary:** intentionality can strengthen signalhood/function evidence where supported but cannot be a universal prerequisite for communication.

### Cephalopod visual/body patterning

The same body-pattern machinery participates in camouflage, defense, courtship, agonistic display, and communication.

**Contribution:** signalhood must be a contextual hypothesis over form, audience, history, and response rather than a permanent property of a pattern.

### Chemical and persistent signaling

Ant pheromone trails are deposited, reinforced, diffused, decayed, and sampled by later individuals. A trace can be collectively authored and persist after the original producer has left.

**Contribution:** communication need not be synchronous, dyadic, or segmented into discrete message events.

### Electrical communication

Weakly electric fish use electric organ discharges for both electrolocation and social communication.

**Contribution:** the physical substrate used for sensing the environment and communicating may overlap. `sensor stream` and `communication channel` cannot be universally disjoint components.

### Substrate-borne, polarization, and other modalities

Comparative communication research includes vibrational, tactile, polarization-sensitive, electric, and chemical channels that ordinary human interfaces may not expose.

**Contribution:** channel discovery is logically prior to semantic decoding; a translator can fail before semantics if it cannot sense the communication substrate.

## 10. Interstellar message design

### Pioneer/Voyager

The Pioneer plaques and Voyager Golden Record demonstrate the challenge of creating self-explanatory physical artifacts. Voyager uses symbolic playback instructions, binary arithmetic, astronomical/physical references, images, natural sounds, music, and multilingual greetings.

### Lincos

Hans Freudenthal's 1960 Lincos is a designed language for cosmic communication. It proposes a progressively taught radio language beginning with mathematics and extending to richer discourse.

Freudenthal explicitly assumes a receiver sufficiently humanlike in mental state and experience.

**Contribution:** the idea of semantic curriculum and progressive bootstrapping is not new.

**UNVTRSLR extension:** infer signalhood, exploit shared observable structure where it exists, permit nonlinguistic channels, and explicitly attack humanlike cognitive assumptions.

### Exosemiotics

Vakoch and others have challenged both the optimistic assumption that mathematics/science will be straightforwardly shared and the pessimistic claim that communication is impossible. One proposed middle path is to simulate or present natural phenomena themselves, using iconic/shared physical structure as common ground.

**Contribution:** supports grounding through shared phenomena rather than arbitrary notation.

### Interstellar digital communications engineering

Messerschmitt & Morrison emphasize that transmitter and receiver cannot coordinate beforehand and recommend layered architecture for detectability, synchronization, channel impairments, reliability, and higher-level message structure.

**Contribution:** semantic bootstrapping must sit above a separately solved physical/framing layer — while the nonhuman pass warns that embodiment can sometimes blur sensing and communication at higher layers.

## 11. Self-describing messages and decoding

Interstellar-decoding work proposes first finding message dimensions and symbol structures, then inferring meanings from redundancy, relationships, functions, and shared physics patterns.

**Contribution:** a receiver may have to infer framing and symbol classes before semantics.

**UNVTRSLR extension:** literal self-description should not be treated as the first zero-semantics move. The current staged hypothesis is `self-demonstrating -> convention-forming -> recursively self-describing`.

## 12. Active learning, identifiability, and scientific inference

UNVTRSLR's active semantic-discovery loop is closely related to experimental design: choose an observation, playback, intervention, exposure, or interaction regime that best distinguishes competing hypotheses.

Information-gain-style selection is a natural baseline, although no one probabilistic formalism should be assumed mandatory.

The project now adds an earlier question: is the target distinction distinguishable through the actual learner-visible interaction surface at all?

**Contribution:** provides a principled way to ask “what evidence could separate these meanings?”

**Boundary:** identifiability is necessary but not sufficient for learner credit. A privileged adapter or mediator can make a distinction visible while already performing the semantic normalization the learner is later credited with discovering.

## 13. Multimodal grounding

Embodied AI and multimodal learning show that linguistic or symbolic representations can be tied to perception and sensorimotor interaction.

**Contribution:** meaning can be linked to action/perception rather than text alone.

**UNVTRSLR extension:** neither modality nor perceptual decomposition is assumed shared, and communication may be continuous, simultaneous, persistent, distributed, or fused with ordinary sensing.

## 14. Cross-pass synthesis: what survives progressive removal of human assumptions

The three evidence passes do not reveal one universal symbol inventory. They instead support a thinner set of architectural responsibilities:

1. discover candidate structure rather than assume messages;
2. retain multiple interpretations under ambiguity;
3. distinguish correlation from receiver/coupled-process evidence;
4. seek discriminating histories when available;
5. preserve provenance and evidence level;
6. distinguish discovered correspondence from negotiated convention;
7. permit different perceptual metrics and ontology partitions;
8. support continuous, spatial, simultaneous, persistent, multimodal, and distributed signaling;
9. test transfer/systematic reuse rather than task reward alone;
10. preserve partial/non-equivalence and honest failure.

The broadest current problem formulation is no longer necessarily `two agents exchanging messages`. A more general project hypothesis is:

> initially unaligned adaptive systems or coupled processes with partially overlapping observables and influence surfaces may under some conditions construct reusable, scoped cross-system correspondences.

The original two-agent shared-environment experiment remains the correct first controlled fixture because it is falsifiable and tractable.

## 15. What appears novel in the combined program

The individual components have substantial precedent. The potentially distinctive contribution is their combination under an unusually strict target:

1. no assumed linguistic channel;
2. signalhood/channel discovery;
3. shared-world but potentially asymmetric perception and metric structure;
4. interaction-identifiability audit before semantic promotion;
5. active or passive discriminating-history selection;
6. negotiated conventions separated from decoded pre-existing correspondences;
7. competing semantic substrates rather than one human-readable ontology;
8. provenance-aware semantic conservation and bridge attribution;
9. rewarded partial/non-equivalence detection;
10. human and nonhuman systems used as graded controls rather than universal truth;
11. adversarial protection against task codes, evaluator subsidy, and pretrained leakage;
12. self-describing interstellar bootstrap retained as a downstream falsification target rather than assumed capability.

This novelty claim is provisional. A formal literature review should continue to search for prior systems combining the same responsibilities.

## Research discipline

Related work should be classified as one of:

- `DIRECT_PRECURSOR` — solves substantially the same problem;
- `PARTIAL_PRECURSOR` — solves one required responsibility;
- `CONTROL_RESOURCE` — useful as evaluator ground truth or stress test;
- `ARCHITECTURAL_INSPIRATION` — suggests a representation or algorithm;
- `WARNING/COUNTEREXAMPLE` — demonstrates a false-success mode;
- `OPEN_COMPETITOR` — a simpler or stronger rival architecture.

The project should prefer discovering that a supposed novelty already exists over rebranding prior work.

Detailed cross-species evidence and claim ceilings are in `research/NONHUMAN_COMMUNICATION.md`, `research/NONHUMAN_CLAIMS.md`, `docs/NONHUMAN_CONTROL_OVERLAYS.md`, and `docs/NONHUMAN_FIRST100_REVIEW.md`.