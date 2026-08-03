"""Controlled mapping from opportunity requirements to Google Cloud services."""

from __future__ import annotations

import json
from pathlib import Path

from schemas.opportunity import OpportunityProfile, SolutionComponent

CATALOG_PATH = Path(__file__).resolve().parents[1] / "config" / "service_catalog.json"


def map_requirements_to_gcp_services(profile: OpportunityProfile) -> list[SolutionComponent]:
    """Map requirements through a reviewed catalog instead of free-form invention."""
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    corpus = " ".join(
        [profile.use_case]
        + [item.requirement for item in profile.requirements if item.status == "confirmed"]
    ).lower()
    components: list[SolutionComponent] = []
    for capability, entry in catalog.items():
        if any(trigger.lower() in corpus for trigger in entry["triggers"]):
            components.append(
                SolutionComponent(
                    capability=capability.replace("_", " ").title(),
                    service=entry["service"],
                    rationale=entry["rationale"],
                    confidence="high"
                    if capability in {"managed_generative_ai", "analytics_data"}
                    else "medium",
                )
            )
    return components
