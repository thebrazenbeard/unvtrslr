# R2 three-host causal convention acquisition: next experimental gate

Status: `PROPOSED / NOT EXECUTED / NO_GROUNDING_CLAIM`

Independent native ChatGPT architecture and hostile reviewers examined
`unvtrslr` main `dc083969333e42534f9b2451084484cd6319986f`
(tree `8ce5a19aecc5406cd512b755130197d29dcfc0bc`) on 2026-10-26.
Their review was internal model review, not independent laboratory evidence.
Individual reviewer model/runtime versions were not separately attested.
Lappy, VN1 and VN2 have **not** completed the experiment or independently
verified runtime isolation.

## Minimal falsifiable claim

Two initially non-coordinated learners acquire a bounded operational
convention through observations, messages, actions and scalar consequences.
Frozen conventions then cause receiver behavior in blind interventions and
generalize to novel stimuli. This is not a claim of universal translation.

## Host roles and information barriers

1. **Lappy, sealed evaluator:** own trial randomization, intervention plan,
   raw stimulus generation, independently frozen holdouts and correct answers.
   Never send factor labels, answer keys or trial IDs to either learner.
2. **VN1, sender learner:** receive only nuisance-varied raw observations,
   local state and bounded learning feedback; emit a bounded message.
3. **VN2, receiver learner:** receive the message and action affordances;
   choose an action before scalar consequences arrive. No true labels or
   privileged intended actions in its input.

Actual machine separation alone is insufficient. First attest model binary,
weights, prompts, code and environment; probe filesystem, network, shared
Bus/brokers, timing, caches, system variables and training contamination for
side channels. Block qualification until these surfaces are controlled.

## Preregistered evaluation

- Freeze both learner states and holdouts after bounded interactive learning.
- On matched receiver states, compare original, removed, shuffled and
  counterfactually substituted messages in randomized order.
- Test held-out nuisance conditions, novel feature combinations, new
  partners, third-party learning, role reversal and scoped abstention.
- Compare no-message, pre-agreed-codebook and task-specific private-code
  baselines. Publish effect sizes, uncertainty, leakage tests and failures.
- Reject grounding if performance survives message ablation, can be predicted
  from filenames/time/IDs, fails partner/composition transfer, or depends on
  distinctions already destroyed by preprocessing.

`r2_process_probe.py` remains a useful **synthetic negative control**: its
sender gets the evaluator's binary `factor`, its receiver gets an explicit
task, and even perfect scores correctly stay `COUNTERFACTUAL_UNQUALIFIED`.
POSIX process-group termination is best-effort; intentionally detached
children may escape, and Windows descendant containment remains unqualified.

Primary research: Lowe et al. (AAMAS 2019),
https://ifaamas.org/Proceedings/aamas2019/pdfs/p693.pdf (causal listening);
Chaabouni et al. (ACL 2020),
https://aclanthology.org/2020.acl-main.407/ (compositional generalization).

The first justified positive result would be a **causally effective learned
convention within this controlled task**, not a universal translator.
