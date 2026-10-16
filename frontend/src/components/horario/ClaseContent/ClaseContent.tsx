import type { ClaseCelda } from '../../../types/academic.types'
import type { ClaseAgenda } from '../../../types/mi.types'

/**
 * Contenido de una casilla en el horario de una ficha:
 * temática, instructor y ambiente (como en el archivo).
 */
export function ClaseFicha({ clase }: { clase: ClaseCelda }) {
  return (
    <>
      <span className="clase-celda__tematica" title={clase.tematica}>
        {clase.tematica}
      </span>
      <span className="clase-celda__meta">{clase.instructor}</span>
      <span
        className={`clase-celda__tag ${
          clase.modalidad === 'sincronico' ? 'clase-celda__tag--sincronico' : ''
        }`}
      >
        {clase.ambiente}
      </span>
    </>
  )
}

/**
 * Contenido de una casilla en la agenda del instructor:
 * ficha, temática y ambiente.
 */
export function ClaseInstructor({ clase }: { clase: ClaseAgenda }) {
  return (
    <>
      <span className="clase-celda__meta">
        <strong>Ficha {clase.ficha}</strong>
      </span>
      <span className="clase-celda__tematica" title={clase.tematica}>
        {clase.tematica}
      </span>
      <span
        className={`clase-celda__tag ${
          clase.modalidad === 'sincronico' ? 'clase-celda__tag--sincronico' : ''
        }`}
      >
        {clase.ambiente}
      </span>
    </>
  )
}
