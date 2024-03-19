import uuid
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from geojson_projects.dependencies import get_db_session
from geojson_projects.projects.models import Project
from geojson_projects.projects.repositories import ProjectRepository
from geojson_projects.projects.schemas import ProjectCreateSchema, ProjectOutputSchema, ProjectUpdateSchema

router = APIRouter(prefix="/projects")


@router.get("/")
async def get_all(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[ProjectOutputSchema]:
    project_repository = ProjectRepository(session)
    instances = await project_repository.get_all()

    return [ProjectOutputSchema.model_validate(instance) for instance in instances]


@router.get("/{pk}")
async def get_by_pk(
    pk: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProjectOutputSchema:
    project_repository = ProjectRepository(session)

    instance = await project_repository.get_by_pk(pk)

    return ProjectOutputSchema.model_validate(instance)


@router.post("/")
async def create(
    project: ProjectCreateSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProjectOutputSchema:
    project_repository = ProjectRepository(session)

    instance = Project(pk=uuid.uuid4(), **project.dict())
    await project_repository.add(instance)
    await session.commit()

    return ProjectOutputSchema.model_validate(instance)


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_pk(
    pk: UUID,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> None:
    project_repository = ProjectRepository(session)

    instance = await project_repository.get_by_pk(pk)
    await project_repository.delete(instance)
    await session.commit()


@router.put("/{pk}")
async def update_by_pk(
    pk: UUID,
    project: ProjectUpdateSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ProjectOutputSchema:
    project_repository = ProjectRepository(session)

    await project_repository.update(pk, project.dict())
    await session.commit()

    instance = await project_repository.get_by_pk(pk)

    return ProjectOutputSchema.model_validate(instance)
