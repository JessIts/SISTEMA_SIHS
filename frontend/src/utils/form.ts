import type { FormValues, SelectOption } from '../components/crud/EntityForm/EntityForm'

/** Lee un campo del formulario como texto (sin espacios sobrantes). */
export function text(values: FormValues, name: string): string {
  const value = values[name]

  return typeof value === 'string' ? value.trim() : ''
}

/** Texto opcional: vacío -> null */
export function optionalText(values: FormValues, name: string): string | null {
  return text(values, name) || null
}

export function integer(values: FormValues, name: string): number {
  return Number.parseInt(text(values, name), 10)
}

/** Número opcional: vacío -> null */
export function optionalInteger(values: FormValues, name: string): number | null {
  const value = text(values, name)

  return value ? Number.parseInt(value, 10) : null
}

export function list(values: FormValues, name: string): string[] {
  const value = values[name]

  return Array.isArray(value) ? value : []
}

/** Convierte una lista de entidades en opciones para un <select>. */
export function toSelectOptions<T extends { uuid: string }>(
  items: T[],
  label: (item: T) => string,
): SelectOption[] {
  return items.map((item) => ({
    value: item.uuid,
    label: label(item),
  }))
}
