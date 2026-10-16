-- =====================================================================
-- 03_carga_masiva.sql : carga de horarios desde CSV usando LLAVES NATURALES
--   (código de ficha, documento del instructor, nombre del ambiente...)
--   Flujo: CSV -> tabla staging (todo texto) -> validación -> tabla real
-- =====================================================================
SET search_path TO horarios;

-- Staging: recibe el archivo tal cual, sin restricciones
CREATE TABLE IF NOT EXISTS stg_horarios (
    fila                 SERIAL PRIMARY KEY,
    codigo_ficha         TEXT,
    anio                 TEXT,
    numero_trimestre     TEXT,
    dia                  TEXT,     -- LUNES, MARTES ...
    hora_inicio          TEXT,     -- 12:00
    codigo_competencia   TEXT,
    codigo_resultado     TEXT,
    documento_instructor TEXT,
    modalidad            TEXT,     -- PRESENCIAL / SINCRONICO
    sede                 TEXT,
    ambiente             TEXT,
    error                TEXT      -- lo llena la función
);

-- Resuelve llaves, marca errores fila por fila e inserta solo las válidas.
-- Devuelve cuántas filas entraron y cuántas quedaron con error.
CREATE OR REPLACE FUNCTION fn_procesar_stg_horarios(OUT insertadas INT, OUT con_error INT)
AS $$
BEGIN
    UPDATE stg_horarios SET error = NULL;

    -- 1) Resolver todas las llaves de una vez (set-based, no fila a fila)
    CREATE TEMP TABLE tmp_resuelto ON COMMIT DROP AS
    SELECT s.fila,
           ft.id_ficha_trimestre, ft.id_trimestre,
           d.id_dia, fh.id_franja, r.id_resultado,
           u.id_usuario AS id_instructor,
           upper(trim(s.modalidad)) AS modalidad,
           a.id_ambiente
    FROM stg_horarios s
    LEFT JOIN fichas f            ON f.codigo_ficha = trim(s.codigo_ficha)
    LEFT JOIN trimestres t        ON t.anio::text = trim(s.anio) AND t.numero::text = trim(s.numero_trimestre)
    LEFT JOIN ficha_trimestre ft  ON ft.id_ficha = f.id_ficha AND ft.id_trimestre = t.id_trimestre
    LEFT JOIN dias_semana d       ON d.nombre_dia = upper(trim(s.dia))
    LEFT JOIN franjas_horarias fh ON fh.hora_inicio = trim(s.hora_inicio)::time
    LEFT JOIN competencias c      ON c.id_programa = f.id_programa AND c.codigo = trim(s.codigo_competencia)
    LEFT JOIN resultados_aprendizaje r ON r.id_competencia = c.id_competencia AND r.codigo = trim(s.codigo_resultado)
    LEFT JOIN usuarios u          ON u.documento = trim(s.documento_instructor)
    LEFT JOIN sedes se            ON se.nombre_sede = trim(s.sede)
    LEFT JOIN ambientes a         ON a.id_sede = se.id_sede AND a.nombre_ambiente = trim(s.ambiente);

    -- 2) Errores de llaves que no existen
    UPDATE stg_horarios s SET error = concat_ws('; ',
        CASE WHEN r.id_ficha_trimestre IS NULL THEN 'ficha/trimestre no programado' END,
        CASE WHEN r.id_dia       IS NULL THEN 'día inválido' END,
        CASE WHEN r.id_franja    IS NULL THEN 'franja inexistente' END,
        CASE WHEN r.id_resultado IS NULL THEN 'resultado no pertenece al programa' END,
        CASE WHEN r.id_instructor IS NULL THEN 'instructor no existe' END,
        CASE WHEN r.modalidad = 'PRESENCIAL' AND r.id_ambiente IS NULL THEN 'ambiente no existe' END)
    FROM tmp_resuelto r WHERE r.fila = s.fila;
    UPDATE stg_horarios SET error = NULL WHERE error = '';

    -- 3) Choques contra lo que YA está en la BD y contra el mismo archivo
    UPDATE stg_horarios s SET error = 'choque: ' || x.motivo
    FROM (
        SELECT r.fila,
               CASE WHEN EXISTS (SELECT 1 FROM horarios h WHERE h.id_ficha_trimestre = r.id_ficha_trimestre
                                   AND h.id_dia = r.id_dia AND h.id_franja = r.id_franja)
                      OR row_number() OVER (PARTITION BY r.id_ficha_trimestre, r.id_dia, r.id_franja ORDER BY r.fila) > 1
                    THEN 'la ficha ya tiene clase en esa franja'
                    WHEN EXISTS (SELECT 1 FROM horarios h WHERE h.id_trimestre = r.id_trimestre
                                   AND h.id_dia = r.id_dia AND h.id_franja = r.id_franja AND h.id_instructor = r.id_instructor)
                      OR row_number() OVER (PARTITION BY r.id_trimestre, r.id_dia, r.id_franja, r.id_instructor ORDER BY r.fila) > 1
                    THEN 'instructor ocupado'
                    WHEN r.id_ambiente IS NOT NULL AND (
                         EXISTS (SELECT 1 FROM horarios h WHERE h.id_trimestre = r.id_trimestre
                                   AND h.id_dia = r.id_dia AND h.id_franja = r.id_franja AND h.id_ambiente = r.id_ambiente)
                      OR row_number() OVER (PARTITION BY r.id_trimestre, r.id_dia, r.id_franja, r.id_ambiente ORDER BY r.fila) > 1)
                    THEN 'ambiente ocupado'
               END AS motivo
        FROM tmp_resuelto r
        JOIN stg_horarios s2 ON s2.fila = r.fila AND s2.error IS NULL
    ) x
    WHERE x.fila = s.fila AND x.motivo IS NOT NULL;

    -- 4) Insertar las válidas (el trigger valida el rol de instructor)
    INSERT INTO horarios (id_ficha_trimestre, id_trimestre, id_dia, id_franja,
                          id_resultado, id_instructor, modalidad, id_ambiente)
    SELECT r.id_ficha_trimestre, r.id_trimestre, r.id_dia, r.id_franja,
           r.id_resultado, r.id_instructor, r.modalidad,
           CASE WHEN r.modalidad = 'PRESENCIAL' THEN r.id_ambiente END
    FROM tmp_resuelto r JOIN stg_horarios s ON s.fila = r.fila
    WHERE s.error IS NULL;
    GET DIAGNOSTICS insertadas = ROW_COUNT;

    SELECT count(*) INTO con_error FROM stg_horarios WHERE error IS NOT NULL;
END $$ LANGUAGE plpgsql;
