import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'

import {
  getCurrentUser,
  login as loginService,
  logout as logoutService,
} from '../services/auth.service'

import type {
  LoginRequest,
  User,
} from '../types/auth.types'

interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => Promise<void>
  updateUser: (user: User) => void
}

const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  const isAuthenticated = user !== null

  useEffect(() => {
    async function restoreSession() {
      try {
        const currentUser = await getCurrentUser()

        setUser(currentUser)
      } catch {
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    restoreSession()
  }, [])

  async function login(
    credentials: LoginRequest,
  ): Promise<void> {
    await loginService(credentials)

    const currentUser = await getCurrentUser()

    setUser(currentUser)
  }

  async function logout(): Promise<void> {
    try {
      await logoutService()
    } finally {
      setUser(null)
    }
  }

  function updateUser(updatedUser: User): void {
    setUser(updatedUser)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        login,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error(
      'useAuthContext debe utilizarse dentro de AuthProvider.',
    )
  }

  return context
}