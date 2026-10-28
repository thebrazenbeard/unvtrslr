"""Fail-closed tests for the Linux namespaced learner/broker boundary."""
from __future__ import annotations
from pathlib import Path
from types import SimpleNamespace
import pytest
from runs.contact_20261027 import isolated_exchange as gate

def test_known_synthetic_negative_claim_ceiling():
    assert gate.MAX_REQUESTS<=100
    assert gate.MAX_SECONDS<=12
    assert gate.EXPECTED["constant_reward"]=="INELIGIBLE"
    assert gate.EXPECTED["drift"]=="HOLDOUT_FAIL"

@pytest.mark.parametrize("raw",[
    [],[True,0],[float("nan"),0],[2,0],
    [0,0,0],["0","0"],None
])
def test_scene_rejects_bad_observations(raw):
    with pytest.raises(ValueError,match="scene"):
        gate.validate_scene(raw)

def test_waveform_requires_bounded_finite_channel():
    assert gate.waveform_channel(gate.outbound(0))==0
    assert gate.waveform_channel(gate.outbound(1))==1
    assert gate.waveform_channel([[0,0]]*64) is None
    assert gate.waveform_channel([[float("inf"),0]]*64) is None
    assert gate.waveform_channel([[0,0]]*63) is None

def test_hidden_heldout_not_sent_to_frozen_learner():
    private=gate.PrivatePartner(17,"responsive")
    for scene in gate.SCENES:
        for _ in range(3):
            private.offer(scene,gate.outbound(int(scene[private.axis]>0)))
    model={"status":"PROPOSAL_CONFIRMED_TRAINING_ONLY",
           "selected_sensor_axis":private.axis,"outbound_motifs":[0,1]}
    result=gate.qualify(private,model)
    assert result["status"]=="HOLDOUT_PASS"
    assert result["advantage"]==.8

def test_constant_reward_rejected_by_wrong_signal():
    private=gate.PrivatePartner(17,"constant_reward")
    model={"status":"PROPOSAL_CONFIRMED_TRAINING_ONLY",
           "selected_sensor_axis":0,"outbound_motifs":[0,1]}
    assert gate.qualify(private,model)["status"]=="HOLDOUT_FAIL"

def test_drift_changes_heldout_reference():
    private=gate.PrivatePartner(17,"drift")
    axis=private.axis
    for scene in gate.SCENES:
        for _ in range(3):
            private.offer(scene,gate.outbound(int(scene[axis]>0)))
    model={"status":"PROPOSAL_CONFIRMED_TRAINING_ONLY",
           "selected_sensor_axis":axis,"outbound_motifs":[0,1]}
    assert gate.qualify(private,model)["status"]=="HOLDOUT_FAIL"

def test_no_unauthorized_private_learner_files(tmp_path,monkeypatch):
    worker=tmp_path/"runs"/"contact_20261027"/"isolated_learner_worker.py"
    worker.parent.mkdir(parents=True)
    worker.write_text("pass")
    root=tmp_path/"src"/"unvtrslr"
    root.mkdir(parents=True)
    for p in ("signal_discovery.py","contact_negotiation.py"):
        (root/p).write_text("pass")
    private=tmp_path/"secret.txt"
    private.write_text("hidden")
    monkeypatch.setattr(gate.sys,"platform","linux")
    monkeypatch.setattr(gate.shutil,"which",lambda _: "/usr/bin/bwrap")
    original=Path.exists
    monkeypatch.setattr(Path,"exists",lambda p: True if str(p).replace("\\","/")
                        in ("/usr","/bin","/lib","/lib64") else original(p))
    argv=gate.sandbox_argv(tmp_path,private)
    assert "--unshare-net" in argv and "--unshare-pid" in argv
    assert "--cap-drop" in argv and "--clearenv" in argv
    assert "--share-net" not in argv
    assert "--bind" not in argv
    assert "/app/isolated_learner_worker.py" in argv
    assert "/app/unvtrslr/contact_negotiation.py" in argv
    assert str(private) in argv
    assert not any(argv[i]=="--ro-bind" and argv[i+1]==str(private)
                   for i in range(len(argv)-1))

def test_fails_closed_without_linux(monkeypatch,tmp_path):
    monkeypatch.setattr(gate.sys,"platform","win32")
    with pytest.raises(ValueError,match="Linux"):
        gate.sandbox_argv(tmp_path,tmp_path/"secret")
