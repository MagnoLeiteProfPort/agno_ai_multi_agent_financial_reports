.PHONY: dev run fmt lint test
dev:
	python -m venv .venv && . .venv/Scripts/activate || . .venv/bin/activate && pip install -U pip && pip install -e .
fmt:
	ruff check --fix .
lint:
	ruff check . && mypy agents core apps tools
run:
	uvicorn apps.api.main:app --reload
test:
	pytest -q

web:
	python apps/web/manage.py migrate && python apps/web/manage.py runserver 9000
