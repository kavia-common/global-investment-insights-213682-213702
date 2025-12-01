#!/bin/bash
cd /home/kavia/workspace/code-generation/global-investment-insights-213682-213702/investment_api_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

