import datetime
import uuid
from typing import Annotated
from uuid import UUID

import geojson_pydantic as geojson
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from geojson_projects.dependencies import get_db_session
from geojson_projects.projects.models import Project
from geojson_projects.projects.repositories import ProjectRepository
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
def get_all(session: Annotated[Session, Depends(get_db_session)]) -> list[ProjectOutputSchema]:
    project_repository = ProjectRepository(session)
    instances = project_repository.get_all()

    return [ProjectOutputSchema.model_validate(instance) for instance in instances]


@router.get("/{pk}")
def get_by_pk(pk: UUID, session: Annotated[Session, Depends(get_db_session)]) -> ProjectOutputSchema:
    project_repository = ProjectRepository(session)

    instance = project_repository.get_by_pk(pk)

    return ProjectOutputSchema.model_validate(instance)


@router.post("/")
def create(project: ProjectCreateSchema, session: Annotated[Session, Depends(get_db_session)]) -> ProjectOutputSchema:
    project_repository = ProjectRepository(session)

    instance = Project(pk=uuid.uuid4(), **project.dict())
    project_repository.add(instance)
    session.commit()

    return ProjectOutputSchema.model_validate(instance)


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_pk(pk: UUID, session: Annotated[Session, Depends(get_db_session)]) -> None:
    project_repository = ProjectRepository(session)

    instance = project_repository.get_by_pk(pk)
    project_repository.delete(instance)


@router.put("/{pk}")
def update_by_pk(
    pk: UUID,
    project: ProjectUpdateSchema,
    session: Annotated[Session, Depends(get_db_session)],
) -> ProjectOutputSchema:
    project_repository = ProjectRepository(session)

    project_repository.update(pk, project.dict())
    session.commit()

    instance = project_repository.get_by_pk(pk)

    return ProjectOutputSchema.model_validate(instance)
