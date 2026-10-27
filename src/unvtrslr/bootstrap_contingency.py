"""Bounded active-probe contingency screen over continuous response traces.

Experimenter supplies interventions, trace boundaries and matched settings.
Evidence of response contingency is NOT evidence of intentional communication,
learned semantics, identity, ontology, or protocol negotiation.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from math import isfinite
from statistics import median
from typing import Sequence

PROBES = ("sham", "probe_a", "probe_b")
CLAIM = "EXPERIMENTER_FRAMED_CONTINUOUS_RESPONSE_CONTINGENCY_ONLY"
MIN_BLOCKS_PER_SETTING = 6
MIN_EFFECT = 0.25
MAX_EARLY_EFFECT = 0.12
MIN_MARGIN = 0.18

@dataclass(frozen=True)
class RawProbeObservation:
    block: str
    setting: str
    probe: str
    order: int
    trace: tuple[float, ...]

@dataclass(frozen=True)
class ContingencyScreen:
    status: str
    selected_probe: str | None
    fitted_settings: tuple[str, ...]
    holdout_settings: tuple[str, ...]
    train_effects: tuple[tuple[str, float], ...]
    holdout_effects: tuple[tuple[str, float], ...]
    claim_ceiling: str = CLAIM
    os_isolation_verified: bool = False
    semantic_qualification: bool = False

def _validate(rows: Sequence[RawProbeObservation], name: str):
    if not isinstance(rows,(list,tuple)) or not 36 <= len(rows) <= 12000:
        raise ValueError(f"{name}: rows outside bounded range")
    if any(type(r) is not RawProbeObservation for r in rows):
        raise ValueError(f"{name}: wrong observation type")
    blocks: dict[str,list[RawProbeObservation]] = defaultdict(list)
    for row in rows:
        if (type(row.block) is not str or not 1 <= len(row.block) <= 80
                or type(row.setting) is not str or not 1 <= len(row.setting) <= 80
                or row.probe not in PROBES or type(row.order) is not int
                or row.order not in (0,1,2)
                or type(row.trace) is not tuple or len(row.trace)!=16
                or any(type(v) not in (float,int) or not isfinite(v)
                       or abs(v)>10.0 for v in row.trace)):
            raise ValueError(f"{name}: malformed observation")
        blocks[row.block].append(row)
    counts=Counter()
    positions=defaultdict(Counter)
    for block,group in blocks.items():
        if (len(group)!=3 or {r.probe for r in group}!=set(PROBES)
                or {r.order for r in group}!={0,1,2}
                or len({r.setting for r in group})!=1):
            raise ValueError(f"{name}: unmatched intervention block")
        setting=group[0].setting
        counts[setting]+=1
        for r in group:
            positions[(setting,r.probe)][r.order]+=1
    if len(counts)<2 or any(v<MIN_BLOCKS_PER_SETTING for v in counts.values()):
        raise ValueError(f"{name}: need two or more independently blocked settings")
    if any(len(c)<3 for c in positions.values()):
        raise ValueError(f"{name}: intervention order is confounded with probe")
    return blocks

def _response(trace: tuple[float,...]) -> tuple[float,float]:
    baseline=sum(trace[:4])/4
    # The fixed response windows are an experimenter-created segmentation.
    return sum(trace[8:])/8-baseline, sum(trace[4:8])/4-baseline

def _effects(blocks):
    differences=defaultdict(lambda: defaultdict(list))
    early=defaultdict(lambda: defaultdict(list))
    for group in blocks.values():
        setting=group[0].setting
        by_probe={r.probe:_response(r.trace) for r in group}
        for probe in PROBES[1:]:
            differences[setting][probe].append(by_probe[probe][0]-by_probe["sham"][0])
            early[setting][probe].append(by_probe[probe][1]-by_probe["sham"][1])
    return ({setting:{probe:median(xs) for probe,xs in inner.items()}
             for setting,inner in differences.items()},
            {setting:{probe:median(xs) for probe,xs in inner.items()}
             for setting,inner in early.items()})

def _eligible(effects, early):
    result={}
    for probe in PROBES[1:]:
        values=[effects[s][probe] for s in sorted(effects)]
        early_values=[early[s][probe] for s in sorted(effects)]
        # Sign and minimum margin must persist in every setting, not only IID mean.
        same_sign=all(x>0 for x in values) or all(x<0 for x in values)
        result[probe]=(min(abs(x) for x in values) if same_sign
                       and max(abs(x) for x in early_values)<=MAX_EARLY_EFFECT else 0.0)
    return result

def screen_bootstrap_contingency(
    training: Sequence[RawProbeObservation],
    holdout: Sequence[RawProbeObservation],
) -> ContingencyScreen:
    """Selection from training alone; separately check disjoint holdout settings."""
    train_blocks=_validate(training,"training")
    test_blocks=_validate(holdout,"holdout")
    train_settings={r.setting for r in training}
    test_settings={r.setting for r in holdout}
    if train_settings & test_settings:
        raise ValueError("holdout must use unseen settings")
    if {r.block for r in training} & {r.block for r in holdout}:
        raise ValueError("train/holdout block overlap")
    fit,fit_early=_effects(train_blocks)
    test,test_early=_effects(test_blocks)
    ranks=_eligible(fit,fit_early)
    ordered=sorted(ranks,key=lambda k:(-ranks[k],k))
    selected=ordered[0] if (ranks[ordered[0]]>=MIN_EFFECT and
                            ranks[ordered[0]]-ranks[ordered[1]]>=MIN_MARGIN) else None
    status="NO_DISCRIMINATING_RESPONSE_CONTINGENCY"
    if selected:
        confirmed=_eligible(test,test_early)
        if confirmed[selected]>=MIN_EFFECT:
            if confirmed[selected]-max(confirmed[p] for p in PROBES[1:] if p!=selected)>=MIN_MARGIN:
                status="RESPONSE_CONTINGENCY_REPLICATED_IN_HELDOUT_SETTINGS"
            else: status="HELDOUT_RESPONSE_AMBIGUOUS"
        else: status="HELDOUT_CONTINGENCY_NOT_REPLICATED"
    return ContingencyScreen(
        status=status,selected_probe=selected,
        fitted_settings=tuple(sorted(train_settings)),
        holdout_settings=tuple(sorted(test_settings)),
        train_effects=tuple((p,round(ranks[p],6)) for p in PROBES[1:]),
        holdout_effects=tuple((p,round(_eligible(test,test_early)[p],6)) for p in PROBES[1:]),
    )
