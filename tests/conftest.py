from collections.abc import AsyncGenerator

import pytest_asyncio
from app.database import Base, get_session
from app.main import app as main_app
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from tests.settings import (
    Urls,
    login_credentials_schema,
    login_credentials_schema2,
    register_user_schema,
    register_user_schema2,
    top_up_balance_schema,
    withdraw_balance_schema,
)

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture()
async def app() -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield main_app
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(app: FastAPI) -> AsyncGenerator:
    connection = await engine.connect()
    transaction = await connection.begin()
    session = Session(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(app: FastAPI, db_session: Session, mocker: MockerFixture) -> AsyncGenerator | TestClient:
    mocker.patch("app.routers.users.send_mail", return_value=True)

    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_session] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture
async def register_user(client: AsyncGenerator | TestClient) -> AsyncGenerator:
    response = client.post(
        Urls.register,
        json=register_user_schema,
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest_asyncio.fixture
async def another_user(client: AsyncGenerator | TestClient) -> AsyncGenerator:
    response = client.post(
        Urls.register,
        json=register_user_schema2,
    )
    assert response.status_code == status.HTTP_201_CREATED
    response = client.post(Urls.login, json=login_credentials_schema2)
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    response = client.post(Urls.create_balance)
    assert response.status_code == status.HTTP_201_CREATED
    client.headers.update({"Authorization": ""})


@pytest_asyncio.fixture
async def auth_client(register_user, client: AsyncGenerator | TestClient) -> AsyncGenerator | TestClient:
    response = client.post(Urls.login, json=login_credentials_schema)
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json().get("access_token")
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    yield client


@pytest_asyncio.fixture
async def create_balance(auth_client, mocker: MockerFixture) -> AsyncGenerator:
    response = auth_client.post(Urls.create_balance)
    assert response.status_code == status.HTTP_201_CREATED


@pytest_asyncio.fixture
async def create_transactions(auth_client, create_balance):
    response = auth_client.post(Urls.top_up_balance, json=top_up_balance_schema)
    assert response.status_code == status.HTTP_200_OK

    response = auth_client.post(Urls.withdraw_balance, json=withdraw_balance_schema)
    assert response.status_code == status.HTTP_200_OK
