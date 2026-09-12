# Output Contracts

## Global Rule

Deliver the requested result first. The complete templates below support full analyses, plans, and multi-part requests; select sections that serve the task rather than automatically returning every heading. For rewriting, default to the revised text and a brief explanation of material changes when useful. For production, default to the finished draft or script and necessary usage notes.

If important inputs are missing but the user asked for a fast draft, start with:

```md
## Assumptions
- ...
```

Only include this section when assumptions are actually being made.

## `analyze`

Full output template:

```md
## Content Formula
## Hook Patterns
## Pacing And Structure Pattern
## Tone And Style Notes
## Retention Or Share Drivers
## Content Gaps
## Reusable Rules
```

## `ideate`

Full output template:

```md
## Positioning Line
## Angle Set
## Topic Slate
## Naming Options
## Recommended Direction
```

Notes:

- include `Naming Options` only when relevant
- use `10` topic ideas by default when the user asks for topic generation without a specific count

## `rewrite`

Full output template:

```md
## Revision Strategy
## Revised Structure
## Upgraded Hook
## Stronger Transitions
## Screenshot Or Share Points
## Final Polished Version
```

Notes:

- omit `Screenshot Or Share Points` if not relevant to the channel
- preserve the user's intended meaning unless they asked for repositioning

## `package`

Full output template:

```md
## Title Set
## Hook Set
## Thumbnail Concepts
## CTA Options
## Interaction Prompts
## Recommended Priority Order
```

Notes:

- if the user only asks for one packaging layer, do not force all sections
- ranking is optional unless the user asks for prioritization

## `produce`

Full output template:

```md
## Content Strategy
## Final Draft Or Script
## Scene Or Visual Tags
## Retention Beats
## CTA Placement
```

Notes:

- `Scene Or Visual Tags` are mainly for video or highly visual social assets
- `Retention Beats` are most relevant for long-form video and some threaded content

## `system`

Full output template:

```md
## Workflow
## Tool And Prompt Stack
## Batch Cadence
## Budget Breakdown
## Operational Risks
```

Notes:

- if the user requests a `3-hour SOP`, include timeboxing by stage
- if the user requests budget guidance, separate fixed and variable costs when possible
