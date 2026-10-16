import { apiRequest } from './api'
import { buildQuery } from './crud.service'

import type { ApiResponse } from '../types/auth.types'
import type { HorarioGrilla } from '../types/academic.types'
import type {
  DashboardResumen,
  MiAgenda,
  MiFicha,
  MiPrograma,
} from '../types/mi.types'

/**
 * Información del usuario autenticado (aprendiz o instructor).
 * El backend solo devuelve lo que le corresponde a ese usuario.
 */
export async function getMisFichas(): Promise<MiFicha[]> {
  const response = await apiRequest<ApiResponse<MiFicha[]>>(
    '/mi/fichas',
    { method: 'GET' },
  )

  return response.data
}

export async function getMisProgramas(): Promise<MiPrograma[]> {
  const response = await apiRequest<ApiResponse<MiPrograma[]>>(
    '/mi/programas',
    { method: 'GET' },
  )

  return response.data
}

export async function getMiHorario(
  fichaTrimestreUuid: string,
): Promise<HorarioGrilla> {
  const response = await apiRequest<ApiResponse<HorarioGrilla>>(
    `/mi/horarios/${fichaTrimestreUuid}`,
    { method: 'GET' },
  )

  return response.data
}

export async function getMiAgenda(
  trimestreUuid?: string,
): Promise<MiAgenda> {
  const response = await apiRequest<ApiResponse<MiAgenda>>(
    `/mi/agenda${buildQuery({ trimestre_uuid: trimestreUuid })}`,
    { method: 'GET' },
  )

  return response.data
}

/**
 * Resumen para los dashboards de administrador y coordinador.
 */
export async function getDashboardResumen(): Promise<DashboardResumen> {
  const response = await apiRequest<ApiResponse<DashboardResumen>>(
    '/dashboard/resumen',
    { method: 'GET' },
  )

  return response.data
}
