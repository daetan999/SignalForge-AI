"""Live Gemini provider for Google Cloud sandbox execution."""
from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from config.settings import Settings
from providers.base import OpportunityProvider
from schemas.opportunity import OpportunityProfile, ParsedDocument


class VertexOpportunityProvider(OpportunityProvider):
    """Use the Google Gen AI SDK with Application Default Credentials."""

    def __init__(
        self,
        settings: Settings,
        client_factory: Callable[..., Any] | None = None,
    ) -> None:
        settings.validate()
        if settings.app_mode != "vertex":
            raise ValueError("VertexOpportunityProvider requires APP_MODE=vertex.")
        self.settings = settings
        self.client_factory = client_factory or _create_client

    def extract_profile(self, documents: list[ParsedDocument]) -> OpportunityProfile:
        """Extract a validated profile using structured JSON output from Gemini."""
        from google.genai import types

        context = "\n\n".join(
            f"DOCUMENT: {document.name}\n{document.text}" for document in documents
        )
        prompt = f"""
You are an enterprise AI opportunity qualification agent.
Extract only facts supported by the supplied documents. Mark missing facts as
unknown. Do not invent customer claims, services, numbers, or stakeholders.
Every confirmed requirement must include the source document name, a short
supporting quote copied from that document, and a confidence score.
Return a JSON object matching the supplied schema.

CUSTOMER MATERIALS
{context}
""".strip()

        client = self.client_factory(
            vertexai=True,
            project=self.settings.project_id,
            location=self.settings.location,
        )
        try:
            last_error: Exception | None = None
            for _ in range(2):
                try:
                    response = client.models.generate_content(
                        model=self.settings.model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.1,
                            response_mime_type="application/json",
                            response_json_schema=OpportunityProfile.model_json_schema(),
                        ),
                    )
                    if not response.text:
                        raise ValueError("Gemini returned an empty response.")
                    return OpportunityProfile.model_validate(json.loads(response.text))
                except (json.JSONDecodeError, ValueError) as exc:
                    last_error = exc
            raise RuntimeError(
                "Gemini did not return a valid opportunity profile after two attempts."
            ) from last_error
        finally:
            client.close()


def _create_client(**kwargs: Any) -> Any:
    """Create the live SDK client lazily so mock mode needs no cloud setup."""
    from google import genai

    return genai.Client(**kwargs)
