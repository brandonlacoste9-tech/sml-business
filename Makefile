.PHONY: help install test serve clean migrate reset

help:  ## Show this help message
	@echo "🐝 KimiClaw Business OS - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

install:  ## Install dependencies
	pip install -r requirements.txt
	pip install -e .

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=kimiclaw --cov-report=html --cov-report=term

serve:  ## Start the FastAPI server
	python -m kimiclaw.cli.main serve

dev:  ## Start server with auto-reload
	uvicorn kimiclaw.main:app --reload --host 0.0.0.0 --port 8000

migrate:  ## Initialize database
	python migrate.py init

seed:  ## Seed database with initial data
	python migrate.py seed

reset:  ## Reset database (WARNING: deletes all data)
	python migrate.py reset

status:  ## Show system status
	python -m kimiclaw.cli.main status

leads:  ## Run lead generation
	python -m kimiclaw.cli.main leads

clean:  ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

format:  ## Format code with black
	black kimiclaw/ tests/

lint:  ## Lint code with flake8
	flake8 kimiclaw/ tests/ --max-line-length=100

docker-up:  ## Start Docker services (PostgreSQL, Redis)
	docker-compose up -d

docker-down:  ## Stop Docker services
	docker-compose down

docker-logs:  ## View Docker logs
	docker-compose logs -f

all: install migrate seed  ## Install, migrate, and seed
