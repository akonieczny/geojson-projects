from geojson_projects.database import get_db_url

TEST_DB = "test_database"
TEST_DB_URL = get_db_url(database_name=TEST_DB)
