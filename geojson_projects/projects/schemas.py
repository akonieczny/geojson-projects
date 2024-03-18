from datetime import datetime
from uuid import UUID

import geojson_pydantic as geojson
from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo

AreaPreValidationType = dict[str, str | None] | geojson.Feature | None  # type: ignore[type-arg]


class ProjectBaseSchema(BaseModel):
    name: str = Field(max_length=32)
    description: str
    start_date: datetime
    end_date: datetime
    area: geojson.Feature  # type: ignore[type-arg]

    @field_validator("area", mode="before")
    @classmethod
    def validate_area(cls, v: AreaPreValidationType) -> AreaPreValidationType:
        if v is None:
            return v  # allow Pydantic raise missing error

        if isinstance(v, geojson.Feature):
            return v

        if "properties" not in v:
            v.update({"properties": None})

        return v

    @field_validator("end_date", mode="after")
    @classmethod
    def validate_end_date(cls, v: datetime, values: ValidationInfo) -> datetime:
        start_date = values.data.get("start_date")
        if start_date is None:
            return v  # allow Pydantic raise missing error

        if v < start_date:
            error_type = "value_error"
            error_msg = 'The "end_date" should be later than the "start_date"'
            error_ctx = {"start_date": values.data["start_date"], "end_date": v}
            raise PydanticCustomError(error_type, error_msg, error_ctx)

        return v


class ProjectOutputSchema(ProjectBaseSchema):
    pk: UUID


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    pass
