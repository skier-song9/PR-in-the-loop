# PR Plan Template

Translate the headings and helper text to the detected user language unless the human supplied exact headings. The Korean headings below are the default Korean rendering of the required section meanings.

```markdown
# [document title]
> For agentic workers: REQUIRED SUB-SKILL: Use `pr-in-the-loop:parallel-development`.
> This PR plan is not implementation permission. Continue only after human approval; `pr-in-the-loop:parallel-development` creates the uncommitted concrete spec before implementation.

## 목표
[이번 PR 에서 달성해야 하는 항목들을 작성한다.]

## 이번 단계에 포함하는 것
[이번 PR에서 작업할 내용들을 작성한다.]

## 이번 단계에 포함하지 않는 것
[이번 PR의 작업 범위를 벗어나는 것들을 기록한다. code review에게 이번 작업의 범위를 명확히 전달한다.]

## 테스트 목표
[이번 PR 작업을 어떻게 테스트하고 검증할 것인지 계획을 세운다. 해당 테스트를 성공하면 구현/개발을 완료한 것으로 간주한다.]
```

Optional sections may be added when the Issue needs them, such as a db schema plan, API contract table, migration order, or architecture sequence diagram.
