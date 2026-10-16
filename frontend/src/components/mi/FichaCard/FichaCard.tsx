import { Link } from 'react-router-dom'

import type { MiFicha } from '../../../types/mi.types'
import { formatDate, formatTrimestre } from '../../../utils/format'
import { ESTADO_FICHA_LABELS, MODALIDAD_FICHA_LABELS } from '../../../utils/labels'

import './FichaCard.css'

interface FichaCardProps {
  ficha: MiFicha
}

/**
 * Resumen de una ficha del usuario con acceso a sus horarios por trimestre.
 */
function FichaCard({ ficha }: FichaCardProps) {
  return (
    <article className="ficha-card">
      <div className="ficha-card__top">
        <span className="ficha-card__code">Ficha {ficha.codigo}</span>
        <span className="ficha-card__state">{ESTADO_FICHA_LABELS[ficha.estado]}</span>
      </div>

      <h3 className="ficha-card__program">{ficha.programa.nombre}</h3>

      <dl className="ficha-card__meta">
        <div>
          <dt>Jornada</dt>
          <dd>{ficha.jornada.nombre}</dd>
        </div>
        <div>
          <dt>Modalidad</dt>
          <dd>{MODALIDAD_FICHA_LABELS[ficha.modalidad]}</dd>
        </div>
        <div>
          <dt>Formación</dt>
          <dd>{formatDate(ficha.fecha_inicio)} – {formatDate(ficha.fecha_fin)}</dd>
        </div>
      </dl>

      {ficha.programaciones.length > 0 && (
        <div className="ficha-card__links">
          <span>Horarios:</span>

          {ficha.programaciones.map((programacion) => (
            <Link
              key={programacion.uuid}
              to={`/mi-horario/${programacion.uuid}`}
              className="btn btn--secondary btn--small"
            >
              {programacion.trimestre_ficha}_TRM · {formatTrimestre(programacion.trimestre)}
            </Link>
          ))}
        </div>
      )}
    </article>
  )
}

export default FichaCard
