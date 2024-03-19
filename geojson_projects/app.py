from fastapi import FastAPI

from geojson_projects.exceptions_handlers import EXCEPTIONS_HANDLERS, generic_exception_handler
from geojson_projects.projects.routes import router as projects_router

app = FastAPI()

app.include_router(projects_router)

for error, eh in EXCEPTIONS_HANDLERS.items():
    app.exception_handler(error)(eh)

app.exception_handler(Exception)(generic_exception_handler)


@app.get("/")
def hello_world() -> str:
    return "Hello World"
