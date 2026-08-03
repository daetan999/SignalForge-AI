---
name: fix-feature-or-bug-across-implementation-and-tests
description: Workflow command scaffold for fix-feature-or-bug-across-implementation-and-tests in SignalForge-AI.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /fix-feature-or-bug-across-implementation-and-tests

Use this workflow when working on **fix-feature-or-bug-across-implementation-and-tests** in `SignalForge-AI`.

## Goal

Fixes a bug or improves a feature, updating both implementation and related tests.

## Common Files

- `providers/mock_provider.py`
- `app.py`
- `tools/discovery.py`
- `tests/test_mvp.py`
- `tests/test_streamlit_app.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Identify the bug or feature to fix.
- Modify implementation files (e.g., in providers/, app.py, tools/).
- Update or add related test files in tests/.
- Commit with a message starting with 'fix:'.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.