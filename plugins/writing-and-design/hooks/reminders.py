#!/usr/bin/env python3
"""Optional reminders that point Claude Code to the writing-and-design skills.

Usage: reminders.py MODE, with the hook event JSON on stdin.
Modes:
  prompt        UserPromptSubmit: the reply to the user follows human-writing and
                uses the reply language the user or the instruction files set.
  pre-write     PreToolUse on Write/Edit: a prose file (report, document, README)
                is being written and human-writing is not loaded yet.
  pre-artifact  PreToolUse on Artifact: design-studio is not loaded yet; the agent
                decides whether the artifact is design work.
The hooks only add context and never block a call. Any error prints nothing and
exits 0.
"""
import json
from pathlib import PurePath
import sys

WRITING = "human-writing"
DESIGN = "design-studio"
PROSE_SUFFIXES = {".md", ".mdx", ".markdown", ".txt", ".rst", ".adoc"}

PROMPT_LOAD = (
    "回覆使用者，或寫報告、文件、說明等給人讀的文字之前，先載入 human-writing skill，照它的流程寫。"
    "純程式碼、結構化資料或指令不在此限。")
PROMPT_FOLLOW = "這一輪回覆使用者，以及要寫的報告、文件，照已載入的 human-writing skill 的流程與檢查清單寫。"
LANGUAGE = (
    "回覆用的語言依序這樣決定："
    "使用者這一則訊息明確指定了語言，就用那個語言；"
    "沒有的話，用 CLAUDE.md、AGENTS.md、系統或專案指示，或使用者先前訊息裡指定的回覆語言；"
    "都沒有指定，才跟著使用者這則訊息的語言。"
    "不要因為使用者這次剛好用了別的語言，或自己思考時用的語言，就換掉指定的回覆語言。")
WRITE_LOAD = (
    "正要寫的是給人讀的文件。先載入 human-writing skill，照它的流程寫。"
    "如果這個檔案是程式設定或機器讀的資料，就忽略這個提醒。")
DESIGN_LOAD = (
    "如果這個 artifact 是設計類成品（網頁、畫面、簡報、海報、設計系統、視覺設計等），先載入 design-studio skill："
    "方向、配色與設計規則照 design-studio，檔案格式與交付照 artifact 類型的說明，"
    "分工見 design-studio 的 references/claude-design.md。不是設計類成品就忽略這個提醒。")


def context(event, text):
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def loaded_skills(transcript):
    """Names of skills loaded with the Skill tool since the last compaction."""
    loaded = set()
    try:
        with open(transcript, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if "compact_boundary" in line:
                    try:
                        record = json.loads(line)
                    except ValueError:
                        continue
                    if record.get("type") == "system" and record.get("subtype") == "compact_boundary":
                        loaded = set()
                elif '"Skill"' in line:
                    try:
                        content = json.loads(line).get("message", {}).get("content")
                    except ValueError:
                        continue
                    for block in content if isinstance(content, list) else []:
                        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                            loaded.add(str((block.get("input") or {}).get("skill", "")).split(":")[-1])
    except (OSError, TypeError):
        return set()
    return loaded


def is_prose_file(tool_input):
    path = str((tool_input or {}).get("file_path") or "") if isinstance(tool_input, dict) else ""
    return PurePath(path).suffix.lower() in PROSE_SUFFIXES


def respond(mode, event):
    if event.get("agent_id"):
        return None  # Delegated subagents follow their task prompt.
    loaded = loaded_skills(event.get("transcript_path"))
    if mode == "prompt":
        return context("UserPromptSubmit", (PROMPT_FOLLOW if WRITING in loaded else PROMPT_LOAD) + LANGUAGE)
    if mode == "pre-write":
        if WRITING in loaded or not is_prose_file(event.get("tool_input")):
            return None
        return context("PreToolUse", WRITE_LOAD)
    if mode == "pre-artifact":
        return None if DESIGN in loaded else context("PreToolUse", DESIGN_LOAD)
    return None


def main():
    try:
        event = json.loads(sys.stdin.read())
        if not isinstance(event, dict):
            return 0
        reply = respond(sys.argv[1] if len(sys.argv) > 1 else "", event)
    except Exception:  # Reminders are optional; never interrupt the session.
        return 0
    if reply:
        # Claude Code reads hook output as UTF-8; Windows consoles default to a legacy code page.
        sys.stdout.buffer.write(json.dumps(reply, ensure_ascii=False).encode("utf-8") + b"\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
