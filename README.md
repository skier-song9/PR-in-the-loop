# PR In The Loop

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Codex Plugins](https://img.shields.io/badge/Codex-plugins-2563EB)](.agents/plugins/marketplace.json)
[![Marketplace](https://img.shields.io/badge/marketplace-pr--in--the--loop-111827)](.agents/plugins/marketplace.json)

Codex plugin marketplace for human-in-the-loop PR development.

[한국어](README.ko.md) | [Install guide](INSTALL.md)

## Quickstart

```bash
git clone https://github.com/skier-song9/PR-in-the-loop.git
cd PR-in-the-loop
codex plugin marketplace add "$(pwd)"
codex plugin add pr-in-the-loop@pr-in-the-loop
```

Start a new Codex thread after installing so the new skills load, then invoke `$pr-in-the-loop:github-dev-workflow`.

## How It Works

PR In The Loop packages Codex workflows as installable plugins. The main plugin, `pr-in-the-loop`, keeps the Superpowers-style development spine:

1. identify a problem and create a GitHub Issue
2. write a human-reviewed PR plan under `docs/`
3. convert the approved PR plan into an uncommitted implementation spec
4. delegate file-scoped work through fresh subagents
5. run typed parallel code review into an HTML report
6. draft a PR message from real issue, diff, test, and review evidence

The goal is not full automation. The human stays in the loop at the decisions that matter: PR scope, review findings, and final PR context.

## Installation

Detailed installation and AI-agent handoff prompts live in [INSTALL.md](INSTALL.md).

### Codex App or Codex CLI

Register this repo as a local marketplace:

```bash
codex plugin marketplace add "$(pwd)"
```

Install the plugin:

```bash
codex plugin add pr-in-the-loop@pr-in-the-loop
```

### Update

```bash
cd PR-in-the-loop
git pull
codex plugin add pr-in-the-loop@pr-in-the-loop
```

Open a new Codex thread after updating, then invoke `$pr-in-the-loop:github-dev-workflow`.

## The Basic Workflow

1. `pr-in-the-loop:issue` - inspect repo context, create or draft a GitHub Issue, write a PR plan, and stop for human review.
2. `pr-in-the-loop:planning-pr` - use Superpowers planning discipline to turn the approved PR plan into a concrete implementation spec. The spec is not human-reviewed and is not committed.
3. `pr-in-the-loop:parallel-development` - copy each file's responsibility from the spec into a short DocString or comment, then dispatch safe file groups to fresh subagents.
4. `pr-in-the-loop:multi-view-code-review` - run typed reviewer subagents in parallel and synthesize one HTML report under `docs/reviews/`.
5. `pr-in-the-loop:open-pr` - draft the final PR message after the human accepts the review state.

## What's Inside

### Plugin Catalog

| Plugin | Category | Purpose |
|---|---|---|
| `pr-in-the-loop` | Coding | Issue-to-PR workflow for scoped planning, implementation, review, and PR messaging. |

### `pr-in-the-loop` Skills

| Skill | When to use |
|---|---|
| `pr-in-the-loop:github-dev-workflow` | Run the full Issue-to-PR workflow. |
| `pr-in-the-loop:issue` | Start from a problem, create/draft a GitHub Issue, and write a human-reviewed PR plan. |
| `pr-in-the-loop:planning-pr` | Convert an approved PR plan into a concrete, uncommitted implementation spec. |
| `pr-in-the-loop:parallel-development` | Implement from a concrete spec with file-scoped delegation and safe subagents. |
| `pr-in-the-loop:multi-view-code-review` | Review code through typed subagents and write one HTML report. |
| `pr-in-the-loop:open-pr` | Draft a PR message from evidence. |

### Reviewer Types

`pr-in-the-loop:multi-view-code-review` includes reviewers for:

- spec compliance
- code quality and edge cases
- ADK and agent architecture
- data, migration, and contract risk
- docs and PR context
- security, idempotency, and deduplication

Every finding must include a concrete example.

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

Run the lightweight repository check:

```bash
python3 scripts/check_plugins.py
```

This validates JSON files, marketplace paths, plugin names, and skill frontmatter using only the Python standard library.

## Philosophy

- Human-reviewed PR scope before implementation
- Evidence over memory
- Uncommitted specs and review reports
- Fresh subagents for implementation and review
- Concrete examples for every review issue
- Small plugin units instead of broad automation

## Contributing

1. Keep plugin names and manifest names identical.
2. Keep marketplace paths relative to the repo root, like `./plugins/plugin-name`.
3. Add or update skills with clear triggers, gates, and termination conditions.
4. Run `python3 scripts/check_plugins.py`.
5. Open a PR with the behavior change and validation result.

## License

Apache-2.0. See [LICENSE](LICENSE).
