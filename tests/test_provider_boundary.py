import json

from config.settings import Settings
from providers.vertex_provider import VertexOpportunityProvider
from schemas.opportunity import ParsedDocument


class _Response:
    def __init__(self, text: str | None):
        self.text = text


class _Models:
    def __init__(self, responses: list[_Response]):
        self.responses = iter(responses)
        self.calls: list[dict] = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.responses)


class _Client:
    def __init__(self, responses: list[_Response]):
        self.models = _Models(responses)
        self.closed = False

    def close(self):
        self.closed = True


def _valid_profile_json() -> str:
    return json.dumps({
        "customer_name": "Northstar Bank",
        "industry": "Financial Services",
        "use_case": "Employee policy assistant",
        "requirements": [],
        "stakeholders": [],
    })


def test_vertex_provider_uses_injected_client_and_configured_model():
    client = _Client([_Response(_valid_profile_json())])
    settings = Settings(
        app_mode="vertex",
        project_id="sandbox-project",
        location="global",
        model_name="gemini-test-model",
    )
    provider = VertexOpportunityProvider(settings, client_factory=lambda **_: client)

    profile = provider.extract_profile([
        ParsedDocument(name="notes.txt", media_type="text/plain", text="Customer: Northstar Bank")
    ])

    assert profile.customer_name == "Northstar Bank"
    assert client.models.calls[0]["model"] == "gemini-test-model"
    assert client.closed is True


def test_vertex_provider_retries_once_after_malformed_structured_output():
    client = _Client([_Response("not-json"), _Response(_valid_profile_json())])
    settings = Settings(app_mode="vertex", project_id="sandbox-project")
    provider = VertexOpportunityProvider(settings, client_factory=lambda **_: client)

    profile = provider.extract_profile([
        ParsedDocument(name="notes.txt", media_type="text/plain", text="Customer: Northstar Bank")
    ])

    assert profile.customer_name == "Northstar Bank"
    assert len(client.models.calls) == 2
    assert client.closed is True
