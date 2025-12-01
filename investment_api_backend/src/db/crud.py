from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.security import get_password_hash, verify_password
from src.db import models


# Users
# PUBLIC_INTERFACE
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get a user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


# PUBLIC_INTERFACE
def create_user(db: Session, email: str, password: str, full_name: Optional[str] = None) -> models.User:
    """Create a new user with hashed password."""
    hashed = get_password_hash(password)
    user = models.User(email=email, full_name=full_name, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# PUBLIC_INTERFACE
def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate user by email and password."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Onboarding
# PUBLIC_INTERFACE
def upsert_onboarding(
    db: Session, user_id: int, experience_level: Optional[str], risk_tolerance: Optional[str],
    goals: Optional[str], markets: Optional[str]
) -> models.Onboarding:
    """Create or update onboarding profile for a user."""
    ob = db.query(models.Onboarding).filter(models.Onboarding.user_id == user_id).first()
    now = datetime.utcnow()
    if not ob:
        ob = models.Onboarding(
            user_id=user_id,
            experience_level=experience_level,
            risk_tolerance=risk_tolerance,
            goals=goals,
            markets=markets,
            created_at=now,
            updated_at=now,
        )
        db.add(ob)
    else:
        ob.experience_level = experience_level
        ob.risk_tolerance = risk_tolerance
        ob.goals = goals
        ob.markets = markets
        ob.updated_at = now
    db.commit()
    db.refresh(ob)
    return ob


# Portfolio
# PUBLIC_INTERFACE
def get_or_create_default_portfolio(db: Session, user_id: int, currency: str = "USD") -> models.Portfolio:
    """Fetch the default portfolio for user or create one."""
    pf = (
        db.query(models.Portfolio)
        .filter(models.Portfolio.user_id == user_id, models.Portfolio.name == "Default")
        .first()
    )
    if pf:
        return pf
    pf = models.Portfolio(user_id=user_id, name="Default", currency=currency)
    db.add(pf)
    db.commit()
    db.refresh(pf)
    return pf


# PUBLIC_INTERFACE
def list_holdings(db: Session, portfolio_id: int) -> List[models.Holding]:
    """List holdings in a portfolio."""
    return db.query(models.Holding).filter(models.Holding.portfolio_id == portfolio_id).all()


# PUBLIC_INTERFACE
def upsert_holding(
    db: Session, portfolio_id: int, symbol: str, quantity: float, average_price: float, market: str
) -> models.Holding:
    """Create or update holding position for a symbol."""
    h = (
        db.query(models.Holding)
        .filter(models.Holding.portfolio_id == portfolio_id, models.Holding.symbol == symbol)
        .first()
    )
    now = datetime.utcnow()
    if not h:
        h = models.Holding(
            portfolio_id=portfolio_id,
            symbol=symbol,
            quantity=quantity,
            average_price=average_price,
            market=market,
            created_at=now,
            updated_at=now,
        )
        db.add(h)
    else:
        h.quantity = quantity
        h.average_price = average_price
        h.market = market
        h.updated_at = now
    db.commit()
    db.refresh(h)
    return h


# Suggestions
# PUBLIC_INTERFACE
def create_suggestion(
    db: Session, user_id: int, symbol: str, action: str, rationale: str, target_price: Optional[float], market: str
) -> models.Suggestion:
    """Create an investment suggestion for a user."""
    s = models.Suggestion(
        user_id=user_id,
        symbol=symbol,
        action=action,
        rationale=rationale,
        target_price=target_price,
        market=market,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


# PUBLIC_INTERFACE
def list_suggestions(db: Session, user_id: int) -> List[models.Suggestion]:
    """List suggestions for a user."""
    return db.query(models.Suggestion).filter(models.Suggestion.user_id == user_id).all()


# Subscription
# PUBLIC_INTERFACE
def set_subscription(db: Session, user_id: int, is_active: bool, plan: str) -> models.Subscription:
    """Create or update subscription for a user."""
    sub = db.query(models.Subscription).filter(models.Subscription.user_id == user_id).first()
    if not sub:
        sub = models.Subscription(user_id=user_id, is_active=is_active, plan=plan)
        db.add(sub)
    else:
        sub.is_active = is_active
        sub.plan = plan
    db.commit()
    db.refresh(sub)
    return sub


# Integrations
# PUBLIC_INTERFACE
def upsert_integration(db: Session, user_id: int, provider: str, access_key: Optional[str]) -> models.Integration:
    """Create or update an integration for a user."""
    integ = (
        db.query(models.Integration)
        .filter(models.Integration.user_id == user_id, models.Integration.provider == provider)
        .first()
    )
    if not integ:
        integ = models.Integration(user_id=user_id, provider=provider, access_key=access_key)
        db.add(integ)
    else:
        integ.access_key = access_key
    db.commit()
    db.refresh(integ)
    return integ
