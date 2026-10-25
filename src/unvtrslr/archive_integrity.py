"""Bounded integrity checks for externally supplied corpus archives.

This module verifies byte identity before archive parsing; it does not unpack
or inspect archive members and does not establish upstream authenticity.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path


def verify_archive_identity(
    path: Path,
    *,
    expected_sha256: str,
    expected_bytes: int,
) -> str:
    """Reject a corpus whose size or SHA-256 differs from the frozen artifact."""
    observed_bytes = path.stat().st_size
    if observed_bytes != expected_bytes:
        raise ValueError(
            f"archive size mismatch: expected {expected_bytes} bytes, "
            f"observed {observed_bytes}"
        )

    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    observed_sha256 = digest.hexdigest()
    if observed_sha256 != expected_sha256:
        raise ValueError(
            "archive SHA-256 mismatch: "
            f"expected {expected_sha256}, observed {observed_sha256}"
        )
    return observed_sha256
