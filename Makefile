build:
	docker compose up --build

daemon:
	docker compose up --build -d

up:
	docker compose up

down:
	docker compose down -v && docker network prune --force

postgres:
	docker exec -it postgres psql -U postgres

fastapi:
	docker exec -it fastapi bash

makemigrations:
	docker exec -it fastapi alembic revision --autogenerate -m "<migration name>"

migrate:
	docker exec -it fastapi alembic upgrade head