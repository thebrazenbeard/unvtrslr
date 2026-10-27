"""Adversarial checks for experimenter-framed continuous-response bootstrap."""
from __future__ import annotations
from dataclasses import replace
import math

import pytest

from runs.bootstrap_20261027.run import EXPECTED,MODES,SEEDS,generate,score
from unvtrslr.bootstrap_contingency import (
    CLAIM, RawProbeObservation, screen_bootstrap_contingency,
)

@pytest.mark.parametrize("seed",SEEDS)
@pytest.mark.parametrize("mode",MODES)
def test_controls_distinguish_contingency_from_shortcuts(seed,mode):
    report=score(seed,mode)
    assert report["control_pass"]
    assert report["result"]["status"]==EXPECTED[mode]
    assert report["result"]["os_isolation_verified"] is False
    assert report["result"]["semantic_qualification"] is False
    assert report["result"]["claim_ceiling"]==CLAIM

def test_positive_selects_probe_and_generalizes_across_unseen_settings():
    train,holdout=generate(17,"contingent")
    result=screen_bootstrap_contingency(train,holdout)
    assert result.selected_probe=="probe_b"
    assert result.fitted_settings==("c0","c1")
    assert result.holdout_settings==("c2","c3")
    assert result.train_effects[1][1]>.6
    assert result.holdout_effects[1][1]>.6

def test_absent_response_no_spurious_semantic_claim():
    result=screen_bootstrap_contingency(*generate(17,"no_response"))
    assert result.selected_probe is None
    assert result.semantic_qualification is False

def test_context_leakage_fails_holdout():
    result=screen_bootstrap_contingency(*generate(17,"training_only"))
    assert result.selected_probe=="probe_b"
    assert result.status=="HELDOUT_CONTINGENCY_NOT_REPLICATED"

def test_unmatched_triples_are_refused():
    train,holdout=generate(17,"contingent")
    with pytest.raises(ValueError,match="unmatched"):
        screen_bootstrap_contingency(train[1:],holdout)

def test_overlap_setting_is_refused():
    train,holdout=generate(17,"contingent")
    tampered=[replace(r,setting="c0") if r.setting=="c2" else r for r in holdout]
    with pytest.raises(ValueError,match="unseen settings"):
        screen_bootstrap_contingency(train,tampered)

def test_overlap_block_id_is_refused():
    train,holdout=generate(17,"contingent")
    tampered=[replace(r,block=r.block.replace("c2","c0").replace("c3","c1"))
              for r in holdout]
    with pytest.raises(ValueError,match="block overlap"):
        screen_bootstrap_contingency(train,tampered)

def test_order_confound_is_refused():
    train,holdout=generate(17,"contingent")
    reordered=[replace(r,order={"sham":0,"probe_a":1,"probe_b":2}[r.probe])
               for r in train]
    with pytest.raises(ValueError,match="confounded"):
        screen_bootstrap_contingency(reordered,holdout)

@pytest.mark.parametrize("bad", [float("nan"),float("inf"),100.0,True])
def test_raw_trace_is_finite_bounded_numeric(bad):
    train,holdout=generate(17,"contingent")
    r=train[0]
    newtrace=(bad,)+r.trace[1:]
    with pytest.raises(ValueError,match="malformed"):
        screen_bootstrap_contingency([replace(r,trace=newtrace)]+train[1:],holdout)

def test_do_not_accept_unsegmented_or_arbitrary_trace_lengths():
    train,holdout=generate(17,"contingent")
    with pytest.raises(ValueError,match="malformed"):
        screen_bootstrap_contingency([replace(train[0],trace=train[0].trace[:8])]+train[1:],holdout)

def test_positive_negative_control_receipts_reproduce():
    for mode in MODES:
        assert score(41,mode)==score(41,mode)

def test_uncontrolled_message_or_ontology_not_in_api():
    train,_=generate(17,"contingent")
    assert set(vars(train[0]))=={"block","setting","probe","order","trace"}
    assert "target_label" not in vars(train[0])
    assert "semantic_intent" not in vars(train[0])
    assert "receiver_identity" not in vars(train[0])
