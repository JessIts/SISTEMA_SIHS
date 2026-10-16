-- =====================================================================
-- 04_pruebas_pgadmin.sql : pruebas para ejecutar en el Query Tool de pgAdmin
--
-- Requisito: haber ejecutado antes 01, 02 y 03 en la base sihs_horarios.
-- pgAdmin solo muestra el resultado de la ÚLTIMA consulta ejecutada, así que:
--   -> SELECCIONA cada bloque (desde "PRUEBA n" hasta el siguiente) y presiona F5.
-- Cada bloque arranca con SET search_path para poder correrlo suelto.
-- =====================================================================


-- =====================================================================
-- PRUEBA 1. Encabezado del horario (como el PDF)
-- =====================================================================
SET search_path TO horarios;
SELECT DISTINCT nombre_grupo, horas_semanales,
       to_char(fecha_inicio,'DD/MM/YYYY') || ' - ' || to_char(fecha_fin,'DD/MM/YYYY') AS periodo
FROM v_horario
WHERE codigo_ficha = '3141665';


-- =====================================================================
-- PRUEBA 2. Grilla del horario: filas = franjas, columnas = días
--           (es lo mismo que debe devolver la API)
-- =====================================================================
SET search_path TO horarios;
SELECT to_char(fh.hora_inicio,'HH24:MI') || ' - ' || to_char(fh.hora_fin,'HH24:MI') AS franja,
       j.nombre_jornada AS jornada,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 1) AS lunes,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 2) AS martes,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 3) AS miercoles,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 4) AS jueves,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 5) AS viernes,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 6) AS sabado
FROM franjas_horarias fh
JOIN jornadas j ON j.id_jornada = fh.id_jornada
LEFT JOIN v_horario v ON v.orden_franja = fh.orden AND v.codigo_ficha = '3141665'
GROUP BY fh.orden, fh.hora_inicio, fh.hora_fin, j.nombre_jornada
ORDER BY fh.orden;


-- =====================================================================
-- PRUEBA 3. Vista plana (una fila por casilla) — formato cómodo para JSON
-- =====================================================================
SET search_path TO horarios;
SELECT nombre_dia, hora_inicio, hora_fin, tematica, instructor, ambiente
FROM v_horario
WHERE codigo_ficha = '3141665'
ORDER BY id_dia, orden_franja;


-- =====================================================================
-- PRUEBA 4. Horas programadas vs horas asignadas (deben ser iguales: 24 / 24)
-- =====================================================================
SET search_path TO horarios;
SELECT f.codigo_ficha,
       ft.horas_semanales AS horas_asignadas,
       sum(extract(epoch FROM fh.hora_fin - fh.hora_inicio) / 3600)::numeric(5,2) AS horas_programadas
FROM horarios h
JOIN ficha_trimestre ft  ON ft.id_ficha_trimestre = h.id_ficha_trimestre
JOIN fichas f            ON f.id_ficha = ft.id_ficha
JOIN franjas_horarias fh ON fh.id_franja = h.id_franja
GROUP BY f.codigo_ficha, ft.horas_semanales;


-- =====================================================================
-- PRUEBA 5. Horario de un instructor y ocupación de ambientes
-- =====================================================================
SET search_path TO horarios;
SELECT instructor, nombre_dia, hora_inicio, hora_fin, codigo_ficha, ambiente
FROM v_horario
WHERE instructor = 'CARLOS PEREZ'
ORDER BY id_dia, orden_franja;

-- (5b) ocupación por ambiente
SET search_path TO horarios;
SELECT ambiente, nombre_dia, hora_inicio, hora_fin, codigo_ficha
FROM v_horario
WHERE ambiente <> 'Sincrónico'
ORDER BY ambiente, id_dia, orden_franja;


-- =====================================================================
-- PRUEBA 6. Reglas anti-choque
--   Ejecuta TODO este bloque (incluye el SELECT final).
--   Cada caso se intenta y se deshace; la columna "ok" debe salir TRUE en todas.
-- =====================================================================
SET search_path TO horarios;
DROP TABLE IF EXISTS pg_temp.resultado_pruebas;
CREATE TEMP TABLE resultado_pruebas (n INT, prueba TEXT, esperado TEXT, obtenido TEXT, detalle TEXT);

DO $$
DECLARE
    -- {descripción, esperado (FALLA / PASA), sql}
    casos TEXT[][] := ARRAY[
      ['Ficha con 2 clases en la misma casilla', 'FALLA',
       $q$INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
          VALUES (1,1,1,3,1,3,'PRESENCIAL',3)$q$],
      ['Instructor en dos fichas a la vez', 'FALLA',
       $q$INSERT INTO fichas (codigo_ficha,id_programa,id_jornada,fecha_inicio,fecha_fin) VALUES ('2000001',1,2,'2025-01-01','2027-01-01');
          INSERT INTO ficha_trimestre (id_ficha,id_trimestre,trimestre_ficha,horas_semanales)
            SELECT id_ficha,1,3,24 FROM fichas WHERE codigo_ficha='2000001';
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT ft.id_ficha_trimestre,1,2,3,1,1,'PRESENCIAL',3
            FROM ficha_trimestre ft JOIN fichas f USING (id_ficha) WHERE f.codigo_ficha='2000001'$q$],
      ['Ambiente ocupado por otra ficha', 'FALLA',
       $q$INSERT INTO fichas (codigo_ficha,id_programa,id_jornada,fecha_inicio,fecha_fin) VALUES ('2000002',1,2,'2025-01-01','2027-01-01');
          INSERT INTO ficha_trimestre (id_ficha,id_trimestre,trimestre_ficha,horas_semanales)
            SELECT id_ficha,1,3,24 FROM fichas WHERE codigo_ficha='2000002';
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT ft.id_ficha_trimestre,1,2,3,1,3,'PRESENCIAL',1
            FROM ficha_trimestre ft JOIN fichas f USING (id_ficha) WHERE f.codigo_ficha='2000002'$q$],
      ['Clase presencial sin ambiente', 'FALLA',
       $q$INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
          VALUES (1,1,3,3,1,3,'PRESENCIAL',NULL)$q$],
      ['Usuario sin rol INSTRUCTOR', 'FALLA',
       $q$INSERT INTO usuarios (documento,nombres,apellidos,email) VALUES ('555','ANA','APRENDIZ','ana@prueba.local');
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT 1,1,3,3,1,id_usuario,'SINCRONICO',NULL FROM usuarios WHERE documento='555'$q$],
      ['Trimestre distinto al de la ficha', 'FALLA',
       $q$INSERT INTO trimestres (anio,numero,fecha_inicio,fecha_fin) VALUES (2026,4,'2026-10-05','2026-12-15');
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT 1,id_trimestre,3,3,1,3,'SINCRONICO',NULL FROM trimestres WHERE anio=2026 AND numero=4$q$],
      ['Resultado de otro programa', 'FALLA',
       $q$INSERT INTO programas (codigo_programa,nombre_programa,id_coordinacion) VALUES ('PRG-OTRO','OTRO PROGRAMA',1);
          INSERT INTO competencias (id_programa,codigo,descripcion) SELECT id_programa,'C-X','x' FROM programas WHERE codigo_programa='PRG-OTRO';
          INSERT INTO resultados_aprendizaje (id_competencia,codigo,descripcion)
            SELECT c.id_competencia,'1','x' FROM competencias c JOIN programas p USING (id_programa) WHERE p.codigo_programa='PRG-OTRO';
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT 1,1,3,3,r.id_resultado,3,'SINCRONICO',NULL
            FROM resultados_aprendizaje r JOIN competencias c USING (id_competencia) WHERE c.codigo='C-X'$q$],
      ['Dos fichas en SINCRÓNICO a la misma hora (permitido)', 'PASA',
       $q$INSERT INTO fichas (codigo_ficha,id_programa,id_jornada,fecha_inicio,fecha_fin) VALUES ('2000003',1,2,'2025-01-01','2027-01-01');
          INSERT INTO ficha_trimestre (id_ficha,id_trimestre,trimestre_ficha,horas_semanales)
            SELECT id_ficha,1,3,24 FROM fichas WHERE codigo_ficha='2000003';
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT ft.id_ficha_trimestre,1,1,3,1,3,'SINCRONICO',NULL
            FROM ficha_trimestre ft JOIN fichas f USING (id_ficha) WHERE f.codigo_ficha='2000003'$q$]
    ];
    i INT;
BEGIN
    FOR i IN 1 .. array_length(casos, 1) LOOP
        BEGIN
            EXECUTE casos[i][3];
            RAISE EXCEPTION USING ERRCODE = 'P0099', MESSAGE = 'se insertó sin error';  -- deshace lo insertado
        EXCEPTION
            WHEN SQLSTATE 'P0099' THEN
                INSERT INTO resultado_pruebas VALUES (i, casos[i][1], casos[i][2], 'PASA', SQLERRM);
            WHEN OTHERS THEN
                INSERT INTO resultado_pruebas VALUES (i, casos[i][1], casos[i][2], 'FALLA', SQLERRM);
        END;
    END LOOP;
END $$;

SELECT n, prueba, esperado, obtenido, (esperado = obtenido) AS ok, detalle
FROM resultado_pruebas ORDER BY n;


-- =====================================================================
-- PRUEBA 7. Carga masiva (simula el CSV con INSERTs, porque pgAdmin no
--           tiene \copy; desde la API cargarías el archivo igual a staging)
--   Ejecuta TODO el bloque. Resultado esperado: 1 insertada, 5 con error.
--   OJO: si lo corres 2 veces, la fila 1 sale como "choque" porque ya quedó
--   insertada. Para repetir desde cero, vuelve a correr 01, 02 y 03.
-- =====================================================================
SET search_path TO horarios;
TRUNCATE stg_horarios RESTART IDENTITY;

INSERT INTO stg_horarios (codigo_ficha, anio, numero_trimestre, dia, hora_inicio,
                          codigo_competencia, codigo_resultado, documento_instructor,
                          modalidad, sede, ambiente) VALUES
 ('3141665','2026','3','MIÉRCOLES','12:00','COMP-01','14','1000000002','PRESENCIAL','Sede Fontibón','304 A'),  -- válida
 ('3141665','2026','3','MIÉRCOLES','12:00','COMP-01','14','1000000002','PRESENCIAL','Sede Fontibón','304 A'),  -- duplicada en el archivo
 ('3141665','2026','3','LUNES',    '12:00','COMP-01','13','1000000003','PRESENCIAL','Sede Fontibón','304 B'),  -- la ficha ya tiene clase
 ('3141665','2026','3','SÁBADO',   '06:15','COMP-01','99','1000000003','PRESENCIAL','Sede Fontibón','304 B'),  -- resultado inexistente
 ('3141665','2026','3','SÁBADO',   '09:00','COMP-01','13','9999999999','PRESENCIAL','Sede Fontibón','404 Z'),  -- instructor y ambiente no existen
 ('9999999','2026','3','SÁBADO',   '09:00','COMP-01','13','1000000003','SINCRONICO', NULL,           NULL);    -- ficha no programada

SELECT * FROM fn_procesar_stg_horarios();

-- (7b) detalle fila por fila
SET search_path TO horarios;
SELECT fila, codigo_ficha, dia, hora_inicio, documento_instructor,
       coalesce(error, 'OK') AS resultado
FROM stg_horarios ORDER BY fila;

-- (7c) la grilla ahora muestra la clase nueva del miércoles: vuelve a ejecutar la PRUEBA 2
