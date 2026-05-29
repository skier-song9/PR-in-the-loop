# Install PR In The Loop

This guide is written for Codex users and for AI agents asked to install this repository.

## Give This To Your AI Agent

```text
Install Codex plugins from https://github.com/skier-song9/PR-in-the-loop.

Steps:
1. Clone the repo to ~/Documents/projects/PR-in-the-loop if it is not already present.
2. Run python3 scripts/check_plugins.py from the repo root.
3. Register the repo as a Codex marketplace:
   codex plugin marketplace add "$(pwd)"
4. Install:
   codex plugin add github-pr-workflow@pr-in-the-loop
5. Tell me to start a new Codex thread after installation and invoke $github-pr-workflow:github-dev-workflow.

Do not copy plugin files into ~/.codex manually. Use the marketplace commands.
```

## Manual Install

Clone:

```bash
mkdir -p ~/Documents/projects
git clone https://github.com/skier-song9/PR-in-the-loop.git ~/Documents/projects/PR-in-the-loop
cd ~/Documents/projects/PR-in-the-loop
```

Validate repo structure:

```bash
python3 scripts/check_plugins.py
```

Register marketplace:

```bash
codex plugin marketplace add "$(pwd)"
```

Install the main workflow plugin:

```bash
codex plugin add github-pr-workflow@pr-in-the-loop
```

Start a new Codex thread and invoke `$github-pr-workflow:github-dev-workflow`.

## Update Existing Install

```bash
cd ~/Documents/projects/PR-in-the-loop
git pull
python3 scripts/check_plugins.py
codex plugin add github-pr-workflow@pr-in-the-loop
```

Start a new Codex thread after updating and invoke `$github-pr-workflow:github-dev-workflow`.

## Verify

Check marketplace file:

```bash
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
```

Check plugin layout:

```bash
python3 scripts/check_plugins.py
```

Expected output:

```text
OK: 1 plugins checked
```

## Troubleshooting

### `codex: command not found`

Install or open Codex first. This repository only supplies plugin marketplace files and plugin content.

### Plugin installed but skills do not appear

Start a new Codex thread. Skills are loaded at thread start.

### Marketplace path wrong

Run marketplace registration from the repo root:

```bash
cd ~/Documents/projects/PR-in-the-loop
codex plugin marketplace add "$(pwd)"
```

### Clone already exists

Use the existing clone:

```bash
cd ~/Documents/projects/PR-in-the-loop
git pull
```

## What Gets Installed

- `github-pr-workflow`: Issue-to-PR planning, spec generation, DocString subagent implementation, HTML review, and PR message drafting.
