.PHONY: help install dev build test lint format docker-up docker-down docker-rebuild clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies (backend + frontend)
	uv sync --locked
	cd client && npm install

dev: ## Start backend dev server
	uv run uvicorn main:app --reload

dev-frontend: ## Start frontend dev server
	cd client && npm run dev

build: ## Build frontend for production
	cd client && npm run build

test: ## Run backend tests
	uv run pytest tests/

lint: ## Run ruff linter and format check
	uv run ruff check .
	uv run ruff format --check .

lint-fix: ## Run ruff linter with auto-fix
	uv run ruff check --fix .

format: ## Format Python code with ruff
	uv run ruff format .

clean: ## Remove build artifacts and caches
	rm -rf __pycache__ .pytest_cache .coverage htmlcov client_build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-up: ## Start all services with Docker Compose
	docker compose up -d

docker-down: ## Stop all Docker Compose services
	docker compose down

docker-rebuild: ## Rebuild and start all services
	docker compose up --build -d

docker-logs: ## Follow Docker Compose logs
	docker compose logs -f
