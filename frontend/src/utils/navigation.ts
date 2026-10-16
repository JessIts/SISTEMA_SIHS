import type { UserRole } from '../types/role.types'

export interface NavLinkItem {
  to: string
  label: string
}

export interface NavSection {
  title?: string
  links: NavLinkItem[]
}

/**
 * Secciones de gestión: solo admin y coordinador
 * (datos que no son personales).
 */
const GESTION: NavSection[] = [
  {
    title: 'Programación',
    links: [
      { to: '/gestion/horarios', label: 'Horarios' },
      { to: '/gestion/fichas-trimestre', label: 'Fichas por trimestre' },
      { to: '/gestion/fichas', label: 'Fichas' },
    ],
  },
  {
    title: 'Académico',
    links: [
      { to: '/gestion/coordinaciones', label: 'Coordinaciones' },
      { to: '/gestion/programas', label: 'Programas' },
      { to: '/gestion/competencias', label: 'Competencias' },
      { to: '/gestion/resultados', label: 'Resultados de aprendizaje' },
      { to: '/gestion/actividades', label: 'Actividades' },
    ],
  },
  {
    title: 'Calendario',
    links: [
      { to: '/gestion/trimestres', label: 'Trimestres' },
      { to: '/gestion/jornadas', label: 'Jornadas' },
      { to: '/gestion/franjas', label: 'Franjas horarias' },
      { to: '/gestion/dias', label: 'Días de la semana' },
    ],
  },
  {
    title: 'Infraestructura',
    links: [
      { to: '/gestion/sedes', label: 'Sedes' },
      { to: '/gestion/ambientes', label: 'Ambientes' },
    ],
  },
]

const CUENTA: NavSection = {
  title: 'Cuenta',
  links: [{ to: '/profile', label: 'Mi perfil' }],
}

export const NAVIGATION: Record<UserRole, NavSection[]> = {
  admin: [
    {
      links: [
        { to: '/admin', label: 'Dashboard' },
        { to: '/users', label: 'Usuarios' },
      ],
    },
    ...GESTION,
    CUENTA,
  ],
  coordinador: [
    { links: [{ to: '/coordinador', label: 'Dashboard' }] },
    ...GESTION,
    CUENTA,
  ],
  instructor: [
    {
      links: [
        { to: '/instructor', label: 'Dashboard' },
        { to: '/mi-programa', label: 'Mis programas' },
      ],
    },
    CUENTA,
  ],
  aprendiz: [
    {
      links: [
        { to: '/aprendiz', label: 'Dashboard' },
        { to: '/mi-programa', label: 'Mi programa' },
      ],
    },
    CUENTA,
  ],
  user: [CUENTA],
}
