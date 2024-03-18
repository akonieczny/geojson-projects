from fastapi import FastAPI

from geojson_projects.projects.routes import router as projects_router

app = FastAPI()

app.include_router(projects_router)


@app.get("/")
def hello_world() -> str:
    return "Hello World"
