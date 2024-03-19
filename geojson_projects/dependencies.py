from geojson_projects.database import SessionSqlAlchemy


def get_db_session():  # type: ignore[no-untyped-def] # noqa: ANN201
    db = SessionSqlAlchemy()
    try:
        yield db
    finally:
        db.close()
