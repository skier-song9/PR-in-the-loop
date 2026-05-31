# Issue #20: issue 스킬을 Issue 발행 전용 흐름으로 축소 PR Plan

> For agentic workers: REQUIRED SUB-SKILL: Use `pr-in-the-loop:parallel-development`.

## 목표
`pr-in-the-loop:issue`가 ambiguity gate 이후 GitHub Issue만 발행하고 멈추도록 역할을 축소한다.

## 이번 단계에 포함하는 것
- `issue` 스킬 설명, language rule, ambiguity gate, process를 Issue-only 흐름에 맞게 수정한다.
- Issue 발행 후 `planning-pr`로 넘어가려면 명시적 사용자 승인이 필요하다는 gate를 추가한다.
- `issue` agent metadata와 README workflow 설명을 새 역할에 맞게 갱신한다.
- 기존 PR plan 작성 책임과 `issue/references/pr-plan-template.md` 의존을 제거한다.
- regression tests로 Issue-only 계약과 documentation surface를 고정한다.

## 이번 단계에 포함하지 않는 것
- `planning-pr`가 새 PR plan 템플릿을 작성하도록 바꾸는 작업은 Issue #21 범위로 남긴다.
- `parallel-development`가 spec을 생성하도록 바꾸는 작업은 Issue #22 범위로 남긴다.
- `open-pr`가 실제 PR을 생성하도록 바꾸는 작업은 Issue #23 범위로 남긴다.
- GitHub Issue body template 자체의 `Description / Tasks / References` 구조는 변경하지 않는다.

## 테스트 목표
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_issue_skill_is_issue_only_and_requires_planning_pr_approval` 가 새 Issue-only gate를 검증한다.
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_issue_language_detection_applies_only_to_issue_artifacts` 가 PR plan 언어 적용 문구가 제거되었는지 검증한다.
- `python3 -m unittest tests.test_skill_requirements` 전체가 통과한다.
- `python3 scripts/check_plugins.py` 가 plugin structure를 통과한다.
