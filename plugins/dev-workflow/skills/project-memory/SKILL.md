---
name: project-memory
description: "Capture and retrieve project learnings. Record pitfalls, patterns, and preferences from real work. Triggers on: 記一下, 之前踩過什麼雷, 學到什麼, 有什麼教訓, remember this, lesson learned, project learnings, 記錄一下, 之前遇過的, 把這個記起來"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  version: "1.0.0"
---

## Auto-trigger

When the user encounters a pitfall, discovers a pattern, or wants to record something learned during development, activate immediately.

---

## Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|;s|.*[:/]\([^/]*/[^/]*\)$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' 2>/dev/null || basename "$PWD")
_LEARN_FILE="$HOME/.mystack/projects/$_SLUG/learnings.jsonl"
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
echo "LEARN_FILE: $_LEARN_FILE"
[ -f "$_LEARN_FILE" ] && echo "TOTAL: $(wc -l < $_LEARN_FILE | tr -d ' ') entries" || echo "TOTAL: 0 entries"
mkdir -p "$HOME/.mystack/projects/$_SLUG"
```

---

## Learning format

Each learning is one JSON line in `~/.mystack/projects/<slug>/learnings.jsonl`:

```json
{"ts":"2026-04-04T10:00:00Z","type":"pitfall","key":"n-plus-one-products","insight":"Product.includes(:variants) needed in catalog controller — N+1 caused 3s load time","confidence":9,"branch":"feat/catalog","files":["app/controllers/catalog_controller.rb"]}
```

Fields:
- `type`: `pattern` | `pitfall` | `preference` | `architecture` | `tool`
- `key`: kebab-case slug
- `insight`: one sentence
- `confidence`: 1-10
- `source`: which skill captured it, or `user-stated`
- `files`: related files

Deduplicate by `key`; latest wins.

---

## Commands

### Add a learning (default when triggered)

Ask (one at a time if needed):
1. **Type** — pattern / pitfall / preference / architecture / tool
2. **Key** — kebab-case slug (suggest one based on context)
3. **Insight** — one sentence
4. **Confidence** — 1-10

Then append:

```bash
_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "{\"ts\":\"$_TS\",\"type\":\"<type>\",\"key\":\"<key>\",\"insight\":\"<insight>\",\"confidence\":<n>,\"source\":\"user-stated\",\"branch\":\"$_BRANCH\",\"files\":[<files>]}" >> "$_LEARN_FILE"
```

### Search

```bash
_QUERY="<user's search terms>"
grep -i "$_QUERY" "$_LEARN_FILE" 2>/dev/null | tail -20 || echo "NO_MATCHES"
```

Display grouped by type, deduplicated by key.

### Show recent

```bash
[ -f "$_LEARN_FILE" ] && tail -50 "$_LEARN_FILE" || echo "NO_LEARNINGS"
```

### Stats

Count unique learnings, breakdown by type, average confidence.

### Export

Format all learnings as markdown suitable for `CLAUDE.md`. Offer:
- copy to clipboard
- append to `CLAUDE.md`
- save as `learnings-export.md`

---

## How other skills capture learnings

Skills can append to the learnings file when they discover something valuable:

```bash
_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
_SLUG=$(git remote get-url origin 2>/dev/null | sed 's|.*[:/]\([^/]*/[^/]*\)\.git$|\1|' | tr '/' '-' | tr -cd 'a-zA-Z0-9._-' || basename "$PWD")
echo "{\"ts\":\"$_TS\",\"skill\":\"<skill>\",\"type\":\"pitfall\",\"key\":\"<key>\",\"insight\":\"<insight>\",\"confidence\":<n>,\"source\":\"<skill>\",\"branch\":\"$(git branch --show-current 2>/dev/null)\",\"files\":[\"<file>\"]}" >> "$HOME/.mystack/projects/$_SLUG/learnings.jsonl"
```

Guidelines:
- only capture confidence >= 7
- only project-specific lessons
- only real encountered pitfalls or successful patterns

---

## Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"project-memory\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
