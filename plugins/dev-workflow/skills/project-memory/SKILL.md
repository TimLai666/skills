---
name: project-memory
description: "Shared cross-agent project memory — pitfalls, patterns and preferences recorded once and readable by any agent that installs this skill. This skill MUST be invoked before starting work in an existing project, to load what was already learned there. MUST also be invoked on the triggers below to record something new, and SHOULD be invoked whenever the user states something worth remembering about how this project behaves. Triggers on: 記一下, 之前踩過什麼雷, 學到什麼, 有什麼教訓, remember this, lesson learned, project learnings, 記錄一下, 之前遇過的, 把這個記起來"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  version: "1.5.0"
---

## Why this store and not the agent's own memory

Every agent has its own memory, and no agent can read another's. A lesson Claude
learns is invisible to Codex, and the reverse. This skill keeps one plain JSONL
file outside all of them, so whichever agent is driving today reads what
yesterday's agent learned.

That only works if every agent **loads** the file, not just writes to it. Loading
is the first half of this skill, not an optional extra.

---

## Auto-trigger

Two situations, both mandatory.

1. **Starting work in a project** — run `load` before reading code or making
   changes. Do this without being asked.
2. **Something was learned** — the user hits a pitfall, discovers a pattern,
   states a preference, or says 記一下 / remember this. Run `add`.

---

## The script

All reads and writes go through `scripts/memory.py` in this skill's own
directory. Do not hand-build JSON with `echo` — an insight containing a quote or
backslash silently corrupts the file.

Requires `python3` (stdlib only, no packages). If it is missing, say so rather
than falling back to shell string-building.

```bash
_MEM="<this skill's directory>/scripts/memory.py"
python3 "$_MEM" --help
```

| Command | What it does |
|---|---|
| `load` | Print this project's memory, deduplicated by key, layered |
| `load --all` | Same but every entry expanded |
| `load --json` | Same, as a JSON array |
| `add` | Append one learning |
| `search QUERY` | Filter learnings by substring |
| `stats` | Counts by type and average confidence |
| `path` | Print the store path for this project |
| `projectdir [--mkdir]` | Print this project's shared directory |

`projectdir` exists for the other dev-workflow skills. `feature-planner` writes
its plan document there and `eng-architect` reads it back; both call this rather
than deriving the slug themselves, because three copy-pasted shell derivations
had already drifted into two different behaviours.

---

## Load (do this first)

```bash
python3 "$_MEM" load
```

The output is layered. `architecture` and `preference` hold for the whole project,
so they print in full — you need them before touching anything. Everything else is
situational and prints as a bare key list:

```
## Project-wide (architecture, preference)
- **no-orm-raw-sql** (9/10) — this project deliberately avoids an ORM

## Index — 42 more, run `search <key>` for the full text
- **pitfall**: n-plus-one-products, tz-naive-timestamps, redis-pool-size
- **tool**: rg-over-grep
```

Every key is always listed, however large the store gets. Collapsing detail is
fine; hiding that an entry exists is not — a key you cannot see is one you will
never search for. When a key looks related to what you are about to do, run
`search <key>` before you touch that area.

Already deduplicated: same key, newest wins. `NO_LEARNINGS` means a fresh
project; carry on. Damaged lines are skipped and reported rather than aborting.

`--all` expands everything, for when you want to read the whole store.

---

## Add

Ask for whatever the user has not already given, one question at a time:

1. **Type** — `architecture` and `preference` are project-wide and always load in
   full; `pitfall`, `pattern` and `tool` are situational and load as keys only.
   Pick by scope, not by how important it feels.
2. **Key** — kebab-case, and it must describe the lesson. Most entries appear in
   `load` as nothing but their key, so `lesson-001` is invisible in practice
   while `n-plus-one-products` is findable. The script rejects generic and
   numbered keys.
3. **Insight** — one sentence
4. **Confidence** — 1-10

```bash
python3 "$_MEM" add \
  --type pitfall \
  --key n-plus-one-products \
  --insight 'Product.includes(:variants) needed in catalog controller — N+1 caused 3s load' \
  --confidence 9 \
  --files 'app/controllers/catalog_controller.rb'
```

The script fills in timestamp, branch and slug. `--source` defaults to
`user-stated`; other skills should pass their own name.

Re-adding an existing key is how you update it. `load` shows only the newest.

---

## What is worth recording

- Confidence 7 or above only.
- Project-specific lessons only. General programming knowledge does not belong here.
- Real pitfalls actually hit, or patterns that actually worked.
- Not task lists and not open bugs — those belong in the project's issue tracker
  or its `AGENTS.md`.

---

## Where it lives

`~/.mystack/projects/<slug>/learnings.jsonl`, one JSON object per line:

```json
{"ts":"2026-04-04T10:00:00Z","type":"pitfall","key":"n-plus-one-products","insight":"Product.includes(:variants) needed in catalog controller","confidence":9,"source":"user-stated","branch":"feat/catalog","files":["app/controllers/catalog_controller.rb"]}
```

`<slug>` comes from the git remote (`org-repo`), falling back to the directory
name when there is no remote. Run `python3 "$_MEM" path` to see it.

The format is deliberately boring: append-only, one line per learning, no index
and no lock. Any agent, in any language, can read it.

---

## How other skills and agents record learnings

One call, no format duplication:

```bash
python3 <project-memory>/scripts/memory.py add \
  --type pitfall --key '<key>' --insight '<one sentence>' \
  --confidence 8 --source '<skill-or-agent-name>' --files '<file>'
```

Same rules apply: confidence 7 or above, project-specific, actually encountered.

---

## Export

Turn the memory into markdown for a `CLAUDE.md`, `AGENTS.md` or handover doc:

```bash
python3 "$_MEM" load --all
```

`--all` matters here: the default view collapses most entries to their key, which
is right for loading context and wrong for a handover document.

The output is already markdown. Copy it, or append it to the target file if the
user asks. Never append automatically — that file is version-controlled and
shared with other people.
