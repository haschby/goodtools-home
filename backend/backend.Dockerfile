FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app \
    PORT=3004

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR $APP_HOME

# AVOID TO REINSTALL THE DEPENDENCIES IF THE pyproject.toml/uv.lock FILE HAS NOT CHANGED
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# COPY THE REST OF THE APPLICATION
COPY . $APP_HOME

EXPOSE $PORT

CMD ["/app/.venv/bin/uvicorn", "main:app", "--port", "3004", "--host", "0.0.0.0"]