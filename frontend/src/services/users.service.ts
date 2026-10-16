import { apiRequest } from './api'

import { buildQuery } from './crud.service'

import type {
  ApiResponse,
  User,
  UserCreate,
} from '../types/auth.types'
import type { UserRole } from '../types/role.types'

export interface UserPagination {
  items: User[]
  page: number
  limit: number
  total: number
  pages: number
}

export interface UserUpdate {
  name?: string
  email?: string
  phone?: string
  document_number?: string
  password?: string
}

export async function getUsers(
  page = 1,
  limit = 10,
  role?: UserRole,
): Promise<UserPagination> {
  const response = await apiRequest<
    ApiResponse<UserPagination>
  >(
    `/users${buildQuery({ page, limit, role })}`,
    {
      method: 'GET',
    },
  )

  return response.data
}

export async function createUser(
  data: UserCreate,
): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    '/users',
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
  )

  return response.data
}

export async function updateUser(
  userUuid: string,
  data: UserUpdate,
): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    `/users/${userUuid}`,
    {
      method: 'PUT',
      body: JSON.stringify(data),
    },
  )

  return response.data
}

export async function deactivateUser(
  userUuid: string,
): Promise<void> {
  await apiRequest<void>(
    `/users/${userUuid}`,
    {
      method: 'DELETE',
    },
  )
}

export async function activateUser(
  userUuid: string,
): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    `/users/${userUuid}/activate`,
    {
      method: 'PATCH',
    },
  )

  return response.data
}

export async function changeUserRole(
  userUuid: string,
  role: UserRole,
): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    `/users/${userUuid}/role`,
    {
      method: 'PATCH',
      body: JSON.stringify({ role }),
    },
  )

  return response.data
}
