import { apiRequest } from './api'

import type {
  ApiResponse,
  LoginRequest,
  User,
} from '../types/auth.types'

export interface RegisterRequest {
  name: string
  email: string
  phone: string
  document_number: string
  password: string
}

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

export async function register(
  data: RegisterRequest,
): Promise<User> {
  const response = await apiRequest<
    ApiResponse<User>
  >(
    '/auth/register',
    {
      method: 'POST',
      body: JSON.stringify(data),
    },
  )

  return response.data
}

export async function getCurrentUser(): Promise<User> {
  const response = await apiRequest<ApiResponse<User>>(
    '/users/me',
    {
      method: 'GET',
    },
  )

  return response.data
}

export interface ProfileUpdateRequest {
  name?: string
  email?: string
  phone?: string
  document_number?: string
  password?: string
}

export async function updateMyProfile(
  data: ProfileUpdateRequest,
): Promise<User> {
  const response = await apiRequest<ApiResponse<User>>(
    '/users/me',
    {
      method: 'PUT',
      body: JSON.stringify(data),
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