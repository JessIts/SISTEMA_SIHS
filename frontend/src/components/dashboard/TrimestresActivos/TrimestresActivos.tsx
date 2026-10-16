import type { MiTrimestre } from '../../../types/mi.types'
import { formatPeriodo, formatTrimestre } from '../../../utils/format'

interface TrimestresActivosProps {
  trimestres: MiTrimestre[]
}

function TrimestresActivos({ trimestres }: TrimestresActivosProps) {
  if (trimestres.length === 0) {
    return (
      <p className="panel__muted">
        No hay trimestres en etapa activa. Cámbialos desde Trimestres.
      </p>
    )
  }

  return (
    <ul className="trimestres-activos">
      {trimestres.map((trimestre) => (
        <li key={trimestre.uuid}>
          <strong>{formatTrimestre(trimestre)}</strong>
          <span>{formatPeriodo(trimestre)}</span>
        </li>
      ))}
    </ul>
  )
}

export default TrimestresActivos
