"""Cross-host transport guards. No real network calls in CI."""
from __future__ import annotations
import json
from types import SimpleNamespace
import pytest

from runs.contact_20261027.crosshost_trial import (
    Channel,RemotePartner,run_one,validate_endpoint,MAX_BYTES
)

@pytest.mark.parametrize("endpoint",[
    "http://8.8.8.8:18047", "https://100.95.37.34:18047",
    "http://100.95.37.34:80","http://100.95.37.34:18047/private",
    "http://admin@100.95.37.34:18047","http://localhost:18047",
    "file:///etc/passwd","http://100.95.37.34:18047?token=x",
])
def test_non_tailnet_or_unauthorized_destinations_fail(endpoint):
    with pytest.raises(ValueError):
        validate_endpoint(endpoint)

def test_valid_private_endpoint():
    assert validate_endpoint("http://100.95.37.34:18047")==(
        "http://100.95.37.34:18047/v1/interaction")

def test_token_validation():
    with pytest.raises(ValueError,match="token"):
        Channel("http://100.95.37.34:18047","short")

def test_transport_size_limit_before_network(monkeypatch):
    channel=Channel("http://100.95.37.34:18047","x"*64)
    with pytest.raises(ValueError,match="too large"):
        channel.send({"payload":"a"*(MAX_BYTES+1)})

def test_peer_rejection_cannot_become_success():
    class EmptyChannel:
        def send(self,req):return {"status":"HOLDOUT_PASS"}
    with pytest.raises(ValueError,match="initiation"):
        run_one(EmptyChannel())

def test_invalid_remote_session():
    channel=Channel("http://100.95.37.34:18047","x"*64)
    with pytest.raises(ValueError,match="session"):
        RemotePartner(channel,"misformatted")

def test_malformed_sensor_response_refused():
    class WrongChannel:
        def send(self,payload):
            return {"trace":"not numeric"}
    subject=RemotePartner(WrongChannel(),"a"*24)
    with pytest.raises(ValueError,match="malformed"):
        subject.observe((.6,-.6))

def test_host_proof_is_not_trusted_without_matching_commitment():
    class ForgedQualification:
        def __init__(self):self.requests=[]
        def send(self,req):
            self.requests.append(req)
            if req["op"]=="begin":
                return {"session":"a"*24,"private_rule_commitment":"b"*64,
                        "schema":"UNV_EXTERNAL_PARTNER_V1","max_observations":48}
            if req["op"]=="observe":
                return {"trace":[[0.0,0.0]]*64}
            if req["op"]=="qualify":
                return {"status":"HOLDOUT_PASS","holdout_count":4,
                        "mean":.9,"ablation_drop":.8,"rule_commitment":"c"*64,
                        "receipt_sha256":"d"*64,"private_rule_kept_on_peer":True}
            raise ValueError("unexpected test call")
    with pytest.raises(ValueError,match="commitment"):
        run_one(ForgedQualification())
