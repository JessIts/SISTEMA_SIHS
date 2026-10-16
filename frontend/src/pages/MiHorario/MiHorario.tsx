import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import PageHeader from '../../components/common/PageHeader/PageHeader'
import { ClaseFicha } from '../../components/horario/ClaseContent/ClaseContent'
import HorarioGrid from '../../components/horario/HorarioGrid/HorarioGrid'
import HorarioHeader from '../../components/horario/HorarioHeader/HorarioHeader'

import { getMiHorario } from '../../services/mi.service'
import type { HorarioGrilla } from '../../types/academic.types'
import { errorMessage } from '../../utils/format'

/**
 * Horario completo de una de las fichas del usuario (solo lectura).
 * El backend verifica que la ficha le pertenezca.
 */
function MiHorario() {
  const { fichaTrimestreUuid } = useParams<{ fichaTrimestreUuid: string }>()

  const [grilla, setGrilla] = useState<HorarioGrilla | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!fichaTrimestreUuid) {
      return
    }

    getMiHorario(fichaTrimestreUuid)
      .then(setGrilla)
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar el horario.')),
      )
  }, [fichaTrimestreUuid])

  return (
    <section>
      <PageHeader
        title="Horario de la ficha"
        description={grilla ? grilla.encabezado.programa : undefined}
        actions={
          <Link to="/" className="btn btn--secondary">
            Volver al inicio
          </Link>
        }
      />

      <div className="panel">
        {error && <p className="panel__error">{error}</p>}

        {!grilla && !error && <p className="panel__muted">Cargando horario...</p>}

        {grilla && (
          <>
            <HorarioHeader encabezado={grilla.encabezado} />

            <HorarioGrid
              dias={grilla.dias}
              jornadas={grilla.jornadas}
              renderClase={(clase) => <ClaseFicha clase={clase} />}
              hideEmptyJornadas
            />
          </>
        )}
      </div>
    </section>
  )
}

export default MiHorario
