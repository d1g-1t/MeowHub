COMPOSE = docker compose

.PHONY: setup up down build logs migrate collectstatic createsuperuser shell stop test

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		python -c "import secrets; import sys; data=sys.stdin.read(); print(data.replace('replace-me', secrets.token_urlsafe(50)))" < .env > .env.tmp && mv .env.tmp .env; \
		echo ".env created with generated SECRET_KEY"; \
	fi
	$(COMPOSE) up -d --build
	$(COMPOSE) exec -T api uv run python manage.py migrate

up:
	$(COMPOSE) up -d --build
	$(COMPOSE) exec -T api uv run python manage.py migrate

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

test:
	$(COMPOSE) run --rm api uv run python manage.py test
