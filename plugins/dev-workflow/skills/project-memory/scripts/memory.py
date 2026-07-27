#!/usr/bin/env python3
"""Shared project memory store for any agent that installs the project-memory skill.

One learning per JSON line in ~/.mystack/projects/<slug>/learnings.jsonl.
The store is agent-neutral on purpose: Claude, Codex, Cursor and others read and
write the same file, so a lesson learned in one agent is visible in the next.

Usage:
  memory.py load [--all] [--json]
  memory.py add --type T --key K --insight S --confidence N [--files a,b] [--source X] [--absorbs k1,k2]
  memory.py search QUERY [--json]
  memory.py stats
  memory.py path
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

TYPES = ("pitfall", "pattern", "preference", "architecture", "tool")
# Always expanded on load: nothing else in the project writes these down, so the
# store is the only place they exist. architecture and tool stay collapsed —
# AGENTS.md and the code itself already carry them, and spending the top of the
# output on them is spending it on something the agent is about to read anyway.
UNWRITTEN_TYPES = ("pitfall", "pattern", "preference")
GENERIC_KEYS = ("lesson", "note", "item", "memo", "learning", "entry", "thing", "misc")
ROOT = os.path.join(os.path.expanduser("~"), ".mystack", "projects")


def slug(cwd=None):
    """Stable per-project id. Falls back to the directory name when there is no remote."""
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        url = ""
    s = ""
    if url:
        url = re.sub(r"\.git$", "", url)
        m = re.search(r"[:/]([^/]+/[^/]+)$", url)
        if m:
            s = m.group(1).replace("/", "-")
    if not s:
        s = os.path.basename(os.path.abspath(cwd or os.getcwd()))
    s = re.sub(r"[^A-Za-z0-9._-]", "", s)
    return s or "unknown"


def branch(cwd=None):
    try:
        return subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def store_path(cwd=None):
    return os.path.join(ROOT, slug(cwd), "learnings.jsonl")


def read_all(path):
    """Return (entries, corrupt_line_numbers). Never raises on a damaged file."""
    entries, corrupt = [], []
    if not os.path.exists(path):
        return entries, corrupt
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                corrupt.append(n)
                continue
            if isinstance(obj, dict) and obj.get("key"):
                entries.append(obj)
            else:
                corrupt.append(n)
    return entries, corrupt


def dedupe(entries):
    """Same key wins by newest ts, matching the 'latest wins' rule in SKILL.md."""
    best = {}
    for e in entries:
        k = e["key"]
        if k not in best or e.get("ts", "") >= best[k].get("ts", ""):
            best[k] = e
    return sorted(best.values(), key=lambda e: (e.get("type", ""), e["key"]))


def absorbed_keys(entries):
    """Keys whose content has moved into a newer entry, so they stop printing alone.

    The claim only holds while it is no older than what it absorbs. That one
    comparison is what keeps a wrong merge as cheap to undo as a wrong entry:
    re-add an absorbed key later and it comes straight back. It also settles
    chains without recursion — when c absorbs b and b absorbs a, b's claim on a
    still counts here even though b itself no longer prints. Timestamps are
    whole seconds, so a merge and its undo have to land in different seconds;
    merging several entries within one second is the case that must work, and
    does.
    """
    latest = {e["key"]: e.get("ts", "") for e in entries}
    hidden = set()
    for e in entries:
        for k in e.get("absorbs") or []:
            # An entry naming itself would erase itself under >=. add rejects
            # that, but a hand-edited file can still carry it.
            if k != e["key"] and k in latest and e.get("ts", "") >= latest[k]:
                hidden.add(k)
    return hidden


def _detail(e):
    absorbs = e.get("absorbs") or []
    merged = "  (absorbs %s)" % ", ".join(absorbs) if absorbs else ""
    files = e.get("files") or []
    tail = "  [%s]" % ", ".join(files) if files else ""
    return "- **%s** (%s/10) — %s%s%s" % (
        e["key"], e.get("confidence", "?"), e.get("insight", ""), merged, tail)


def render(entries, corrupt, path, header, expand_all=False):
    """Layered by default: what only lives here in full, the rest as keys only.

    Every key is always listed. Collapsing detail is fine; hiding that an entry
    exists is not — an agent that cannot see a key will never search for it.
    """
    if not entries:
        return "NO_LEARNINGS (%s)" % path
    by_type = {}
    for e in entries:
        by_type.setdefault(e.get("type", "other"), []).append(e)
    ordered = [t for t in TYPES if t in by_type] + sorted(set(by_type) - set(TYPES))

    if expand_all:
        out = [header]
        for t in ordered:
            out.append("\n## %s" % t)
            out.extend(_detail(e) for e in by_type[t])
        if corrupt:
            out.append("\n⚠ %d unparsable line(s) skipped: %s" % (len(corrupt), corrupt))
        return "\n".join(out)

    unwritten = [e for t in ordered if t in UNWRITTEN_TYPES for e in by_type[t]]
    rest = [(t, by_type[t]) for t in ordered if t not in UNWRITTEN_TYPES]
    n_rest = sum(len(v) for _, v in rest)

    out = [header]
    if unwritten:
        out.append("\n## Only recorded here (%s)" % ", ".join(UNWRITTEN_TYPES))
        out.extend(_detail(e) for e in unwritten)
    if rest:
        out.append("\n## Index — %d more, run `search <key>` for the full text" % n_rest)
        for t, group in rest:
            out.append("- **%s**: %s" % (t, ", ".join(e["key"] for e in group)))
    if corrupt:
        out.append("\n⚠ %d unparsable line(s) skipped: %s" % (len(corrupt), corrupt))
    return "\n".join(out)


def add_reminder():
    """Closing prompt appended to `load`.

    `load` runs far more often than `add`: starting work is a moment an agent
    can detect, while "something was learned" is a judgement with no moment
    attached to it. Hanging the reminder off the one call that reliably happens
    is what gives the write half a moment of its own. It has to restate the
    command and the bar, because by the time it matters SKILL.md is tens of
    turns back in the context.
    """
    return (
        "\n---\n"
        "BEFORE THIS SESSION ENDS — record what was learned here, without waiting to be asked:\n"
        "  python3 %s add --type <pitfall|pattern|preference|architecture|tool> \\\n"
        "    --key <describes-the-lesson> --insight '<one sentence>' \\\n"
        "    --confidence <7-10> --source '<agent-or-skill-name>'\n"
        "Draft every field yourself from what actually happened and write it. Do not ask\n"
        "permission first and do not interview the user field by field; report what you\n"
        "recorded once it is in. A wrong entry is cheap: re-add the same key and the older\n"
        "one stops showing.\n"
        "Bar: confidence 7+, specific to this project, actually encountered, and\n"
        "not something AGENTS.md or the code already says.\n"
        "\"Nothing worth recording\" is a valid answer — say it out loud rather than\n"
        "skipping the decision in silence." % os.path.abspath(__file__)
    )


def cmd_load(args):
    path = store_path()
    entries, corrupt = read_all(path)
    entries = dedupe(entries)
    # Filtered here rather than inside render(), so `search` still finds an
    # absorbed entry under its old key.
    hidden = absorbed_keys(entries)
    entries = [e for e in entries if e["key"] not in hidden]
    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0
    print(render(entries, corrupt, path,
                 "# Project memory — %d learning(s)" % len(entries), expand_all=args.all))
    # --json is machine output and --all is the export path that SKILL.md pastes
    # into AGENTS.md; a prompt aimed at the current session belongs in neither.
    if not args.all:
        print(add_reminder())
    return 0


def _kebab(s):
    """Replace, never delete: silently dropping characters turns "N+1" into "n1"."""
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", s.strip().lower())).strip("-")


def cmd_add(args):
    if args.type not in TYPES:
        print("ERROR: --type must be one of %s" % ", ".join(TYPES), file=sys.stderr)
        return 2
    if not 1 <= args.confidence <= 10:
        print("ERROR: --confidence must be 1-10", file=sys.stderr)
        return 2
    key = _kebab(args.key)
    if not key:
        print("ERROR: --key must contain kebab-case characters", file=sys.stderr)
        return 2
    # load collapses most entries to their key alone, so an uninformative key is
    # invisible in practice — the agent has nothing to judge relevance by.
    # Strip a trailing number first: "db-is-postgres-15" is a real key, only the
    # generic-word-plus-counter shape ("lesson-001") carries no information.
    stem = re.sub(r"-\d+$", "", key)
    if not stem or stem in GENERIC_KEYS:
        print("ERROR: --key %r says nothing about the lesson; use a descriptive "
              "key such as 'n-plus-one-products'" % key, file=sys.stderr)
        return 2
    if len(re.sub(r"[^a-z]", "", key)) < 4:
        print("ERROR: --key %r is too short to be recognisable" % key, file=sys.stderr)
        return 2
    if key.split("-")[0] in GENERIC_KEYS:
        print("WARNING: --key starts with the generic word %r; a specific key is "
              "easier to spot in the index" % key.split("-")[0], file=sys.stderr)

    path = store_path()
    # Self-absorption would be a no-op anyway (the timestamps are equal), but it
    # reads as a typo for a key the author meant to name, so say so.
    absorbs = [k for k in (_kebab(a) for a in args.absorbs.split(",")) if k and k != key]
    if absorbs:
        known = {e["key"] for e in read_all(path)[0]}
        unknown = [k for k in absorbs if k not in known]
        if unknown:
            print("WARNING: --absorbs names %s, which is not in the store; the merge "
                  "records the claim but hides nothing" % ", ".join(unknown), file=sys.stderr)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": args.type,
        "key": key,
        "insight": args.insight.strip(),
        "confidence": args.confidence,
        "source": args.source,
        "branch": args.branch or branch(),
        "files": [f.strip() for f in args.files.split(",") if f.strip()] if args.files else [],
    }
    if absorbs:
        entry["absorbs"] = absorbs
    # json.dumps handles quotes, backslashes and newlines that hand-built JSON breaks on.
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("SAVED %s%s -> %s" % (key, " (absorbs %s)" % ", ".join(absorbs) if absorbs else "", path))
    return 0


def cmd_search(args):
    path = store_path()
    entries, corrupt = read_all(path)
    q = args.query.lower()
    hits = [e for e in dedupe(entries)
            if q in json.dumps(e, ensure_ascii=False).lower()]
    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return 0
    if not hits:
        print("NO_MATCHES for %r in %s" % (args.query, path))
        return 0
    print(render(hits, corrupt, path, "# Matches for %r — %d" % (args.query, len(hits)), expand_all=True))
    return 0


def cmd_stats(args):
    path = store_path()
    entries, corrupt = read_all(path)
    uniq = dedupe(entries)
    # Counted the same way load prints, so the two never disagree about how much
    # is actually in play. Absorbed keys are reported separately rather than
    # dropped: they are the other half of the gap between lines and keys.
    absorbed = absorbed_keys(uniq)
    live = [e for e in uniq if e["key"] not in absorbed]
    print("PATH: %s" % path)
    print("TOTAL: %d line(s), %d live key(s)%s" % (
        len(entries), len(live), ", %d absorbed" % len(absorbed) if absorbed else ""))
    # Ahead of the early return: a store whose keys are all absorbed still needs
    # to report damaged lines.
    if corrupt:
        print("CORRUPT_LINES: %s" % corrupt)
    if not live:
        return 0
    counts = {}
    for e in live:
        counts[e.get("type", "other")] = counts.get(e.get("type", "other"), 0) + 1
    for t, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("  %-14s %d" % (t, c))
    confs = [e["confidence"] for e in live if isinstance(e.get("confidence"), int)]
    if confs:
        print("AVG_CONFIDENCE: %.1f" % (sum(confs) / len(confs)))
    return 0


def cmd_path(args):
    print(store_path())
    return 0


def main():
    p = argparse.ArgumentParser(prog="memory.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    lo = sub.add_parser("load", help="print deduplicated memory for this project")
    lo.add_argument("--json", action="store_true")
    lo.add_argument("--all", action="store_true", help="expand every entry, not just the ones only recorded here")
    lo.set_defaults(func=cmd_load)

    ad = sub.add_parser("add", help="append one learning")
    ad.add_argument("--type", required=True, choices=TYPES)
    ad.add_argument("--key", required=True)
    ad.add_argument("--insight", required=True)
    ad.add_argument("--confidence", required=True, type=int)
    ad.add_argument("--files", default="")
    ad.add_argument("--source", default="user-stated")
    ad.add_argument("--branch", default="")
    ad.add_argument("--absorbs", default="",
                    help="comma-separated keys this entry now covers; they stop printing on their own line")
    ad.set_defaults(func=cmd_add)

    se = sub.add_parser("search", help="filter learnings by substring")
    se.add_argument("query")
    se.add_argument("--json", action="store_true")
    se.set_defaults(func=cmd_search)

    st = sub.add_parser("stats", help="counts and average confidence")
    st.set_defaults(func=cmd_stats)

    pa = sub.add_parser("path", help="print the store path for this project")
    pa.set_defaults(func=cmd_path)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
