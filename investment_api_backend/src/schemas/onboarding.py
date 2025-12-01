from typing import Optional

from pydantic import BaseModel, Field


class OnboardingUpdate(BaseModel):
    experience_level: Optional[str] = Field(None, description="beginner/intermediate/expert")
    risk_tolerance: Optional[str] = Field(None, description="low/medium/high")
    goals: Optional[str] = Field(None, description="Goals as CSV or JSON string")
    markets: Optional[str] = Field(None, description="Markets: US, IN, or US,IN")


class OnboardingPublic(OnboardingUpdate):
    id: int = Field(..., description="Onboarding id")
    user_id: int = Field(..., description="User id")
