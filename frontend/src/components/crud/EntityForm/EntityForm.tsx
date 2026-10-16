import {
  useEffect,
  useState,
  type ChangeEvent,
  type FormEvent,
} from 'react'

import { errorMessage } from '../../../utils/format'

import './EntityForm.css'

export type FieldType =
  | 'text'
  | 'email'
  | 'textarea'
  | 'number'
  | 'date'
  | 'time'
  | 'select'
  | 'multiselect'

export interface SelectOption {
  value: string
  label: string
}

export interface FieldConfig {
  name: string
  label: string
  type?: FieldType
  required?: boolean
  placeholder?: string
  help?: string
  min?: number
  max?: number
  minLength?: number
  maxLength?: number
  /** Opciones fijas (select / multiselect) */
  options?: SelectOption[]
  /** Opciones que se cargan del backend (select / multiselect) */
  loadOptions?: () => Promise<SelectOption[]>
  /** Solo se puede escribir al crear (en edición queda bloqueado) */
  createOnly?: boolean
  /** Ocupa las dos columnas del formulario */
  fullWidth?: boolean
}

export type FormValues = Record<string, string | string[]>

interface EntityFormProps {
  fields: FieldConfig[]
  initialValues: FormValues
  mode: 'create' | 'edit'
  submitLabel?: string
  onSubmit: (values: FormValues) => Promise<void>
  onCancel: () => void
}

function EntityForm({
  fields,
  initialValues,
  mode,
  submitLabel,
  onSubmit,
  onCancel,
}: EntityFormProps) {
  const [values, setValues] = useState<FormValues>(initialValues)

  const [options, setOptions] = useState<
    Record<string, SelectOption[]>
  >({})

  const [loadingOptions, setLoadingOptions] = useState(true)

  const [saving, setSaving] = useState(false)

  const [error, setError] = useState('')

  useEffect(() => {
    let active = true

    async function loadAllOptions() {
      try {
        const entries = await Promise.all(
          fields
            .filter((field) => field.loadOptions)
            .map(async (field) => [
              field.name,
              await field.loadOptions!(),
            ] as const),
        )

        if (active) {
          setOptions(Object.fromEntries(entries))
        }
      } catch (loadError) {
        if (active) {
          setError(
            errorMessage(
              loadError,
              'No fue posible cargar las opciones del formulario.',
            ),
          )
        }
      } finally {
        if (active) {
          setLoadingOptions(false)
        }
      }
    }

    loadAllOptions()

    return () => {
      active = false
    }
  }, [fields])

  function handleChange(
    event: ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) {
    const { name, value } = event.target

    setValues((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function handleToggle(name: string, value: string) {
    setValues((current) => {
      const selected = (current[name] as string[] | undefined) ?? []

      return {
        ...current,
        [name]: selected.includes(value)
          ? selected.filter((item) => item !== value)
          : [...selected, value],
      }
    })
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    try {
      setSaving(true)
      setError('')

      await onSubmit(values)
    } catch (submitError) {
      setError(
        errorMessage(submitError, 'No fue posible guardar los cambios.'),
      )
    } finally {
      setSaving(false)
    }
  }

  function renderField(field: FieldConfig) {
    const type = field.type ?? 'text'
    const id = `field-${field.name}`
    const disabled = mode === 'edit' && field.createOnly
    const value = values[field.name] ?? (type === 'multiselect' ? [] : '')
    const fieldOptions = field.options ?? options[field.name] ?? []

    if (type === 'select') {
      return (
        <select
          id={id}
          name={field.name}
          value={value as string}
          onChange={handleChange}
          required={field.required}
          disabled={disabled || (loadingOptions && !!field.loadOptions)}
        >
          <option value="">
            {loadingOptions && field.loadOptions
              ? 'Cargando...'
              : field.placeholder ?? 'Selecciona una opción'}
          </option>

          {fieldOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      )
    }

    if (type === 'multiselect') {
      const selected = value as string[]

      return (
        <div className="entity-form__checklist" id={id}>
          {loadingOptions && field.loadOptions && (
            <span className="entity-form__muted">Cargando...</span>
          )}

          {!loadingOptions && fieldOptions.length === 0 && (
            <span className="entity-form__muted">No hay opciones disponibles.</span>
          )}

          {fieldOptions.map((option) => (
            <label key={option.value} className="entity-form__check">
              <input
                type="checkbox"
                checked={selected.includes(option.value)}
                onChange={() => handleToggle(field.name, option.value)}
                disabled={disabled}
              />
              {option.label}
            </label>
          ))}
        </div>
      )
    }

    if (type === 'textarea') {
      return (
        <textarea
          id={id}
          name={field.name}
          value={value as string}
          onChange={handleChange}
          required={field.required}
          placeholder={field.placeholder}
          minLength={field.minLength}
          maxLength={field.maxLength}
          rows={3}
          disabled={disabled}
        />
      )
    }

    return (
      <input
        id={id}
        name={field.name}
        type={type}
        value={value as string}
        onChange={handleChange}
        required={field.required}
        placeholder={field.placeholder}
        min={field.min}
        max={field.max}
        minLength={field.minLength}
        maxLength={field.maxLength}
        disabled={disabled}
      />
    )
  }

  return (
    <form className="entity-form" onSubmit={handleSubmit}>
      <div className="entity-form__grid">
        {fields.map((field) => (
          <div
            key={field.name}
            className={`entity-form__group ${
              field.fullWidth || field.type === 'textarea' || field.type === 'multiselect'
                ? 'entity-form__group--full'
                : ''
            }`}
          >
            <label htmlFor={`field-${field.name}`}>
              {field.label}
              {field.required && <span className="entity-form__required">*</span>}
            </label>

            {renderField(field)}

            {field.help && (
              <span className="entity-form__help">{field.help}</span>
            )}
          </div>
        ))}
      </div>

      {error && <p className="entity-form__error">{error}</p>}

      <div className="entity-form__actions">
        <button
          type="button"
          className="btn btn--secondary"
          onClick={onCancel}
          disabled={saving}
        >
          Cancelar
        </button>

        <button
          type="submit"
          className="btn btn--primary"
          disabled={saving}
        >
          {saving
            ? 'Guardando...'
            : submitLabel ?? (mode === 'create' ? 'Crear' : 'Guardar cambios')}
        </button>
      </div>
    </form>
  )
}

export default EntityForm
