import {
  useEffect,
  useState,
} from 'react'

import {
  useNavigate,
  useParams,
} from 'react-router-dom'

import {
  getUsers,
  updateUser,
} from '../../services/users.service'

import './EditUser.css'

function EditUser() {
  const navigate = useNavigate()

  const { userUuid } = useParams<{
    userUuid: string
  }>()

  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    document_number: '',
  })

  const [loading, setLoading] =
    useState(true)

  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState('')

  useEffect(() => {
    async function loadUser() {
      if (!userUuid) {
        setError(
          'Identificador de usuario inválido.',
        )
        setLoading(false)
        return
      }

      try {
        setError('')

        /*
         * Temporalmente utilizamos el listado
         * para localizar el usuario.
         *
         * Más adelante podemos crear un
         * getUserByUuid() específico.
         */
        const response = await getUsers(
          1,
          100,
        )

        const user = response.items.find(
          (item) =>
            item.uuid === userUuid,
        )

        if (!user) {
          throw new Error(
            'Usuario no encontrado.',
          )
        }

        setForm({
          name: user.name,
          email: user.email,
          phone: user.phone,
          document_number:
            user.document_number,
        })

      } catch (error) {
        if (error instanceof Error) {
          setError(error.message)
        } else {
          setError(
            'No fue posible obtener el usuario.',
          )
        }
      } finally {
        setLoading(false)
      }
    }

    loadUser()
  }, [userUuid])

  function handleChange(
    event: React.ChangeEvent<HTMLInputElement>,
  ) {
    const {
      name,
      value,
    } = event.target

    setForm({
      ...form,
      [name]: value,
    })
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    if (!userUuid) {
      return
    }

    try {
      setSaving(true)
      setError('')

      await updateUser(
        userUuid,
        form,
      )

      navigate('/users')

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          'No fue posible actualizar el usuario.',
        )
      }
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <section className="edit-user">
        <p>Cargando usuario...</p>
      </section>
    )
  }

  if (error && !form.name) {
    return (
      <section className="edit-user">
        <p className="edit-user__error">
          {error}
        </p>

        <button
          type="button"
          onClick={() => navigate('/users')}
          className="edit-user__cancel"
        >
          Volver
        </button>
      </section>
    )
  }

  return (
    <section className="edit-user">

      <div className="edit-user__header">

        <div>
          <h1>Editar usuario</h1>

          <p>
            Actualiza la información del usuario.
          </p>
        </div>

      </div>

      <form
        className="edit-user__form"
        onSubmit={handleSubmit}
      >

        <div className="edit-user__group">

          <label htmlFor="name">
            Nombre completo
          </label>

          <input
            id="name"
            name="name"
            value={form.name}
            onChange={handleChange}
            required
          />

        </div>

        <div className="edit-user__group">

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

        <div className="edit-user__group">

          <label htmlFor="phone">
            Teléfono
          </label>

          <input
            id="phone"
            name="phone"
            value={form.phone}
            onChange={handleChange}
            required
          />

        </div>

        <div className="edit-user__group">

          <label htmlFor="document_number">
            Documento
          </label>

          <input
            id="document_number"
            name="document_number"
            value={form.document_number}
            onChange={handleChange}
            required
          />

        </div>

        {error && (
          <p className="edit-user__error">
            {error}
          </p>
        )}

        <div className="edit-user__actions">

          <button
            type="button"
            onClick={() => navigate('/users')}
            className="edit-user__cancel"
          >
            Cancelar
          </button>

          <button
            type="submit"
            disabled={saving}
            className="edit-user__submit"
          >
            {saving
              ? 'Guardando...'
              : 'Guardar cambios'}
          </button>

        </div>

      </form>

    </section>
  )
}

export default EditUser
