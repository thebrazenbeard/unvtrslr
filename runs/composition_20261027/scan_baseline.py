"""Read-only official SCAN add-primitive control; does NOT run the learner."""
import argparse
import hashlib
import json
from pathlib import Path

OFFICIAL_SCAN_GIT_HEAD="c4b756cbc010d75c912f16c42c8f15dc6b7e6c8f"
TRAIN_SHA="15c82c6bd4222a1f44d28aea6e56f23a52002c9a8b05f77497544114055a62b7"
TEST_SHA="14ea0560537282a343141d324a278ee4d7337a1744f740dc811307ab6f162450"

def read_tasks(path, digest):
    if path.stat().st_size > 5_000_000:
        raise ValueError("unexpectedly large SCAN split")
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=digest:
        raise ValueError("SCAN source digest mismatch")
    result=[]
    for line in data.decode("utf-8").splitlines():
        if not line.startswith("IN: ") or " OUT: " not in line:
            raise ValueError("invalid SCAN task record")
        source,target=line[4:].split(" OUT: ",1)
        if not source or not target or len(source)>512 or len(target)>4096:
            raise ValueError("oversized SCAN task")
        result.append((source,target))
    seen={}
    for source,target in result:
        if source in seen and seen[source]!=target:
            raise ValueError("conflicting SCAN source labels")
        seen[source]=target
    return result

def evaluate(scan_root):
    base=scan_root/"add_prim_split"
    train=read_tasks(base/"tasks_train_addprim_jump.txt",TRAIN_SHA)
    test=read_tasks(base/"tasks_test_addprim_jump.txt",TEST_SHA)
    memo=dict(train)
    hits=sum(source in memo for source,_ in test)
    copied=sum(source==target for source,target in test)
    return {"schema":"UNV_SCAN_ADDPRIM_JUMP_NEGATIVE_CONTROL_V1",
            "dataset_repo":"brendenlake/SCAN","git_head":OFFICIAL_SCAN_GIT_HEAD,
            "train_sha256":TRAIN_SHA,"test_sha256":TEST_SHA,
            "train_records":len(train),"test_records":len(test),
            "exact_phrasebook_coverage":hits/len(test),
            "source_copy_exact_match":copied/len(test),
            "current_positional_learner":"NOT_APPLICABLE_TO_VARIABLE_LENGTH_ACTION_SEQUENCES",
            "claim_ceiling":"NEGATIVE_CONTROLS_ONLY_NO_SCAN_MODEL_MEASURED"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--scan-root",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    if args.out.exists(): raise ValueError("report exists")
    report=evaluate(args.scan_root)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report,sort_keys=True))

if __name__=="__main__":
    main()
