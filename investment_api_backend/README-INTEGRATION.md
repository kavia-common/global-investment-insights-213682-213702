# Investment API Backend - Testing

## Running tests (pytest)
Uses SQLite test database by default.

Commands:
- Make: `make test-backend`
- Direct: `cd investment_api_backend && TEST_DATABASE_URL=sqlite:///./test_db.sqlite3 pytest -q`

Environment:
- TEST_DATABASE_URL: override to use a different DB for tests (default: SQLite file).
- Regular app DB envs are ignored by tests due to dependency override in tests/conftest.py.
- CREATE_DB_ON_STARTUP: when set to `true`, the FastAPI app will create tables on startup using the configured database engine. Leave unset/false during tests to avoid touching Postgres.

## API Smoke Flow
`tests/test_api_smoke_flow.py` performs a register → login → onboarding → suggestion → portfolio flow using FastAPI TestClient.

## Notes
- External providers (market data/trading) are mocked/stubbed in code; suggestions use a simple deterministic service, so tests are stable.
