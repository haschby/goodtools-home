PORT ?= 2223

migrate:
	alembic revision --autogenerate -m "$(message)"

migrate-upgrade:
	alembic upgrade head

migrate-downgrade:
	alembic downgrade -1

migrate-history:
	alembic history

run-app: 
	uv run uvicorn main:app --reload --port $(PORT)