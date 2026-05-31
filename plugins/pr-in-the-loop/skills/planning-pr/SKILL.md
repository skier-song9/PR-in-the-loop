---
name: planning-pr
description: Use when an approved PR plan must become a concrete implementation spec or plan.
---

# Planning PR

Turn an approved PR plan into a concrete implementation spec while preserving Superpowers planning.

**REQUIRED SUB-SKILL:** Use `superpowers:writing-plans`.

## Language Rule

Always write the generated spec in English, even when the PR plan, Issue, conversation, or repository docs use another language. Preserve code symbols, file paths, commands, errors, and quoted source text exactly.

## Preconditions

- A PR plan markdown file exists under `docs/`.
- The human has explicitly approved that PR plan.
- The target PR boundary is known when one Issue has multiple PRs.

If any precondition is missing, stop and request the missing artifact or approval.

## Process

1. Locate the PR plan from the user path, linked Issue, current branch, or recent `docs/` PR plan files. Ask if multiple plausible plans exist.
2. Read repo rules and the relevant code before writing the spec.
3. Use `superpowers:writing-plans` standards: exact files, concrete tasks, TDD steps, commands, expected outputs, and self-review. The spec content must be English.
4. Save the spec near the PR plan or under `docs/superpowers/plans/` when repo convention points there.
5. Run a placeholder scan and self-review for scope drift.
6. Verify the spec is not staged. Do not commit it.

## Overrides From User Workflow

- Do not ask the human to review the spec.
- Do not include the spec in a GitHub commit.
- Do not let the spec expand beyond the approved PR plan.
- Implementation permission comes from the human-approved PR plan plus this generated spec, not from separate human spec approval.

Use `references/spec-template.md` for the minimum expected shape.
