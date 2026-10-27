"""Strict aggregation of two independently supplied ordinal review sheets.

Input is UNVERIFIED annotator submissions; no human or independent review
provenance is established by possessing a JSONL rating sheet.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

LOCALES=("fr-FR","de-DE","sw-KE","tr-TR")
ERRORS=frozenset(("OMISSION","ADDITION","ROLE_SWAP","NEGATION",
    "TIME","ENTITY","UNINTELLIGIBLE","OTHER"))
PACKET_KEYS=frozenset(("task_id","source_language","target_locale","source_text","candidate_text"))
RATING_KEYS=frozenset(("task_id","reviewer_id","status","adequacy","fluency","errors","comment"))

def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()

def reject_dupes(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError("duplicate JSON key")
        result[key]=value
    return result

def jsonl(path: Path, limit: int) -> list[dict]:
    if not path.is_file() or path.stat().st_size > 4_000_000:
        raise ValueError("missing/oversized review JSONL")
    rows=[]
    with path.open("r",encoding="utf-8") as stream:
        for line in stream:
            if not line.strip() or len(line)>8192 or len(rows)>=limit:
                raise ValueError("blank/oversized/excess review record")
            row=json.loads(line,object_pairs_hook=reject_dupes,
                parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
            if type(row) is not dict: raise ValueError("non-object review record")
            rows.append(row)
    if not rows: raise ValueError("empty review input")
    return rows

def valid_task_id(value):
    return type(value) is str and len(value)==20 and all(c in "0123456789abcdef" for c in value)

def load_packet(path: Path) -> dict[str,dict]:
    rows=jsonl(path,800)
    result={}
    for row in rows:
        if (set(row)!=PACKET_KEYS or not valid_task_id(row["task_id"])
                or row["source_language"]!="en" or row["target_locale"] not in LOCALES
                or type(row["source_text"]) is not str or not row["source_text"].strip()
                or len(row["source_text"])>4096
                or type(row["candidate_text"]) is not str or not row["candidate_text"].strip()
                or len(row["candidate_text"])>4096):
            raise ValueError("malformed blind packet")
        if row["task_id"] in result: raise ValueError("duplicate packet task")
        result[row["task_id"]]=row
    return result

def validate_reviewer_id(value):
    return (type(value) is str and 1<=len(value)<=64
            and all(ch.isascii() and (ch.isalnum() or ch in "_-.") for ch in value))

def validate_rating(row, reviewer_ids):
    if set(row)!=RATING_KEYS or not valid_task_id(row.get("task_id")):
        raise ValueError("malformed rating schema")
    if type(row["reviewer_id"]) is not str or row["reviewer_id"] not in reviewer_ids:
        raise ValueError("unexpected reviewer ID")
    if row["status"] not in ("RATED","UNRATABLE"):
        raise ValueError("invalid review status")
    if row["status"]=="RATED":
        if (type(row["adequacy"]) is not int or not 0<=row["adequacy"]<=4
                or type(row["fluency"]) is not int or not 0<=row["fluency"]<=4):
            raise ValueError("invalid ordinal ratings")
    elif row["adequacy"] is not None or row["fluency"] is not None:
        raise ValueError("unratable task must have null scores")
    if (type(row["errors"]) is not list or len(row["errors"])>len(ERRORS)
            or any(type(error) is not str or error not in ERRORS for error in row["errors"])
            or len(row["errors"])!=len(set(row["errors"]))):
        raise ValueError("invalid error taxonomy")
    if type(row["comment"]) is not str or len(row["comment"])>1000:
        raise ValueError("oversized/nontext review comment")

def language_summary(rows: list[tuple[dict,dict]]) -> dict:
    a,b=zip(*rows)
    paired=[(x["adequacy"],y["adequacy"]) for x,y in rows
            if x["status"]=="RATED" and y["status"]=="RATED"]
    statuses={"both_rated":len(paired),"any_unratable":len(rows)-len(paired)}
    agreement=sum(x==y for x,y in paired)
    n=len(paired)
    if n:
        ac,bc=Counter(x for x,_ in paired),Counter(y for _,y in paired)
        chance=sum(ac[v]*bc[v] for v in range(5))/(n*n)
        kappa=(agreement/n-chance)/(1-chance) if chance<1 else None
    else: kappa=None
    distributions={rid:dict(sorted(Counter(x["adequacy"] for x in side
                      if x["status"]=="RATED").items()))
                   for rid,side in (("reviewer_a",a),("reviewer_b",b))}
    return {**statuses,"ordinal_histograms":distributions,
            "exact_pair_agreement":agreement/n if n else None,
            "cohen_unweighted_kappa":kappa,
            "adequacy_at_least_3_both":sum(x>=3 and y>=3 for x,y in paired)/n if n else None}

def aggregate(packet_path: Path, rating_path: Path, reviewer_a: str, reviewer_b: str) -> dict:
    if (not validate_reviewer_id(reviewer_a) or not validate_reviewer_id(reviewer_b)
            or reviewer_a==reviewer_b):
        raise ValueError("reviewer IDs must be two distinct valid identifiers")
    packet=load_packet(packet_path)
    ratings=jsonl(rating_path,len(packet)*2+1)
    by_pair={}
    reviewers={reviewer_a,reviewer_b}
    for row in ratings:
        validate_rating(row,reviewers)
        if row["task_id"] not in packet: raise ValueError("unknown task_id")
        key=(row["task_id"],row["reviewer_id"])
        if key in by_pair: raise ValueError("duplicate rating")
        by_pair[key]=row
    expected={(task,reviewer) for task in packet for reviewer in reviewers}
    if set(by_pair)!=expected: raise ValueError("missing/extra reviewer ratings")
    grouped={locale:[] for locale in LOCALES}
    for task,row in packet.items():
        grouped[row["target_locale"]].append((
            by_pair[(task,reviewer_a)],by_pair[(task,reviewer_b)]))
    return {"schema":"UNV_BILINGUAL_TWO_REVIEWER_QA_V1",
            "claim_ceiling":"UNVERIFIED_ANNOTATOR_SUBMISSIONS_NOT_INDEPENDENTLY_ATTESTED",
            "packet_sha256":sha(packet_path),"ratings_sha256":sha(rating_path),
            "reviews_supplied":len(ratings),"tasks_supplied":len(packet),
            "reviewers":["reviewer_a","reviewer_b"],
            "independence_proven":False,"human_provenance_verified":False,
            "languages":{locale:language_summary(grouped[locale])
                         for locale in LOCALES if grouped[locale]}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--packet",required=True,type=Path)
    ap.add_argument("--ratings",required=True,type=Path)
    ap.add_argument("--reviewer-a",required=True)
    ap.add_argument("--reviewer-b",required=True)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--expected-packet-sha256",required=True)
    args=ap.parse_args()
    expected=args.expected_packet_sha256
    if (len(expected)!=64 or any(c not in "0123456789abcdef" for c in expected)
            or sha(args.packet)!=expected):
        raise ValueError("blind packet digest mismatch")
    if args.out.exists(): raise ValueError("refuse report overwrite")
    result=aggregate(args.packet,args.ratings,args.reviewer_a,args.reviewer_b)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"tasks":result["tasks_supplied"],
        "reviews":result["reviews_supplied"],
        "human_provenance_verified":False,
        "out":str(args.out)},sort_keys=True))

if __name__=="__main__":
    main()
