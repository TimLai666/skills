---
name: defuddle
description: >-
  Extract clean markdown content from web pages using Defuddle CLI, removing
  clutter and navigation to save tokens. This skill MUST be used instead of
  WebFetch when the user provides a URL to read or analyze, for online
  documentation, articles, blog posts, or any standard web page. MUST NOT be
  used for content already served as Markdown; identify it by the response
  content type and actual body rather than the URL suffix, and read it
  directly with WebFetch or curl.
metadata:
  version: "1.2.0"
---

# Defuddle

Use Defuddle CLI to extract clean readable content from web pages. Prefer over WebFetch for standard web pages — it removes navigation, ads, and clutter, reducing token usage.

If not installed, use `npx defuddle parse <url> --md`. For repeated use,
`npm install -g defuddle` is also available.

## Usage

Use `--md` for plain Markdown output:

```bash
defuddle parse <url> --md
```

Save to file:

```bash
defuddle parse <url> --md -o content.md
```

Extract specific metadata:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Format |
|------|--------|
| `--md` | Markdown (default choice) |
| `--json` | JSON with metadata, HTML in `content`, and Markdown in `contentMarkdown` |
| `--json --md` | JSON with metadata and Markdown in `content`; no separate `contentMarkdown` |
| (none) | HTML |
| `-p <name>` | Specific metadata property |
