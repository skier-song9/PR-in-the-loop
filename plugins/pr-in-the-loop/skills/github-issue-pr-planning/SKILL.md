---
name: github-issue-pr-planning
description: Use when a problem needs a GitHub Issue and a human-reviewed PR plan before implementation.
---

<!-- DocString Spec Excerpt: Define explicit user-language detection and the Description/Tasks/References Issue Template for GitHub Issue drafting while preserving existing PR planning gates. -->

# GitHub Issue PR Planning

Create the problem record and PR plan. This is the user's GitHub-aware version of brainstorming.

**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming` discipline: explore context, ask only blocking questions, compare approaches, present a plan, and wait for human approval before implementation.

## Language Rule

Detect the user's language before drafting any GitHub Issue or PR plan. Write the Issue title, Issue body, and PR plan in the detected user language.

## User Language Detection

Before drafting or creating a GitHub Issue:

1. Inspect the current user request first.
2. Inspect the surrounding conversation only as supporting evidence.
3. If the current user request is mostly one natural language, use that language.
4. If the conversation is mixed, use the language the user used when asking for the Issue or PR plan.
5. If the user explicitly names a target language, use that language.
6. Apply the detected language to the Issue title, Issue body, and PR plan.
7. Preserve repository identifiers, code symbols, commands, file paths, links, and quoted output exactly.

## Ambiguity Gate

Before creating the Issue or PR plan, remove ambiguity with the same discipline as `superpowers:brainstorming`:

- Read repo context first so questions are grounded in files, templates, and current branch state.
- Ask one concise blocking question at a time when the answer could change the Issue, PR boundary, or acceptance signals.
- Compare 2-3 approaches with tradeoffs only after the problem is clear enough to avoid the wrong Issue.
- Treat ambiguity as resolved only when the problem, user impact, chosen approach, included scope, excluded scope, dependencies, and reviewer acceptance signals are all concrete.
- Do not create the Issue or PR plan while blocking ambiguity remains.

## Process

1. Read current repo context: `AGENTS.md`, issue template, relevant docs, branch, recent related files, and existing GitHub issue/PR state.
2. Run User Language Detection and keep the detected language fixed for the Issue title, Issue body, and PR plan unless the user corrects it.
3. Run the Ambiguity Gate. If the problem is vague enough to create the wrong Issue or PR boundary, ask one concise question in the detected user language and stop.
4. Once ambiguity is resolved, propose 2-3 solution approaches with tradeoffs and recommend one in the detected user language.
5. Create or update a GitHub Issue using the GitHub plugin/app first, then `gh` if needed. The Issue title and Issue body must use the detected user language and the Issue Template. In no-write or dry-run mode, produce the issue draft and mark it `not-created`.
6. Write a PR plan markdown file under the most relevant `docs/` subtree, using the detected user language. In no-write or dry-run mode, return the PR plan draft in the response, name the intended path, and do not write the file.
7. If one Issue needs multiple PRs, create one plan section per PR and make ordering explicit.
8. Stop for human review. Do not create a spec, code, branch, commit, or PR until approval is explicit.

## Issue Template

Draft every GitHub Issue body with this structure, translated into the detected user language when the user is not writing in English. Keep the heading labels exactly as shown unless the user supplies a different template.

```markdown
## Description
one-line feature or problem summary

detailed explanation; screenshots, videos, links, and examples may be included when useful

## Tasks
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

## References
- [Link text](Link addr)
- related Issue or PR
```

Fill `Tasks` with concrete checkbox items from the clarified scope. Fill `References` with relevant links, related Issues or PRs, source files, or `None` when there is no useful reference.

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
