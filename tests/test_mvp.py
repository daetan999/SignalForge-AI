from agent.orchestrator import analyze_opportunity
from providers.mock_provider import MockOpportunityProvider
from schemas.opportunity import ParsedDocument
from tools.discovery import calculate_discovery_coverage, identify_discovery_gaps
from tools.document_parser import parse_document
from tools.risk_assessment import assess_opportunity_risks


def test_parse_text_document():
    parsed = parse_document("notes.txt", b"Customer: Test Co")
    assert parsed.name == "notes.txt"
    assert "Test Co" in parsed.text


def test_mock_profile_exposes_commercial_gap():
    profile = MockOpportunityProvider().extract_profile(
        [ParsedDocument(name="notes.txt", media_type="text/plain", text="Customer: Test Co")]
    )
    coverage = calculate_discovery_coverage(profile)
    gaps = identify_discovery_gaps(coverage)
    assert coverage.score < 100
    assert any(gap.dimension == "commercial approval" for gap in gaps)


def test_unknown_data_classification_is_high_risk():
    profile = MockOpportunityProvider().extract_profile(
        [ParsedDocument(name="notes.txt", media_type="text/plain", text="Customer: Test Co")]
    )
    risks = assess_opportunity_risks(profile, calculate_discovery_coverage(profile))
    assert any(risk.category == "security" and risk.severity == "high" for risk in risks)


def test_unknown_scale_is_a_technical_risk_even_when_latency_is_known():
    profile = MockOpportunityProvider().extract_profile(
        [
            ParsedDocument(
                name="notes.txt",
                media_type="text/plain",
                text="Customer: Test Co\nUse Case: AI assistant\nLatency under 3 seconds",
            )
        ]
    )
    assert any(
        item.category == "performance" and item.status == "confirmed"
        for item in profile.requirements
    )
    assert any(
        item.category == "performance" and item.status == "unknown" for item in profile.requirements
    )

    risks = assess_opportunity_risks(profile, calculate_discovery_coverage(profile))

    assert any(risk.category == "technical" for risk in risks)


def test_full_mock_workflow_returns_handoff_ready_result():
    result = analyze_opportunity(
        [
            ParsedDocument(
                name="meridian.txt",
                media_type="text/plain",
                text=(
                    "Customer: Meridian Hospitality Group\n"
                    "Use Case: Internal AI assistant\n"
                    "Existing cloud is Google Cloud.\n"
                    "5,000 users\n"
                    "pilot within 8 weeks"
                ),
            )
        ],
        MockOpportunityProvider(),
    )
    assert result.profile.customer_name == "Meridian Hospitality Group"
    assert result.coverage.score > 0
    assert result.gaps
    assert result.risks
    assert result.solution_direction
    assert "digraph" in result.architecture_dot
    assert result.execution_trace
