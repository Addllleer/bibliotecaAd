from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

def not_found_error_handler(request: Request, exc: LookupError):
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno inesperado"},
    )
