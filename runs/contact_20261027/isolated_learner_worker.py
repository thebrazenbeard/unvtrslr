"""A narrowly scoped learner inside an OS-namespaced worker; trusted source only.

JSONL request/reply. No peer code, simulator truth, target labels, or network
socket is mounted inside the worker. Not an arbitrary-model security boundary.
"""
from __future__ import annotations
from dataclasses import asdict
import json
import os
from pathlib import Path
import socket
import sys

sys.path.insert(0, "/app")  # explicit minimal stdlib-only package staging
from unvtrslr.contact_negotiation import negotiate

MAX_MESSAGE=18000

def send(record: dict) -> dict:
    raw=json.dumps(record,sort_keys=True,separators=(",",":"))
    if len(raw)>MAX_MESSAGE:
        raise ValueError("outbound worker message exceeds contract")
    sys.stdout.write(raw+"\n")
    sys.stdout.flush()
    reply=sys.stdin.readline(MAX_MESSAGE+1)
    if not reply or len(reply)>MAX_MESSAGE:
        raise ValueError("missing or oversized parent reply")
    obj=json.loads(reply)
    if type(obj) is not dict or obj.get("ok") is not True:
        raise ValueError("parent rejected worker message")
    return obj

class FramedPartner:
    def observe(self,scene):
        reply=send({"op":"observe","scene":list(scene)})
        trace=reply.get("trace")
        if type(trace) is not list or len(trace)!=64:
            raise ValueError("invalid 64-frame observation")
        return tuple(tuple(row) for row in trace)
    def offer(self,scene,signal):
        reply=send({"op":"offer","scene":list(scene),
                    "signal":[list(row) for row in signal]})
        if reply.get("accepted") is not True:
            raise ValueError("peer rejected offered signal")
    def outcome(self,scene,signal):
        reply=send({"op":"outcome","scene":list(scene),
                    "signal":[list(row) for row in signal]})
        return reply.get("feedback")

def main():
    if len(sys.argv)!=2:
        raise ValueError("worker requires private canary path argument")
    secret=Path(sys.argv[1])
    canary_visible=secret.exists()
    try:
        with socket.create_connection(("127.0.0.1",22377),timeout=.15):
            loopback_reachable=True
    except OSError:
        loopback_reachable=False
    network_namespace=os.readlink("/proc/self/ns/net")
    evidence=send({"op":"attest","canary_visible":canary_visible,
                   "loopback_reachable":loopback_reachable,
                   "network_namespace":network_namespace})
    if not evidence.get("attested"):
        raise ValueError("custody denied")
    state=negotiate(FramedPartner())
    report=asdict(state)
    response=send({"op":"final","result":report})
    if response.get("terminal") is not True:
        raise ValueError("terminal receipt rejected")

if __name__=="__main__":
    main()
