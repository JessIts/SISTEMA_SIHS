import type { UserRole } from './role.types'

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface ApiResponse<T> {
  message: string
  data: T
}

export interface User {
  uuid: string
  name: string
  email: string
  phone: string
  document_number: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export interface UserCreate {
  name: string
  email: string
  phone: string
  document_number: string
  password: string
}