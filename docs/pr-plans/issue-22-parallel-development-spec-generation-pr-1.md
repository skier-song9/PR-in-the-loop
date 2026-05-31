# Issue #22: parallel-development 스킬이 PR plan에서 spec을 생성한 뒤 구현하도록 재구성 PR Plan

> For agentic workers: REQUIRED SUB-SKILL: Use `pr-in-the-loop:parallel-development`.
> This PR plan is not implementation permission. Continue only after human approval; `pr-in-the-loop:parallel-development` creates the uncommitted concrete spec before implementation.

## 목표
`parallel-development`가 human-approved PR plan을 읽어 `docs/specs/` 아래 concrete spec을 먼저 생성하고, 그 뒤 기존 파일별 위임/병렬 구현 흐름을 실행하도록 한다.

## 이번 단계에 포함하는 것
- `parallel-development` precondition을 approved PR plan 기반으로 갱신한다.
- `superpowers:writing-plans`를 사용해 concrete spec을 생성하는 단계를 process 앞부분에 추가한다.
- spec 기본 저장 위치를 `docs/specs/`로 정의한다.
- spec title 바로 아래에 `> For agentic workers: Never commit this file.` 문구를 강제한다.
- spec 파일이 staged/committed 되지 않도록 확인 gate를 추가한다.
- `planning-pr`에서 남아 있던 spec-missing compatibility gate를 제거하고 README/workflow/tests를 갱신한다.

## 이번 단계에 포함하지 않는 것
- `planning-pr`의 PR plan authoring 세부 정책 변경은 Issue #21 범위다.
- worker delegation, model/effort selection, reviewer flow의 의미는 유지한다.
- `open-pr`가 GitHub PR을 실제 생성하는 변경은 Issue #23 범위다.

## 테스트 목표
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_parallel_development_generates_uncommitted_spec_from_pr_plan` 가 새 spec 생성 gate를 검증한다.
- `python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_parallel_development_spec_template_requires_never_commit_notice` 가 새 spec template을 검증한다.
- `python3 -m unittest tests.test_skill_requirements` 전체가 통과한다.
- `python3 scripts/check_plugins.py` 가 통과한다.
