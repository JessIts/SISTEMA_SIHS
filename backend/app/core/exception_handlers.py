from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppException,
    ConflictException,
    NotFoundException,
    ValidationException,
    UnauthorizedException,
)


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def conflict_exception_handler(
    request: Request,
    exc: ConflictException,
):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "message": exc.message,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: ValidationException,
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": exc.message,
        },
    )
    
async def unauthorized_exception_handler(
    request: Request,
    exc: UnauthorizedException,
):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "message": exc.message,
        },
    )