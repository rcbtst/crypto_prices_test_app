FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

RUN chmod +x /app/start.sh

RUN chown -R app:app /app

USER app

CMD ["./start.sh"]
