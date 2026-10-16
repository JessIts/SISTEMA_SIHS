/**
 * Tipos del módulo académico / horarios.
 * Reflejan los schemas de respuesta del backend (app/schemas/*.py).
 */

// ----------------------------------------------------------------------
// Enumeraciones
// ----------------------------------------------------------------------
export type ModalidadClase = 'presencial' | 'sincronico'
export type ModalidadFicha = 'presencial' | 'virtual' | 'mixta'
export type EstadoFicha = 'en_formacion' | 'finalizada' | 'cancelada'
export type EstadoTrimestre = 'planeacion' | 'activo' | 'cerrado'

// ----------------------------------------------------------------------
// Referencias resumidas (briefs)
// ----------------------------------------------------------------------
export interface SedeBrief {
  uuid: string
  nombre: string
}

export interface AmbienteBrief {
  uuid: string
  nombre: string
  sede: SedeBrief
}

export interface CoordinacionBrief {
  uuid: string
  nombre: string
}

export interface ProgramaBrief {
  uuid: string
  codigo: string
  nombre: string
}

export interface CompetenciaBrief {
  uuid: string
  codigo: string
  descripcion: string
}

export interface ResultadoBrief {
  uuid: string
  codigo: string
  descripcion: string
}

export interface JornadaBrief {
  uuid: string
  nombre: string
}

export interface FranjaBrief {
  uuid: string
  hora_inicio: string
  hora_fin: string
}

export interface DiaBrief {
  uuid: string
  numero: number
  nombre: string
}

export interface TrimestreBrief {
  uuid: string
  anio: number
  numero: number
  fecha_inicio: string
  fecha_fin: string
}

export interface FichaBrief {
  uuid: string
  codigo: string
}

export interface FichaTrimestreBrief {
  uuid: string
  trimestre_ficha: number
  ficha: FichaBrief
  trimestre: TrimestreBrief
}

export interface UserBrief {
  uuid: string
  name: string
  document_number: string
}

// ----------------------------------------------------------------------
// Entidades
// ----------------------------------------------------------------------
interface BaseEntity {
  uuid: string
  is_active: boolean
  created_at: string
}

export interface Sede extends BaseEntity {
  nombre: string
  direccion: string
  tipo: string
}

export interface SedeCreate {
  nombre: string
  direccion: string
  tipo: string
}

export interface Ambiente extends BaseEntity {
  nombre: string
  capacidad: number | null
  sede: SedeBrief
}

export interface AmbienteCreate {
  sede_uuid: string
  nombre: string
  capacidad: number | null
}

export interface Coordinacion extends BaseEntity {
  nombre: string
  sedes: SedeBrief[]
}

export interface CoordinacionCreate {
  nombre: string
  sedes_uuids: string[]
}

export interface Programa extends BaseEntity {
  codigo: string
  nombre: string
  nivel: string | null
  coordinacion: CoordinacionBrief
}

export interface ProgramaCreate {
  codigo: string
  nombre: string
  nivel: string | null
  coordinacion_uuid: string
}

export interface Competencia extends BaseEntity {
  codigo: string
  descripcion: string
  programa: ProgramaBrief
}

export interface CompetenciaCreate {
  programa_uuid: string
  codigo: string
  descripcion: string
}

export interface ResultadoAprendizaje extends BaseEntity {
  codigo: string
  descripcion: string
  competencia: CompetenciaBrief
}

export interface ResultadoAprendizajeCreate {
  competencia_uuid: string
  codigo: string
  descripcion: string
}

export interface ActividadAprendizaje extends BaseEntity {
  codigo: string
  descripcion: string
  tipo: string
  duracion_minutos: number
  resultado: ResultadoBrief
}

export interface ActividadAprendizajeCreate {
  resultado_uuid: string
  codigo: string
  descripcion: string
  tipo: string
  duracion_minutos: number
}

export interface Jornada extends BaseEntity {
  nombre: string
}

export interface JornadaCreate {
  nombre: string
}

export interface FranjaHoraria extends BaseEntity {
  hora_inicio: string
  hora_fin: string
  orden: number
  jornada: JornadaBrief
}

export interface FranjaHorariaCreate {
  jornada_uuid: string
  hora_inicio: string
  hora_fin: string
  orden: number
}

export interface DiaSemana extends BaseEntity {
  numero: number
  nombre: string
}

export interface DiaSemanaCreate {
  numero: number
  nombre: string
}

export interface Trimestre extends BaseEntity {
  anio: number
  numero: number
  fecha_inicio: string
  fecha_fin: string
  estado: EstadoTrimestre
}

export interface TrimestreCreate {
  anio: number
  numero: number
  fecha_inicio: string
  fecha_fin: string
  estado: EstadoTrimestre
}

export interface Ficha extends BaseEntity {
  codigo: string
  programa: ProgramaBrief
  jornada: JornadaBrief
  modalidad: ModalidadFicha
  fecha_inicio: string
  fecha_fin: string
  estado: EstadoFicha
}

export interface FichaCreate {
  codigo: string
  programa_uuid: string
  jornada_uuid: string
  modalidad: ModalidadFicha
  fecha_inicio: string
  fecha_fin: string
  estado: EstadoFicha
}

export interface FichaTrimestre extends BaseEntity {
  ficha: FichaBrief
  trimestre: TrimestreBrief
  trimestre_ficha: number
  horas_semanales: number
}

export interface FichaTrimestreCreate {
  ficha_uuid: string
  trimestre_uuid: string
  trimestre_ficha: number
  horas_semanales: number
}

export interface FichaTrimestreUpdate {
  trimestre_ficha?: number
  horas_semanales?: number
}

export interface Horario {
  uuid: string
  ficha_trimestre: FichaTrimestreBrief
  dia: DiaBrief
  franja: FranjaBrief
  resultado: ResultadoBrief
  instructor: UserBrief
  modalidad: ModalidadClase
  ambiente: AmbienteBrief | null
  observacion: string | null
  created_at: string
}

export interface HorarioCreate {
  ficha_trimestre_uuid: string
  dia_uuid: string
  franja_uuid: string
  resultado_uuid: string
  instructor_uuid: string
  modalidad: ModalidadClase
  ambiente_uuid: string | null
  observacion: string | null
}

export type HorarioUpdate = Partial<
  Omit<HorarioCreate, 'ficha_trimestre_uuid'>
>

// ----------------------------------------------------------------------
// Cuadrícula del horario (como el archivo PDF)
// ----------------------------------------------------------------------
export interface GridCell<TClase> {
  dia_numero: number
  dia: string
  clase: TClase | null
}

export interface GridRow<TClase> {
  franja_uuid: string
  hora_inicio: string
  hora_fin: string
  celdas: GridCell<TClase>[]
}

export interface GridJornada<TClase> {
  jornada: string
  franjas: GridRow<TClase>[]
}

export interface ClaseCelda {
  horario_uuid: string
  tematica: string
  resultado_codigo: string
  instructor: string
  instructor_uuid: string
  modalidad: ModalidadClase
  ambiente: string
}

export interface EncabezadoGrilla {
  ficha_trimestre_uuid: string
  nombre_grupo: string
  ficha: string
  programa: string
  trimestre_ficha: number
  anio: number
  trimestre_anio: number
  fecha_inicio: string
  fecha_fin: string
  horas_semanales: number
  horas_programadas: number
  aprendices: number
}

export interface HorarioGrilla {
  encabezado: EncabezadoGrilla
  dias: DiaBrief[]
  jornadas: GridJornada<ClaseCelda>[]
}
