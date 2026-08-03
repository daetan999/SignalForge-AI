---
name: add-or-update-tests-for-feature-or-bugfix
description: Workflow command scaffold for add-or-update-tests-for-feature-or-bugfix in SignalForge-AI.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-or-update-tests-for-feature-or-bugfix

Use this workflow when working on **add-or-update-tests-for-feature-or-bugfix** in `SignalForge-AI`.

## Goal

Adds or updates test files to cover new features, bug fixes, or boundary conditions.

## Common Files

- `tests/test_decisions.py`
- `tests/test_mock_provider.py`
- `tests/test_streamlit_app.py`
- `tests/test_mvp.py`
- `tests/test_packaging.py`
- `tests/test_provider_boundary.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Identify the feature, bug, or boundary to cover.
- Edit or create relevant test files in the tests/ directory.
- Commit with a message starting with 'test:' describing the coverage.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.