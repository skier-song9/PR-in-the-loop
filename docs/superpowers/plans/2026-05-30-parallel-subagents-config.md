# Parallel Subagents Config Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `github-pr-workflow:docstring-parallel-implementation` or `superpowers:subagent-driven-development`. Steps use checkbox (`- [ ]`) syntax for tracking.
> This spec must be written in English.

> Supersession note (2026-05-31): The latest human requirement supersedes the earlier `max_threads = 12` guidance below. Current implementation target is `max_threads = 16`, `max_depth = 1`, explicit consent before global config edits, writable tests/fixtures must be owned by `ASSIGNED_PATHS`, worker summaries include `Changed files outside ownership: yes/no`, and workers must not spawn nested subagents.

**Issue:** https://github.com/skier-song9/PR-in-the-loop/issues/6
**PR Plan:** `docs/pr-plans/issue-6-parallel-subagents-config.md`
**Goal:** Strengthen `docstring-parallel-implementation` parallel sub-agent instructions and document the recommended Codex `[agents]` config for higher local sub-agent concurrency.
**Architecture:** This is a documentation-driven plugin behavior change. The skill file defines the runtime policy for safe parallel worker spawning; the worker prompt template defines required worker return fields; `INSTALL.md` documents the optional user config. `tests/test_skill_requirements.py` locks the policy and config guidance with string-based regression tests.
**Tech Stack:** Markdown skill instructions, Python standard-library `unittest`, existing plugin validation scripts.

---

## Scope
- Included:
  - Add explicit parallel subagent spawn policy to `docstring-parallel-implementation`.
  - Require one sub-agent per independent task and prevent multiple write-capable agents from editing the same files.
  - Require read-only explorer agents for investigation tasks.
  - Require waiting for all subagents before consolidation.
  - Require structured summaries with findings, changed files, risks, and next actions.
  - Add worker prompt return fields for findings, changed files, risks, and next actions.
  - Add `INSTALL.md` guidance for `[agents] max_threads = 12` and `max_depth = 1` in Codex config.
  - Add tests for the new skill and install documentation requirements.
- Excluded:
  - Changing the Codex runtime scheduler or `spawn_agent` tool implementation.
  - Editing the user's local `~/.codex/config.toml`.
  - Changing `multi-review-html`.
  - Changing plugin identifier/name.
  - Changing the existing model/effort selection policy from Issue #5.
  - Committing generated plan/spec documents.

## File Structure
- Modify `plugins/github-pr-workflow/skills/docstring-parallel-implementation/SKILL.md`: add parallel subagent spawn policy and structured summary requirements while preserving existing DocString delegation and model/effort selection policy.
- Modify `plugins/github-pr-workflow/skills/docstring-parallel-implementation/references/worker-prompt-template.md`: require worker returns for findings, changed files, risks, and next actions.
- Modify `INSTALL.md`: document optional Codex `config.toml` `[agents]` settings and instruct users/agents to add them only when missing.
- Modify `tests/test_skill_requirements.py`: add tests that lock the skill policy, worker prompt return fields, and install config guidance.

## Tasks

### Task 1: Add failing tests for Issue #6 policy and install guidance

**Files:**
- Modify: `tests/test_skill_requirements.py`

- [ ] **Step 1: Add an install reader helper**

Add this helper after `read_reference`.

```python
def read_root_file(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")
```

- [ ] **Step 2: Add a focused test for parallel subagent policy**

Add this method after `test_docstring_parallel_requires_model_effort_selection_policy`.

```python
    def test_docstring_parallel_requires_parallel_spawn_policy(self) -> None:
        text = read_skill("docstring-parallel-implementation")
        prompt = read_reference("docstring-parallel-implementation", "worker-prompt-template.md")

        self.assertIn("Parallel Subagent Spawn Policy", text)
        self.assertIn("Use parallel subagents for independent work", text)
        self.assertIn("Spawn one subagent per task", text)
        self.assertIn("Do not let multiple write-capable agents edit the same files", text)
        self.assertIn("Use read-only explorer agents for investigation", text)
        self.assertIn("Wait for all subagents, then consolidate the results", text)
        self.assertIn("Return a structured summary with findings, changed files, risks, and next actions", text)
        self.assertIn("findings", prompt)
        self.assertIn("changed files", prompt)
        self.assertIn("risks", prompt)
        self.assertIn("next actions", prompt)
```

- [ ] **Step 3: Add a focused test for install config guidance**

Add this method after the new parallel policy test.

```python
    def test_install_documents_agents_parallel_config(self) -> None:
        text = read_root_file("INSTALL.md")

        self.assertIn("[agents]", text)
        self.assertIn("max_threads = 12", text)
        self.assertIn("max_depth = 1", text)
        self.assertIn("~/.codex/config.toml", text)
        self.assertIn("only if the block is missing", text)
```

- [ ] **Step 4: Run the new tests and verify RED**

Run:

```bash
python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_docstring_parallel_requires_parallel_spawn_policy tests.test_skill_requirements.SkillRequirementTests.test_install_documents_agents_parallel_config
```

Expected: `FAIL` because the new policy and install guidance do not exist yet.

### Task 2: Add parallel subagent spawn policy to the skill

**Files:**
- Modify: `plugins/github-pr-workflow/skills/docstring-parallel-implementation/SKILL.md`

- [ ] **Step 1: Add the file-level DocString Spec Excerpt**

Replace the current top HTML comment with this exact comment.

```markdown
<!-- DocString Spec Excerpt: Add parallel subagent spawn policy and structured worker summaries while preserving DocString delegation and model/effort selection. -->
```

- [ ] **Step 2: Insert policy section before `## Subagent Model And Effort Selection`**

Add this exact section after the paragraph beginning `This skill intentionally improves speed`.

```markdown
## Parallel Subagent Spawn Policy

Use parallel subagents for independent work only after safe ownership is proven.

- Use parallel subagents for independent work.
- Spawn one subagent per task.
- Do not let multiple write-capable agents edit the same files.
- Use read-only explorer agents for investigation.
- Wait for all subagents, then consolidate the results.
- Return a structured summary with findings, changed files, risks, and next actions.

Investigation-only tasks must use read-only explorer agents. Implementation workers are write-capable only for their assigned file group and directly required tests. If two workers need the same file, same generated artifact, shared schema, public contract, or shared test fixture, keep that work sequential.
```

- [ ] **Step 3: Update final process consolidation wording**

In the final process step, append this sentence.

```markdown
The final consolidation must include findings, changed files, risks, and next actions.
```

- [ ] **Step 4: Update subagent verification bullets**

In `## Subagent Verification`, add these bullets before `status`.

```markdown
- findings
- changed files
- risks
- next actions
```

### Task 3: Add structured return fields to the worker prompt

**Files:**
- Modify: `plugins/github-pr-workflow/skills/docstring-parallel-implementation/references/worker-prompt-template.md`

- [ ] **Step 1: Update the prompt DocString Spec Excerpt**

Replace the existing top HTML comment with this exact comment.

```markdown
<!-- DocString Spec Excerpt: Require structured worker summaries with findings, changed files, risks, and next actions for safe parallel consolidation. -->
```

- [ ] **Step 2: Add read-only investigation and ownership rules**

Add these bullets under `Rules:`.

```markdown
- Treat investigation-only assignments as read-only explorer work.
- Do not edit files outside the assigned file group.
- If another write-capable agent would need the same file, stop and report `BLOCKED`.
```

- [ ] **Step 3: Update return fields**

Replace `- Files changed` and `- Concerns` in the return list with these exact fields while keeping the existing selected model, DocString, tests, and status fields.

```markdown
- Findings
- Changed files
- Risks
- Next actions
```

### Task 4: Document Codex agents config in install instructions

**Files:**
- Modify: `INSTALL.md`

- [ ] **Step 1: Add agents config instruction to the AI-agent install prompt**

In the `Give This To Your AI Agent` code block, add this step after plugin installation and before starting a new Codex thread.

```text
5. Ensure ~/.codex/config.toml contains this block, adding it only if the block is missing:
   [agents]
   max_threads = 12
   max_depth = 1
6. Tell me to start a new Codex thread after installation and invoke $github-pr-workflow:github-dev-workflow.
```

Renumber the existing start-thread step from `5` to `6`.

- [ ] **Step 2: Add a manual config section after the install command**

Add this section after `codex plugin add github-pr-workflow@pr-in-the-loop` in `Manual Install`.

```markdown
## Optional Parallel Subagent Config

For workflows that spawn parallel subagents, ensure `~/.codex/config.toml` contains this block. Add it only if the block is missing:

```toml
[agents]
max_threads = 12
max_depth = 1
```
```

- [ ] **Step 3: Add the same reminder to update instructions**

After the `Update Existing Install` command block, add this sentence.

```markdown
After updating, keep the optional `[agents]` block in `~/.codex/config.toml`; add it only if the block is missing.
```

### Task 5: Validate and review

**Files:**
- Read: `tests/test_skill_requirements.py`
- Read: `plugins/github-pr-workflow/skills/docstring-parallel-implementation/SKILL.md`
- Read: `plugins/github-pr-workflow/skills/docstring-parallel-implementation/references/worker-prompt-template.md`
- Read: `INSTALL.md`

- [ ] **Step 1: Run focused tests**

Run:

```bash
python3 -m unittest tests.test_skill_requirements.SkillRequirementTests.test_docstring_parallel_requires_parallel_spawn_policy tests.test_skill_requirements.SkillRequirementTests.test_install_documents_agents_parallel_config
```

Expected: `OK`.

- [ ] **Step 2: Run all tests**

Run:

```bash
python3 -m unittest discover -s tests
```

Expected: all tests pass. The expected count after adding two tests is `Ran 11 tests` and `OK`.

- [ ] **Step 3: Run repository plugin validation**

Run:

```bash
python3 scripts/check_plugins.py
```

Expected:

```text
OK: 1 plugins checked
```

- [ ] **Step 4: Run plugin validator**

Run:

```bash
/tmp/codex-plugin-validate-venv/bin/python /Users/song9/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py /Users/song9/Documents/projects/PR-in-the-loop/plugins/github-pr-workflow
```

Expected:

```text
Plugin validation passed: /Users/song9/Documents/projects/PR-in-the-loop/plugins/github-pr-workflow
```

- [ ] **Step 5: Run skill quick validation for all skills**

Run:

```bash
for d in plugins/github-pr-workflow/skills/*; do /tmp/codex-plugin-validate-venv/bin/python /Users/song9/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$d" >/dev/null || exit 1; done; echo "Skill validation passed: 6 skills"
```

Expected:

```text
Skill validation passed: 6 skills
```

- [ ] **Step 6: Inspect implementation diff**

Run:

```bash
git diff -- tests/test_skill_requirements.py plugins/github-pr-workflow/skills/docstring-parallel-implementation/SKILL.md plugins/github-pr-workflow/skills/docstring-parallel-implementation/references/worker-prompt-template.md INSTALL.md
```

Expected:
- tests lock parallel spawn policy and install config guidance.
- skill text contains `Parallel Subagent Spawn Policy`.
- worker prompt return fields include findings, changed files, risks, and next actions.
- `INSTALL.md` documents `~/.codex/config.toml` with `[agents]`, `max_threads = 12`, and `max_depth = 1`.

- [ ] **Step 7: Keep generated docs uncommitted**

Run:

```bash
git status --short
```

Expected: generated `docs/` plan/spec files may remain untracked; do not stage them for this implementation commit.

## Self Review
- Spec coverage: Covers all Issue #6 requirements: parallel subagent policy, one agent per task, write ownership, read-only explorers, wait-all consolidation, structured summaries, install config, and tests.
- Placeholder scan: No placeholders remain. Each task includes exact file paths, exact text to add, commands, and expected outputs.
- Type and path consistency: File paths match the current repository. The test helper names match the existing `tests/test_skill_requirements.py` pattern.
