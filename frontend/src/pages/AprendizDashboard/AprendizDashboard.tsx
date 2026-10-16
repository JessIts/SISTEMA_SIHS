import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import PageHeader from '../../components/common/PageHeader/PageHeader'
import { ClaseFicha } from '../../components/horario/ClaseContent/ClaseContent'
import HorarioGrid from '../../components/horario/HorarioGrid/HorarioGrid'
import HorarioHeader from '../../components/horario/HorarioHeader/HorarioHeader'
import FichaCard from '../../components/mi/FichaCard/FichaCard'

import { useAuth } from '../../hooks/useAuth'
import { getMiHorario, getMisFichas } from '../../services/mi.service'
import type { HorarioGrilla } from '../../types/academic.types'
import type { MiFicha } from '../../types/mi.types'
import { errorMessage, formatTrimestre } from '../../utils/format'

import '../Dashboard/Dashboard.css'

/**
 * Dashboard del aprendiz: su ficha y su horario actual. Solo lectura.
 */
function AprendizDashboard() {
  const { user } = useAuth()

  const [fichas, setFichas] = useState<MiFicha[] | null>(null)
  const [programacion, setProgramacion] = useState('')
  const [grilla, setGrilla] = useState<HorarioGrilla | null>(null)

  const [error, setError] = useState('')

  useEffect(() => {
    getMisFichas()
      .then((items) => {
        setFichas(items)

        // Por defecto, el trimestre más reciente de la primera ficha
        const primera = items[0]?.programaciones[0]

        if (primera) {
          setProgramacion(primera.uuid)
        }
      })
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar tu ficha.')),
      )
  }, [])

  useEffect(() => {
    if (!programacion) {
      return
    }

    getMiHorario(programacion)
      .then(setGrilla)
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar tu horario.')),
      )
  }, [programacion])

  const programaciones = (fichas ?? []).flatMap((ficha) =>
    ficha.programaciones.map((item) => ({ ...item, ficha: ficha.codigo })),
  )

  return (
    <section className="dashboard-page">
      <PageHeader
        title={`Hola, ${user?.name ?? ''}`}
        description="Tu ficha, tu horario y la información de tu programa."
        actions={
          <Link to="/mi-programa" className="btn btn--secondary">
            Ver mi programa
          </Link>
        }
      />

      {error && <p className="panel__error">{error}</p>}

      {fichas === null && !error && <p className="panel__muted">Cargando...</p>}

      {fichas && fichas.length === 0 && (
        <div className="panel">
          <p className="panel__muted">
            Aún no perteneces a ninguna ficha. Cuando coordinación te asigne a una, verás aquí tu horario.
          </p>
        </div>
      )}

      {fichas && fichas.length > 0 && (
        <div className="dashboard-stack">
          <div className="ficha-card-list">
            {fichas.map((ficha) => (
              <FichaCard key={ficha.uuid} ficha={ficha} />
            ))}
          </div>

          <div className="panel">
            <div className="panel__header">
              <h2 className="panel__title">Mi horario</h2>

              {programaciones.length > 1 && (
                <select
                  aria-label="Trimestre"
                  value={programacion}
                  onChange={(event) => setProgramacion(event.target.value)}
                >
                  {programaciones.map((item) => (
                    <option key={item.uuid} value={item.uuid}>
                      Ficha {item.ficha} · {item.trimestre_ficha}_TRM · {formatTrimestre(item.trimestre)}
                    </option>
                  ))}
                </select>
              )}
            </div>

            {programaciones.length === 0 && (
              <p className="panel__muted">Tu ficha aún no tiene horario publicado.</p>
            )}

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
        </div>
      )}
    </section>
  )
}

export default AprendizDashboard
