import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from geojson_projects.app import app


@pytest.fixture()
def test_app() -> FastAPI:
    return app


@pytest.fixture()
def api_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)
