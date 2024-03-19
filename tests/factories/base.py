from typing import Any, Generic, cast

import factory
from sqlalchemy.orm import Session

from geojson_projects.aliases import TModel


class SessionRegistry:
    session: Session | None = None


class BaseSQLAlchemyFactory(Generic[TModel], factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session: Session | None = None  # Injected in container
        sqlalchemy_session_persistence = "commit"

    @classmethod
    def create(cls, **kwargs: Any) -> TModel:  # noqa: ANN401
        cls._meta.sqlalchemy_session = SessionRegistry.session
        return cast(TModel, super().create(**kwargs))
