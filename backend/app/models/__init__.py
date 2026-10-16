# Importa todos los modelos para que queden registrados en Base.metadata
# (lo necesitan Alembic y la configuración de relaciones entre modelos).
from app.models.user import User  # noqa: F401
from app.models.sede import Sede  # noqa: F401
from app.models.ambiente import Ambiente  # noqa: F401
from app.models.coordinacion import Coordinacion, coordinacion_sede  # noqa: F401
from app.models.programa import Programa  # noqa: F401
from app.models.competencia import Competencia  # noqa: F401
from app.models.resultado_aprendizaje import ResultadoAprendizaje  # noqa: F401
from app.models.actividad_aprendizaje import ActividadAprendizaje  # noqa: F401
from app.models.jornada import Jornada  # noqa: F401
from app.models.franja_horaria import FranjaHoraria  # noqa: F401
from app.models.dia_semana import DiaSemana  # noqa: F401
from app.models.trimestre import Trimestre  # noqa: F401
from app.models.ficha import Ficha, ficha_aprendiz  # noqa: F401
from app.models.ficha_trimestre import FichaTrimestre  # noqa: F401
from app.models.horario import Horario  # noqa: F401
