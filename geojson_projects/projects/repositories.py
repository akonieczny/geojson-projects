from geojson_projects.projects.models import Project
from geojson_projects.repositories import BaseSqlAlchemyRepository


class ProjectRepository(BaseSqlAlchemyRepository[Project]):
    pass
