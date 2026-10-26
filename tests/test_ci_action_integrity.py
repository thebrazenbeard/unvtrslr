"""Prevent mutable action references in repository-owned CI workflows.

These checks cover source configuration only. They do not establish that an
upstream action remains trustworthy, nor do they execute hosted CI.
"""

from pathlib import Path
import re
import sys

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
GIT_SHA = re.compile(r"^[0-9a-f]{40}$")


class _UniqueKeysLoader(yaml.SafeLoader):
    """Reject duplicate keys rather than accepting parser-specific overrides."""


def _load_unique_mapping(loader: _UniqueKeysLoader, node: yaml.MappingNode) -> dict:
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        assert key not in result, f"duplicate workflow YAML key: {key}"
        result[key] = loader.construct_object(value_node, deep=True)
    return result


_UniqueKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _load_unique_mapping,
)


def _action_mappings(node: object):
    """Find actions in all YAML shapes, including flow steps and job-level uses."""
    if isinstance(node, dict):
        if "uses" in node:
            yield node
        for value in node.values():
            yield from _action_mappings(value)
    elif isinstance(node, list):
        for value in node:
            yield from _action_mappings(value)


def _workflow_actions(workflow: Path) -> list[dict]:
    try:
        source = yaml.load(workflow.read_text(encoding="utf-8"), Loader=_UniqueKeysLoader)
    except yaml.YAMLError as exc:
        pytest.fail(f"{workflow.name}: invalid workflow YAML: {exc}")
    assert isinstance(source, dict), f"{workflow.name}: expected workflow mapping"
    actions = list(_action_mappings(source))
    assert actions, f"{workflow.name}: no action references found"
    return actions


def _workflows() -> list[Path]:
    directory = ROOT / ".github" / "workflows"
    return sorted(set(directory.glob("*.yml")) | set(directory.glob("*.yaml")))


def _disables_persisted_credentials(step: dict) -> bool:
    settings = step.get("with")
    if not isinstance(settings, dict) or "persist-credentials" not in settings:
        return False
    return settings["persist-credentials"] is False or settings["persist-credentials"] == "false"


def test_all_workflow_action_references_are_immutable_full_commit_shas():
    workflows = _workflows()
    assert workflows, "the repository must retain a CI workflow"
    for workflow in workflows:
        for step in _workflow_actions(workflow):
            action = step["uses"]
            assert isinstance(action, str), f"{workflow.name}: action must be a string"
            assert "@" in action, f"{workflow.name}: action missing a pinned ref: {action}"
            revision = action.rsplit("@", 1)[-1]
            assert GIT_SHA.fullmatch(revision), (
                f"{workflow.name}: mutable or abbreviated action ref: {action}"
            )


def test_all_checkout_workflows_disable_persisted_token():
    for workflow in _workflows():
        checkouts = [
            step for step in _workflow_actions(workflow)
            if isinstance(step["uses"], str) and step["uses"].startswith("actions/checkout@")
        ]
        for index, step in enumerate(checkouts, start=1):
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
    with pytest.raises(AssertionError, match="duplicate|checkout"):
        test_all_checkout_workflows_disable_persisted_token()


def test_inline_yaml_action_mapping_cannot_hide_mutable_reference(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "flow.yml").write_text(
        f"steps:\n"
        f"  - uses: actions/checkout@{pinned}\n"
        f"    with:\n"
        f"      persist-credentials: false\n"
        f"  - {{uses: actions/setup-python@v5}}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="mutable"):
        test_all_workflow_action_references_are_immutable_full_commit_shas()


def test_inline_yaml_checkout_mapping_cannot_hide_token_persistence(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "flow.yaml").write_text(
        f"steps:\n"
        f"  - uses: actions/checkout@{pinned}\n"
        f"    with:\n"
        f"      persist-credentials: false\n"
        f"  - {{uses: actions/checkout@{pinned}, with: {{persist-credentials: true}}}}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="checkout"):
        test_all_checkout_workflows_disable_persisted_token()


def test_yaml_space_before_uses_colon_does_not_hide_mutable_action(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "spaced.yml").write_text(
        f"steps:\n"
        f"  - uses: actions/checkout@{pinned}\n"
        f"    with: {{persist-credentials: false}}\n"
        f"  - uses : actions/setup-python@v5\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="mutable"):
        test_all_workflow_action_references_are_immutable_full_commit_shas()


def test_duplicate_yaml_action_keys_rejected_before_scoring(tmp_path, monkeypatch):
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    pinned = "11bd71901bbe5b1630ceea73d27597364c9af683"
    (workflows / "duplicate.yml").write_text(
        f"steps:\n"
        f"  - uses: actions/setup-python@v5\n"
        f"    uses: actions/checkout@{pinned}\n"
        f"    with: {{persist-credentials: false}}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys.modules[__name__], "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="duplicate"):
        test_all_workflow_action_references_are_immutable_full_commit_shas()
