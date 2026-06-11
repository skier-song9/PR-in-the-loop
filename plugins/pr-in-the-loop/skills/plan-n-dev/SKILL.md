---
name: plan-n-dev
description: Use when a planning-pr PR plan document already exists and Codex needs to turn it into a concrete implementation spec, save that spec under .memory/specs, and start implementation immediately. Trigger automatically when a PR plan exists, no matching spec exists, and the user asks what to do next, says to proceed, or appears unsure how to move from PR planning into development. Do not use for issue discovery before an issue exists, writing human-reviewable PR plans, code review only, or PR publishing only.
---

# Plan N Dev

Turn an existing `planning-pr` PR plan into an uncommitted English implementation spec, then implement the spec without a separate approval gate.

## Rules

- Use automatically when a PR plan exists, no spec exists, and the user does not know what to do next.
- Start from one PR plan document, normally under `docs/pr-plans/`, or a plan path explicitly provided by the user.
- Always write the spec document in English, regardless of the user's language.
- Save specs under `.memory/specs/` and run `sh <plugin-root>/scripts/ensure-memory-gitignore.sh` from the target project root before writing there.
- Spec documents are not commit targets. Never stage or commit `.memory/specs/` unless the user explicitly overrides this rule.
- Do not ask for approval before implementation. After saving the spec, start development immediately.
- Ask the user only when ambiguity blocks correct execution, for example multiple plausible PR plans, contradictory requirements, missing source files, or a validation strategy that cannot be inferred from the repo.
- Keep implementation narrow and faithful to the PR plan. Do not bundle unrelated cleanup, hardening, docs, or behavior changes.

## Workflow

1. **Find the PR plan**
   - Inspect the user request, `docs/pr-plans/`, git status, and recent plan files.
   - If exactly one relevant plan is clear, use it without asking.
   - If several plans could apply, ask one focused question with 3 options and a recommendation.

2. **Orient the repository**
   - Read the selected PR plan completely.
   - Inspect the files, tests, docs, and local conventions named by the plan.
   - Prefer repo-local code and tests over assumptions.

3. **Write the implementation spec**
   - Create `.memory/specs/YYYY-MM-DD-<pr-plan-slug>-spec.md`.
   - Make the spec detailed enough for a fresh worker with no prior context.
   - Use exact paths, exact commands, expected failures/passes, and concrete test examples.
   - Remove vague text such as `TBD`, `TODO`, `fill in`, `add appropriate handling`, or `similar to previous task`.

4. **Self-review the spec**
   - Verify every PR plan requirement maps to a task.
   - Verify every task is testable and scoped to one coherent change.
   - Verify file names, function names, test names, and commands are consistent across tasks.
   - Fix gaps inline before implementation.

5. **Implement immediately**
   - Execute the tasks from the saved spec in order.
   - Prefer a fresh implementation worker for each task when worker dispatch is available. If not, execute inline while preserving the same gates.
   - Do not pause between tasks unless blocked, the spec is wrong, or all tasks are complete.

6. **Verify and finish**
   - Run scoped tests from the spec, then the smallest relevant broader test suite.
   - Run `git diff --check`.
   - Check `git status --short` and confirm `.memory/specs/` is not staged.
   - Report changed files, validation results, and any residual risk.

## Spec Format

Every generated spec must use this structure:

```markdown
# <Feature Name> Implementation Spec

**Source PR Plan:** `docs/pr-plans/<plan-file>.md`

**Goal:** <One sentence describing the concrete implementation outcome>

**Architecture:** <2-3 sentences describing the approach, boundaries, and data flow>

**Tech Stack:** <Languages, frameworks, test tools, and relevant local scripts>

**Commit Policy:** This spec is local memory and not a commit target. Commit only implementation and test files unless the user explicitly says otherwise.

---

## File Structure

- Create: `exact/path/to/new_file.ext` - <responsibility>
- Modify: `exact/path/to/existing_file.ext` - <responsibility>
- Test: `tests/exact/path/test_file.ext` - <behavior covered>

## Tasks

### Task N: <Component Name>

**Files:**
- Create: `exact/path/to/file.ext`
- Modify: `exact/path/to/existing.ext`
- Test: `tests/exact/path/test_file.ext`

- [ ] **Step 1: Write the failing test**

```<language>
<complete test code or exact patch-sized snippet>
```

- [ ] **Step 2: Run test to verify it fails**

Run: `<exact test command>`
Expected: FAIL because `<specific missing behavior>`

- [ ] **Step 3: Write minimal implementation**

```<language>
<complete implementation code or exact patch-sized snippet>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `<exact test command>`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add <implementation-and-test-files-only>
git commit -m "<type>: <specific change>"
```
```

## Execution Discipline

For each task:

- Give a fresh implementation worker the full task text, source PR plan path, spec path, target repo path, and any relevant local conventions. Do not make the worker rediscover the plan file when you can pass the exact task.
- Require test-first work: write the failing test, run it, implement the minimum code, then run it again.
- Require the worker to report `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`.
- Treat `NEEDS_CONTEXT` as a prompt-quality failure: provide the missing context and retry.
- Treat `BLOCKED` as a real blocker: provide better context, split the task, or ask the user only if no local evidence can resolve it.
- After implementation, perform spec compliance review before code quality review.
- Spec compliance review checks the actual code against the task line by line, looking for missing requirements, extra work, and misunderstood scope.
- Code quality review starts only after spec compliance passes. It checks maintainability, tests, file boundaries, naming, and consistency with repo patterns.
- Fix every critical or important review finding, then re-run the relevant review.
- Do not pause between tasks for progress confirmation. Continue until all tasks are complete or a genuine blocker remains.

## Explicit Model Calls

Do not describe strong subagent selection with implicit wording. When a strong implementation review, architecture review, or final whole-change review is needed, call the subagent with explicit settings:

```yaml
model: "gpt-5.5"
reasoning_effort: "xhigh"
service_tier: "priority"
```

Use these literal values in the subagent dispatch request so the runtime can select the intended model and effort.

## Quality Bar

Before finishing, verify:

- The selected PR plan is named in the spec.
- The spec is written in English.
- The spec lives under `.memory/specs/`.
- The spec is ignored by git and not staged.
- Every task has exact files, test-first steps, commands, expected outputs, and commit instructions.
- Implementation matches the PR plan and the saved spec.
- Scoped validation ran and results are reported.
- No unrelated changes were introduced.
