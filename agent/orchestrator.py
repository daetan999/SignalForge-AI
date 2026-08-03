"""Multi-step opportunity analysis workflow."""

from __future__ import annotations

from config.settings import Settings
from providers.base import OpportunityProvider
from providers.mock_provider import MockOpportunityProvider
from providers.vertex_provider import VertexOpportunityProvider
from schemas.opportunity import AnalysisResult, ParsedDocument
from tools.architecture_builder import build_architecture_dot
from tools.discovery import (
    calculate_discovery_coverage,
    determine_next_action,
    identify_discovery_gaps,
)
from tools.risk_assessment import assess_opportunity_risks
from tools.solution_mapper import map_requirements_to_gcp_services


def get_provider(settings: Settings) -> OpportunityProvider:
    """Resolve the active AI provider without changing application code."""
    settings.validate()
    if settings.app_mode == "vertex":
        return VertexOpportunityProvider(settings)
    return MockOpportunityProvider()


def analyze_opportunity(
    documents: list[ParsedDocument],
    provider: OpportunityProvider,
) -> AnalysisResult:
    """Run the complete observe-evaluate-decide-act workflow."""
    trace = [f"Parsed {len(documents)} customer document(s)"]
    profile = provider.extract_profile(documents)
    confirmed_count = sum(requirement.status == "confirmed" for requirement in profile.requirements)
    trace.append(f"Extracted {confirmed_count} confirmed requirements")

    coverage = calculate_discovery_coverage(profile)
    gaps = identify_discovery_gaps(coverage)
    trace.append(f"Identified {len(gaps)} missing discovery dimension(s)")

    risks = assess_opportunity_risks(profile, coverage)
    trace.append(f"Assessed {len(risks)} material opportunity risk(s)")

    solution = map_requirements_to_gcp_services(profile)
    trace.append(f"Mapped requirements to {len(solution)} controlled Google Cloud capabilities")

    decision = determine_next_action(profile, coverage, risks)
    high_risk_count = sum(risk.severity == "high" for risk in risks)
    readiness = max(0, min(100, coverage.score - high_risk_count * 12 - len(gaps) * 2))
    trace.append("Selected the recommended next action")
    trace.append("Generated AE-to-SE handoff artifacts")

    return AnalysisResult(
        profile=profile,
        coverage=coverage,
        gaps=gaps,
        risks=risks,
        readiness_score=readiness,
        solution_direction=solution,
        decision=decision,
        architecture_dot=build_architecture_dot(solution),
        execution_trace=trace,
    )
