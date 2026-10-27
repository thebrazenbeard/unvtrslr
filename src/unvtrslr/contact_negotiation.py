"""Interactive two-feature contact experiment over untrusted continuous signals.

No shared words, target labels, semantic dictionary or partner's rule are given
to the learner. The sensor axes, intervention actions and scalar feedback are
experimenter-provided affordances; this is NOT universal autonomous contact.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from math import isfinite
from typing import Protocol

from .signal_discovery import fingerprint, recognize

CEILING = "SYNTHETIC_INTERACTIVE_OPERATIONAL_CONVENTION_ONLY"
SCENES = ((-.6,-.6),(.6,-.6),(-.6,.6),(.6,.6))

class PartnerPort(Protocol):
    """Device adapter must report observations, not evaluator semantic labels."""
    def observe(self, scene: tuple[float,float]) -> tuple[tuple[float,...],...]: ...
    def offer(self, scene: tuple[float,float], signal: tuple[tuple[float,...],...]) -> None: ...
    def outcome(self, scene: tuple[float,float], signal: tuple[tuple[float,...],...]) -> float: ...

@dataclass(frozen=True)
class ContactResult:
    status: str
    selected_sensor_axis: int | None
    observed_motifs: int
    training_interactions: int
    proposed_signals: int
    heldout_success: float | None
    withheld_contexts: int
    outbound_motifs: tuple[int,int] | None = None
    claim_ceiling: str = CEILING
    intent_inferred: bool = False
    universal_semantics: bool = False
    actual_unknown_intelligence_contacted: bool = False

def _sign(scene: tuple[float,float],axis: int) -> int:
    return int(scene[axis] > 0)

def _validate_scene(scene):
    if (type(scene) is not tuple or len(scene)!=2
            or any(type(v) not in (int,float) or not isfinite(v)
                   or not -1<=v<=1 for v in scene)):
        raise ValueError("invalid sensor-side scene")

def _signature(raw):
    # Observe raw 2-channel time series; refuse missing/multiple-event recordings.
    signature=fingerprint(raw)
    if signature is None or len(signature)!=2:
        return None
    return signature

def _fit_relation(observations):
    if len(observations)<12:
        return None
    eligible=[]
    for axis in (0,1):
        groups=defaultdict(list)
        for scene,motif in observations:
            groups[_sign(scene,axis)].append(motif)
        if not all(len(groups[state])>=6 for state in (0,1)):
            continue
        winners={}
        mistakes=0
        for state in (0,1):
            counter=Counter(groups[state])
            winner=counter.most_common(1)[0][0]
            winners[state]=winner
            mistakes += len(groups[state])-counter[winner]
        if winners[0]!=winners[1] and mistakes==0:
            eligible.append((axis,winners))
    return eligible[0] if len(eligible)==1 else None

def _outbound_symbol(label:int) -> tuple[tuple[float,...],...]:
    """A learner-proposed *arbitrary* waveform: no claim of shared encoding."""
    if type(label) is not int or label not in (0,1):
        raise ValueError("unsupported proposed symbol")
    result=[]
    for position in range(64):
        value = -.85 if 11<=position<18 else 0.0
        result.append((value if label==0 else 0.0,
                       value if label==1 else 0.0))
    return tuple(result)

def _next_scene(history):
    """Choose a counterfactual intervention online, based on coverage and past."""
    counts=Counter(scene for scene,_ in history)
    last=history[-1][0] if history else None
    # Prefer underexplored sensor interventions; ensure balanced full factorial
    # rather than assuming one axis matters a priori.
    return min(SCENES,key=lambda scene:(
        counts[scene],sum(int(x==y) for x,y in zip(scene,last)) if last else 0,
        SCENES.index(scene)))

def negotiate(port: PartnerPort, *, max_observations:int=24) -> ContactResult:
    if type(max_observations) is not int or not 12<=max_observations<=48:
        raise ValueError("invalid interaction budget")
    prototypes=[]
    history=[]
    # No gold sender rule or expected messages supplied.
    relation=None
    for _ in range(max_observations):
        scene=_next_scene(history)
        _validate_scene(scene)
        signature=_signature(port.observe(scene))
        if signature is None:
            return ContactResult("NO_DECODABLE_CANDIDATE",None,len(prototypes),
                                 len(history)+1,0,None,0)
        label=recognize(signature,prototypes)
        if label is None:
            if len(prototypes)>=4:
                return ContactResult("UNSTABLE_CHANNEL",None,len(prototypes),
                                     len(history)+1,0,None,0)
            label=len(prototypes)
            prototypes.append(signature)
        history.append((scene,label))
        relation=_fit_relation(history)
        if relation is not None:
            break
    if relation is None:
        return ContactResult("NO_IDENTIFIABLE_SENSOR_RELATION",None,
                             len(prototypes),len(history),0,None,0)
    axis,mapping=relation
    if len(prototypes)!=2:
        return ContactResult("UNSTABLE_CHANNEL",None,len(prototypes),
                             len(history),0,None,0)
    # New, arbitrary outbound codebook. The actor is not given the partner's
    # internal map and does not transmit explicit semantic class labels.
    reverse={motif:state for state,motif in mapping.items()}
    if len(reverse)!=2:
        return ContactResult("AMBIGUOUS_SENSOR_RELATION",None,len(prototypes),
                             len(history),0,None,0)
    proposed=0
    confirmed=False
    # A response can refuse an initially proposed code. Use measured training
    # outcomes (not an assumed ACK token), offer it again, and retest before
    # touching novel holdout contexts. Bounded to two negotiation attempts.
    for _attempt in range(2):
        for scene in SCENES * 3:
            chosen=mapping[_sign(scene,axis)]
            port.offer(scene,_outbound_symbol(chosen))
            proposed+=1
        confirmations=[]
        for scene in SCENES:
            chosen=mapping[_sign(scene,axis)]
            feedback=port.outcome(scene,_outbound_symbol(chosen))
            if type(feedback) not in (int,float) or not isfinite(feedback) or not 0<=feedback<=1:
                raise ValueError("invalid external coordination observation")
            control=port.outcome(scene,_outbound_symbol(1-chosen))
            if type(control) not in (int,float) or not isfinite(control) or not 0<=control<=1:
                raise ValueError("invalid counterfactual coordination observation")
            confirmations.append((float(feedback),float(control)))
        if all(value>=.75 and value-control>=.5 for value,control in confirmations):
            confirmed=True
            break
    if not confirmed:
        return ContactResult("PROPOSAL_NOT_CONFIRMED",axis,len(prototypes),
                             len(history),proposed,None,0)
    # Freeze the learned operational codebook. Withheld situations, feedback,
    # and pass/fail thresholds belong exclusively to an evaluator, not here.
    return ContactResult("PROPOSAL_CONFIRMED_TRAINING_ONLY",
                         axis,len(prototypes),len(history),proposed,None,0,
                         outbound_motifs=(mapping[0],mapping[1]))
