import { apiRequest } from './api'

import type { ApiResponse } from '../types/auth.types'
import type { Paginated } from '../types/common.types'

export type QueryParams = Record<
  string,
  string | number | undefined | null
>

export function buildQuery(params: QueryParams = {}): string {
  const search = new URLSearchParams()

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      search.set(key, String(value))
    }
  })

  const query = search.toString()

  return query ? `?${query}` : ''
}

/**
 * Operaciones estándar que expone cada recurso del backend:
 *   GET    /recurso            (paginado + filtros)
 *   GET    /recurso/inactive
 *   GET    /recurso/{uuid}
 *   POST   /recurso
 *   PUT    /recurso/{uuid}
 *   DELETE /recurso/{uuid}     (desactiva; en horarios elimina)
 *   PATCH  /recurso/{uuid}/activate
 */
export interface CrudService<T, TCreate, TUpdate> {
  resource: string
  list: (params?: QueryParams) => Promise<Paginated<T>>
  listAll: (params?: QueryParams) => Promise<T[]>
  listInactive: () => Promise<T[]>
  get: (uuid: string) => Promise<T>
  create: (data: TCreate) => Promise<T>
  update: (uuid: string, data: TUpdate) => Promise<T>
  remove: (uuid: string) => Promise<void>
  activate: (uuid: string) => Promise<T>
}

export function createCrudService<
  T,
  TCreate,
  TUpdate = Partial<TCreate>,
>(resource: string): CrudService<T, TCreate, TUpdate> {
  return {
    resource,

    async list(params = {}) {
      const response = await apiRequest<ApiResponse<Paginated<T>>>(
        `${resource}${buildQuery({ page: 1, limit: 10, ...params })}`,
        { method: 'GET' },
      )

      return response.data
    },

    /**
     * Trae hasta 100 registros activos (para llenar selects).
     */
    async listAll(params = {}) {
      const response = await apiRequest<ApiResponse<Paginated<T>>>(
        `${resource}${buildQuery({ ...params, page: 1, limit: 100 })}`,
        { method: 'GET' },
      )

      return response.data.items
    },

    async listInactive() {
      const response = await apiRequest<ApiResponse<T[]>>(
        `${resource}/inactive`,
        { method: 'GET' },
      )

      return response.data
    },

    async get(uuid) {
      const response = await apiRequest<ApiResponse<T>>(
        `${resource}/${uuid}`,
        { method: 'GET' },
      )

      return response.data
    },

    async create(data) {
      const response = await apiRequest<ApiResponse<T>>(
        resource,
        {
          method: 'POST',
          body: JSON.stringify(data),
        },
      )

      return response.data
    },

    async update(uuid, data) {
      const response = await apiRequest<ApiResponse<T>>(
        `${resource}/${uuid}`,
        {
          method: 'PUT',
          body: JSON.stringify(data),
        },
      )

      return response.data
    },

    async remove(uuid) {
      await apiRequest<void>(
        `${resource}/${uuid}`,
        { method: 'DELETE' },
      )
    },

    async activate(uuid) {
      const response = await apiRequest<ApiResponse<T>>(
        `${resource}/${uuid}/activate`,
        { method: 'PATCH' },
      )

      return response.data
    },
  }
}
