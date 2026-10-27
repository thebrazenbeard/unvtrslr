"""Supervised, fixed-length semantic-composition learner; not universal translation."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

SCHEMA = "UNV_SUPERVISED_POSITIONAL_COMPOSITION_V1"
MAX_RECORDS = 4096

def tokens(value):
    if type(value) is not str or not value or len(value) > 512:
        raise ValueError("bad source")
    result = tuple(value.split())
    if not 1 <= len(result) <= 16 or any(len(t) > 64 for t in result):
        raise ValueError("bad source tokens")
    return result

def validate_meaning(value):
    if type(value) is not dict or not 1 <= len(value) <= 12:
        raise ValueError("invalid meaning")
    if any(type(k) is not str or not k or len(k) > 48 or
           type(v) is not str or not v or len(v) > 64
           for k,v in value.items()):
        raise ValueError("invalid meaning fields")
    return value

def fit(rows):
    if type(rows) is not list or not 4 <= len(rows) <= MAX_RECORDS:
        raise ValueError("invalid training count")
    ids, utterances = set(), set()
    fields, npos = None, None
    for row in rows:
        if type(row) is not dict or set(row) != {"id","source_text","meaning"}:
            raise ValueError("train schema leakage")
        if type(row["id"]) is not str or not row["id"] or len(row["id"]) > 100:
            raise ValueError("invalid training id")
        words = tokens(row["source_text"])
        meaning = validate_meaning(row["meaning"])
        if row["id"] in ids or row["source_text"] in utterances:
            raise ValueError("duplicate training record")
        ids.add(row["id"]); utterances.add(row["source_text"])
        if fields is None:
            fields, npos = tuple(sorted(meaning)), len(words)
        if tuple(sorted(meaning)) != fields or len(words) != npos:
            raise ValueError("heterogeneous training shape")
    hypotheses = {}
    for field in fields:
        proposals = []
        for pos in range(npos):
            counts = defaultdict(Counter)
            for row in rows:
                counts[tokens(row["source_text"])[pos]][row["meaning"][field]] += 1
            supported = {term: next(iter(counter)) for term,counter in counts.items()
                         if len(counter) == 1 and sum(counter.values()) >= 2}
            correct = sum(supported.get(tokens(r["source_text"])[pos]) == r["meaning"][field]
                          for r in rows)
            proposals.append((correct / len(rows), pos, supported))
        proposals.sort(key=lambda r: (-r[0],r[1]))
        best = proposals[0]
        second = proposals[1][0] if len(proposals) > 1 else 0.0
        if best[0] >= .85 and best[0] - second >= .15:
            hypotheses[field] = {"position":best[1],"mapping":best[2],
                                 "train_loo_accuracy":best[0]}
    digest = hashlib.sha256(json.dumps(rows,sort_keys=True,ensure_ascii=False,
                    separators=(",",":")).encode("utf-8")).hexdigest()
    return {"schema":SCHEMA,"train_sha256":digest,"train_rows":len(rows),
            "positions":npos,"fields":list(fields),"hypotheses":hypotheses,
            "claim_ceiling":"SUPERVISED_FIXED_LENGTH_POSITIONAL_COMPOSITION_SYNTHETIC_ONLY"}

def validate_model(model):
    """Reject structural alteration; this does not authenticate who fitted it."""
    required = {"schema","train_sha256","train_rows","positions",
                "fields","hypotheses","claim_ceiling"}
    if type(model) is not dict or set(model) != required or model.get("schema") != SCHEMA:
        raise ValueError("unrecognized fitted model schema")
    if model["claim_ceiling"] != "SUPERVISED_FIXED_LENGTH_POSITIONAL_COMPOSITION_SYNTHETIC_ONLY":
        raise ValueError("model claim ceiling altered")
    if type(model["train_rows"]) is not int or not 4 <= model["train_rows"] <= MAX_RECORDS:
        raise ValueError("bad model train count")
    digest = model["train_sha256"]
    if type(digest) is not str or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("bad model digest")
    n = model["positions"]
    if type(n) is not int or not 1 <= n <= 16:
        raise ValueError("bad model dimensions")
    fields = model["fields"]
    if (type(fields) is not list or not 1 <= len(fields) <= 12
            or any(type(x) is not str or not x or len(x) > 48 for x in fields)
            or fields != sorted(set(fields))):
        raise ValueError("bad model fields")
    hypotheses = model["hypotheses"]
    if type(hypotheses) is not dict or not set(hypotheses).issubset(set(fields)):
        raise ValueError("bad model hypotheses")
    for field,hyp in hypotheses.items():
        if type(hyp) is not dict or set(hyp) != {"position","mapping","train_loo_accuracy"}:
            raise ValueError("malformed model hypothesis")
        position = hyp["position"]
        if type(position) is not int or not 0 <= position < n:
            raise ValueError("model position out of bounds")
        accuracy = hyp["train_loo_accuracy"]
        if type(accuracy) not in (float,int) or not .85 <= accuracy <= 1.0:
            raise ValueError("invalid model support")
        mapping = hyp["mapping"]
        if type(mapping) is not dict or not 1 <= len(mapping) <= MAX_RECORDS:
            raise ValueError("invalid model mapping")
        if any(type(term) is not str or not term or len(term) > 64
               or any(ch.isspace() for ch in term) or type(value) is not str
               or not value or len(value) > 64 for term,value in mapping.items()):
            raise ValueError("malformed model symbols")
    return model


def predict(model, source):
    validate_model(model)
    words = tokens(source)
    if len(words) != model["positions"]:
        return {"status":"ABSTAIN","meaning":None,"unresolved":model["fields"]}
    values, missing = {}, []
    for field in model["fields"]:
        hyp = model["hypotheses"].get(field)
        value = hyp["mapping"].get(words[hyp["position"]]) if hyp else None
        if value is None: missing.append(field)
        else: values[field] = value
    return {"status":"ABSTAIN" if missing else "OK",
            "meaning":None if missing else values,"unresolved":missing}

def load_jsonl(path, keys):
    if not path.is_file() or path.stat().st_size > 2_000_000:
        raise ValueError("file missing or too large")
    def no_duplicates(items):
        out = {}
        for k,v in items:
            if k in out: raise ValueError("duplicate JSON key")
            out[k] = v
        return out
    result = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip() or len(line) > 16384 or len(result) >= MAX_RECORDS:
                raise ValueError("invalid line/row count")
            row = json.loads(line,object_pairs_hook=no_duplicates,
                parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite")))
            if type(row) is not dict or set(row) != keys:
                raise ValueError("reference labels in source-only requests")
            result.append(row)
    if not result: raise ValueError("empty input")
    return result

def save_new(path, obj):
    if path.exists(): raise ValueError("refuse output overwrite")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(obj,ensure_ascii=False,sort_keys=True,
                      separators=(",",":"))+"\n").encode("utf-8"))

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="mode",required=True)
    fit_parser = sub.add_parser("fit")
    fit_parser.add_argument("--training",type=Path,required=True)
    fit_parser.add_argument("--model-out",type=Path,required=True)
    pred_parser = sub.add_parser("predict")
    pred_parser.add_argument("--model",type=Path,required=True)
    pred_parser.add_argument("--requests",type=Path,required=True)
    pred_parser.add_argument("--predictions-out",type=Path,required=True)
    args = parser.parse_args()
    if args.mode == "fit":
        save_new(args.model_out,fit(load_jsonl(args.training,{"id","source_text","meaning"})))
    else:
        if not args.model.is_file() or args.model.stat().st_size > 2_000_000:
            raise ValueError("missing or oversized fitted model")
        model = json.loads(args.model.read_text(encoding="utf-8"))
        validate_model(model)
        rows = load_jsonl(args.requests,{"id","source_text"})
        if any(type(r["id"]) is not str or not r["id"] for r in rows):
            raise ValueError("invalid request ID")
        ids = [r["id"] for r in rows]
        if len(ids) != len(set(ids)): raise ValueError("duplicate request")
        save_new(args.predictions_out,[{"id":r["id"],**predict(model,r["source_text"])}
                                       for r in rows])

if __name__ == "__main__":
    main()
