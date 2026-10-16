-- =====================================================================
-- 02_datos_base.sql : catálogos + el horario de la ficha 3141665
-- (documentos, correos y códigos de programa/competencia son de prueba)
-- =====================================================================
SET search_path TO horarios;

INSERT INTO roles (nombre_rol) VALUES ('ADMIN'),('COORDINADOR'),('INSTRUCTOR'),('APRENDIZ');

INSERT INTO jornadas (nombre_jornada) VALUES ('MAÑANA'),('TARDE'),('NOCHE');

INSERT INTO franjas_horarias (id_jornada, hora_inicio, hora_fin, orden) VALUES
 (1,'06:15','09:00',1),
 (1,'09:00','12:00',2),
 (2,'12:00','15:00',3),
 (2,'15:00','18:00',4),
 (3,'18:00','20:00',5),
 (3,'20:00','22:00',6);

INSERT INTO dias_semana VALUES
 (1,'LUNES'),(2,'MARTES'),(3,'MIÉRCOLES'),(4,'JUEVES'),(5,'VIERNES'),(6,'SÁBADO');

INSERT INTO sedes (nombre_sede, direccion, tipo_sede) VALUES
 ('Sede Principal',  'Calle 52 # 13-65',  'PRINCIPAL'),
 ('Sede Unigermana', 'AK 14 # 63-87',     'SECUNDARIA'),
 ('Sede Fontibón',   'Cl 19A # 96c-40',   'SECUNDARIA');

INSERT INTO ambientes (id_sede, nombre_ambiente, capacidad) VALUES
 (3,'202 A',30),(3,'304 A',30),(3,'304 B',30);

INSERT INTO coordinaciones (nombre_coordinacion) VALUES ('Coordinación Comercio y Mercadeo');
INSERT INTO coordinacion_sede VALUES (1,3);

INSERT INTO programas (codigo_programa, nombre_programa, nivel, id_coordinacion)
VALUES ('PRG-MERC', 'DESARROLLO DE PROCESOS DE MERCADEO', 'TECNÓLOGO', 1);

INSERT INTO competencias (id_programa, codigo, descripcion)
VALUES (1, 'COMP-01', 'Competencia de prueba del programa de mercadeo');

INSERT INTO resultados_aprendizaje (id_competencia, codigo, descripcion) VALUES
 (1,'13','Aplicar acciones del plan de merchandising en el canal de acuerdo con objetivos de mercadeo y normativa'),
 (1,'14','Establecer el plan de acción de endomarketing de acuerdo con la identidad corporativa'),
 (1,'15','Seleccionar técnica de evaluación de estrategias para el plan de mercadeo según políticas de la organización');

INSERT INTO usuarios (documento, nombres, apellidos, email) VALUES
 ('1000000001','CARLOS','PEREZ','carlos.perez@prueba.local'),
 ('1000000002','OMAR','SANCHEZ','omar.sanchez@prueba.local'),
 ('1000000003','NAYUBI','ROJAS','nayubi.rojas@prueba.local');
INSERT INTO usuario_rol SELECT id_usuario, 3 FROM usuarios;   -- los 3 son INSTRUCTOR

INSERT INTO trimestres (anio, numero, fecha_inicio, fecha_fin, estado)
VALUES (2026, 3, '2026-07-09', '2026-09-28', 'ACTIVO');

INSERT INTO fichas (codigo_ficha, id_programa, id_jornada, fecha_inicio, fecha_fin)
VALUES ('3141665', 1, 2, '2024-10-01', '2026-12-31');

INSERT INTO ficha_trimestre (id_ficha, id_trimestre, trimestre_ficha, horas_semanales)
VALUES (1, 1, 7, 24);

-- Celdas del horario (jornada tarde: franjas 3 y 4)
-- resultado: 1='13', 2='14', 3='15' | ambientes: 1=202A, 2=304A, 3=304B
INSERT INTO horarios (id_ficha_trimestre, id_trimestre, id_dia, id_franja,
                      id_resultado, id_instructor, modalidad, id_ambiente) VALUES
 (1,1,1,3, 3,1,'SINCRONICO',NULL), (1,1,1,4, 3,1,'SINCRONICO',NULL),  -- lunes
 (1,1,2,3, 3,1,'PRESENCIAL',1),    (1,1,2,4, 3,1,'PRESENCIAL',1),     -- martes
 (1,1,4,3, 2,2,'PRESENCIAL',2),    (1,1,4,4, 2,2,'PRESENCIAL',2),     -- jueves
 (1,1,5,3, 1,3,'PRESENCIAL',3),    (1,1,5,4, 1,3,'PRESENCIAL',3);     -- viernes
