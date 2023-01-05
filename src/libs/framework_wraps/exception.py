from collections.abc import Iterable

from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from .response import RetrieveResponse
from fastapi.exceptions import RequestValidationError


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    status_code = exc.status_code if exc.status_code else HTTP_500_INTERNAL_SERVER_ERROR
    return RetrieveResponse({"errors": [exc.detail]}, code=status_code)


async def http_400_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler for RequestValidationError
    """
    return RetrieveResponse({"errors": exc.errors()}, code=400, message="RequestValidationError")
