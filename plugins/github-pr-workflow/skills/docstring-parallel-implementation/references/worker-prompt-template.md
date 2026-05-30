# Worker Prompt Template

```markdown
You are a fresh implementation worker.

Repo: REPO_PATH
File group: ASSIGNED_PATHS
Issue/PR plan: PLAN_PATH_OR_URL
Spec excerpt:
RELEVANT_TASK_AND_FILE_RESPONSIBILITY

DocString used:
PASTE_THE_DOCSTRING_SPEC_EXCERPT_FOUND_IN_THE_ASSIGNED_FILE

Required skills:
- Use `superpowers:test-driven-development`.

Rules:
- Edit only the assigned file group and directly required tests.
- Follow the delegated DocString/comment already placed in the file.
- Ask for context if the assignment conflicts with current code.
- Run the exact tests below.

Tests:
- EXACT_TEST_COMMAND

Return:
- Status: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED
- Files changed
- DocString used
- Tests run and results
- Concerns
```
