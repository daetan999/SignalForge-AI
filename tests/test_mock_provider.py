from providers.mock_provider import MockOpportunityProvider
from schemas.opportunity import ParsedDocument


def _document(text: str) -> ParsedDocument:
    return ParsedDocument(name="customer-notes.txt", media_type="text/plain", text=text)


def test_mock_provider_extracts_supported_customer_facts_without_meridian_defaults():
    profile = MockOpportunityProvider().extract_profile(
        [
            _document(
                """Customer: Northstar Bank
Industry: Financial Services
Use Case: Employee policy assistant
The pilot is for 800 users in Singapore and must launch within 12 weeks.
Policies are stored in SharePoint.
"""
            )
        ]
    )

    assert profile.customer_name == "Northstar Bank"
    assert profile.industry == "Financial Services"
    assert profile.use_case == "Employee policy assistant"
    assert profile.intended_users == 800
    assert profile.pilot_timeline_weeks == 12
    assert all("Meridian" not in item.requirement for item in profile.requirements)
    assert all("Google Cloud" not in item.requirement for item in profile.requirements)


def test_mock_provider_marks_unstated_profile_fields_unknown_instead_of_inventing_them():
    profile = MockOpportunityProvider().extract_profile(
        [_document("Customer: Northstar Bank\nUse Case: Employee policy assistant")]
    )

    assert profile.industry == "Unknown"
    assert profile.intended_users is None
    assert profile.pilot_timeline_weeks is None
    assert profile.geography == []
    assert profile.stakeholders == []
    assert not any(
        item.status == "confirmed" and item.category == "users" for item in profile.requirements
    )


def test_every_confirmed_mock_requirement_has_source_evidence():
    profile = MockOpportunityProvider().extract_profile(
        [
            _document(
                """Customer: Northstar Bank
Use Case: Employee policy assistant
The pilot is for 800 users.
Role-based access control is required.
"""
            )
        ]
    )

    confirmed = [item for item in profile.requirements if item.status == "confirmed"]
    assert confirmed
    assert all(item.evidence is not None for item in confirmed)
    assert all(item.evidence.source == "customer-notes.txt" for item in confirmed)
    assert all(item.evidence.quote for item in confirmed)


def test_mock_provider_recognizes_confirmed_scale_requirements():
    profile = MockOpportunityProvider().extract_profile(
        [
            _document(
                """Customer: Northstar Bank
Use Case: Employee policy assistant
Peak concurrency is 120 users and monthly request volume is 900,000.
"""
            )
        ]
    )

    performance = [item for item in profile.requirements if item.category == "performance"]
    assert any(
        item.status == "confirmed" and "scale" in item.requirement.lower() for item in performance
    )
    assert not any(item.status == "unknown" for item in performance)
