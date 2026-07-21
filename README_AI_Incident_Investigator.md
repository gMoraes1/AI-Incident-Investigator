# AI Incident Investigator

## Visão Geral

O AI Incident Investigator é uma plataforma de observabilidade inteligente que auxilia equipes de engenharia na investigação de incidentes em aplicações distribuídas.

### Objetivo
Reduzir o tempo de investigação (MTTR) utilizando IA para correlacionar logs, identificar causas prováveis e sugerir ações corretivas.

## Arquitetura

Frontend (React)
-> FastAPI
-> Incident Service
-> Rules Engine + LLM (Ollama/Ll
ama)
-> PostgreSQL / OpenSearch / Redis

## Fluxo
1. Recebe logs via API.
2. Normaliza eventos.
3. Agrupa logs semelhantes.
4. Correlaciona serviços afetados.
5. Envia contexto ao LLM.
6. Gera causa raiz, severidade e recomendações.
7. Persiste incidente.
8. Exibe dashboard.

## Módulos
- Autenticação JWT
- Ingestão de Logs
- Correlação de Incidentes
- IA para análise
- Dashboard
- Notificações

## APIs
- POST /logs
- POST /incidents/analyze
- GET /incidents
- GET /incidents/{id}
- GET /metrics

## Banco
- users
- incidents
- log_entries
- ai_analysis
- services
- notifications

## Tecnologias
Backend: Python, FastAPI, SQLAlchemy, Alembic, Pydantic
Banco: PostgreSQL, Redis, OpenSearch/Elasticsearch
IA: Ollama + Llama 3
Infra: Docker, Docker Compose, Kubernetes
Observabilidade: Prometheus, Grafana
Qualidade: Pytest, Ruff, GitHub Actions

## Roadmap
MVP: upload de logs, agrupamento, IA, dashboard.
V2: Slack, Prometheus, correlação entre serviços.
V3: RAG com documentação, playbooks, análise preditiva.

## Diferenciais
Projeto inspirado em plataformas de observabilidade corporativas, utilizando IA para acelerar investigação de incidentes.