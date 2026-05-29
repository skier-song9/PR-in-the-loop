---
name: pr-message-writer
description: Use when implementation and review are done and a Korean PR message is needed.
---

# PR Message Writer

Draft the final PR message from evidence, not memory.

## Inputs

Read the approved PR plan, GitHub Issue, final diff, tests actually run, and HTML review report if present. Do not invent test results or follow-ups.

## Preconditions

- The HTML review has been read by the human, or the human confirmed that no further fixes are needed.
- Critical and Important findings are fixed, explicitly deferred, or rejected with technical evidence.

If these are missing, stop and request the missing review decision.

## Template

Use this Korean template by default:

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
