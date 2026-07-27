"""Pydantic models shared across the agent, tools, and UI."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    name: str
    media_type: str
    text: str


class Evidence(BaseModel):
    source: str
    quote: str
    confidence: float = Field(ge=0.0, le=1.0)


class Requirement(BaseModel):
    category: Literal[
        "business", "users", "data", "security", "performance",
        "integration", "timeline", "commercial", "operations"
    ]
    requirement: str
    status: Literal["confirmed", "assumed", "unknown"] = "confirmed"
    evidence: Evidence | None = None


class Stakeholder(BaseModel):
    role: str
    influence: Literal["high", "medium", "low"]
    priority: Literal["champion", "decision_maker", "technical", "commercial", "user"]


class OpportunityProfile(BaseModel):
    customer_name: str
    industry: str
    use_case: str
    stage: str = "Technical discovery"
    geography: list[str] = Field(default_factory=list)
    intended_users: int | None = None
    pilot_timeline_weeks: int | None = None
    budget_status: Literal["approved", "estimated", "unknown"] = "unknown"
    data_sensitivity: Literal["public", "internal", "confidential", "restricted", "unknown"] = "unknown"
    requirements: list[Requirement] = Field(default_factory=list)
    stakeholders: list[Stakeholder] = Field(default_factory=list)


class CoverageAssessment(BaseModel):
    score: int = Field(ge=0, le=100)
    covered_dimensions: list[str]
    missing_dimensions: list[str]


class DiscoveryGap(BaseModel):
    dimension: str
    priority: Literal["critical", "important", "optional"]
    question: str
    rationale: str


class Risk(BaseModel):
    category: Literal["security", "commercial", "delivery", "technical", "adoption"]
    severity: Literal["high", "medium", "low"]
    statement: str
    impact: str
    mitigation: str
    owner: str


class SolutionComponent(BaseModel):
    capability: str
    service: str
    rationale: str
    confidence: Literal["high", "medium", "low"] = "medium"


class Decision(BaseModel):
    recommendation: str
    reason: str
    next_steps: list[str]


class AnalysisResult(BaseModel):
    profile: OpportunityProfile
    coverage: CoverageAssessment
    gaps: list[DiscoveryGap]
    risks: list[Risk]
    readiness_score: int = Field(ge=0, le=100)
    solution_direction: list[SolutionComponent]
    decision: Decision
    architecture_dot: str
    execution_trace: list[str]
