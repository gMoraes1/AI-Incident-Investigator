.PHONY: help up down logs backend frontend test lint migrate

help:
	@echo "Targets:"
	@echo "  up        Start the full stack with docker compose"
	@echo "  down      Stop the stack"
	@echo "  logs      Tail all service logs"
	@echo "  backend   Run the backend locally (reload)"
	@echo "  frontend  Run the frontend dev server"
	@echo "  test      Run backend tests"
	@echo "  lint      Lint backend and frontend"
	@echo "  migrate   Apply database migrations"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest

lint:
	cd backend && ruff check app tests
	cd frontend && npm run lint

migrate:
	cd backend && alembic upgrade head
