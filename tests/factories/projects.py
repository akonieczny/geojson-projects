import datetime as dt
import json
from pathlib import Path
from typing import cast

import factory
from mimesis_factory import MimesisField

from geojson_projects.projects.models import Project
from tests.factories.base import BaseSQLAlchemyFactory


def load_geojson() -> str:
    with open(Path(__file__).parent / "artifacts" / "geojson.json") as f:
        geojson = cast(str, json.load(f))

    return geojson  # noqa: RET504


class ProjectFactory(BaseSQLAlchemyFactory[Project]):
    pk = MimesisField("uuid")
    name = factory.Sequence(lambda n: f"Project name: {n}")
    description = "Description"
    start_date = dt.datetime.now(tz=dt.UTC) - dt.timedelta(days=5)
    end_date = dt.datetime.now(tz=dt.UTC)
    area = factory.LazyFunction(load_geojson)

    class Meta:
        model = Project
