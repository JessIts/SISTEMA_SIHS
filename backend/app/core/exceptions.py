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


class ValidationException(AppException):
    """Error de validación de negocio."""