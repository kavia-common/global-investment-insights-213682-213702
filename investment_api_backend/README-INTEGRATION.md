# Investment API Backend - Integration and Environment

This FastAPI service powers authentication, onboarding, portfolio, suggestions, subscriptions, and integrations. It connects to PostgreSQL and exposes REST endpoints for the React SPA.

## Environment Variables

Create a .env file in this directory using the template below (see .env.example):

Required
- SECRET_KEY: JWT signing secret (use a long random string)
- POSTGRES_URL: Full SQLAlchemy URL if provided, e.g. postgresql+psycopg2://appuser:dbuser123@localhost:5000/myapp
  - Alternatively set discrete parts:
    - POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
- BACKEND_CORS_ORIGINS: Comma-separated list of allowed frontend origins (scheme+host+port), e.g.
  - http://localhost:3000,https://preview-frontend.example.com
- CORS_ALLOW_CREDENTIALS: true/false; default true

Optional
- ACCESS_TOKEN_EXPIRE_MINUTES: default 1440
- APP_NAME, APP_DESCRIPTION, APP_VERSION
- SITE_URL: Base URL for frontend if needed in link generation
- External keys (stubs): ALPHA_VANTAGE_API_KEY, ALPACA_API_KEY, ALPACA_API_SECRET, ZERODHA_API_KEY, ZERODHA_API_SECRET

Notes
- If BACKEND_CORS_ORIGINS is empty, service allows ["*"] to simplify local development.
- assemble_database_uri() will use POSTGRES_URL if set, otherwise builds from individual parts.

## CORS

CORS is configured in src/api/main.py using:
- allow_origins = settings.BACKEND_CORS_ORIGINS or ["*"]
- allow_credentials = settings.CORS_ALLOW_CREDENTIALS (default true)
- allow_methods, allow_headers default ["*"]

To allow your frontend:
- Set BACKEND_CORS_ORIGINS=http://localhost:3000 in local dev
- Set it to your preview/prod frontend URLs in those environments

## Database

The backend expects a PostgreSQL database. It uses SQLAlchemy and psycopg2.

Set:
- POSTGRES_URL=postgresql+psycopg2://appuser:dbuser123@localhost:5000/myapp
or
- POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD

## OpenAPI generation

To regenerate the OpenAPI spec after modifying routes:

1) Install dependencies:
   pip install -r requirements.txt

2) Generate:
   python -m src.api.generate_openapi

Output is written to interfaces/openapi.json.

## Running locally

1) Ensure database is running (see investment_database/startup.sh)
2) Create .env (see below)
3) Install deps: pip install -r requirements.txt
4) Start: uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
5) Docs: http://localhost:8000/docs

## .env template (copy from .env.example)

SECRET_KEY=change-me
POSTGRES_URL=postgresql+psycopg2://appuser:dbuser123@localhost:5000/myapp
BACKEND_CORS_ORIGINS=http://localhost:3000
CORS_ALLOW_CREDENTIALS=true
ACCESS_TOKEN_EXPIRE_MINUTES=1440
