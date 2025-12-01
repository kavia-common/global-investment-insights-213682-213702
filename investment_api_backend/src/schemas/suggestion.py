from typing import List, Optional

from pydantic import BaseModel, Field


class SuggestionCreate(BaseModel):
    symbol: str = Field(..., description="Ticker symbol")
    action: str = Field(..., description="buy/sell/hold")
    rationale: Optional[str] = Field(None, description="Reason for suggestion")
    target_price: Optional[float] = Field(None, description="Target price")
    market: str = Field(default="US", description="US or IN")


class SuggestionPublic(SuggestionCreate):
    id: int = Field(..., description="Suggestion id")
    user_id: int = Field(..., description="User id")


class SuggestionList(BaseModel):
    items: List[SuggestionPublic] = Field(default_factory=list, description="List of suggestions")
