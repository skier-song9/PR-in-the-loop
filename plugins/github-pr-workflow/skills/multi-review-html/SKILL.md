---
name: multi-review-html
description: Use when implemented code needs independent typed reviewers and an HTML review report.
---

# Multi Review HTML

Run code review with multiple fresh reviewer subagents, then synthesize one HTML report.

**REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review`.

## Review Scope

1. Determine base and head:
   - staged diff: base `HEAD`, head staged changes
   - committed branch: base `git merge-base HEAD origin/main` or repo default branch, head `HEAD`
   - include unstaged changes only when the human asks
2. Read the approved PR plan, concrete spec if available, changed files, and test output.
3. If plan/spec paths are ambiguous, ask before reviewing.

## Reviewer Set

Use all relevant prompt files under `references/reviewers/`:

- spec compliance
- code quality and edge cases
- ADK and agent architecture
- data, migration, and contract
- docs and PR context
- security, idempotency, and deduplication

Dispatch reviewers in parallel when the platform supports fresh subagents. Otherwise run them sequentially while keeping each prompt isolated.

## Finding Contract

Every issue must include:

- severity: Critical, Important, or Minor
- file and line when available
- concrete evidence
- why it matters
- an example showing the failure, confusion, or safer shape
- suggested fix or deferral reason

Do not accept vague findings without examples.

## HTML Report

Save the synthesized report to:

`docs/reviews/YYYY-MM-DD-topic-code-review.html`

Topic comes from the PR plan filename, branch name, or main changed component. Keep it lowercase hyphen-case.

The HTML report is not committed. After writing it, stop for human review and report the path.

Use `references/html-report-template.md` for structure.
