-- =====================================================================
-- 04_pruebas.sql : verifica que la BD arma el horario y bloquea choques
-- Ejecutar con psql DESDE esta carpeta (usa \copy del CSV de ejemplo)
-- =====================================================================
SET search_path TO horarios;
\pset null '·'

\echo '=== 1. Encabezado del horario (como el PDF) ==='
SELECT DISTINCT nombre_grupo, horas_semanales,
       to_char(fecha_inicio,'DD/MM/YYYY') || ' - ' || to_char(fecha_fin,'DD/MM/YYYY') AS periodo
FROM v_horario WHERE codigo_ficha = '3141665';

\echo '=== 2. Grilla: filas = franjas, columnas = días (lo que pinta la API) ==='
SELECT to_char(fh.hora_inicio,'HH24:MI') || '-' || to_char(fh.hora_fin,'HH24:MI') AS franja,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 1) AS lunes,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 2) AS martes,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 3) AS miercoles,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 4) AS jueves,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 5) AS viernes,
       max(v.tematica || ' | ' || v.instructor || ' | ' || v.ambiente) FILTER (WHERE v.id_dia = 6) AS sabado
FROM franjas_horarias fh
LEFT JOIN v_horario v ON v.orden_franja = fh.orden AND v.codigo_ficha = '3141665'
GROUP BY fh.orden, fh.hora_inicio, fh.hora_fin
ORDER BY fh.orden;

\echo '=== 3. Horas programadas vs horas asignadas al trimestre ==='
SELECT f.codigo_ficha, ft.horas_semanales AS asignadas,
       sum(extract(epoch FROM fh.hora_fin - fh.hora_inicio) / 3600)::numeric(5,2) AS programadas
FROM horarios h
JOIN ficha_trimestre ft  ON ft.id_ficha_trimestre = h.id_ficha_trimestre
JOIN fichas f            ON f.id_ficha = ft.id_ficha
JOIN franjas_horarias fh ON fh.id_franja = h.id_franja
GROUP BY f.codigo_ficha, ft.horas_semanales;

\echo '=== 4. Horario de un instructor (otra vista que pedirá la API) ==='
SELECT nombre_dia, hora_inicio, hora_fin, codigo_ficha, ambiente
FROM v_horario WHERE instructor = 'CARLOS PEREZ' ORDER BY id_dia, orden_franja;

\echo '=== 5. Reglas anti-choque: cada intento DEBE fallar ==='
DO $$
DECLARE
    pruebas TEXT[][] := ARRAY[
      ['ficha con 2 clases a la misma hora',
       $q$INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
          VALUES (1,1,1,3,1,3,'PRESENCIAL',3)$q$],
      ['instructor en dos fichas a la vez',
       $q$INSERT INTO fichas (codigo_ficha,id_programa,id_jornada,fecha_inicio,fecha_fin) VALUES ('2000001',1,2,'2025-01-01','2027-01-01');
          INSERT INTO ficha_trimestre (id_ficha,id_trimestre,trimestre_ficha,horas_semanales)
            SELECT id_ficha,1,3,24 FROM fichas WHERE codigo_ficha='2000001';
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT id_ficha_trimestre,1,2,3,1,1,'PRESENCIAL',3 FROM ficha_trimestre WHERE trimestre_ficha=3$q$],
      ['ambiente ocupado por otra ficha',
       $q$INSERT INTO fichas (codigo_ficha,id_programa,id_jornada,fecha_inicio,fecha_fin) VALUES ('2000002',1,2,'2025-01-01','2027-01-01');
          INSERT INTO ficha_trimestre (id_ficha,id_trimestre,trimestre_ficha,horas_semanales)
            SELECT id_ficha,1,3,24 FROM fichas WHERE codigo_ficha='2000002';
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT id_ficha_trimestre,1,2,3,1,3,'PRESENCIAL',1 FROM ficha_trimestre WHERE trimestre_ficha=3$q$],
      ['presencial sin ambiente',
       $q$INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
          VALUES (1,1,3,3,1,3,'PRESENCIAL',NULL)$q$],
      ['usuario sin rol instructor',
       $q$INSERT INTO usuarios (documento,nombres,apellidos,email) VALUES ('555','ANA','APRENDIZ','ana@prueba.local');
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT 1,1,3,3,1,id_usuario,'SINCRONICO',NULL FROM usuarios WHERE documento='555'$q$],
      ['trimestre que no corresponde a la ficha',
       $q$INSERT INTO trimestres (anio,numero,fecha_inicio,fecha_fin) VALUES (2026,4,'2026-10-05','2026-12-15');
          INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
            SELECT 1,id_trimestre,3,3,1,3,'SINCRONICO',NULL FROM trimestres WHERE numero=4$q$]
    ];
    i INT;
BEGIN
    FOR i IN 1 .. array_length(pruebas,1) LOOP
        BEGIN
            EXECUTE pruebas[i][2];
            RAISE NOTICE '✗ FALLÓ LA PRUEBA (se permitió): %', pruebas[i][1];
            RAISE EXCEPTION 'rollback';            -- deshace lo insertado
        EXCEPTION WHEN OTHERS THEN
            IF SQLERRM <> 'rollback' THEN
                RAISE NOTICE '✓ bloqueado: % -> %', pruebas[i][1], SQLERRM;
            END IF;
        END;
    END LOOP;
END $$;

\echo '=== 6. Ambiente sincrónico: dos fichas a la vez SÍ se permite ==='
BEGIN;
INSERT INTO fichas (codigo_ficha,id_programa,id_jornada,fecha_inicio,fecha_fin) VALUES ('2000003',1,2,'2025-01-01','2027-01-01');
INSERT INTO ficha_trimestre (id_ficha,id_trimestre,trimestre_ficha,horas_semanales)
  SELECT id_ficha,1,3,24 FROM fichas WHERE codigo_ficha='2000003';
INSERT INTO horarios (id_ficha_trimestre,id_trimestre,id_dia,id_franja,id_resultado,id_instructor,modalidad,id_ambiente)
  SELECT id_ficha_trimestre,1,1,3,1,3,'SINCRONICO',NULL FROM ficha_trimestre WHERE trimestre_ficha=3;
SELECT count(*) AS fichas_sincronicas_lunes_12 FROM horarios WHERE id_dia=1 AND id_franja=3 AND modalidad='SINCRONICO';
ROLLBACK;

\echo '=== 7. Carga masiva desde CSV (6 filas: 1 válida, 5 con errores) ==='
TRUNCATE stg_horarios RESTART IDENTITY;
\copy stg_horarios (codigo_ficha,anio,numero_trimestre,dia,hora_inicio,codigo_competencia,codigo_resultado,documento_instructor,modalidad,sede,ambiente) FROM 'horarios_ejemplo.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
SELECT * FROM fn_procesar_stg_horarios();
SELECT fila, codigo_ficha, dia, hora_inicio, documento_instructor, coalesce(error,'OK') AS resultado
FROM stg_horarios ORDER BY fila;
