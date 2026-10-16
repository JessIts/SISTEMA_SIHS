from fastapi import APIRouter

from app.routes.user_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.register_routes import router as register_router

from app.routes.sede_routes import router as sede_router
from app.routes.ambiente_routes import router as ambiente_router
from app.routes.coordinacion_routes import router as coordinacion_router
from app.routes.programa_routes import router as programa_router
from app.routes.competencia_routes import router as competencia_router
from app.routes.resultado_aprendizaje_routes import router as resultado_aprendizaje_router
from app.routes.actividad_aprendizaje_routes import router as actividad_aprendizaje_router
from app.routes.jornada_routes import router as jornada_router
from app.routes.franja_horaria_routes import router as franja_horaria_router
from app.routes.dia_semana_routes import router as dia_semana_router
from app.routes.trimestre_routes import router as trimestre_router
from app.routes.ficha_routes import router as ficha_router
from app.routes.ficha_trimestre_routes import router as ficha_trimestre_router
from app.routes.horario_routes import router as horario_router
from app.routes.mi_routes import router as mi_router
from app.routes.dashboard_routes import router as dashboard_router


api_router = APIRouter(
    prefix="/api/v1",
)


api_router.include_router(user_router)

api_router.include_router(auth_router)

api_router.include_router(register_router)

# Infraestructura
api_router.include_router(sede_router)
api_router.include_router(ambiente_router)

# Estructura académica
api_router.include_router(coordinacion_router)
api_router.include_router(programa_router)
api_router.include_router(competencia_router)
api_router.include_router(resultado_aprendizaje_router)
api_router.include_router(actividad_aprendizaje_router)

# Calendario
api_router.include_router(jornada_router)
api_router.include_router(franja_horaria_router)
api_router.include_router(dia_semana_router)
api_router.include_router(trimestre_router)

# Fichas y horarios
api_router.include_router(ficha_router)
api_router.include_router(ficha_trimestre_router)
api_router.include_router(horario_router)

# Paneles
api_router.include_router(mi_router)
api_router.include_router(dashboard_router)
