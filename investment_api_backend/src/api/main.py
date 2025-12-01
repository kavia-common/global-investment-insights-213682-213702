import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import auth as auth_router
from src.api.routers import onboarding as onboarding_router
from src.api.routers import portfolio as portfolio_router
from src.api.routers import suggestions as suggestions_router
from src.api.routers import subscription as subscription_router
from src.api.routers import integrations as integrations_router
from src.core.config import get_settings

# Important: avoid importing engine at module import to prevent DB connection attempts during tests
# Importing Base and engine only within startup event when needed.
settings = get_settings()

openapi_tags = [
    {"name": "Authentication", "description": "User registration, login, and session endpoints."},
    {"name": "Onboarding", "description": "Profile onboarding and risk/goals."},
    {"name": "Portfolio", "description": "Portfolio and holdings management."},
    {"name": "Suggestions", "description": "Investment suggestions and rationale."},
    {"name": "Subscription", "description": "Subscription management and pricing."},
    {"name": "Integrations", "description": "External trading/data provider integrations."},
]

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_tags=openapi_tags,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS or ["*"],
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
def on_startup():
    """
    Optionally create database tables on application startup.

    Controlled via environment variable:
    - CREATE_DB_ON_STARTUP=true: create all tables using configured engine.
    - Any other value or unset: do not touch the database (safe for tests).
    """
    create_on_start = os.getenv("CREATE_DB_ON_STARTUP", "false").lower() == "true"
    if not create_on_start:
        return
    # Deferred import to prevent DB engine creation at import time
    from src.db.session import Base, engine

    # Create DB tables if they do not exist yet (useful for local/dev bootstrap)
    Base.metadata.create_all(bind=engine)


@app.get("/", summary="Health Check", tags=["Authentication"])
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"message": "Healthy"}


@app.get(
    "/websocket-usage",
    summary="WebSocket Usage",
    description=(
        "This API currently does not expose WebSocket endpoints. "
        "In future versions, real-time updates may be provided."
    ),
    tags=["Authentication"],
)
def websocket_usage():
    return {"websocket": "No WebSocket endpoints available at this time."}


# Routers
app.include_router(auth_router.router)
app.include_router(onboarding_router.router)
app.include_router(portfolio_router.router)
app.include_router(suggestions_router.router)
app.include_router(subscription_router.router)
app.include_router(integrations_router.router)
