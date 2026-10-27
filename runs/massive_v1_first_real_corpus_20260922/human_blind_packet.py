"""Produce source-only blinded bilingual review tasks; NO human scores fabricated."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from runs.massive_v1_first_real_corpus_20260922.argos_source_only import read_requests
from runs.massive_v1_first_real_corpus_20260922.blind_text import load_external_predictions

LOCALES={"fr":"fr-FR","de":"de-DE","sw":"sw-KE","tr":"tr-TR"}
PREDICTION_SHA={
 "fr":"3d2dc8ae73c39320addddfa0f4d2392a4ec0d15c2c48fe06216351d927dffb1c",
 "de":"f42419d68d8c79be168e91d55572a1a90b62f0a4245c2860e1503719725c2dd3",
 "sw":"49ccda3669c77a28311e942fbef57f7b29ab665a4836cabdd1ba2283926f1c43",
 "tr":"977c16f2e12a2cb4a8b43b6893d9f083508948da208544d2a2384462e22e5654",
}
SAMPLE_SEED="UNV_BILINGUAL_QA_SHA_SAMPLE_V1"

def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()

def make_tasks(requests, predictions, locale, count=20):
    if len(requests)!=len(predictions) or len(requests)!=200:
        raise ValueError("frozen request/prediction count mismatch")
    by_id={p["id"]:p for p in predictions}
    if len(by_id)!=200 or set(by_id)!={r["id"] for r in requests}:
        raise ValueError("prediction identities mismatch")
    if not 1 <= count <= 200: raise ValueError("invalid sampling count")
    for prediction in predictions:
        if set(prediction)!={"id","status","text"} or prediction["status"]!="OK":
            raise ValueError("unusable prediction")
        if type(prediction["text"]) is not str or not prediction["text"].strip():
            raise ValueError("empty prediction")
    ordered=sorted(requests,key=lambda r:hashlib.sha256(
        f"{SAMPLE_SEED}/{locale}/{r['id']}".encode()).hexdigest())[:count]
    reviewer=[]
    private=[]
    for row in ordered:
        rid=row["id"]
        task_id=hashlib.sha256(f"ANON/{SAMPLE_SEED}/{locale}/{rid}".encode()).hexdigest()[:20]
        reviewer.append({"task_id":task_id,"source_language":"en",
                         "target_locale":locale,"source_text":row["source_text"],
                         "candidate_text":by_id[rid]["text"]})
        private.append({"task_id":task_id,"private_source_id":rid,
                        "engine":"argostranslate==1.11.0",
                        "note":"never send this manifest to annotators"})
    return reviewer,private

def check_output_separation(public, private):
    """Separate reviewer/manifest trees; not filesystem ACL enforcement."""
    public=public.resolve(strict=False)
    private=private.resolve(strict=False)
    if (public==private or public.parent==private.parent
            or public.is_relative_to(private.parent)
            or private.is_relative_to(public.parent)):
        raise ValueError("reviewer/private output tree overlap")


def write_new(path, rows):
    if path.exists(): raise ValueError("refuse to overwrite review artifact")
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8",newline="\n") as stream:
        for row in rows: stream.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--requests-dir",required=True,type=Path)
    p.add_argument("--predictions-dir",required=True,type=Path)
    p.add_argument("--reviewer-out",required=True,type=Path)
    p.add_argument("--private-out",required=True,type=Path)
    p.add_argument("--per-language",type=int,default=20)
    args=p.parse_args()
    public=args.reviewer_out.resolve(strict=False)
    private=args.private_out.resolve(strict=False)
    check_output_separation(public,private)
    if public.exists() or private.exists(): raise ValueError("refuse overwrite")
    reviewer,manifest=[],[]
    for target,locale in LOCALES.items():
        requests=read_requests(args.requests_dir/f"requests_en_to_{locale}.jsonl",target,200)
        path=args.predictions_dir/f"predictions_en_to_{locale}.jsonl"
        if sha(path)!=PREDICTION_SHA[target]:
            raise ValueError("Argos frozen prediction digest mismatch")
        predictions=load_external_predictions(path,expected_count=200)
        review,private_rows=make_tasks(requests,predictions,locale,args.per_language)
        reviewer+=review;manifest+=private_rows
    reviewer.sort(key=lambda r:hashlib.sha256((SAMPLE_SEED+"/"+r["task_id"]).encode()).hexdigest())
    manifest.sort(key=lambda r:r["task_id"])
    if len({r["task_id"] for r in reviewer})!=len(reviewer):
        raise ValueError("colliding anonymized review IDs")
    write_new(public,reviewer)
    write_new(private,manifest)
    print(json.dumps({"schema":"UNV_BILINGUAL_HUMAN_PACKET_V1",
        "reviewer_rows":len(reviewer),"private_rows":len(manifest),
        "reviewer_sha256":sha(public),"private_sha256":sha(private),
        "human_scores":"NOT_YET_COLLECTED",
        "isolation":"separate output dirs, not OS-enforced access controls"}))

if __name__=="__main__":
    main()
