"""Verify pinned Argos archives before local-only package installation."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import stat
from pathlib import Path, PurePosixPath
import zipfile

SUPPORTED_TARGETS = ("fr", "de", "sw", "tr")
PINNED_CORPUS_SHA256 = "7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8"
PINNED_ARGOS_WHEEL_SHA256 = "a89b42d82f40843900338f9ac60d4c82fda590b6898247f5d0c15d46731ca7df"


def validate_lock(lock: dict) -> None:
    """Reject incomplete or altered model declarations before any package install."""
    if type(lock) is not dict or (
        lock.get("schema") != "UNV_ARGOS_MODEL_LOCK_V1"
        or lock.get("engine_package") != "argostranslate==1.11.0"
        or lock.get("engine_wheel_sha256") != PINNED_ARGOS_WHEEL_SHA256
        or lock.get("source_corpus_sha256") != PINNED_CORPUS_SHA256
    ):
        raise ValueError("unrecognized Argos model lock identity")
    models = lock.get("models")
    if type(models) is not list or len(models) != len(SUPPORTED_TARGETS):
        raise ValueError("incomplete Argos model lock")
    targets = []
    for spec in models:
        if type(spec) is not dict or set(spec) != {
            "target", "package_version", "argos_version", "bytes", "sha256", "url"
        }:
            raise ValueError("malformed Argos package lock")
        target = spec["target"]
        if target not in SUPPORTED_TARGETS or type(target) is not str:
            raise ValueError("unknown Argos direct target")
        if (type(spec["bytes"]) is not int or not 1 <= spec["bytes"] <= 400_000_000
                or type(spec["sha256"]) is not str or len(spec["sha256"]) != 64
                or any(char not in "0123456789abcdef" for char in spec["sha256"])):
            raise ValueError("invalid model digest or size")
        if (type(spec["package_version"]) is not str or not spec["package_version"]
                or type(spec["argos_version"]) is not str or not spec["argos_version"]
                or type(spec["url"]) is not str
                or not spec["url"].startswith("https://argos-net.com/v1/translate-en_"
                                             + target + "-")):
            raise ValueError("unrecognized direct Argos source")
        targets.append(target)
    if tuple(targets) != SUPPORTED_TARGETS:
        raise ValueError("Argos model targets missing, duplicated, or reordered")


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
            if (p.is_absolute() or ".." in p.parts or "\\" in item.filename
                    or not p.parts or ":" in p.parts[0]):
                raise ValueError("unsafe archive member")
            if item.create_system == 3 and stat.S_IFMT(item.external_attr >> 16) == stat.S_IFLNK:
                raise ValueError("symlink archive member not permitted")
        metas = [name for name in names if name.endswith("/metadata.json")]
        if len(metas) != 1:
            raise ValueError("exactly one package metadata required")
        meta = json.loads(archive.read(metas[0]))
        if (meta.get("from_code"), meta.get("to_code"), str(meta.get("package_version")), str(meta.get("argos_version"))) != ("en", spec["target"], spec["package_version"], spec["argos_version"]):
            raise ValueError("model identity mismatch")
    return meta

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, required=True)
    parser.add_argument("--download-dir", type=Path, required=True)
    a = parser.parse_args()
    lock = json.loads(a.lock.read_text(encoding="utf-8"))
    validate_lock(lock)
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
