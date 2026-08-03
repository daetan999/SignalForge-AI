"""Document-grounded offline provider for local development and resilient demos."""
from __future__ import annotations

import re
from collections.abc import Callable

from providers.base import OpportunityProvider
from schemas.opportunity import Evidence, OpportunityProfile, ParsedDocument, Requirement, Stakeholder


class MockOpportunityProvider(OpportunityProvider):
    """Extract a conservative profile without calling a model.

    The mock provider is intentionally less capable than Gemini, but it follows
    the same grounding contract: confirmed facts must be present in the source
    documents and must carry evidence.
    """

    def extract_profile(self, documents: list[ParsedDocument]) -> OpportunityProfile:
        if not documents:
            raise ValueError("At least one parsed document is required.")

        combined = "\n".join(document.text for document in documents)
        customer = _match(combined, r"^Customer:\s*(.+)$", "Unknown customer")
        industry = _match(combined, r"^Industry:\s*(.+)$", "Unknown")
        use_case = _match(combined, r"^Use Case:\s*(.+)$", "Use case not stated")
        users = _match_int(combined, r"([\d,]+)\s+(?:intended\s+)?users")
        timeline = _match_int(combined, r"(?:within|in)\s+(\d+)\s+weeks")

        requirements = _extract_requirements(documents, use_case, users, timeline)
        budget_status = _budget_status(combined)
        data_sensitivity = _data_sensitivity(combined)
        requirements.extend(_unknown_requirements(requirements, budget_status, data_sensitivity))

        return OpportunityProfile(
            customer_name=customer,
            industry=industry,
            use_case=use_case,
            geography=_extract_geography(combined),
            intended_users=users,
            pilot_timeline_weeks=timeline,
            budget_status=budget_status,
            data_sensitivity=data_sensitivity,
            requirements=requirements,
            stakeholders=_extract_stakeholders(combined),
        )


def _match(text: str, pattern: str, default: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else default


def _match_int(text: str, pattern: str) -> int | None:
    match = re.search(pattern, text, re.IGNORECASE)
    return int(match.group(1).replace(",", "")) if match else None


def _req(category: str, requirement: str, source: str, quote: str) -> Requirement:
    return Requirement(
        category=category,
        requirement=requirement,
        status="confirmed",
        evidence=Evidence(source=source, quote=quote, confidence=0.96),
    )


def _find_evidence(
    documents: list[ParsedDocument],
    predicate: Callable[[str], bool],
) -> tuple[str, str] | None:
    for document in documents:
        for raw_line in document.text.splitlines():
            line = raw_line.strip(" -\t")
            if line and predicate(line.lower()):
                return document.name, line
    return None


def _extract_requirements(
    documents: list[ParsedDocument],
    use_case: str,
    users: int | None,
    timeline: int | None,
) -> list[Requirement]:
    requirements: list[Requirement] = []

    business = _find_evidence(documents, lambda line: line.startswith("use case:"))
    if business:
        requirements.append(_req("business", use_case, *business))

    user_evidence = _find_evidence(documents, lambda line: bool(re.search(r"\b[\d,]+\s+(?:intended\s+)?users\b", line)))
    if users is not None and user_evidence:
        requirements.append(_req("users", f"Support approximately {users:,} intended users.", *user_evidence))

    patterns: list[tuple[str, str, tuple[str, ...]]] = [
        ("data", "Use the documented enterprise data sources.", ("bigquery", "google drive", "sharepoint", "data source")),
        ("integration", "Integrate with the documented existing environment.", ("existing cloud", "integration", "identity provider")),
        ("security", "Enforce the documented identity and audit controls.", ("role-based", "rbac", "audit logging", "least privilege")),
        ("performance", "Meet the documented response-latency target.", ("latency", "response time", "seconds")),
    ]
    for category, summary, keywords in patterns:
        evidence = _find_evidence(documents, lambda line, keys=keywords: any(key in line for key in keys))
        if evidence:
            requirements.append(_req(category, summary, *evidence))

    timeline_evidence = _find_evidence(
        documents,
        lambda line: bool(re.search(r"(?:within|in)\s+\d+\s+weeks", line)),
    )
    if timeline is not None and timeline_evidence:
        requirements.append(_req("timeline", f"Deliver the pilot within {timeline} weeks.", *timeline_evidence))

    approved_budget = _find_evidence(
        documents,
        lambda line: "budget" in line and any(word in line for word in ("approved", "estimated", "allocated")) and "not" not in line,
    )
    if approved_budget:
        requirements.append(_req("commercial", "Operate within the documented pilot budget.", *approved_budget))
    return requirements


def _unknown_requirements(
    requirements: list[Requirement],
    budget_status: str,
    data_sensitivity: str,
) -> list[Requirement]:
    unknowns: list[Requirement] = []
    if budget_status == "unknown":
        unknowns.append(Requirement(category="commercial", requirement="Confirm an approved pilot budget.", status="unknown"))
    if data_sensitivity == "unknown":
        unknowns.append(Requirement(category="security", requirement="Confirm the formal data classification and PII scope.", status="unknown"))
    if not any(item.category == "performance" and "volume" in item.requirement.lower() for item in requirements):
        unknowns.append(Requirement(category="performance", requirement="Confirm peak concurrency and request volume.", status="unknown"))
    return unknowns


def _budget_status(text: str) -> str:
    if re.search(r"budget[^\n.]*(?:not yet approved|not approved|unknown|tbd)", text, re.IGNORECASE):
        return "unknown"
    if re.search(r"(?:approved|allocated)[^\n.]*budget|budget[^\n.]*(?:approved|allocated)", text, re.IGNORECASE):
        return "approved"
    if re.search(r"estimated[^\n.]*budget|budget[^\n.]*estimated", text, re.IGNORECASE):
        return "estimated"
    return "unknown"


def _data_sensitivity(text: str) -> str:
    if re.search(r"(?:not confirmed|unknown|tbd)[^\n.]*(?:pii|data classification)|(?:pii|data classification)[^\n.]*(?:not confirmed|unknown|tbd)", text, re.IGNORECASE):
        return "unknown"
    for label in ("restricted", "confidential", "internal", "public"):
        if re.search(rf"data (?:is |classification:?\s*){label}\b", text, re.IGNORECASE):
            return label
    return "unknown"


def _extract_geography(text: str) -> list[str]:
    candidates = [("Singapore", r"\bsingapore\b"), ("Asia-Pacific", r"\b(?:asia-pacific|apac)\b")]
    return [label for label, pattern in candidates if re.search(pattern, text, re.IGNORECASE)]


def _extract_stakeholders(text: str) -> list[Stakeholder]:
    catalog = [
        ("Chief Information Officer", "high", "decision_maker"),
        ("Head of IT", "high", "technical"),
        ("Director of Operations", "medium", "champion"),
        ("Finance Manager", "medium", "commercial"),
    ]
    return [
        Stakeholder(role=role, influence=influence, priority=priority)
        for role, influence, priority in catalog
        if re.search(rf"\b{re.escape(role)}\b", text, re.IGNORECASE)
    ]
