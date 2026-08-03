from schemas.opportunity import CoverageAssessment, OpportunityProfile, Risk
from tools.discovery import determine_next_action


def _risk(severity: str) -> Risk:
    return Risk(
        category="security",
        severity=severity,
        statement="Security controls need validation.",
        impact="Architecture cannot be finalized.",
        mitigation="Run a security workshop.",
        owner="Security lead",
    )


def test_complete_opportunity_without_blocking_risk_proceeds_to_sizing():
    decision = determine_next_action(
        OpportunityProfile(customer_name="Northstar", industry="Finance", use_case="Assistant"),
        CoverageAssessment(score=100, covered_dimensions=["all"], missing_dimensions=[]),
        [],
    )

    assert decision.recommendation == "Proceed to solution validation and pilot sizing"


def test_high_risk_blocks_progress_even_when_discovery_is_complete():
    decision = determine_next_action(
        OpportunityProfile(customer_name="Northstar", industry="Finance", use_case="Assistant"),
        CoverageAssessment(score=100, covered_dimensions=["all"], missing_dimensions=[]),
        [_risk("high")],
    )

    assert decision.recommendation == "Run a focused technical discovery workshop"
    assert "1 high-severity risk" in decision.reason


def test_medium_risk_does_not_block_a_complete_opportunity():
    decision = determine_next_action(
        OpportunityProfile(customer_name="Northstar", industry="Finance", use_case="Assistant"),
        CoverageAssessment(score=100, covered_dimensions=["all"], missing_dimensions=[]),
        [_risk("medium")],
    )

    assert decision.recommendation == "Proceed to solution validation and pilot sizing"
