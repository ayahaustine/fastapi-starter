.PHONY: help install dev-install run test lint format type-check pre-commit-install pre-commit-run clean migrate upgrade downgrade revision db-reset setup-git release auto-release semver changelog

APP=app.main:app
PORT=8000

help:
	@echo "Available commands:"
	@echo "  make install            Install dependencies"
	@echo "  make dev-install        Install dev dependencies + pre-commit hooks"
	@echo "  make setup-git          Setup git commit template"
	@echo "  make run                Run FastAPI app (dev)"
	@echo "  make test               Run tests"
	@echo "  make clean              Remove temporary files"
	@echo "  make lint               Run linters"
	@echo "  make format             Auto-format code"
	@echo "  make type-check         Run type checking with mypy"
	@echo "  make pre-commit-install Install pre-commit hooks"
	@echo "  make pre-commit-run     Run pre-commit on all files"
	@echo "  make semver             Calculate next version from commits"
	@echo "  make auto-release       Create release with automatic version"
	@echo "  make release            Create a new release (provide VERSION=x.y.z)"
	@echo "  make changelog          Generate changelog"
	@echo "  make revision           Create new migration"
	@echo "  make upgrade            Apply migrations"
	@echo "  make downgrade          Roll back last migration"
	@echo "  make db-reset           Reset database (DANGEROUS)"

install:
	pip install -e .

	@echo "✅ Development environment setup complete!"
	@echo "💡 Run 'make setup-git' to configure git commit template"

setup-git:
	git config --local commit.template .gitmessage
	@echo "✅ Git commit template configured!"
	@echo "📝 Use 'git commit' to see the template"
dev-install:
	pip install -e ".[dev]"
	pre-commit install

run:
	uvicorn $(APP) --reload --port $(PORT)

test:
	pytest -v

type-check:
	mypy app/ --ignore-missing-imports

lint:
	ruff check .

format:
	ruff format .
	ruff check . --fix

semver:
	@python3 scripts/semver.py

auto-release:
	@./scripts/auto-release.sh

release:
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Error: VERSION is required. Usage: make release VERSION=1.0.0"; \
		exit 1; \
	fi
	@echo "🚀 Creating release v$(VERSION)..."
	@git tag -a "v$(VERSION)" -m "Release v$(VERSION)"
	@git push origin "v$(VERSION)"
	@echo "✅ Release v$(VERSION) created and pushed!"
	@echo "📝 GitHub Actions will automatically generate release notes"

changelog:
	@echo "📝 Generating changelog..."
	@if command -v git-chglog >/dev/null 2>&1; then \
		git-chglog -o CHANGELOG.md; \
		echo "✅ Changelog generated!"; \
	else \
		echo "⚠️  git-chglog not installed. Install with: brew install git-chglog"; \
		echo "📖 Manual changelog update recommended"; \
	fi


pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/

revision:
	poetry run alembic revision --autogenerate -m "$(msg)"

upgrade:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

db-reset:
	rm -f dev.db
	poetry run alembic upgrade head

create-module:
	@read -p "Enter module name: " name; \
	poetry run python scripts/create_module.py "$$name"
