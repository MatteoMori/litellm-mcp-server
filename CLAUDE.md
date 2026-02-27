# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python MCP (Model Context Protocol) server that exposes **read-only tools** for querying a [LiteLLM proxy](https://docs.litellm.ai/). AI agents use these tools to gather information from a LiteLLM proxy instance. Changes to the proxy itself should be made via the proxy's `config.yaml`.

## Tech Stack

- **Python 3.10+** managed with **uv**
- **FastMCP 3.0.2** — MCP server framework
- **httpx** — HTTP client with retry transport (3 retries, 30s timeout)
- **pydantic-settings** + **python-dotenv** — env-based config from `.env`

## Development Setup

```bash
uv sync
```

**Environment variables** (see `.env.example`):
- `LITELLM_BASE_URL` — proxy URL (e.g. `http://localhost:8081`)
- `LITELLM_API_KEY` — admin/master API key
- `MCP_SERVER_LOGGING_LEVEL` — log level (default: `INFO`)
- `MCP_SERVER_PORT` — port the MCP server listens on (default: `8000`)
- `MCP_SERVER_VERSION` — server version string (default: `development`)

## Running the Server

```bash
# Locally via uv (preferred for development)
make run
# which runs: uv run python ./src/litellm_mcp_server/mcp_server.py

# Docker
make docker-build
make docker-run

# Kubernetes (KIND cluster)
make deploy
```

## Architecture

### Request flow

```
Agent → FastMCP (mcp_server.py) → @mcp.tool handler (tools/*.py) → httpx client (http_client.py) → LiteLLM Proxy
```

### Key modules

- **`mcp_server.py`** — Entry point. Configures logging, imports `tools/` to trigger `@mcp.tool` registration, then runs the server on `MCP_SERVER_PORT` with HTTP transport.
- **`mcp_instance.py`** — Creates the single `FastMCP` instance that all tools register against.
- **`http_client.py`** — Shared `httpx.Client` with base URL, Bearer auth, 30s timeout, and 3-retry transport. All tools and helpers import `http` from here.
- **`config.py`** — Loads `.env` via `python-dotenv` and exports a `SysEnv` dict.
- **`helpers.py`** — Internal lookup helpers (NOT MCP tools). Provides `fetch_X_lookup()` functions that return `{id: name}` dicts for enriching tool responses. Results are cached for 5 minutes via `_cached_fetch()`.
- **`tools/__init__.py`** — Wildcard-imports all tool modules so their `@mcp.tool` decorators fire on import.

### Adding a new tool

1. Create `src/litellm_mcp_server/tools/your_tool.py`
2. Import `mcp` from `mcp_instance` and `http` from `http_client`
3. Decorate your function with `@mcp.tool`
4. Add `from .your_tool import *` to `tools/__init__.py`

### ID enrichment pattern

Tools return raw UUIDs from LiteLLM (team_id, user_id). To make responses human-readable:
1. Add a `fetch_X_lookup()` in `helpers.py` that returns `{id: name}`
2. Call it from your tool after fetching data, enrich each record
3. Use `.get(id, id)` to fall back to the raw ID if lookup misses

The lookup helpers use `_cached_fetch()` with a 5-minute TTL so multiple tools calling the same lookup don't hammer the proxy.

### Pagination pattern

Tools that list entities (`get_users_list`, `get_keys_list`) paginate with `page`/`page_size` params and accumulate results until `page >= total_pages`.

## Deployment

### Docker

```bash
make docker-build   # builds litellm-mcp-server:latest
make docker-run     # runs on port 8000
```

The Dockerfile uses `python:3.14-alpine` with `uv` for dependency management.

### Kubernetes

Manifests live in `kube/`. The Makefile `deploy` target builds the image, loads it into a KIND cluster named `homelab`, and applies all manifests.

```bash
make deploy
```

Copy `kube/secret.yaml.example` → `kube/secret.yaml` and fill in credentials before deploying.

## API Documentation

Detailed LiteLLM endpoint docs (parameters, response shapes) are in `docs/`. Reference these when adding or modifying tools.
