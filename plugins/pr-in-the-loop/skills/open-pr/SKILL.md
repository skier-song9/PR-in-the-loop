---
name: open-pr
description: Use when implementation and review are done, or when completed changes are ready to be represented as a pull request. Draft the PR body and open the GitHub PR by default unless the human explicitly opts out.
---

# Open PR

Draft the final PR message and open the GitHub pull request by default from evidence, not memory.

## Trigger Rule

Use this skill when completed changes are ready to be represented as a pull request and the user's intent is for the agent to prepare that pull request, regardless of the user's exact phrasing. Open PR is the mandatory evidence-to-PR-body step and PR-creation step before any pull request creation or publication flow in the GitHub PR Workflow plugin.

This rule is about the user's intent to turn completed work into a pull request, not about matching a fixed verb such as create, open, publish, upload, raise, or draft.

Unless the human explicitly says not to open a GitHub PR, create the GitHub pull request after drafting the PR message. Only skip GitHub PR creation when the human explicitly opts out with wording such as "do not open a PR", "draft only", "PR은 열지 마", or equivalent.

## Language Rule

Write the PR message in the user's primary language. Infer the user's primary language from the current request and surrounding agent conversation. If the conversation is mixed, use the language the user used when asking for the PR message. Keep Issue references, file paths, commands, code identifiers, and quoted output unchanged except for required PR Write Safety Gate redactions.

## Inputs

Read the approved PR plan, GitHub Issue, final diff, tests actually run, and HTML review report if present. Do not invent test results or follow-ups.

## Preconditions

- The HTML review has been read by the human, or the human confirmed that no further fixes are needed.
- Critical and Important findings are fixed, explicitly deferred, or rejected with technical evidence.

If these are missing, stop and request the missing review decision.

## Process

1. Read the approved PR plan, GitHub Issue, final diff, tests actually run, HTML review report if present, current branch, base branch, and repository remote.
2. Draft the PR message in the user's primary language using the Template and evidence rules.
3. Run the PR Write Safety Gate before any GitHub write.
4. Verify the reviewed changes are committed on the head branch and pushed to the remote before opening the PR.
5. Open the pull request after drafting the PR message unless the human explicitly opted out of GitHub PR creation.
6. Use the GitHub plugin/app first, then `gh` CLI as fallback when the plugin lacks permission or coverage. When using `gh` fallback, pass explicit repository, base, head, title, and sanitized body arguments. Do not use `--fill` for fallback PR creation.
7. If the human opted out, return the PR message draft, intended base/head, and gate status `complete`.
8. If the PR is created or an existing matching PR is reused, Report the PR URL, gate status `complete`, and any remaining follow-ups.

## Template

Use this template in the user's primary language. The Korean headings below are examples for Korean sessions; translate the headings and helper text when the user's primary language is not Korean.

```markdown
## 무엇을 수정하였는가?
한 줄 요약:

- 수정 대상: 작업 내용

## 왜 수정하였는가?
PR의 작업 맥락을 먼저 소개.
각 수정 대상에서 주요 수정사항의 작업 맥락과 수정 이유 작성.

## 이번 단계에서 포함하지 않은 것
PR 계획에 포함하지 않은 범위를 명시한다.

## 테스트 방법
- pytest 결과가 있으면 결과만 요약한다.
- 사람이 직접 수동 테스트해야 하면 실행 방법을 bash 코드로 작성한다.

## Follow-ups
후속 PR 내용. 없으면 이 섹션은 생략한다.
```

If the active repository `AGENTS.md` mandates different section headings, use those exact headings while preserving this template's meaning.

## Rules

- Include the Issue reference.
- Keep "included" and "not included" aligned with the approved PR plan.
- Mention only tests with actual command output or user-provided evidence.
- Do not include the concrete spec path unless the repo asks for it.
- Do not invent PR URLs or GitHub issue numbers.
- Open the pull request after drafting the PR message unless the human explicitly says not to open a GitHub PR.
- After creating or reusing one PR, report `complete` unless the human asks for revisions.

## PR Write Safety Gate

Before creating or updating a pull request:

- Redact or summarize secrets, credentials, tokens, personal data, private URLs, and absolute local paths from the PR title, body, quoted output, test output, review evidence, and references.
- Pull request base and head repositories must match the current repository remote unless the human explicitly confirms a cross-repository PR immediately before the write.
- If reviewed local changes are not committed and pushed to the PR head branch, stop before creating the PR. If the reviewed changes are not committed or pushed, report gate status `needs-commit-or-push`, the intended base/head, and the missing commit or push step.
- Before creating a pull request, check for an existing open PR for the same head branch and base branch.
- Reuse an existing PR only when its Issue reference, title/body marker, head owner/repo, base branch, and intended base SHA match the current evidence.
- After creation, treat the PR URL and number as the idempotency key. Do not create duplicate PRs on retry; update or reuse the existing PR instead.
