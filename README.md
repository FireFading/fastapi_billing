## features
- JWT-authentication
> ***


## setup
- in env.example all variables used in project, change it to .env, several variables that are common, already define as example, secret variables is empty

## run project
- `docker compose up --build` OR `make build` - first time
- `docker compose up` OR `make up` - run without building, also you can prove -d flag to run as daemon

## down docker
- `docker compose down && docker network prune --force` OR `make down`

## database
- connect to postgres: `docker exec -it postgres psql -U postgres`

## migrations
- run docker containers by commands in "run project" section
- connect to docker container: `docker exec -it fastapi bash`
- apply migrations: `alembic upgrade head` in fastapi container
- create new migrations: `alembic revision --autogenerate -m "<migration name>"` in fastapi container
> ***

## formatting and linting
- run ufmt: `ufmt format .`
- run black: `black --config=configs/.black.toml app`
- run ruff: `ruff check --config=configs/.ruff.toml --fix app`
- run flake8: `flake8 --config=configs/.flake8 app`

- OR `nox` in root

## run tests
- `pytest .` OR `pytest ./tests` OR run `nox`
