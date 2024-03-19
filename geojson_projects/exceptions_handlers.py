from collections.abc import Callable
from urllib.request import Request

from starlette import status
from starlette.responses import JSONResponse

from geojson_projects.aliases import TFunc
from geojson_projects.exceptions import (
    AlreadyExistError,
    BaseError,
    NotFoundError,
)

EXCEPTIONS_HANDLERS: dict[type[BaseError], TFunc] = {}  # type: ignore[valid-type]


def _register_exception_handler(*errors: type[BaseError]) -> Callable[[TFunc], TFunc]:
    def wrapper(func: TFunc) -> TFunc:
        for error in errors:
            EXCEPTIONS_HANDLERS[error] = func
        return func

    return wrapper


@_register_exception_handler(AlreadyExistError)
async def already_exist_error_exception_handler(request: Request, exc: BaseError) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message},
    )


@_register_exception_handler(NotFoundError)
async def not_found_error_exception_handler(request: Request, exc: BaseError) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error"},
    )
