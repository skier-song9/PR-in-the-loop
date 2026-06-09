# Local Work Environment Memory

Use `.memory/open-issue/work-context.md` as the persistent work environment memory for this skill.

## Why This File

- Platform-neutral: any agent can read and write Markdown.
- Repo-local: context follows the project directory.
- Private by default: `.memory/` should be listed in `.gitignore`.
- Tool-agnostic: works whether the current agent is Codex, Claude Code, Gemini, or another CLI.

Do not use platform-native memory as the source of truth for this skill. It may not transfer across agents.

## When to Read

Read this file at the start of every `open-issue` run before querying workplace tools or drafting an issue.

Before reading or writing it, run the bundled script from the target project root:

```bash
sh <plugin-root>/scripts/ensure-memory-gitignore.sh
```

If the script fails, stop and resolve the `.gitignore` problem before creating or reading the memory file.

If `.memory/open-issue/work-context.md` exists, use it and skip asking the user to describe their work environment. Ask only when the user requests a refresh or the file conflicts with current evidence.

If it does not exist:

1. Inspect the repo for hints: `.github/`, issue/PR URLs, ticket IDs, docs, owner notes, Slack/Notion/Linear/Jira/Google links.
2. Start first-run memory setup before drafting any issue.
3. If repo hints are enough, create `.memory/open-issue/work-context.md` from stable source names and links.
4. If workplace context is missing, ask the user for the environment before drafting.

## When to Ask

Ask when any of these are unknown and matter for the issue:

- Source of truth: GitHub Issues, Linear, Jira, Notion, Slack, Google Docs, or another system.
- Priority signal: roadmap, sprint board, incident channel, customer report, CI failure, release deadline.
- Ownership: team, maintainer, assignee, reviewer, project area.
- Reference location: Slack channel/thread, Notion page, Linear/Jira project, Google Drive folder.

When asking for a decision, provide at least 3 options:

- `Recommended`: usually GitHub plus local repo evidence, because it is reproducible and issue-native.
- `Alternative`: GitHub plus project docs, lower external-tool dependency but may miss workplace priority.
- `Alternative`: GitHub plus workplace tools, richer context but requires connectors or user-provided links.

## What to Store

Store stable navigation facts, not transient task details:

```markdown
# Open Issue Work Context

## Project
- Repository: <owner/repo or URL>
- Default issue tracker: GitHub Issues
- Primary planning source: <GitHub Projects | Linear | Jira | Notion | none known>
- Primary communication source: <Slack channel/thread pattern | none known>
- Spec/document source: <Notion page | Google Drive folder | docs path | none known>

## Source Links
- GitHub Issues: <url>
- Project board: <url>
- Linear/Jira project: <url>
- Notion workspace/page: <url>
- Slack channel/thread: <url>
- Google Drive/Docs: <url>

## Preferences
- Issue language: <Korean | English | match user>
- Issue template preference: <repo template | default open-issue template>
- Labels/milestones/assignees: <rules if known>

## Notes
- <short stable note>

## Last Updated
- <YYYY-MM-DD>
```

## What Not to Store

- Secrets, tokens, cookies, API keys, private credentials.
- Full Slack or email message bodies.
- Sensitive customer data.
- Large pasted documents.
- Temporary issue drafts or implementation plans.

## Update Rules

- Create the file on first run when the Markdown file does not exist and the user or repo provides enough stable environment facts.
- Update it after the user confirms new stable work-source information.
- Keep entries short and link-based.
- Run `scripts/ensure-memory-gitignore.sh` before every read/write path.
- Do not stage or commit `.memory/open-issue/work-context.md`.
