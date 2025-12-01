from pydantic import BaseModel, Field


class SubscriptionUpdate(BaseModel):
    is_active: bool = Field(..., description="Is subscription active")
    plan: str = Field(..., description="Plan type: free/monthly/annual")


class SubscriptionPublic(SubscriptionUpdate):
    id: int = Field(..., description="Subscription id")
    user_id: int = Field(..., description="User id")
