"""Offline provider used for local development and resilient demos."""
from __future__ import annotations

import re

from providers.base import OpportunityProvider
from schemas.opportunity import Evidence, OpportunityProfile, ParsedDocument, Requirement, Stakeholder


class MockOpportunityProvider(OpportunityProvider):
    """Return deterministic structured output without calling a model."""

    def extract_profile(self, documents: list[ParsedDocument]) -> OpportunityProfile:
        combined = "\n".join(document.text for document in documents)
        source = documents[0].name

        customer = _match(combined, r"Customer:\s*(.+)", "Meridian Hospitality Group")
        industry = _match(combined, r"Industry:\s*(.+)", "Hospitality")
        use_case = _match(
            combined,
            r"Use Case:\s*(.+)",
            "Internal enterprise AI assistant for knowledge and operational analytics",
        )
        users = _match_int(combined, r"([\d,]+)\s+(?:intended\s+)?users", 5000)
        timeline = _match_int(combined, r"(?:within|in)\s+(\d+)\s+weeks", 8)

        requirements = [
            _req("business", "Deploy an internal AI assistant for enterprise employees.", source, "internal AI assistant"),
            _req("users", f"Support approximately {users:,} intended users.", source, f"{users:,} users"),
            _req("data", "Use Google Drive documents and BigQuery datasets as knowledge sources.", source, "Google Drive and BigQuery"),
            _req("integration", "Operate within the customer's existing Google Cloud environment.", source, "existing cloud is Google Cloud"),
            _req("security", "Enforce role-based access control and audit logging.", source, "RBAC and audit logging"),
            _req("performance", "Target user response latency below three seconds.", source, "latency under 3 seconds"),
            _req("timeline", f"Deliver a pilot within {timeline} weeks.", source, f"pilot within {timeline} weeks"),
            Requirement(category="commercial", requirement="Confirm an approved pilot budget.", status="unknown"),
            Requirement(category="security", requirement="Confirm the formal data classification and PII scope.", status="unknown"),
            Requirement(category="performance", requirement="Confirm peak concurrency and request volume.", status="unknown"),
        ]

        return OpportunityProfile(
            customer_name=customer,
            industry=industry,
            use_case=use_case,
            geography=["Singapore", "Asia-Pacific"],
            intended_users=users,
            pilot_timeline_weeks=timeline,
            budget_status="unknown",
            data_sensitivity="unknown",
            requirements=requirements,
            stakeholders=[
                Stakeholder(role="Chief Information Officer", influence="high", priority="decision_maker"),
                Stakeholder(role="Head of IT", influence="high", priority="technical"),
                Stakeholder(role="Director of Operations", influence="medium", priority="champion"),
                Stakeholder(role="Finance Manager", influence="medium", priority="commercial"),
            ],
        )


def _match(text: str, pattern: str, default: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else default


def _match_int(text: str, pattern: str, default: int) -> int:
    match = re.search(pattern, text, re.IGNORECASE)
    return int(match.group(1).replace(",", "")) if match else default


def _req(category: str, requirement: str, source: str, quote: str) -> Requirement:
    return Requirement(
        category=category,
        requirement=requirement,
        status="confirmed",
        evidence=Evidence(source=source, quote=quote, confidence=0.96),
    )
