# -------------------------------------------------------------------------------------------------
# Introspection targets
# -------------------------------------------------------------------------------------------------

.PHONY: help
help: targets

.PHONY: targets
targets:
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@echo "\033[34mAvailable Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-24s\033[0m %s\n", $$1, $$2}'
	@echo ""

# -------------------------------------------------------------------------------------------------
# Development targets
# -------------------------------------------------------------------------------------------------

.PHONY: install
install: ## Install dependencies
	poetry install

.PHONY: lock
lock: ## Update lock file
	poetry lock --no-update

.PHONY: run
run: start ## Run the server (alias for start)

.PHONY: start
start: ## Starts the server
	$(eval include .env)
	$(eval export $(sh sed 's/=.*//' .env))

	poetry run uvicorn src.server:app --port 9095 --reload

# -------------------------------------------------------------------------------------------------
# Linting and Formatting
# -------------------------------------------------------------------------------------------------

.PHONY: check
check: check-format lint ## Run all checks (format + lint)

.PHONY: check-format
check-format: ## Dry-run code formatter
	poetry run black ./ --check
	poetry run isort ./ --profile black --check

.PHONY: lint
lint: ## Run linter
	poetry run pylint ./api ./app ./core
 
.PHONY: format
format: ## Run code formatter
	poetry run black ./
	poetry run isort ./ --profile black

.PHONY: check-lockfile
check-lockfile: ## Compares lock file with pyproject.toml
	poetry lock --check

# -------------------------------------------------------------------------------------------------
# Database targets
# -------------------------------------------------------------------------------------------------

.PHONY: db-init
db-init: ## Initialize database tables using Alembic migrations
	alembic upgrade head

.PHONY: db-reset
db-reset: ## Reset database (drop all tables and recreate using migrations)
	@echo "⚠️  WARNING: This will drop all tables and data!"
	@read -p "Are you sure? Type 'yes' to continue: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo "Dropping all tables..."; \
		poetry run python -c "from src.core.database.init import drop_tables; drop_tables()"; \
		echo "Recreating tables using migrations..."; \
		alembic upgrade head; \
		echo "Database reset complete."; \
	else \
		echo "Database reset cancelled."; \
	fi

.PHONY: db-reset-all
db-reset-all: ## Complete reset: delete migrations, drop tables, create new schema and migration
	@echo "⚠️  WARNING: This will completely reset the database and migrations!"
	@echo "This will:"
	@echo "  1. Delete all migration versions"
	@echo "  2. Drop all tables and data"
	@echo "  3. Create new initial migration"
	@echo "  4. Apply the new migration"
	@read -p "Are you sure? Type 'yes' to continue: " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		echo "Deleting all migration versions..."; \
		rm -rf src/core/database/migrations/versions/*; \
		echo "Dropping all tables..."; \
		poetry run python -c "from src.core.database.init import drop_tables; drop_tables()"; \
		echo "Creating new initial migration..."; \
		alembic revision --autogenerate -m "Initial migration"; \
		echo "Applying new migration..."; \
		alembic upgrade head; \
		echo "Complete database reset finished."; \
	else \
		echo "Complete database reset cancelled."; \
	fi

.PHONY: db-migrate
db-migrate: ## Generate a new migration
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

.PHONY: db-upgrade
db-upgrade: ## Apply all pending migrations
	alembic upgrade head

.PHONY: db-downgrade
db-downgrade: ## Rollback one migration
	alembic downgrade -1

.PHONY: db-current
db-current: ## Show current migration version
	alembic current

.PHONY: db-history
db-history: ## Show migration history
	alembic history

.PHONY: db-stamp
db-stamp: ## Mark database as up-to-date with current migration
	alembic stamp head

.PHONY: db-check
db-check: ## Check if database is up to date with migrations
	alembic check

.PHONY: db-show
db-show: ## Show pending migrations
	alembic show head

.PHONY: db-help
db-help: ## Show all available database commands
	@echo "Available database commands:"
	@echo "  make db-init      - Initialize database using migrations"
	@echo "  make db-reset     - Reset database (drop and recreate)"
	@echo "  make db-reset-all - Complete reset (delete migrations, drop tables, recreate)"
	@echo "  make db-migrate   - Generate new migration"
	@echo "  make db-upgrade   - Apply pending migrations"
	@echo "  make db-downgrade - Rollback one migration"
	@echo "  make db-current   - Show current migration version"
	@echo "  make db-history   - Show migration history"
	@echo "  make db-stamp     - Mark database as up-to-date"
	@echo "  make db-check     - Check if database is up to date"
	@echo "  make db-show      - Show pending migrations"

reset-migrations:
	@echo "Deleting and re-initializing Alembic migrations..."
	rm -rf src/core/database/migrations
	$(ALEMBIC) init src/core/database/migrations
	@echo "Restoring custom env.py logic..."
	cp env.py.bak src/core/database/migrations/env.py || true

migrate:
	@echo "Generating and applying Alembic migrations..."
	$(ALEMBIC) revision --autogenerate -m "Initial migration with UUID IDs"
	$(ALEMBIC) upgrade head

# -------------------------------------------------------------------------------------------------
# Testing targets
# -------------------------------------------------------------------------------------------------

.PHONY: test
test: ## Run tests
	poetry run pytest

.PHONY: test-coverage
test-coverage: ## Run tests with coverage
	poetry run pytest --cov=src