import { apiRequest } from './api'
import { createCrudService } from './crud.service'

import type { ApiResponse, User } from '../types/auth.types'
import type {
  ActividadAprendizaje,
  ActividadAprendizajeCreate,
  Ambiente,
  AmbienteCreate,
  Competencia,
  CompetenciaCreate,
  Coordinacion,
  CoordinacionCreate,
  DiaSemana,
  DiaSemanaCreate,
  Ficha,
  FichaCreate,
  FichaTrimestre,
  FichaTrimestreCreate,
  FichaTrimestreUpdate,
  FranjaHoraria,
  FranjaHorariaCreate,
  Horario,
  HorarioCreate,
  HorarioGrilla,
  HorarioUpdate,
  Jornada,
  JornadaCreate,
  Programa,
  ProgramaCreate,
  ResultadoAprendizaje,
  ResultadoAprendizajeCreate,
  Sede,
  SedeCreate,
  Trimestre,
  TrimestreCreate,
} from '../types/academic.types'

// ----------------------------------------------------------------------
// CRUD estándar de cada recurso
// ----------------------------------------------------------------------
export const sedesService =
  createCrudService<Sede, SedeCreate>('/sedes')

export const ambientesService =
  createCrudService<Ambiente, AmbienteCreate>('/ambientes')

export const coordinacionesService =
  createCrudService<Coordinacion, CoordinacionCreate>('/coordinaciones')

export const programasService =
  createCrudService<Programa, ProgramaCreate>('/programas')

export const competenciasService =
  createCrudService<Competencia, CompetenciaCreate>('/competencias')

export const resultadosService =
  createCrudService<ResultadoAprendizaje, ResultadoAprendizajeCreate>(
    '/resultados-aprendizaje',
  )

export const actividadesService =
  createCrudService<ActividadAprendizaje, ActividadAprendizajeCreate>(
    '/actividades-aprendizaje',
  )

export const jornadasService =
  createCrudService<Jornada, JornadaCreate>('/jornadas')

export const franjasService =
  createCrudService<FranjaHoraria, FranjaHorariaCreate>('/franjas-horarias')

export const diasService =
  createCrudService<DiaSemana, DiaSemanaCreate>('/dias-semana')

export const trimestresService =
  createCrudService<Trimestre, TrimestreCreate>('/trimestres')

export const fichasService =
  createCrudService<Ficha, FichaCreate>('/fichas')

export const fichasTrimestreService =
  createCrudService<
    FichaTrimestre,
    FichaTrimestreCreate,
    FichaTrimestreUpdate
  >('/fichas-trimestre')

export const horariosService =
  createCrudService<Horario, HorarioCreate, HorarioUpdate>('/horarios')

// ----------------------------------------------------------------------
// Operaciones adicionales
// ----------------------------------------------------------------------
export async function getGrillaHorario(
  fichaTrimestreUuid: string,
): Promise<HorarioGrilla> {
  const response = await apiRequest<ApiResponse<HorarioGrilla>>(
    `/horarios/grilla/${fichaTrimestreUuid}`,
    { method: 'GET' },
  )

  return response.data
}

export async function getAprendicesFicha(
  fichaUuid: string,
): Promise<User[]> {
  const response = await apiRequest<ApiResponse<User[]>>(
    `/fichas/${fichaUuid}/aprendices`,
    { method: 'GET' },
  )

  return response.data
}

export async function addAprendizFicha(
  fichaUuid: string,
  userUuid: string,
): Promise<User[]> {
  const response = await apiRequest<ApiResponse<User[]>>(
    `/fichas/${fichaUuid}/aprendices/${userUuid}`,
    { method: 'POST' },
  )

  return response.data
}

export async function removeAprendizFicha(
  fichaUuid: string,
  userUuid: string,
): Promise<void> {
  await apiRequest<void>(
    `/fichas/${fichaUuid}/aprendices/${userUuid}`,
    { method: 'DELETE' },
  )
}
