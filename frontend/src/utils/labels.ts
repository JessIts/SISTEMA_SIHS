import type {
  EstadoFicha,
  EstadoTrimestre,
  ModalidadClase,
  ModalidadFicha,
} from '../types/academic.types'

export const MODALIDAD_CLASE_LABELS: Record<ModalidadClase, string> = {
  presencial: 'Presencial',
  sincronico: 'Sincrónico',
}

export const MODALIDAD_FICHA_LABELS: Record<ModalidadFicha, string> = {
  presencial: 'Presencial',
  virtual: 'Virtual',
  mixta: 'Mixta',
}

export const ESTADO_FICHA_LABELS: Record<EstadoFicha, string> = {
  en_formacion: 'En formación',
  finalizada: 'Finalizada',
  cancelada: 'Cancelada',
}

export const ESTADO_TRIMESTRE_LABELS: Record<EstadoTrimestre, string> = {
  planeacion: 'Planeación',
  activo: 'Activo',
  cerrado: 'Cerrado',
}

export function toOptions<T extends string>(
  labels: Record<T, string>,
): { value: string; label: string }[] {
  return (Object.keys(labels) as T[]).map((value) => ({
    value,
    label: labels[value],
  }))
}
