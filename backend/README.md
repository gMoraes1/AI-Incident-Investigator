# AI Incident Investigator — Backend

FastAPI service that ingests logs, correlates events, runs LLM-assisted root-cause
analysis and exposes incidents through a REST API.

## Stack

- Python 3.12, FastAPI, SQLAlchemy 2.0 (async), Alembic
- PostgreSQL, Redis, OpenSearch
- Ollama (Llama 3) for LLM analysis, with a deterministic rules-engine fallback

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env

alembic revision --autogenerate -m "initial schema"
alembic upgrade head

uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

## Tests

```bash
pytest
ruff check .
```

## Layout

```
app/
  api/        HTTP layer (routers, dependencies)
  core/       Config, database, security, redis
  models/     SQLAlchemy ORM models
  schemas/    Pydantic request/response models
  services/   Business logic (ingestion, correlation, AI, notifications)
```
