"""Prevent mutable action references in repository-owned CI workflows.

These checks cover source configuration only. They do not establish that an
upstream action remains trustworthy, nor do they execute hosted CI.
"""

from pathlib import Path
import re
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
ACTION = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)", re.MULTILINE)
GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
STEP_START = re.compile(r"^(?P<indent> *)-\s+[A-Za-z_-]+\s*:")


def _workflows() -> list[Path]:
    directory = ROOT / ".github" / "workflows"
    return sorted(set(directory.glob("*.yml")) | set(directory.glob("*.yaml")))


def _checkout_steps(source: str) -> list[list[str]]:
    """Extract steps containing a checkout action without a YAML dependency.

    This deliberately conservative lexical check is not a complete YAML
    interpreter; an unfamiliar checkout shape must fail closed rather than
    using an unrelated step's credential setting as authorization.
    """
    lines = source.splitlines()
    steps = []
    for action_index, line in enumerate(lines):
        match = ACTION.match(line)
        if not match or not match.group(1).startswith("actions/checkout@"):
            continue
        action_indent = len(line) - len(line.lstrip(" "))
        first = None
        step_indent = None
        for index in range(action_index, -1, -1):
            start = STEP_START.match(lines[index])
            if start and len(start.group("indent")) <= action_indent:
                first = index
                step_indent = len(start.group("indent"))
                break
        if first is None or step_indent is None:
            steps.append([])
            continue
        last = len(lines)
        for index in range(action_index + 1, len(lines)):
            stripped = lines[index].strip()
            if not stripped or stripped.startswith("#"):
                continue
            indent = len(lines[index]) - len(lines[index].lstrip(" "))
            if indent <= step_indent:
                last = index
                break
        steps.append(lines[first:last])
    return steps


def _disables_persisted_credentials(step: list[str]) -> bool:
    with_indent = None
    with_count = 0
    settings = []
    for line in step:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if stripped == "with:" or stripped.startswith("with: #"):
            with_count += 1
            with_indent = indent
        elif with_indent is not None and indent > with_indent and stripped.startswith("persist-credentials:"):
            value = stripped.partition(":")[2].split("#", 1)[0].strip()
            settings.append(value)
    # Multiple declarations are ambiguous across YAML parsers. Accept one
    # explicit false only; earlier false followed by true must not bypass it.
    return with_count == 1 and len(settings) == 1 and settings[0] in (
        "false", "'false'", '"false"'
    )


def test_all_workflow_action_references_are_immutable_full_commit_shas():
    workflows = _workflows()
    assert workflows, "the repository must retain a CI workflow"
    for workflow in workflows:
        uses = ACTION.findall(workflow.read_text(encoding="utf-8"))
        assert uses, f"{workflow.name}: no action references found"
        for action in uses:
            assert "@" in action, f"{workflow.name}: action missing a pinned ref: {action}"
            revision = action.rsplit("@", 1)[-1]
            assert GIT_SHA.fullmatch(revision), (
                f"{workflow.name}: mutable or abbreviated action ref: {action}"
            )


def test_all_checkout_workflows_disable_persisted_token():
    for workflow in _workflows():
        source = workflow.read_text(encoding="utf-8")
        for index, step in enumerate(_checkout_steps(source), start=1):
            assert _disables_persisted_credentials(step), (
                f"{workflow.name}: checkout #{index} must explicitly disable persisted credentials"
            )


def test_action_integrity_includes_yaml_extension(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "safe.yml").write_text(f"steps:\n  - uses: actions/checkout@{pinned}\n", encoding="utf-8")
    (workflows / "unsafe.yaml").write_text("steps:\n  - uses: actions/setup-python@v5\n", encoding="utf-8")
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="mutable"):
        test_all_workflow_action_references_are_immutable_full_commit_shas()


def test_each_checkout_step_must_disable_persisted_token(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "mixed.yml").write_text(
        f"steps:\n"
        f"  - uses: actions/checkout@{pinned}\n"
        f"    with:\n"
        f"      persist-credentials: false\n"
        f"  - uses: actions/checkout@{pinned}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="checkout"):
        test_all_checkout_workflows_disable_persisted_token()


def test_duplicate_checkout_credentials_cannot_hide_true_value(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "duplicate.yaml").write_text(
        f"steps:\n"
        f"  - uses: actions/checkout@{pinned}\n"
        f"    with:\n"
        f"      persist-credentials: false\n"
        f"      persist-credentials: true\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="checkout"):
        test_all_checkout_workflows_disable_persisted_token()
