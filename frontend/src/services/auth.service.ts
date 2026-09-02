import { apiRequest } from './api'

import type {
  ApiResponse,
  LoginRequest,
  TokenResponse,
  User,
} from '../types/auth.types'

export async function login(
  credentials: LoginRequest,
): Promise<TokenResponse> {
  const response = await apiRequest<
    ApiResponse<TokenResponse>
  >(
    '/auth/login',
    {
      method: 'POST',
      body: JSON.stringify(credentials),
    },
  )

  return response.data
}

export async function getCurrentUser(
  token: string,
): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    '/users/me',
    {
      method: 'GET',
    },
    token,
  )

  return response.data
}