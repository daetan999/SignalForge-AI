"""Deterministic opportunity risk rules."""

from __future__ import annotations

from schemas.opportunity import CoverageAssessment, OpportunityProfile, Risk


def assess_opportunity_risks(
    profile: OpportunityProfile,
    coverage: CoverageAssessment,
) -> list[Risk]:
    """Assess material risks without relying on model-generated severity scores."""
    risks: list[Risk] = []
    if profile.data_sensitivity == "unknown":
        risks.append(
            Risk(
                category="security",
                severity="high",
                statement="Data classification and PII scope are unconfirmed.",
                impact=(
                    "The team cannot finalize access controls, residency, logging, "
                    "or model-data handling."
                ),
                mitigation=(
                    "Run security discovery and obtain data-owner approval before "
                    "solution validation."
                ),
                owner="Customer security lead",
            )
        )
    if profile.budget_status == "unknown":
        risks.append(
            Risk(
                category="commercial",
                severity="medium",
                statement="No approved pilot budget is recorded.",
                impact="Technical design may progress without a viable commercial path.",
                mitigation="Confirm budget range, buying process, and financial approver.",
                owner="Account executive",
            )
        )
    if profile.pilot_timeline_weeks and profile.pilot_timeline_weeks <= 8 and coverage.score < 75:
        risks.append(
            Risk(
                category="delivery",
                severity="high",
                statement="The pilot timeline is aggressive relative to discovery maturity.",
                impact="Unresolved requirements could create rework or an over-scoped pilot.",
                mitigation=(
                    "Define one measurable use case and sequence non-critical "
                    "integrations after the pilot."
                ),
                owner="Solutions engineer",
            )
        )
    performance_requirements = [
        requirement for requirement in profile.requirements if requirement.category == "performance"
    ]
    if not any(
        requirement.status == "confirmed" for requirement in performance_requirements
    ) or any(requirement.status == "unknown" for requirement in performance_requirements):
        risks.append(
            Risk(
                category="technical",
                severity="medium",
                statement="Peak concurrency and request volume are unknown.",
                impact="Capacity, latency, and cost assumptions cannot be validated.",
                mitigation=(
                    "Collect expected daily requests, peak concurrency, context size, "
                    "and latency SLO."
                ),
                owner="Customer platform lead",
            )
        )
    return risks
