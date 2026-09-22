"""UNVTRSLR reference implementation.

This package is a research/reference implementation. It does not establish
semantic grounding or a universal translation capability.
"""

from .acoustics import acoustic_fingerprint, extract_frame_features
from .information import conditional_mutual_information, mutual_information
from .calibration import (
    FingerprintObservation,
    calibrate_feature_information,
    fingerprint_scalars,
)

__all__ = [
    "acoustic_fingerprint",
    "extract_frame_features",
    "mutual_information",
    "conditional_mutual_information",
    "FingerprintObservation",
    "calibrate_feature_information",
    "fingerprint_scalars",
]
