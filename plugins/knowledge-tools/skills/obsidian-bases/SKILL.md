---
name: obsidian-bases
description: >-
  Create and edit Obsidian Bases (.base files) with views, filters, formulas,
  and summaries. This skill MUST be used when working with .base files,
  creating database-like views of notes, or when the user mentions Bases,
  table views, card views, filters, or formulas in Obsidian.
metadata:
  version: "1.2.0"
---

# Obsidian Bases Skill

## Workflow

1. Read the target `.base` file when editing, and inspect the vault's relevant note properties and conventions before creating or changing a view.
2. Define which notes belong in the base, then choose views and displayed properties. Read [Schema and Views](references/schema-and-views.md) before using nested filters, grouping, summaries or view-specific settings.
3. Add formulas when needed. Read [Properties and Formulas](references/properties-and-formulas.md) for file properties, `this`, date arithmetic and formula examples; consult [Functions Reference](references/FUNCTIONS_REFERENCE.md) for the functions actually used.
4. For a task tracker, reading list or daily-note index, read the corresponding [complete example](references/examples.md) before adapting it. Preserve the vault's actual field names and types.
5. Save a `.base` file with valid YAML in the intended vault location, then run the validation below.

## Minimal Base

A base is a YAML file with the `.base` extension. This example lists active notes
and computes a date-derived column. Adapt `status` and `due_date` to the vault.

```yaml
filters:
  and:
    - 'file.ext == "md"'
    - 'status == "active"'
formulas:
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
properties:
  formula.days_until_due:
    displayName: "Days Until Due"
views:
  - type: table
    name: "Active Notes"
    order:
      - file.name
      - status
      - formula.days_until_due
```

Global filters apply to all views; view filters further narrow that view.
The full schema and table, cards, list and map examples are in
[Schema and Views](references/schema-and-views.md). Check required plugins and
view-specific settings before choosing a view.

## Properties and Formula References

- Note properties come from frontmatter: `note.author` or `author`.
- File properties describe the file: `file.name`, `file.mtime`, etc.
- Formula properties reference definitions: `formula.my_formula` must have a matching `my_formula` entry under `formulas`.
- Inspect relevant notes for missing values and data types. A property need not exist on every note; guard optional inputs where used.

Complete file-property tables, `this` behavior and formula examples are in
[Properties and Formulas](references/properties-and-formulas.md).

## Common Pitfalls

### YAML quoting

Use single quotes around expressions containing double quotes. Quote display
strings that YAML could interpret as structure, such as a colon followed by a space.

```text
Incorrect: displayName: Status: Active
Correct:   displayName: "Status: Active"

Incorrect: label: "if(done, "Yes", "No")"
Correct:   label: 'if(done, "Yes", "No")'
```

### Duration and missing values

Subtracting dates returns a Duration. Access a numeric field such as `.days`,
`.hours`, `.minutes`, `.seconds` or `.milliseconds` before applying numeric functions.

```text
Incorrect: (now() - file.ctime).round(0)
Correct:   (now() - file.ctime).days.round(0)
```

Guard optional date inputs before converting or subtracting them:

```yaml
formulas:
  days_until_due: 'if(due_date, (date(due_date) - today()).days, "")'
```

For more date expressions, read
[Date Arithmetic](references/properties-and-formulas.md#date-arithmetic).

## Embedding Bases

```markdown
![[MyBase.base]]

<!-- Specific view -->
![[MyBase.base#View Name]]
```

## Validation

- Parse the actual `.base` as YAML. Resolve quoting errors and confirm fields contain concrete values rather than schema alternatives.
- Verify every referenced `formula.X` exists under `formulas`; check note-property names and types against the intended notes.
- Check filters, displayed columns, grouping and summaries against the requested result, including notes with missing optional values.
- Open the `.base` in Obsidian and actually inspect each affected view. Confirm formulas, filters and summaries work, then correct and recheck failures.
- If Obsidian or a required plugin is unavailable, report the unverified views or behavior. YAML parsing alone does not establish rendering or formula correctness.

## References

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)
- [Views](https://help.obsidian.md/bases/views)
- [Formulas](https://help.obsidian.md/formulas)
