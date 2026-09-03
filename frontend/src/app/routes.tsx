import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom'

import AuthLayout from '../layouts/AuthLayout/AuthLayout'
import DashboardLayout from '../layouts/DashboardLayout/DashboardLayout'

import ProtectedRoute from '../components/common/ProtectedRoute/ProtectedRoute'
import HomeRedirect from '../components/common/HomeRedirect/HomeRedirect'

import Login from '../pages/Login/Login'
import Register from '../pages/Register/Register'
import Dashboard from '../pages/Dashboard/Dashboard'
import Users from '../pages/Users/Users'
import CreateUser from '../pages/CreateUser/CreateUser'
import EditUser from '../pages/EditUser/EditUser'
import NotFound from '../pages/NotFound/NotFound'
import Profile from '../pages/Profile/Profile'

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        {/* =========================
            RUTAS PÚBLICAS
        ========================== */}

        <Route element={<AuthLayout />}>
          <Route
            path="/login"
            element={<Login />}
          />

          <Route
            path="/register"
            element={<Register />}
          />
        </Route>


        {/* =========================
            RUTAS AUTENTICADAS
        ========================== */}

        <Route element={<ProtectedRoute />}>

          {/* Punto de entrada según rol */}
          <Route
            path="/"
            element={<HomeRedirect />}
          />

          {/* =========================
              RUTAS ADMINISTRATIVAS
          ========================== */}

          <Route
            element={
              <ProtectedRoute
                allowedRoles={['admin']}
              />
            }
          >
            <Route element={<DashboardLayout />}>

              <Route
                path="/admin"
                element={<Dashboard />}
              />

              <Route
                path="/users"
                element={<Users />}
              />

              <Route
                path="/users/create"
                element={<CreateUser />}
              />

              <Route
                path="/users/:userUuid/edit"
                element={<EditUser />}
              />

            </Route>
          </Route>

          {/* =========================
              ÁREA DEL USUARIO
          ========================== */}

          <Route element={<DashboardLayout />}>

            <Route
              path="/profile"
              element={<Profile />}
            />

          </Route>

        </Route>


        {/* =========================
            404
        ========================== */}

        <Route
          path="*"
          element={<NotFound />}
        />

      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes