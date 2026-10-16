import { Outlet } from 'react-router-dom'

import './AuthLayout.css'

function AuthLayout() {
  return (
    <div className="auth-layout">

      <main className="auth-layout__main">

        <div className="auth-layout__brand">
          <div className="auth-layout__logo">
            SIHS
          </div>

          <h1 className="auth-layout__title">
            Sistema de Información
          </h1>

          <p className="auth-layout__subtitle">
            Plataforma de gestión institucional
          </p>
        </div>

        <div className="auth-layout__content">
          <Outlet />
        </div>

        <footer className="auth-layout__footer">
          <span>SIHS</span>
          <span>© 2026</span>
        </footer>

      </main>

    </div>
  )
}

export default AuthLayout