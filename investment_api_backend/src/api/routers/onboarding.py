from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.routers.auth import get_current_user
from src.db.crud import upsert_onboarding
from src.db.session import get_db
from src.schemas.onboarding import OnboardingPublic, OnboardingUpdate

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.post(
    "",
    response_model=OnboardingPublic,
    summary="Upsert onboarding",
    description="Create or update onboarding profile for the authenticated user.",
)
def update_onboarding(payload: OnboardingUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ob = upsert_onboarding(
        db=db,
        user_id=current_user.id,
        experience_level=payload.experience_level,
        risk_tolerance=payload.risk_tolerance,
        goals=payload.goals,
        markets=payload.markets,
    )
    return OnboardingPublic(
        id=ob.id,
        user_id=ob.user_id,
        experience_level=ob.experience_level,
        risk_tolerance=ob.risk_tolerance,
        goals=ob.goals,
        markets=ob.markets,
    )
