---
name: project-memory
description: "Shared cross-agent project memory — pitfalls, patterns and preferences recorded once and readable by any agent that installs this skill. This skill MUST be invoked before starting work in an existing project, to load what was already learned there, and MUST be invoked again as that work wraps up, to record what this session learned before it ends. MUST also be invoked on the triggers below to record something new, and SHOULD be invoked whenever the user states something worth remembering about how this project behaves. MUST NOT be used for task lists or open bugs, which belong in the issue tracker or AGENTS.md. Triggers on: 記一下, 之前踩過什麼雷, 學到什麼, 有什麼教訓, remember this, lesson learned, project learnings, 記錄一下, 之前遇過的, 把這個記起來"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  version: "1.9.0"
---

## Why this store and not the agent's own memory

Every agent has its own memory, and no agent can read another's. A lesson Claude
learns is invisible to Codex, and the reverse. This skill keeps one plain JSONL
file outside all of them, so whichever agent is driving today reads what
yesterday's agent learned.

That only works if every agent **loads** the file, not just writes to it. Loading
is the first half of this skill, not an optional extra.

---

## Two mandatory moves

Two situations, both mandatory.

1. **Starting work in a project** — run `load` before reading code or making
   changes. Do this without being asked.
2. **Work wraps up, or the moment something is learned** — whichever comes
   first. The user hits a pitfall, discovers a pattern, states a preference, or
   says 記一下 / remember this. Run `add`.

The end of a session is a checkpoint, not a courtesy: decide out loud whether
anything is worth keeping, and answer "nothing this time" when that is true.
Skipping the decision in silence is how this store loses most of its entries.

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
| `add` | Append one learning, optionally merging older ones into it |
| `search QUERY` | Filter learnings by substring |
| `stats` | Counts by type and average confidence |
| `path` | Print the store path for this project |

---

## Load (do this first)

```bash
python3 "$_MEM" load
```

The output is layered by where else the knowledge exists. `pitfall`, `pattern` and
`preference` print in full, because nothing else in the project writes them down.
`architecture` and `tool` print as a bare key list, because `AGENTS.md` and the
code already carry them and the agent is about to read those anyway:

```
## Only recorded here (pitfall, pattern, preference)
- **n-plus-one-products** (9/10) — Product.includes(:variants) needed in catalog controller

## Index — 42 more, run `search <key>` for the full text
- **architecture**: no-orm-raw-sql, events-are-append-only
- **tool**: rg-over-grep
```

Every key is always listed, however large the store gets. Collapsing detail is
fine; hiding that an entry exists is not — a key you cannot see is one you will
never search for. When a key looks related to what you are about to do, run
`search <key>` before you touch that area.

Already deduplicated: same key, newest wins. `NO_LEARNINGS` means a fresh
project; carry on. Damaged lines are skipped and reported rather than aborting.

`--all` expands everything, for when you want to read the whole store.

`load` closes with a reminder to record what this session learns. That is
deliberate. `load` fires far more reliably than `add`, because starting work is
a moment an agent can detect while "something was learned" is a judgement with
no moment attached to it, so the write half borrows a moment from the read half.
`--json` and `--all` skip the reminder, being machine output and export.

---

## Add

Draft all four fields yourself from what actually happened and write the entry.
Do not ask permission first, and do not walk the user through the fields one
question at a time. Every question at this point is another reason the entry
never gets written, and a wrong entry is cheap to fix: re-add the same key and
`load` shows only the newest. Report what you recorded once it is in.

1. **Type** — `pitfall` for something that actually went wrong, `pattern` for a
   way of working that turned out to hold, `preference` for how the user wants
   things done. Those three load in full. `architecture` and `tool` describe how
   the project is put together and load as keys only, because a file in the repo
   already says it. Pick by which of those the entry is, not by how important it
   feels or by which one gets shown.
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

## Merging entries

Merge two entries when they turn out to have the same root cause, not when the
output feels long. The merged insight has to carry the specifics that made each
one worth keeping — the number, the file, the thing that actually broke.
Collapsing two concrete lessons into one general statement throws away the only
thing this store holds that `AGENTS.md` does not.

A merge is an ordinary `add` that names what it now covers:

```bash
python3 "$_MEM" add \
  --type pitfall \
  --key skill-instructions-need-an-execution-point \
  --insight '<one sentence, keeping the specifics from both>' \
  --confidence 8 \
  --absorbs 'skill-write-actions-need-a-moment,printed-suggestion-is-not-an-executed-step'
```

The absorbed keys stop taking a line of their own and print after the merged
entry instead, so nothing drops out of the output and `search` still finds them
under their old keys. No line ever leaves the file. This is not a delete: re-add
an absorbed key with a fresh timestamp and it stands on its own again.

---

## What is worth recording

- Confidence 7 or above only.
- Project-specific lessons only. General programming knowledge does not belong here.
- Would the line be at home in `AGENTS.md`? Then write it there instead. This
  store is for what only surfaces while doing the work: what broke, what the fix
  turned out to be, what the user wants done differently next time.
- Real pitfalls actually hit, patterns that actually held up, preferences the
  user actually stated.
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
