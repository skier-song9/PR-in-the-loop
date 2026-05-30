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

Dispatch every reviewer prompt under `references/reviewers/` as a fresh reviewer subagent:

- spec compliance
- code quality and edge cases
- ADK and agent architecture
- data, migration, and contract
- docs and PR context
- security, idempotency, and deduplication

Dispatch reviewers in parallel when the platform supports fresh subagents. Otherwise run them sequentially while keeping each prompt isolated. Do not skip a reviewer because the domain seems irrelevant; that reviewer should return `APPROVED` or `NOT_APPLICABLE` with a short reason when its domain does not apply.

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

## Kami-inspired Layout Guide

Use a restrained document layout inspired by `tw93/kami`:

- canvas background `#f5f4ed`, never pure white
- single ink-blue accent `#1B365D`; use it for section bars, links, and small tags only
- warm neutral text and borders; avoid cool blue-gray UI styling
- serif-led hierarchy for report title and section headings; system sans may be used for labels and metadata
- line-height around `1.5-1.55` for body text
- cards use ivory `#faf9f5`, thin warm borders, and 8px radius
- use ring or whisper shadows only; no hard drop shadows
- include a compact evidence table for reviewer agents, changed files, and test commands
- include counts for Critical, Important, Minor, Approved, and Not Applicable findings
