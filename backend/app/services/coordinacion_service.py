from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException
from app.models.coordinacion import Coordinacion
from app.models.sede import Sede
from app.repositories.coordinacion_repository import CoordinacionRepository
from app.repositories.sede_repository import SedeRepository
from app.schemas.coordinacion import CoordinacionCreate
from app.services.base_service import BaseService


class CoordinacionService(BaseService[Coordinacion]):

    repository_class = CoordinacionRepository
    entity_label = "coordinación"
    female = True

    constraint_messages = {
        "coordinaciones_nombre_key": "Ya existe una coordinación con ese nombre.",
    }

    dependents = [
        ("programas", "No se puede desactivar la coordinación: tiene programas activos."),
    ]

    def _sedes(self, sedes_uuids: list[UUID]) -> list[Sede]:
        return [
            self.resolve(
                SedeRepository,
                sede_uuid,
                f"La sede {sede_uuid} no existe o está inactiva.",
            )
            for sede_uuid in dict.fromkeys(sedes_uuids)  # sin duplicados
        ]

    def build_entity(self, data: CoordinacionCreate) -> Coordinacion:
        return Coordinacion(
            nombre=data.nombre,
            sedes=self._sedes(data.sedes_uuids),
        )

    def apply_update(self, entity: Coordinacion, update_data: dict) -> None:
        sedes_uuids = update_data.pop("sedes_uuids", None)

        if sedes_uuids is not None:
            entity.sedes = self._sedes(sedes_uuids)

        super().apply_update(entity, update_data)

    # ------------------------------------------------------------------
    # Sedes de la coordinación (relación N:M)
    # ------------------------------------------------------------------
    def add_sede(self, coordinacion_uuid: UUID, sede_uuid: UUID) -> Coordinacion:
        coordinacion = self.get(coordinacion_uuid)
        sede = self._sedes([sede_uuid])[0]

        if sede in coordinacion.sedes:
            raise ConflictException("La sede ya está asociada a la coordinación.")

        coordinacion.sedes.append(sede)

        return self._commit(coordinacion, "No fue posible asociar la sede.")

    def remove_sede(self, coordinacion_uuid: UUID, sede_uuid: UUID) -> Coordinacion:
        coordinacion = self.get(coordinacion_uuid)

        sede = next(
            (s for s in coordinacion.sedes if s.uuid == sede_uuid),
            None,
        )

        if not sede:
            raise NotFoundException("La sede no está asociada a la coordinación.")

        coordinacion.sedes.remove(sede)

        return self._commit(coordinacion, "No fue posible quitar la sede.")
