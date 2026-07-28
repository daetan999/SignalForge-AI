"""Discovery coverage, gap generation, and deterministic next-step logic."""
from __future__ import annotations

from schemas.opportunity import CoverageAssessment, Decision, DiscoveryGap, OpportunityProfile, Risk


DIMENSIONS = {
    "business objective": "business",
    "user population": "users",
    "data sources": "data",
    "security and governance": "security",
    "performance and scale": "performance",
    "integrations": "integration",
    "timeline": "timeline",
    "commercial approval": "commercial",
}

QUESTIONS = {
    "business objective": ("important", "Which measurable business outcome defines pilot success?"),
    "user population": ("important", "How many users and peak concurrent sessions must the pilot support?"),
    "data sources": ("critical", "Which systems and repositories are in scope, and who owns access approval?"),
    "security and governance": ("critical", "What data classification, PII, residency, and audit requirements apply?"),
    "performance and scale": ("important", "What are the peak request volume, latency target, and availability requirement?"),
    "integrations": ("important", "Which identity, data, and workflow integrations are mandatory for the pilot?"),
    "timeline": ("important", "What date is fixed, and which dependencies could affect the pilot timeline?"),
    "commercial approval": ("critical", "What pilot budget is approved, and who owns commercial sign-off?"),
}


def calculate_discovery_coverage(profile: OpportunityProfile) -> CoverageAssessment:
    """Calculate coverage from confirmed requirements across required dimensions."""
    confirmed = {item.category for item in profile.requirements if item.status == "confirmed"}
    covered = [label for label, category in DIMENSIONS.items() if category in confirmed]
    missing = [label for label, category in DIMENSIONS.items() if category not in confirmed]
    score = round(len(covered) / len(DIMENSIONS) * 100)
    return CoverageAssessment(score=score, covered_dimensions=covered, missing_dimensions=missing)


def identify_discovery_gaps(coverage: CoverageAssessment) -> list[DiscoveryGap]:
    """Create prioritized, actionable questions for every missing dimension."""
    gaps: list[DiscoveryGap] = []
    for dimension in coverage.missing_dimensions:
        priority, question = QUESTIONS[dimension]
        gaps.append(
            DiscoveryGap(
                dimension=dimension,
                priority=priority,
                question=question,
                rationale=f"{dimension.title()} is required before final solution validation.",
            )
        )
    return gaps


def determine_next_action(
    profile: OpportunityProfile,
    coverage: CoverageAssessment,
    risks: list[Risk],
) -> Decision:
    """Select the next sales-engineering action from coverage and risk signals."""
    high_risks = [risk for risk in risks if risk.severity == "high"]
    if coverage.score < 60 or high_risks:
        return Decision(
            recommendation="Run a focused technical discovery workshop",
            reason=(
                f"Discovery coverage is {coverage.score}% with {len(high_risks)} high-severity risk(s); "
                "a firm architecture or commercial commitment would be premature."
            ),
            next_steps=[
                "Resolve critical security, scale, and budget questions.",
                "Confirm pilot success metrics and executive sponsor.",
                "Narrow the pilot scope to an achievable eight-week outcome.",
            ],
        )
    return Decision(
        recommendation="Proceed to solution validation and pilot sizing",
        reason=f"Discovery coverage is {coverage.score}% and no blocking risk remains.",
        next_steps=[
            "Validate the initial architecture with the customer engineering team.",
            "Estimate capacity, delivery effort, and pilot cost.",
            "Prepare the executive business case and mutual action plan.",
        ],
    )
