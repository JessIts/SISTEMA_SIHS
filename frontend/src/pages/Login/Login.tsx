import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import Input from '../../components/ui/Input/Input'
import Button from '../../components/ui/Button/Button'

import { useAuth } from '../../hooks/useAuth'

import './Login.css'

function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      await login({
        email,
        password,
      })

      navigate('/')

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          'No fue posible iniciar sesión.',
        )
      }

    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="login-page">

      <div className="login-page__header">
        <h2>Iniciar sesión</h2>

        <p>
          Ingresa tus credenciales para continuar.
        </p>
      </div>

      <form
        className="login-page__form"
        onSubmit={handleSubmit}
      >

        <Input
          id="email"
          name="email"
          type="email"
          label="Correo electrónico"
          placeholder="correo@ejemplo.com"
          value={email}
          onChange={(event) =>
            setEmail(event.target.value)
          }
          required
        />

        <Input
          id="password"
          name="password"
          type="password"
          label="Contraseña"
          placeholder="••••••••"
          value={password}
          onChange={(event) =>
            setPassword(event.target.value)
          }
          required
        />

        {error && (
          <p className="login-page__error">
            {error}
          </p>
        )}

        <Button
          type="submit"
          loading={loading}
        >
          Iniciar sesión
        </Button>
        <button
          type="button"
          onClick={() => navigate('/register')}
          className="login-page__register"
        >
          Crear una cuenta
        </button>
      </form>

    </section>
  )
}

export default Login