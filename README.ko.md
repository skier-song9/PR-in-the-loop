# PR In The Loop

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Codex Plugins](https://img.shields.io/badge/Codex-plugins-2563EB)](.agents/plugins/marketplace.json)
[![Marketplace](https://img.shields.io/badge/marketplace-pr--in--the--loop-111827)](.agents/plugins/marketplace.json)

사람이 PR 루프 안에 남아 있도록 설계한 Codex 플러그인 marketplace.

[English](README.md) | [설치 가이드](INSTALL.md)

## Quickstart

```bash
git clone https://github.com/skier-song9/PR-in-the-loop.git
cd PR-in-the-loop
codex plugin marketplace add "$(pwd)"
codex plugin add pr-in-the-loop@pr-in-the-loop
```

설치 후 새 Codex thread를 시작해야 새 skill이 로드된다. 시작 skill은 `$pr-in-the-loop:github-dev-workflow`이다.

## How It Works

PR In The Loop는 Codex 개발 워크플로우를 설치 가능한 플러그인으로 묶는다. 핵심 플러그인인 `pr-in-the-loop`는 Superpowers식 개발 흐름을 유지한다.

1. 문제를 인식하고 GitHub Issue를 만들거나 draft로 작성한 뒤, PR 계획 전 명시적 승인에서 멈춘다.
2. 승인 후 `docs/pr-plans/` 아래에 사람이 리뷰하는 짧은 PR 계획 문서를 작성한다.
3. 승인된 PR 계획에서 커밋하지 않는 구현 spec을 생성한다.
4. 파일별 책임을 DocString/comment로 위임하고 fresh subagent에게 구현을 맡긴다.
5. 유형별 reviewer subagent를 병렬 호출해 HTML 리뷰 보고서를 만든다.
6. Issue, diff, test, review 근거로 PR 메시지를 작성한다.

목표는 완전 자동화가 아니다. PR 범위, 리뷰 결과, 최종 PR 맥락은 사람이 결정한다.

## Installation

자세한 설치 절차와 AI agent에게 줄 프롬프트는 [INSTALL.md](INSTALL.md)에 있다.

### Codex App 또는 Codex CLI

이 repo를 로컬 marketplace로 등록한다.

```bash
codex plugin marketplace add "$(pwd)"
```

플러그인을 설치한다.

```bash
codex plugin add pr-in-the-loop@pr-in-the-loop
```

### Update

```bash
cd PR-in-the-loop
git pull
codex plugin add pr-in-the-loop@pr-in-the-loop
```

업데이트 후 새 Codex thread를 열고 `$pr-in-the-loop:github-dev-workflow`를 호출한다.

## The Basic Workflow

1. `pr-in-the-loop:issue` - repo 맥락을 확인하고 GitHub Issue를 만들거나 draft로 작성한 뒤 멈춘다. PR 계획 단계로 이동하려면 명시적 사용자 승인이 필요하다.
2. `pr-in-the-loop:planning-pr` - 승인된 Issue를 읽고 접근안을 구체화한 뒤 `docs/pr-plans/` 아래에 사람이 리뷰하는 짧은 PR 계획 문서를 작성한다.
3. `pr-in-the-loop:parallel-development` - 승인된 PR 계획에서 커밋하지 않는 구현 spec을 생성하고, spec의 파일별 책임을 짧은 DocString/comment로 옮긴 뒤 안전한 파일 그룹만 fresh subagent에게 병렬 위임한다.
4. `pr-in-the-loop:multi-view-code-review` - 유형별 reviewer subagent를 병렬 실행하고 `docs/reviews/` 아래 HTML 보고서 하나로 합친다.
5. `pr-in-the-loop:open-pr` - 사람이 리뷰 상태를 승인한 뒤 근거 기반 PR 메시지를 작성한다.

## What's Inside

### Plugin Catalog

| Plugin | Category | Purpose |
|---|---|---|
| `pr-in-the-loop` | Coding | Issue부터 PR 메시지까지 계획, 구현, 리뷰를 연결하는 워크플로우. |

### `pr-in-the-loop` Skills

| Skill | When to use |
|---|---|
| `pr-in-the-loop:github-dev-workflow` | Issue-to-PR 전체 흐름을 실행할 때. |
| `pr-in-the-loop:issue` | 문제에서 시작해 GitHub Issue를 만들거나 draft로 작성하고 PR planning 전에 멈출 때. |
| `pr-in-the-loop:planning-pr` | 승인된 Issue를 짧고 사람이 리뷰하는 PR 계획 문서로 바꿀 때. |
| `pr-in-the-loop:parallel-development` | PR 계획에서 커밋하지 않는 구현 spec을 생성하고 파일별 책임 위임과 안전한 subagent 구현이 필요할 때. |
| `pr-in-the-loop:multi-view-code-review` | 유형별 reviewer subagent로 코드 리뷰하고 HTML 보고서를 만들 때. |
| `pr-in-the-loop:open-pr` | 근거 기반 PR 메시지가 필요할 때. |

### Reviewer Types

`pr-in-the-loop:multi-view-code-review`에는 다음 reviewer가 포함된다.

- spec compliance
- code quality and edge cases
- ADK and agent architecture
- data, migration, and contract risk
- docs and PR context
- security, idempotency, and deduplication

모든 지적 사항은 구체적 예시를 포함해야 한다.

## Repository Structure

```text
.agents/plugins/marketplace.json
plugins/
  pr-in-the-loop/
    .codex-plugin/plugin.json
    skills/
scripts/check_plugins.py
```

## Validate

가벼운 repo 구조 검증을 실행한다.

```bash
python3 scripts/check_plugins.py
```

Python 표준 라이브러리만 사용해 JSON, marketplace path, plugin name, skill frontmatter를 확인한다.

## Philosophy

- 구현 전 사람이 PR 범위를 리뷰한다.
- 기억보다 근거를 우선한다.
- spec과 HTML 리뷰 보고서는 커밋하지 않는다.
- 구현과 리뷰에는 fresh subagent를 쓴다.
- 모든 리뷰 이슈는 구체적 예시를 포함한다.
- 넓은 자동화보다 작은 플러그인 단위를 선호한다.

## Contributing

1. plugin 폴더명과 manifest 이름을 같게 유지한다.
2. marketplace path는 `./plugins/plugin-name`처럼 repo root 기준 상대 경로로 유지한다.
3. skill에는 명확한 trigger, gate, 종료 조건을 둔다.
4. `python3 scripts/check_plugins.py`를 실행한다.
5. 변경 내용과 검증 결과를 포함해 PR을 연다.

## License

Apache-2.0. [LICENSE](LICENSE)를 참고.
