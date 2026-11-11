"""Adversarial inert fixtures: nothing in these tests is ever executed."""

import shutil
from pathlib import Path
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "security"))
from check_editor_source_safety import FONT_SHA256, _load_jsonc, UnsafeSource, check  # noqa: E402


class EditorSourceSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".vscode").mkdir()
        shutil.copytree(REPO / "public" / "fonts", self.root / "public" / "fonts")
        (self.root / ".vscode" / "settings.json").write_text(
            '{"task.allowAutomaticTasks":"off"}', encoding="utf-8"
        )
        (self.root / ".vscode" / "tasks.json").write_text(
            '{"version":"2.0.0","tasks":[]}', encoding="utf-8"
        )

    def violations(self):
        return check(self.root)

    def task(self, source: str):
        (self.root / ".vscode" / "tasks.json").write_text(source, encoding="utf-8")

    def setting(self, source: str):
        (self.root / ".vscode" / "settings.json").write_text(source, encoding="utf-8")

    def test_repository_source_clean(self):
        self.assertEqual(check(REPO), [])

    def test_clean_manual_task_and_string_slashes(self):
        self.task('{"tasks":[{"label":"manual","command":"echo // not a comment",'
                  '"args":["safe,} text"],"runOptions":{"reevaluateOnRerun":true}}]}')
        self.assertEqual(self.violations(), [])

    def test_bom_jsonc_comments_and_trailing_commas_safe(self):
        (self.root / ".vscode" / "tasks.json").write_bytes(
            b'\xef\xbb\xbf{ // comment\n "tasks":[ /* a */ { "label":"manual", }, ], }'
        )
        self.assertEqual(self.violations(), [])

    def test_bom_jsonc_hidden_autostart_rejected(self):
        (self.root / ".vscode" / "tasks.json").write_bytes(
            b'\xef\xbb\xbf{"tasks":[{"runOptions":{"runOn":"folderOpen"},}],}'
        )
        self.assertTrue(any("folderOpen" in error for error in self.violations()))

    def test_duplicate_keys_rejected_even_nested(self):
        self.task('{"tasks":[{"runOptions":{"runOn":"manual","runOn":"folderOpen"}}]}')
        self.assertTrue(any("duplicate" in error for error in self.violations()))
        self.setting('{"task.allowAutomaticTasks":"off","task.allowAutomaticTasks":true}')
        self.assertTrue(any("duplicate" in error for error in self.violations()))

    def test_os_specific_top_level_and_nested_tasks_rejected(self):
        for source in (
            '{"windows":{"tasks":[{"runOptions":{"runOn":"folderOpen"}}]},"tasks":[]}',
            '{"tasks":[{"linux":{"runOptions":{"runOn":"folderOpen"}}}]}',
            '{"tasks":[{"osx":{"tasks":[{"runOptions":{"runOn":"folderOpen"}}]}}]}',
        ):
            with self.subTest(source=source):
                self.task(source)
                self.assertTrue(any("folderOpen" in error for error in self.violations()))

    def test_workspace_file_settings_and_tasks_rejected(self):
        workspace = self.root / "test.code-workspace"
        workspace.write_text(
            '{"settings":{"task.allowAutomaticTasks":true},'
            '"tasks":{"tasks":[{"runOptions":{"runOn":"folderOpen"}}]}}',
            encoding="utf-8",
        )
        self.assertTrue(self.violations())
        workspace.write_text(
            '{"settings":{"tasks":{"label":"nested"}}}', encoding="utf-8"
        )
        self.assertTrue(any("embedded" in error for error in self.violations()))
        workspace.unlink()
        subfolder = self.root / "subfolder"
        subfolder.mkdir()
        (subfolder / "nested.code-workspace").write_text(
            '{"tasks":{"tasks":[{"runOptions":{"runOn":"folderOpen"}}]}}',
            encoding="utf-8",
        )
        self.assertTrue(any("folderOpen" in error for error in self.violations()))

    def test_other_vscode_json_auto_run_rejected(self):
        (self.root / ".vscode" / "launch.json").write_text(
            '{"configurations":[{"runOptions":{"runOn":"folderOpen"}}]}',
            encoding="utf-8",
        )
        self.assertTrue(any("folderOpen" in error for error in self.violations()))

    def test_inherited_command_font_argument_rejected(self):
        self.task('{"tasks":[{"command":"node",'
                  '"windows":{"args":["./public/fonts/fa-solid-900.ttf"]}}]}')
        self.assertTrue(any("font asset" in error for error in self.violations()))
        self.task('{"tasks":[{"command":"node",'
                  '"args":[".\\\\public\\\\fonts\\\\fa-solid-900.ttf"]}]}')
        self.assertTrue(self.violations())

    def test_bad_settings_and_embedded_task_rejected(self):
        self.setting('{"task.allowAutomaticTasks":true}')
        self.assertTrue(any("automatic" in error for error in self.violations()))
        self.setting('{"task.allowAutomaticTasks":"off","tasks":{"label":"hidden"}}')
        self.assertTrue(any("embedded" in error for error in self.violations()))

    def test_missing_pinned_font_rejected(self):
        (self.root / "public" / "fonts" / "fa-brands-400.ttf").unlink()
        self.assertTrue(any("missing" in error for error in self.violations()))

    def test_extra_counterfeit_font_rejected(self):
        (self.root / "public" / "fonts" / "fa-solid-600.ttf").write_text("INERT", encoding="utf-8")
        self.assertTrue(any("unapproved" in error for error in self.violations()))

    def test_symlink_font_dir_and_asset_rejected(self):
        fonts = self.root / "public" / "fonts"
        target = fonts / "fa-brands-400.ttf"
        target.unlink()
        target.symlink_to(REPO / "public" / "fonts" / "fa-brands-400.ttf")
        self.assertTrue(any("symlink pinned" in error for error in self.violations()))
        target.unlink()
        shutil.rmtree(fonts)
        fonts.symlink_to(REPO / "public" / "fonts", target_is_directory=True)
        self.assertTrue(any("symlink public/fonts" in error for error in self.violations()))

    def test_symlink_editor_config_rejected(self):
        tasks = self.root / ".vscode" / "tasks.json"
        tasks.unlink()
        tasks.symlink_to(REPO / ".vscode" / "tasks.json")
        self.assertTrue(any("symlink editor config" in error for error in self.violations()))

    def test_symlink_font_readme_rejected(self):
        readme = self.root / "public" / "fonts" / "README.md"
        readme.unlink()
        readme.symlink_to(REPO / "public" / "fonts" / "README.md")
        self.assertTrue(any("symlink font README" in error for error in self.violations()))

    def test_svg_crlf_only_normalized(self):
        svg = self.root / "public" / "fonts" / "fa-regular-400.svg"
        original = svg.read_bytes()
        self.assertIn(b"\n", original)
        svg.write_bytes(original.replace(b"\n", b"\r\n"))
        self.assertEqual(self.violations(), [])
        svg.write_bytes(svg.read_bytes() + b"<script>inert injection</script>")
        self.assertTrue(any("SHA256 mismatch" in error for error in self.violations()))

    def test_other_font_mutation_rejected(self):
        font = self.root / "public" / "fonts" / "fa-solid-900.woff2"
        font.write_bytes(font.read_bytes() + b"INERT")
        self.assertTrue(any("SHA256 mismatch" in error for error in self.violations()))

    def test_pin_count_and_real_hashes_present(self):
        self.assertEqual(len(FONT_SHA256), 15)
        self.assertEqual(len({name for name in FONT_SHA256 if name.endswith(".ttf")}), 3)

    def test_invalid_or_duplicate_jsonc_rejected(self):
        self.task('{"tasks":[,]}')
        self.assertTrue(any("invalid JSONC" in error for error in self.violations()))
        self.task('{"tasks":[],"x":{"y":1,"y":2}}')
        self.assertTrue(any("duplicate" in error for error in self.violations()))


if __name__ == "__main__":
    unittest.main()
