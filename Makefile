export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up

build:
	docker-compose build

up:
	docker-compose up -d postgres

down:
	docker-compose down --remove-orphans --volumes

test:
	pytest

isort:
	poetry run isort .

black:
	poetry run black .

flake8:
	poetry run flake8 .

mypy:
	poetry run mypy --show-error-context --pretty -p food_r

food-r-app:
	poetry run food_r runserver 0.0.0.0:8000

make-migration:
	poetry run food_r makemigrations

migrate:
	poetry run food_r migrate

pre-commit: black flake8 mypy test
