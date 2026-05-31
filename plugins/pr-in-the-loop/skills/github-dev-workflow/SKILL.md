---
name: github-dev-workflow
description: Use when running an end-to-end GitHub Issue to PR development workflow for a coding task.
---

# GitHub Dev Workflow

Run the user's GitHub work loop while preserving the Superpowers spine.

## Required Order

1. **REQUIRED SUB-SKILL:** Use `superpowers:brainstorming` discipline through `pr-in-the-loop:issue`.
2. **REQUIRED SUB-SKILL:** Use `superpowers:writing-plans` discipline through `pr-in-the-loop:planning-pr`.
3. **REQUIRED SUB-SKILL:** Use `superpowers:subagent-driven-development` discipline through `pr-in-the-loop:parallel-development`.
4. **REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review` discipline through `pr-in-the-loop:multi-view-code-review`.
5. Use `pr-in-the-loop:open-pr` after the human accepts the HTML review or confirms no more fixes remain. When the user asks the agent to prepare the completed work as a pull request, use `pr-in-the-loop:open-pr` before creating or publishing the pull request.

If a Superpowers skill is unavailable, follow the same gate locally and report the fallback.

## Gates

- Do not implement before a GitHub Issue exists or an issue draft is explicitly accepted as dry-run output.
- After `pr-in-the-loop:issue`, create or draft a GitHub Issue, then stop at the Issue boundary; starting the separate `pr-in-the-loop:planning-pr` PR-plan step requires explicit human approval. If `planning-pr` still requires an approved PR plan artifact and none exists, stop and request that artifact instead of inventing one.
- Do not write a concrete implementation spec until the PR plan markdown has been human-reviewed and approved.
- Do not implement until a concrete spec exists and traces back to the approved PR plan.
- Do not commit the concrete spec or HTML review report.
- Do not draft the PR message until review findings are resolved or deferred by the human.

## Evidence Rules

- Prefer current repository files, `AGENTS.md`, issue templates, GitHub records, diffs, and test output over memory.
- If using session history as background, treat it as pattern evidence only.
- Never invent issue numbers, test results, review approvals, or GitHub URLs.

## Output

At every handoff, report:

- current artifact path or GitHub URL
- gate status: `needs-human-review`, `ready-for-spec`, `ready-for-implementation`, `ready-for-review`, `ready-for-pr-message`, or `complete`
- next required skill or human action
