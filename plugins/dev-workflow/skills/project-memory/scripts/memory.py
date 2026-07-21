#!/usr/bin/env python3
"""Shared project memory store for any agent that installs the project-memory skill.

One learning per JSON line in ~/.mystack/projects/<slug>/learnings.jsonl.
The store is agent-neutral on purpose: Claude, Codex, Cursor and others read and
write the same file, so a lesson learned in one agent is visible in the next.

Usage:
  memory.py load [--all] [--json]
  memory.py add --type T --key K --insight S --confidence N [--files a,b] [--source X]
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

TYPES = ("pattern", "pitfall", "preference", "architecture", "tool")
# Always expanded on load: these hold for the whole project, so an agent needs
# them before touching anything. The rest are situational and stay collapsed.
PROJECT_TYPES = ("architecture", "preference")
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


def _detail(e):
    files = e.get("files") or []
    tail = "  [%s]" % ", ".join(files) if files else ""
    return "- **%s** (%s/10) — %s%s" % (e["key"], e.get("confidence", "?"), e.get("insight", ""), tail)


def render(entries, corrupt, path, header, expand_all=False):
    """Layered by default: project-wide entries in full, the rest as keys only.

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

    wide = [e for t in ordered if t in PROJECT_TYPES for e in by_type[t]]
    rest = [(t, by_type[t]) for t in ordered if t not in PROJECT_TYPES]
    n_rest = sum(len(v) for _, v in rest)

    out = [header]
    if wide:
        out.append("\n## Project-wide (%s)" % ", ".join(PROJECT_TYPES))
        out.extend(_detail(e) for e in wide)
    if rest:
        out.append("\n## Index — %d more, run `search <key>` for the full text" % n_rest)
        for t, group in rest:
            out.append("- **%s**: %s" % (t, ", ".join(e["key"] for e in group)))
    if corrupt:
        out.append("\n⚠ %d unparsable line(s) skipped: %s" % (len(corrupt), corrupt))
    return "\n".join(out)


def cmd_load(args):
    path = store_path()
    entries, corrupt = read_all(path)
    entries = dedupe(entries)
    if args.json:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
        return 0
    print(render(entries, corrupt, path,
                 "# Project memory — %d learning(s)" % len(entries), expand_all=args.all))
    return 0


def cmd_add(args):
    if args.type not in TYPES:
        print("ERROR: --type must be one of %s" % ", ".join(TYPES), file=sys.stderr)
        return 2
    if not 1 <= args.confidence <= 10:
        print("ERROR: --confidence must be 1-10", file=sys.stderr)
        return 2
    # Replace, never delete: silently dropping characters turns "N+1" into "n1".
    key = re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", args.key.strip().lower())).strip("-")
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
    # json.dumps handles quotes, backslashes and newlines that hand-built JSON breaks on.
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("SAVED %s -> %s" % (key, path))
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
    print("PATH: %s" % path)
    print("TOTAL: %d line(s), %d unique key(s)" % (len(entries), len(uniq)))
    if not uniq:
        return 0
    counts = {}
    for e in uniq:
        counts[e.get("type", "other")] = counts.get(e.get("type", "other"), 0) + 1
    for t, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("  %-14s %d" % (t, c))
    confs = [e["confidence"] for e in uniq if isinstance(e.get("confidence"), int)]
    if confs:
        print("AVG_CONFIDENCE: %.1f" % (sum(confs) / len(confs)))
    if corrupt:
        print("CORRUPT_LINES: %s" % corrupt)
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
    lo.add_argument("--all", action="store_true", help="expand every entry, not just project-wide ones")
    lo.set_defaults(func=cmd_load)

    ad = sub.add_parser("add", help="append one learning")
    ad.add_argument("--type", required=True, choices=TYPES)
    ad.add_argument("--key", required=True)
    ad.add_argument("--insight", required=True)
    ad.add_argument("--confidence", required=True, type=int)
    ad.add_argument("--files", default="")
    ad.add_argument("--source", default="user-stated")
    ad.add_argument("--branch", default="")
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
