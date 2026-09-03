import { apiRequest } from './api'

import type {
  ApiResponse,
  LoginRequest,
  User,
} from '../types/auth.types'

export async function login(
  credentials: LoginRequest,
): Promise<void> {
  await apiRequest<
    ApiResponse<{
      authenticated: boolean
    }>
  >(
    '/auth/login',
    {
      method: 'POST',
      body: JSON.stringify(credentials),
    },
  )
}

export async function getCurrentUser(): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    '/users/me',
    {
      method: 'GET',
    },
  )

  return response.data
}

export async function logout(): Promise<void> {
  await apiRequest<
    ApiResponse<{
      authenticated: boolean
    }>
  >(
    '/auth/logout',
    {
      method: 'POST',
    },
  )
}