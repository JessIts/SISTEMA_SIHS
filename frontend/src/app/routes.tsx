import { BrowserRouter, Routes, Route } from 'react-router-dom'

import AuthLayout from '../layouts/AuthLayout/AuthLayout'
import DashboardLayout from '../layouts/DashboardLayout/DashboardLayout'

import Login from '../pages/Login/Login'
import Dashboard from '../pages/Dashboard/Dashboard'
import NotFound from '../pages/NotFound/NotFound'

export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Rutas públicas */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
        </Route>

        {/* Rutas autenticadas */}
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<Dashboard />} />
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFound />} />

      </Routes>
    </BrowserRouter>
  )
}