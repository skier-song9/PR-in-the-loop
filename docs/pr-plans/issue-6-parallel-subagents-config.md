# Issue #6: sub-agent 병렬 spawn 지침과 agents config 설치 안내 강화 PR Plan

> Supersession note (2026-05-31): The latest human requirement supersedes the earlier `max_threads = 12` guidance below. Current implementation target is `max_threads = 16`, `max_depth = 1`, explicit consent before global config edits, writable tests/fixtures must be owned by `ASSIGNED_PATHS`, worker summaries include `Changed files outside ownership: yes/no`, and workers must not spawn nested subagents.

## Clarification Notes
- Blocking questions asked: 없음. 사용자가 확인할 스킬, 강화할 문구, 설치 문서에 넣을 config 값을 구체적으로 지정했다.
- Decisions that resolved ambiguity:
  - `docstring-parallel-implementation`의 sub-agent spawn instructions를 강화한다.
  - `INSTALL.md`에는 Codex `config.toml`의 `[agents]` 권장 설정을 안내한다.
  - `max_depth`는 사용자가 제안한 대로 `1`, `max_threads`는 `12`로 고정한다.
  - 기존 workflow의 승인 gate, DocString 위임, 파일 소유권 분리, 테스트/리뷰 흐름은 유지한다.
- Remaining ambiguity: 없음.
- Status: ambiguity-resolved

## Problem
현재 `docstring-parallel-implementation` 스킬은 병렬 수행이 가능한 조건을 “disjoint source files with independent tests and no shared generated artifact”로 설명하고, 안전한 파일 그룹마다 fresh worker를 dispatch하라고 지시한다. 그러나 병렬 sub-agent를 안정적으로 운용하는 데 필요한 다음 규칙은 명시적으로 충분하지 않다.

- 독립 작업에는 parallel subagents를 사용한다.
- 작업 하나당 sub-agent 하나를 spawn한다.
- 여러 write-capable agent가 같은 파일을 수정하지 않도록 한다.
- 조사는 read-only explorer agent로 분리한다.
- 모든 sub-agent를 기다린 뒤 결과를 통합한다.
- findings, changed files, risks, next actions가 포함된 structured summary를 반환한다.

또한 `INSTALL.md`에는 Codex `config.toml`에서 병렬 sub-agent thread 한도를 늘리는 `[agents]` 설정 안내가 없다. 사용자가 기대하는 기본 권장값은 다음과 같다.

```toml
[agents]
max_threads = 12
max_depth = 1
```

## Why This Matters
sub-agent 병렬화는 파일 소유권과 결과 통합 규칙이 명확할 때만 안정적이다. 지침이 느슨하면 같은 파일을 여러 worker가 수정하거나, 조사 agent가 쓰기 작업까지 수행하거나, 완료된 sub-agent 결과가 누락될 수 있다. 설치 문서에 agents thread 설정도 안내하면, 사용자가 병렬 sub-agent 기반 workflow를 사용할 때 필요한 Codex 설정을 더 쉽게 준비할 수 있다.

## Candidate Approaches
- Approach A: `docstring-parallel-implementation`에 병렬 spawn 운영 규칙을 별도 섹션으로 추가하고, `INSTALL.md`에 `[agents]` config 권장 설정을 추가한다. 가장 직접적으로 문제를 해결하며 기존 workflow를 바꾸지 않는다.
- Approach B: worker prompt template에만 병렬 규칙을 넣는다. worker에게는 도움이 되지만 main agent가 spawn을 설계하는 단계의 규칙이 약하게 남는다.
- Approach C: `INSTALL.md`만 수정한다. thread capacity는 안내할 수 있지만 스킬 자체의 병렬 안전성은 개선하지 못한다.
- Recommendation: Approach A. spawn 설계는 스킬 본문에, worker별 책임과 반환 형식은 worker prompt template 및 verification 규칙에 반영하는 것이 가장 명확하다.

## PR Breakdown
### PR1: 병렬 sub-agent 운영 규칙과 설치 config 안내 추가
- Goal: `docstring-parallel-implementation`의 병렬 sub-agent spawn instructions를 강화하고, 설치 문서에 Codex agents thread 설정 안내를 추가한다.
- Included:
  - `plugins/github-pr-workflow/skills/docstring-parallel-implementation/SKILL.md`에 parallel subagent spawn policy 추가
  - 독립 작업별 sub-agent 1개, write-capable agent의 파일 소유권 분리, read-only explorer agent 사용, wait-all 후 consolidation 규칙 추가
  - `Subagent Verification` 또는 새 summary 섹션에 findings, changed files, risks, next actions 반환 요구사항 추가
  - `plugins/github-pr-workflow/skills/docstring-parallel-implementation/references/worker-prompt-template.md`에 changed files, risks, next actions 반환 항목 보강
  - `INSTALL.md`에 `~/.codex/config.toml` 또는 Codex config 위치의 `[agents] max_threads = 12`, `max_depth = 1` 설정 확인/추가 안내
  - `tests/test_skill_requirements.py`에 새 스킬 지침과 설치 config 문구를 검증하는 assertion 추가
- Excluded:
  - Codex runtime의 실제 thread scheduler 변경
  - 사용자의 로컬 `~/.codex/config.toml` 직접 수정
  - Issue #5의 model/effort 선택 정책 구현
  - 다른 스킬의 sub-agent 정책 변경
- Depends on:
  - Issue #6
  - 현재 작업 중인 Issue #4/#5 문서 및 테스트 변경과 충돌하지 않는 통합
- Acceptance signals:
  - 스킬 본문이 독립 작업 병렬화, task당 sub-agent 1개, write-capable 파일 소유권 분리, read-only explorer, wait-all consolidation을 명시한다.
  - worker/subagent 결과 요약에 findings, changed files, risks, next actions가 포함된다.
  - `INSTALL.md`가 `[agents] max_threads = 12`, `max_depth = 1` 설정을 확인하고 없으면 추가하도록 안내한다.
  - `python3 -m unittest discover -s tests` 통과
  - `python3 scripts/check_plugins.py` 통과

## Follow-ups
Issue #5에서 model/effort 선택 정책을 별도로 구현할 때, 이 PR의 병렬 spawn policy와 충돌하지 않도록 같은 섹션에 통합할 수 있다.

## Human Review Notes
Status: needs-review
