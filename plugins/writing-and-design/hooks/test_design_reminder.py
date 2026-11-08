"""Design reminder hook for the writing-and-design plugin, run as Claude Code would run it."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HOOKS = Path(__file__).resolve().parent
SCRIPT = HOOKS / "design_reminder.py"


class DesignReminder(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.transcript = Path(tmp.name) / "session.jsonl"
        self.transcript.write_text("", encoding="utf-8")

    def run_hook(self, tool_input=None, extra=None, raw=None, mode="pre-artifact"):
        event = dict(session_id="s1", transcript_path=str(self.transcript), hook_event_name="PreToolUse",
                     tool_name="Artifact", tool_input=tool_input or {"file_path": "page.html"})
        event.update(extra or {})
        result = subprocess.run([sys.executable, str(SCRIPT), mode],
                                input=raw if raw is not None else json.dumps(event),
                                capture_output=True, text=True, encoding="utf-8", timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def reminder(self, tool_input=None, extra=None):
        out = self.run_hook(tool_input, extra)
        if not out.strip():
            return None
        data = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(data["hookEventName"], "PreToolUse")
        self.assertNotIn("permissionDecision", data)
        return data["additionalContext"]

    def record(self, *items):
        with open(self.transcript, "a", encoding="utf-8") as handle:
            for item in items:
                handle.write(json.dumps(item) + "\n")

    def load_skill(self, name="writing-and-design:design-studio"):
        self.record({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": name}}]}})

    def test_any_artifact_call_gets_reminder_and_agent_decides(self):
        for tool_input in ({"file_path": "report.html"}, {"type_url": "https://claude.ai/artifact/x"},
                           {"action": "quickstart", "intent": "other"}):
            text = self.reminder(tool_input)
            self.assertIn("design-studio", text)
            self.assertIn("不是設計類成品就忽略", text)

    def test_no_reminder_after_skill_loaded(self):
        self.load_skill()
        self.assertIsNone(self.reminder())

    def test_other_skill_does_not_count(self):
        self.load_skill("writing-and-design:landing-page-studio")
        self.assertIsNotNone(self.reminder())

    def test_compaction_resets_loaded_state(self):
        self.load_skill()
        self.record({"type": "system", "subtype": "compact_boundary"})
        self.assertIsNotNone(self.reminder())

    def test_subagents_are_skipped(self):
        self.assertIsNone(self.reminder(extra={"agent_id": "a1"}))

    def test_other_modes_do_nothing(self):
        self.assertEqual(self.run_hook(mode="other"), "")

    def test_output_is_utf8(self):
        out = subprocess.run([sys.executable, str(SCRIPT), "pre-artifact"],
                             input=json.dumps(dict(transcript_path=str(self.transcript), tool_input={})).encode("utf-8"),
                             capture_output=True, timeout=20).stdout
        self.assertIn("設計".encode("utf-8"), out)

    def test_bad_input_never_fails(self):
        self.assertEqual(self.run_hook(raw="not json"), "")
        self.assertEqual(self.run_hook(raw="[]"), "")
        self.assertIsNotNone(self.reminder(extra={"transcript_path": "/missing/file.jsonl"}))


if __name__ == "__main__":
    unittest.main()
