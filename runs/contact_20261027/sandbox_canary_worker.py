"""Adversarial sandbox worker: positive public computation and forbidden probes.

Only results booleans exit this test. Does not run any partner or evaluator
business logic; do not mistake this test for production isolation proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket

def attempt_private(path: str, digest: str):
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
    except (OSError, ValueError):
        return False

def attempt_network(port: int):
    try:
        with socket.create_connection(("127.0.0.1",port),timeout=.35):
            return True
    except OSError:
        return False

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--public",required=True)
    p.add_argument("--secret",required=True)
    p.add_argument("--secret-sha256",required=True)
    p.add_argument("--network-port",type=int,required=True)
    a=p.parse_args()
    request=json.loads(Path(a.public).read_text(encoding="utf-8"))
    if set(request)!={"challenge","values"} or type(request["challenge"]) is not str:
        raise ValueError("invalid public input")
    vals=request["values"]
    if type(vals) is not list or len(vals)!=4 or any(type(x) is not int for x in vals):
        raise ValueError("invalid public values")
    digest=hashlib.sha256((request["challenge"]+":"+str(sum(vals))).encode()).hexdigest()
    try:net_ns=os.readlink("/proc/self/ns/net")
    except OSError:net_ns=None
    print(json.dumps({"public_result_sha256":digest,
        "private_canary_read":attempt_private(a.secret,a.secret_sha256),
        "host_loopback_reachable":attempt_network(a.network_port),
        "network_namespace":net_ns,
        "peer_private_home_mounted":Path(a.secret).parent.parent.exists()},
        sort_keys=True))
if __name__=="__main__":main()
