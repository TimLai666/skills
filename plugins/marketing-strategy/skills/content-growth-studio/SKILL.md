---
name: content-growth-studio
description: >-
  This skill MUST be used for growth-oriented article, video, newsletter, and
  social content work, including content analysis, ideation, rewriting,
  packaging, production, repurposing, and repeatable editorial workflows.
  MUST trigger on natural-language requests such as 幫影片想標題、拆解成功內容、
  規劃內容主題、把文章改成社群貼文、設計內容生產流程; users need not name the skill
  or explicitly say growth. SHOULD be used when the context calls for improving
  content reach, retention, engagement, or conversion. MUST NOT trigger solely
  because a request contains a URL, notes, or general proofreading without
  a content-growth purpose. Supports source-led and brief-led work.
metadata:
  version: "1.2.0"
---

# Content Growth Studio

## Overview

Orchestrate article, video, newsletter, and social content work from existing
material or a brief. Select the mode from the user's intended outcome, shape the
content for its audience and channel, and assemble one coherent deliverable.

## Input Contract

Need at least one of `source_artifacts` or `topic_or_subject`. Determine the
`target_audience`, `primary_channel`, `goal`, `brand_or_voice`, and `constraints`
from the request and available material where possible.

- `source-led`: URLs, transcripts, articles, scripts, title plus outline,
  competitor examples, notes, or review/support/social evidence.
- `brief-led`: topic, audience, channel, goal, voice, and constraints.
- When both are present, use the sources to calibrate the brief.

For structured inputs or mode-specific missing information, read
[Input Contracts And Gates](./references/02-input-contracts-and-gates.md).
These fields describe working inputs, not a form the user must fill out.

## Data Sufficiency Gate

Proceed when the information supports a useful result. State only assumptions
that are actually needed and materially affect the output, with no fixed count.
Ask concise questions only when missing information blocks the requested result.
For a quick draft, use reasonable stated assumptions where possible and continue.

Never invent performance results, source facts, unobserved competitor data, or
supposedly evidence-backed audience insights. If linked material is inaccessible,
request a transcript, excerpt, notes, or screenshots for work that depends on it.

## Workflow

### Select The Mode

Use `mode: auto` by default. Infer the mode from natural language and the requested
result. Combine modes when the request requires them, keeping the delivery within
its scope. Read the relevant section of each linked reference before that work.

| Mode | Intended result | Read before execution |
| --- | --- | --- |
| `analyze` | Content teardown, source comparison, reusable formulas | [Source analysis](./references/03-source-analysis-playbook.md), including its full analysis dimensions |
| `ideate` | Positioning, topics, series, names, or angles | [Channel playbooks](./references/04-channel-playbooks.md) for the target channel |
| `rewrite` | Improve an existing draft while preserving its intent | [Source analysis](./references/03-source-analysis-playbook.md) and the target [channel playbook](./references/04-channel-playbooks.md) |
| `package` | Titles, hooks, thumbnails, CTA, or interaction prompts | [Packaging systems](./references/05-packaging-systems.md) and the target [channel playbook](./references/04-channel-playbooks.md) |
| `produce` | Finished article, script, post, or cross-channel adaptation | Target [channel playbooks](./references/04-channel-playbooks.md); also [source analysis](./references/03-source-analysis-playbook.md) when working from existing material |
| `system` | Editorial workflow, cadence, tools, time or budget plan | The `system` section of [Output Contracts](./references/06-output-contracts.md) |

For ambiguous requests or detailed scenario examples, read
[Scope And Mode Routing](./references/01-scope-and-mode-routing.md).

### Execute And Assemble

1. Identify the audience, core promise, source meaning, and channel requirements.
2. Apply the chosen mode and relevant channel rules. For title or hook work within
   another mode, read [Packaging Systems](./references/05-packaging-systems.md).
3. When audience research, psychology, theory coding, or another specialty needs
   deeper work, read [Handoff Matrix](./references/07-handoff-matrix.md) before
   selecting a specialist. It specifies the input to provide and expected return.
   Page construction belongs to `landing-page-studio`; this skill handles its
   content package when requested.
4. Assemble the result using the output rules below. Check source fidelity,
   channel fit, and whether the packaging fulfills the content's actual promise.

## Output Contract

Deliver the requested result first. For rewriting, default to the revised text
with a brief explanation of material changes when useful. For production, provide
the finished draft or script and the notes needed to use it.

For a full analysis, planning package, or multi-part deliverable, read the selected
mode in [Output Contracts](./references/06-output-contracts.md). Its complete
section templates are available when appropriate; choose sections that serve the
request. A title-only request calls for titles, not a full packaging report.

## Quality Rules

- Default to Traditional Chinese with Taiwan phrasing unless the user's material
  clearly indicates another language.
- Preserve source meaning in `rewrite` unless repositioning is requested.
- Match structure, opening speed, pacing, evidence, and CTA to the target channel.
  Cross-channel adaptations retain the core promise while changing its delivery.
- Tie titles and hooks to what the content actually delivers. Explain ranking
  logic briefly when prioritization is requested.
- Keep observations separate from predictions about retention, sharing, or
  conversion; persuasive structure alone does not establish actual performance.
- Integrate specialist results into the requested deliverable.

## Quick Reference

- [Scope and mode examples](./references/01-scope-and-mode-routing.md): ambiguous
  requests and boundaries with other skills.
- [Input contracts](./references/02-input-contracts-and-gates.md): structured input
  fields and missing-data handling by mode.
- [Source analysis](./references/03-source-analysis-playbook.md): full analysis
  method and source-specific handling.
- [Channel playbooks](./references/04-channel-playbooks.md): article/newsletter,
  long video, short video, and social delivery rules.
- [Packaging systems](./references/05-packaging-systems.md): title and hook
  families, thumbnails, CTA, and interaction assets.
- [Output contracts](./references/06-output-contracts.md): complete mode templates
  for analyses, plans, and multi-part deliveries.
- [Handoff matrix](./references/07-handoff-matrix.md): specialist selection,
  required inputs, and expected results.
