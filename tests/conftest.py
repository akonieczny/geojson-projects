import contextlib
import time
from collections.abc import Generator

import pytest
import sqlalchemy as sa
import sqlalchemy_utils as sa_utils
from fastapi import FastAPI
from pytest_postgresql import factories
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from geojson_projects import settings
from geojson_projects.app import app
from geojson_projects.database import sqlalchemy_metadata
from geojson_projects.dependencies import get_db_session
from tests.consts import TEST_DB, TEST_DB_URL
from tests.factories.base import SessionRegistry

postgresql_noproc = factories.postgresql_noproc(
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    dbname=TEST_DB,
)

postgresql = factories.postgresql("postgresql_noproc")


@pytest.fixture()
def test_engine(postgresql: Connection) -> Generator[Engine, None, None]:
    with contextlib.suppress(ProgrammingError):
        sa_utils.drop_database(TEST_DB_URL)
        time.sleep(0.05)

    sa_utils.create_database(TEST_DB_URL)
    cursor = postgresql.cursor()  # type: ignore[attr-defined]

    engine = sa.create_engine(TEST_DB_URL)
    sqlalchemy_metadata.create_all(engine)
    yield engine
    cursor.close()


@pytest.fixture()
def test_db_session(test_engine: Engine) -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        SessionRegistry.session = session
        yield session


@pytest.fixture()
def test_app(test_db_session: Session) -> Generator[FastAPI, None, None]:
    app.dependency_overrides[get_db_session] = lambda: test_db_session
    yield app
    app.dependency_overrides.clear()


@pytest.fixture()
def api_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)
