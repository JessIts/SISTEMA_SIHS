import type {
  CoordinacionBrief,
  DiaBrief,
  EstadoFicha,
  EstadoTrimestre,
  GridJornada,
  JornadaBrief,
  ModalidadClase,
  ModalidadFicha,
  ProgramaBrief,
} from './academic.types'

export interface MiTrimestre {
  uuid: string
  anio: number
  numero: number
  fecha_inicio: string
  fecha_fin: string
  estado: EstadoTrimestre
}

export interface MiProgramacion {
  uuid: string
  trimestre_ficha: number
  horas_semanales: number
  trimestre: MiTrimestre
}

export interface MiFicha {
  uuid: string
  codigo: string
  modalidad: ModalidadFicha
  estado: EstadoFicha
  fecha_inicio: string
  fecha_fin: string
  jornada: JornadaBrief
  programa: ProgramaBrief
  programaciones: MiProgramacion[]
}

export interface MiResultado {
  uuid: string
  codigo: string
  descripcion: string
}

export interface MiCompetencia {
  uuid: string
  codigo: string
  descripcion: string
  resultados: MiResultado[]
}

export interface MiPrograma {
  uuid: string
  codigo: string
  nombre: string
  nivel: string | null
  coordinacion: CoordinacionBrief
  competencias: MiCompetencia[]
}

export interface ClaseAgenda {
  horario_uuid: string
  ficha: string
  ficha_trimestre_uuid: string
  tematica: string
  resultado_codigo: string
  modalidad: ModalidadClase
  ambiente: string
}

export interface MiAgenda {
  trimestre: MiTrimestre | null
  trimestres: MiTrimestre[]
  horas_programadas: number
  total_clases: number
  dias: DiaBrief[]
  jornadas: GridJornada<ClaseAgenda>[]
}

// ----------------------------------------------------------------------
// Dashboard de administración / coordinación
// ----------------------------------------------------------------------
export interface ProgramacionResumen {
  ficha_trimestre_uuid: string
  ficha: string
  programa: string
  trimestre_ficha: number
  trimestre: string
  horas_semanales: number
  horas_programadas: number
}

export interface DashboardResumen {
  conteos: {
    sedes: number
    ambientes: number
    programas: number
    fichas: number
    trimestres: number
    horarios: number
  }
  usuarios: {
    admin: number
    coordinador: number
    instructor: number
    aprendiz: number
    user: number
  }
  trimestres_activos: MiTrimestre[]
  programaciones: ProgramacionResumen[]
}
