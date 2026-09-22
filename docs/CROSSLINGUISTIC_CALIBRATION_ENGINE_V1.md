# Cross-Linguistic Calibration Engine V1

Status: `REFERENCE_IMPLEMENTATION_CANDIDATE / KNOWN-SYSTEM MEASUREMENT CALIBRATION`

## Purpose

UNVTRSLR should not assume that pitch, timbre, rhythm, intensity, phonation, or any other acoustic dimension carries the same information in every communication system.

V1 therefore uses known systems as a **calibration universe**. It asks which measured dimensions distinguish supplied system labels after conditioning on declared nuisance variables such as speaker/source identity.

The result is a measurement prior. It is not a dictionary and it is not evidence that an unknown system uses the same distinctions.

## Research basis

The Zero Resource Speech benchmark treats acoustic-unit discovery as learning representations directly from raw audio without text labels, and explicitly evaluates whether representations retain relevant contrasts while discarding nuisance variation such as speaker and recording conditions.

Recent speaker/noise-invariant representation work such as R-Spin likewise treats nuisance invariance as a learned/evaluated property rather than an assumption.

Recent information-theoretic analysis of discrete speech units also warns that discretization does not automatically remove speaker information. A cluster or feature therefore receives no linguistic or semantic credit merely because it is discrete.

References:

- Zero Resource Speech Benchmark, Acoustic Unit Discovery / Speech Representation Learning: https://zerospeech.com/tasks/task_1/tasks_goals/
- Chang & Glass, *R-Spin: Efficient Speaker and Noise-invariant Representation Learning with Acoustic Pieces*, NAACL 2024, DOI `10.18653/v1/2024.naacl-long.36`.
- Yeh & Tang, *Estimating the Completeness of Discrete Speech Units*, arXiv:2409.06109 (2024).

## Input

Each observation binds an observation ID, a known `system_id`, a declared `source_id`, optional content/family IDs, and an `UNVTRSLR_ACOUSTIC_FINGERPRINT_V1` object.

The system label is not exposed to acoustic feature extraction. It enters only when the calibration report measures association.

## Feature vector

V1 flattens auditable scalar measurements from the acoustic fingerprint, including raw absolute pitch, source-relative pitch contour, intensity dynamics, periodicity, spectral statistics, `H1-H2`, MFCC statistics, and the envelope-modulation rhythm proxy.

Raw and relative pitch remain separate features. The engine can therefore discover that one view generalizes better than another rather than deleting either in advance.

## Core statistic

For discretized feature `X`, known-system target `Y`, and nuisance stratum `Z`, V1 computes:

`I(X ; Y | Z)`

It also reports raw `I(X ; Y)` and a deterministic within-stratum permutation null.

A feature becomes `CONDITIONAL_INFORMATION_SUPPORTED` only when the target is identifiable within observed nuisance strata, the feature varies sufficiently, and conditional information exceeds the frozen permutation-null criterion.

## Identifiability gate

If every nuisance stratum contains only one target class, target and nuisance are confounded. V1 returns:

`TARGET_CONFOUNDED_WITH_NUISANCE`

It does not reinterpret conditional MI near zero as evidence that the feature contains no system information. The corpus cannot answer that question under that design.

## Why this matters

A classifier can succeed by recognizing microphones, speakers, recording sites, or corpus artifacts. That is useless to a Universal Translator.

UNVTRSLR instead needs to know whether a dimension continues to carry information after obvious nuisance explanations are conditioned away and whether the corpus contains the contrasts required to identify the claim.

## Known limitations

V1 uses scalar summary features and quantile discretization. It does not yet model full trajectories, cross-channel synergy, causal interventions, genealogical/areal non-independence, or high-dimensional learned representations.

Permutation testing is diagnostic, not a universal significance procedure. Small or poorly crossed corpora can remain unidentifiable even with many recordings.

## Claim ceiling

`KNOWN_SYSTEM_MEASUREMENT_PRIOR_ONLY_NO_UNKNOWN_SEMANTIC_DECODING`

A high-scoring feature may justify prioritizing that measurement in later unknown-system experiments. It does not establish what an unknown signal means, that two systems share an ontology, or that translation has been achieved.
