---
name: github-issue-pr-planning
description: Use when a problem needs a GitHub Issue and a human-reviewed PR plan before implementation.
---

# GitHub Issue PR Planning

Create the problem record and PR plan. This is the user's GitHub-aware version of brainstorming.

**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming` discipline: explore context, ask only blocking questions, compare approaches, present a plan, and wait for human approval before implementation.

## Process

1. Read current repo context: `AGENTS.md`, issue template, relevant docs, branch, recent related files, and existing GitHub issue/PR state.
2. If the problem is vague enough to create the wrong issue, ask one concise question. Otherwise proceed.
3. Propose 2-3 solution approaches with tradeoffs and recommend one.
4. Create or update a GitHub Issue using the GitHub plugin/app first, then `gh` if needed. In no-write or dry-run mode, produce the issue draft and mark it `not-created`.
5. Write a PR plan markdown file under the most relevant `docs/` subtree. In no-write or dry-run mode, return the PR plan draft in the response, name the intended path, and do not write the file.
6. If one Issue needs multiple PRs, create one plan section per PR and make ordering explicit.
7. Stop for human review. Do not create a spec, code, branch, commit, or PR until approval is explicit.

## PR Plan Requirements

The PR plan is not a concrete implementation spec. It must focus on:

- problem and user impact
- why this PR exists
- chosen approach and rejected alternatives
- scope included in this PR
- scope excluded from this PR
- follow-up PRs if needed
- acceptance signals for reviewers

Use `references/pr-plan-template.md` as the artifact shape.

## Approval Rules

Only proceed when the human clearly approves the PR plan, such as `approved`, `승인`, `이대로 진행`, or equivalent. Silence, "looks close", or unresolved comments are not approval.

If the human requests changes, update the plan and repeat the review gate.
