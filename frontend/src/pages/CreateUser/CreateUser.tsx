import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { createUser } from '../../services/users.service'

import './CreateUser.css'

function CreateUser() {
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

      await createUser(form)

      navigate('/users')

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          'No fue posible crear el usuario.',
        )
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="create-user">

      <div className="create-user__header">

        <div>
          <h1>Nuevo usuario</h1>

          <p>
            Registra un nuevo usuario en el sistema.
          </p>
        </div>

      </div>

      <form
        className="create-user__form"
        onSubmit={handleSubmit}
      >

        <div className="create-user__group">

          <label htmlFor="name">
            Nombre completo
          </label>

          <input
            id="name"
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Nombre del usuario"
            required
          />

        </div>

        <div className="create-user__group">

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

        <div className="create-user__group">

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
          />

        </div>

        <div className="create-user__group">

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
          />

        </div>

        <div className="create-user__group">

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
            minLength={8}
            required
          />

        </div>

        {error && (
          <p className="create-user__error">
            {error}
          </p>
        )}

        <div className="create-user__actions">

          <button
            type="button"
            onClick={() => navigate('/users')}
            className="create-user__cancel"
          >
            Cancelar
          </button>

          <button
            type="submit"
            disabled={loading}
            className="create-user__submit"
          >
            {loading
              ? 'Creando...'
              : 'Crear usuario'}
          </button>

        </div>

      </form>

    </section>
  )
}

export default CreateUser