# Spec Template

```markdown
# [PR name] Implementation Spec
> For agentic workers: Never commit this file.

**Issue:** ISSUE_URL_OR_NUMBER
**PR Plan:** PLAN_PATH
**Goal:** ONE_SENTENCE_GOAL
**Architecture:** TWO_OR_THREE_SENTENCE_APPROACH
**Tech Stack:** STACK_AND_LIBRARIES

## Scope
- Included:
- Excluded:

## File Structure
- Modify `path/to/file.py`: file responsibility
- Create `path/to/file.py`: file responsibility

## Tasks
### Task 1: TASK_NAME
- Files:
- Test first:
- Expected failing command:
- Implementation steps:
- Passing command:
- Commit boundary:

## Self Review
- Spec coverage:
- Placeholder scan:
- Type and path consistency:
- Commit exclusion:
```

The generated spec must live under `docs/specs/` by default and must not be staged, tracked, or committed.
