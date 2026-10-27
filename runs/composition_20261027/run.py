"""Evaluator-side synthetic composition benchmark, not Num'ta'reen canon."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

SEEDS=(17,23,47,61)
SIZES=(8,16,32,48,64,96)
SCHEMA="UNV_SYNTHETIC_COMPOSITION_BENCHMARK_V1"

def cases(seed):
    def token(kind,i):
        return "v"+hashlib.sha256(f"{seed}/private/{kind}/{i}".encode()).hexdigest()[:10]
    nouns={v:token("n",i) for i,v in enumerate(("ari","bel","cen","dor"))}
    verbs={v:token("v",i) for i,v in enumerate(("see","call","guide"))}
    tenses={v:token("t",i) for i,v in enumerate(("past","present"))}
    pols={v:token("p",i) for i,v in enumerate(("positive","negative"))}
    result=[]
    for actor,action,patient,tense,polarity in itertools.product(nouns,verbs,nouns,tenses,pols):
        meaning={"actor":actor,"action":action,"patient":patient,"tense":tense,"polarity":polarity}
        source=" ".join([nouns[actor],verbs[action],nouns[patient],tenses[tense],pols[polarity]])
        rid=hashlib.sha256(f"{seed}/{source}".encode()).hexdigest()[:16]
        result.append({"id":rid,"source_text":source,"meaning":meaning})
    random.Random(seed).shuffle(result)
    return result[:96],result[96:]

def sha(rows):
    content="".join(json.dumps(x,sort_keys=True)+"\n" for x in rows).encode()
    return hashlib.sha256(content).hexdigest()

def dump(path,rows):
    path.write_text("".join(json.dumps(x,sort_keys=True)+"\n" for x in rows),encoding="utf-8")

def run_worker(train,holdout,folder):
    folder.mkdir()
    tp,rp,mp,pp=(folder/x for x in ("train.jsonl","requests.jsonl","model.json","pred.json"))
    dump(tp,train)
    dump(rp,[{"id":x["id"],"source_text":x["source_text"]} for x in holdout])
    script=Path(__file__).resolve().parents[2]/"src"/"unvtrslr"/"compositional_probe.py"
    commands=(
      [sys.executable,str(script),"fit","--training",str(tp),"--model-out",str(mp)],
      [sys.executable,str(script),"predict","--model",str(mp),"--requests",str(rp),"--predictions-out",str(pp)])
    for command in commands:
        p=subprocess.run(command,cwd=str(folder),capture_output=True,text=True,timeout=45,check=False)
        if p.returncode: raise RuntimeError(f"worker error {p.returncode}: {p.stderr[:500]}")
    predictions=json.loads(pp.read_text(encoding="utf-8"))
    model=json.loads(mp.read_text(encoding="utf-8"))
    if len(predictions)!=len(holdout) or [x["id"] for x in predictions]!=[x["id"] for x in holdout]:
        raise ValueError("prediction count/identity mismatch")
    return predictions,model

def score(predictions,targets):
    n=len(targets)
    correct=sum(p["status"]=="OK" and p["meaning"]==t["meaning"] for p,t in zip(predictions,targets))
    covered=sum(p["status"]=="OK" for p in predictions)
    return {"records":n,"coverage":covered/n,"exact_accuracy":correct/n}

def evaluate(seed,folder):
    train,holdout=cases(seed)
    assert not {x["source_text"] for x in train}&{x["source_text"] for x in holdout}
    result={"seed":seed,"train_sha256":sha(train),"holdout_sha256":sha(holdout),"curves":[]}
    for n in SIZES:
        predictions,model=run_worker(train[:n],holdout,folder/f"{seed}_{n}")
        result["curves"].append({"train":n,**score(predictions,holdout),
            "learned_positions":{k:v["position"] for k,v in model["hypotheses"].items()}})
    phrasebook={x["source_text"]:x["meaning"] for x in train}
    control=[{"status":"OK","meaning":phrasebook[x["source_text"]]}
             if x["source_text"] in phrasebook else {"status":"ABSTAIN","meaning":None}
             for x in holdout]
    result["phrasebook_control"]=score(control,holdout)
    labels=[x["meaning"] for x in train]
    random.Random(seed+104729).shuffle(labels)
    corrupted=[{**x,"meaning":labels[i]} for i,x in enumerate(train)]
    baseline,_=run_worker(corrupted,holdout,folder/f"{seed}_scrambled")
    result["shuffled_label_control"]=score(baseline,holdout)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,choices=SEEDS,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists(): raise ValueError("refuse to overwrite report")
    with tempfile.TemporaryDirectory(prefix="unv-private-composition-") as temp:
        result=evaluate(args.seed,Path(temp))
    receipt={"schema":SCHEMA,"seed":args.seed,"sizes":SIZES,
             "origin":"private-synthetic; not source-attested Numtareen",
             "claim_ceiling":"SUPERVISED_FIXED_LENGTH_POSITIONAL_COMPOSITION_SYNTHETIC_ONLY",
             "isolation":"separate process; OS filesystem permissions NOT restricted",
             "result":result}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"seed":args.seed,"curve":[(r["train"],r["exact_accuracy"])
        for r in result["curves"]],"phrasebook":result["phrasebook_control"],
        "shuffled":result["shuffled_label_control"]}))

if __name__=="__main__":
    main()
