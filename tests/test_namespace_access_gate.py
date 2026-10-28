"""Linux namespace custody regressions with mocked bwrap on CI hosts.

Real positive/negative access proof requires separately executed VN2 receipt.
"""
from __future__ import annotations
import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from runs.contact_20261027 import namespace_access_gate as gate

@pytest.fixture
def fixture_paths(tmp_path):
    worker=tmp_path/"worker.py"
    public=tmp_path/"public.json"
    secret=tmp_path/"secret.txt"
    worker.write_text("pass\n")
    public.write_text('{"challenge":"abc","values":[1,2,3,4]}')
    secret.write_text("evaluator-only")
    return worker,public,secret

def test_protection_flags_and_explicit_minimal_mount(monkeypatch,fixture_paths):
    worker,public,secret=fixture_paths
    monkeypatch.setattr(gate.platform,"system",lambda:"Linux")
    monkeypatch.setattr(gate.shutil,"which",lambda n:"/usr/bin/bwrap")
    exists=Path.exists
    monkeypatch.setattr(Path,"exists",lambda p:True if str(p).replace("\\","/") in
                        ("/bin","/usr","/lib","/lib64") else exists(p))
    cmd=gate.command_for(worker,public,secret,"a"*64,12345)
    assert cmd[0]=="/usr/bin/bwrap"
    for flag in ("--unshare-user","--unshare-net","--unshare-pid","--unshare-ipc",
                 "--cap-drop","--clearenv","--ro-bind","--die-with-parent"):
        assert flag in cmd
    assert "--share-net" not in cmd
    assert "--bind" not in cmd
    # The absolute secret path is passed as an adversarial probe, NOT mounted.
    for i,x in enumerate(cmd):
        if x=="--ro-bind":
            assert cmd[i+1]!=str(secret)
    assert ["/usr/bin/python3","-I","/app/probe.py"]==cmd[
        cmd.index("/usr/bin/python3"):cmd.index("/usr/bin/python3")+3]

def test_fail_closed_when_bwrap_unavailable(monkeypatch,fixture_paths):
    monkeypatch.setattr(gate.platform,"system",lambda:"Linux")
    monkeypatch.setattr(gate.shutil,"which",lambda _:None)
    with pytest.raises(ValueError,match="unavailable"):
        gate.command_for(*fixture_paths,"a"*64,12345)

def test_different_public_private_required(monkeypatch,fixture_paths):
    monkeypatch.setattr(gate.platform,"system",lambda:"Linux")
    monkeypatch.setattr(gate.shutil,"which",lambda _:"bwrap")
    worker,public,secret=fixture_paths
    with pytest.raises(ValueError,match="private and public"):
        gate.command_for(worker,public,public,"a"*64,12345)

def test_runtime_is_linux_only(monkeypatch,fixture_paths):
    monkeypatch.setattr(gate.platform,"system",lambda:"Windows")
    with pytest.raises(ValueError,match="Linux host"):
        gate.evaluate(fixture_paths[0])

def test_worker_nonzero_exit_rejected(monkeypatch):
    monkeypatch.setattr(gate.subprocess,"run",lambda *a,**k:
        SimpleNamespace(returncode=3,stdout="{}",stderr="bad"))
    with pytest.raises(ValueError,match="failed closed"):
        gate.checked_run(["command"])

@pytest.mark.parametrize("output",['{}','not json',
    '{"public_result_sha256":"x","private_canary_read":1,"host_loopback_reachable":true,"network_namespace":"net:[1]","peer_private_home_mounted":false}'])
def test_invalid_subprocess_evidence_refused(monkeypatch,output):
    monkeypatch.setattr(gate.subprocess,"run",lambda *a,**k:
        SimpleNamespace(returncode=0,stdout=output,stderr=""))
    with pytest.raises(ValueError):
        gate.checked_run(["command"])

def test_no_fallback_after_subprocess_os_error(monkeypatch):
    def deny(*args,**kwargs):
        raise PermissionError("kernel namespace denied")
    monkeypatch.setattr(gate.subprocess,"run",deny)
    with pytest.raises(PermissionError):
        gate.checked_run(["command"])

def test_fixed_claim_scope():
    assert gate.CLAIM=="ONE_FIXED_WORKER_FILESYSTEM_NETWORK_NEGATIVE_ACCESS_ONLY"
    assert gate.MAX_TIMEOUT<=7
