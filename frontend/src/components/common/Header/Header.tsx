import { useAuth } from '../../../hooks/useAuth'

import './Header.css'

function Header() {
  const { user, logout } = useAuth()

  return (
    <header className="header">

      <div className="header__brand">
        <span className="header__logo">
          SIHS
        </span>

        <span className="header__system-name">
          Sistema de Información
        </span>
      </div>

      <div className="header__user">
        <span className="header__user-name">
          {user?.name}
        </span>

        <span className="header__user-role">
          {user?.role}
        </span>

        <button
          type="button"
          onClick={logout}
          className="header__logout"
        >
          Cerrar sesión
        </button>
      </div>

    </header>
  )
}

export default Header