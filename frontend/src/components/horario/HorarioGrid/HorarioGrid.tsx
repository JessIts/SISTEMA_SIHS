import type { ReactNode } from 'react'

import type {
  DiaBrief,
  GridCell,
  GridJornada,
  GridRow,
} from '../../../types/academic.types'
import { formatTime } from '../../../utils/format'

import './HorarioGrid.css'

interface HorarioGridProps<TClase> {
  dias: DiaBrief[]
  jornadas: GridJornada<TClase>[]
  renderClase: (clase: TClase) => ReactNode
  /** Si se define, las celdas son botones (editor de horarios) */
  onCellClick?: (row: GridRow<TClase>, cell: GridCell<TClase>) => void
  /** Oculta las jornadas sin clases (vista de consulta) */
  hideEmptyJornadas?: boolean
}

/**
 * Horario con la forma del archivo de la ficha:
 * columnas = días, filas = franjas agrupadas por jornada.
 */
function HorarioGrid<TClase>({
  dias,
  jornadas,
  renderClase,
  onCellClick,
  hideEmptyJornadas = false,
}: HorarioGridProps<TClase>) {
  const visibles = hideEmptyJornadas
    ? jornadas.filter((jornada) =>
        jornada.franjas.some((row) =>
          row.celdas.some((cell) => cell.clase !== null),
        ),
      )
    : jornadas

  if (visibles.length === 0) {
    return (
      <p className="horario-grid__empty">
        No hay clases programadas.
      </p>
    )
  }

  return (
    <div className="horario-grid">
      <table className="horario-grid__table">
        <thead>
          <tr>
            <th className="horario-grid__corner">Franja</th>

            {dias.map((dia) => (
              <th key={dia.uuid}>{dia.nombre}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {visibles.map((jornada) => (
            <JornadaRows
              key={jornada.jornada}
              jornada={jornada}
              columnas={dias.length}
              renderClase={renderClase}
              onCellClick={onCellClick}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}

interface JornadaRowsProps<TClase> {
  jornada: GridJornada<TClase>
  columnas: number
  renderClase: (clase: TClase) => ReactNode
  onCellClick?: (row: GridRow<TClase>, cell: GridCell<TClase>) => void
}

function JornadaRows<TClase>({
  jornada,
  columnas,
  renderClase,
  onCellClick,
}: JornadaRowsProps<TClase>) {
  return (
    <>
      <tr className="horario-grid__jornada">
        <td colSpan={columnas + 1}>Jornada {jornada.jornada.toLowerCase()}</td>
      </tr>

      {jornada.franjas.map((row) => (
        <tr key={row.franja_uuid}>
          <th scope="row" className="horario-grid__franja">
            {formatTime(row.hora_inicio)}
            <span>{formatTime(row.hora_fin)}</span>
          </th>

          {row.celdas.map((cell) => {
            const content = cell.clase ? (
              <div className="horario-grid__clase">
                {renderClase(cell.clase)}
              </div>
            ) : (
              onCellClick && (
                <span className="horario-grid__add">+ Asignar</span>
              )
            )

            return (
              <td
                key={cell.dia_numero}
                className={cell.clase ? 'horario-grid__cell--busy' : ''}
              >
                {onCellClick ? (
                  <button
                    type="button"
                    className="horario-grid__cell-button"
                    onClick={() => onCellClick(row, cell)}
                    aria-label={`${cell.dia} ${formatTime(row.hora_inicio)}`}
                  >
                    {content}
                  </button>
                ) : (
                  content
                )}
              </td>
            )
          })}
        </tr>
      ))}
    </>
  )
}

export default HorarioGrid
