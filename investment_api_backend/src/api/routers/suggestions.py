from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.routers.auth import get_current_user
from src.db.crud import create_suggestion, list_suggestions
from src.db.session import get_db
from src.schemas.suggestion import SuggestionCreate, SuggestionList, SuggestionPublic
from src.services.market_data import market_data_service

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])


@router.get(
    "",
    response_model=SuggestionList,
    summary="List suggestions",
    description="List saved suggestions for the authenticated user.",
)
def get_suggestions(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    items = list_suggestions(db, current_user.id)
    result_items = []
    for s in items:
        result_items.append(
            SuggestionPublic(
                id=s.id,
                user_id=s.user_id,
                symbol=s.symbol,
                action=s.action,
                rationale=s.rationale,
                target_price=s.target_price,
                market=s.market,
            )
        )
    return SuggestionList(items=result_items)


@router.post(
    "",
    response_model=SuggestionPublic,
    summary="Generate and save a suggestion",
    description="Generate a mock suggestion using market data and save it.",
)
def generate_suggestion(payload: SuggestionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    quote = market_data_service.get_quote(
        payload.symbol,
        payload.market,
    )
    action = payload.action
    rationale = (
        payload.rationale
        or f"Based on recent price {quote['price']}"
    )
    s = create_suggestion(
        db=db,
        user_id=current_user.id,
        symbol=payload.symbol,
        action=action,
        rationale=rationale,
        target_price=payload.target_price,
        market=payload.market,
    )
    return SuggestionPublic(
        id=s.id,
        user_id=s.user_id,
        symbol=s.symbol,
        action=s.action,
        rationale=s.rationale,
        target_price=s.target_price,
        market=s.market,
    )
