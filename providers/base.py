"""Provider contract that keeps model access separate from business logic."""
from __future__ import annotations

from abc import ABC, abstractmethod

from schemas.opportunity import OpportunityProfile, ParsedDocument


class OpportunityProvider(ABC):
    """Extract a structured opportunity profile from unstructured documents."""

    @abstractmethod
    def extract_profile(self, documents: list[ParsedDocument]) -> OpportunityProfile:
        """Return a validated opportunity profile."""
        raise NotImplementedError
