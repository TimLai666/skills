"""Reminder hooks for the writing-and-design plugin, run as Claude Code would run them."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HOOKS = Path(__file__).resolve().parent
SCRIPT = HOOKS / "reminders.py"


class Reminders(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.transcript = Path(tmp.name) / "session.jsonl"
        self.transcript.write_text("", encoding="utf-8")

    def run_hook(self, mode, payload=None, raw=None):
        event = dict(session_id="s1", transcript_path=str(self.transcript))
        event.update(payload or {})
        result = subprocess.run([sys.executable, str(SCRIPT), mode],
                                input=(raw if raw is not None else json.dumps(event)).encode("utf-8"),
                                capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.decode("utf-8")

    def context(self, mode, event, payload=None):
        out = self.run_hook(mode, dict(hook_event_name=event, **(payload or {})))
        if not out.strip():
            return None
        data = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(data["hookEventName"], event)
        self.assertNotIn("permissionDecision", data)
        return data["additionalContext"]

    def load(self, *names):
        for name in names:
            with open(self.transcript, "a", encoding="utf-8") as handle:
                handle.write(json.dumps({"type": "assistant", "message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": name}}]}}) + "\n")

    def compact(self):
        with open(self.transcript, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"type": "system", "subtype": "compact_boundary"}) + "\n")

    # human-writing on every user prompt
    def test_prompt_asks_to_load_human_writing(self):
        text = self.context("prompt", "UserPromptSubmit", {"prompt": "寫一份報告"})
        self.assertIn("載入 human-writing", text)

    def test_prompt_after_loading_asks_to_follow_it(self):
        self.load("writing-and-design:human-writing")
        text = self.context("prompt", "UserPromptSubmit", {"prompt": "好"})
        self.assertIn("已載入的 human-writing", text)

    def test_prompt_after_compaction_asks_to_load_again(self):
        self.load("writing-and-design:human-writing")
        self.compact()
        self.assertIn("載入 human-writing", self.context("prompt", "UserPromptSubmit"))

    # human-writing before writing prose files
    def test_prose_file_write_gets_reminder(self):
        for path in ("docs/report.md", "README.MD", "notes/summary.txt", "guide.rst"):
            text = self.context("pre-write", "PreToolUse", {"tool_name": "Write", "tool_input": {"file_path": path}})
            self.assertIn("human-writing", text, path)

    def test_code_and_data_files_are_ignored(self):
        for path in ("src/app.py", "package.json", "index.html", "styles.css", ""):
            self.assertIsNone(self.context("pre-write", "PreToolUse", {"tool_name": "Edit", "tool_input": {"file_path": path}}), path)

    def test_prose_write_silent_after_loading(self):
        self.load("human-writing")
        self.assertIsNone(self.context("pre-write", "PreToolUse", {"tool_input": {"file_path": "report.md"}}))

    # design-studio before Artifact calls
    def test_artifact_call_gets_design_reminder(self):
        text = self.context("pre-artifact", "PreToolUse", {"tool_name": "Artifact", "tool_input": {"file_path": "x.html"}})
        self.assertIn("design-studio", text)
        self.assertIn("不是設計類成品就忽略", text)

    def test_artifact_silent_after_design_studio_loaded(self):
        self.load("writing-and-design:design-studio")
        self.assertIsNone(self.context("pre-artifact", "PreToolUse", {"tool_input": {}}))

    def test_other_skill_does_not_count(self):
        self.load("writing-and-design:landing-page-studio")
        self.assertIsNotNone(self.context("pre-artifact", "PreToolUse", {"tool_input": {}}))
        self.assertIsNotNone(self.context("pre-write", "PreToolUse", {"tool_input": {"file_path": "a.md"}}))

    # shared behaviour
    def test_subagents_are_skipped(self):
        for mode, event in (("prompt", "UserPromptSubmit"), ("pre-write", "PreToolUse"), ("pre-artifact", "PreToolUse")):
            self.assertIsNone(self.context(mode, event, {"agent_id": "a1", "tool_input": {"file_path": "a.md"}}))

    def test_unknown_mode_and_bad_input_never_fail(self):
        self.assertEqual(self.run_hook("other"), "")
        self.assertEqual(self.run_hook("prompt", raw="not json"), "")
        self.assertEqual(self.run_hook("prompt", raw="[]"), "")
        self.assertEqual(self.run_hook("pre-write", {"tool_input": "text"}), "")
        self.assertIn("human-writing", self.context("prompt", "UserPromptSubmit", {"transcript_path": "/missing.jsonl"}))


if __name__ == "__main__":
    unittest.main()
