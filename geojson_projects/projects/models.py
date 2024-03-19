import datetime as dt
import uuid

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as sa_pg

from geojson_projects.models import BaseSqlAlchemyModel


class Project(BaseSqlAlchemyModel):
    __tablename__ = "project"

    pk: uuid.UUID = sa.Column(sa.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)  # type: ignore[assignment]
    name: str = sa.Column(sa.String(length=32), nullable=False)  # type: ignore[assignment]
    description: str | None = sa.Column(sa.TEXT)  # type: ignore[assignment]
    start_date: dt.datetime = sa.Column(sa.DateTime, nullable=False)  # type: ignore[assignment]
    end_date: dt.datetime = sa.Column(sa.DateTime, nullable=False)  # type: ignore[assignment]
    area: str = sa.Column(sa_pg.JSONB, nullable=False)  # type: ignore[assignment]
