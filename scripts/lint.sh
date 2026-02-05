#!/bin/bash

# Exit on error
set -e

echo "Running linters and formatters..."
echo ""

# Ruff check (linting)
echo "Running Ruff linter..."
ruff check . --fix

# Ruff format (formatting)
echo "Running Ruff formatter..."
ruff format .

# MyPy type checking
echo "Running MyPy type checker..."
mypy app/ --ignore-missing-imports

echo ""
echo "✅ All checks passed!"
