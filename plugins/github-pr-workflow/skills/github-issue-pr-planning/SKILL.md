---
name: github-issue-pr-planning
description: Use when a problem needs a GitHub Issue and a human-reviewed PR plan before implementation.
---

# GitHub Issue PR Planning

Create the problem record and PR plan. This is the user's GitHub-aware version of brainstorming.

**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming` discipline: explore context, ask only blocking questions, compare approaches, present a plan, and wait for human approval before implementation.

## Language Rule

Write the PR plan in the agent conversation session's primary language. Infer the primary language from the current user request and the surrounding conversation. If the conversation is mixed, use the language the user used for the request that triggered planning. Keep repository identifiers, code symbols, commands, file paths, and quoted errors unchanged.

## Ambiguity Gate

Before creating the Issue or PR plan, remove ambiguity with the same discipline as `superpowers:brainstorming`:

- Read repo context first so questions are grounded in files, templates, and current branch state.
- Ask one concise blocking question at a time when the answer could change the Issue, PR boundary, or acceptance signals.
- Compare 2-3 approaches with tradeoffs only after the problem is clear enough to avoid the wrong Issue.
- Treat ambiguity as resolved only when the problem, user impact, chosen approach, included scope, excluded scope, dependencies, and reviewer acceptance signals are all concrete.
- Do not create the Issue or PR plan while blocking ambiguity remains.

## Process

1. Read current repo context: `AGENTS.md`, issue template, relevant docs, branch, recent related files, and existing GitHub issue/PR state.
2. Run the Ambiguity Gate. If the problem is vague enough to create the wrong Issue or PR boundary, ask one concise question and stop.
3. Once ambiguity is resolved, propose 2-3 solution approaches with tradeoffs and recommend one.
4. Create or update a GitHub Issue using the GitHub plugin/app first, then `gh` if needed. In no-write or dry-run mode, produce the issue draft and mark it `not-created`.
5. Write a PR plan markdown file under the most relevant `docs/` subtree, using the session's primary language. In no-write or dry-run mode, return the PR plan draft in the response, name the intended path, and do not write the file.
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
