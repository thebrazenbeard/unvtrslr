"""Explicit, opt-in Lappy client for a separately hosted scripted peer.

No peer rule, oracle targets, or held-out scene coordinates in this module.
Transport credentials are read from an ignored/local external file.
No server process or privileged remote command is launched here.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict
from hashlib import sha256
import ipaddress
import json
from pathlib import Path
import time
from urllib.parse import urlsplit
from urllib.request import build_opener, ProxyHandler, Request
from unvtrslr.contact_negotiation import negotiate

SCHEMA = "UNV_EXTERNAL_PARTNER_V1"
MAX_BYTES = 90000
MAX_TRIALS = 16

def validate_endpoint(url: str):
    if type(url) is not str or len(url)>160:
        raise ValueError("endpoint URL unavailable")
    split=urlsplit(url)
    if split.scheme!="http" or split.path or split.query or split.fragment or split.username:
        raise ValueError("only private HTTP endpoint root permitted")
    try:
        addr=ipaddress.ip_address(split.hostname)
        port=split.port
    except (ValueError,TypeError):
        raise ValueError("endpoint must use explicit private IPv4 address") from None
    if addr.version!=4 or addr not in ipaddress.ip_network("100.64.0.0/10") or not 1024<=port<=65535:
        raise ValueError("endpoint not on authorized private tailnet")
    return url.rstrip("/")+"/v1/interaction"

class Channel:
    def __init__(self, endpoint: str, token: str):
        self.endpoint=validate_endpoint(endpoint)
        if type(token) is not str or len(token)<48 or len(token)>256:
            raise ValueError("invalid private authorization token")
        self._token=token
        self.opener=build_opener(ProxyHandler({}))
    def send(self, message: dict):
        if type(message) is not dict:
            raise ValueError("invalid request")
        encoded=json.dumps(message,sort_keys=True,separators=(",",":")).encode("utf-8")
        if len(encoded)>MAX_BYTES:
            raise ValueError("outgoing request too large")
        request=Request(self.endpoint,data=encoded,method="POST",
                        headers={"X-BT2-Token":self._token,
                                 "Content-Type":"application/json"})
        try:
            with self.opener.open(request, timeout=4) as response:
                if response.status!=200:
                    raise ValueError("peer refused interaction")
                raw=response.read(MAX_BYTES+1)
        except Exception as exc:
            raise ValueError("partner unavailable/refused interaction") from None
        if len(raw)>MAX_BYTES:raise ValueError("oversized peer response")
        try:result=json.loads(raw)
        except (ValueError,UnicodeDecodeError):
            raise ValueError("malformed peer response") from None
        if type(result) is not dict or "error" in result:
            raise ValueError("unexpected peer response")
        return result

class RemotePartner:
    def __init__(self, channel: Channel, session: str):
        self.channel=channel
        if type(session) is not str or len(session)!=24 or not all(
                c in "0123456789abcdef" for c in session):
            raise ValueError("invalid session handle")
        self.session=session
    def _scene(self,scene):
        if type(scene) is not tuple or len(scene)!=2:
            raise ValueError("bad scene")
        return list(scene)
    def observe(self,scene):
        reply=self.channel.send({"op":"observe","session":self.session,
                                 "scene":self._scene(scene)})
        if set(reply)!={"trace"} or type(reply["trace"]) is not list:
            raise ValueError("peer observation malformed")
        return tuple(tuple(row) for row in reply["trace"])
    def offer(self,scene,signal):
        reply=self.channel.send({"op":"offer","session":self.session,
                                 "scene":self._scene(scene),
                                 "signal":[list(x) for x in signal]})
        if reply!={"accepted_for_exposure":True}:
            raise ValueError("peer did not acknowledge exposure")
    def outcome(self,scene,signal):
        reply=self.channel.send({"op":"outcome","session":self.session,
                                 "scene":self._scene(scene),
                                 "signal":[list(x) for x in signal]})
        if set(reply)!={"environment_feedback"}:
            raise ValueError("peer response contract violation")
        return reply["environment_feedback"]

def run_one(channel:Channel):
    begin=channel.send({"op":"begin"})
    if set(begin)!={"session","private_rule_commitment","schema","max_observations"}:
        raise ValueError("unexpected peer initiation")
    if begin["schema"]!=SCHEMA or begin["max_observations"]!=48:
        raise ValueError("peer schema mismatch")
    sid=begin["session"]
    partner=RemotePartner(channel,sid)
    fitted=negotiate(partner)
    proof=channel.send({"op":"qualify","session":sid,
        "selected_sensor_axis":fitted.selected_sensor_axis,
        "outbound_motifs":list(fitted.outbound_motifs) if fitted.outbound_motifs else None})
    needed={"status","holdout_count","mean","ablation_drop",
            "rule_commitment","receipt_sha256","private_rule_kept_on_peer"}
    if set(proof)!=needed or proof["rule_commitment"]!=begin["private_rule_commitment"]:
        raise ValueError("peer commitment changed between training and qualification")
    if proof["status"] not in ("HOLDOUT_PASS","HOLDOUT_FAIL","INELIGIBLE"):
        raise ValueError("invalid partner qualification")
    if proof["status"]=="HOLDOUT_PASS" and fitted.status!="PROPOSAL_CONFIRMED_TRAINING_ONLY":
        raise ValueError("peer passed without frozen learner")
    return {"learner_status":fitted.status,"learner_claim_ceiling":fitted.claim_ceiling,
            "participant_commitment":proof["rule_commitment"],
            "peer_receipt_sha256":proof["receipt_sha256"],
            "peer_heldout_status":proof["status"],"peer_holdout_count":proof["holdout_count"],
            "peer_mean":proof["mean"],"peer_ablation_drop":proof["ablation_drop"],
            "private_rule_kept_on_peer":proof["private_rule_kept_on_peer"],
            "proposal_count":fitted.proposed_signals,
            "training_observations":fitted.training_interactions,
            "contact_with_real_unknown_intelligence":False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--endpoint",required=True)
    parser.add_argument("--token-file",type=Path,required=True)
    parser.add_argument("--trials",type=int,default=8)
    parser.add_argument("--report-out",type=Path,required=True)
    args=parser.parse_args()
    if type(args.trials) is not int or not 1<=args.trials<=MAX_TRIALS:
        raise ValueError("invalid trial count")
    if args.report_out.exists():
        raise ValueError("refuse evidence overwrite")
    if not args.token_file.is_file() or args.token_file.stat().st_size>256:
        raise ValueError("missing/unbounded local credential")
    channel=Channel(args.endpoint,args.token_file.read_text(encoding="ascii").strip())
    trials=[]
    for i in range(args.trials):
        result=run_one(channel)
        trials.append(result)
        print(json.dumps({"trial":i+1,"training":result["learner_status"],
              "peer_test":result["peer_heldout_status"],
              "holdout":result["peer_holdout_count"],
              "ablation":result["peer_ablation_drop"]},sort_keys=True),flush=True)
    output={"schema":"UNV_CROSSHOST_SCRIPTED_CONTACT_LIVE_TRIAL_V1",
        "learner_host":"Lappy","partner_host":"VN2",
        "transport":"private Tailscale HTTP, without TLS",
        "independent_host_scripted_peer":True,
        "verified_real_world_communication":False,
        "access_boundary":"separate host; not strong sandbox",
        "source_code_contains_private_rule":False,
        "results":trials,"total":len(trials)}
    args.report_out.parent.mkdir(parents=True,exist_ok=True)
    args.report_out.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"trials":len(trials),
       "pass":sum(x["peer_heldout_status"]=="HOLDOUT_PASS" for x in trials),
       "fail":sum(x["peer_heldout_status"]=="HOLDOUT_FAIL" for x in trials),
       "ineligible":sum(x["peer_heldout_status"]=="INELIGIBLE" for x in trials)}))

if __name__=="__main__":
    main()
