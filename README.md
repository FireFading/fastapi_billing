## Features
- JWT-authentication
- topup user balance
### soon
- watch user balance
- withdraw money from balance
- watch all transactions
- transfer to another account
- all features test with `pytest`

## Installation
- in env.example all variables used in project, change it to .env, several variables that are common, already define as example, secret variables is empty

## Run Locally
```bash
  docker compose up --build
```
OR `make build` - first time
```bash
  docker compose up
```
OR `make up` - run without building, also you can prove -d flag to run as daemon

## Down docker
```bash
  docker compose down && docker network prune --force
```
OR `make down`

## Database
- connect to postgres
```bash
  docker exec -it postgres psql -U postgres
```

## Migrations
- run docker containers
- connect to docker container
```bash
  docker exec -it fastapi bash
```
- apply migrations in fastapi container
```bash
  alembic upgrade head
``` 
- create new migrations in fastapi container
```bash
  alembic revision --autogenerate -m "<migration name>"
```

> ***

## formatting and linting
- run ufmt: `ufmt format .`
- run black: `black --config=configs/.black.toml app`
- run ruff: `ruff check --config=configs/.ruff.toml --fix app`
- run flake8: `flake8 --config=configs/.flake8 app`

- OR `nox` in root

## run tests
- `pytest .` OR `pytest ./tests` OR run `nox`
