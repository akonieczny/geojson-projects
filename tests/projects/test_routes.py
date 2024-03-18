import datetime
import json
import uuid
from pathlib import Path

import pytest
from fastapi import status
from starlette.testclient import TestClient


@pytest.fixture()
def request_body(geojson_filename: str) -> dict[str, str]:
    with open(Path(__file__).parent / "artifacts" / geojson_filename) as f:
        geojson = json.load(f)

    return {
        "name": "Test project",
        "description": "Description of the project",
        "start_date": (datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=5)).isoformat(),
        "end_date": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        "area": geojson,
    }


class TestGetAllProject:
    def test_success(
        self,
        api_client: TestClient,
    ) -> None:
        # given

        # when
        response = api_client.get("/projects/")

        # then
        assert response.status_code == status.HTTP_200_OK, response.content
        expected_projects_count = 4
        assert len(response.json()) == expected_projects_count, response.content


class TestGetProjectByPk:
    def test_success(
        self,
        api_client: TestClient,
    ) -> None:
        # given
        pk = uuid.uuid4()

        # when
        response = api_client.get(f"/projects/{pk}")

        # then
        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.json()["pk"] == str(pk), response.content


class TestCreateProject:
    @pytest.mark.parametrize(
        ("geojson_filename", "properties_value"),
        [
            ("correct_geojson.json", None),
            ("correct_geojson_with_properties.json", {"name": "Terra_de_meio.json"}),
        ],
    )
    def test_success(
        self,
        geojson_filename: str,  # noqa: ARG002
        properties_value: dict[str, str] | None,
        request_body: dict[str, str],
        api_client: TestClient,
    ) -> None:
        # given

        # when
        response = api_client.post("/projects/", json=request_body)

        # then
        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.json()["area"]["properties"] == properties_value, response.content

    @pytest.mark.parametrize(
        "geojson_filename",
        [
            "incorrect_geojson_missing_coordinates.json",
            "incorrect_geojson_missing_geometry_type.json",
            "incorrect_geojson_missing_type.json",
        ],
    )
    def test_missing_values_in_area(
        self,
        geojson_filename: str,  # noqa: ARG002
        request_body: dict[str, str],
        api_client: TestClient,
    ) -> None:
        # given

        # when
        response = api_client.post("/projects/", json=request_body)

        # then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.content

    @pytest.mark.parametrize(
        ("geojson_filename", "body_key"),
        [
            ("correct_geojson.json", "name"),
            ("correct_geojson.json", "description"),
            ("correct_geojson.json", "start_date"),
            ("correct_geojson.json", "end_date"),
            ("correct_geojson.json", "area"),
        ],
    )
    def test_missing_values_in_body(
        self,
        geojson_filename: str,  # noqa: ARG002
        body_key: str,
        request_body: dict[str, str],
        api_client: TestClient,
    ) -> None:
        # given
        del request_body[body_key]

        # when
        response = api_client.post("/projects/", json=request_body)

        # then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.content


class TestDeleteProject:
    def test_success(
        self,
        api_client: TestClient,
    ) -> None:
        # given
        pk = uuid.uuid4()

        # when
        response = api_client.delete(f"/projects/{pk}")

        # then
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content


class TestUpdateProject:
    @pytest.mark.parametrize(
        ("geojson_filename", "properties_value"),
        [
            ("correct_geojson.json", None),
            ("correct_geojson_with_properties.json", {"name": "Terra_de_meio.json"}),
        ],
    )
    def test_success(
        self,
        geojson_filename: str,  # noqa: ARG002
        properties_value: dict[str, str] | None,
        request_body: dict[str, str],
        api_client: TestClient,
    ) -> None:
        # given
        pk = uuid.uuid4()

        # when
        response = api_client.put(f"/projects/{pk}", json=request_body)

        # then
        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.json()["area"]["properties"] == properties_value, response.content

    @pytest.mark.parametrize(
        "geojson_filename",
        [
            "incorrect_geojson_missing_coordinates.json",
            "incorrect_geojson_missing_geometry_type.json",
            "incorrect_geojson_missing_type.json",
        ],
    )
    def test_missing_values_in_area(
        self,
        geojson_filename: str,  # noqa: ARG002
        request_body: dict[str, str],
        api_client: TestClient,
    ) -> None:
        # given
        pk = uuid.uuid4()

        # when
        response = api_client.put(f"/projects/{pk}", json=request_body)

        # then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.content

    @pytest.mark.parametrize(
        ("geojson_filename", "body_key"),
        [
            ("correct_geojson.json", "name"),
            ("correct_geojson.json", "description"),
            ("correct_geojson.json", "start_date"),
            ("correct_geojson.json", "end_date"),
            ("correct_geojson.json", "area"),
        ],
    )
    def test_missing_values_in_body(
        self,
        geojson_filename: str,  # noqa: ARG002
        body_key: str,
        request_body: dict[str, str],
        api_client: TestClient,
    ) -> None:
        # given
        pk = uuid.uuid4()
        del request_body[body_key]

        # when
        response = api_client.put(f"/projects/{pk}", json=request_body)

        # then
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.content
