COMPOSE = docker compose
MANAGE = $(COMPOSE) run --rm api python manage.py
MANAGE_EXEC = $(COMPOSE) exec -T api python manage.py

.PHONY: setup up down build logs migrate collectstatic createsuperuser shell stop test lint

setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		openssl rand -base64 48 > /dev/null 2>&1 && \
		sed -i "s/replace-me/$$(openssl rand -base64 48 | tr -d '\n')/" .env || \
		python -c "import secrets; d=open('.env').read(); open('.env','w').write(d.replace('replace-me',secrets.token_urlsafe(50)))"; \
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
