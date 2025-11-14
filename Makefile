COMPOSE = docker compose

.PHONY: up down build logs migrate collectstatic createsuperuser shell stop

up:
	$(COMPOSE) up -d --build

build:
	$(COMPOSE) build

down:
	$(COMPOSE) down

stop:
	$(COMPOSE) stop

logs:
	$(COMPOSE) logs -f api

migrate:
	$(COMPOSE) run --rm api uv run python manage.py migrate

collectstatic:
	$(COMPOSE) run --rm api uv run python manage.py collectstatic --noinput

createsuperuser:
	$(COMPOSE) run --rm api uv run python manage.py createsuperuser

shell:
	$(COMPOSE) run --rm api uv run python manage.py shell
