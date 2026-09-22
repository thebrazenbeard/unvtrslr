"""UNVTRSLR reference implementation.

This package is a research/reference implementation. It does not establish
semantic grounding or a universal translation capability.
"""

from .acoustics import acoustic_fingerprint, extract_frame_features
from .information import conditional_mutual_information, mutual_information
from .unit_registry import (
    GlobalUnitAssignment,
    LocalUnitEvidence,
    UnitRegistryResult,
    build_unit_registry,
    evidence_from_event_result,
)
from .unit_model import (
    FrozenUnitModel,
    FrozenUnitPrototype,
    OutOfSampleUnitAssignment,
    assign_source_units,
    fit_frozen_unit_model,
    frozen_unit_model_from_dict,
)
from .event_evidence import (
    evidence_from_audio_event_result,
    evidence_from_event_frames,
)
from .translator import (
    AcousticContextEpisode,
    FrozenSemanticRelation,
    ReferenceTranslation,
    ReferenceTranslatorModel,
    SourceCalibrationProfile,
    fit_reference_translator,
    fit_source_calibration_profile,
    freeze_operational_relations,
    prepare_audio_evidence,
    reference_translator_model_from_dict,
    source_calibration_profile_from_dict,
    translate_query_evidence,
    translate_source_evidence,
)

__all__ = [
    "acoustic_fingerprint",
    "extract_frame_features",
    "mutual_information",
    "conditional_mutual_information",
    "GlobalUnitAssignment",
    "LocalUnitEvidence",
    "UnitRegistryResult",
    "build_unit_registry",
    "evidence_from_event_result",
    "FrozenUnitModel",
    "FrozenUnitPrototype",
    "OutOfSampleUnitAssignment",
    "assign_source_units",
    "fit_frozen_unit_model",
    "frozen_unit_model_from_dict",
    "evidence_from_audio_event_result",
    "evidence_from_event_frames",
    "AcousticContextEpisode",
    "FrozenSemanticRelation",
    "ReferenceTranslation",
    "ReferenceTranslatorModel",
    "SourceCalibrationProfile",
    "fit_reference_translator",
    "fit_source_calibration_profile",
    "freeze_operational_relations",
    "prepare_audio_evidence",
    "reference_translator_model_from_dict",
    "source_calibration_profile_from_dict",
    "translate_query_evidence",
    "translate_source_evidence",
]
