"""Adversarial synthetic contact qualification: no human/unknown-intelligence claims."""
from __future__ import annotations
from dataclasses import replace
import math
from random import Random
import pytest
from runs.contact_20261027.run import (
    SEEDS,MODES,EXPECTED,PrivateSyntheticPartner,evaluate,evaluate_heldout,HELDOUT,raw_stream
)
from unvtrslr.contact_negotiation import (
    SCENES,CEILING,_fit_relation,_next_scene,_outbound_symbol,negotiate
)
from unvtrslr.signal_discovery import (
    CLAIM,cosine,discover,fingerprint,recognize,validate_stream
)

@pytest.mark.parametrize("seed",SEEDS)
@pytest.mark.parametrize("mode",MODES)
def test_synthetic_interactive_partner_controls(seed,mode):
    r=evaluate(seed,mode)
    assert r["observed"]["status"]==EXPECTED[mode]
    assert r["control_pass"]
    assert r["observed"]["claim_ceiling"]==CEILING
    assert not r["observed"]["actual_unknown_intelligence_contacted"]
    assert not r["observed"]["universal_semantics"]

@pytest.mark.parametrize("seed",SEEDS)
@pytest.mark.parametrize("kind,status",[
 ("candidate","RECURRENT_CANDIDATE_UNINTERPRETED"),
 ("noise","NO_RECURRENT_CANDIDATE"),
 ("periodic","PERIODIC_REGULARITY_UNINTERPRETED"),
])
def test_unsegmented_discovery_null_vs_periodic(seed,kind,status):
    record=discover(raw_stream(seed,kind))
    assert record.status==status
    assert record.claim_ceiling==CLAIM
    assert not record.intent_inferred and not record.semantics_inferred
    if kind=="candidate":
        assert len(record.recurring_motifs)>=2
        assert len(record.events)>=10

def test_positive_contact_learns_unknown_axis_and_reciprocal_signal():
    partner=PrivateSyntheticPartner(107,"responsive")
    fitted=negotiate(partner)
    assert fitted.status=="PROPOSAL_CONFIRMED_TRAINING_ONLY"
    assert fitted.heldout_success is None and fitted.withheld_contexts==0
    result=evaluate_heldout(partner,fitted)
    assert result.selected_sensor_axis==partner.axis==0
    assert result.observed_motifs==2
    assert result.training_interactions>=12
    assert result.proposed_signals==12
    assert result.heldout_success==.9 and result.withheld_contexts==4

def test_no_message_partner_abstains_before_new_waveforms():
    partner=PrivateSyntheticPartner(17,"silent")
    result=negotiate(partner)
    assert result.status=="NO_DECODABLE_CANDIDATE"
    assert result.proposed_signals==0
    assert result.heldout_success is None

def test_independent_emissions_do_not_get_operational_credit():
    partner=PrivateSyntheticPartner(73,"independent")
    result=negotiate(partner)
    assert result.status=="NO_IDENTIFIABLE_SENSOR_RELATION"
    assert result.proposed_signals==0

def test_partner_remap_fails_holdout():
    partner=PrivateSyntheticPartner(107,"partner_drift")
    result=evaluate_heldout(partner,negotiate(partner))
    assert result.status=="RECIPROCAL_CONVENTION_NOT_REPLICATED"
    assert result.heldout_success is not None
    assert result.heldout_success<.75

def test_unadapted_new_partner_fails_without_relearning():
    old=PrivateSyntheticPartner(107,"responsive")
    assert evaluate_heldout(old,negotiate(old)).status=="RECIPROCAL_OPERATIONAL_CONVENTION_ON_HELDOUT_CONTEXTS"
    fresh=PrivateSyntheticPartner(41,"responsive")
    # Blindly replay a convention into a new partner that never saw its offers.
    assert all(fresh.outcome(scene,_outbound_symbol(int(scene[0]>0)))==.1
               for scene in HELDOUT)
    assert evaluate_heldout(fresh,negotiate(fresh)).status=="RECIPROCAL_OPERATIONAL_CONVENTION_ON_HELDOUT_CONTEXTS"

def test_measured_signals_are_not_predefined_in_client():
    partner=PrivateSyntheticPartner(41,"responsive")
    signatures=[fingerprint(partner.observe(scene)) for scene in SCENES]
    assert all(sig is not None and len(sig)==2 for sig in signatures)
    assert len({tuple(sig) for sig in signatures})==4  # measurement noise differs
    assert cosine(signatures[0],signatures[1])<.1 or cosine(signatures[0],signatures[2])<.1

@pytest.mark.parametrize("bad", [float("nan"),float("inf"),True,200.0])
def test_invalid_raw_channel_rejected(bad):
    source=[list(row) for row in raw_stream(17,"candidate")]
    source[20][0]=bad
    with pytest.raises(ValueError,match="malformed"):
        discover(source)

def test_oversized_stream_and_channel_count_rejected():
    with pytest.raises(ValueError,match="length"):
        validate_stream([[0.0,0.0]]*8193)
    with pytest.raises(ValueError,match="channel"):
        validate_stream([[0.0]*9 for _ in range(64)])

def test_unbounded_scene_inputs_not_allowed():
    from unvtrslr.contact_negotiation import _validate_scene
    for scene in ((float("nan"),0), (True,0), (2,0), "0,0"):
        with pytest.raises(ValueError):
            _validate_scene(scene)

def test_identifiability_requires_unique_dimension_with_replicates():
    both=[(scene,int(scene[0]>0)) for scene in SCENES for _ in range(3)]
    axis,mapping=_fit_relation(both)
    assert axis==0 and mapping=={0:0,1:1}
    xor=[(scene,int((scene[0]>0)!=(scene[1]>0))) for scene in SCENES for _ in range(3)]
    assert _fit_relation(xor) is None
    assert _fit_relation(both[:3]) is None

def test_probe_selection_is_adaptive_to_observed_coverage():
    assert _next_scene([])==SCENES[0]
    history=[(SCENES[0],0),(SCENES[0],0),(SCENES[1],1)]
    assert _next_scene(history) in (SCENES[2],SCENES[3])

def test_invalid_receiver_feedback_refused():
    class MaliciousPartner(PrivateSyntheticPartner):
        def outcome(self,scene,signal):return float("nan")
    with pytest.raises(ValueError,match="invalid external"):
        negotiate(MaliciousPartner(107,"responsive"))

def test_inference_disagrees_with_noncommunicative_periodic_control():
    result=discover(raw_stream(41,"periodic"))
    assert result.status!="RECURRENT_CANDIDATE_UNINTERPRETED"

def test_cross_seed_determinism_under_fresh_partner_state():
    assert evaluate(17,"responsive")==evaluate(17,"responsive")
    assert evaluate(107,"partner_drift")==evaluate(107,"partner_drift")

def test_never_expose_private_rule_to_learner_protocol():
    from unvtrslr.contact_negotiation import PartnerPort
    assert {"observe","offer","outcome"}.issubset(set(PartnerPort.__dict__))
    assert "axis" not in PartnerPort.__dict__
    assert "mapping" not in PartnerPort.__dict__

def test_negotiated_correction_retries_after_initial_unconfirmed_offer():
    delayed=PrivateSyntheticPartner(107,"slow_adaptation")
    result=evaluate_heldout(delayed,negotiate(delayed))
    assert result.status=="RECIPROCAL_OPERATIONAL_CONVENTION_ON_HELDOUT_CONTEXTS"
    assert result.proposed_signals==24
    assert result.heldout_success==.9

def test_noncooperative_partner_refuses_without_claiming_contact():
    refuses=PrivateSyntheticPartner(107,"no_adaptation")
    result=negotiate(refuses)
    assert result.status=="PROPOSAL_NOT_CONFIRMED"
    assert result.proposed_signals==24
    assert result.heldout_success is None
