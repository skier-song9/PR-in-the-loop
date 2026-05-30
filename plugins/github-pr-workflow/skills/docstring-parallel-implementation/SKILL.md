---
name: docstring-parallel-implementation
description: Use when implementing a concrete spec from an approved PR plan with file-scoped delegation and subagents.
---

<!-- DocString Spec Excerpt: Add parallel subagent spawn policy and structured worker summaries while preserving DocString delegation and model/effort selection. -->

# DocString Parallel Implementation

Implement from a concrete spec by delegating responsibility into target files, then assigning fresh subagents.

**REQUIRED SUB-SKILL:** Use `superpowers:subagent-driven-development` for task/review discipline; the parallel policy in this skill supersedes the sub-skill's sequential default only for proven disjoint safe file groups.
**REQUIRED SUB-SKILL FOR IMPLEMENTATION WORKERS:** Use `superpowers:test-driven-development`. Investigation-only workers stay read-only and do not use test-driven development.

## Process

1. Verify the concrete spec traces to a human-approved PR plan, then read the plan, spec, repo rules, and relevant current files. Stop if the trace or approval is missing.
2. Extract the write set: each changed source file, writable test, writable fixture, generated artifact, its responsibility, tests, and dependencies.
3. Add a short file-level DocString or comment to each target file that states only that file's delegated responsibility from the spec.
4. Partition work by safe ownership:
   - parallel: disjoint source, test, and fixture files with independent tests and no shared generated artifact
   - sequential: shared schema, migration, public contract, shared tests, or uncertain ownership
5. Before dispatch, create an ownership ledger that maps each worker to exactly one safe file group and confirms no writable path appears in more than one write-capable group. Then classify each safe file group by task difficulty and choose the worker `model` and `reasoning_effort` from `Subagent Model And Effort Selection`.
6. Dispatch one fresh worker per safe file group, treating each safe file group as one subagent task. Set `model` and `reasoning_effort` when spawning each worker, and give each worker the selected model, selected reasoning effort, selection reason, full assigned file group as `ASSIGNED_PATHS`, delegated DocString/comment, exact spec excerpt, tests to run, and no session history.
7. Do not dispatch a worker until its target files contain the delegated DocString Spec Excerpt from the spec.
8. After each worker, record Subagent verification: the worker read the DocString used, stayed inside its assigned file group, reported whether it changed files outside ownership, ran its exact tests, and reported status. Parent verification must compare the actual changed paths against the ownership ledger and the worker's assigned file group. Do not rely only on the worker's self-report.
9. After each worker, run spec-compliance review before code-quality review. Fix and re-review until both reviewer subagents approve.
10. After all groups, run integration tests and a final review. The final consolidation must include findings, changed files, risks, and next actions. Complete only when tests and reviews pass, or report a blocker.

This skill intentionally improves speed only where disjoint file ownership is proven. If parallel safety is not proven, fall back to the original sequential `superpowers:subagent-driven-development` flow.

## Parallel Subagent Spawn Policy

Use parallel subagents for independent work only after safe ownership is proven.

- Use parallel subagents for independent work.
- Spawn one subagent per task; in this skill, a task maps to one safe file group.
- Do not let multiple write-capable agents edit the same files.
- Use read-only explorer agents for investigation.
- Wait for all subagents, then consolidate the results.
- Return a structured summary with findings, changed files, risks, and next actions.

Read-only explorer dispatch is parent-controlled. Parent agents may use read-only explorer agents for investigation-only tasks, but implementation workers must not spawn nested subagents. If a worker receives an investigation-only assignment, it must act read-only itself and report findings.

Writable tests and fixtures must be explicitly included in the safe file group before dispatch. This is the most efficient ownership rule because it avoids locks and merge arbitration: a worker can edit only paths in its assigned group, and any shared test, shared fixture, same generated artifact, shared schema, or public contract forces sequential work.

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
- changed files outside ownership: yes/no
- findings
- changed files
- risks
- next actions
- status: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, or `BLOCKED`

Use `references/worker-prompt-template.md` for worker dispatch.
