```markdown
# SignalForge-AI Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development conventions and workflows of the SignalForge-AI repository, a Python codebase built on Flask. You'll learn how to write code that fits the project's style, how to contribute using established commit and workflow patterns, and how to manage testing and deployment configurations effectively.

## Coding Conventions

- **Language:** Python
- **Framework:** Flask
- **File Naming:** Use `snake_case` for all file names.
  - Example: `mock_provider.py`, `test_decisions.py`
- **Import Style:** Use relative imports within the package.
  - Example:
    ```python
    from .mock_provider import MockProvider
    ```
- **Export Style:** Use named exports; avoid wildcard (`*`) exports.
  - Example:
    ```python
    def my_function():
        pass

    __all__ = ['my_function']
    ```
- **Commit Messages:** Follow [Conventional Commits](https://www.conventionalcommits.org/) with these prefixes:
  - `test:`, `fix:`, `refactor:`, `chore:`
  - Example: `fix: handle edge case in provider boundary check`

## Workflows

### Add or Update Tests for Feature or Bugfix
**Trigger:** When implementing a new feature, fixing a bug, or increasing test coverage.  
**Command:** `/add-test-coverage`

1. Identify the feature, bug, or boundary condition to cover.
2. Edit or create relevant test files in the `tests/` directory.
3. Commit with a message starting with `test:` describing the coverage.
   - Example: `test: add coverage for provider boundary case`

**Files Involved:**
- `tests/test_decisions.py`
- `tests/test_mock_provider.py`
- `tests/test_streamlit_app.py`
- `tests/test_mvp.py`
- `tests/test_packaging.py`
- `tests/test_provider_boundary.py`
- `tests/test_settings.py`

---

### Fix Feature or Bug Across Implementation and Tests
**Trigger:** When fixing a bug or improving a feature, ensuring both code and tests are updated.  
**Command:** `/fix-feature-bug`

1. Identify the bug or feature to fix.
2. Modify implementation files (e.g., in `providers/`, `app.py`, `tools/`).
3. Update or add related test files in `tests/`.
4. Commit with a message starting with `fix:`.
   - Example: `fix: correct mock provider return value in edge case`

**Files Involved:**
- `providers/mock_provider.py`
- `app.py`
- `tools/discovery.py`
- `tests/test_mvp.py`
- `tests/test_streamlit_app.py`

---

### Update Deployment and Ignore Configs
**Trigger:** When adjusting which files are included/excluded in deployment or packaging.  
**Command:** `/update-deployment-configs`

1. Edit `.dockerignore`, `.gcloudignore`, `.gitignore` as needed.
2. Update deployment scripts (e.g., `scripts/package_for_gcp.sh`, `scripts/deploy_cloud_run.sh`).
3. Commit with a message indicating packaging or deployment boundary changes.
   - Example: `chore: update .dockerignore to exclude test data files`

**Files Involved:**
- `.dockerignore`
- `.gcloudignore`
- `.gitignore`
- `scripts/package_for_gcp.sh`
- `scripts/deploy_cloud_run.sh`

---

## Testing Patterns

- **Framework:** Not explicitly detected, but tests are written in Python and follow the pattern `tests/test_*.py`.
- **Test File Naming:** All test files use `snake_case` and begin with `test_`.
  - Example: `test_streamlit_app.py`
- **Typical Test Structure:**
  ```python
  import unittest
  from ..providers.mock_provider import MockProvider

  class TestMockProvider(unittest.TestCase):
      def test_returns_expected(self):
          provider = MockProvider()
          self.assertEqual(provider.get(), "expected_value")
  ```
- **Commit Pattern:** Use `test:` prefix for all test-related commits.

## Commands

| Command                   | Purpose                                                        |
|---------------------------|----------------------------------------------------------------|
| /add-test-coverage        | Add or update tests for new features or bug fixes              |
| /fix-feature-bug          | Fix a feature or bug and update related tests                  |
| /update-deployment-configs| Update deployment scripts and ignore files for packaging/deploy |
```
