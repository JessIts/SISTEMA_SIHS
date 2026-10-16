import { useAuth } from './useAuth'

import { isManager } from '../utils/roles'

/**
 * Permisos derivados del rol del usuario autenticado.
 *  - canManage: admin y coordinador pueden modificar datos no personales.
 *  - isAdmin:   solo el admin gestiona cuentas de usuario.
 */
export function usePermissions() {
  const { user } = useAuth()

  return {
    role: user?.role,
    isAdmin: user?.role === 'admin',
    canManage: isManager(user?.role),
  }
}
