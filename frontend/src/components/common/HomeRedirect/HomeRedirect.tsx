import { Navigate } from 'react-router-dom'

import { useAuth } from '../../../hooks/useAuth'
import { HOME_BY_ROLE } from '../../../utils/roles'

/**
 * Cada rol tiene su propio dashboard.
 */
function HomeRedirect() {
  const { user } = useAuth()

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return (
    <Navigate
      to={HOME_BY_ROLE[user.role] ?? '/profile'}
      replace
    />
  )
}

export default HomeRedirect
