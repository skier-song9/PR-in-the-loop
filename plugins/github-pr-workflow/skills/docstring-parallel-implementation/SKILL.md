---
name: docstring-parallel-implementation
description: Use when implementing a concrete spec from an approved PR plan with file-scoped delegation and subagents.
---

<!-- DocString Spec Excerpt: Add task-difficulty-based subagent model and reasoning effort selection while preserving DocString delegation and worker verification. -->

# DocString Parallel Implementation

Implement from a concrete spec by delegating responsibility into target files, then assigning fresh subagents.

**REQUIRED SUB-SKILL:** Use `superpowers:subagent-driven-development`.
**REQUIRED SUB-SKILL FOR WORKERS:** Use `superpowers:test-driven-development`.

## Process

1. Verify the concrete spec traces to a human-approved PR plan, then read the plan, spec, repo rules, and relevant current files. Stop if the trace or approval is missing.
2. Extract the write set: each changed file, its responsibility, tests, and dependencies.
3. Add a short file-level DocString or comment to each target file that states only that file's delegated responsibility from the spec.
4. Partition work by safe ownership:
   - parallel: disjoint source files with independent tests and no shared generated artifact
   - sequential: shared schema, migration, public contract, shared tests, or uncertain ownership
5. Before dispatch, classify each safe file group by task difficulty and choose the worker `model` and `reasoning_effort` from `Subagent Model And Effort Selection`.
6. Dispatch one fresh worker per safe file group. Set `model` and `reasoning_effort` when spawning each worker, and give each worker the selected model, selected reasoning effort, selection reason, file path, delegated DocString/comment, exact spec excerpt, tests to run, and no session history.
7. Do not dispatch a worker until its target files contain the delegated DocString Spec Excerpt from the spec.
8. After each worker, record Subagent verification: the worker read the DocString used, stayed inside its assigned file group, ran its exact tests, and reported status.
9. After each worker, run spec-compliance review before code-quality review. Fix and re-review until both reviewer subagents approve.
10. After all groups, run integration tests and a final review. Complete only when tests and reviews pass, or report a blocker.

This skill intentionally improves speed only where disjoint file ownership is proven. If parallel safety is not proven, fall back to the original sequential `superpowers:subagent-driven-development` flow.

## Subagent Model And Effort Selection

Set `model` and `reasoning_effort` when spawning each worker if the platform supports overrides. Spawned workers inherit the parent model and effort only when no explicit override is appropriate or when the platform lacks override support.

Choose the smallest capable model/effort pair for the delegated work:

- trivial or mechanical docs/test checks: `gpt-5.4-mini` + `low`
- simple bounded docs, tests, or code edits: `gpt-5.3-codex-spark` or `gpt-5.4-mini` + `medium`
- routine implementation with local tests: `gpt-5.3-codex` or `gpt-5.4` + `medium`
- complex integration, shared contracts, or reviewer work: `gpt-5.4` + `high`
- high-uncertainty architecture, security, or cross-system work: `gpt-5.5` + `high` or `xhigh`

Record the selected model, selected reasoning effort, and selection reason in the worker prompt. If a task is misclassified after reading the file group, prefer raising the model/effort before spawning over recovering from a weak worker result.

Subagents cannot reliably self-attest their actual runtime model or reasoning effort from inside their visible context. Verify model/effort selection from the spawn request, accepted tool arguments, and retained worker prompt metadata rather than from sub-agent self-report alone.

## DocString Rules

- Keep the delegation note short and specific.
- Use a heading or first sentence containing `DocString Spec Excerpt` when the file format allows it.
- Include only the exact responsibility, accepted inputs/outputs, invariants, and tests from the spec for that file.
- Do not paste the whole spec.
- Do not include secrets, user data, issue discussion, or unverifiable claims.
- Prefer module/class/function docstrings in Python; otherwise use the smallest local comment block that fits existing style.
- The file owner completes only the work described in that note.

## Subagent Verification

Each worker result must include:

- assigned file group
- selected model
- selected reasoning effort
- selection reason
- DocString used
- exact test command and result
- whether the worker changed files outside its ownership
- status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`

Use `references/worker-prompt-template.md` for worker dispatch.
