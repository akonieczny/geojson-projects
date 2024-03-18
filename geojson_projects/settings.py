from envparse import Env

env = Env()

POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.str("POSTGRES_PORT", default=5432)
POSTGRES_DB = env.str("POSTGRES_DB", default="geojson_projects")
POSTGRES_USER = env.str("POSTGRES_USER", default="geojson_projects")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="pass")
