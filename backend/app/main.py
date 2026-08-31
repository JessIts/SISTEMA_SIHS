from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import (
    app_exception_handler,
    conflict_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
)
from app.core.exceptions import (
    AppException,
    ConflictException,
    NotFoundException,
    ValidationException,
)
from app.routes.router import api_router


app = FastAPI(
    title=settings.app_name,
    description="API backend para el sistema de información",
    version=settings.app_version,
    debug=settings.debug,
)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    NotFoundException,
    not_found_exception_handler,
)

app.add_exception_handler(
    ConflictException,
    conflict_exception_handler,
)

app.add_exception_handler(
    ValidationException,
    validation_exception_handler,
)


app.include_router(api_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }