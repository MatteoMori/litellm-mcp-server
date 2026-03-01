# https://docs.astral.sh/uv/guides/integration/docker/#compiling-bytecode
FROM python:3.14-alpine3.23
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
WORKDIR /app

# Disable development dependencies
ENV UV_NO_DEV=1
# Prevent Rich from wrapping log lines in Docker (no real terminal)
ENV COLUMNS=200


COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

COPY . /app
RUN uv sync --locked --no-dev --no-editable

CMD ["uv", "run", "--no-sync", "python", "./src/litellm_mcp_server/mcp_server.py"]
