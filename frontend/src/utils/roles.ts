import type { UserRole } from '../types/role.types'

export const ROLE_LABELS: Record<UserRole, string> = {
  admin: 'Administrador',
  coordinador: 'Coordinador',
  instructor: 'Instructor',
  aprendiz: 'Aprendiz',
  user: 'Usuario',
}

/**
 * Roles que pueden modificar datos que NO son personales
 * (sedes, programas, fichas, horarios...).
 */
export const MANAGER_ROLES: UserRole[] = [
  'admin',
  'coordinador',
]

export const HOME_BY_ROLE: Record<UserRole, string> = {
  admin: '/admin',
  coordinador: '/coordinador',
  instructor: '/instructor',
  aprendiz: '/aprendiz',
  user: '/profile',
}

export function isManager(role?: UserRole): boolean {
  return role !== undefined && MANAGER_ROLES.includes(role)
}
