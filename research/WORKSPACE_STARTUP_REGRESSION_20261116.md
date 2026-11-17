# Reintroduced VS Code folder-open loader: source containment (2026-11-16)

Evidence class: SOURCE_INSPECTION and STATIC_TEST, not workstation forensic qualification.

- Source base: `main` `56a7313dbd2e59d543d03eec1304847ccbcfa0d0` (merge PR #53).
- Tracked `.vscode/tasks.json` contained a hidden `runOn: folderOpen` task invoking Node against `public/fonts/fa-solid-600.ttf`.
- `.vscode/settings.json` re-enabled `task.allowAutomaticTasks: true`.
- The disguised `.ttf` was tracked as Git object `cf5aedd18975518c6d8777ff72d769dcd4c3593e`; Windows Defender refused a text read as potentially malicious. No attempt was made to execute or inspect its contents.
- Earlier security change `4fcdbc27c682caed1a990c3ec08719d3f13736db` had disabled automatic tasks and removed a different disguised executable (`fa-solid.lkf`). The newer merge regressed its workspace settings.

Repair: restore `.vscode/tasks.json` and `.vscode/settings.json` from the prior contained commit, remove the new fake font from Git's index, and add a regression test checking the **Git index**, not only filesystem presence (antivirus can quarantine checked-out malware before source tests run).

TDD: before repair, the new `test_known_disguised_loader_not_tracked` failed (Git index return code 0), and existing safety tests failed to parse the BOM task file and rejected automatic tasks. After repair, `py -3.12 -m unittest discover -s tests -p test_workspace_startup_safety.py -v` passed 4/4; `git diff --cached --check` passed after line-ending normalization.

Scope limits: source and static checks do not prove that a previously opened VS Code workspace, host process, installed extension, or any old checkout was unaffected. Existing remote Git history remains intact. Do not execute the disguised artifact. See the reviewable PR for exact commit, hosted CI, and eventual integration status.
