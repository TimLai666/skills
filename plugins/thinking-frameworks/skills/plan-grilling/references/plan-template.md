# Plan and decision templates

Use a saved plan only when requested or when an identified reader needs it for
execution or handoff. Update the existing plan when one exists. Use the sections
needed for the current decision; omit empty sections and details expressed by
the implementation. Follow the user's requested coverage and format.

## Short plan

```markdown
# Plan: [intended outcome]

## Goal and constraints
[Problem, who encounters it, desired result and constraints that affect action]

## Next step
[Small usable or executable outcome, or experiment, and its scope]
[Only the dependencies and effort limit needed to take this step]

## How to evaluate it
[Observable acceptance criterion or uncertainty to resolve, and how to check it]
[How the result determines whether to continue, adjust or reconsider]

## Unresolved items
[If relevant: what blocks this step and needs a decision]
[What can wait, and what evidence or dependency makes it relevant]
```

## Decision record

Add a record only for a consequential choice whose reason is not evident from
the implementation. Consolidate repeated discussion into the current decision.

```markdown
### [Decision topic]
- Decision: [what was agreed]
- Reason: [evidence and consequential tradeoff]
- Revisit when: [if relevant, the evidence that would change the decision]
```

## Result update

After an authorized step, update its outcome and the next action in place.
Record what was observed, which assumption it supports or contradicts, and what
remains before the overall goal is complete. Link to relevant implementation
or validation evidence instead of duplicating implementation details.
