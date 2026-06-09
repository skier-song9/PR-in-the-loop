# Plugin Test Projects

Use this reference only when the user asks to test, validate, or dogfood this plugin. Do not load it during normal `open-issue` runs for a user's active project.

## Canonical Sandbox

- Repository: https://github.com/skier-song9/pr-in-the-loop-test-game
- Purpose: live sandbox for testing the `pr-in-the-loop` plugin against a small browser game project.
- Product shape: simple web browser car racing game.
- Primary test skill: `open-issue`.

## How To Use It

1. Clone the sandbox outside the plugin repository, preferably under a temporary or worktree-specific path.
2. Run `open-issue` from the sandbox repository root.
3. Treat the sandbox as a real target project: inspect git state, `.github/`, docs, app files, tests, issues, and PRs before drafting an issue.
4. Use `.memory/open-issue/work-context.md` in the sandbox repo for first-run work-environment memory. If no workplace tools are known, record GitHub Issues as the default tracker and mark Slack, Notion, Linear, Jira, and Google Workspace as `none known`.
5. Do not commit `.memory/` in the sandbox. The `ensure-memory-gitignore.sh` script must add or verify `.memory/` in that repo before memory is read or written.

## Expected Validation Scenarios

- First-run memory setup: the skill should create or update local work-environment memory before issue drafting.
- GitHub-only workflow: the skill should still produce a concrete issue when no Slack, Notion, Linear, Jira, or Google Workspace context exists.
- Empty or minimal repo handling: if the sandbox has no usable app structure yet, the first issue should define a single initial project problem, such as creating the minimal playable browser racing game scaffold.
- Existing-project handling: if the sandbox already contains game code, the skill should inspect the app and choose one issue-sized next improvement or bug.
- Duplicate detection: before publishing a new issue, the skill should search existing sandbox issues and PRs.
- Template fallback: if the sandbox has no `.github/` issue template, use the `open-issue` default issue template.

## Boundaries

- This sandbox is not a dependency of plugin validation scripts; unavailable GitHub access should not make local skill/plugin validation fail.
- Do not hard-code sandbox-specific issue content into `open-issue`.
- Do not use the sandbox repository for production examples, user project defaults, or unrelated manual tests.
