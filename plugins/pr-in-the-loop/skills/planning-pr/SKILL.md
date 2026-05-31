---
name: planning-pr
description: Use when an approved GitHub Issue needs a concise, human-reviewed PR plan.
---

# Planning PR

Create a lightweight PR plan from an approved GitHub Issue. This step decides why and how the Issue should be solved before implementation begins.

**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming` discipline: read context, ask only blocking questions, compare approaches, present the chosen PR boundary, and wait for human approval before writing the final plan.

## Language Rule

Detect the user's language from the current request and Issue context. Write the PR plan in the detected user language unless the human explicitly requests another language. Preserve repository identifiers, code symbols, commands, file paths, links, errors, and quoted source text exactly except for required Redaction And Plan Write Safety Gate edits.

## Preconditions

- A GitHub Issue exists or an issue draft has been explicitly accepted.
- The human has explicitly approved moving from `pr-in-the-loop:issue` to `pr-in-the-loop:planning-pr`.
- The target PR boundary is known when one Issue has multiple PRs.

If any precondition is missing, stop and request the missing artifact or approval.

## Ambiguity Gate

Before writing the PR plan, remove ambiguity with the same discipline as `superpowers:brainstorming`:

- Read the Issue or accepted draft, repo context, current development environment, related files, existing plans, and relevant tests before asking questions.
- Ask one concise blocking question at a time when the answer could change the approach, PR boundary, dependencies, included scope, excluded scope, or test goals.
- Treat ambiguity as resolved only when the problem, user impact, chosen approach, included scope, excluded scope, dependencies, PR order, and reviewer acceptance signals are concrete.
- Do not write the PR plan while blocking ambiguity remains.

## Process

1. Locate the GitHub Issue or accepted issue draft from the user path, issue number, current branch, current thread artifact, or recent conversation. Ask if multiple plausible Issues or drafts exist.
2. Read repo rules, current development environment, related files, existing PR plans, and relevant tests before proposing implementation shape.
3. Run the Ambiguity Gate. If the problem is vague enough to create the wrong PR boundary, ask one concise question in the detected user language and stop.
4. Once ambiguity is resolved, propose 2-3 solution approaches with tradeoffs, explain why the recommended approach is most effective and efficient for this repo, and wait for human approval or selection.
5. If one Issue needs multiple PRs, write the PR plan for the first PR only and make follow-up ordering explicit.
6. Run the Redaction And Plan Write Safety Gate before writing the PR plan.
7. Save the PR plan to `docs/pr-plans/` by default, unless the human specified another location.
8. Name the file `issue-[issue number]-[issue title]-pr-[pr number].md`. Keep the Issue title portion readable and filesystem-safe.
9. Use `references/pr-plan-template.md` as the minimum required structure. Translate template headings and helper text to the detected user language unless the human supplied exact headings. Add optional sections only when the Issue needs them, such as db schema, API contract, migration order, or architecture sequence diagram.
10. Stop for human review. Do not create a concrete implementation spec, code, branch, commit, or pull request in this skill.

## Redaction And Plan Write Safety Gate

Before writing or updating a PR plan:

- Redact or summarize secrets, credentials, tokens, personal data, private URLs, and absolute local paths from Issue context, logs, errors, links, quoted output, and references.
- Before creating a new PR plan, search `docs/pr-plans/` for an existing plan with the same Issue number and PR number.
- If a matching reviewed plan already exists, update it only when the human explicitly requested changes; otherwise reuse the existing path.
- After creation, treat the PR plan path as the idempotency key. On retries, update that path instead of creating a duplicate plan with a different title slug or PR number.

## Required PR Plan Section Meanings

The PR plan must include these four section meanings in the detected user language. Korean defaults are:

- `## 목표`
- `## 이번 단계에 포함하는 것`
- `## 이번 단계에 포함하지 않는 것`
- `## 테스트 목표`

Do not pad the plan with long clarification notes, rejected implementation detail, or concrete task-by-task spec content. The PR plan should be short enough for human review while still making reviewer scope clear. `pr-in-the-loop:parallel-development` owns the uncommitted concrete spec after this plan is approved.
