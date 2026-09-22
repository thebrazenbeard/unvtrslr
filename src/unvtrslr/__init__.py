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
]
