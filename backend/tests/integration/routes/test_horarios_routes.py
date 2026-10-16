"""
Flujo completo del módulo de horarios contra la API (igual que en Swagger):
login con cookie -> CRUD de catálogos -> casillas -> reglas anti-choque -> grilla.
"""
from itertools import count
from uuid import uuid4

import pytest

from app.core.security import hash_password
from app.models.roles import UserRole
from app.models.user import User


API = "/api/v1"
PASSWORD = "Password123!"

# Valores únicos dentro de la sesión de pruebas (orden y horas de las franjas)
_franja_seq = count(100)


def _uid() -> str:
    return uuid4().hex[:8]


def _create_user(db, role: UserRole) -> User:
    suffix = _uid()

    user = User(
        name=f"{role.value.upper()} {suffix}",
        email=f"{role.value}-{suffix}@example.com",
        phone="3001234567",
        document_number=f"D-{suffix}",
        password_hash=hash_password(PASSWORD),
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def _login(client, user: User) -> None:
    response = client.post(
        f"{API}/auth/login",
        json={"email": user.email, "password": PASSWORD},
    )

    assert response.status_code == 200, response.json()


def _post(client, url: str, body: dict) -> dict:
    response = client.post(f"{API}{url}", json=body)

    assert response.status_code == 201, response.json()

    return response.json()["data"]


def _get_or_create_dia(client, numero: int, nombre: str) -> dict:
    items = client.get(f"{API}/dias-semana", params={"limit": 100}).json()["data"]["items"]

    for item in items:
        if item["numero"] == numero:
            return item

    return _post(client, "/dias-semana", {"numero": numero, "nombre": nombre})


@pytest.fixture
def admin_client(client, db):
    admin = _create_user(db, UserRole.ADMIN)

    _login(client, admin)

    return client


@pytest.fixture
def escenario(admin_client, db):
    """Catálogos mínimos para armar un horario."""

    c = admin_client
    s = _uid()

    jornada = _post(c, "/jornadas", {"nombre": f"TARDE-{s}"})

    base_orden = next(_franja_seq) * 2
    minuto = base_orden % 59

    franja_1 = _post(c, "/franjas-horarias", {
        "jornada_uuid": jornada["uuid"],
        "hora_inicio": f"12:{minuto:02d}",
        "hora_fin": f"14:{minuto:02d}",
        "orden": base_orden,
    })

    franja_2 = _post(c, "/franjas-horarias", {
        "jornada_uuid": jornada["uuid"],
        "hora_inicio": f"15:{minuto:02d}",
        "hora_fin": f"18:{minuto:02d}",
        "orden": base_orden + 1,
    })

    lunes = _get_or_create_dia(c, 1, "LUNES")
    martes = _get_or_create_dia(c, 2, "MARTES")

    sede = _post(c, "/sedes", {"nombre": f"Sede {s}", "direccion": "Calle 1 # 2-3"})

    ambiente_a = _post(c, "/ambientes", {"sede_uuid": sede["uuid"], "nombre": "101", "capacidad": 30})
    ambiente_b = _post(c, "/ambientes", {"sede_uuid": sede["uuid"], "nombre": "102"})

    coordinacion = _post(c, "/coordinaciones", {
        "nombre": f"Coordinación {s}",
        "sedes_uuids": [sede["uuid"]],
    })

    programa = _post(c, "/programas", {
        "codigo": f"P-{s}",
        "nombre": "PROGRAMA DE PRUEBA",
        "coordinacion_uuid": coordinacion["uuid"],
    })

    competencia = _post(c, "/competencias", {
        "programa_uuid": programa["uuid"],
        "codigo": "C1",
        "descripcion": "Competencia de prueba",
    })

    resultado = _post(c, "/resultados-aprendizaje", {
        "competencia_uuid": competencia["uuid"],
        "codigo": "15",
        "descripcion": "Seleccionar técnica de evaluación",
    })

    trimestre = _post(c, "/trimestres", {
        "anio": 2000 + int(s, 16) % 100,
        "numero": int(s, 16) % 4 + 1,
        "fecha_inicio": "2026-07-09",
        "fecha_fin": "2026-09-28",
    })

    def nueva_ficha(codigo: str) -> dict:
        ficha = _post(c, "/fichas", {
            "codigo": codigo,
            "programa_uuid": programa["uuid"],
            "jornada_uuid": jornada["uuid"],
            "fecha_inicio": "2024-10-01",
            "fecha_fin": "2026-12-31",
        })

        return _post(c, "/fichas-trimestre", {
            "ficha_uuid": ficha["uuid"],
            "trimestre_uuid": trimestre["uuid"],
            "trimestre_ficha": 7,
            "horas_semanales": 24,
        })

    instructor_1 = _create_user(db, UserRole.INSTRUCTOR)
    instructor_2 = _create_user(db, UserRole.INSTRUCTOR)

    return {
        "jornada": jornada,
        "franja_1": franja_1,
        "franja_2": franja_2,
        "lunes": lunes,
        "martes": martes,
        "sede": sede,
        "ambiente_a": ambiente_a,
        "ambiente_b": ambiente_b,
        "programa": programa,
        "competencia": competencia,
        "resultado": resultado,
        "trimestre": trimestre,
        "ft_1": nueva_ficha(f"F1{s}"),
        "ft_2": nueva_ficha(f"F2{s}"),
        "instructor_1": str(instructor_1.uuid),
        "instructor_2": str(instructor_2.uuid),
    }


def _casilla(e: dict, **overrides) -> dict:
    body = {
        "ficha_trimestre_uuid": e["ft_1"]["uuid"],
        "dia_uuid": e["lunes"]["uuid"],
        "franja_uuid": e["franja_1"]["uuid"],
        "resultado_uuid": e["resultado"]["uuid"],
        "instructor_uuid": e["instructor_1"],
        "modalidad": "presencial",
        "ambiente_uuid": e["ambiente_a"]["uuid"],
    }
    body.update(overrides)
    return body


# ----------------------------------------------------------------------
# Autenticación y permisos
# ----------------------------------------------------------------------
def test_listar_sin_autenticacion_devuelve_401(client):
    response = client.get(f"{API}/sedes")

    assert response.status_code == 401


def test_usuario_sin_rol_admin_no_puede_crear(client, db):
    _login(client, _create_user(db, UserRole.INSTRUCTOR))

    response = client.post(f"{API}/sedes", json={"nombre": "X", "direccion": "Calle 1"})

    assert response.status_code == 403


# ----------------------------------------------------------------------
# CRUD genérico (sedes / ambientes)
# ----------------------------------------------------------------------
def test_crud_sede_y_ambiente(admin_client):
    c = admin_client
    s = _uid()

    sede = _post(c, "/sedes", {"nombre": f"Sede CRUD {s}", "direccion": "Calle 9"})

    # Duplicado -> 409 con mensaje claro
    dup = c.post(f"{API}/sedes", json={"nombre": f"Sede CRUD {s}", "direccion": "Otra"})
    assert dup.status_code == 409
    assert dup.json()["message"] == "Ya existe una sede con ese nombre."

    ambiente = _post(c, "/ambientes", {"sede_uuid": sede["uuid"], "nombre": "A1"})
    assert ambiente["sede"]["uuid"] == sede["uuid"]

    # Filtro por sede
    listado = c.get(f"{API}/ambientes", params={"sede_uuid": sede["uuid"]}).json()["data"]
    assert listado["total"] == 1

    # Sede inexistente -> 422
    bad = c.post(f"{API}/ambientes", json={"sede_uuid": str(uuid4()), "nombre": "A2"})
    assert bad.status_code == 422

    # Actualizar
    upd = c.put(f"{API}/sedes/{sede['uuid']}", json={"direccion": "Calle 10"})
    assert upd.status_code == 200
    assert upd.json()["data"]["direccion"] == "Calle 10"

    # No se desactiva una sede con ambientes activos
    blocked = c.delete(f"{API}/sedes/{sede['uuid']}")
    assert blocked.status_code == 409

    assert c.delete(f"{API}/ambientes/{ambiente['uuid']}").status_code == 204
    assert c.delete(f"{API}/sedes/{sede['uuid']}").status_code == 204
    assert c.get(f"{API}/sedes/{sede['uuid']}").status_code == 404

    inactivas = c.get(f"{API}/sedes/inactive").json()["data"]
    assert any(item["uuid"] == sede["uuid"] for item in inactivas)

    activada = c.patch(f"{API}/sedes/{sede['uuid']}/activate")
    assert activada.status_code == 200
    assert activada.json()["data"]["is_active"] is True


# ----------------------------------------------------------------------
# Horarios: reglas
# ----------------------------------------------------------------------
def test_crear_casilla_y_choques(admin_client, escenario):
    c = admin_client
    e = escenario

    casilla = _post(c, "/horarios", _casilla(e))
    assert casilla["ambiente"]["nombre"] == "101"
    assert casilla["ficha_trimestre"]["trimestre_ficha"] == 7

    # 1) La misma ficha en la misma casilla
    r = c.post(f"{API}/horarios", json=_casilla(e, instructor_uuid=e["instructor_2"], ambiente_uuid=e["ambiente_b"]["uuid"]))
    assert r.status_code == 409
    assert "La ficha ya tiene una clase" in r.json()["message"]

    # 2) El instructor en otra ficha a la misma hora
    r = c.post(f"{API}/horarios", json=_casilla(e, ficha_trimestre_uuid=e["ft_2"]["uuid"], ambiente_uuid=e["ambiente_b"]["uuid"]))
    assert r.status_code == 409
    assert "El instructor ya tiene clase" in r.json()["message"]

    # 3) El ambiente ocupado por otra ficha
    r = c.post(f"{API}/horarios", json=_casilla(e, ficha_trimestre_uuid=e["ft_2"]["uuid"], instructor_uuid=e["instructor_2"]))
    assert r.status_code == 409
    assert "ya está ocupado" in r.json()["message"]

    # 4) Sincrónico a la misma hora en otra ficha: permitido
    _post(c, "/horarios", _casilla(
        e,
        ficha_trimestre_uuid=e["ft_2"]["uuid"],
        instructor_uuid=e["instructor_2"],
        modalidad="sincronico",
        ambiente_uuid=None,
    ))


def test_validaciones_de_casilla(admin_client, escenario, db):
    c = admin_client
    e = escenario

    r = c.post(f"{API}/horarios", json=_casilla(e, ambiente_uuid=None))
    assert r.status_code == 422
    assert r.json()["message"] == "Una clase presencial requiere ambiente."

    r = c.post(f"{API}/horarios", json=_casilla(e, modalidad="sincronico"))
    assert r.status_code == 422

    aprendiz = _create_user(db, UserRole.APRENDIZ)
    r = c.post(f"{API}/horarios", json=_casilla(e, instructor_uuid=str(aprendiz.uuid)))
    assert r.status_code == 422
    assert r.json()["message"] == "El usuario indicado no tiene rol instructor."

    # Resultado de OTRO programa
    otro_programa = _post(c, "/programas", {
        "codigo": f"OTRO-{_uid()}",
        "nombre": "OTRO",
        "coordinacion_uuid": e["programa"]["coordinacion"]["uuid"],
    })
    otra_comp = _post(c, "/competencias", {"programa_uuid": otro_programa["uuid"], "codigo": "X", "descripcion": "xxx"})
    otro_res = _post(c, "/resultados-aprendizaje", {"competencia_uuid": otra_comp["uuid"], "codigo": "1", "descripcion": "xxx"})

    r = c.post(f"{API}/horarios", json=_casilla(e, resultado_uuid=otro_res["uuid"]))
    assert r.status_code == 422
    assert "no pertenece al programa" in r.json()["message"]


def test_actualizar_eliminar_y_grilla(admin_client, escenario):
    c = admin_client
    e = escenario

    casilla = _post(c, "/horarios", _casilla(e))
    _post(c, "/horarios", _casilla(e, dia_uuid=e["martes"]["uuid"], modalidad="sincronico", ambiente_uuid=None))

    # Mover la casilla a la franja 2 y volverla sincrónica (libera el ambiente)
    upd = c.put(f"{API}/horarios/{casilla['uuid']}", json={
        "franja_uuid": e["franja_2"]["uuid"],
        "modalidad": "sincronico",
    })
    assert upd.status_code == 200, upd.json()
    assert upd.json()["data"]["ambiente"] is None

    # Filtros del listado
    listado = c.get(f"{API}/horarios", params={"ficha_trimestre_uuid": e["ft_1"]["uuid"]}).json()["data"]
    assert listado["total"] == 2

    # Grilla
    grilla = c.get(f"{API}/horarios/grilla/{e['ft_1']['uuid']}")
    assert grilla.status_code == 200, grilla.json()

    data = grilla.json()["data"]
    assert data["encabezado"]["nombre_grupo"].startswith("7_TRM_")
    assert data["encabezado"]["horas_semanales"] == 24
    assert data["encabezado"]["horas_programadas"] == 5.0  # 2 h + 3 h

    filas = {
        fila["franja_uuid"]: fila
        for jornada in data["jornadas"]
        for fila in jornada["franjas"]
    }

    fila_2 = filas[e["franja_2"]["uuid"]]
    lunes = next(celda for celda in fila_2["celdas"] if celda["dia_numero"] == 1)
    assert lunes["clase"]["ambiente"] == "Sincrónico"

    # Eliminar (físico) libera la casilla
    assert c.delete(f"{API}/horarios/{casilla['uuid']}").status_code == 204
    assert c.get(f"{API}/horarios/{casilla['uuid']}").status_code == 404


def test_aprendices_y_rol(admin_client, escenario, db):
    c = admin_client
    e = escenario

    ficha_uuid = e["ft_1"]["ficha"]["uuid"]
    usuario = _create_user(db, UserRole.USER)

    # Un usuario sin rol aprendiz no se puede asociar
    r = c.post(f"{API}/fichas/{ficha_uuid}/aprendices/{usuario.uuid}")
    assert r.status_code == 422

    # Cambiar rol desde la API
    r = c.patch(f"{API}/users/{usuario.uuid}/role", json={"role": "aprendiz"})
    assert r.status_code == 200
    assert r.json()["data"]["role"] == "aprendiz"

    r = c.post(f"{API}/fichas/{ficha_uuid}/aprendices/{usuario.uuid}")
    assert r.status_code == 201
    assert len(r.json()["data"]) == 1

    grilla = c.get(f"{API}/horarios/grilla/{e['ft_1']['uuid']}").json()["data"]
    assert grilla["encabezado"]["aprendices"] == 1

    assert c.delete(f"{API}/fichas/{ficha_uuid}/aprendices/{usuario.uuid}").status_code == 204
    assert c.get(f"{API}/fichas/{ficha_uuid}/aprendices").json()["data"] == []


# ----------------------------------------------------------------------
# Permisos por rol y paneles personales
# ----------------------------------------------------------------------
def test_coordinador_gestiona_y_otros_roles_no_leen_catalogos(client, db):
    _login(client, _create_user(db, UserRole.COORDINADOR))

    sede = _post(client, "/sedes", {"nombre": f"Sede Coord {_uid()}", "direccion": "Calle 5"})
    assert client.get(f"{API}/sedes/{sede['uuid']}").status_code == 200
    assert client.get(f"{API}/dashboard/resumen").status_code == 200

    # El coordinador consulta usuarios por rol, pero no administra cuentas
    assert client.get(f"{API}/users", params={"role": "instructor"}).status_code == 200
    assert client.get(f"{API}/users/inactive").status_code == 403

    client.cookies.clear()
    _login(client, _create_user(db, UserRole.INSTRUCTOR))

    assert client.get(f"{API}/sedes").status_code == 403
    assert client.get(f"{API}/dashboard/resumen").status_code == 403
    assert client.get(f"{API}/users").status_code == 403


def test_paneles_de_aprendiz_e_instructor(client, db, escenario):
    c = client
    e = escenario

    _post(c, "/horarios", _casilla(e))  # instructor_1 en ficha 1

    aprendiz = _create_user(db, UserRole.APRENDIZ)
    ficha_uuid = e["ft_1"]["ficha"]["uuid"]
    assert c.post(f"{API}/fichas/{ficha_uuid}/aprendices/{aprendiz.uuid}").status_code == 201

    instructor = db.query(User).filter(User.uuid == e["instructor_1"]).first()

    # --- Aprendiz: solo su ficha, su programa y su horario
    c.cookies.clear()
    _login(c, aprendiz)

    fichas = c.get(f"{API}/mi/fichas").json()["data"]
    assert [f["codigo"] for f in fichas] == [e["ft_1"]["ficha"]["codigo"]]
    assert fichas[0]["programaciones"][0]["uuid"] == e["ft_1"]["uuid"]

    programas = c.get(f"{API}/mi/programas").json()["data"]
    assert programas[0]["competencias"][0]["resultados"][0]["codigo"] == "15"

    assert c.get(f"{API}/mi/horarios/{e['ft_1']['uuid']}").status_code == 200
    assert c.get(f"{API}/mi/horarios/{e['ft_2']['uuid']}").status_code == 403
    assert c.get(f"{API}/horarios/grilla/{e['ft_1']['uuid']}").status_code == 403

    # --- Instructor: su agenda con la clase asignada
    c.cookies.clear()
    _login(c, instructor)

    agenda = c.get(f"{API}/mi/agenda").json()["data"]
    assert agenda["total_clases"] == 1
    assert agenda["trimestre"]["uuid"] == e["trimestre"]["uuid"]

    clases = [
        celda["clase"]
        for jornada in agenda["jornadas"]
        for fila in jornada["franjas"]
        for celda in fila["celdas"]
        if celda["clase"]
    ]
    assert clases[0]["ficha"] == e["ft_1"]["ficha"]["codigo"]

    assert [f["codigo"] for f in c.get(f"{API}/mi/fichas").json()["data"]] == [e["ft_1"]["ficha"]["codigo"]]
    assert c.get(f"{API}/mi/horarios/{e['ft_2']['uuid']}").status_code == 403
