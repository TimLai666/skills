#!/usr/bin/env python3
"""Compute SHA-256 of wiki page bodies (excluding YAML frontmatter).

Usage:
  # Single file — outputs one sha256 hash
  python sha256_wiki.py path/to/wiki-page.md

  # Directory — scans all .md files, outputs JSON mapping
  python sha256_wiki.py path/to/wiki/

  # Directory with custom glob
  python sha256_wiki.py path/to/wiki/ --glob "concepts/*.md"
"""

import hashlib
import json
import sys
import os
import glob as globmod


def extract_body(content: str) -> str:
    """Extract body content after YAML frontmatter."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return content


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 of file body (excluding frontmatter)."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    body = extract_body(content)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def scan_directory(dirpath: str, pattern: str = "*.md") -> dict:
    """Scan directory and compute sha256 for all matching files."""
    results = {}
    search = os.path.join(dirpath, "**", pattern)
    for filepath in globmod.glob(search, recursive=True):
        relpath = os.path.relpath(filepath, dirpath).replace("\\", "/")
        try:
            results[relpath] = compute_sha256(filepath)
        except Exception as e:
            results[relpath] = f"ERROR: {e}"
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: sha256_wiki.py <file-or-directory> [--glob pattern]", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    pattern = "*.md"

    if "--glob" in sys.argv:
        idx = sys.argv.index("--glob")
        if idx + 1 < len(sys.argv):
            pattern = sys.argv[idx + 1]

    if os.path.isfile(target):
        print(compute_sha256(target))
    elif os.path.isdir(target):
        results = scan_directory(target, pattern)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"Error: {target} not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
