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
} from '../services/auth.service'

import type {
  LoginRequest,
  User,
} from '../types/auth.types'

interface AuthContextValue {
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean
  loading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<
  AuthContextValue | undefined
>(undefined)

const ACCESS_TOKEN_KEY = 'sihs_access_token'

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)

  const [accessToken, setAccessToken] =
    useState<string | null>(null)

  const [loading, setLoading] = useState(true)

  const isAuthenticated =
    accessToken !== null && user !== null

  useEffect(() => {
    async function restoreSession() {
      const storedToken =
        localStorage.getItem(ACCESS_TOKEN_KEY)

      if (!storedToken) {
        setLoading(false)
        return
      }

      try {
        const currentUser =
          await getCurrentUser(storedToken)

        setAccessToken(storedToken)
        setUser(currentUser)

      } catch {
        localStorage.removeItem(ACCESS_TOKEN_KEY)
        setAccessToken(null)
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
    const tokenResponse =
      await loginService(credentials)

    const currentUser =
      await getCurrentUser(
        tokenResponse.access_token,
      )

    localStorage.setItem(
      ACCESS_TOKEN_KEY,
      tokenResponse.access_token,
    )

    setAccessToken(
      tokenResponse.access_token,
    )

    setUser(currentUser)
  }

  function logout() {
    localStorage.removeItem(
      ACCESS_TOKEN_KEY,
    )

    setAccessToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        isAuthenticated,
        loading,
        login,
        logout,
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