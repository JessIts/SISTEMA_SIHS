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

import CoordinadorDashboard from '../pages/CoordinadorDashboard/CoordinadorDashboard'
import InstructorDashboard from '../pages/InstructorDashboard/InstructorDashboard'
import AprendizDashboard from '../pages/AprendizDashboard/AprendizDashboard'
import MiPrograma from '../pages/MiPrograma/MiPrograma'
import MiHorario from '../pages/MiHorario/MiHorario'

import Sedes from '../pages/Sedes/Sedes'
import Ambientes from '../pages/Ambientes/Ambientes'
import Coordinaciones from '../pages/Coordinaciones/Coordinaciones'
import Programas from '../pages/Programas/Programas'
import Competencias from '../pages/Competencias/Competencias'
import ResultadosAprendizaje from '../pages/ResultadosAprendizaje/ResultadosAprendizaje'
import ActividadesAprendizaje from '../pages/ActividadesAprendizaje/ActividadesAprendizaje'
import Jornadas from '../pages/Jornadas/Jornadas'
import FranjasHorarias from '../pages/FranjasHorarias/FranjasHorarias'
import DiasSemana from '../pages/DiasSemana/DiasSemana'
import Trimestres from '../pages/Trimestres/Trimestres'
import Fichas from '../pages/Fichas/Fichas'
import FichasTrimestre from '../pages/FichasTrimestre/FichasTrimestre'
import Horarios from '../pages/Horarios/Horarios'

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

          <Route element={<DashboardLayout />}>

            {/* =========================
                ADMINISTRADOR
            ========================== */}

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['admin']}
                />
              }
            >
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

            {/* =========================
                COORDINADOR
            ========================== */}

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['coordinador']}
                />
              }
            >
              <Route
                path="/coordinador"
                element={<CoordinadorDashboard />}
              />
            </Route>

            {/* =========================
                GESTIÓN (admin y coordinador)
                Datos no personales: solo estos
                roles pueden modificarlos.
            ========================== */}

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['admin', 'coordinador']}
                />
              }
            >
              <Route path="/gestion/sedes" element={<Sedes />} />
              <Route path="/gestion/ambientes" element={<Ambientes />} />
              <Route path="/gestion/coordinaciones" element={<Coordinaciones />} />
              <Route path="/gestion/programas" element={<Programas />} />
              <Route path="/gestion/competencias" element={<Competencias />} />
              <Route path="/gestion/resultados" element={<ResultadosAprendizaje />} />
              <Route path="/gestion/actividades" element={<ActividadesAprendizaje />} />
              <Route path="/gestion/jornadas" element={<Jornadas />} />
              <Route path="/gestion/franjas" element={<FranjasHorarias />} />
              <Route path="/gestion/dias" element={<DiasSemana />} />
              <Route path="/gestion/trimestres" element={<Trimestres />} />
              <Route path="/gestion/fichas" element={<Fichas />} />
              <Route path="/gestion/fichas-trimestre" element={<FichasTrimestre />} />
              <Route path="/gestion/horarios" element={<Horarios />} />
            </Route>

            {/* =========================
                INSTRUCTOR Y APRENDIZ
                (solo su información)
            ========================== */}

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['instructor']}
                />
              }
            >
              <Route
                path="/instructor"
                element={<InstructorDashboard />}
              />
            </Route>

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['aprendiz']}
                />
              }
            >
              <Route
                path="/aprendiz"
                element={<AprendizDashboard />}
              />
            </Route>

            <Route
              element={
                <ProtectedRoute
                  allowedRoles={['instructor', 'aprendiz']}
                />
              }
            >
              <Route
                path="/mi-programa"
                element={<MiPrograma />}
              />

              <Route
                path="/mi-horario/:fichaTrimestreUuid"
                element={<MiHorario />}
              />
            </Route>

            {/* =========================
                ÁREA DEL USUARIO (todos)
            ========================== */}

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
