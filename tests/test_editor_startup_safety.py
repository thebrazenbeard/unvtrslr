"""Static regressions for editor-startup safety; never execute workspace tasks."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class EditorStartupSafetyTests(unittest.TestCase):
    def test_tasks_parse_without_implicit_execution(self):
        text = (ROOT / ".vscode" / "tasks.json").read_text(encoding="utf-8")
        tasks = json.loads(text)
        self.assertEqual(tasks.get("tasks"), [])
        self.assertIsNone(re.search(r'"runOn"\s*:\s*"folderOpen"', text))
        self.assertIsNone(re.search(r"\bnode\s+[^\n]*public/fonts/", text))

    def test_settings_do_not_override_automatic_task_policy(self):
        settings = json.loads(
            (ROOT / ".vscode" / "settings.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("task.allowAutomaticTasks", settings)
        self.assertNotIn("tasks", settings)

    def test_disguised_asset_absent(self):
        self.assertFalse((ROOT / "public" / "fonts" / "fa-solid.lkf").exists())


if __name__ == "__main__":
    unittest.main()
