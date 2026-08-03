"""Runtime configuration for SignalForge AI."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    """Application settings resolved entirely from environment variables."""

    app_mode: str = field(default_factory=lambda: os.getenv("APP_MODE", "mock").lower())
    project_id: str | None = field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    )
    location: str = field(
        default_factory=lambda: (
            os.getenv("GOOGLE_CLOUD_LOCATION") or os.getenv("GOOGLE_CLOUD_REGION") or "global"
        )
    )
    model_name: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    output_bucket: str | None = field(default_factory=lambda: os.getenv("OUTPUT_BUCKET"))

    def validate(self) -> None:
        """Raise a clear error when live mode lacks required cloud context."""
        if self.app_mode not in {"mock", "vertex"}:
            raise ValueError("APP_MODE must be either 'mock' or 'vertex'.")
        if self.app_mode == "vertex" and not self.project_id:
            raise RuntimeError("Vertex mode requires GOOGLE_CLOUD_PROJECT or GCLOUD_PROJECT.")


settings = Settings()
