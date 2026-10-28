"""Fail-closed Linux bwrap custody test, not a general malicious-code sandbox.

Requires working Linux user/mount/PID/network namespaces. This gate tests a
read-only, fixed allowlist against canary and loopback attacks, with *positive*
unsandboxed controls. It intentionally never runs unknown code.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import platform
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile

SCHEMA="UNV_LINUX_BWRAP_ACCESS_GATE_V1"
CLAIM="ONE_FIXED_WORKER_FILESYSTEM_NETWORK_NEGATIVE_ACCESS_ONLY"
MAX_TIMEOUT=7

def command_for(worker:Path,public:Path,secret:Path,secret_digest:str,port:int):
    """Explicit read-only host roots and one public-file bind. NO home bind."""
    if platform.system()!="Linux":
        raise ValueError("Linux-only fail-closed namespace gate")
    executable=shutil.which("bwrap")
    if not executable:raise ValueError("bwrap unavailable")
    if any(not p.is_file() for p in (worker,public,secret)):
        raise ValueError("missing gate input")
    if worker.resolve()==secret.resolve() or public.resolve()==secret.resolve():
        raise ValueError("private and public files must differ")
    if len(secret_digest)!=64 or not all(c in "0123456789abcdef" for c in secret_digest):
        raise ValueError("invalid private digest")
    roots=("--ro-bind","/usr","/usr",
           "--ro-bind","/bin","/bin",
           "--ro-bind","/lib","/lib",
           "--ro-bind","/lib64","/lib64")
    for i in range(0,len(roots),3):
        if not Path(roots[i+1]).exists():
            raise ValueError("runtime root unavailable")
    return [executable,"--unshare-user","--unshare-pid","--unshare-net",
       "--unshare-ipc","--unshare-uts","--die-with-parent","--new-session",
       "--cap-drop","ALL","--clearenv","--setenv","PATH","/usr/bin",
       "--setenv","HOME","/tmp",*roots,
       "--proc","/proc","--dev","/dev","--tmpfs","/tmp","--dir","/app",
       "--ro-bind",str(worker),"/app/probe.py",
       "--ro-bind",str(public),"/app/public.json","--chdir","/app",
       "/usr/bin/python3","-I","/app/probe.py",
       "--public","/app/public.json","--secret",str(secret),
       "--secret-sha256",secret_digest,"--network-port",str(port)]

def checked_run(argv:list[str]):
    run=subprocess.run(argv,capture_output=True,text=True,
                       timeout=MAX_TIMEOUT,check=False,close_fds=True,
                       stdin=subprocess.DEVNULL)
    if run.returncode!=0 or len(run.stdout)>4096 or len(run.stderr)>4096:
        raise ValueError("worker/sandbox failed closed")
    try:record=json.loads(run.stdout)
    except ValueError:raise ValueError("malformed worker output") from None
    expected={"public_result_sha256","private_canary_read",
              "host_loopback_reachable","network_namespace",
              "peer_private_home_mounted"}
    if type(record) is not dict or set(record)!=expected:
        raise ValueError("unexpected worker output")
    if (type(record["private_canary_read"]) is not bool or
        type(record["host_loopback_reachable"]) is not bool or
        type(record["peer_private_home_mounted"]) is not bool):
        raise ValueError("malformed worker fields")
    return record

def evaluate(worker:Path):
    if platform.system()!="Linux":raise ValueError("Linux host required")
    if not worker.is_file():raise ValueError("worker missing")
    with tempfile.TemporaryDirectory(prefix="unv-private-canary-",dir=str(Path.home())) as temp:
        private=Path(temp)/"evaluator_only.txt"
        private.write_bytes(secrets.token_bytes(48))
        private.chmod(0o600)
        hidden_digest=sha256(private.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="unv-public-test-") as public_dir:
            public=Path(public_dir)/"public.json"
            challenge=secrets.token_hex(16)
            public.write_text(json.dumps({"challenge":challenge,"values":[17,3,2,9]}),
                              encoding="utf-8")
            expected=sha256((challenge+":31").encode()).hexdigest()
            with socket.socket() as listener:
                listener.bind(("127.0.0.1",0))
                listener.listen(5)
                port=listener.getsockname()[1]
                prefix=["--secret",str(private),"--secret-sha256",hidden_digest,
                        "--network-port",str(port)]
                # Positive exposure outside namespaces proves the probes are not
                # simply broken or aimed at a nonexistent canary/network.
                host=checked_run([sys.executable,str(worker),"--public",str(public),*prefix])
                isolated=checked_run(command_for(worker,public,private,hidden_digest,port))
            host_correct=(host["public_result_sha256"]==expected
                and host["private_canary_read"] and host["host_loopback_reachable"])
            isolated_correct=(isolated["public_result_sha256"]==expected
                and not isolated["private_canary_read"]
                and not isolated["host_loopback_reachable"]
                and not isolated["peer_private_home_mounted"]
                and isolated["network_namespace"]!=host["network_namespace"])
            if not host_correct or not isolated_correct:
                raise ValueError("namespace canary gate did not qualify")
            return {"schema":SCHEMA,"status":"CONTROLLED_NAMESPACE_ACCESS_GATE_PASS",
                "claim_ceiling":CLAIM,
                "bwrap_executable":shutil.which("bwrap"),
                "worker_sha256":sha256(worker.read_bytes()).hexdigest(),
                "host_control":{"public_compute":True,"private_read":True,
                                "network_reachable":True},
                "sandbox_test":{"public_compute":True,"private_read":False,
                                "network_reachable":False,"home_mounted":False,
                                "network_namespace_distinct":True},
                "independent_third_party_verified":False,
                "host_kernel_protection_against_malicious_code_proven":False,
                "real_partner_causality_proven":False}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--worker",type=Path,required=True)
    ap.add_argument("--report-out",type=Path,required=True)
    a=ap.parse_args()
    if a.report_out.exists():
        raise ValueError("refusing evidence overwrite")
    evidence=evaluate(a.worker)
    a.report_out.parent.mkdir(parents=True,exist_ok=True)
    a.report_out.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(evidence,sort_keys=True))

if __name__=="__main__":
    main()
