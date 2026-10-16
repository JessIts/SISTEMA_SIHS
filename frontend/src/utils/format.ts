/**
 * "2026-07-09" -> "09/07/2026"
 * Se arma a mano para no sufrir el corrimiento de zona horaria
 * que produce new Date("2026-07-09") (UTC) en Colombia.
 */
export function formatDate(value?: string | null): string {
  if (!value) {
    return '—'
  }

  const [year, month, day] = value.slice(0, 10).split('-')

  return `${day}/${month}/${year}`
}

/** "12:00:00" -> "12:00" */
export function formatTime(value?: string | null): string {
  return value ? value.slice(0, 5) : '—'
}

export function formatTrimestre(trimestre: {
  anio: number
  numero: number
}): string {
  return `${trimestre.anio}-T${trimestre.numero}`
}

export function formatPeriodo(trimestre: {
  fecha_inicio: string
  fecha_fin: string
}): string {
  return `${formatDate(trimestre.fecha_inicio)} – ${formatDate(trimestre.fecha_fin)}`
}

export function formatHoras(value: number): string {
  return Number.isInteger(value)
    ? `${value} h`
    : `${value.toFixed(1)} h`
}

export function errorMessage(
  error: unknown,
  fallback: string,
): string {
  return error instanceof Error ? error.message : fallback
}
