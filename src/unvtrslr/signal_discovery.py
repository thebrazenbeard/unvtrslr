"""Unsupervised candidate-event segmentation in bounded continuous multichannel traces.

No utterance timestamps, vocabulary, language identity or simulator intent are
inputs. Recurrence is NOT signalhood, communication or semantic grounding.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import median
from typing import Sequence

MAX_FRAMES = 8192
MAX_CHANNELS = 8
CLAIM = "UNSUPERVISED_RECURRENCE_NOT_COMMUNICATIVE_SIGNALHOOD"

@dataclass(frozen=True)
class CandidateEvent:
    start: int
    stop: int
    signature: tuple[float, ...]
    motif: int

@dataclass(frozen=True)
class DiscoveryResult:
    status: str
    events: tuple[CandidateEvent, ...]
    recurring_motifs: tuple[tuple[int, int], ...]
    claim_ceiling: str = CLAIM
    intent_inferred: bool = False
    semantics_inferred: bool = False

def validate_stream(samples: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    if not isinstance(samples, (list, tuple)) or not 32 <= len(samples) <= MAX_FRAMES:
        raise ValueError("stream length outside supported bounds")
    if not isinstance(samples[0], (list, tuple)) or not 1 <= len(samples[0]) <= MAX_CHANNELS:
        raise ValueError("invalid channel dimension")
    width = len(samples[0])
    output = []
    for sample in samples:
        if (not isinstance(sample, (list, tuple)) or len(sample) != width
                or any(type(v) not in (int, float) or not isfinite(v)
                       or abs(v) > 20 for v in sample)):
            raise ValueError("nonfinite/malformed channel sample")
        output.append(tuple(float(v) for v in sample))
    return tuple(output)

def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return sum(x*y for x,y in zip(a,b))

def _segments(samples):
    cols = tuple(zip(*samples))
    centers = tuple(median(col) for col in cols)
    thresholds = tuple(max(.065, 5 * 1.4826 * median(abs(x-mid) for x in col))
                       for col,mid in zip(cols,centers))
    active = [any(abs(v-mid) > threshold for v,mid,threshold
                  in zip(row,centers,thresholds)) for row in samples]
    ranges = []
    position = 0
    while position < len(active):
        if not active[position]:
            position += 1
            continue
        start = position
        end = position + 1
        # Merge short within-event gaps; no timing metadata is supplied.
        while end < len(active):
            if active[end]:
                end += 1
            elif any(active[end + 1:min(end + 3,len(active))]):
                end += 1
            else:
                break
        if 3 <= end-start <= 40:
            rows = samples[start:end]
            direction = tuple(sum(row[j]-centers[j] for row in rows)/len(rows)
                              for j in range(len(centers)))
            size = sqrt(sum(x*x for x in direction))
            if size > .065:
                ranges.append((start,end,tuple(round(x/size,7) for x in direction)))
        position = end
    return ranges

def discover(samples: Sequence[Sequence[float]], *, min_recurrences: int = 3) -> DiscoveryResult:
    if type(min_recurrences) is not int or not 2 <= min_recurrences <= 24:
        raise ValueError("invalid recurrence threshold")
    rows = validate_stream(samples)
    candidates = _segments(rows)
    prototypes = []
    events = []
    counts = Counter()
    for start,stop,signature in candidates:
        similarities = [cosine(signature,proto) for proto in prototypes]
        if similarities and max(similarities) >= .85:
            label = max(range(len(prototypes)), key=lambda idx: similarities[idx])
        elif len(prototypes) < 32:
            label = len(prototypes)
            prototypes.append(signature)
        else:
            continue
        events.append(CandidateEvent(start,stop,signature,label))
        counts[label] += 1
    recurrent = tuple(sorted((label,count) for label,count in counts.items()
                             if count >= min_recurrences))
    if not recurrent:
        status = "NO_RECURRENT_CANDIDATE"
    else:
        onsets = [event.start for event in events if counts[event.motif] >= min_recurrences]
        gaps = [b-a for a,b in zip(onsets,onsets[1:])]
        # Perfectly regular pulses can be a clock, sensor nuisance, or machinery.
        if len(gaps)>=4 and median(gaps)>0 and max(gaps)-min(gaps) < median(gaps)*.08:
            status = "PERIODIC_REGULARITY_UNINTERPRETED"
        else:
            status = "RECURRENT_CANDIDATE_UNINTERPRETED"
    return DiscoveryResult(status,tuple(events),recurrent)

def fingerprint(samples: Sequence[Sequence[float]]) -> tuple[float, ...] | None:
    """Extract a single event signature from a raw recording, without labels."""
    result = discover(samples,min_recurrences=2)
    if len(result.events) != 1:
        return None
    return result.events[0].signature

def recognize(signature: tuple[float,...], prototypes: Sequence[tuple[float,...]]) -> int | None:
    if not prototypes:
        return None
    sims=[cosine(signature,p) for p in prototypes]
    best=max(range(len(sims)),key=lambda i:sims[i])
    return best if sims[best]>=.85 and (len(sims)==1 or
        sims[best]-max(s for i,s in enumerate(sims) if i!=best)>.2) else None
