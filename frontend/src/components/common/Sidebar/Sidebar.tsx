import { NavLink } from 'react-router-dom'

import { useAuth } from '../../../hooks/useAuth'

import './Sidebar.css'

function Sidebar() {
  const { user } = useAuth()

  return (
    <aside className="sidebar">
      <nav className="sidebar__navigation">

        {user?.role === 'admin' && (
          <>
            <NavLink
              to="/admin"
              className={({ isActive }) =>
                `sidebar__link ${
                  isActive
                    ? 'sidebar__link--active'
                    : ''
                }`
              }
            >
              Dashboard
            </NavLink>

            <NavLink
              to="/users"
              className={({ isActive }) =>
                `sidebar__link ${
                  isActive
                    ? 'sidebar__link--active'
                    : ''
                }`
              }
            >
              Usuarios
            </NavLink>
          </>
        )}

        {user?.role === 'user' && (
          <NavLink
            to="/profile"
            className={({ isActive }) =>
              `sidebar__link ${
                isActive
                  ? 'sidebar__link--active'
                  : ''
              }`
            }
          >
            Mi perfil
          </NavLink>
        )}

      </nav>
    </aside>
  )
}

export default Sidebar