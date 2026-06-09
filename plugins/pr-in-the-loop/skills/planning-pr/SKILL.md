---
name: planning-pr
description: Use when a user has an existing GitHub Issue or issue draft and wants a human-reviewable PR plan, PR decomposition, implementation phase plan, or next PR scope before coding. Trigger for docs/pr-plans work, minimum PR splitting, and planning the ordered PRs needed to solve an issue. Do not use for issue discovery before an issue exists, implementation, code review, or PR publishing.
---

# Planning PR

Write human-reviewable PR planning documents for one existing Issue.

This skill starts after `open-issue` or after the user provides an issue. It defines one or more pull requests that solve the issue in implementation order, with each PR scoped to the minimum functional unit a reviewer can evaluate.

## Rules

- Start from one existing GitHub Issue, issue URL, or issue draft. If no issue exists, use `open-issue` first.
- Do not implement code. Do not open pull requests, stage code, or perform code review.
- Prefer actual issue text, project state, codebase search, docs, official docs, and web search over assumptions.
- Write the plan in the user's language. For Korean PR plans, read `../../references/korean-writing-tips.md` and apply it.
- Create one or more plan documents under `docs/pr-plans/` unless the user requests another path.
- Treat PR plan documents as a commit target by default.
- If the user explicitly opts out of committing PR plan documents, record that preference in `.memory/planning-pr/work-context.md` and honor it in future planning runs unless the user overrides it.
- Keep implementation plans narrow. Split unrelated cleanup, hardening, docs, and behavior changes into separate PRs or separate issues.
- If a decision is ambiguous, ask before writing the final plan. Offer 3-4 options with a reason, tradeoff, and recommendation.

## Memory

Use `.memory/planning-pr/work-context.md` for durable planning preferences that should not be committed.

At the start of each run:

1. Run `sh <plugin-root>/scripts/ensure-memory-gitignore.sh` from the target project root to verify `.memory/` is gitignored.
2. Read `.memory/planning-pr/work-context.md` if it exists.
3. Apply stored preferences unless the current user message overrides them.

Only store stable workflow preferences, for example:

```markdown
# Planning PR Work Context

- PR plan document commit policy: commit by default
- User override: do not commit PR plan documents
- Preferred PR plan directory: docs/pr-plans
```

Never store secrets, tokens, copied private message bodies, or credentials.

## Workflow

1. **Load Issue Context**
   - Read the issue URL/body or issue draft.
   - Identify the problem, desired outcome, and any acceptance criteria.
   - Check for linked PRs, prior plans, specs, review notes, or related issues.

2. **Orient Repository**
   - Inspect `git status --short --branch`, remotes, recent commits, README, docs, tests, CI config, and relevant project conventions.
   - Find existing plan formats under `docs/pr-plans/` or nearby docs and follow them when they do not conflict with this skill.

3. **Research the Solution**
   - Run codebase search for the relevant modules, APIs, tests, and existing patterns.
   - Search project docs and related docs for local contracts.
   - Search official docs when APIs, libraries, frameworks, platform behavior, or policy may affect the plan.
   - Use web search when current external behavior matters and official docs are insufficient.
   - Add every source that materially shapes the plan to `## Reference`.

4. **Split PRs**
   - List the work needed to solve the issue.
   - Split it into one or more PRs in implementation order.
   - Each PR must be a minimum functional unit: useful, reviewable, testable, and mergeable without depending on unmerged local edits outside its stated base.
   - If the issue needs multiple features, create separate phase plans in the order they should be implemented.
   - Do not make a "cleanup" PR part of the issue plan unless it is required to ship or validate the issue.

5. **Resolve Ambiguity**
   - Stop and ask the user when the issue scope, PR split, desired behavior, validation strategy, compatibility risk, data migration, or source of truth is unclear.
   - Present 3-4 options:
     - `Recommended`: the path you would choose, with the reason and tradeoff.
     - `Alternative`: a narrower or lower-risk path, with the tradeoff.
     - `Alternative`: a broader or faster path, with the tradeoff.
     - `Alternative` when useful: a defer-to-separate-issue path, with the tradeoff.
   - Continue only after the user selects a direction, unless evidence already points to one clear answer.

6. **Write Plan Documents**
   - Default file name: `docs/pr-plans/YYYY-MM-DD-issue-<number>-phase-<n>-<slug>.md`.
   - For one PR, use `phase-1`.
   - For multiple PRs, write one document per PR unless the user asks for a single combined plan.
   - Preserve the required headings below. Add project-specific fields only after these sections or inside them.

## PR Plan Template

```markdown
# PR Plan: <short title>

## Goal
<State the Issue problem/task this PR solves. Include the issue number or URL.>

## Scope for This Phase
<Explain how this PR advances the Goal. Define exact files, modules, behavior, contracts, and tests in scope. Base this section on codebase search, docs search, official docs search, web search, and issue context. Add all referenced sources to Reference.>

## Out of Scope
<State what this PR will not handle. For each item, say whether it belongs to another PR in this issue's sequence or a separate issue.>

## Validation
<List the tests, checks, manual verification, migrations, screenshots, or release checks expected for this PR.>

## PR Split Rationale
<Explain why this is the minimum functional unit and how it fits in the implementation order. If this is part of a multi-PR sequence, name previous and next phases.>

## Review Notes
<Call out reviewer-sensitive risks, compatibility concerns, files that deserve close review, and non-obvious decisions.>

## Reference
- <Issue URL, local file path, official doc URL, web source, project doc, or related PR>
```

If there are no references, write `- None` in English or `- 없음` in Korean.

## Quality Bar

Before finishing, verify:

- The plan starts from one issue and names that issue.
- Each planned PR is a minimum functional unit.
- Multi-PR work is ordered by implementation dependency, not by file ownership convenience.
- `## Scope for This Phase` says what will change and why this phase is enough.
- `## Out of Scope` tells reviewers whether deferred work belongs to another PR or another issue.
- `## Validation` is executable and scoped to the PR.
- `## Reference` includes all sources used for the plan.
- Korean writing follows `../../references/korean-writing-tips.md` when applicable.
- No placeholders such as TBD, TODO, or `<...>` remain in the final plan document.
- PR plan documents are treated as commit targets unless the user explicitly opted out and `.memory/planning-pr/work-context.md` records that preference.
