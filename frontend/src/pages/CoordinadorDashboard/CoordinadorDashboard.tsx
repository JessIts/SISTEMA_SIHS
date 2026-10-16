import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import PageHeader from '../../components/common/PageHeader/PageHeader'
import ProgramacionesTable from '../../components/dashboard/ProgramacionesTable/ProgramacionesTable'
import StatCard from '../../components/dashboard/StatCard/StatCard'
import TrimestresActivos from '../../components/dashboard/TrimestresActivos/TrimestresActivos'

import { useAuth } from '../../hooks/useAuth'
import { getDashboardResumen } from '../../services/mi.service'
import type { DashboardResumen } from '../../types/mi.types'
import { errorMessage } from '../../utils/format'

import '../Dashboard/Dashboard.css'

/**
 * Dashboard del coordinador: centrado en armar los horarios
 * de las fichas del trimestre.
 */
function CoordinadorDashboard() {
  const { user } = useAuth()

  const [resumen, setResumen] = useState<DashboardResumen | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getDashboardResumen()
      .then(setResumen)
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar el resumen.')),
      )
  }, [])

  const pendientes = resumen
    ? resumen.programaciones.filter((item) => item.horas_programadas < item.horas_semanales).length
    : 0

  return (
    <section className="dashboard-page">
      <PageHeader
        title={`Hola, ${user?.name ?? ''}`}
        description="Panel de coordinación académica."
        actions={
          <Link to="/gestion/horarios" className="btn btn--primary">
            Armar horarios
          </Link>
        }
      />

      {error && <p className="panel__error">{error}</p>}

      {!resumen && !error && <p className="panel__muted">Cargando resumen...</p>}

      {resumen && (
        <div className="dashboard-stack">
          <div className="stat-grid">
            <StatCard
              label="Horarios incompletos"
              value={pendientes}
              hint={`de ${resumen.programaciones.length} fichas en trimestres vigentes`}
            />
            <StatCard label="Fichas" value={resumen.conteos.fichas} to="/gestion/fichas" />
            <StatCard label="Instructores" value={resumen.usuarios.instructor} />
            <StatCard label="Aprendices" value={resumen.usuarios.aprendiz} />
            <StatCard label="Ambientes" value={resumen.conteos.ambientes} to="/gestion/ambientes" />
            <StatCard label="Clases asignadas" value={resumen.conteos.horarios} to="/gestion/horarios" />
          </div>

          <div className="dashboard-columns">
            <div className="panel">
              <div className="panel__header">
                <div>
                  <h2 className="panel__title">Horarios por armar</h2>
                  <p className="panel__subtitle">
                    Horas programadas frente a las horas asignadas de cada ficha.
                  </p>
                </div>
              </div>

              <ProgramacionesTable programaciones={resumen.programaciones} />
            </div>

            <div className="dashboard-stack">
              <div className="panel">
                <div className="panel__header">
                  <h2 className="panel__title">Accesos rápidos</h2>
                </div>

                <div className="quick-actions">
                  <Link to="/gestion/fichas-trimestre" className="btn btn--secondary">
                    Programar ficha en trimestre
                  </Link>
                  <Link to="/gestion/fichas" className="btn btn--secondary">
                    Fichas y aprendices
                  </Link>
                  <Link to="/gestion/resultados" className="btn btn--secondary">
                    Resultados de aprendizaje
                  </Link>
                </div>
              </div>

              <div className="panel">
                <div className="panel__header">
                  <h2 className="panel__title">Trimestres activos</h2>
                </div>

                <TrimestresActivos trimestres={resumen.trimestres_activos} />
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}

export default CoordinadorDashboard
