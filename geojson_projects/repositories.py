import abc
import uuid
from functools import cached_property, wraps
from typing import Any, Generic, cast

import typing_inspect
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from geojson_projects.aliases import TFunc, TModel
from geojson_projects.exceptions import AlreadyExistError, NotFoundError


def not_found(function: TFunc) -> TFunc:
    """Decorator for repositories' methods which access data"""

    @wraps(function)
    async def inner(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        try:
            result = await function(*args, **kwargs)
        except NoResultFound:
            raise NotFoundError from None

        return result

    return cast(TFunc, inner)


def already_exist(function: TFunc) -> TFunc:
    """Decorator for repositories' methods which inserts/updates data"""

    @wraps(function)
    async def inner(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        try:
            await function(*args, **kwargs)
        except IntegrityError:
            raise AlreadyExistError from None

    return cast(TFunc, inner)


class BaseSqlAlchemyRepository(Generic[TModel], abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[TModel]:
        statement = select(self._model_class)
        result = await self.session.execute(statement)
        instances = result.scalars().all()
        return cast(list[TModel], instances)

    @not_found
    async def get_by_pk(self, instance_pk: uuid.UUID) -> TModel:
        statement = select(self._model_class).where(self._model_class.pk == instance_pk)
        result = await self.session.execute(statement)
        instance = result.scalars().one()
        return cast(TModel, instance)

    @already_exist
    async def add(self, instance: TModel) -> None:
        self.session.add(instance)
        await self.session.flush()

    async def delete(self, instance: TModel) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    async def update(self, instance_pk: uuid.UUID, instance_data: dict[str, str]) -> None:
        instance = await self.get_by_pk(instance_pk)
        for k, v in instance_data.items():
            setattr(instance, k, v)
        await self.add(instance)

    @cached_property
    def _model_class(self) -> type[TModel]:
        repository_type_annotation = typing_inspect.get_generic_bases(self)[0]
        model_class = repository_type_annotation.__args__[0]

        return cast(type[TModel], model_class)
