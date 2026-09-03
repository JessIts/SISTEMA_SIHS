from fastapi import APIRouter

from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.register_routes import router as register_router


api_router = APIRouter(
    prefix="/api/v1",
)


api_router.include_router(user_router)

api_router.include_router(auth_router)

api_router.include_router(register_router)