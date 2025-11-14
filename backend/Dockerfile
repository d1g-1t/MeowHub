FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENV=/app/.venv \
    PYTHONPATH=/app/backend

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
RUN uv sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY backend/manage.py ./manage.py
COPY backend ./backend

CMD ["uv", "run", "gunicorn", "meowhub_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
