# Makefile

# Variables
MANAGE = docker compose -f local.yml run --rm django python manage.py

# Commands
up:
	docker compose -f local.yml up

down:
	docker compose -f local.yml down

down-v:
	docker compose -f local.yml down -v

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

test:
	docker-compose -f local.yml run --rm django coverage run -m pytest

shell:
	$(MANAGE) shell_plus

superuser:
	$(MANAGE) createsuperuser

precommit:
	pre-commit run --all-files

show:
	docker compose -f local.yml ps

stop django:
	docker rm -f c_ride_local_django

start django:
	docker-compose -f local.yml run --rm --service-ports django

.PHONY: run migrate test shell superuser
