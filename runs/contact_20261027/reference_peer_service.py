"""Private, separately hosted *scripted* peer. NEVER a claim of alien contact.

Linux VN2-only; rule, withheld scenes and random state are not in learner Git.
HTTP transport is accessible only on the configured Tailscale address with
a pre-shared authorization token and a finite small bounded request protocol.
"""
from __future__ import annotations
from collections import defaultdict
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import secrets
import threading
import time

HOME=Path(__file__).resolve().parent
TOKEN=(HOME/"token.txt").read_text().strip()
HOST=os.environ.get("BT2_PEER_HOST","100.95.37.34")
PORT=int(os.environ.get("BT2_PEER_PORT","18047"))
MODES=["responsive","slow","silent","fixed","random","constant_reward","nonadaptive","drift"]
secrets.SystemRandom().shuffle(MODES)
SESSION={}
LOCK=threading.Lock()
LOG=HOME/"private_receipts.jsonl"
CAP=16
RNG=secrets.SystemRandom()

def wire_signature(rows):
    if type(rows) is not list or len(rows)!=64 or any(
        type(p) is not list or len(p)!=2 or any(type(x) not in (float,int)
        or not math.isfinite(x) or abs(x)>2 for x in p) for p in rows):
        raise ValueError("invalid bounded signal")
    totals=[sum(abs(p[c]) for p in rows) for c in range(2)]
    largest=max(range(2),key=lambda c:totals[c])
    if totals[largest]<4 or totals[1-largest]>.8:return None
    return largest

def scene_state(s,scene,holdout=False):
    if type(scene) is not list or len(scene)!=2 or any(
        type(x) not in (int,float) or not math.isfinite(x) or not -1<=x<=1
        for x in scene):raise ValueError("invalid scene")
    axis=1-s["axis"] if holdout and s["mode"]=="drift" else s["axis"]
    return int(scene[axis]>0)

def payoff(s,scene,signal,holdout=False):
    state=scene_state(s,scene,holdout)
    if s["mode"]=="constant_reward":return .9
    if s["mode"] in ("silent","nonadaptive"):return .1
    ch=wire_signature(signal)
    if ch is None:return .1
    required=9 if s["mode"]=="slow" else 3
    selected=s["offers"][state]
    opposite=s["offers"][1-state]
    if len(selected)<required or len(opposite)<required:return .1
    if all(value==ch for value in selected) and all(value!=ch for value in opposite):
        return .9
    return .1

def new():
    if len(SESSION)>=len(MODES):raise ValueError("session cap exhausted")
    sid=secrets.token_hex(12)
    mode=MODES[len(SESSION)]
    salt=secrets.token_hex(16)
    s={"mode":mode,"axis":RNG.randrange(2),"flip":RNG.randrange(2),
       "salt":salt,"offers":defaultdict(list),"observed":0,"offered":0,
       "queries":0,"finished":False}
    s["commit"]=sha256(f"{sid}/{mode}/{s['axis']}/{s['flip']}/{salt}".encode()).hexdigest()
    SESSION[sid]=s
    return {"session":sid,"private_rule_commitment":s["commit"],
            "schema":"UNV_EXTERNAL_PARTNER_V1","max_observations":48}

def observe(s,scene):
    state=scene_state(s,scene)
    s["observed"]+=1
    if s["observed"]>48:raise ValueError("observation budget exhausted")
    mode=s["mode"]
    symbol=state^s["flip"]
    if mode=="fixed":symbol=0
    if mode=="random":symbol=RNG.randrange(2)
    if mode=="silent":symbol=None
    pos=RNG.randrange(8,27)
    raw=[]
    for i in range(64):
        noise=[RNG.uniform(-.006,.006),RNG.uniform(-.006,.006)]
        if symbol is not None and pos<=i<pos+7:
            noise[symbol]+=.8
        raw.append([round(v,6) for v in noise])
    return {"trace":raw}

def qualify(s,body,sid):
    s["finished"]=True
    axis=body.get("selected_sensor_axis")
    mapping=body.get("outbound_motifs")
    if (type(axis) is not int or axis not in (0,1) or
            type(mapping) is not list or len(mapping)!=2 or
            sorted(mapping)!=[0,1] or s["offered"]<12):
        result={"status":"INELIGIBLE","holdout_count":0,"mean":None,
                "ablation_drop":None}
    else:
        tests=[]
        for sign_a,sign_b in ((-1,-1),(1,-1),(-1,1),(1,1)):
            scene=[round(sign_a*RNG.uniform(.58,.96),6),
                   round(sign_b*RNG.uniform(.58,.96),6)]
            label=mapping[int(scene[axis]>0)]
            def signal(ch):
                return [[(-.85 if 11<=i<18 and c==ch else 0.0)
                         for c in range(2)] for i in range(64)]
            actual=payoff(s,scene,signal(label),True)
            reversed_=payoff(s,scene,signal(1-label),True)
            tests.append((actual,reversed_))
        passed=all(a>=.75 and a-b>=.5 for a,b in tests)
        result={"status":"HOLDOUT_PASS" if passed else "HOLDOUT_FAIL",
                "holdout_count":len(tests),
                "mean":sum(a for a,_ in tests)/len(tests),
                "ablation_drop":sum(a-b for a,b in tests)/len(tests)}
    record={"session":sid,"mode":s["mode"],"axis":s["axis"],
            "flip":s["flip"],"salt":s["salt"],"commit":s["commit"],
            "observed":s["observed"],"offered":s["offered"],
            "queries":s["queries"],**result}
    with LOG.open("a",encoding="utf-8") as stream:
        stream.write(json.dumps(record,sort_keys=True)+"\n")
    return {**result,"rule_commitment":s["commit"],
            "receipt_sha256":sha256(json.dumps(record,sort_keys=True).encode()).hexdigest(),
            "private_rule_kept_on_peer":True}

class Handler(BaseHTTPRequestHandler):
    server_version="BT2Peer/1"
    def log_message(self,fmt,*args):
        return
    def _reply(self,status,obj):
        blob=json.dumps(obj,separators=(",",":"),sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.send_header("Cache-Control","no-store")
        self.send_header("Content-Length",str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)
    def do_GET(self):
        if self.path=="/health":
            return self._reply(200,{"schema":"UNV_EXTERNAL_PARTNER_V1",
                                    "status":"READY","count":len(SESSION)})
        self._reply(404,{"error":"route_unavailable"})
    def do_POST(self):
        if self.path!="/v1/interaction":
            return self._reply(404,{"error":"route_unavailable"})
        supplied=self.headers.get("X-BT2-Token","")
        if not secrets.compare_digest(supplied,TOKEN):
            return self._reply(403,{"error":"unauthorized"})
        try:
            length=int(self.headers.get("Content-Length","-1"))
            if not 2<=length<=85000:raise ValueError("bounded request size")
            body=json.loads(self.rfile.read(length))
            if type(body) is not dict:raise ValueError("object required")
            op=body.get("op")
            with LOCK:
                if op=="begin":
                    if set(body)!={"op"}:raise ValueError("unsupported begin shape")
                    out=new()
                elif op in ("observe","offer","outcome","qualify"):
                    sid=body.get("session")
                    if type(sid) is not str or sid not in SESSION:
                        raise ValueError("invalid session")
                    s=SESSION[sid]
                    if s["finished"]:raise ValueError("session already finalized")
                    s["queries"]+=1
                    if s["queries"]>250:raise ValueError("query cap exceeded")
                    if op=="qualify":
                        if set(body)!={"op","session","selected_sensor_axis","outbound_motifs"}:
                            raise ValueError("invalid qualification request")
                        out=qualify(s,body,sid)
                    else:
                        expected={"op","session","scene"}
                        if op in ("offer","outcome"):expected.add("signal")
                        if set(body)!=expected:raise ValueError("unexpected input fields")
                        scene=body["scene"]
                        scene_state(s,scene)
                        if op=="observe":
                            out=observe(s,scene)
                        elif op=="offer":
                            channel=wire_signature(body["signal"])
                            if channel is None:raise ValueError("invalid output waveform")
                            state=scene_state(s,scene)
                            s["offers"][state].append(channel)
                            s["offered"]+=1
                            out={"accepted_for_exposure":True}
                        else:
                            out={"environment_feedback":payoff(s,scene,body["signal"])}
                else:
                    raise ValueError("unknown operation")
            self._reply(200,out)
        except (ValueError,TypeError,KeyError,UnicodeDecodeError) as exc:
            self._reply(400,{"error":"request_rejected"})
        except Exception:
            self._reply(500,{"error":"peer_server_error"})

def main():
    if len(TOKEN)<48:raise ValueError("token too weak")
    if not HOME.is_dir():raise ValueError("private root missing")
    os.umask(0o077)
    with ThreadingHTTPServer((HOST,PORT),Handler) as server:
        server.daemon_threads=True
        print(json.dumps({"ready":True,"host":HOST,"port":PORT,
                          "service_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
                          "private_root_mode":oct(HOME.stat().st_mode&0o777),
                          "program":"scripted-peer; NOT unknown intelligence"}),flush=True)
        server.serve_forever(poll_interval=.4)

if __name__=="__main__":
    main()
