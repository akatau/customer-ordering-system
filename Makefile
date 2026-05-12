# Makefile for Customer Ordering Sub-system

.PHONY: help install install-backend install-frontend dev dev-backend dev-frontend test test-backend test-frontend lint lint-backend lint-frontend format format-backend format-frontend build build-backend build-frontend clean docker-up docker-down migrate migrate-up migrate-down db-reset

# Default target
help:
	@echo "Available commands:"
	@echo "  install          - Install all dependencies"
	@echo "  install-backend  - Install Python dependencies"
	@echo "  install-frontend - Install Node.js dependencies"
	@echo "  dev              - Start all development servers"
	@echo "  dev-backend      - Start backend development server"
	@echo "  dev-frontend     - Start frontend development server"
	@echo "  test             - Run all tests"
	@echo "  test-backend     - Run backend tests"
	@echo "  test-frontend    - Run frontend tests"
	@echo "  lint             - Run all linters"
	@echo "  lint-backend     - Run Python linters"
	@echo "  lint-frontend    - Run TypeScript linters"
	@echo "  format           - Format all code"
	@echo "  format-backend   - Format Python code"
	@echo "  format-frontend  - Format TypeScript code"
	@echo "  build            - Build all components"
	@echo "  build-backend    - Build backend container"
	@echo "  build-frontend   - Build frontend"
	@echo "  clean            - Clean build artifacts"
	@echo "  docker-up        - Start all services with Docker"
	@echo "  docker-down      - Stop all Docker services"
	@echo "  migrate          - Run database migrations"
	@echo "  migrate-up       - Upgrade database to latest migration"
	@echo "  migrate-down     - Downgrade database by one migration"
	@echo "  db-reset         - Reset database (WARNING: destroys data)"

# Installation
install: install-backend install-frontend

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && yarn install

# Development
dev:
	@echo "Starting all development servers..."
	@make -j2 dev-backend dev-frontend

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && yarn dev

# Testing
test: test-backend test-frontend

test-backend:
	cd backend && pytest -v --cov=app --cov-report=html --cov-report=term

test-frontend:
	cd frontend && yarn test --coverage --watchAll=false

# Linting
lint: lint-backend lint-frontend

lint-backend:
	cd backend && flake8 app tests && mypy app

lint-frontend:
	cd frontend && yarn lint

# Formatting
format: format-backend format-frontend

format-backend:
	cd backend && black app tests && isort app tests

format-frontend:
	cd frontend && yarn format

# Building
build: build-backend build-frontend

build-backend:
	docker build -t customer-ordering-backend:latest backend/

build-frontend:
	cd frontend && yarn build

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name node_modules -prune -exec rm -rf {} +
	find . -type d -name .next -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".coverage" -delete
	find . -name "coverage.xml" -delete

# Docker
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Database
migrate:
	cd backend && alembic revision --autogenerate -m "$(msg)"

migrate-up:
	cd backend && alembic upgrade head

migrate-down:
	cd backend && alembic downgrade -1

db-reset:
	@echo "WARNING: This will destroy all data in the database!"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		cd backend && alembic downgrade base; \
	else \
		echo "Aborted."; \
	fi

# Development setup
setup-dev:
	@echo "Setting up development environment..."
	@make install
	@make docker-up
	@sleep 10
	@make migrate-up
	@echo "Development environment ready!"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"

# Production deployment (example)
deploy:
	@echo "Deploying to production..."
	@make build
	@echo "Push images to registry..."
	@echo "Update Kubernetes manifests..."
	@echo "Deploy to cluster..."
	@echo "Run migrations..."
	@echo "Update load balancer..."
	@echo "Deployment complete!"

# Health checks
health-check:
	@echo "Checking backend health..."
	@curl -f http://localhost:8000/health || echo "Backend not healthy"
	@echo "Checking frontend health..."
	@curl -f http://localhost:3000 || echo "Frontend not healthy"

# Logs
logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f db

# Database shell
db-shell:
	docker-compose exec db psql -U postgres -d customer_ordering_dev
