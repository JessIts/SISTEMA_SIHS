import { useEffect, useState } from 'react'

import type { SelectOption } from '../../components/crud/EntityForm/EntityForm'

import {
  addAprendizFicha,
  getAprendicesFicha,
  removeAprendizFicha,
} from '../../services/academic.service'
import type { Ficha } from '../../types/academic.types'
import type { User } from '../../types/auth.types'
import { errorMessage } from '../../utils/format'
import { opcionesAprendices } from '../../utils/options'

import './Fichas.css'

interface FichaAprendicesProps {
  ficha: Ficha
}

/**
 * Lista los aprendices de la ficha y permite agregar o retirar.
 * Solo aparecen como opción los usuarios con rol "aprendiz".
 */
function FichaAprendices({ ficha }: FichaAprendicesProps) {
  const [aprendices, setAprendices] = useState<User[]>([])
  const [opciones, setOpciones] = useState<SelectOption[]>([])
  const [seleccion, setSeleccion] = useState('')

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true

    async function load() {
      try {
        const [actuales, disponibles] = await Promise.all([
          getAprendicesFicha(ficha.uuid),
          opcionesAprendices(),
        ])

        if (active) {
          setAprendices(actuales)
          setOpciones(disponibles)
        }
      } catch (loadError) {
        if (active) {
          setError(errorMessage(loadError, 'No fue posible cargar los aprendices.'))
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    load()

    return () => {
      active = false
    }
  }, [ficha.uuid])

  const disponibles = opciones.filter(
    (opcion) => !aprendices.some((aprendiz) => aprendiz.uuid === opcion.value),
  )

  async function handleAdd() {
    if (!seleccion) {
      return
    }

    try {
      setSaving(true)
      setError('')

      setAprendices(await addAprendizFicha(ficha.uuid, seleccion))
      setSeleccion('')
    } catch (addError) {
      setError(errorMessage(addError, 'No fue posible agregar el aprendiz.'))
    } finally {
      setSaving(false)
    }
  }

  async function handleRemove(aprendiz: User) {
    if (!window.confirm(`¿Retirar a ${aprendiz.name} de la ficha ${ficha.codigo}?`)) {
      return
    }

    try {
      setError('')

      await removeAprendizFicha(ficha.uuid, aprendiz.uuid)

      setAprendices((current) =>
        current.filter((item) => item.uuid !== aprendiz.uuid),
      )
    } catch (removeError) {
      setError(errorMessage(removeError, 'No fue posible retirar el aprendiz.'))
    }
  }

  if (loading) {
    return <p className="ficha-aprendices__muted">Cargando aprendices...</p>
  }

  return (
    <div className="ficha-aprendices">
      <div className="ficha-aprendices__add">
        <label htmlFor="aprendiz-select">Agregar aprendiz</label>

        <div className="ficha-aprendices__add-row">
          <select
            id="aprendiz-select"
            value={seleccion}
            onChange={(event) => setSeleccion(event.target.value)}
          >
            <option value="">
              {disponibles.length > 0
                ? 'Selecciona un aprendiz'
                : 'No hay aprendices disponibles'}
            </option>

            {disponibles.map((opcion) => (
              <option key={opcion.value} value={opcion.value}>
                {opcion.label}
              </option>
            ))}
          </select>

          <button
            type="button"
            className="btn btn--primary"
            onClick={handleAdd}
            disabled={!seleccion || saving}
          >
            {saving ? 'Agregando...' : 'Agregar'}
          </button>
        </div>

        <span className="ficha-aprendices__muted">
          Solo aparecen usuarios con rol aprendiz. El rol se asigna en Usuarios.
        </span>
      </div>

      {error && <p className="ficha-aprendices__error">{error}</p>}

      {aprendices.length === 0 ? (
        <p className="ficha-aprendices__muted">La ficha aún no tiene aprendices.</p>
      ) : (
        <table className="ficha-aprendices__table">
          <thead>
            <tr>
              <th>Aprendiz</th>
              <th>Documento</th>
              <th>Correo</th>
              <th aria-label="Acciones" />
            </tr>
          </thead>

          <tbody>
            {aprendices.map((aprendiz) => (
              <tr key={aprendiz.uuid}>
                <td>{aprendiz.name}</td>
                <td>{aprendiz.document_number}</td>
                <td>{aprendiz.email}</td>
                <td>
                  <button
                    type="button"
                    className="btn btn--danger btn--small"
                    onClick={() => handleRemove(aprendiz)}
                  >
                    Retirar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <p className="ficha-aprendices__total">
        {aprendices.length} aprendiz{aprendices.length === 1 ? '' : 'ces'} en formación
      </p>
    </div>
  )
}

export default FichaAprendices
