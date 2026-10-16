export interface Paginated<T> {
  items: T[]
  page: number
  limit: number
  total: number
  pages: number
}

/**
 * Toda entidad del backend se identifica por su uuid.
 */
export interface Entity {
  uuid: string
  is_active?: boolean
  created_at?: string
}
