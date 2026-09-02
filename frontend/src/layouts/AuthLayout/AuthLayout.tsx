import { Outlet } from 'react-router-dom'
import './AuthLayout.css'

function AuthLayout() {
  return (
    <div className="auth-layout">
      <main className="auth-layout__content">
        <Outlet />
      </main>
    </div>
  )
}

export default AuthLayout