"""Separate evaluator-side synthetic partner, with private sensor rule and codebook."""
from __future__ import annotations
import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
from random import Random

from unvtrslr.signal_discovery import discover,fingerprint,cosine
from unvtrslr.contact_negotiation import SCENES,_outbound_symbol,negotiate

HELDOUT=((-0.87,-0.72),(0.92,-0.73),(-0.84,0.88),(0.96,0.91))
SEEDS=(17,41,73,107)
MODES=("responsive","silent","fixed","independent","xor",
       "no_adaptation","partner_drift","slow_adaptation","always_reward")
EXPECTED={
 "responsive":"RECIPROCAL_OPERATIONAL_CONVENTION_ON_HELDOUT_CONTEXTS",
 "silent":"NO_DECODABLE_CANDIDATE",
 "fixed":"NO_IDENTIFIABLE_SENSOR_RELATION",
 "independent":"NO_IDENTIFIABLE_SENSOR_RELATION",
 "xor":"NO_IDENTIFIABLE_SENSOR_RELATION",
 "no_adaptation":"PROPOSAL_NOT_CONFIRMED",
 "partner_drift":"RECIPROCAL_CONVENTION_NOT_REPLICATED",
 "slow_adaptation":"RECIPROCAL_OPERATIONAL_CONVENTION_ON_HELDOUT_CONTEXTS",
 "always_reward":"PROPOSAL_NOT_CONFIRMED",
}
class PrivateSyntheticPartner:
    """Rule and original sign code never cross learner's PartnerPort API."""
    def __init__(self, seed:int, mode:str):
        if mode not in MODES: raise ValueError("invalid synthetic partner mode")
        self.rng=Random(seed)
        self.axis=self.rng.randrange(2)
        self.permute=self.rng.randrange(2)
        self.mode=mode
        self.counter=0
        self.offered={0:[],1:[]}
    def _private_class(self,scene,*,testing=False):
        axis=1-self.axis if testing and self.mode=="partner_drift" and scene not in SCENES else self.axis
        state=int(scene[axis]>0)
        if self.mode=="xor":state=int((scene[0]>0)!=(scene[1]>0))
        if self.mode=="fixed":state=0
        if self.mode=="independent":state=self.rng.randrange(2)
        return state
    def observe(self,scene):
        self.counter+=1
        state=self._private_class(scene)
        if self.mode=="silent":state=None
        channel=state ^ self.permute if state is not None else None
        position=self.rng.randrange(7,27)
        raw=[]
        for i in range(64):
            noise=(self.rng.uniform(-.007,.007),self.rng.uniform(-.007,.007))
            pulse=.8 if position<=i<position+7 else 0.0
            raw.append(tuple(round(noise[j]+(pulse if channel==j else 0.0),6)
                             for j in range(2)))
        return tuple(raw)
    def offer(self,scene,signal):
        if self.mode in ("silent","no_adaptation"):return
        state=self._private_class(scene)
        signature=fingerprint(signal)
        if signature is not None:self.offered[state].append(signature)
    def outcome(self,scene,signal):
        if self.mode=="always_reward":return .9
        if self.mode in ("silent","no_adaptation"):return .1
        state=self._private_class(scene,testing=True)
        signature=fingerprint(signal)
        if signature is None:return .1
        offered=self.offered[state]
        other=self.offered[1-state]
        required=9 if self.mode=="slow_adaptation" else 3
        if len(offered)<required or len(other)<required:return .1
        if (min(cosine(signature,x) for x in offered)<.85
                or max(cosine(signature,x) for x in other)>.85):
            return .1
        return .9

def raw_stream(seed:int,mode:str):
    rng=Random(seed)
    raw=[[rng.uniform(-.006,.006) for _ in range(2)] for _ in range(768)]
    if mode=="noise":return tuple(tuple(x) for x in raw)
    starts=list(range(32,704,56)) if mode=="periodic" else [
        34,98,142,208,253,327,369,441,516,564,632,697]
    for number,start in enumerate(starts):
        ch=number%2
        for offset in range(6):
            raw[start+offset][ch]+=.83
    return tuple(tuple(round(v,6) for v in x) for x in raw)

def evaluate_heldout(partner,model):
    """Only evaluator accesses the frozen withheld scenes; never fit on them."""
    if model.status!="PROPOSAL_CONFIRMED_TRAINING_ONLY":
        return model
    if model.selected_sensor_axis not in (0,1) or model.outbound_motifs is None:
        raise ValueError("missing frozen learned convention")
    observations=[]
    for scene in HELDOUT:
        selected=model.outbound_motifs[int(scene[model.selected_sensor_axis]>0)]
        expected=partner.outcome(scene,_outbound_symbol(selected))
        control=partner.outcome(scene,_outbound_symbol(1-selected))
        if (type(expected) not in (int,float) or type(control) not in (int,float)
                or not 0<=expected<=1 or not 0<=control<=1):
            raise ValueError("invalid heldout outcome")
        observations.append((expected,control))
    success=all(actual>=.75 and actual-control>=.5
                for actual,control in observations)
    return replace(model,
        status=("RECIPROCAL_OPERATIONAL_CONVENTION_ON_HELDOUT_CONTEXTS"
                if success else "RECIPROCAL_CONVENTION_NOT_REPLICATED"),
        heldout_success=sum(pair[0] for pair in observations)/len(observations),
        withheld_contexts=len(observations))

def evaluate(seed,mode):
    partner=PrivateSyntheticPartner(seed,mode)
    fitted=negotiate(partner)
    result=evaluate_heldout(partner,fitted)
    return {"seed":seed,"mode":mode,"expected":EXPECTED[mode],
            "observed":asdict(result),
            "control_pass":result.status==EXPECTED[mode]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists():raise ValueError("refuse to overwrite existing evidence")
    interaction=[evaluate(seed,mode) for seed in SEEDS for mode in MODES]
    discovery=[{"seed":seed,"kind":mode,"result":asdict(discover(raw_stream(seed,mode)))}
               for seed in SEEDS for mode in ("candidate","noise","periodic")]
    expected={"candidate":"RECURRENT_CANDIDATE_UNINTERPRETED",
              "noise":"NO_RECURRENT_CANDIDATE",
              "periodic":"PERIODIC_REGULARITY_UNINTERPRETED"}
    discovery_ok=all(record["result"]["status"]==expected[record["kind"]]
                     for record in discovery)
    report={"schema":"UNV_AUTONOMOUS_SIGNAL_AND_RECIPROCAL_CONVENTION_SYNTHETIC_V1",
            "git_version":"phase-0/2 source-bound executable",
            "claim_ceiling":"SYNTHETIC_WITH_EXPERIMENTER_SENSOR_CHANNELS_NO_REAL_CONTACT",
            "learner_does_not_receive":["partner sensor axis","partner signal codebook",
                "private reference interpretation","true partner mode",
                "synthetic evaluator oracle labels"],
            "experimenter_provided":["2 numeric sensor dimensions","4 accessible probe scenes",
                "known trial capture windows for negotiation","single scalar environmental success metric",
                "partner offer/observation affordance"],
            "seeds":list(SEEDS),"discovery":discovery,"interaction":interaction,
            "discovery_expected_matched":discovery_ok,
            "interaction_expected_matched":all(x["control_pass"] for x in interaction),
            "real_unknown_partner_contacted":False,
            "os_isolation_verified":False}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"discovery_cases":len(discovery),
        "discovery_pass":sum(x["result"]["status"]==expected[x["kind"]] for x in discovery),
        "negotiation_cases":len(interaction),
        "negotiation_pass":sum(x["control_pass"] for x in interaction),
        "positive":[{"seed":x["seed"],"status":x["observed"]["status"],
                     "axis":x["observed"]["selected_sensor_axis"],
                     "heldout":x["observed"]["heldout_success"]}
                    for x in interaction if x["mode"]=="responsive"]},sort_keys=True))

if __name__=="__main__":
    main()
