---
name: ship-it
description: "Prepare a feature branch for a pull request: verify scope, sync when needed, test, review, push and open or update the PR. This skill MUST be used when the user requests this branch-to-PR workflow or explicitly invokes ship-it (開 PR、準備 PR、整理分支交付). It SHOULD be used when the user asks to prepare a completed feature for review. It MUST NOT be triggered solely by a push, merge, release, deployment request or a general readiness question."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.4.0"
---

## Step 1 — Confirm scope and project rules

Read the project's coordination and delivery instructions. Confirm the requested
outcome, current branch, target remote and PR base from repository settings and
user intent; do not guess `main` when the base is unknown.

Use the project's existing delivery document. With no other arrangement, look
for `delivery-status.md`; support `delivery-plan.md` in older projects. Read the
current phase, expected output and acceptance requirements, not just the first
few lines. If the diff conflicts with the agreed scope, resolve that decision
with the user before shipping. Do not create a status file just for this check.

Inspect working-tree changes and outgoing commits. Include only the intended
work. Proceed with already authorized commits without asking again; do not
silently stash, discard or include unrelated changes. If the work is on the base
branch, establish a suitable PR branch without resetting existing work.

After setting `_SHIP_REMOTE`, `_SHIP_BASE` and `_SHIP_BRANCH` to verified values:

```bash
git status --short
git diff "$_SHIP_REMOTE/$_SHIP_BASE...HEAD" --stat
git log "$_SHIP_REMOTE/$_SHIP_BASE..HEAD" --oneline
```

## Step 2 — Sync when needed

Fetch the target base and check whether synchronization is needed. Follow the
project's merge or rebase convention; do not automatically merge the base into
every branch. Avoid rewriting shared history without authorization.

```bash
git fetch "$_SHIP_REMOTE" "$_SHIP_BASE"
```

Resolve conflicts from the intended behavior and both sides' changes, then
validate the resolution. Ask only when a material behavior or scope decision
cannot be determined from available evidence.

## Step 3 — Verify behavior and review the final diff

Run tests appropriate to the changes and risks. Run the project's full suite
according to its rules. Reuse prior results only when they cover the current
code and relevant environment; rerun affected checks after subsequent edits or
conflict resolution.

Check coverage of important behavior, boundary conditions and error handling.
Add meaningful tests where those behaviors lack evidence, rather than requiring
a test for every new code path or testing implementation details alone.

Fix failures introduced by this branch. Establish evidence for pre-existing
failures or environment blockers, apply project delivery rules, and report any
remaining gate instead of presenting partial results as a pass.

Run **diff-inspector** on the outgoing diff unless an existing review covers
that same diff. Review later changes and their effects. Resolve confirmed
findings according to severity and project rules, and distinguish unresolved
questions from confirmed defects.

## Step 4 — Push and open or update the PR

Before pushing, scan the outgoing commits and diff for secrets, including keys,
tokens, credentials and sensitive connection strings. If found, stop the push
and report their locations without reproducing secret values.

```bash
git push "$_SHIP_REMOTE" "$_SHIP_BRANCH"
```

Check for an existing PR for the branch before creating one. Follow the
repository's PR template. If none exists, use
[the PR body template](assets/pr-body.md), filling it with actual changes and
verification results. Scale detail to the change and remove irrelevant sections.

**Do not append co-author credits, `Co-authored-by` trailers or agent signatures
to PR titles or descriptions.**

With an authenticated GitHub CLI, save the completed body to a temporary file
and use its path as `_SHIP_PR_BODY`. Set `_SHIP_TITLE` from the actual change:

```bash
gh pr create --base "$_SHIP_BASE" --head "$_SHIP_BRANCH" \
  --title "$_SHIP_TITLE" --body-file "$_SHIP_PR_BODY"
```

For an existing PR, update it with `gh pr edit` using the completed body file.
If the CLI is unavailable or unauthenticated, use an available authorized
alternative or provide the completed title and body for manual submission.
Report which operations actually succeeded.

## Step 5 — Check CI and record lessons

Read checks for the resulting PR and report passed, failed, pending or unavailable:

```bash
gh pr checks "$_SHIP_PR_URL"
```

When waiting for required CI is part of the requested delivery, actively watch
those checks to a result and handle failures within scope:

```bash
gh pr checks "$_SHIP_PR_URL" --watch
```

When deployment verification is requested, identify the deployment workflow run
for the intended revision and environment. Set `_SHIP_RUN_ID` to that verified
run ID and watch it explicitly:

```bash
gh run watch "$_SHIP_RUN_ID" --exit-status
```

Inspect failed checks or jobs and resolve failures within scope. Verify the
deployment's required outcome before reporting success; a passing unrelated
workflow is not deployment evidence. If monitoring is blocked or interrupted,
report the last observed state, the PR or run URL, and what remains unverified.

Run **project-memory** at this wrap-up checkpoint, following its recording
criteria. Save qualifying project-specific lessons and report saved entries.
If nothing qualifies, no announcement is needed.

## Delivery report

Report the branch and scope, actual test and review results, PR URL, CI state
and unresolved requirements. Distinguish pushed, PR created or updated, merged,
and deployed based on evidence. Creating a PR does not establish merge or deployment.
