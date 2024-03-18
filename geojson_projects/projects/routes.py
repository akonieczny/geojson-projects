import datetime
import uuid
from uuid import UUID

import geojson_pydantic as geojson
from fastapi import APIRouter, status

from geojson_projects.projects.schemas import ProjectCreateSchema, ProjectOutputSchema, ProjectUpdateSchema

router = APIRouter(prefix="/projects")


def project_output(pk: UUID) -> ProjectOutputSchema:
    geojson_content = {
        "type": "Feature",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-52.8430645648562, -5.63351005831322],
                        [-52.797327415758296, -5.654301057317909],
                        [-52.719404865443295, -5.626204935899693],
                        [-52.8430645648562, -5.63351005831322],
                    ]
                ]
            ],
        },
        "properties": None,
    }

    return ProjectOutputSchema(
        pk=pk,
        name="Test project",
        description="Description of the project",
        start_date=datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=5),
        end_date=datetime.datetime.now(tz=datetime.UTC),
        area=geojson.Feature(**geojson_content),  # type: ignore[arg-type]
    )


@router.get("/")
def get_all() -> list[ProjectOutputSchema]:
    return [
        project_output(uuid.uuid4()),
        project_output(uuid.uuid4()),
        project_output(uuid.uuid4()),
        project_output(uuid.uuid4()),
    ]


@router.get("/{pk}")
def get_by_pk(pk: UUID) -> ProjectOutputSchema:
    return project_output(pk)


@router.post("/")
def create(project: ProjectCreateSchema) -> ProjectOutputSchema:
    pk = uuid.uuid4()
    return ProjectOutputSchema(pk=pk, **project.dict())


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_pk(pk: UUID) -> None:  # noqa: ARG001
    pass


@router.put("/{pk}")
def update_by_pk(pk: UUID, project: ProjectUpdateSchema) -> ProjectOutputSchema:
    return ProjectOutputSchema(pk=pk, **project.dict())
