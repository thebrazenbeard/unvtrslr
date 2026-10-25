"""No corpus may be read or qualified before byte-identity validation."""

import hashlib
from pathlib import Path
import runpy
import sys
from tempfile import TemporaryDirectory
from unittest import TestCase, mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from unvtrslr.archive_integrity import verify_archive_identity  # noqa: E402


class MassiveArchiveIntegrityTests(TestCase):
    def test_verified_test_artifact(self):
        payload = b"unit-test-corpus"
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "corpus.tar.gz"
            path.write_bytes(payload)
            observed = verify_archive_identity(
                path,
                expected_sha256=hashlib.sha256(payload).hexdigest(),
                expected_bytes=len(payload),
            )
            self.assertEqual(observed, hashlib.sha256(payload).hexdigest())

    def test_wrong_size_rejects_before_read(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "corpus.tar.gz"
            path.write_bytes(b"altered")
            with mock.patch("pathlib.Path.open", side_effect=AssertionError("read attempted")):
                with self.assertRaisesRegex(ValueError, "size mismatch"):
                    verify_archive_identity(
                        path, expected_sha256="0" * 64, expected_bytes=39500415
                    )

    def test_same_size_corruption_rejected(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "corpus.tar.gz"
            path.write_bytes(b"forged")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                verify_archive_identity(
                    path, expected_sha256="0" * 64, expected_bytes=6
                )

    def test_runner_fails_before_writing_outputs(self):
        main = runpy.run_path(
            str(ROOT / "runs" / "massive_v1_first_real_corpus_20260922" / "run.py")
        )["main"]
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "tampered.tar.gz"
            path.write_bytes(b"not the dataset")
            output = Path(tmp) / "generated"
            argv = [
                "run.py", "--dataset-tar", str(path), "--out", str(output),
                "--thresholds", str(Path(tmp) / "nonexistent.json"),
            ]
            with mock.patch.object(sys, "argv", argv):
                with self.assertRaisesRegex(ValueError, "archive size mismatch"):
                    main()
            self.assertFalse(output.exists())
