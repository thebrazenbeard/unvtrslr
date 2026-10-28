"""Linux-only evaluator/broker for an actual namespaced UNVTRSLR learner.

Trusted evaluator owns partner rule and holdouts; learner gets only bounded
JSONL observation/offer/outcome operations over pipes. Not independent alien
or human communication, and not arbitrary untrusted-code containment.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from hashlib import sha256
import json
import math
import os
from pathlib import Path
from random import Random
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time

SCENES=((-0.6,-0.6),(0.6,-0.6),(-0.6,0.6),(0.6,0.6))
MODES=("responsive","slow","silent","fixed","random","constant_reward","drift")
EXPECTED={"responsive":"HOLDOUT_PASS","slow":"HOLDOUT_PASS",
          "silent":"INELIGIBLE","fixed":"INELIGIBLE",
          "random":"INELIGIBLE","constant_reward":"INELIGIBLE",
          "drift":"HOLDOUT_FAIL"}
MAX_LINE=18000
MAX_REQUESTS=100
MAX_SECONDS=12

class PrivatePartner:
    def __init__(self,seed,mode):
        if mode not in MODES:raise ValueError("unsupported private mode")
        self.rng=Random(seed)
        self.mode=mode
        self.axis=self.rng.randrange(2)
        self.flip=self.rng.randrange(2)
        self.exposures=defaultdict(list)
        self.observe_count=0
    def state(self,scene,holdout=False):
        axis=1-self.axis if holdout and self.mode=="drift" else self.axis
        return int(scene[axis]>0)
    def observe(self,scene):
        self.observe_count+=1
        state=self.state(scene)
        marker=state^self.flip
        if self.mode=="fixed":marker=0
        if self.mode=="random":marker=self.rng.randrange(2)
        if self.mode=="silent":marker=None
        start=self.rng.randrange(7,27)
        return [[round(self.rng.uniform(-.006,.006)+
                   (.8 if i>=start and i<start+7 and marker==ch else 0),6)
                  for ch in range(2)] for i in range(64)]
    def offer(self,scene,signal):
        ch=waveform_channel(signal)
        if ch is None:raise ValueError("invalid outbound waveform")
        self.exposures[self.state(scene)].append(ch)
    def outcome(self,scene,signal,holdout=False):
        if self.mode=="constant_reward":return .9
        if self.mode=="silent":return .1
        state=self.state(scene,holdout)
        ch=waveform_channel(signal)
        if ch is None:return .1
        required=9 if self.mode=="slow" else 3
        selected=self.exposures[state]
        other=self.exposures[1-state]
        return (.9 if len(selected)>=required and len(other)>=required
                and all(x==ch for x in selected)
                and all(x!=ch for x in other) else .1)

def validate_scene(scene):
    if type(scene) is not list or len(scene)!=2 or any(
        type(v) not in (float,int) or not math.isfinite(v)
        or not -1<=v<=1 for v in scene):
        raise ValueError("invalid scene")
    return tuple(scene)

def waveform_channel(signal):
    if type(signal) is not list or len(signal)!=64 or any(
        type(row) is not list or len(row)!=2 or any(
            type(v) not in (int,float) or not math.isfinite(v)
            or abs(v)>2 for v in row) for row in signal):
        return None
    summed=[sum(abs(row[ch]) for row in signal) for ch in range(2)]
    biggest=0 if summed[0]>summed[1] else 1
    return biggest if summed[biggest]>=4 and summed[1-biggest]<.8 else None

def outbound(label):
    if type(label) is not int or label not in (0,1):
        raise ValueError("invalid frozen symbol")
    return [[(-.85 if 11<=i<18 and ch==label else 0.0)
             for ch in range(2)] for i in range(64)]

def qualify(private,model):
    if (type(model) is not dict or
        model.get("status")!="PROPOSAL_CONFIRMED_TRAINING_ONLY"):
        return {"status":"INELIGIBLE","holdout_count":0,"advantage":None}
    axis=model.get("selected_sensor_axis")
    mapping=model.get("outbound_motifs")
    if type(axis) is not int or axis not in (0,1) or type(mapping) is not list or sorted(mapping)!=[0,1]:
        raise ValueError("incoherent fitted model")
    results=[]
    for a,b in ((-1,-1),(1,-1),(-1,1),(1,1)):
        scene=(a*private.rng.uniform(.70,.94), b*private.rng.uniform(.70,.94))
        symbol=mapping[int(scene[axis]>0)]
        valid=private.outcome(scene,outbound(symbol),True)
        control=private.outcome(scene,outbound(1-symbol),True)
        results.append((valid,control))
    passed=all(x>=.75 and x-y>=.5 for x,y in results)
    return {"status":"HOLDOUT_PASS" if passed else "HOLDOUT_FAIL",
            "holdout_count":len(results),
            "advantage":round(sum(x-y for x,y in results)/len(results),6)}

def sandbox_argv(repo,secret):
    if sys.platform!="linux" or not shutil.which("bwrap"):
        raise ValueError("Linux Bubblewrap required; fail closed")
    root=repo/"src"/"unvtrslr"
    worker=repo/"runs"/"contact_20261027"/"isolated_learner_worker.py"
    files=(worker,root/"contact_negotiation.py",root/"signal_discovery.py")
    if not all(p.is_file() for p in files) or not secret.is_file():
        raise ValueError("missing source/canary material")
    roots=("/usr","/bin","/lib","/lib64")
    if any(not Path(r).exists() for r in roots):
        raise ValueError("missing read-only Linux runtime root")
    args=[shutil.which("bwrap"),"--unshare-user","--unshare-pid",
         "--unshare-net","--unshare-ipc","--unshare-uts",
         "--die-with-parent","--new-session","--cap-drop","ALL",
         "--clearenv","--setenv","PATH","/usr/bin",
         "--setenv","HOME","/tmp"]
    for r in roots:args.extend(("--ro-bind",r,r))
    args+=["--proc","/proc","--dev","/dev","--tmpfs","/tmp",
           "--dir","/app","--dir","/app/unvtrslr",
           "--ro-bind",str(worker),"/app/isolated_learner_worker.py",
           "--ro-bind",str(root/"contact_negotiation.py"),"/app/unvtrslr/contact_negotiation.py",
           "--ro-bind",str(root/"signal_discovery.py"),"/app/unvtrslr/signal_discovery.py",
           "--chdir","/app","/usr/bin/python3","-I","-B",
           "/app/isolated_learner_worker.py",str(secret)]
    return args
def session(repo:Path,seed:int,mode:str):
    private=PrivatePartner(seed,mode)
    with tempfile.TemporaryDirectory(prefix="unv-broker-private-",dir=str(Path.home())) as hidden:
        secret=Path(hidden)/"evaluator_secret"
        secret.write_bytes(os.urandom(48))
        secret.chmod(0o600)
        argv=sandbox_argv(repo,secret)
        host_ns=os.readlink("/proc/self/ns/net")
        p=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL,bufsize=1,text=True,
                           start_new_session=True,close_fds=True)
        final=None
        attested=False
        count=0
        deadline=time.monotonic()+MAX_SECONDS
        try:
            while final is None:
                remain=deadline-time.monotonic()
                if remain<=0 or count>=MAX_REQUESTS:
                    raise ValueError("worker request/time budget exceeded")
                if not select.select([p.stdout],[],[],remain)[0]:
                    raise ValueError("worker response timed out")
                line=p.stdout.readline(MAX_LINE+1)
                if not line or len(line)>MAX_LINE:
                    raise ValueError("worker ended or emitted oversized message")
                try:request=json.loads(line)
                except ValueError:raise ValueError("malformed worker request") from None
                if type(request) is not dict:
                    raise ValueError("worker request must be object")
                op=request.get("op")
                count+=1
                if op=="attest" and not attested and count==1:
                    expected={"op","canary_visible","loopback_reachable","network_namespace"}
                    ns=request.get("network_namespace")
                    if (set(request)!=expected or
                          type(request["canary_visible"]) is not bool or
                          type(request["loopback_reachable"]) is not bool or
                          type(ns) is not str or not ns.startswith("net:[")
                          or not ns.endswith("]") or not ns[5:-1].isdigit()
                          or request["canary_visible"] or request["loopback_reachable"]
                          or ns==host_ns):
                        raise ValueError("worker isolation attestation failed")
                    attested=True
                    response={"ok":True,"attested":True}
                elif op in ("observe","offer","outcome") and attested:
                    expected={"op","scene"}|({"signal"} if op!="observe" else set())
                    if set(request)!=expected:
                        raise ValueError("extraneous learner API fields")
                    scene=validate_scene(request["scene"])
                    if op=="observe":
                        if private.observe_count>=48:raise ValueError("observation cap")
                        response={"ok":True,"trace":private.observe(scene)}
                    elif op=="offer":
                        if waveform_channel(request["signal"]) is None:
                            raise ValueError("invalid waveform proposal")
                        private.offer(scene,request["signal"])
                        response={"ok":True,"accepted":True}
                    else:
                        response={"ok":True,"feedback":private.outcome(scene,request["signal"])}
                elif op=="final" and attested:
                    if set(request)!={"op","result"}:
                        raise ValueError("invalid final worker shape")
                    final=request["result"]
                    if type(final) is not dict or final.get("claim_ceiling")!=(
                            "SYNTHETIC_INTERACTIVE_OPERATIONAL_CONVENTION_ONLY"):
                        raise ValueError("invalid worker claim ceiling")
                    response={"ok":True,"terminal":True}
                else:
                    raise ValueError("illegal negotiation transition")
                p.stdin.write(json.dumps(response,separators=(",",":"))+"\n")
                p.stdin.flush()
            p.stdin.close()
            p.wait(timeout=max(.5,deadline-time.monotonic()))
            if p.returncode!=0:
                raise ValueError("worker terminated unsuccessfully")
        finally:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGKILL)
                except ProcessLookupError:pass
                p.wait()
            if p.stdin and not p.stdin.closed:p.stdin.close()
            if p.stdout:p.stdout.close()
    result=qualify(private,final)
    expected=EXPECTED[mode]
    return {"mode":mode,"seed":seed,"worker_status":final.get("status"),
            "private_heldout":result,
            "expected":expected,"matched":result["status"]==expected,
            "attested":attested,"rpc_count":count,
            "worker_sha256":sha256((repo/"runs"/"contact_20261027"/"isolated_learner_worker.py").read_bytes()).hexdigest(),
            "namespaced_known_source":True,"independent_peer":False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--report-out",type=Path,required=True)
    parser.add_argument("--seed",type=int,default=73)
    ap=parser.parse_args()
    if ap.report_out.exists():raise ValueError("refuse report overwrite")
    cases=[session(ap.repo,ap.seed+i*31,mode) for i,mode in enumerate(MODES)]
    result={"schema":"UNV_NAMESPACED_REAL_LEARNER_WITH_RPC_BROKER_V1",
        "source":"tracked UNVTRSLR Python learner, not surrogate canary worker",
        "worker_isolation":"Linux bwrap read-only explicit files, separate network/mount/pid",
        "claim_ceiling":"SYNTHETIC_BROKERED_OPERATIONAL_CONTACT_ONLY",
        "private_partner_and_heldouts_outside_worker_mount":True,
        "actual_unknown_intelligence":False,
        "os_security_against_arbitrary_malicious_models_verified":False,
        "cases":cases,"all_expected_met":all(c["matched"] for c in cases)}
    ap.report_out.parent.mkdir(parents=True,exist_ok=True)
    ap.report_out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"case_count":len(cases),"matched":sum(c["matched"] for c in cases),
        "statuses":{c["mode"]:c["private_heldout"]["status"] for c in cases}},sort_keys=True))

if __name__=="__main__":
    main()
