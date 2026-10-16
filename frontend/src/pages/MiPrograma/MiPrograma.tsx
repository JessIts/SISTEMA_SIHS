import { useEffect, useState } from 'react'

import PageHeader from '../../components/common/PageHeader/PageHeader'

import { getMisProgramas } from '../../services/mi.service'
import type { MiPrograma as Programa } from '../../types/mi.types'
import { errorMessage } from '../../utils/format'

import './MiPrograma.css'

/**
 * Programa(s) del aprendiz o instructor con sus competencias
 * y resultados de aprendizaje. Solo lectura.
 */
function MiPrograma() {
  const [programas, setProgramas] = useState<Programa[] | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getMisProgramas()
      .then(setProgramas)
      .catch((loadError) =>
        setError(errorMessage(loadError, 'No fue posible cargar tu programa.')),
      )
  }, [])

  return (
    <section className="mi-programa">
      <PageHeader
        title={programas && programas.length > 1 ? 'Mis programas' : 'Mi programa'}
        description="Competencias y resultados de aprendizaje de tu programa de formación."
      />

      {error && <p className="panel__error">{error}</p>}

      {programas === null && !error && <p className="panel__muted">Cargando...</p>}

      {programas && programas.length === 0 && (
        <div className="panel">
          <p className="panel__muted">
            No tienes un programa asociado todavía.
          </p>
        </div>
      )}

      <div className="dashboard-stack">
        {programas?.map((programa) => {
          const totalResultados = programa.competencias.reduce(
            (total, competencia) => total + competencia.resultados.length,
            0,
          )

          return (
            <article key={programa.uuid} className="panel">
              <div className="mi-programa__head">
                <span className="mi-programa__code">{programa.codigo}</span>
                <h2>{programa.nombre}</h2>
                <p>
                  {programa.nivel ?? 'Nivel no definido'} · {programa.coordinacion.nombre} ·{' '}
                  {programa.competencias.length} competencia{programa.competencias.length === 1 ? '' : 's'} ·{' '}
                  {totalResultados} resultado{totalResultados === 1 ? '' : 's'}
                </p>
              </div>

              {programa.competencias.length === 0 ? (
                <p className="panel__muted">El programa aún no tiene competencias registradas.</p>
              ) : (
                <div className="mi-programa__competencias">
                  {programa.competencias.map((competencia, index) => (
                    <details key={competencia.uuid} open={index === 0}>
                      <summary>
                        <span className="mi-programa__comp-code">{competencia.codigo}</span>
                        <span>{competencia.descripcion}</span>
                        <span className="mi-programa__count">
                          {competencia.resultados.length}
                        </span>
                      </summary>

                      {competencia.resultados.length === 0 ? (
                        <p className="panel__muted">Sin resultados de aprendizaje.</p>
                      ) : (
                        <ol className="mi-programa__resultados">
                          {competencia.resultados.map((resultado) => (
                            <li key={resultado.uuid}>
                              <strong>{resultado.codigo}</strong>
                              <span>{resultado.descripcion}</span>
                            </li>
                          ))}
                        </ol>
                      )}
                    </details>
                  ))}
                </div>
              )}
            </article>
          )
        })}
      </div>
    </section>
  )
}

export default MiPrograma
