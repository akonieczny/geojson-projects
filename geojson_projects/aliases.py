from collections.abc import Callable
from typing import Any, TypeVar

from geojson_projects.models import BaseSqlAlchemyModel

TFunc = TypeVar("TFunc", bound=Callable[..., Any])
TModel = TypeVar("TModel", bound=BaseSqlAlchemyModel)
