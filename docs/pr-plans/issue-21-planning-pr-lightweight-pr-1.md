# Issue #21: planning-pr 스킬을 경량 PR 계획 작성 흐름으로 재구성 PR Plan

> For agentic workers: REQUIRED SUB-SKILL: Use `pr-in-the-loop:parallel-development`.

## 목표
`pr-in-the-loop:planning-pr`가 승인된 GitHub Issue를 바탕으로 사용자와 접근안을 확정하고, 짧은 PR plan 문서를 작성하도록 재구성한다.

## 이번 단계에 포함하는 것
- `planning-pr` 스킬을 Issue 기반 PR plan authoring 단계로 변경한다.
- `superpowers:brainstorming` 방식의 ambiguity gate, 접근안 비교, 사용자 승인 gate를 명시한다.
- 기본 파일명과 저장 위치를 `docs/pr-plans/issue-[issue number]-[issue title]-pr-[pr number].md` / `docs/pr-plans/`로 정의한다.
- 새 경량 PR plan template을 `planning-pr/references/pr-plan-template.md`에 추가한다.
- 기존 spec 생성 책임과 `planning-pr/references/spec-template.md`를 제거한다.
- README, `github-dev-workflow`, agent metadata, tests를 새 workflow 역할에 맞게 갱신한다.

## 이번 단계에 포함하지 않는 것
- `parallel-development`가 PR plan에서 spec을 생성하고 구현을 시작하는 흐름은 Issue #22 범위다.
- `open-pr`가 GitHub PR을 실제 생성하는 흐름은 Issue #23 범위다.
- Issue creation behavior 자체는 Issue #20 범위로 완료되어 있다.

## 테스트 목표
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_planning_pr_creates_lightweight_pr_plan_from_issue` 가 새 planning-pr 역할을 검증한다.
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_planning_pr_template_uses_compact_required_sections` 가 새 template을 검증한다.
- `python3 -m unittest tests.test_skill_requirements` 전체가 통과한다.
- `python3 scripts/check_plugins.py` 가 통과한다.
