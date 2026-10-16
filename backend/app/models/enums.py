from enum import Enum


class ModalidadClase(str, Enum):
    """Cómo se dicta una casilla del horario."""

    PRESENCIAL = "presencial"
    SINCRONICO = "sincronico"


class ModalidadFicha(str, Enum):
    PRESENCIAL = "presencial"
    VIRTUAL = "virtual"
    MIXTA = "mixta"


class EstadoFicha(str, Enum):
    EN_FORMACION = "en_formacion"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class EstadoTrimestre(str, Enum):
    PLANEACION = "planeacion"
    ACTIVO = "activo"
    CERRADO = "cerrado"


def enum_values(enum_class) -> list[str]:
    """Guarda en PostgreSQL el valor del enum ('presencial') y no su nombre."""

    return [member.value for member in enum_class]
