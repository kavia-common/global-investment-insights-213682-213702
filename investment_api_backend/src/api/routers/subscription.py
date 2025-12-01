from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.routers.auth import get_current_user
from src.db.crud import set_subscription
from src.db.session import get_db
from src.schemas.subscription import SubscriptionPublic, SubscriptionUpdate

router = APIRouter(prefix="/subscription", tags=["Subscription"])


@router.post(
    "",
    response_model=SubscriptionPublic,
    summary="Set subscription",
    description="Create or update the user's subscription.",
)
def update_subscription(payload: SubscriptionUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    sub = set_subscription(db, user_id=current_user.id, is_active=payload.is_active, plan=payload.plan)
    return SubscriptionPublic(id=sub.id, user_id=sub.user_id, is_active=sub.is_active, plan=sub.plan)
