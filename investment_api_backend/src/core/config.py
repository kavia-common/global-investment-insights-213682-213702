import os
from functools import lru_cache
from typing import List, Optional

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator
from dotenv import load_dotenv

# Load .env from project root or container dir automatically
load_dotenv()


class Settings(BaseModel):
    """Application settings loaded from environment variables via .env."""
    APP_NAME: str = Field(default="Investment API", description="Application Name")
    APP_DESCRIPTION: str = Field(
        default=(
            "Backend API for investment analysis, integrations, auth, onboarding, "
            "portfolio, and compliance."
        ),
        description=(
            "Application description for OpenAPI metadata"
        ),
    )
    APP_VERSION: str = Field(default="0.1.0", description="Application Version")

    # Security
    SECRET_KEY: str = Field(default="change-me", description="JWT signing secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24, description="Access token expiry in minutes")
    ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")
    PASSWORD_HASH_SCHEME: str = Field(default="argon2", description="Password hashing scheme (deprecated setting; argon2 is enforced)")

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list, description="Allowed CORS origins")
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default_factory=lambda: ["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default_factory=lambda: ["*"])

    # Database
    POSTGRES_URL: Optional[str] = Field(default=None, description="Full PostgreSQL URL, if provided will be used")
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None
    POSTGRES_HOST: Optional[str] = Field(default="localhost")

    # External Services (stubs for now)
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    YAHOO_FINANCE_ENABLED: bool = True
    ALPACA_API_KEY: Optional[str] = None
    ALPACA_API_SECRET: Optional[str] = None
    ZERODHA_API_KEY: Optional[str] = None
    ZERODHA_API_SECRET: Optional[str] = None

    # Pricing / Subscription
    REGISTRATION_FEE_USD: float = 0.0
    SUBSCRIPTION_MONTHLY_USD: float = 0.0

    # Site URL for email redirects (if needed by frontend flows)
    SITE_URL: Optional[AnyHttpUrl] = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if not v:
            # Try to read CSV from env BACKEND_CORS_ORIGINS
            raw = os.getenv("BACKEND_CORS_ORIGINS")
            if not raw:
                return []
            items = [item.strip() for item in raw.split(",") if item.strip()]
            return items
        if isinstance(v, str):
            items = [item.strip() for item in v.split(",") if item.strip()]
            return items
        return v

    # PUBLIC_INTERFACE
    def assemble_database_uri(self) -> str:
        """Assemble SQLAlchemy database URI from either POSTGRES_URL or discrete parts."""
        if self.POSTGRES_URL:
            return self.POSTGRES_URL
        user = self.POSTGRES_USER or ""
        password = self.POSTGRES_PASSWORD or ""
        host = self.POSTGRES_HOST or "localhost"
        port = self.POSTGRES_PORT or "5432"
        db = self.POSTGRES_DB or "postgres"
        if password:
            return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
        return f"postgresql+psycopg2://{user}@{host}:{port}/{db}"


# PUBLIC_INTERFACE
@lru_cache
def get_settings() -> Settings:
    """Return cached application settings from environment variables."""
    return Settings(
        APP_NAME=os.getenv("APP_NAME", "Investment API"),
        APP_DESCRIPTION=os.getenv(
            "APP_DESCRIPTION",
            (
                "Backend API for investment analysis, integrations, auth, onboarding, "
                "portfolio, and compliance."
            ),
        ),
        APP_VERSION=os.getenv("APP_VERSION", "0.1.0"),
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me"),
        ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24))),
        ALGORITHM=os.getenv("ALGORITHM", "HS256"),
        PASSWORD_HASH_SCHEME=os.getenv("PASSWORD_HASH_SCHEME", "argon2"),
        BACKEND_CORS_ORIGINS=[],  # parsed in validator from BACKEND_CORS_ORIGINS env
        CORS_ALLOW_CREDENTIALS=os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true",
        CORS_ALLOW_METHODS=["*"],
        CORS_ALLOW_HEADERS=["*"],
        POSTGRES_URL=os.getenv("POSTGRES_URL"),
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        POSTGRES_DB=os.getenv("POSTGRES_DB"),
        POSTGRES_PORT=os.getenv("POSTGRES_PORT"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost"),
        ALPHA_VANTAGE_API_KEY=os.getenv("ALPHA_VANTAGE_API_KEY"),
        YAHOO_FINANCE_ENABLED=os.getenv("YAHOO_FINANCE_ENABLED", "true").lower() == "true",
        ALPACA_API_KEY=os.getenv("ALPACA_API_KEY"),
        ALPACA_API_SECRET=os.getenv("ALPACA_API_SECRET"),
        ZERODHA_API_KEY=os.getenv("ZERODHA_API_KEY"),
        ZERODHA_API_SECRET=os.getenv("ZERODHA_API_SECRET"),
        REGISTRATION_FEE_USD=float(os.getenv("REGISTRATION_FEE_USD", "0.0")),
        SUBSCRIPTION_MONTHLY_USD=float(os.getenv("SUBSCRIPTION_MONTHLY_USD", "0.0")),
        SITE_URL=os.getenv("SITE_URL"),
    )
