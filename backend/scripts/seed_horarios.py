"""
Carga datos base y el horario de ejemplo de la ficha 3141665.

Uso (desde la carpeta backend, con el venv activo):
    python -m scripts.seed_horarios

Es idempotente: si un registro ya existe (por su llave natural) no lo duplica.

Crea:
  - Catálogos: jornadas, franjas horarias, días de la semana
  - Sedes y ambientes
  - Coordinación, programa, competencia y resultados de aprendizaje
  - Trimestre 2026-T3, ficha 3141665 y su programación (trimestre 7, 24 h)
  - 3 instructores (contraseña: Instructor123*)
  - 1 coordinador (Coordinador123*) y 2 aprendices de la ficha (Aprendiz123*)
  - Las 8 casillas del horario del PDF
"""

from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import (
    Ambiente,
    Competencia,
    Coordinacion,
    DiaSemana,
    Ficha,
    FichaTrimestre,
    FranjaHoraria,
    Horario,
    Jornada,
    Programa,
    ResultadoAprendizaje,
    Sede,
    Trimestre,
    User,
)
from app.models.enums import EstadoTrimestre, ModalidadClase
from app.models.roles import UserRole


INSTRUCTOR_PASSWORD = "Instructor123*"
COORDINADOR_PASSWORD = "Coordinador123*"
APRENDIZ_PASSWORD = "Aprendiz123*"


def get_or_create(db: Session, model, lookup: dict, **values):
    """Busca por `lookup`; si no existe lo crea con lookup + values."""

    instance = db.scalar(select(model).filter_by(**lookup))

    if instance:
        return instance, False

    instance = model(**lookup, **values)
    db.add(instance)
    db.flush()

    return instance, True


def seed(db: Session) -> None:
    creados = 0

    def track(result):
        nonlocal creados
        instance, created = result
        creados += int(created)
        return instance

    # ------------------------------------------------------------------
    # Calendario
    # ------------------------------------------------------------------
    manana = track(get_or_create(db, Jornada, {"nombre": "MAÑANA"}))
    tarde = track(get_or_create(db, Jornada, {"nombre": "TARDE"}))
    noche = track(get_or_create(db, Jornada, {"nombre": "NOCHE"}))

    franjas_def = [
        (manana, time(6, 15), time(9, 0), 1),
        (manana, time(9, 0), time(12, 0), 2),
        (tarde, time(12, 0), time(15, 0), 3),
        (tarde, time(15, 0), time(18, 0), 4),
        (noche, time(18, 0), time(20, 0), 5),
        (noche, time(20, 0), time(22, 0), 6),
    ]

    franjas = {}
    for jornada, inicio, fin, orden in franjas_def:
        franjas[orden] = track(get_or_create(
            db,
            FranjaHoraria,
            {"orden": orden},
            jornada=jornada,
            hora_inicio=inicio,
            hora_fin=fin,
        ))

    dias = {}
    for numero, nombre in enumerate(
        ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO"],
        start=1,
    ):
        dias[numero] = track(get_or_create(db, DiaSemana, {"numero": numero}, nombre=nombre))

    # ------------------------------------------------------------------
    # Infraestructura
    # ------------------------------------------------------------------
    track(get_or_create(db, Sede, {"nombre": "Sede Principal"}, direccion="Calle 52 # 13-65", tipo="PRINCIPAL"))
    track(get_or_create(db, Sede, {"nombre": "Sede Unigermana"}, direccion="AK 14 # 63-87"))
    fontibon = track(get_or_create(db, Sede, {"nombre": "Sede Fontibón"}, direccion="Cl 19A # 96c-40"))

    ambientes = {}
    for nombre in ["202 A", "304 A", "304 B"]:
        ambientes[nombre] = track(get_or_create(
            db,
            Ambiente,
            {"sede_id": fontibon.id, "nombre": nombre},
            capacidad=30,
        ))

    # ------------------------------------------------------------------
    # Estructura académica
    # ------------------------------------------------------------------
    coordinacion = track(get_or_create(db, Coordinacion, {"nombre": "Coordinación Comercio y Mercadeo"}))

    if fontibon not in coordinacion.sedes:
        coordinacion.sedes.append(fontibon)

    programa = track(get_or_create(
        db,
        Programa,
        {"codigo": "PRG-MERC"},
        nombre="DESARROLLO DE PROCESOS DE MERCADEO",
        nivel="TECNÓLOGO",
        coordinacion=coordinacion,
    ))

    competencia = track(get_or_create(
        db,
        Competencia,
        {"programa_id": programa.id, "codigo": "COMP-01"},
        descripcion="Competencia de prueba del programa de mercadeo",
    ))

    resultados = {}
    for codigo, descripcion in [
        ("13", "Aplicar acciones del plan de merchandising en el canal de acuerdo con objetivos de mercadeo y normativa"),
        ("14", "Establecer el plan de acción de endomarketing de acuerdo con la identidad corporativa"),
        ("15", "Seleccionar técnica de evaluación de estrategias para el plan de mercadeo según políticas de la organización"),
    ]:
        resultados[codigo] = track(get_or_create(
            db,
            ResultadoAprendizaje,
            {"competencia_id": competencia.id, "codigo": codigo},
            descripcion=descripcion,
        ))

    # ------------------------------------------------------------------
    # Instructores (usuarios con rol instructor)
    # ------------------------------------------------------------------
    instructores = {}
    for documento, nombre, email in [
        ("1000000001", "CARLOS PEREZ", "carlos.perez@example.com"),
        ("1000000002", "OMAR SANCHEZ", "omar.sanchez@example.com"),
        ("1000000003", "NAYUBI ROJAS", "nayubi.rojas@example.com"),
    ]:
        instructores[nombre] = track(get_or_create(
            db,
            User,
            {"document_number": documento},
            name=nombre,
            email=email,
            phone="3000000000",
            password_hash=hash_password(INSTRUCTOR_PASSWORD),
            role=UserRole.INSTRUCTOR,
        ))

    coordinador = track(get_or_create(
        db,
        User,
        {"document_number": "1000000010"},
        name="LAURA GOMEZ",
        email="coordinacion.mercadeo@example.com",
        phone="3000000010",
        password_hash=hash_password(COORDINADOR_PASSWORD),
        role=UserRole.COORDINADOR,
    ))

    aprendices = [
        track(get_or_create(
            db,
            User,
            {"document_number": documento},
            name=nombre,
            email=email,
            phone="3000000020",
            password_hash=hash_password(APRENDIZ_PASSWORD),
            role=UserRole.APRENDIZ,
        ))
        for documento, nombre, email in [
            ("1000000021", "SOFIA MARTINEZ", "sofia.martinez@example.com"),
            ("1000000022", "JUAN RAMIREZ", "juan.ramirez@example.com"),
        ]
    ]

    # ------------------------------------------------------------------
    # Ficha y su programación en el trimestre
    # ------------------------------------------------------------------
    trimestre = track(get_or_create(
        db,
        Trimestre,
        {"anio": 2026, "numero": 3},
        fecha_inicio=date(2026, 7, 9),
        fecha_fin=date(2026, 9, 28),
        estado=EstadoTrimestre.ACTIVO,
    ))

    ficha = track(get_or_create(
        db,
        Ficha,
        {"codigo": "3141665"},
        programa=programa,
        jornada=tarde,
        fecha_inicio=date(2024, 10, 1),
        fecha_fin=date(2026, 12, 31),
    ))

    for aprendiz in aprendices:
        if aprendiz not in ficha.aprendices:
            ficha.aprendices.append(aprendiz)

    ficha_trimestre = track(get_or_create(
        db,
        FichaTrimestre,
        {"ficha_id": ficha.id, "trimestre_id": trimestre.id},
        trimestre_ficha=7,
        horas_semanales=24,
    ))

    # ------------------------------------------------------------------
    # Casillas del horario (jornada tarde: franjas 3 y 4)
    # ------------------------------------------------------------------
    casillas = [
        # día, resultado, instructor, modalidad, ambiente
        (1, "15", "CARLOS PEREZ", ModalidadClase.SINCRONICO, None),
        (2, "15", "CARLOS PEREZ", ModalidadClase.PRESENCIAL, "202 A"),
        (4, "14", "OMAR SANCHEZ", ModalidadClase.PRESENCIAL, "304 A"),
        (5, "13", "NAYUBI ROJAS", ModalidadClase.PRESENCIAL, "304 B"),
    ]

    for dia, resultado, instructor, modalidad, ambiente in casillas:
        for orden_franja in (3, 4):
            track(get_or_create(
                db,
                Horario,
                {
                    "ficha_trimestre_id": ficha_trimestre.id,
                    "dia_id": dias[dia].id,
                    "franja_id": franjas[orden_franja].id,
                },
                trimestre_id=trimestre.id,
                resultado=resultados[resultado],
                instructor=instructores[instructor],
                modalidad=modalidad,
                ambiente=ambientes[ambiente] if ambiente else None,
            ))

    db.commit()

    print(f"Registros nuevos: {creados}")
    print()
    print("UUIDs útiles para Swagger:")
    print(f"  ficha_trimestre (grilla) : {ficha_trimestre.uuid}")
    print(f"  ficha 3141665            : {ficha.uuid}")
    print(f"  trimestre 2026-T3        : {trimestre.uuid}")
    print(f"  programa                 : {programa.uuid}")
    print(f"  competencia COMP-01      : {competencia.uuid}")
    for codigo, resultado in resultados.items():
        print(f"  resultado {codigo}             : {resultado.uuid}")
    for nombre, user in instructores.items():
        print(f"  instructor {nombre:<13} : {user.uuid}")
    print()
    print("Cuentas de prueba (correo / contraseña):")
    for nombre, user in instructores.items():
        print(f"  instructor  {user.email:<36} {INSTRUCTOR_PASSWORD}")
    print(f"  coordinador {coordinador.email:<36} {COORDINADOR_PASSWORD}")
    for aprendiz in aprendices:
        print(f"  aprendiz    {aprendiz.email:<36} {APRENDIZ_PASSWORD}")


def main():
    db = SessionLocal()

    try:
        seed(db)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
