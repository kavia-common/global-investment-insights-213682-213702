from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.routers.auth import get_current_user
from src.db.crud import upsert_integration
from src.db.session import get_db
from src.schemas.integration import IntegrationPublic, IntegrationUpsert

router = APIRouter(prefix="/integrations", tags=["Integrations"])


@router.post(
    "",
    response_model=IntegrationPublic,
    summary="Upsert integration",
    description="Connect or update a trading/data provider integration.",
)
def upsert_integration_endpoint(
    payload: IntegrationUpsert, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    integ = upsert_integration(db, user_id=current_user.id, provider=payload.provider, access_key=payload.access_key)
    return IntegrationPublic(id=integ.id, user_id=integ.user_id, provider=integ.provider, access_key=integ.access_key)
