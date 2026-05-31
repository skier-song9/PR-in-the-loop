# Issue #23: open-pr 스킬이 기본적으로 GitHub PR을 생성하도록 강화 PR Plan

> For agentic workers: REQUIRED SUB-SKILL: Use `pr-in-the-loop:parallel-development`.
> This PR plan is not implementation permission. Continue only after human approval; `pr-in-the-loop:parallel-development` creates the uncommitted concrete spec before implementation.

## 목표
`open-pr`가 완료된 변경사항의 PR 메시지를 작성한 뒤, 사용자가 명시적으로 GitHub PR open을 금지하지 않는 한 실제 GitHub PR까지 생성하도록 한다.

## 이번 단계에 포함하는 것
- `open-pr` trigger/process를 PR message drafting + GitHub PR creation으로 변경한다.
- 명시적 opt-out 문구가 있을 때만 PR creation 없이 draft message로 멈추도록 한다.
- GitHub app/plugin 우선, `gh` CLI fallback을 명시한다.
- PR body/test/review evidence는 실제 근거만 사용하고 invented 결과를 금지하는 기존 규칙을 유지한다.
- PR write safety, duplicate PR idempotency, output URL/gate status 규칙을 추가한다.
- README, `github-dev-workflow`, agent metadata, tests를 새 역할에 맞게 갱신한다.

## 이번 단계에 포함하지 않는 것
- Issue/PR plan/spec/implementation/review workflow 단계의 의미 변경은 포함하지 않는다.
- GitHub app 권한 문제 자체를 해결하지 않는다. 권한 문제가 있으면 `gh` fallback을 사용하도록 지시만 한다.

## 테스트 목표
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_open_pr_creates_github_pr_by_default_with_opt_out` 가 default PR creation과 opt-out을 검증한다.
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_open_pr_requires_write_safety_and_idempotency` 가 PR write safety와 duplicate prevention을 검증한다.
- `python3 -m unittest tests.test_skill_requirements` 전체가 통과한다.
- `python3 scripts/check_plugins.py` 가 통과한다.
