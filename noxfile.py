import nox
from dotenv import load_dotenv


@nox.session
def format(session: nox.Session) -> None:
    session.install("ufmt", "black", "isort")
    session.run("ufmt", "format", "app", "tests")
    session.run("black", "--config=configs/.black.toml", "app", "tests")
    session.run(
        "isort",
        "--sp=configs/.isort.cfg",
        "app",
        "tests"
    )


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff", "flake8", "mypy")
    session.run(
        "ruff",
        "check",
        "--config=configs/.ruff.toml",
        "--fix",
        "app",
    )
    session.run("flake8", "--config=configs/.flake8", "app")
    session.run(
        "mypy",
        "--config-file=configs/.mypy.ini",
        "app"
    )


@nox.session
def run_tests(session: nox.Session) -> None:
    load_dotenv(dotenv_path="./.env.example")
    session.install("-r", "requirements.txt")
    session.run("pytest")


@nox.session
def coverage(session: nox.Session) -> None:
    load_dotenv(dotenv_path="./.env.example")
    session.install("-r", "requirements.txt")
    session.run("coverage", "run", "-m", "pytest")