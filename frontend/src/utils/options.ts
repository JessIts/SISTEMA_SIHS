import {
  competenciasService,
  coordinacionesService,
  fichasService,
  jornadasService,
  programasService,
  resultadosService,
  sedesService,
  trimestresService,
} from '../services/academic.service'
import { getUsers } from '../services/users.service'

import { formatTrimestre } from './format'
import { toSelectOptions } from './form'

/**
 * Cargadores de opciones para los selects de los formularios y filtros.
 * Se definen una sola vez para que las referencias sean estables.
 */
export const opcionesSedes = async () =>
  toSelectOptions(await sedesService.listAll(), (sede) => sede.nombre)

export const opcionesCoordinaciones = async () =>
  toSelectOptions(await coordinacionesService.listAll(), (item) => item.nombre)

export const opcionesProgramas = async () =>
  toSelectOptions(
    await programasService.listAll(),
    (programa) => `${programa.codigo} · ${programa.nombre}`,
  )

export const opcionesCompetencias = async () =>
  toSelectOptions(
    await competenciasService.listAll(),
    (competencia) => `${competencia.programa.codigo} · ${competencia.codigo} · ${competencia.descripcion}`,
  )

export const opcionesResultados = async () =>
  toSelectOptions(
    await resultadosService.listAll(),
    (resultado) => `${resultado.competencia.codigo} · ${resultado.codigo}. ${resultado.descripcion}`,
  )

export const opcionesJornadas = async () =>
  toSelectOptions(await jornadasService.listAll(), (jornada) => jornada.nombre)

export const opcionesTrimestres = async () =>
  toSelectOptions(
    await trimestresService.listAll(),
    (trimestre) => `${formatTrimestre(trimestre)} (${trimestre.estado})`,
  )

export const opcionesFichas = async () =>
  toSelectOptions(
    await fichasService.listAll(),
    (ficha) => `${ficha.codigo} · ${ficha.programa.nombre}`,
  )

export const opcionesInstructores = async () =>
  toSelectOptions(
    (await getUsers(1, 100, 'instructor')).items,
    (user) => `${user.name} · ${user.document_number}`,
  )

export const opcionesAprendices = async () =>
  toSelectOptions(
    (await getUsers(1, 100, 'aprendiz')).items,
    (user) => `${user.name} · ${user.document_number}`,
  )
