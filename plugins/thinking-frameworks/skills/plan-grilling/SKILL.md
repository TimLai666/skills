---
name: plan-grilling
description: >-
  This skill MUST be used to clarify or pressure-test a plan before committing
  resources, including requests such as 幫我規劃、規劃一下、幫我想一下、這個怎麼做、
  逼問我、壓力測試這個計畫、幫我想這個功能、grill me、planning mode、動手之前先想清楚.
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
  version: "2.3.0"
---

## Overview

Clarify the real problem, challenge assumptions and scope, and turn unresolved
choices into a plan the user can act on. This applies to features, campaigns,
proposals, process changes, hiring and personal decisions.

## Input Contract

Identify the intended outcome, affected people, current approach, constraints,
existing plan and decisions already made. Read available files, configuration,
history and other relevant evidence before asking the user for facts.

Use the user's chosen document location or existing project convention.
Otherwise use `docs/plans/<slug>-plan.md` within the current workspace, whether
or not it uses Git. If there is no clear workspace, ask where to save the plan.
Read an existing document before updating it and preserve unrelated content.

## Workflow

### 1. Understand the problem

Before the interview, read [Interview guide](references/interview-guide.md).
Check the pain, affected people and current workaround. Identify assumptions,
contradictory evidence and consequences if the assumptions fail. Reframe the
problem when that clarifies a meaningful difference, and confirm changes to
the intended outcome before proceeding.

### 2. Resolve scope and decisions

Review all ten areas in the interview guide. Reuse established answers and
ask only about unresolved choices that affect direction, scope, resources or
acceptance. Keep relevant findings even when they require no question.

Ask one question at a time and wait for the answer. For a choice, give concrete
options and mark a recommendation with a reason based on the evidence. Use a
plain question when asking for an experience or missing context rather than
inventing choices for it.

For build plans, check the guide's rules for verifiable scope items even when
the scope is already settled. Clarify wording within the agreed scope yourself.
Ask before a rewrite changes capabilities, dependencies, scope or acceptance
criteria. Do not infer a new capability from a technical label alone.

End the interview when the available information supports an executable plan
with clear acceptance criteria and no consequential choice still requires the
user's decision. Record remaining uncertainties as assumptions to validate.
If the user asks to stop or consolidate now, deliver the current conclusions
and unresolved items.

### 3. Consolidate the plan

Before writing or updating the plan, read [Plan and decision templates](references/plan-template.md).
Record substantive decisions, reasons and consequential tradeoffs as they are
settled. Consolidate repeated discussion into the current decision; preserve
reasons for a superseded decision when they help explain the change.

Separate confirmed decisions from assumptions and unresolved choices. Check
that the final scope, success criteria and next step agree with the discussion.

## Output Contract

Deliver the plan at its actual path, with the problem, scope, assumptions,
success criteria, failure modes and decisions. Use the user's language and
requested format. Include a reframe only when one was useful.

For development plans, recommend `eng-architect` as the next step when it is
available, and provide the actual plan path for it to read. Otherwise describe
the next planning action in ordinary language. For other plans, identify the
next action that advances the decision. A planning request does not itself
authorize implementation.

## Quality Rules

- Facts come from available evidence; unresolved preferences belong to the user.
- Recommendations explain the tradeoff and the consequences of a wrong assumption.
- Success criteria specify what will be observed and when, using the plan's real horizon.
- A decision to proceed, revise or reconsider follows the findings. Ask for a choice
  only when the next action requires an unresolved user decision.
