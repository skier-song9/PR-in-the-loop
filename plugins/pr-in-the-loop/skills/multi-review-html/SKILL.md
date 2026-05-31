---
name: multi-review-html
description: Use when implemented code needs independent typed reviewers and an HTML review report.
---

<!-- DocString Spec Excerpt
Context: Issue #11 makes this skill own HTML review report language detection and user-facing report language rules.
References: Issue #11; https://github.com/skier-song9/PR-in-the-loop/issues/11.
Work Process: Add workflow instructions before report synthesis; keep code identifiers, paths, commands, quoted errors, and reviewer verdict keywords unchanged.
Test Method: python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_multi_review_html_requires_language_detection_and_template_language_placeholders
-->

# Multi Review HTML

Run code review with multiple fresh reviewer subagents, then synthesize one HTML report.

**REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review`.

## Language Rule

Keep the detected user language fixed for the whole HTML report.

For DETECTED_LANGUAGE_BCP47, emit a valid BCP 47 language tag; prefer regional tags when the user names a regional variant, and use en when language detection remains ambiguous.

Apply the detected user language to report title, summary, reviewer evidence, findings, next actions, status text, metric labels, table headings, metadata, and narrative copy.

Preserve code identifiers, file paths, commands, quoted errors, and reviewer verdict keywords exactly.

Reviewer verdict keywords and severity contract names remain visible as contract values, while adjacent labels, explanations, and prose use the detected user language.

Preserve reviewer verdict keywords exactly when reviewers provide contract keywords such as `APPROVED` or `NOT_APPLICABLE`.

Exact verdict keywords may appear as bare keywords or as leading verdict prefixes such as `APPROVED:` or `NOT_APPLICABLE:`; preserve the keyword, and use detected-language prose for the adjacent reason/status.

Do not invent reviewer verdict keywords for reviewers that report findings; use detected-language status prose and the finding evidence instead.

When a reviewer uses a clear no-issue or not-applicable phrase without an exact verdict keyword, classify it for the summary count using detected-language status prose, but do not present an invented verdict keyword as quoted reviewer output.

Keep severity contract names visible for findings, with localized adjacent labels/prose.

Before substituting dynamic values into HTML, HTML-escape reviewer evidence, findings, test output, commands, file paths, quoted errors, and narrative text.

Preservation rules apply after required HTML escaping.

## User Language Detection

Before writing the HTML report, detect the user's language from the current user request and surrounding conversation.

- Inspect the current user request first.
- Inspect surrounding conversation only as supporting evidence.
- If the current user request is mostly one natural language, use that language.
- If the conversation is mixed, use the language the user used when asking for review or report generation.
- If the user explicitly names a target language, use that language.
- Explicit target-language requests override other detection signals.

This detection policy intentionally mirrors the GitHub issue planning language rules locally because skills load independently; keep semantic changes synchronized across language-aware workflow skills.

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

Use `references/html-report-template.md` for structure, then replace all placeholder language markers and sample copy with detected-language report text.

Preserve severity contract names as contract values; translated prose around them follows the detected user language.

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
- include counts for severity buckets (Critical, Important, Minor) and reviewer verdict buckets (Approved, Not Applicable)
