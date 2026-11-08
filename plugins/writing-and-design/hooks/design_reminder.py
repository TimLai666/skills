#!/usr/bin/env python3
"""Optional reminder that points Claude Code to the design-studio skill.

Usage: design_reminder.py pre-artifact, with the PreToolUse event JSON on stdin.
Before every Artifact call, when design-studio has not been loaded since the last
compaction, the hook adds a reminder to Claude's context. The agent decides
whether the artifact is design work. The hook never blocks the call. Any error
prints nothing and exits 0.
"""
import json
import sys

SKILL = "design-studio"

REMINDER = (
    "如果這個 artifact 是設計類成品（網頁、畫面、簡報、海報、設計系統、視覺設計等），先載入 design-studio skill："
    "方向、配色與設計規則照 design-studio，檔案格式與交付照 artifact 類型的說明，"
    "分工見 design-studio 的 references/claude-design.md。不是設計類成品就忽略這個提醒。")


def skill_loaded(transcript):
    """True when design-studio was loaded after the last compaction."""
    loaded = False
    try:
        with open(transcript, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if "compact_boundary" in line:
                    try:
                        record = json.loads(line)
                    except ValueError:
                        continue
                    if record.get("type") == "system" and record.get("subtype") == "compact_boundary":
                        loaded = False
                elif '"Skill"' in line and SKILL in line:
                    try:
                        content = json.loads(line).get("message", {}).get("content")
                    except ValueError:
                        continue
                    for block in content if isinstance(content, list) else []:
                        if not isinstance(block, dict):
                            continue
                        name = str((block.get("input") or {}).get("skill", ""))
                        if block.get("type") == "tool_use" and block.get("name") == "Skill" and \
                                name.split(":")[-1] == SKILL:
                            loaded = True
    except (OSError, TypeError):
        return False
    return loaded


def respond(mode, event):
    if mode != "pre-artifact" or event.get("agent_id"):
        return None
    if skill_loaded(event.get("transcript_path")):
        return None
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": REMINDER}}


def main():
    try:
        event = json.loads(sys.stdin.read())
        if not isinstance(event, dict):
            return 0
        reply = respond(sys.argv[1] if len(sys.argv) > 1 else "", event)
    except Exception:  # The reminder is optional; never interrupt the session.
        return 0
    if reply:
        # Claude Code reads hook output as UTF-8; Windows consoles default to a legacy code page.
        sys.stdout.buffer.write(json.dumps(reply, ensure_ascii=False).encode("utf-8") + b"\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
