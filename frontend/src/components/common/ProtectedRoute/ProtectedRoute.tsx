import { Navigate, Outlet } from 'react-router-dom'

import { useAuth } from '../../../hooks/useAuth'

import type { UserRole } from '../../../types/role.types'

interface ProtectedRouteProps {
  allowedRoles?: UserRole[]
}

function ProtectedRoute({
  allowedRoles,
}: ProtectedRouteProps) {
  const {
    user,
    isAuthenticated,
    loading,
  } = useAuth()

  if (loading) {
    return null
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />
  }

  if (
    allowedRoles &&
    !allowedRoles.includes(user.role)
  ) {
    return <Navigate to="/" replace />
  }

  return <Outlet />
}

export default ProtectedRoute