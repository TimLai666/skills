---
name: review-salience-xlsx
description: >
  Use this skill when the user has product review files and wants to score each
  review on a set of attributes using a salience scale (0–7), then export the
  result as a review × attribute matrix in Excel (.xlsx). Trigger on requests
  like 「逐則評論評分」、「顯著度矩陣」、「salience scoring」、「評論×屬性 Excel」, or whenever
  the user wants to know how prominently each attribute is mentioned in each
  individual review. Also trigger when this step follows an attribute-discovery
  workflow and the user wants to turn the attribute catalog into scored data.
  Use this skill even if the user only mentions part of the pipeline (e.g.
  "score the reviews" or "make an Excel matrix").
---

# Review Salience → Excel Matrix

Converts a review corpus and a frozen attribute catalog into a **review × attribute
salience matrix** exported as `.xlsx`.

Salience measures *how prominently* a reviewer mentions an attribute — not
sentiment. Each cell is an integer 0–7:

| Score | Meaning |
|-------|---------|
| 0 | Attribute not mentioned at all |
| 1–3 | Slight or indirect mention |
| 4 | Neutral or ambiguous mention |
| 5–6 | Clearly and explicitly mentioned |
| 7 | Strongly and fully emphasised |

For the Excel output format, read `references/xlsx-format.md`.  
For a worked example (safety-eyewear corpus, 923 reviews, 30 attributes), read `references/worked-example.md`.

---

## Concepts

### Attribute catalog
A frozen, ordered list of attributes produced upstream (e.g. by the
`review-scoring-docx` skill). Each attribute has an `id` (zero-padded, e.g.
`01`) and a `label`. The catalog **must not change** after scoring begins.

### Scorer
The component that reads one review and returns 30 integers. This skill is
**scorer-agnostic**: Claude reads and scores by default, but the architecture
supports swapping in any external scorer without changing the rest of the pipeline.
See [Scorer contract](#scorer-contract) below.

### Salience matrix
A table with one row per review and one column per attribute, plus metadata
columns (`review_id`, `product`, `review_text`). Column names follow the pattern
`s01`, `s02` … `s30` (or however many attributes exist).

---

## Workflow

### Step 0 — Locate required skills
Check your available skills for an **xlsx skill** (covers `.xlsx` or spreadsheet
creation). Read its SKILL.md before writing any Excel code.

### Step 1 — Ingest reviews

Load all reviews for each product. Never truncate. Accept all languages.

```python
import csv

def load_reviews(filepath):
    candidates = ['body', 'Body', 'review', 'text', 'content']
    with open(filepath, encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        col = next((c for c in candidates if c in reader.fieldnames), None)
        if col is None:
            raise ValueError(f"No text column found. Headers: {reader.fieldnames}")
        return [r[col].strip() for r in reader
                if r[col].strip() and len(r[col].strip()) > 15]
```

Print a per-product count summary before proceeding.

### Step 2 — Confirm the attribute catalog

Either receive the catalog from upstream (e.g. from the `review-scoring-docx`
skill output) or rediscover it by reading the corpus. The catalog must be frozen
as an ordered list before scoring starts:

```python
ATTRS = [
    ("01", "attribute label 1"),
    ("02", "attribute label 2"),
    # ...
]
```

### Step 3 — Score reviews  ← swap point for external scorers

This is the **scorer contract boundary**. Anything that satisfies the contract
below can replace Claude's built-in scoring.

#### Scorer contract

**Input:** a single review string (any language)  
**Output:** a list of integers, one per attribute, in catalog order, each in
range 0–7

**Built-in scorer (Claude reads semantically):**

Read each review, understand its meaning, and assign a score per attribute.
Do not use keyword matching. Consider the full semantic content including
negations, comparisons, and implicit references. See `references/worked-example.md`
for calibration examples.

**External scorer (n8n / API / other service):**

If the user has connected an external scoring service, call it instead.
The external scorer must return the same contract: a list of N integers per review.
See `references/external-scorer.md` for integration patterns (n8n webhook,
REST API, batch CSV round-trip).

#### Scoring loop

```python
import json

# scores[product_id] = list of lists; each inner list has len == len(ATTRS)
scores = {}
for pid, reviews in all_reviews.items():
    scores[pid] = []
    for review_text in reviews:
        row_scores = score_one_review(review_text, ATTRS)  # scorer contract
        scores[pid].append(row_scores)
```

Save progress incrementally if scoring a large corpus (> 200 reviews).

### Step 4 — Build the Excel file

Read the xlsx skill (Step 0) for the full openpyxl API reference.
See `references/xlsx-format.md` for the exact sheet structure and colour scheme.

The workbook has two sheets:

**Sheet 1 — Full matrix** (`評論×屬性 顯著度矩陣`)
- Columns: `review_id` | `product` | `salience_sum` (Excel SUM formula) | `review_text` (truncated) | `s01` … `sN`
- Freeze panes at column E, row 3
- Colour-scale conditional formatting on score columns: white (0) → yellow (mid) → orange (max)

**Sheet 2 — Product summary** (`產品×屬性 平均顯著度`)
- Mean salience per product per attribute
- Same conditional formatting
- One row per product, labelled with review count

### Step 5 — Output

Save to `/home/claude/salience_matrix.xlsx`, copy to `/mnt/user-data/outputs/`,
then call `present_files`.

Accompany with a prose summary stating:
- Total reviews scored, per product
- Languages present in the corpus
- Top 5 attributes by mean salience (most-discussed)
- Any attributes with near-zero salience across all products (possible catalog gap)

---

## Hard rules

1. **Never truncate reviews.** Every valid review (> 15 chars) must be scored.
2. **All languages count.** Do not filter by language.
3. **Catalog is frozen before scoring.** No mid-run additions or reordering.
4. **Integer scores only.** Each cell is a whole number 0–7.
5. **Scorer is swappable.** The rest of the pipeline must not assume Claude is
   the scorer. Pass reviews through the scorer contract; don't hard-code logic.
6. **Use absolute column widths.** Percentage widths break in Google Sheets.
7. **Present with `present_files`.** Never ask the user to navigate to the file.
