import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import PageHeader from '../../components/common/PageHeader/PageHeader'
import StatCard from '../../components/dashboard/StatCard/StatCard'
import { ClaseInstructor } from '../../components/horario/ClaseContent/ClaseContent'
import HorarioGrid from '../../components/horario/HorarioGrid/HorarioGrid'
import FichaCard from '../../components/mi/FichaCard/FichaCard'

import { useAuth } from '../../hooks/useAuth'
import { getMiAgenda, getMisFichas } from '../../services/mi.service'
import type { MiAgenda, MiFicha } from '../../types/mi.types'
import { errorMessage, formatHoras, formatPeriodo, formatTrimestre } from '../../utils/format'

import '../Dashboard/Dashboard.css'

/**
 * Dashboard del instructor: su horario personal (todas sus fichas)
 * y las fichas en las que dicta clases. Solo lectura.
 */
function InstructorDashboard() {
  const { user } = useAuth()

  const [agenda, setAgenda] = useState<MiAgenda | null>(null)
  const [fichas, setFichas] = useState<MiFicha[]>([])
  const [trimestre, setTrimestre] = useState('')

  const [error, setError] = useState('')

  useEffect(() => {
    getMisFichas()
      .then(setFichas)
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar tus fichas.')),
      )
  }, [])

  useEffect(() => {
    getMiAgenda(trimestre || undefined)
      .then(setAgenda)
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar tu horario.')),
      )
  }, [trimestre])

  const programas = new Set(fichas.map((ficha) => ficha.programa.uuid)).size

  return (
    <section className="dashboard-page">
      <PageHeader
        title={`Hola, ${user?.name ?? ''}`}
        description="Tus clases de la semana y las fichas en las que participas."
        actions={
          <Link to="/mi-programa" className="btn btn--secondary">
            Ver mis programas
          </Link>
        }
      />

      {error && <p className="panel__error">{error}</p>}

      <div className="dashboard-stack">
        <div className="stat-grid">
          <StatCard label="Clases por semana" value={agenda?.total_clases ?? '—'} />
          <StatCard
            label="Horas por semana"
            value={agenda ? formatHoras(agenda.horas_programadas) : '—'}
          />
          <StatCard label="Fichas" value={fichas.length} />
          <StatCard label="Programas" value={programas} to="/mi-programa" />
        </div>

        <div className="panel">
          <div className="panel__header">
            <div>
              <h2 className="panel__title">Mi horario</h2>
              {agenda?.trimestre && (
                <p className="panel__subtitle">
                  Trimestre {formatTrimestre(agenda.trimestre)} · {formatPeriodo(agenda.trimestre)}
                </p>
              )}
            </div>

            {agenda && agenda.trimestres.length > 1 && (
              <select
                aria-label="Trimestre"
                value={agenda.trimestre?.uuid ?? ''}
                onChange={(event) => setTrimestre(event.target.value)}
              >
                {agenda.trimestres.map((item) => (
                  <option key={item.uuid} value={item.uuid}>
                    {formatTrimestre(item)}
                  </option>
                ))}
              </select>
            )}
          </div>

          {!agenda && !error && <p className="panel__muted">Cargando horario...</p>}

          {agenda && agenda.trimestres.length === 0 && (
            <p className="panel__muted">
              Aún no tienes clases asignadas. Cuando coordinación te asigne una, aparecerá aquí.
            </p>
          )}

          {agenda && agenda.trimestres.length > 0 && (
            <HorarioGrid
              dias={agenda.dias}
              jornadas={agenda.jornadas}
              renderClase={(clase) => <ClaseInstructor clase={clase} />}
              hideEmptyJornadas
            />
          )}
        </div>

        <div className="panel">
          <div className="panel__header">
            <h2 className="panel__title">Mis fichas</h2>
          </div>

          {fichas.length === 0 ? (
            <p className="panel__muted">No tienes fichas asignadas.</p>
          ) : (
            <div className="ficha-card-list">
              {fichas.map((ficha) => (
                <FichaCard key={ficha.uuid} ficha={ficha} />
              ))}
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default InstructorDashboard
