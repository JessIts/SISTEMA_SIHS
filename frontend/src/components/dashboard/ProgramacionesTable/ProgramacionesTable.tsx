import { Link } from 'react-router-dom'

import type { ProgramacionResumen } from '../../../types/mi.types'
import { formatHoras } from '../../../utils/format'

import './ProgramacionesTable.css'

interface ProgramacionesTableProps {
  programaciones: ProgramacionResumen[]
}

/**
 * Fichas programadas en los trimestres vigentes y cuánto
 * de su horario está armado (horas programadas vs asignadas).
 */
function ProgramacionesTable({ programaciones }: ProgramacionesTableProps) {
  if (programaciones.length === 0) {
    return (
      <p className="programaciones-table__empty">
        No hay fichas programadas en trimestres activos o en planeación.
      </p>
    )
  }

  return (
    <div className="programaciones-table">
      <table>
        <thead>
          <tr>
            <th>Ficha</th>
            <th>Programa</th>
            <th>Trimestre</th>
            <th>Horas armadas</th>
            <th aria-label="Acciones" />
          </tr>
        </thead>

        <tbody>
          {programaciones.map((item) => {
            const avance = Math.min(item.horas_programadas / item.horas_semanales, 1)
            const completo = item.horas_programadas >= item.horas_semanales

            return (
              <tr key={item.ficha_trimestre_uuid}>
                <td className="programaciones-table__ficha">{item.ficha}</td>
                <td>{item.programa}</td>
                <td>
                  T{item.trimestre_ficha}
                  <span className="programaciones-table__muted"> · {item.trimestre}</span>
                </td>
                <td className="programaciones-table__hours">
                  <span>
                    {formatHoras(item.horas_programadas)} / {formatHoras(item.horas_semanales)}
                  </span>
                  <span className="programaciones-table__bar">
                    <span
                      className={completo ? 'is-complete' : ''}
                      style={{ width: `${avance * 100}%` }}
                    />
                  </span>
                </td>
                <td>
                  <Link
                    to={`/gestion/horarios?ficha_trimestre=${item.ficha_trimestre_uuid}`}
                    className="btn btn--secondary btn--small"
                  >
                    {completo ? 'Ver horario' : 'Armar horario'}
                  </Link>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

export default ProgramacionesTable
