import type { EncabezadoGrilla } from '../../../types/academic.types'
import { formatDate, formatHoras } from '../../../utils/format'

import './HorarioHeader.css'

interface HorarioHeaderProps {
  encabezado: EncabezadoGrilla
}

/**
 * Encabezado del horario, igual al del archivo:
 * "7_TRM_3141665_..." · horas asignadas · fechas del trimestre.
 */
function HorarioHeader({ encabezado }: HorarioHeaderProps) {
  const avance = encabezado.horas_semanales
    ? Math.min(encabezado.horas_programadas / encabezado.horas_semanales, 1)
    : 0

  const completo = encabezado.horas_programadas >= encabezado.horas_semanales

  return (
    <div className="horario-header">
      <div className="horario-header__title">
        <span className="horario-header__eyebrow">
          Ficha {encabezado.ficha} · Trimestre {encabezado.trimestre_ficha} de formación
        </span>

        <h2>{encabezado.nombre_grupo}</h2>
      </div>

      <dl className="horario-header__meta">
        <div>
          <dt>Periodo</dt>
          <dd>
            {formatDate(encabezado.fecha_inicio)} – {formatDate(encabezado.fecha_fin)}
            <span> ({encabezado.anio}-T{encabezado.trimestre_anio})</span>
          </dd>
        </div>

        <div>
          <dt>Aprendices</dt>
          <dd>{encabezado.aprendices}</dd>
        </div>

        <div className="horario-header__hours">
          <dt>Horas por semana</dt>
          <dd>
            <strong>{formatHoras(encabezado.horas_programadas)}</strong> de{' '}
            {formatHoras(encabezado.horas_semanales)}

            <span
              className="horario-header__bar"
              role="progressbar"
              aria-valuemin={0}
              aria-valuemax={encabezado.horas_semanales}
              aria-valuenow={encabezado.horas_programadas}
            >
              <span
                className={completo ? 'is-complete' : ''}
                style={{ width: `${avance * 100}%` }}
              />
            </span>
          </dd>
        </div>
      </dl>
    </div>
  )
}

export default HorarioHeader
