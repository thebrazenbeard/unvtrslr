"""UNVTRSLR reference implementation.

This package is a research/reference implementation. It does not establish
semantic grounding or a universal translation capability.
"""

from .acoustics import acoustic_fingerprint, extract_frame_features
from .information import conditional_mutual_information, mutual_information
from .calibration import (
    FingerprintObservation,
    FeatureInteraction,
    calibrate_feature_information,
    calibrate_pairwise_interactions,
    fingerprint_scalars,
)

__all__ = [
    "acoustic_fingerprint",
    "extract_frame_features",
    "mutual_information",
    "conditional_mutual_information",
    "FingerprintObservation",
    "FeatureInteraction",
    "calibrate_feature_information",
    "calibrate_pairwise_interactions",
    "fingerprint_scalars",
]
