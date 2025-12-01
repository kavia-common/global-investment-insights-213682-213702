from typing import List

from pydantic import BaseModel, Field


class HoldingUpsert(BaseModel):
    symbol: str = Field(..., description="Ticker symbol")
    quantity: float = Field(..., ge=0, description="Quantity/shares")
    average_price: float = Field(..., ge=0, description="Average purchase price")
    market: str = Field(default="US", description="US or IN")


class HoldingPublic(HoldingUpsert):
    id: int = Field(..., description="Holding id")
    portfolio_id: int = Field(..., description="Portfolio id")


class PortfolioPublic(BaseModel):
    id: int = Field(..., description="Portfolio id")
    name: str = Field(..., description="Portfolio name")
    currency: str = Field(..., description="Portfolio currency")
    total_value: float = Field(..., description="Total market value")


class PortfolioWithHoldings(PortfolioPublic):
    holdings: List[HoldingPublic] = Field(default_factory=list, description="List of holdings")
