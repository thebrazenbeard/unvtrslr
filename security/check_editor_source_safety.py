"""Static, standard-library-only guard for tracked editor startup and font assets.

This reads source bytes. It never starts VS Code, Node, a task, or a font.
Passing does not qualify an installed host, extensions, or user editor settings.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


# Pinned from the genuine pre-poison source assets in Git history, not from
# an external download or the masquerading fa-solid-600.ttf.
FONT_SHA256 = {
    "fa-brands-400.eot": "811e1577184066108ceca86d5a624a9012303df5206c5cb0b27d5e3fedcba5a3",
    "fa-brands-400.svg": "02340ba1789d09bcc507563c89c4a847ba537bb8132082777a50519cf74bcb5b",
    "fa-brands-400.ttf": "a0c145382acfe59767d1487d6505f349665b685c2885cd91b621d141a292b0f8",
    "fa-brands-400.woff": "e836c5d5dfc13e18170c5bddefb4fdac7c65ac0ad43a4b431acdc4a98865a260",
    "fa-brands-400.woff2": "5d9190292acdd48ba0fc35080f7e7448f3cdf0d79199a4d23f0f49b5341fdf29",
    "fa-regular-400.eot": "01f4416f5db59e2dd6b6fbd9dc32336d99db18f7eb623a49f584d04afd279473",
    "fa-regular-400.svg": "865fd23de13b1920280e182359579e09eff7a09eb24676eceec7552838559f55",
    "fa-regular-400.ttf": "f32b94a29060dfec0c797a1dfe111357eb1d682f1aca4ac4b95cf0f4c3e2bfa9",
    "fa-regular-400.woff": "8e2d96198711b63752e5f2f5987b8ffc536df6156a065bdbe28cb7231cad793d",
    "fa-regular-400.woff2": "6a8c8e9e1e7f692c21af1956de163f3d026778e6449fe93a09a671847ca1ae65",
    "fa-solid-900.eot": "32501727bb23fc77615b1ec76b5f298ec22198c0f3d6a3e7d6fe4ac3cf315db9",
    "fa-solid-900.svg": "e768539808757f7eec20f09c9ee9b36b0e6c5636e90c9ee697995cbbc6ee0555",
    "fa-solid-900.ttf": "231d68cefbc6846fb78cafca8467401a4f371e226418662e8900e3d52adc00ab",
    "fa-solid-900.woff": "352f8ead280419dd953d2bc7843386bb9430e8152c2dbd2c2d2494f6b9567ee7",
    "fa-solid-900.woff2": "7f4d3fd0a705dbf8403298aad91d5de6972e6b5d536068eba8b24954a5a0a8c7",
}


class UnsafeSource(ValueError):
    """Source contains an unsafe or unverifiable editor/font construct."""


def _jsonc_tokens(raw: bytes) -> str:
    """JSONC comments/trailing commas, respecting quoted strings and escapes."""
    text = raw.decode("utf-8-sig")
    result = []
    i = 0
    quote = False
    while i < len(text):
        char = text[i]
        if quote:
            result.append(char)
            if char == "\\" and i + 1 < len(text):
                i += 1
                result.append(text[i])
            elif char == '"':
                quote = False
            i += 1
            continue
        if char == '"':
            quote = True
            result.append(char)
            i += 1
            continue
        if char == "/" and i + 1 < len(text) and text[i + 1] == "/":
            i += 2
            while i < len(text) and text[i] not in "\r\n":
                i += 1
            result.append(" ")
            continue
        if char == "/" and i + 1 < len(text) and text[i + 1] == "*":
            i += 2
            end = text.find("*/", i)
            if end < 0:
                raise UnsafeSource("unterminated JSONC block comment")
            result.append(" ")
            i = end + 2
            continue
        result.append(char)
        i += 1
    if quote:
        raise UnsafeSource("unterminated JSONC string")
    uncom = "".join(result)
    cleaned = []
    quote = False
    i = 0
    while i < len(uncom):
        char = uncom[i]
        if quote:
            cleaned.append(char)
            if char == "\\" and i + 1 < len(uncom):
                i += 1
                cleaned.append(uncom[i])
            elif char == '"':
                quote = False
        elif char == '"':
            quote = True
            cleaned.append(char)
        elif char == ",":
            j = i + 1
            while j < len(uncom) and uncom[j].isspace():
                j += 1
            k = len(cleaned) - 1
            while k >= 0 and cleaned[k].isspace():
                k -= 1
            # An empty list/object never has a trailing comma: "[,]" must
            # remain invalid rather than silently normalizing into "[]".
            if j < len(uncom) and uncom[j] in "}]" and k >= 0 and cleaned[k] not in "[{,:":
                i += 1
                continue
            cleaned.append(char)
        else:
            cleaned.append(char)
        i += 1
    return "".join(cleaned)


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise UnsafeSource(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_jsonc(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise UnsafeSource(f"missing/nonregular/symlink editor config: {path}")
    try:
        parsed = json.loads(_jsonc_tokens(path.read_bytes()), object_pairs_hook=_unique_object)
    except (UnicodeError, ValueError) as error:
        raise UnsafeSource(f"invalid JSONC in {path}: {error}") from error
    if not isinstance(parsed, dict):
        raise UnsafeSource(f"editor config must be an object: {path}")
    return parsed


def _inspect(value: object, path: str) -> None:
    if isinstance(value, dict):
        for key, inner in value.items():
            field = f"{path}.{key}"
            # All editor startup triggers are disallowed, even nested inside
            # platform-specific/OS task definitions or workspace objects.
            if key == "runOn" and str(inner).lower() == "folderopen":
                raise UnsafeSource(f"folderOpen auto-task: {field}")
            if key == "task.allowAutomaticTasks" and inner != "off":
                raise UnsafeSource(f"automatic tasks enabled: {field}")
            if key == "tasks" and (
                path == "settings" or path.startswith("settings.")
                or path.endswith(".settings") or ".settings." in path
            ):
                raise UnsafeSource(f"embedded tasks under editor settings: {field}")
            _inspect(inner, field)
    elif isinstance(value, list):
        for index, inner in enumerate(value):
            _inspect(inner, f"{path}[{index}]")
    elif isinstance(value, str):
        # A task can inherit its command and hide the file reference in args.
        # Font assets must never be used as executable task arguments.
        lowered = value.replace("\\", "/").lower()
        if ("public/fonts/" in lowered and any(ext in lowered for ext in (".ttf", ".woff", ".eot", ".svg", ".lkf"))):
            raise UnsafeSource(f"font asset referenced by editor config: {path}")


def check(root: Path) -> list[str]:
    """Return all static violations without executing any source artifact."""
    violations: list[str] = []
    editor = root / ".vscode"
    if editor.is_symlink() or not editor.is_dir():
        violations.append("missing or symlink .vscode directory")
    paths = {editor / "tasks.json", editor / "settings.json"}
    # A root-only glob misses nested workspace folders. Casefold is necessary
    # because a tree checked on Linux may later be opened on case-insensitive
    # Windows, where .VSCODE and TASKS.JSON can resolve to editor paths.
    for dirname, subdirs, filenames in os.walk(root, followlinks=False):
        current = Path(dirname)
        subdirs[:] = [name for name in subdirs if name != ".git"]
        for name in subdirs:
            if name.casefold() != ".vscode":
                continue
            candidate = current / name
            if name != ".vscode":
                violations.append(f"case-variant editor directory: {candidate}")
            if candidate.is_symlink():
                violations.append(f"symlink editor directory: {candidate}")
        if current.name.casefold() == ".vscode":
            for name in filenames:
                if not name.casefold().endswith(".json"):
                    continue
                if name.casefold() in {"tasks.json", "settings.json"} and name != name.lower():
                    violations.append(f"case-variant editor filename: {current / name}")
                paths.add(current / name)
        for name in filenames:
            if name.casefold().endswith(".code-workspace"):
                paths.add(current / name)
    for path in sorted(paths):
        try:
            payload = _load_jsonc(path)
            _inspect(payload, path.stem.casefold())
            if path == editor / "settings.json" and payload.get("task.allowAutomaticTasks") != "off":
                raise UnsafeSource("workspace task.allowAutomaticTasks is not string 'off'")
            if path.name.casefold() == "tasks.json" and not isinstance(payload.get("tasks"), list):
                raise UnsafeSource("tasks.json tasks must be an array")
        except UnsafeSource as error:
            violations.append(str(error))

    fonts = root / "public" / "fonts"
    if fonts.is_symlink() or not fonts.is_dir():
        violations.append("missing or symlink public/fonts directory")
        return violations
    actual = {path.name for path in fonts.iterdir()}
    expected = set(FONT_SHA256) | {"README.md"}
    for unexpected in sorted(actual - expected):
        violations.append(f"unapproved font-directory entry: {unexpected}")
    readme = fonts / "README.md"
    if readme.is_symlink() or not readme.is_file():
        violations.append("missing/nonregular/symlink font README.md")
    for name, expected_hash in FONT_SHA256.items():
        path = fonts / name
        if path.is_symlink() or not path.is_file():
            violations.append(f"missing/nonregular/symlink pinned font: {name}")
            continue
        data = path.read_bytes()
        if name.endswith(".svg"):
            # Git Windows checkouts can represent unchanged SVG line endings
            # as CRLF. No other byte alteration or executable suffix is allowed.
            data = data.replace(b"\r\n", b"\n")
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash != expected_hash:
            violations.append(f"font SHA256 mismatch: {name}")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    violations = check(root)
    if violations:
        for violation in violations:
            print(f"EDITOR_SOURCE_UNSAFE: {violation}", file=sys.stderr)
        return 1
    print(f"EDITOR_SOURCE_OK: JSONC configurations, no automatic startup, {len(FONT_SHA256)} pinned assets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
