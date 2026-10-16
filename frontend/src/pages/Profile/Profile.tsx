import { useEffect, useState } from 'react'
import { useAuth } from '../../hooks/useAuth'

import {
  getCurrentUser,
  updateMyProfile,
} from '../../services/auth.service'

import type { User } from '../../types/auth.types'

import './Profile.css'

function Profile() {

  const { updateUser } = useAuth()
  const [user, setUser] = useState<User | null>(null)

  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    document_number: '',
    password: '',
  })

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    async function loadProfile() {
      try {
        setLoading(true)
        setError('')

        const currentUser = await getCurrentUser()

        setUser(currentUser)

        setForm({
          name: currentUser.name,
          email: currentUser.email,
          phone: currentUser.phone,
          document_number: currentUser.document_number,
          password: '',
        })
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message)
        } else {
          setError('No fue posible obtener el perfil.')
        }
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [])

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const { name, value } = event.target

    setForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }))
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    try {
      setSaving(true)
      setError('')
      setSuccess('')

      const updateData = {
        name: form.name,
        email: form.email,
        phone: form.phone,
        document_number: form.document_number,
        ...(form.password
          ? { password: form.password }
          : {}),
      }

      const updatedUser = await updateMyProfile(
        updateData,
      )

      setUser(updatedUser)
      updateUser(updatedUser)

      setForm({
        name: updatedUser.name,
        email: updatedUser.email,
        phone: updatedUser.phone,
        document_number:
          updatedUser.document_number,
        password: '',
      })

      setSuccess(
        'Perfil actualizado correctamente.',
      )
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError('No fue posible actualizar el perfil.')
      }
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <section className="profile-page">
        <div className="profile-page__card">
          <p>Cargando perfil...</p>
        </div>
      </section>
    )
  }

  if (error && !user) {
    return (
      <section className="profile-page">
        <div className="profile-page__card">
          <p className="profile-page__error">
            {error}
          </p>
        </div>
      </section>
    )
  }

  if (!user) {
    return (
      <section className="profile-page">
        <div className="profile-page__card">
          <p>No fue posible cargar el perfil.</p>
        </div>
      </section>
    )
  }

  return (
    <section className="profile-page">
      <div className="profile-page__header">
        <div>
          <h1>Mi perfil</h1>
          <p>
            Consulta y actualiza tu información personal.
          </p>
        </div>
      </div>

      <div className="profile-page__card">
        <form
          className="profile-page__form"
          onSubmit={handleSubmit}
        >
          <div className="profile-page__group">
            <label htmlFor="name">
              Nombre completo
            </label>

            <input
              id="name"
              name="name"
              value={form.name}
              onChange={handleChange}
              minLength={2}
              maxLength={100}
              required
            />
          </div>

          <div className="profile-page__group">
            <label htmlFor="email">
              Correo electrónico
            </label>

            <input
              id="email"
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="profile-page__group">
            <label htmlFor="phone">
              Teléfono
            </label>

            <input
              id="phone"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              minLength={7}
              maxLength={20}
              required
            />
          </div>

          <div className="profile-page__group">
            <label htmlFor="document_number">
              Documento
            </label>

            <input
              id="document_number"
              name="document_number"
              value={form.document_number}
              onChange={handleChange}
              minLength={5}
              maxLength={30}
              required
            />
          </div>

          <div className="profile-page__group">
            <label htmlFor="password">
              Nueva contraseña
            </label>

            <input
              id="password"
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              minLength={8}
              maxLength={128}
              placeholder="Déjalo vacío para conservar la actual"
            />
          </div>

          {error && (
            <p className="profile-page__error">
              {error}
            </p>
          )}

          {success && (
            <p className="profile-page__success">
              {success}
            </p>
          )}

          <button
            type="submit"
            disabled={saving}
            className="profile-page__submit"
          >
            {saving
              ? 'Guardando...'
              : 'Guardar cambios'}
          </button>
        </form>

        <div className="profile-page__account">
          <div className="profile-page__field">
            <span className="profile-page__label">
              Rol
            </span>

            <span className="profile-page__value">
              {user.role}
            </span>
          </div>

          <div className="profile-page__field">
            <span className="profile-page__label">
              Estado
            </span>

            <span className="profile-page__value">
              {user.is_active
                ? 'Activo'
                : 'Inactivo'}
            </span>
          </div>

          <div className="profile-page__field">
            <span className="profile-page__label">
              Fecha de registro
            </span>

            <span className="profile-page__value">
              {new Date(
                user.created_at,
              ).toLocaleString()}
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Profile