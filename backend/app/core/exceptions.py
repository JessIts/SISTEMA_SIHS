class AppException(Exception):
    """Excepción base de la aplicación."""

    def __init__(
        self,
        message: str,
    ):
        self.message = message

        super().__init__(message)


class NotFoundException(AppException):
    """Recurso no encontrado."""


class ConflictException(AppException):
    """Conflicto con el estado actual del recurso."""

class UnauthorizedException(AppException):
    """Credenciales inválidas o autenticación requerida."""

class ValidationException(AppException):
    """Error de validación de negocio."""
    
class ForbiddenException(AppException):
    """El usuario autenticado no tiene permisos suficientes."""