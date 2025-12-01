from typing import Optional

from pydantic import BaseModel, Field


class IntegrationUpsert(BaseModel):
    provider: str = Field(..., description="Provider name: alpaca/zerodha/etc")
    access_key: Optional[str] = Field(None, description="Provider access key or token id (do not store secrets)")


class IntegrationPublic(IntegrationUpsert):
    id: int = Field(..., description="Integration id")
    user_id: int = Field(..., description="User id")
