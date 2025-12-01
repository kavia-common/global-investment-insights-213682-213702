# Backend-Frontend-DB Integration Summary

- Database: investment_database (PostgreSQL via startup.sh)
- Backend: investment_api_backend (FastAPI)
  - CORS: BACKEND_CORS_ORIGINS must include the frontend origin
  - DB: Use POSTGRES_URL or discrete env vars
  - OpenAPI: python -m src.api.generate_openAPI (outputs interfaces/openapi.json)
- Frontend: investment_web_frontend (React)
  - REACT_APP_API_BASE_URL should point to backend base URL

See:
- investment_api_backend/README-INTEGRATION.md
- investment_web_frontend/README-INTEGRATION-FINAL.md
- investment_database/README.md
- global-investment-insights-213682-213700/INTEGRATION-CHECKLIST.md
