# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                                  # Install dependencies
uv run uvicorn main:app --reload         # Start dev server with hot reload
```

No test suite is configured.

## Architecture

Fjorden is a ferry schedule viewer for the Mortavika–Arsvågen route in Norway. It is a minimal full-stack app:

- **[main.py](main.py)** — FastAPI backend that acts as a proxy for the [Entur GraphQL Journey Planner API](https://api.entur.io/journey-planner/v3/graphql). It loads GraphQL queries from [graphql-queries/](graphql-queries/), posts them to Entur, and exposes a single endpoint: `GET /api/departures/{route_key}` where `route_key` is either `mor-ars` or `ars-mor`. It also serves the frontend via `StaticFiles`.

- **[static/index.html](static/index.html)** — Vanilla JS single-page app. Polls the backend every 60 seconds and renders two departure boards (one per direction). No build step required.

- **[graphql-queries/](graphql-queries/)** — Contains the two named GraphQL queries (one per direction). These are read from disk at startup and cached in memory.

## Deployment

Hosted on [Railway](https://fjorden-production.up.railway.app/). The [Procfile](Procfile) defines the production start command:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Railway injects the `$PORT` environment variable automatically.
