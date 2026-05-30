# Install PR In The Loop

<!-- DocString Spec Excerpt: Document optional Codex agents thread settings for parallel subagent workflows with explicit user consent before global config edits. -->

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
   codex plugin add pr-in-the-loop@pr-in-the-loop
5. If this install will use parallel subagent workflows, explain that the optional global Codex config is:
   [agents]
   max_threads = 16
   max_depth = 1
   This changes `~/.codex/config.toml`. Ask whether I agree before changing `~/.codex/config.toml`. Do not edit it unless I agree.
   If I agree, preserve existing keys and comments, create the full `[agents]` block only if the block is missing, do not append a duplicate `[agents]` table, and record previous values before editing.
6. Tell me to start a new Codex thread after installation and invoke $pr-in-the-loop:github-dev-workflow.

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
codex plugin add pr-in-the-loop@pr-in-the-loop
```

## Optional Parallel Subagent Config

For workflows that spawn parallel subagents, these optional agent settings can be added to the user's global `~/.codex/config.toml`:

```toml
[agents]
max_threads = 16
max_depth = 1
```

These values change global Codex behavior. Ask for explicit consent before changing global Codex settings. Do not edit `~/.codex/config.toml` unless the user agrees.

After the user agrees, apply this rule: If `~/.codex/config.toml` already has an `[agents]` section, add or update `max_threads = 16` and `max_depth = 1` inside that section while preserving existing keys and comments. Create the full block only if the block is missing. Record any previous values so the user can roll back.

Start a new Codex thread and invoke `$pr-in-the-loop:github-dev-workflow`.

## Update Existing Install

```bash
cd ~/Documents/projects/PR-in-the-loop
git pull
python3 scripts/check_plugins.py
codex plugin add pr-in-the-loop@pr-in-the-loop
```

After updating, review Optional Parallel Subagent Config. Ask before changing global Codex settings. If the user agrees and `~/.codex/config.toml` already has an `[agents]` section, add or update the keys there while preserving existing keys and comments; create the full block only if the block is missing.

Start a new Codex thread after updating and invoke `$pr-in-the-loop:github-dev-workflow`.

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

- `pr-in-the-loop`: Issue-to-PR planning, spec generation, DocString subagent implementation, HTML review, and PR message drafting.
