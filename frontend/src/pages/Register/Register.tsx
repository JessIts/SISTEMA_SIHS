import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { register } from '../../services/auth.service'

import './Register.css'

function Register() {
  const navigate = useNavigate()

  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    document_number: '',
    password: '',
  })

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const { name, value } = event.target

    setForm({
      ...form,
      [name]: value,
    })
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    try {
      setLoading(true)
      setError('')
      setSuccess('')

      await register(form)

      setSuccess(
        'Cuenta creada correctamente. Ahora puedes iniciar sesión.',
      )

      setTimeout(() => {
        navigate('/login')
      }, 1500)
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError('No fue posible crear la cuenta.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="register-page">
      <div className="register-page__card">
        <div className="register-page__header">
          <h1>Crear cuenta</h1>
          <p>
            Regístrate para acceder al sistema.
          </p>
        </div>

        <form
          className="register-page__form"
          onSubmit={handleSubmit}
        >
          <div className="register-page__group">
            <label htmlFor="name">
              Nombre completo
            </label>

            <input
              id="name"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Nombre completo"
              required
              minLength={2}
              maxLength={100}
            />
          </div>

          <div className="register-page__group">
            <label htmlFor="email">
              Correo electrónico
            </label>

            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              placeholder="correo@ejemplo.com"
              required
            />
          </div>

          <div className="register-page__group">
            <label htmlFor="phone">
              Teléfono
            </label>

            <input
              id="phone"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              placeholder="3001234567"
              required
              minLength={7}
              maxLength={20}
            />
          </div>

          <div className="register-page__group">
            <label htmlFor="document_number">
              Documento
            </label>

            <input
              id="document_number"
              name="document_number"
              value={form.document_number}
              onChange={handleChange}
              placeholder="Número de documento"
              required
              minLength={5}
              maxLength={30}
            />
          </div>

          <div className="register-page__group">
            <label htmlFor="password">
              Contraseña
            </label>

            <input
              id="password"
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Mínimo 8 caracteres"
              required
              minLength={8}
              maxLength={128}
            />
          </div>

          {error && (
            <p className="register-page__error">
              {error}
            </p>
          )}

          {success && (
            <p className="register-page__success">
              {success}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="register-page__submit"
          >
            {loading ? 'Creando cuenta...' : 'Crear cuenta'}
          </button>

          <button
            type="button"
            onClick={() => navigate('/login')}
            className="register-page__login"
          >
            Ya tengo una cuenta
          </button>
        </form>
      </div>
    </section>
  )
}

export default Register