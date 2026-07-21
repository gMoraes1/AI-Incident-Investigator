# AI Incident Investigator

Intelligent observability platform that helps engineering teams investigate incidents
in distributed applications. It ingests logs, correlates related events, and uses an
LLM (with a deterministic rules-engine fallback) to propose a probable root cause,
severity and corrective actions — reducing MTTR.

> Product specification: [README_AI_Incident_Investigator.md](README_AI_Incident_Investigator.md)

## Architecture

```
React (SPA)  ──►  FastAPI  ──►  Incident Service  ──►  Rules Engine + LLM (Ollama/Llama 3)
                                        │
                                        ▼
                        PostgreSQL · Redis · OpenSearch
```

The investigation pipeline: ingest logs → normalize events → group similar events
→ correlate affected services → send context to the LLM → produce root cause,
severity and recommendations → persist incident → surface in the dashboard.

## Project layout

```
backend/     FastAPI service (Python 3.12, SQLAlchemy async, Alembic)
frontend/    React + TypeScript SPA (Vite)
docker-compose.yml   Full local stack
Makefile     Common developer tasks
```

## Quickstart (Docker)

```bash
docker compose up --build
# API   → http://localhost:8000/docs
# App   → http://localhost:5173
```

Pull the LLM model once the stack is up:

```bash
docker compose exec ollama ollama pull llama3
```

## Local development

Backend:

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API

| Method | Path                          | Description                          |
| ------ | ----------------------------- | ------------------------------------ |
| POST   | `/api/v1/auth/register`       | Create an account                    |
| POST   | `/api/v1/auth/login`          | Obtain a JWT access token            |
| POST   | `/api/v1/logs`                | Ingest a batch of logs               |
| POST   | `/api/v1/incidents/analyze`   | Analyze logs and open an incident    |
| GET    | `/api/v1/incidents`           | List incidents (paginated)           |
| GET    | `/api/v1/incidents/{id}`      | Incident detail with AI analysis     |
| GET    | `/api/v1/metrics`             | Dashboard metrics overview           |

## Testing & quality

```bash
make test    # backend tests
make lint    # backend + frontend lint
```
