# Interview guide

## Understand the pain

Use these questions where the context leaves a gap, one at a time:

- 「你上次遇到這個問題是什麼時候？給我一個具體的例子。」
- 「誰有這個問題？他們在什麼情境下遇到？」
- 「他們現在怎麼做？為什麼不夠好？」

Distinguish observed experience from a proposed scenario. Examine what the
answers imply, which assumptions may fail, and whether another framing would
change the solution. Confirm meaningful changes to the problem being solved.

## Scope direction

When the desired scope is unresolved, compare the relevant directions:

- Expand: pursue a larger outcome, explaining each proposed addition and its cost.
- Selectively expand: keep the core and consider specific extensions.
- Hold: improve the current plan within its agreed scope.
- Reduce: find the smallest version that can test the important assumptions.

Recommend a direction from the actual context. A choice to explore expansion
is not approval for every resulting addition.

## Ten review areas

Review each area; use existing evidence and decisions wherever sufficient.
Ask about a gap only when resolving it needs a user choice or unavailable context.

| Area | What to examine |
| --- | --- |
| Problem clarity | Is the pain concrete, and what evidence supports it? |
| Who it is for | Who encounters it, in what situation? |
| Scope in | How does each item address the problem? |
| Scope out | Which exclusions matter to expectations and effort? |
| Success metric | What observable result counts as success, and when can it be assessed? |
| Assumptions | Which unverified assumptions could change the decision? |
| Ambitious version | Would exploring the upper limit help the user's decision? |
| Minimum version | Can a smaller version answer the critical question? |
| Failure modes | What could make the plan fail, and how can that be addressed? |
| Recommendation | Proceed, revise or reconsider, with reasons and outstanding decisions. |

### Scope items name what someone can do

This governs how Scope in and Scope out get written, and applies only when the plan is
about building something — a feature, a product, a service. Campaigns, hiring
calls and other non-build plans keep plain `- [item] - reason` entries.

Every scope item must read as "<who> can <do what>". An item that cannot be said
that way is not a scope item yet.

- Rewrite anything whose subject is a module, a layer or a technology.
  「做會員 API」is not a scope item;「訪客可以用 email 註冊並登入」is.
- Test each item: once this is done, can anyone see or use the difference? If
  not, it is not a feature.
- Foundations do not disappear, they move. Shared scaffolding, auth, core tables
  and mechanical refactors that fan across the codebase are not user functions.
  Collect them into one item the others depend on, rather than slicing them into
  one item per layer.
- Layers still matter, but only inside a single item — schema first, then logic,
  then screen. Never as the axis that splits the whole plan.

