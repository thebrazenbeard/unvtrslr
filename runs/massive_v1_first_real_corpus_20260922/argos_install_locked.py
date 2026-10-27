"""Verify pinned Argos archives before local-only package installation."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import stat
from pathlib import Path, PurePosixPath
import zipfile

def validate_model(path: Path, spec: dict) -> dict:
    if not path.is_file() or path.stat().st_size != spec["bytes"]:
        raise ValueError(f"archive size mismatch for {path.name}")
    with path.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != spec["sha256"]:
        raise ValueError(f"archive hash mismatch for {path.name}")
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        names = [item.filename for item in entries]
        if len(names) != len(set(names)) or not entries:
            raise ValueError("duplicate/empty zip members")
        if sum(item.file_size for item in entries) > 2_000_000_000:
            raise ValueError("unexpected model expansion size")
        for item in entries:
            p = PurePosixPath(item.filename)
            if p.is_absolute() or ".." in p.parts or "\\" in item.filename:
                raise ValueError("unsafe archive member")
            if item.create_system == 3 and stat.S_IFMT(item.external_attr >> 16) == stat.S_IFLNK:
                raise ValueError("symlink archive member not permitted")
        metas = [name for name in names if name.endswith("/metadata.json")]
        if len(metas) != 1:
            raise ValueError("exactly one package metadata required")
        meta = json.loads(archive.read(metas[0]))
        if (meta.get("from_code"), meta.get("to_code"), str(meta.get("package_version"))) != ("en", spec["target"], spec["package_version"]):
            raise ValueError("model identity mismatch")
    return meta

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    a = parser.parse_args()
    lock = json.loads(a.lock.read_text(encoding="utf-8"))
    if importlib.metadata.version("argostranslate") != "1.11.0":
        raise ValueError("unqualified Argos engine version")
    verified = []
    for spec in lock["models"]:
        path = a.download_dir / f'en_{spec["target"]}.argosmodel'
        metadata = validate_model(path, spec)
        print("VERIFIED", spec["target"], spec["sha256"], metadata, flush=True)
        verified.append(path)
    from argostranslate import package
    for path in verified:
        package.install_from_path(path)
        print("INSTALLED", path.name, flush=True)

if __name__ == "__main__":
    main()
