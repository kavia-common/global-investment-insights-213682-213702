from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.routers.auth import get_current_user
from src.db.crud import get_or_create_default_portfolio, list_holdings, upsert_holding
from src.db.session import get_db
from src.schemas.portfolio import HoldingPublic, HoldingUpsert, PortfolioWithHoldings

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get(
    "",
    response_model=PortfolioWithHoldings,
    summary="Get portfolio",
    description="Get the authenticated user's default portfolio with holdings.",
)
def get_portfolio(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    pf = get_or_create_default_portfolio(db, user_id=current_user.id)
    holdings = list_holdings(db, portfolio_id=pf.id)
    return PortfolioWithHoldings(
        id=pf.id,
        name=pf.name,
        currency=pf.currency,
        total_value=pf.total_value,
        holdings=[
            HoldingPublic(
                id=h.id,
                portfolio_id=pf.id,
                symbol=h.symbol,
                quantity=h.quantity,
                average_price=h.average_price,
                market=h.market,
            )
            for h in holdings
        ],
    )


@router.post(
    "/holdings",
    response_model=HoldingPublic,
    summary="Upsert holding",
    description="Create or update a holding in the default portfolio.",
)
def upsert_holding_endpoint(
    payload: HoldingUpsert, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    pf = get_or_create_default_portfolio(db, user_id=current_user.id)
    h = upsert_holding(
        db, portfolio_id=pf.id, symbol=payload.symbol, quantity=payload.quantity,
        average_price=payload.average_price, market=payload.market
    )
    return HoldingPublic(
        id=h.id,
        portfolio_id=pf.id,
        symbol=h.symbol,
        quantity=h.quantity,
        average_price=h.average_price,
        market=h.market,
    )
