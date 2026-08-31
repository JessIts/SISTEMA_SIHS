from fastapi import FastAPI

from app.core.config import settings
from app.routes.router import api_router


app = FastAPI(
    title=settings.app_name,
    description="API backend para el sistema de información",
    version=settings.app_version,
    debug=settings.debug,
)


app.include_router(api_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }