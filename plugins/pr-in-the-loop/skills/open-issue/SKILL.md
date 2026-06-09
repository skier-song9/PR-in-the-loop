---
name: open-issue
description: Use when a user wants to start or resume engineering work by discovering what should be done, inspecting current project state, turning vague work context into one concrete problem, or creating/publishing a GitHub Issue. Trigger for task-finding, project triage, daily engineering kickoff, backlog discovery, external-work-context synthesis, GitHub issue drafting, and requests to proceed with a named workstream before implementation begins. Do not use for implementation, PR planning, code review, or opening pull requests after an issue already exists.
---

# Open Issue

Turn current work context into exactly one concrete GitHub Issue.

This skill is the entry point before implementation. It should understand the project, identify the next problem worth solving, write a clear issue, and publish it to GitHub when write access is available.

## Rules

- Create one issue only unless the user explicitly asks for multiple.
- Do not implement code, write a PR plan, or open a PR.
- Prefer actual project/tool state over assumptions.
- At the start of each run, inspect the user's work environment memory before deciding which sources to query.
- Ask the user for missing information when available evidence is not enough to define a concrete issue.
- If the user must make a decision, present at least 3 recommended options. For each option, explain the reason to choose it, the tradeoff, and which option you recommend.
- If one problem is clear, proceed without extra confirmation and open the issue.
- If GitHub write access is unavailable, produce the final issue draft and report the exact blocker.

## Work Environment Memory

Use a local Markdown file as platform-neutral memory:

- Default path: `.memory/open-issue/work-context.md`
- This path is intentionally local and should be ignored by git.
- It works across Codex, Claude Code, Gemini, and other agents because it is just a repo-local text file.
- Never store secrets, API keys, cookies, private tokens, or copied private message bodies in this file.

Read `references/local-work-environment-memory.md` before creating or updating this file.

Before reading or writing the memory file, run the bundled guard script from the target project root:

```bash
sh <plugin-root>/scripts/ensure-memory-gitignore.sh
```

Resolve any script failure before continuing. This script creates `.memory/open-issue/` if needed, adds `.memory/` to the target repo `.gitignore`, and verifies the memory file is ignored when the target is a git repository.

## Context Sources

Inspect work environment context first:

- Existing `.memory/open-issue/work-context.md`
- User-provided links or instructions in the current request
- Local project hints for Slack, Notion, Linear, Jira, Google Workspace, GitHub Projects, or other work systems

Then inspect local project context:

- `git status --short --branch`, current branch, remotes, recent commits
- README, docs, project manifests, tests, CI config, `.github/`
- TODO/FIXME comments, failing tests, local notes, issue/PR references in files

Then use available work tools when relevant. Do not claim a source was checked if the tool is unavailable. See `references/work-context-sources.md` for source-specific guidance.

Prefer this order:

1. User-provided request and links
2. Work environment memory
3. Local repository state
4. GitHub issues, PRs, discussions, projects, CI
5. Slack, Linear/Jira, Notion, Google Workspace, and other connected work tools
6. Official docs or web sources when needed to define the problem accurately

## Workflow

1. **Load Work Environment**
   - Run `sh <plugin-root>/scripts/ensure-memory-gitignore.sh` from the target project root. Stop if it fails.
   - Read `.memory/open-issue/work-context.md` if it exists.
   - If that Markdown file exists, use it and skip the work-environment discovery question unless the user asks to refresh it or the file is clearly stale/contradictory.
   - If it does not exist, treat this as first-run setup and start the memory-file writing step before drafting an issue.
   - In first-run setup, look for repo hints such as `.github/`, issue URLs, Linear/Jira ticket IDs, Notion or Slack links, Google Docs links, docs mentioning ownership, and project-management references.
   - If repo hints are enough, create `.memory/open-issue/work-context.md` from stable source names and links, then continue.
   - If repo hints are not enough, ask the user which sources to use. Present at least 3 options and recommend one. Example option categories: GitHub-only, GitHub plus project docs, GitHub plus workplace tools.
   - After the user provides environment details, create or update `.memory/open-issue/work-context.md` with stable source names and links only.

2. **Orient Project**
   - Identify repository owner/name from `git remote -v` or GitHub context.
   - Summarize current state in 2-4 bullets for yourself: branch, dirty files, important docs, active work signals.
   - Find existing `.github/` issue templates before drafting.

3. **Recognize the Problem**
   - Convert broad work context into a single issue-sized problem.
   - The problem must have a clear current state, desired state, and reason it matters.
   - Avoid umbrella issues such as "improve the project" unless the user explicitly wants an epic.

4. **Resolve Ambiguity**
   - If the issue scope, priority, source of truth, owner, or expected outcome is ambiguous, stop and ask the user before drafting.
   - Ask one focused question at a time.
   - When asking the user to choose a direction, provide at least 3 options:
     - `Recommended`: the option you would choose, with the reason.
     - `Alternative`: a narrower or lower-risk option, with the tradeoff.
     - `Alternative`: a broader or faster option, with the tradeoff.
   - Do not ask for confirmation when the evidence points to one clear issue-sized problem.

5. **Check Existing Work**
   - Search open issues and PRs for duplicates.
   - If a duplicate exists, update or reference it instead of opening a new issue, unless the user asked for a new tracking issue.
   - Capture useful references: issue/PR URLs, Slack threads, Linear tickets, Notion pages, Google Docs, specs, official docs.

6. **Draft the Issue**
   - Use the project's existing issue template if `.github/` contains an issue-related template.
   - If there are multiple issue templates, choose the one closest to the problem type.
   - If the template is a YAML issue form, fill its fields faithfully; do not invent required fields.
   - If no issue template exists, use the default template below.
   - Write in the user's language. For Korean issue text, read `../../references/korean-writing-tips.md` first and apply it.

7. **Publish**
   - Prefer an authenticated GitHub connector/app if available.
   - Otherwise use `gh issue create` when `gh auth status` confirms write access.
   - Title format: concise imperative or problem statement, no trailing period.
   - Add labels/milestone/assignee only when project convention or user instruction makes them clear.
   - Return the issue URL and a one-line summary.

## Default Issue Template

Use this exact header structure only when the project has no issue template:

```markdown
## Description
<One-line summary of the problem. Then explain the context: why this should be solved, what current behavior or gap exists, and the intended direction.>

## Task
- [ ] <First concrete step>
- [ ] <Next concrete step>
- [ ] <Validation or documentation step>

## Reference
- <Related issue, PR, work-tool URL, official doc, or external reference>
```

If there are no references, write `- 없음` under `## Reference`.

## Quality Bar

Before publishing, verify:

- The issue is about one problem, not a bundle of unrelated work.
- The first sentence says what problem will be solved.
- Tasks are ordered and executable.
- References are URLs or clear local file paths.
- `scripts/ensure-memory-gitignore.sh` ran successfully or an equivalent `.memory/` ignore check passed.
- Work environment memory was read, or first-run memory setup created `.memory/open-issue/work-context.md` before issue drafting.
- Ambiguity was resolved through evidence or a user decision with 3 options and reasons.
- No placeholder text remains.
- Existing project issue template rules were honored.
