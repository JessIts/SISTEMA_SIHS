from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    COORDINADOR = "coordinador"
    INSTRUCTOR = "instructor"
    APRENDIZ = "aprendiz"
