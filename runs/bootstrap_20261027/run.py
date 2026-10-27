"""Evaluator-side synthetic active-probe contingency tests (not extraterrestrial contact)."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import itertools
import json
from pathlib import Path
from random import Random
from unvtrslr.bootstrap_contingency import (
    PROBES,RawProbeObservation,screen_bootstrap_contingency,
)

SEEDS=(17,41,73)
MODES=("contingent","no_response","context_confounded","early_only",
       "training_only","ambiguous","order_artifact")
EXPECTED={"contingent":"RESPONSE_CONTINGENCY_REPLICATED_IN_HELDOUT_SETTINGS",
          "no_response":"NO_DISCRIMINATING_RESPONSE_CONTINGENCY",
          "context_confounded":"NO_DISCRIMINATING_RESPONSE_CONTINGENCY",
          "early_only":"NO_DISCRIMINATING_RESPONSE_CONTINGENCY",
          "training_only":"HELDOUT_CONTINGENCY_NOT_REPLICATED",
          "ambiguous":"NO_DISCRIMINATING_RESPONSE_CONTINGENCY",
          "order_artifact":"NO_DISCRIMINATING_RESPONSE_CONTINGENCY"}

def generate(seed: int, mode: str):
    if type(seed) is not int or type(mode) is not str or mode not in MODES:
        raise ValueError("unsupported synthetic run")
    rng=Random(seed)
    result=[]
    for context in range(4):
        setting=f"c{context}"  # deliberately opaque; no semantic factor names given
        permutations=list(itertools.permutations(PROBES))
        assigned=permutations*3
        rng.shuffle(assigned)
        for block_index,assignment in enumerate(assigned):
            baseline=0.15*context+0.012*(block_index%5)
            # One block holds all three modes, with randomized intervention order.
            drift=rng.uniform(-.035,.035)
            for position,probe in enumerate(assignment):
                early_effect,late_effect=0.0,0.0
                if mode=="contingent" and probe=="probe_b":
                    late_effect=.72
                if mode=="training_only" and probe=="probe_b" and context<2:
                    late_effect=.72
                if mode=="early_only" and probe=="probe_b":
                    early_effect=.72
                if mode=="ambiguous" and probe!="sham":
                    late_effect=.72
                if mode=="context_confounded":
                    late_effect=.72 if context%2 else -.72
                if mode=="order_artifact":
                    late_effect=.72 if position==2 else 0.0
                noise=lambda: rng.uniform(-.012,.012)
                trace=tuple(round(baseline+drift+noise()+
                           (early_effect if 4<=i<8 else late_effect if i>=8 else 0),6)
                            for i in range(16))
                result.append(RawProbeObservation(
                    block=f"{setting}_b{block_index}",
                    setting=setting,probe=probe,order=position,trace=trace))
    return result[:2*18*3],result[2*18*3:]

def score(seed: int,mode: str) -> dict:
    train,test=generate(seed,mode)
    status=screen_bootstrap_contingency(train,test)
    return {"seed":seed,"mode":mode,"training_trials":len(train),
            "heldout_trials":len(test),"result":asdict(status),
            "expected_status":EXPECTED[mode],
            "control_pass":status.status==EXPECTED[mode]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    if args.out.exists(): raise ValueError("refuse report overwrite")
    trials=[score(seed,mode) for seed in SEEDS for mode in MODES]
    record={"schema":"UNV_EXPERIMENTER_FRAMED_BOOTSTRAP_CAUSAL_SCREEN_V1",
            "claim_ceiling":"CONTROLLED_SYNTHETIC_CONTINGENCY_NOT_SIGNALHOOD_OR_SEMANTICS",
            "experimenter_assumptions":["predefined candidate probe actions",
              "presegmented 16-point receiver traces","matched sham interventions",
              "experimenter-designated observed target","known matched settings",
              "no OS isolation, evaluator holds generated truth"],
            "seeds":list(SEEDS),"modes":list(MODES),"controls":trials,
            "all_control_expectations_met":all(r["control_pass"] for r in trials)}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"controls":len(trials),
        "passed":sum(r["control_pass"] for r in trials),
        "status_by_mode":{mode:[r["result"]["status"] for r in trials
                         if r["mode"]==mode] for mode in MODES}},sort_keys=True))

if __name__=="__main__":
    main()
