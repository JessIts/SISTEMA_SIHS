import { useEffect, useState } from 'react'

import PageHeader from '../../components/common/PageHeader/PageHeader'
import ProgramacionesTable from '../../components/dashboard/ProgramacionesTable/ProgramacionesTable'
import StatCard from '../../components/dashboard/StatCard/StatCard'
import TrimestresActivos from '../../components/dashboard/TrimestresActivos/TrimestresActivos'

import { useAuth } from '../../hooks/useAuth'
import { getDashboardResumen } from '../../services/mi.service'
import type { DashboardResumen } from '../../types/mi.types'
import type { UserRole } from '../../types/role.types'
import { errorMessage } from '../../utils/format'
import { ROLE_LABELS } from '../../utils/roles'

import './Dashboard.css'

const ROLES_ORDEN: UserRole[] = ['admin', 'coordinador', 'instructor', 'aprendiz', 'user']

/**
 * Dashboard del administrador: visión general del sistema,
 * cuentas por rol y avance de los horarios.
 */
function Dashboard() {
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

  const totalUsuarios = resumen
    ? Object.values(resumen.usuarios).reduce((total, value) => total + value, 0)
    : 0

  const maxUsuarios = resumen
    ? Math.max(...Object.values(resumen.usuarios), 1)
    : 1

  return (
    <section className="dashboard-page">
      <PageHeader
        title={`Hola, ${user?.name ?? ''}`}
        description="Panel de administración: cuentas, estructura académica y avance de los horarios."
      />

      {error && <p className="panel__error">{error}</p>}

      {!resumen && !error && <p className="panel__muted">Cargando resumen...</p>}

      {resumen && (
        <div className="dashboard-stack">
          <div className="stat-grid">
            <StatCard label="Usuarios activos" value={totalUsuarios} to="/users" />
            <StatCard label="Fichas" value={resumen.conteos.fichas} to="/gestion/fichas" />
            <StatCard label="Programas" value={resumen.conteos.programas} to="/gestion/programas" />
            <StatCard label="Sedes" value={resumen.conteos.sedes} to="/gestion/sedes" />
            <StatCard label="Ambientes" value={resumen.conteos.ambientes} to="/gestion/ambientes" />
            <StatCard
              label="Clases asignadas"
              value={resumen.conteos.horarios}
              hint="casillas de horario"
              to="/gestion/horarios"
            />
          </div>

          <div className="dashboard-columns">
            <div className="panel">
              <div className="panel__header">
                <div>
                  <h2 className="panel__title">Horarios en curso</h2>
                  <p className="panel__subtitle">
                    Fichas de los trimestres vigentes, primero las que tienen menos horas armadas.
                  </p>
                </div>
              </div>

              <ProgramacionesTable programaciones={resumen.programaciones} />
            </div>

            <div className="dashboard-stack">
              <div className="panel">
                <div className="panel__header">
                  <h2 className="panel__title">Usuarios por rol</h2>
                </div>

                <ul className="role-bars">
                  {ROLES_ORDEN.map((role) => (
                    <li key={role}>
                      <span>{ROLE_LABELS[role]}</span>
                      <span className="role-bars__track">
                        <span style={{ width: `${(resumen.usuarios[role] / maxUsuarios) * 100}%` }} />
                      </span>
                      <strong>{resumen.usuarios[role]}</strong>
                    </li>
                  ))}
                </ul>
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

export default Dashboard
