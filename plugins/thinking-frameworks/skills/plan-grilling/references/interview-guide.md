# Interview guide

## Establish the immediate decision

Use existing evidence to identify the problem, who encounters it, the intended
result and the constraints on the next action. Ask about missing context only
when it changes that action. For example, ask about the last observed occurrence
when distinguishing an actual problem from a hypothetical one matters.

Check whether a smaller step could test the critical assumption. Compare broader
scope only when it would materially change the user's decision. Confirm changes
to the intended outcome or agreed scope before adopting them.

## Choose how to resolve uncertainty

| Missing information | Response |
| --- | --- |
| A fact available in code, configuration, records or other sources | Inspect the source. |
| A user preference or tradeoff that changes the next action | Ask one focused question with a recommendation. |
| Behavior, feasibility or usability that needs observation | Propose the smallest useful experiment and its observable check; execute within authorization. |
| A reversible, low-cost implementation choice within scope | Decide it and verify the result. |
| A later detail that does not affect the next action or a costly commitment | Defer it until relevant evidence or a dependency makes it necessary. |
| A choice with irreversible effects or substantial rework | Establish the necessary constraints and authorization before the affected action. |

Before another question, identify how each answer would change the next action.
Compare asking with inspecting evidence or experimenting. Ask for context the
user has; do not ask the user to predict results that need observation.

## Check readiness for the next step

End clarification when the intended result, scope of the next action, observable
check and necessary constraints are clear. Review affected dependencies and
consequences far enough to avoid a costly commitment made on an unchecked
assumption. Open questions about later work can remain open.

For an experiment, name the uncertainty, the action, the evidence to inspect and
what would support continuing or changing direction. A failed experiment can
answer the question. It does not satisfy the feature's acceptance criteria.

Use deeper questioning when the cost of a wrong choice warrants it or the user
requests a broader review. Apply the same readiness check to the requested scope.

## Scope items name observable outcomes

For build work, name a usable behavior or an executable result someone can check.
Use "<who> can <do what>" for user-facing features. For a technical experiment,
state the question it answers and the result that can be observed.

- 「做會員 API」needs an outcome such as「訪客可以用 email 註冊並登入」;
  confirm the capability instead of inferring it from the technical label.
- Keep the layers needed for one behavior inside that step. Include foundations
  only as required dependencies, rather than planning every layer in advance.
- Describe later features only enough to understand the overall direction and
  consequential dependencies. Elaborate when they become the next step.

## Example applications

These are hypothetical situations; use the actual task's evidence and constraints.

- The user authorizes a small behavior change and supplies clear acceptance
  criteria: inspect the affected code and make the change without a new interview.
- A performance plan depends on whether an existing implementation can handle the
  expected input: measure a representative case before designing an optimization.
  Use the result to decide whether optimization is needed and where to focus it.
- A data migration could discard records and retention requirements are unknown:
  clarify those requirements before any destructive action. Read-only inspection
  can continue within authorization.
- A campaign's audience and budget are settled but the message is uncertain:
  propose a small comparison with an observable response criterion. Obtain any
  missing authorization before external publication or spending.
