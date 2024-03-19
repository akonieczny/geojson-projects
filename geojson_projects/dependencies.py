from geojson_projects.database import SessionSqlAlchemy


async def get_db_session():  # type: ignore[no-untyped-def] # noqa: ANN201
    async with SessionSqlAlchemy() as db_session:
        yield db_session
