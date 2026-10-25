"""Bounded integrity checks for externally supplied corpus archives.

Use the verified byte snapshot for parsing; verifying a path and reopening it
later would allow a concurrent path replacement to invalidate the attestation.
Neither check inspects archive members or establishes upstream authenticity.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path


def load_verified_archive(
    path: Path,
    *,
    expected_sha256: str,
    expected_bytes: int,
) -> tuple[bytes, str]:
    """Return a bounded immutable snapshot and its verified SHA-256 digest.

    Hold these bytes until all archive parsing finishes; never re-open ``path``
    as an alleged continuation of this verification. The frozen MASSIVE corpus
    is approximately 40 MiB, so an in-memory snapshot is a bounded tradeoff.
    """
    observed_bytes = path.stat().st_size
    if observed_bytes != expected_bytes:
        raise ValueError(
            f"archive size mismatch: expected {expected_bytes} bytes, "
            f"observed {observed_bytes}"
        )

    with path.open("rb") as stream:
        # The extra byte detects growth even when the pre-open stat was correct.
        archive_bytes = stream.read(expected_bytes + 1)
    if len(archive_bytes) != expected_bytes:
        raise ValueError(
            f"archive size mismatch: expected {expected_bytes} bytes, "
            f"observed {len(archive_bytes)}"
        )

    observed_sha256 = sha256(archive_bytes).hexdigest()
    if observed_sha256 != expected_sha256:
        raise ValueError(
            "archive SHA-256 mismatch: "
            f"expected {expected_sha256}, observed {observed_sha256}"
        )
    return archive_bytes, observed_sha256


def verify_archive_identity(
    path: Path,
    *,
    expected_sha256: str,
    expected_bytes: int,
) -> str:
    """Check byte identity at read time (not a promise for later path reads)."""
    _, digest = load_verified_archive(
        path,
        expected_sha256=expected_sha256,
        expected_bytes=expected_bytes,
    )
    return digest
