# PurpleWatch API

FastAPI backend for PurpleWatch.

## PW-501 — FastAPI Backend Foundation

This foundation provides:

- a minimal stateless FastAPI application;
- environment-based configuration;
- a deterministic `GET /health` endpoint;
- automated backend tests;
- CI coverage for backend tests;
- a base for future PostgreSQL and Wazuh adapters.

## Requirements

- Python 3.12+
- `venv`
- `pip`

## Local setup

From the repository root:

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run the API

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "purplewatch-api",
  "version": "0.1.0",
  "environment": "development"
}
```

## Tests

```bash
pytest -ra
```

## Configuration

PurpleWatch API environment variables use the `PURPLEWATCH_` prefix.

A non-secret example is provided in `.env.example`.

The local `.env` file is ignored by Git. Never commit passwords, tokens, Wazuh credentials, PostgreSQL credentials, API keys, or other secrets.

## Security boundaries

PW-501 does not provide arbitrary command execution or remote execution against lab endpoints.

Future PostgreSQL and Wazuh integrations must be implemented behind dedicated adapters rather than directly inside route handlers.

The development server is bound to `127.0.0.1` by default in the documented command.

## Out of scope for PW-501

This phase does not yet implement:

- PostgreSQL persistence;
- Wazuh integration;
- validation business routes;
- frontend functionality.
