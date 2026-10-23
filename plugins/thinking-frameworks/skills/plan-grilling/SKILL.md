---
name: plan-grilling
description: >-
  This skill MUST be used to clarify or pressure-test a plan and identify the
  next useful, verifiable step, including requests such as 幫我規劃、規劃一下、
  幫我想一下、這個怎麼做、逼問我、壓力測試這個計畫、幫我想這個功能、grill me、
  planning mode、動手之前先想清楚.
  It SHOULD also be used when the user thinks aloud about a feature, campaign,
  proposal, process change, or personal decision with unresolved choices.
  It MUST NOT reopen settled decisions or turn an already authorized execution
  task into a new planning interview.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
metadata:
  version: "2.5.0"
---

## Overview

Clarify the goal and plan far enough to take the next useful, verifiable step.
Use implementation, experiments and observed results to resolve uncertainties
that discussion cannot settle. Apply this to features, campaigns, proposals,
process changes, hiring and personal decisions.

## Input Contract

Identify the intended outcome, current scope, constraints, success criteria
and decisions already made. Read available files, code, configuration and
other relevant evidence before asking the user for facts.

Use the requested format. Keep a short plan in the chat unless the user asks
for a document or an identified reader needs it for execution or handoff.
For a saved plan, use the user's chosen location or existing project convention;
otherwise use `docs/plan-grilling/<slug>-plan.md`. Ask for a location only when
saving is needed and no workspace is clear. Read before updating and preserve
unrelated content. Keep the same path as the plan evolves.

## Workflow

### 1. Identify what blocks the next step

Read [Interview guide](references/interview-guide.md) when deciding what needs
clarification. Establish the problem, who encounters it and the result sought.
Check assumptions and consequences that could change the immediate direction.
Confirm a meaningful change to the intended outcome before proceeding.

Distinguish a user decision from a fact that can be checked and an uncertainty
that needs an experiment. Resolve available facts yourself. Decide reversible,
low-cost implementation details within the authorized scope yourself.

### 2. Ask only where an answer is needed now

Ask when different answers would change the next action, its acceptance or a
costly commitment. Compare the cost and value of another question with checking
evidence or running a small experiment. Prefer an experiment when it can answer
the uncertainty more reliably at lower cost within the authorized scope.

Ask one question at a time and wait for the answer. State the consequential
choice and give a recommendation with its tradeoff. For missing experience or
context, ask a plain question rather than inventing options. Follow-ups target
a contradiction, consequential assumption or ambiguity in the answer.

Keep settled decisions closed unless new evidence contradicts them. Defer
questions about later steps until their answers affect action. Deepen review
where a wrong choice would cause substantial loss, irreversible effects or
expensive rework. Pause only the affected action when a necessary decision or
authorization is missing.

End the interview as soon as the goal, scope of the next step, observable check
and necessary constraints are clear, with no unresolved decision blocking that
step. The user can also say 「先出草案」 to end it and receive current conclusions
with remaining uncertainties. A request for a full plan or deeper pressure test
sets the requested coverage; mark details needing evidence as unresolved rather
than inventing precision.

### 3. Choose the next verifiable step

For build work, select a small usable or executable part that tests an important
assumption or delivers an observable improvement. Use the guide's scope rules
when naming it. Clarify wording within agreed scope yourself; ask before changing
capabilities, dependencies, scope or acceptance criteria.

Specify what to do, what evidence to inspect and how the result changes the next
decision. Bound an experiment's effort where cost or duration could grow. Keep
later work at the level needed to understand dependencies and overall direction.

Use the code and observed behavior to describe the current implementation.
Keep intended outcomes and acceptance criteria explicit; check behavior against
them before treating it as correct. Record only consequential constraints,
assumptions and decision reasons that the implementation cannot convey.

### 4. Update from results

When execution is authorized, carry out the next step and inspect the result.
Use that evidence to continue, adjust the approach or revisit the affected
assumption. Reopen user choices only when the evidence requires a consequential
change outside the agreed scope or direction.

When the request is planning only, deliver the next action and how to evaluate
it. Recommend further architecture work only when a concrete unresolved design
choice blocks progress. A planning request does not authorize implementation.

## Output Contract

Deliver the goal, scope of the next step, observable acceptance or learning
criterion, and any blocking decision. Include consequential assumptions and
constraints where relevant. State remaining uncertainties without making them
all prerequisites for action.

Before writing a saved plan, read [Plan and decision templates](references/plan-template.md).
Use only the sections needed by its reader and provide its actual path. Keep
what the user needs for the current decision in the chat reply.

Briefly disclose consequential assumptions and reversible choices made on the
user's behalf. Distinguish these from decisions requiring explicit approval;
silence does not grant additional authorization.

## Quality Rules

- Planning depth follows the cost of a wrong decision and the evidence available.
- A question must improve an immediate decision more than the available alternatives.
- Experiments have an observable result and a decision that result will inform.
- Acceptance criteria come from the intended outcome, not merely existing behavior.
- Validate each completed step; success in one step does not complete the whole goal.
- Keep documents focused on intent, constraints and reasons; let code express implementation details.
