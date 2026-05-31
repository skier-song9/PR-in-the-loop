---
name: issue
description: Use when a problem needs a GitHub Issue before PR planning or implementation.
---

<!-- DocString Spec Excerpt: Define explicit user-language detection and the Description/Tasks/References Issue Template for GitHub Issue drafting while separating Issue creation from PR planning. -->

# Issue

Create or draft the GitHub Issue only. This is the user's GitHub-aware problem-definition step before PR planning.

**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming` discipline: explore context, ask only blocking questions, compare approaches, present the clarified Issue scope, and wait for human approval before moving to `pr-in-the-loop:planning-pr`.

## Language Rule

Detect the user's language before drafting any GitHub Issue. Write the Issue title and Issue body in the detected user language.

## User Language Detection

Before drafting or creating a GitHub Issue:

1. Inspect the current user request first.
2. Inspect the surrounding conversation only as supporting evidence.
3. If the current user request is mostly one natural language, use that language.
4. If the conversation is mixed, use the language the user used when asking for the Issue.
5. If the user explicitly names a target language, use that language.
6. Apply the detected language to the Issue title and Issue body.
7. Preserve repository identifiers, code symbols, commands, file paths, links, and quoted output exactly except for required Redaction And Write Safety Gate edits.

## Ambiguity Gate

Before creating the Issue, remove ambiguity with the same discipline as `superpowers:brainstorming`:

- Read repo context first so questions are grounded in files, templates, and current branch state.
- Ask one concise blocking question at a time when the answer could change the Issue scope, task list, dependencies, or acceptance signals.
- Compare 2-3 approaches with tradeoffs only after the problem is clear enough to avoid the wrong Issue.
- Treat ambiguity as resolved only when the problem, user impact, chosen approach, included scope, excluded scope, dependencies, and reviewer acceptance signals are all concrete.
- Do not create the Issue while blocking ambiguity remains.

## Process

1. Read current repo context: `AGENTS.md`, issue template, relevant docs, branch, recent related files, and existing GitHub issue/PR state.
2. Run User Language Detection and keep the detected language fixed for the Issue title and Issue body unless the user explicitly corrects the target Issue language.
3. Run the Ambiguity Gate. If the problem is vague enough to create the wrong Issue scope, task list, dependency set, or acceptance signal, ask one concise question in the detected user language and stop.
4. Once ambiguity is resolved, propose 2-3 solution approaches with tradeoffs and recommend one in the detected user language.
5. Run the Redaction And Write Safety Gate before any GitHub write.
6. Create or update a GitHub Issue using the GitHub plugin/app first, then `gh` if needed. The Issue title and Issue body must use the detected user language and the Issue Template. In no-write or dry-run mode, produce the issue draft and mark it `not-created`.
7. Do not write a PR plan, concrete spec, implementation branch, commit, or pull request in this skill.
8. Stop after the Issue exists or the issue draft is accepted. Starting the separate `pr-in-the-loop:planning-pr` PR-plan step requires explicit human approval.
9. Do not create a spec, code, branch, commit, or PR until the human explicitly approves the next workflow step.

## Redaction And Write Safety Gate

Before creating or updating a GitHub Issue:

- Redact or summarize secrets, credentials, tokens, personal data, private URLs, and absolute local paths from Issue title, body, screenshots, logs, quoted output, and references.
- Issue create or update targets must match the current repository remote. If the target owner/repo differs, ask for explicit human confirmation immediately before the write.
- Before creating a new Issue, search current-repo open Issues for the same title or a known issue URL/artifact marker from the current thread.
- After creation, treat the Issue URL and number as the idempotency key. On retries, update that Issue instead of creating a duplicate.

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

## Next-Step Approval Rules

Only proceed from this Issue step to `pr-in-the-loop:planning-pr` when the human clearly approves, such as `approved`, `승인`, `이대로 진행`, or equivalent. Silence, "looks close", or unresolved comments are not approval.

If the human requests changes before planning, update the Issue or issue draft and repeat the review gate.
