from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from src.db.session import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    onboarding = relationship("Onboarding", back_populates="user", uselist=False)
    portfolios = relationship("Portfolio", back_populates="user")
    suggestions = relationship("Suggestion", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    integrations = relationship("Integration", back_populates="user")


class Onboarding(Base):
    __tablename__ = "onboarding"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    experience_level = Column(String(50), nullable=True)  # e.g., beginner/intermediate/expert
    risk_tolerance = Column(String(50), nullable=True)  # e.g., low/medium/high
    goals = Column(Text, nullable=True)  # JSON string or CSV of goals
    markets = Column(String(50), nullable=True)  # e.g., 'US', 'IN', or 'US,IN'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="onboarding")


class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), default="Default", nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    total_value = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="portfolios")
    holdings = relationship("Holding", back_populates="portfolio")


class Holding(Base):
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False, index=True)
    symbol = Column(String(20), nullable=False)
    quantity = Column(Float, default=0.0, nullable=False)
    average_price = Column(Float, default=0.0, nullable=False)
    market = Column(String(10), default="US", nullable=False)  # US or IN
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")
    __table_args__ = (UniqueConstraint("portfolio_id", "symbol", name="uq_portfolio_symbol"),)


class Suggestion(Base):
    __tablename__ = "suggestions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    symbol = Column(String(20), nullable=False)
    action = Column(String(10), nullable=False)  # buy/sell/hold
    rationale = Column(Text, nullable=True)
    target_price = Column(Float, nullable=True)
    market = Column(String(10), default="US", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="suggestions")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    plan = Column(String(50), default="free", nullable=False)  # free/monthly/annual
    current_period_end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="subscription")


class Integration(Base):
    __tablename__ = "integrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(50), nullable=False)  # alpaca/zerodha/...
    access_key = Column(String(255), nullable=True)  # store token ids, not secrets, in production use vault
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="integrations")
