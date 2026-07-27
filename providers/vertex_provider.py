"""Live Gemini provider for Google Cloud sandbox execution."""
from __future__ import annotations

import json

from config.settings import Settings
from providers.base import OpportunityProvider
from schemas.opportunity import OpportunityProfile, ParsedDocument


class VertexOpportunityProvider(OpportunityProvider):
    """Use the Google Gen AI SDK with Application Default Credentials."""

    def __init__(self, settings: Settings) -> None:
        settings.validate()
        if settings.app_mode != "vertex":
            raise ValueError("VertexOpportunityProvider requires APP_MODE=vertex.")
        self.settings = settings

    def extract_profile(self, documents: list[ParsedDocument]) -> OpportunityProfile:
        """Extract a validated profile using structured JSON output from Gemini."""
        from google import genai
        from google.genai import types

        context = "\n\n".join(
            f"DOCUMENT: {document.name}\n{document.text}" for document in documents
        )
        prompt = f"""
You are an enterprise AI opportunity qualification agent.
Extract only facts supported by the supplied documents. Mark missing facts as
unknown. Do not invent customer claims, services, numbers, or stakeholders.
Return a JSON object matching the supplied schema.

CUSTOMER MATERIALS
{context}
""".strip()

        client = genai.Client(
            vertexai=True,
            project=self.settings.project_id,
            location=self.settings.location,
        )
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
                raise RuntimeError("Gemini returned an empty response.")
            return OpportunityProfile.model_validate(json.loads(response.text))
        finally:
            client.close()
