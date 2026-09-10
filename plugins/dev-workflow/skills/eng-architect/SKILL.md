---
name: eng-architect
description: "This skill MUST be used for architecture decisions, module boundaries, turning plans or specs into tickets, or explicit UI/design reviews. SHOULD be used when implementation requires unresolved architectural choices or the user is unsure how to divide the work. MUST NOT expand an already specified implementation into a new planning exercise. Triggers on: 技術方案, 架構設計, 怎麼切模組, 拆任務, 切票, 排開發順序, 技術規劃, design review, UI review, AI slop scan."
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
  version: "1.11.0"
---

## Overview

Design architecture and verifiable tickets, or review an existing UI. Preserve the requested scope and existing project decisions.

## Command routing

Infer the mode from the requested outcome:

- Architecture, module boundaries, technical plans, or tickets: read [Engineering workflow](references/engineering-workflow.md) in full before the per-feature analysis, including its examples.
- UI critique, design review, or AI slop scan: read [Design review workflow](references/design-review-workflow.md) in full before reviewing, including its examples.
- If both are requested, use both workflows for their respective outputs. Ask which mode only when the intended outcome remains materially ambiguous.

Read the other references at the workflow step that needs them.

## Shared decision rules

Use evidence from the project and prior user decisions. Analyze each feature's flow, failure paths, boundaries, and testing approach before consolidating the architecture.

Collect unresolved decisions that require user tradeoffs and present related choices together with a recommendation and consequences. Ask before changing agreed scope, architecture, workflows, or other consequential choices that are not authorized. Continue independent analysis while awaiting answers. Reuse settled decisions without asking again.

A request for review or discussion produces the corresponding analysis. An authorized implementation or ticket-writing request permits routine work within its agreed boundaries.

## Project records

Use existing architecture documents, task systems, status records, and coordination conventions. When none exists and full development handoff is needed, use the complete default set in the engineering workflow. For a bounded decision or review, deliver the requested result and update an existing relevant record when appropriate.

Read existing content before updating it, preserve unrelated sections, and register actual artifact paths with when they must be read. Keep shared technical decisions in the architecture record and per-ticket acceptance criteria on the owning ticket.

## Completion check

- The result answers the requested architecture, ticketing, or UI-review need.
- Engineering analysis covers feature flows, failures, interaction boundaries, testing, and applicable migration risks; ticketing work assigns every analyzed acceptance item an owner and records real blockers.
- Unresolved assumptions and decisions are explicit. Project-required validation and delivery rules are followed.
- Updated records retain unrelated content, link to the actual sources, and identify the next verifiable action when handing off.
