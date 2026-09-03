import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import {
  activateUser,
  deactivateUser,
  getUsers,
} from '../../services/users.service'

import type { User } from '../../types/auth.types'

import './Users.css'

function Users() {
  const navigate = useNavigate()

  const [users, setUsers] = useState<User[]>([])

  const [page, setPage] = useState(1)

  const [pages, setPages] = useState(1)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  useEffect(() => {
    async function loadUsers() {
      try {
        setLoading(true)
        setError('')

        const response = await getUsers(
          page,
          10,
        )

        setUsers(response.items)
        setPages(response.pages)

      } catch (error) {
        if (error instanceof Error) {
          setError(error.message)
        } else {
          setError(
            'No fue posible obtener los usuarios.',
          )
        }
      } finally {
        setLoading(false)
      }
    }

    loadUsers()
  }, [page])

  function handlePreviousPage() {
    if (page > 1) {
      setPage((currentPage) =>
        currentPage - 1,
      )
    }
  }

  function handleNextPage() {
    if (page < pages) {
      setPage((currentPage) =>
        currentPage + 1,
      )
    }
  }

  async function handleDeactivate(
    user: User,
  ) {
    const confirmed = window.confirm(
      `¿Deseas desactivar al usuario ${user.name}?`,
    )

    if (!confirmed) {
      return
    }

    try {
      setError('')

      await deactivateUser(user.uuid)

      setUsers((currentUsers) =>
        currentUsers.map((currentUser) =>
          currentUser.uuid === user.uuid
            ? {
                ...currentUser,
                is_active: false,
              }
            : currentUser,
        ),
      )

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          'No fue posible desactivar el usuario.',
        )
      }
    }
  }

  async function handleActivate(
    user: User,
  ) {
    try {
      setError('')

      const activatedUser =
        await activateUser(user.uuid)

      setUsers((currentUsers) =>
        currentUsers.map((currentUser) =>
          currentUser.uuid === user.uuid
            ? activatedUser
            : currentUser,
        ),
      )

    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError(
          'No fue posible activar el usuario.',
        )
      }
    }
  }

  return (
    <section className="users-page">

      <div className="users-page__header">

        <div>
          <h1>Usuarios</h1>

          <p>
            Gestión de usuarios del sistema.
          </p>
        </div>

        <button
          type="button"
          onClick={() =>
            navigate('/users/create')
          }
          className="users-page__create-button"
        >
          Nuevo usuario
        </button>

      </div>

      <div className="users-page__content">

        {loading && (
          <p>
            Cargando usuarios...
          </p>
        )}

        {!loading && error && (
          <p className="users-page__error">
            {error}
          </p>
        )}

        {!loading &&
          !error &&
          users.length === 0 && (
            <p>
              No hay usuarios registrados.
            </p>
          )}

        {!loading &&
          !error &&
          users.length > 0 && (
            <>
              <div className="users-page__table-wrapper">

                <table className="users-page__table">

                  <thead>
                    <tr>
                      <th>Nombre</th>
                      <th>Correo</th>
                      <th>Teléfono</th>
                      <th>Documento</th>
                      <th>Rol</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>

                  <tbody>
                    {users.map((user) => (
                      <tr key={user.uuid}>

                        <td>
                          {user.name}
                        </td>

                        <td>
                          {user.email}
                        </td>

                        <td>
                          {user.phone}
                        </td>

                        <td>
                          {user.document_number}
                        </td>

                        <td>
                          {user.role}
                        </td>

                        <td>
                          {user.is_active
                            ? 'Activo'
                            : 'Inactivo'}
                        </td>

                        <td>
                          <div className="users-page__actions">

                            <button
                              type="button"
                              className="users-page__action users-page__action--edit"
                              onClick={() =>
                                navigate(
                                  `/users/${user.uuid}/edit`,
                                )
                              }
                            >
                              Editar
                            </button>

                            {user.is_active ? (
                              <button
                                type="button"
                                className="users-page__action users-page__action--deactivate"
                                onClick={() =>
                                  handleDeactivate(
                                    user,
                                  )
                                }
                              >
                                Desactivar
                              </button>
                            ) : (
                              <button
                                type="button"
                                className="users-page__action users-page__action--activate"
                                onClick={() =>
                                  handleActivate(
                                    user,
                                  )
                                }
                              >
                                Activar
                              </button>
                            )}

                          </div>
                        </td>

                      </tr>
                    ))}
                  </tbody>

                </table>

              </div>

              <div className="users-page__pagination">

                <button
                  type="button"
                  onClick={
                    handlePreviousPage
                  }
                  disabled={
                    page === 1 || loading
                  }
                  className="users-page__pagination-button"
                >
                  Anterior
                </button>

                <span className="users-page__pagination-info">
                  Página {page} de {pages}
                </span>

                <button
                  type="button"
                  onClick={
                    handleNextPage
                  }
                  disabled={
                    page === pages ||
                    loading
                  }
                  className="users-page__pagination-button"
                >
                  Siguiente
                </button>

              </div>
            </>
          )}

      </div>

    </section>
  )
}

export default Users
