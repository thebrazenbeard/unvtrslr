"""Prevent mutable action references in repository-owned CI workflows.

These checks cover source configuration only. They do not establish that an
upstream action remains trustworthy, nor do they execute hosted CI.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
ACTION = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)", re.MULTILINE)
GIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def test_all_workflow_action_references_are_immutable_full_commit_shas():
    workflows = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
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
    for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        source = workflow.read_text(encoding="utf-8")
        if "uses: actions/checkout@" in source:
            assert "persist-credentials: false" in source, (
                f"{workflow.name}: checkout must not leave token in repository configuration"
            )
