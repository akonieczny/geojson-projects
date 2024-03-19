from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from geojson_projects import settings

__all__ = ["engine", "get_db_url", "sqlalchemy_metadata", "SessionSqlAlchemy"]


NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def get_db_url(database_name: str | None = settings.POSTGRES_DB) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=database_name,
    )


sqlalchemy_metadata = MetaData(naming_convention=NAMING_CONVENTION)

engine = create_async_engine(get_db_url())

SessionSqlAlchemy = sessionmaker(  # type: ignore[call-overload]
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
