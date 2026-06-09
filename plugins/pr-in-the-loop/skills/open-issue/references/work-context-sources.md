# Work Context Sources

Use these sources only when available and relevant. Prefer direct links and exact titles over paraphrased memories.

Start with `.memory/open-issue/work-context.md` if it exists. That file is the skill's platform-neutral memory for source-of-truth links, preferred trackers, communication channels, and document locations.

## Local Project

- Git: branch, remotes, dirty files, recent commits, tags.
- Repo docs: README, docs, architecture notes, changelogs, specs.
- Code signals: TODO/FIXME, failing tests, CI config, issue IDs in comments.
- Package/project files: dependencies, scripts, test commands, app entrypoints.

## GitHub

- Existing open issues and PRs for duplicates or active work.
- Closed issues/PRs for prior decisions and regression context.
- GitHub Projects or milestones for priority and ownership.
- Checks, Actions logs, releases, discussions when the problem is CI, release, or support related.

## Slack

- Threads with explicit decisions, blockers, bug reports, screenshots, or user reports.
- Prefer channel/thread permalink as reference.
- Extract only work-relevant facts: who reported, observed behavior, expected behavior, deadline, owner.

## Linear or Jira

- Tickets, labels, priority, assignee, status, parent epic.
- Link the source ticket in `## Reference`.
- If the tracker ticket already has a precise scope, GitHub Issue should mirror the engineering implementation boundary, not duplicate unrelated product notes.

## Notion

- PRDs, meeting notes, project briefs, retrospectives, design docs.
- Use Notion as source of context and acceptance criteria, but convert prose into executable GitHub tasks.
- Link the page in `## Reference` if it informed the issue.

## Google Workspace

- Docs: specs, meeting notes, design drafts.
- Sheets: bug lists, prioritization matrices, migration inventories.
- Drive files: screenshots, recordings, exported PDFs.
- Calendar/Gmail only when the user explicitly points to them or they are part of the work context.

## Other Engineering Tools

- CI/CD: GitHub Actions, Vercel, Netlify, Render, Fly.io, CircleCI.
- Observability: Sentry, Datadog, Grafana, CloudWatch, Logtail.
- Product/support: Intercom, Zendesk, customer feedback tools.

When a source requires authentication and no connector/session is available, ask for a link or continue with available evidence and mark the missing source as a blocker only if it prevents a concrete issue.
