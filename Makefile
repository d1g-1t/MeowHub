COMPOSE = docker compose
MANAGE = $(COMPOSE) run --rm api python manage.py
MANAGE_EXEC = $(COMPOSE) exec -T api python manage.py

SHELL = sh

.PHONY: setup up down build logs migrate collectstatic createsuperuser shell stop test lint

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		SECRET=$$(cat /dev/urandom 2>/dev/null | tr -dc 'A-Za-z0-9' | head -c 50); \
		if [ -z "$$SECRET" ]; then \
			SECRET=$$(date +%s | sha256sum | head -c 50); \
		fi; \
		sed "s|replace-me|$${SECRET}|" .env > .env.tmp && mv .env.tmp .env; \
		echo ".env created with generated SECRET_KEY"; \
	fi
	$(COMPOSE) up -d --build
	$(MANAGE_EXEC) migrate

up:
	$(COMPOSE) up -d --build
	$(MANAGE_EXEC) migrate

build:
	$(COMPOSE) build

down:
	$(COMPOSE) down

stop:
	$(COMPOSE) stop

logs:
	$(COMPOSE) logs -f api

migrate:
	$(MANAGE) migrate

collectstatic:
	$(MANAGE) collectstatic --noinput

createsuperuser:
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

test:
	$(MANAGE) test

lint:
	$(MANAGE_EXEC) pip install ruff
	$(MANAGE_EXEC) ruff check backend/
