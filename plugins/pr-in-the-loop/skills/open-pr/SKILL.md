---
name: open-pr
description: Use when implementation and review are done, or when completed changes are ready to be represented as a pull request and the user asks the agent to prepare that pull request regardless of the user's exact phrasing.
---

# Open PR

Draft the final PR message from evidence, not memory.

## Trigger Rule

Use this skill when completed changes are ready to be represented as a pull request and the user's intent is for the agent to prepare that pull request, regardless of the user's exact phrasing. Open PR is the mandatory evidence-to-PR-body step before any pull request creation or publication flow in the GitHub PR Workflow plugin.

This rule is about the user's intent to turn completed work into a pull request, not about matching a fixed verb such as create, open, publish, upload, raise, or draft.

## Language Rule

Write the PR message in the user's primary language. Infer the user's primary language from the current request and surrounding agent conversation. If the conversation is mixed, use the language the user used when asking for the PR message. Keep Issue references, file paths, commands, code identifiers, and quoted output unchanged.

## Inputs

Read the approved PR plan, GitHub Issue, final diff, tests actually run, and HTML review report if present. Do not invent test results or follow-ups.

## Preconditions

- The HTML review has been read by the human, or the human confirmed that no further fixes are needed.
- Critical and Important findings are fixed, explicitly deferred, or rejected with technical evidence.

If these are missing, stop and request the missing review decision.

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
- After drafting one PR message, report `complete` unless the human asks for revisions.
