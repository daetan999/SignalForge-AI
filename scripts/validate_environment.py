"""Fast event-day checks before launching the full application."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from config.settings import settings  # noqa: E402

REQUIRED_IMPORTS = ["streamlit", "pydantic", "docx", "google.genai"]


def main() -> int:
    print(f"Python: {sys.version.split()[0]}")
    print(f"APP_MODE: {settings.app_mode}")
    print(f"GOOGLE_CLOUD_PROJECT: {settings.project_id or 'not set'}")
    print(f"GOOGLE_CLOUD_LOCATION: {settings.location}")
    print(f"GEMINI_MODEL: {settings.model_name}")

    failures: list[str] = []
    for module in REQUIRED_IMPORTS:
        try:
            importlib.import_module(module)
            print(f"OK import: {module}")
        except Exception as exc:
            failures.append(f"{module}: {exc}")

    if settings.app_mode == "vertex" and not settings.project_id:
        failures.append("Vertex mode requires GOOGLE_CLOUD_PROJECT.")

    if failures:
        print("\nEnvironment validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("\nEnvironment validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
