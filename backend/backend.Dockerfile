FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app \
    PORT=3004

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . $APP_HOME

WORKDIR $APP_HOME

RUN uv sync --frozen --no-dev

EXPOSE $PORT

CMD ["/app/.venv/bin/uvicorn", "main:app", "--port", "3004", "--host", "0.0.0.0"]