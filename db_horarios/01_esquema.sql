-- =====================================================================
-- SIHS - Base de datos de pruebas para HORARIOS (PostgreSQL 14+)
-- 01_esquema.sql : crea todas las tablas desde cero
--
-- Uso:  createdb sihs_horarios
--       psql -d sihs_horarios -f 01_esquema.sql
-- =====================================================================

DROP SCHEMA IF EXISTS horarios CASCADE;
CREATE SCHEMA horarios;
SET search_path TO horarios;

-- ---------------------------------------------------------------------
-- 1. SEGURIDAD: usuarios y roles (igual que tu MER, + documento)
-- ---------------------------------------------------------------------
CREATE TABLE roles (
    id_rol      SMALLSERIAL PRIMARY KEY,
    nombre_rol  VARCHAR(50) NOT NULL UNIQUE          -- ADMIN, COORDINADOR, INSTRUCTOR, APRENDIZ
);

CREATE TABLE usuarios (
    id_usuario      SERIAL PRIMARY KEY,
    documento       VARCHAR(20)  NOT NULL UNIQUE,    -- llave natural para cargas masivas
    nombres         VARCHAR(100) NOT NULL,
    apellidos       VARCHAR(100) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255),                    -- NULL hasta que active la cuenta
    estado          VARCHAR(20)  NOT NULL DEFAULT 'ACTIVO'
                    CHECK (estado IN ('ACTIVO','INACTIVO')),
    fecha_registro  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE usuario_rol (
    id_usuario  INT      NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_rol      SMALLINT NOT NULL REFERENCES roles(id_rol),
    PRIMARY KEY (id_usuario, id_rol)
);

-- ---------------------------------------------------------------------
-- 2. ESTRUCTURA FÍSICA: sedes y ambientes
-- ---------------------------------------------------------------------
CREATE TABLE sedes (
    id_sede      SMALLSERIAL PRIMARY KEY,
    nombre_sede  VARCHAR(150) NOT NULL UNIQUE,
    direccion    VARCHAR(255) NOT NULL,
    tipo_sede    VARCHAR(50)  NOT NULL DEFAULT 'SECUNDARIA'
);

CREATE TABLE ambientes (
    id_ambiente      SERIAL PRIMARY KEY,
    id_sede          SMALLINT     NOT NULL REFERENCES sedes(id_sede),
    nombre_ambiente  VARCHAR(100) NOT NULL,          -- '202 A', '304 B'
    capacidad        SMALLINT     CHECK (capacidad > 0),
    UNIQUE (id_sede, nombre_ambiente)
);

-- ---------------------------------------------------------------------
-- 3. ESTRUCTURA ACADÉMICA
-- ---------------------------------------------------------------------
CREATE TABLE coordinaciones (
    id_coordinacion      SMALLSERIAL PRIMARY KEY,
    nombre_coordinacion  VARCHAR(150) NOT NULL UNIQUE
);

-- Relación "Contiene" de tu MER: una coordinación puede operar en varias sedes
CREATE TABLE coordinacion_sede (
    id_coordinacion  SMALLINT NOT NULL REFERENCES coordinaciones(id_coordinacion) ON DELETE CASCADE,
    id_sede          SMALLINT NOT NULL REFERENCES sedes(id_sede) ON DELETE CASCADE,
    PRIMARY KEY (id_coordinacion, id_sede)
);

CREATE TABLE programas (
    id_programa      SERIAL PRIMARY KEY,
    codigo_programa  VARCHAR(30)  NOT NULL UNIQUE,
    nombre_programa  VARCHAR(150) NOT NULL,
    nivel            VARCHAR(50),                    -- TECNÓLOGO, TÉCNICO...
    id_coordinacion  SMALLINT NOT NULL REFERENCES coordinaciones(id_coordinacion)
);

CREATE TABLE competencias (
    id_competencia  SERIAL PRIMARY KEY,
    id_programa     INT         NOT NULL REFERENCES programas(id_programa) ON DELETE CASCADE,
    codigo          VARCHAR(50) NOT NULL,
    descripcion     TEXT        NOT NULL,
    UNIQUE (id_programa, codigo)
);

-- La "TEMÁTICA" de cada celda del horario es un resultado de aprendizaje
CREATE TABLE resultados_aprendizaje (
    id_resultado    SERIAL PRIMARY KEY,
    id_competencia  INT         NOT NULL REFERENCES competencias(id_competencia) ON DELETE CASCADE,
    codigo          VARCHAR(50) NOT NULL,            -- '13', '14', '15'
    descripcion     TEXT        NOT NULL,
    UNIQUE (id_competencia, codigo)
);

CREATE TABLE actividades_aprendizaje (
    id_actividad      SERIAL PRIMARY KEY,
    id_resultado      INT         NOT NULL REFERENCES resultados_aprendizaje(id_resultado) ON DELETE CASCADE,
    codigo            VARCHAR(50) NOT NULL,
    descripcion       TEXT        NOT NULL,
    tipo_actividad    VARCHAR(50) NOT NULL,
    duracion_minutos  INT         NOT NULL CHECK (duracion_minutos > 0),
    UNIQUE (id_resultado, codigo)
);

-- ---------------------------------------------------------------------
-- 4. CALENDARIO: jornadas, franjas, días, trimestres
-- ---------------------------------------------------------------------
CREATE TABLE jornadas (
    id_jornada      SMALLSERIAL PRIMARY KEY,
    nombre_jornada  VARCHAR(30) NOT NULL UNIQUE      -- MAÑANA, TARDE, NOCHE
);

-- Cada FILA del horario (6:15-9:00, 9:00-12:00, 12:00-3:00 ...)
CREATE TABLE franjas_horarias (
    id_franja    SMALLSERIAL PRIMARY KEY,
    id_jornada   SMALLINT NOT NULL REFERENCES jornadas(id_jornada),
    hora_inicio  TIME     NOT NULL,
    hora_fin     TIME     NOT NULL,
    orden        SMALLINT NOT NULL UNIQUE,           -- para pintar las filas en orden
    CHECK (hora_fin > hora_inicio),
    UNIQUE (hora_inicio, hora_fin)
);

-- Cada COLUMNA del horario (lunes..sábado). id = ISODOW (1=lunes)
CREATE TABLE dias_semana (
    id_dia      SMALLINT PRIMARY KEY CHECK (id_dia BETWEEN 1 AND 7),
    nombre_dia  VARCHAR(15) NOT NULL UNIQUE
);

-- Trimestre = periodo de CALENDARIO (no pertenece a una ficha)
CREATE TABLE trimestres (
    id_trimestre  SERIAL PRIMARY KEY,
    anio          SMALLINT    NOT NULL,
    numero        SMALLINT    NOT NULL CHECK (numero BETWEEN 1 AND 4),
    fecha_inicio  DATE        NOT NULL,
    fecha_fin     DATE        NOT NULL,
    estado        VARCHAR(20) NOT NULL DEFAULT 'PLANEACION'
                  CHECK (estado IN ('PLANEACION','ACTIVO','CERRADO')),
    CHECK (fecha_fin > fecha_inicio),
    UNIQUE (anio, numero)
);

-- ---------------------------------------------------------------------
-- 5. FICHAS
-- ---------------------------------------------------------------------
CREATE TABLE fichas (
    id_ficha      SERIAL PRIMARY KEY,
    codigo_ficha  VARCHAR(20) NOT NULL UNIQUE,       -- '3141665'
    id_programa   INT         NOT NULL REFERENCES programas(id_programa),
    id_jornada    SMALLINT    NOT NULL REFERENCES jornadas(id_jornada),
    modalidad     VARCHAR(30) NOT NULL DEFAULT 'PRESENCIAL',
    fecha_inicio  DATE        NOT NULL,
    fecha_fin     DATE        NOT NULL,
    estado        VARCHAR(20) NOT NULL DEFAULT 'EN_FORMACION',
    CHECK (fecha_fin > fecha_inicio)
);

-- Aprendices (e instructores líderes) asociados a la ficha
CREATE TABLE ficha_usuario (
    id_ficha    INT NOT NULL REFERENCES fichas(id_ficha) ON DELETE CASCADE,
    id_usuario  INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    PRIMARY KEY (id_ficha, id_usuario)
);

-- ENCABEZADO del archivo de horario: "7_TRM_3141665 ... 24 horas ... 09/07 - 28/09"
-- Une la ficha con el trimestre de calendario y guarda en qué trimestre
-- de SU formación va la ficha y cuántas horas se le asignan.
CREATE TABLE ficha_trimestre (
    id_ficha_trimestre  SERIAL PRIMARY KEY,
    id_ficha            INT      NOT NULL REFERENCES fichas(id_ficha) ON DELETE CASCADE,
    id_trimestre        INT      NOT NULL REFERENCES trimestres(id_trimestre),
    trimestre_ficha     SMALLINT NOT NULL CHECK (trimestre_ficha > 0),  -- el "7" de 7_TRM
    horas_semanales     SMALLINT NOT NULL CHECK (horas_semanales > 0),  -- el "24"
    UNIQUE (id_ficha, id_trimestre),
    UNIQUE (id_ficha, trimestre_ficha),
    UNIQUE (id_ficha_trimestre, id_trimestre)        -- necesario para la FK compuesta de abajo
);

-- ---------------------------------------------------------------------
-- 6. HORARIOS: una fila = una CELDA del archivo
--    (ficha + trimestre) x día x franja -> temática, instructor, ambiente
-- ---------------------------------------------------------------------
CREATE TABLE horarios (
    id_horario          SERIAL PRIMARY KEY,
    id_ficha_trimestre  INT      NOT NULL,
    id_trimestre        INT      NOT NULL,           -- copia controlada, permite las reglas anti-choque
    id_dia              SMALLINT NOT NULL REFERENCES dias_semana(id_dia),
    id_franja           SMALLINT NOT NULL REFERENCES franjas_horarias(id_franja),
    id_resultado        INT      NOT NULL REFERENCES resultados_aprendizaje(id_resultado),
    id_instructor       INT      NOT NULL REFERENCES usuarios(id_usuario),
    modalidad           VARCHAR(20) NOT NULL CHECK (modalidad IN ('PRESENCIAL','SINCRONICO')),
    id_ambiente         INT      REFERENCES ambientes(id_ambiente),
    observacion         VARCHAR(255),

    -- id_trimestre siempre coincide con el de la ficha_trimestre
    FOREIGN KEY (id_ficha_trimestre, id_trimestre)
        REFERENCES ficha_trimestre(id_ficha_trimestre, id_trimestre) ON DELETE CASCADE,

    -- presencial => tiene ambiente ; sincrónico => sin ambiente
    CONSTRAINT ck_ambiente_modalidad CHECK (
        (modalidad = 'PRESENCIAL' AND id_ambiente IS NOT NULL) OR
        (modalidad = 'SINCRONICO' AND id_ambiente IS NULL)),

    -- REGLAS ANTI-CHOQUE (las hace cumplir la BD, no solo la API)
    CONSTRAINT uq_ficha_celda      UNIQUE (id_ficha_trimestre, id_dia, id_franja),
    CONSTRAINT uq_instructor_celda UNIQUE (id_trimestre, id_dia, id_franja, id_instructor),
    CONSTRAINT uq_ambiente_celda   UNIQUE (id_trimestre, id_dia, id_franja, id_ambiente)
    -- (en uq_ambiente_celda los NULL no chocan: varias fichas pueden estar en sincrónico)
);

CREATE INDEX ix_horarios_instructor ON horarios (id_instructor, id_trimestre);
CREATE INDEX ix_horarios_ambiente   ON horarios (id_ambiente, id_trimestre);

-- Reglas que un CHECK no puede expresar:
--  * el instructor debe tener rol INSTRUCTOR
--  * el resultado de aprendizaje debe pertenecer al programa de la ficha
CREATE OR REPLACE FUNCTION fn_validar_horario() RETURNS trigger AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM usuario_rol ur JOIN roles r USING (id_rol)
        WHERE ur.id_usuario = NEW.id_instructor AND r.nombre_rol = 'INSTRUCTOR'
    ) THEN
        RAISE EXCEPTION 'El usuario % no tiene rol INSTRUCTOR', NEW.id_instructor;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM ficha_trimestre ft
        JOIN fichas f                 ON f.id_ficha = ft.id_ficha
        JOIN competencias c           ON c.id_programa = f.id_programa
        JOIN resultados_aprendizaje r ON r.id_competencia = c.id_competencia
        WHERE ft.id_ficha_trimestre = NEW.id_ficha_trimestre
          AND r.id_resultado = NEW.id_resultado
    ) THEN
        RAISE EXCEPTION 'El resultado % no pertenece al programa de la ficha', NEW.id_resultado;
    END IF;
    RETURN NEW;
END $$ LANGUAGE plpgsql;

CREATE TRIGGER tg_validar_horario
BEFORE INSERT OR UPDATE ON horarios
FOR EACH ROW EXECUTE FUNCTION fn_validar_horario();

-- ---------------------------------------------------------------------
-- 7. VISTA PLANA: lo que consumiría la API (GET /fichas/{codigo}/horario)
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW v_horario AS
SELECT
    f.codigo_ficha,
    ft.trimestre_ficha,
    ft.trimestre_ficha || '_TRM_' || f.codigo_ficha || '_' || p.nombre_programa AS nombre_grupo,
    t.anio, t.numero AS trimestre_anio, t.fecha_inicio, t.fecha_fin,
    ft.horas_semanales,
    j.nombre_jornada,
    fh.orden          AS orden_franja,
    fh.hora_inicio, fh.hora_fin,
    d.id_dia, d.nombre_dia,
    r.codigo || '. ' || r.descripcion          AS tematica,
    u.nombres || ' ' || u.apellidos            AS instructor,
    CASE WHEN h.modalidad = 'SINCRONICO' THEN 'Sincrónico'
         ELSE a.nombre_ambiente || ' ' || s.nombre_sede END AS ambiente,
    h.id_horario
FROM horarios h
JOIN ficha_trimestre ft        ON ft.id_ficha_trimestre = h.id_ficha_trimestre
JOIN fichas f                  ON f.id_ficha = ft.id_ficha
JOIN programas p               ON p.id_programa = f.id_programa
JOIN trimestres t              ON t.id_trimestre = ft.id_trimestre
JOIN dias_semana d             ON d.id_dia = h.id_dia
JOIN franjas_horarias fh       ON fh.id_franja = h.id_franja
JOIN jornadas j                ON j.id_jornada = fh.id_jornada
JOIN resultados_aprendizaje r  ON r.id_resultado = h.id_resultado
JOIN usuarios u                ON u.id_usuario = h.id_instructor
LEFT JOIN ambientes a          ON a.id_ambiente = h.id_ambiente
LEFT JOIN sedes s              ON s.id_sede = a.id_sede;
