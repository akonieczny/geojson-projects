from sqlalchemy.ext.declarative import declarative_base

from geojson_projects.database import sqlalchemy_metadata

BaseSqlAlchemyModel = declarative_base(metadata=sqlalchemy_metadata)
