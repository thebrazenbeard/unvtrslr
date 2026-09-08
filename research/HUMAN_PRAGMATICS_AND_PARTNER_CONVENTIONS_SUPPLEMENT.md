# Human Pragmatics and Partner-Specific Convention Supplement

Status: `POST_PASS_1_AUDIT / HUMAN_SCOPE_ONLY / PR4_REFINEMENT`

Bound integration subject before this refinement:

- repository: `thebrazenbeard/unvtrslr`
- branch: `research/integrate-human-nonhuman-evidence-v2-20260907`
- predecessor head: `bc9229c85d0848342d6abfb2f82edfc7c4d1691b`
- draft PR: `#4`

This supplement closes a gap in the original Human Verbal Pass: the pass covered ambiguity reduction, repair, convention emergence, iconicity, cultural transmission, typology, and provenance, but underweighted **collaborative reference, partner-specific conventions, common-ground modeling, and pragmatic inference**.

The evidence here remains human-language evidence. It does not establish species-neutral pragmatics or a universal theory-of-mind primitive.

## Evidence labels

- `SUPPORTED_PRIOR_WORK` — directly supported by cited empirical/review literature;
- `SUPPORTED_LIMITED_SCOPE` — supported in narrower human interaction paradigms;
- `PROJECT_HYPOTHESIS` — UNVTRSLR proposal motivated but not established by the literature;
- `INFERENCE` — project synthesis;
- `CHALLENGE` — false-success or overclaim risk;
- `UNKNOWN` — evidence does not settle the question.

## 1. Reference can be collaboratively constructed rather than decoded in one shot

Clark & Wilkes-Gibbs (1986) studied pairs referring to difficult figures and modeled definite reference as an iterative collaborative process: a speaker proposes a description and participants may repair, expand, replace, or accept it before moving on.

**Evidence class:** `SUPPORTED_PRIOR_WORK / HUMAN DYADIC CONVERSATION`.

**UNVTRSLR consequence:** a candidate reference mapping should be allowed to emerge through a sequence of proposals, responses, repairs, and acceptances rather than being scored only as `signal -> referent` on isolated trials.

**Claim ceiling:** the experiment begins with humans who already share a language, conversational norms, object segmentation, task goals, and strong social/pragmatic priors. It demonstrates collaborative stabilization of reference, not zero-shared-language grounding.

Reference: Clark, H. H. & Wilkes-Gibbs, D. (1986). *Referring as a collaborative process*. Cognition 22(1):1-39. DOI `10.1016/0010-0277(86)90010-7`.

## 2. Stable local meaning can be partner-specific

Brennan & Clark (1996) found that conversational partners repeatedly referring to the same objects tend to reuse partner-specific lexicalizations, motivating the notion of `conceptual pacts`. Hawkins, Frank & Goodman (2020) later quantified repeated reference games and found that different dyads converged on diverse, idiosyncratic, efficient, stable solutions.

**Evidence class:** `SUPPORTED_PRIOR_WORK / HUMAN DYADIC REFERENCE`.

**UNVTRSLR consequence:** the bridge needs a scope dimension for **which participants and interaction history** support a convention. A mapping can be stable and useful inside one pair without yet being a community-wide or species-wide semantic convention.

A bridge record should therefore distinguish at least:

- `PAIR_LOCAL_CONVENTION`;
- `PARTNER_TRANSFER_SUPPORTED`;
- `COMMUNITY_GENERALIZATION_SUPPORTED`;
- `PREEXISTING_POPULATION_CONVENTION`;
- `GENERALIZATION_UNKNOWN`.

This is provenance/scope, not an assertion that human lexical conventions are the universal form of meaning.

References:

- Brennan, S. E. & Clark, H. H. (1996). *Conceptual pacts and lexical choice in conversation*. Journal of Experimental Psychology: Learning, Memory, and Cognition 22(6):1482-1493. DOI `10.1037/0278-7393.22.6.1482`.
- Hawkins, R. D., Frank, M. C. & Goodman, N. D. (2020). *Characterizing the Dynamics of Learning in Repeated Reference Games*. Cognitive Science 44(6):e12845. DOI `10.1111/cogs.12845`.

## 3. Do not over-interpret lexical entrainment as proof of a shared concept

Bangerter, Mayor & Knutsen (2020) found lexical entrainment even in a modified matching task where participants received new cards on each trial and therefore could not build object-specific conceptual pacts in the classic sense. Their results suggest that lexical convergence can partly reflect broader shared interaction history, category learning, or a developing meta-perspective rather than a single partner-specific pact about one object.

**Evidence class:** `SUPPORTED_PRIOR_WORK / MECHANISM CHALLENGE`.

**UNVTRSLR consequence:** convergence on the same signal form is not semantic proof. The evaluator must still test what distinction the form tracks, what interventions preserve it, and whether a simpler interaction-history explanation accounts for the convergence.

**False-success control:** create pairs that converge strongly in form because of recency/frequency or task scaffolding while the signal fails world-factor intervention, cross-task transfer, or novel-instance tests.

Reference: Bangerter, A., Mayor, E. & Knutsen, D. (2020). *Lexical entrainment without conceptual pacts? Revisiting the matching task*. Journal of Memory and Language 114:104129. DOI `10.1016/j.jml.2020.104129`.

## 4. Common ground is a participant model, not privileged truth

Human pragmatics treats common ground as information participants treat as shared background for an interaction. A recent review by Rubio-Fernandez & Harris (2026) emphasizes the distinction and contact between formal and psycholinguistic traditions studying common ground.

But Keysar et al. (2000) showed that human listeners do not perfectly restrict interpretation to what is mutually known: eye movements revealed temporary consideration of referents the speaker could not see. Human comprehension can therefore use imperfect, partly egocentric heuristics and later correction.

**Evidence class:** `SUPPORTED_PRIOR_WORK / HUMAN PRAGMATICS`.

**UNVTRSLR consequence:** never implement `common_ground` as an evaluator-truth table exposed to the learner. At most, each participant may maintain uncertain models of what evidence or conventions are mutually available.

Required distinction:

- `WORLD_OR_EVALUATOR_TRUTH`;
- `A_OBSERVED`;
- `B_OBSERVED`;
- `A_BELIEVES_SHARED`;
- `B_BELIEVES_SHARED`;
- `MUTUALLY_TESTED_CONVENTION`;
- `SHAREDNESS_UNKNOWN_OR_DISPUTED`.

A false belief about what is shared must remain representable without being silently corrected by the evaluator.

References:

- Keysar, B., Barr, D. J., Balin, J. A. & Brauner, J. S. (2000). *Taking Perspective in Conversation: The Role of Mutual Knowledge in Comprehension*. Psychological Science 11(1):32-38. DOI `10.1111/1467-9280.00211`.
- Rubio-Fernandez, P. & Harris, D. W. (2026). *Common Ground: Between Formal Pragmatics and Psycholinguistics*. Annual Review of Linguistics 12:249-271. DOI `10.1146/annurev-linguistics-041824-032410`.

## 5. Pragmatic inference can resolve underspecified signals, but it imports strong human assumptions

Frank & Goodman (2012) showed that a simple probabilistic model in which a speaker attempts to be informative and a listener reasons about the speaker's likely intended referent closely predicted human judgments in referential language games.

**Evidence class:** `SUPPORTED_PRIOR_WORK / HUMAN PRAGMATIC INFERENCE`.

**What this supports:** semantic interpretation can depend on the set of alternatives, context, and expectations about the communicator, not just signal/world co-occurrence.

**Claim ceiling:** assumptions such as knowledgeable speakers, informative choice, intentional reference, cooperative goals, and approximately shared utility are powerful human/task priors. They cannot be hidden inside the universal bootstrap architecture.

**UNVTRSLR consequence:** pragmatic/social inference should be a **candidate model family** tested against weaker alternatives, not a mandatory semantic primitive. R1/R2 should include cases where the counterpart is noncooperative, mistaken, stochastic, deceptive, or simply not optimizing informativeness.

Reference: Frank, M. C. & Goodman, N. D. (2012). *Predicting pragmatic reasoning in language games*. Science 336(6084):998. DOI `10.1126/science.1218633`.

## 6. Partner-specificity changes how third-party acquisition should be interpreted

The existing R2 partner-swap test is valuable, but human evidence shows that local conventions and population conventions are different achievements.

**Project inference:** third-party acquisition should be decomposed rather than treated as one binary semantic gate.

Suggested evaluation states:

1. `LOCAL_BRIDGE_STABLE` — original pair can reuse/repair the distinction across held-out contexts;
2. `NEW_PARTNER_REGROUNDABLE` — a fresh partner can acquire it from allowed interaction without hidden codebook access;
3. `POPULATION_CONVENTION_GENERALIZES` — unfamiliar partners already interpret it with no pair-specific negotiation under the tested population condition;
4. `TRANSFER_REQUIRES_SHARED_PRIOR` — success disappears when human/pretrained population priors are removed;
5. `LOCAL_ONLY / GENERALIZATION_NOT_ESTABLISHED`.

Failure of immediate zero-shot partner transfer should not by itself erase evidence that a pair built a genuine local grounded convention. Conversely, easy transfer among humans may be explained by shared language/culture rather than by the bootstrap protocol.

**Evidence class:** `INFERENCE / DESIGN REFINEMENT`.

## 7. New false-success mode: dyadic semantic overfitting

A system can look semantically excellent by forming an efficient, stable pair-specific code that survives repeated trials while relying on interaction history or jointly learned shortcuts that do not correspond to the claimed external distinction.

Call this:

`DYADIC_SEMANTIC_OVERFIT`

Qualification pressure should include:

- novel objects/instances;
- changed distractor sets;
- changed task incentives;
- partner swap with re-grounding allowed;
- partner swap with no re-grounding for population-generalization claims;
- world-factor interventions;
- nuisance/history controls;
- tests that separate form convergence from stable denotation/function.

This complements, rather than replaces, the existing private-code and co-training controls.

## 8. Challenge to the self-describing-bootstrap thesis

Human reference research strengthens the staged formulation

`self-demonstrating -> convention-forming -> recursively self-describing`

but adds an important scope warning: the first recursive descriptions may themselves be **locally negotiated metalanguage**, not universal protocol semantics.

Therefore a protocol saying, in effect, `this form means repeat` has only achieved a scoped meta-convention until a new partner can reconstruct that convention from the permitted interaction surface or an independent evaluator can verify the claimed functional invariants.

**Evidence class:** `INFERENCE / CHALLENGE`.

## 9. Resulting architecture pressure

This supplement recommends no new universal semantic atom. It recommends stronger state/provenance separation:

- participant-specific evidence models;
- uncertain sharedness/common-ground hypotheses;
- convention scope by partner/community/history;
- separation of lexical/form convergence from denotational/functional evidence;
- explicit local-vs-transfer qualification;
- pragmatic reasoning as a tested optional model family.

This makes the bootstrap more realistic while reducing the temptation to smuggle human cooperative pragmatics into the generic interface.

## 10. Claim ceiling

Human pragmatics provides strong evidence that people collaboratively negotiate reference, form partner-specific conventions, use fallible common-ground models, and infer meaning from context and assumptions about speakers.

It does **not** establish that arbitrary agents:

- possess common-ground representations;
- model intentions;
- optimize informativeness;
- share cooperative utilities;
- distinguish speaker/listener roles;
- form partner-specific lexical pacts;
- or generalize local conventions to new partners.

Those remain hypotheses to test under progressively weaker shared priors.