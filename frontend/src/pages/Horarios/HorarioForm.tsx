import { useState, type FormEvent } from 'react'

import type { SelectOption } from '../../components/crud/EntityForm/EntityForm'

import type { ModalidadClase } from '../../types/academic.types'
import { errorMessage } from '../../utils/format'
import { MODALIDAD_CLASE_LABELS, toOptions } from '../../utils/labels'

export interface HorarioFormValues {
  dia_uuid: string
  franja_uuid: string
  resultado_uuid: string
  instructor_uuid: string
  modalidad: ModalidadClase
  ambiente_uuid: string
  observacion: string
}

export interface HorarioFormOptions {
  dias: SelectOption[]
  franjas: SelectOption[]
  resultados: SelectOption[]
  instructores: SelectOption[]
  ambientes: SelectOption[]
}

interface HorarioFormProps {
  initialValues: HorarioFormValues
  options: HorarioFormOptions
  isEdit: boolean
  onSubmit: (values: HorarioFormValues) => Promise<void>
  onDelete?: () => Promise<void>
  onCancel: () => void
}

const MODALIDADES = toOptions(MODALIDAD_CLASE_LABELS)

/**
 * Formulario de una casilla del horario.
 * Si la clase es sincrónica no se pide ambiente (el backend lo exige así).
 */
function HorarioForm({
  initialValues,
  options,
  isEdit,
  onSubmit,
  onDelete,
  onCancel,
}: HorarioFormProps) {
  const [values, setValues] = useState(initialValues)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  function set<K extends keyof HorarioFormValues>(name: K, value: HorarioFormValues[K]) {
    setValues((current) => ({ ...current, [name]: value }))
  }

  async function run(action: () => Promise<void>, fallback: string) {
    try {
      setSaving(true)
      setError('')

      await action()
    } catch (actionError) {
      setError(errorMessage(actionError, fallback))
    } finally {
      setSaving(false)
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    void run(() => onSubmit(values), 'No fue posible guardar la clase.')
  }

  const presencial = values.modalidad === 'presencial'

  return (
    <form className="entity-form" onSubmit={handleSubmit}>
      <div className="entity-form__grid">
        <div className="entity-form__group">
          <label htmlFor="horario-dia">Día</label>
          <select
            id="horario-dia"
            value={values.dia_uuid}
            onChange={(event) => set('dia_uuid', event.target.value)}
            required
          >
            {options.dias.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div className="entity-form__group">
          <label htmlFor="horario-franja">Franja</label>
          <select
            id="horario-franja"
            value={values.franja_uuid}
            onChange={(event) => set('franja_uuid', event.target.value)}
            required
          >
            {options.franjas.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div className="entity-form__group entity-form__group--full">
          <label htmlFor="horario-resultado">
            Temática (resultado de aprendizaje)<span className="entity-form__required">*</span>
          </label>
          <select
            id="horario-resultado"
            value={values.resultado_uuid}
            onChange={(event) => set('resultado_uuid', event.target.value)}
            required
          >
            <option value="">
              {options.resultados.length
                ? 'Selecciona la temática'
                : 'El programa no tiene resultados de aprendizaje'}
            </option>
            {options.resultados.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div className="entity-form__group entity-form__group--full">
          <label htmlFor="horario-instructor">
            Instructor<span className="entity-form__required">*</span>
          </label>
          <select
            id="horario-instructor"
            value={values.instructor_uuid}
            onChange={(event) => set('instructor_uuid', event.target.value)}
            required
          >
            <option value="">
              {options.instructores.length
                ? 'Selecciona el instructor'
                : 'No hay usuarios con rol instructor'}
            </option>
            {options.instructores.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div className="entity-form__group">
          <label htmlFor="horario-modalidad">Modalidad</label>
          <select
            id="horario-modalidad"
            value={values.modalidad}
            onChange={(event) => set('modalidad', event.target.value as ModalidadClase)}
          >
            {MODALIDADES.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div className="entity-form__group">
          <label htmlFor="horario-ambiente">
            Ambiente{presencial && <span className="entity-form__required">*</span>}
          </label>
          <select
            id="horario-ambiente"
            value={presencial ? values.ambiente_uuid : ''}
            onChange={(event) => set('ambiente_uuid', event.target.value)}
            required={presencial}
            disabled={!presencial}
          >
            <option value="">
              {presencial ? 'Selecciona el ambiente' : 'No aplica (sincrónico)'}
            </option>
            {options.ambientes.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>

        <div className="entity-form__group entity-form__group--full">
          <label htmlFor="horario-observacion">Observación</label>
          <textarea
            id="horario-observacion"
            value={values.observacion}
            onChange={(event) => set('observacion', event.target.value)}
            maxLength={255}
            rows={2}
          />
        </div>
      </div>

      {error && <p className="entity-form__error">{error}</p>}

      <div className="entity-form__actions horario-form__actions">
        {isEdit && onDelete && (
          <button
            type="button"
            className="btn btn--danger horario-form__delete"
            disabled={saving}
            onClick={() => {
              if (window.confirm('¿Eliminar esta clase del horario? La casilla quedará libre.')) {
                void run(onDelete, 'No fue posible eliminar la clase.')
              }
            }}
          >
            Eliminar clase
          </button>
        )}

        <button type="button" className="btn btn--secondary" onClick={onCancel} disabled={saving}>
          Cancelar
        </button>

        <button type="submit" className="btn btn--primary" disabled={saving}>
          {saving ? 'Guardando...' : isEdit ? 'Guardar cambios' : 'Asignar clase'}
        </button>
      </div>
    </form>
  )
}

export default HorarioForm
