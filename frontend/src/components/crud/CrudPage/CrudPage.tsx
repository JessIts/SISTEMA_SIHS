import {
  useCallback,
  useEffect,
  useState,
  type ReactNode,
} from 'react'

import EntityForm, {
  type FieldConfig,
  type FormValues,
  type SelectOption,
} from '../EntityForm/EntityForm'
import Modal from '../../ui/Modal/Modal'
import PageHeader from '../../common/PageHeader/PageHeader'

import { usePermissions } from '../../../hooks/usePermissions'
import type { CrudService } from '../../../services/crud.service'
import { errorMessage } from '../../../utils/format'

import './CrudPage.css'

export interface CrudColumn<T> {
  header: string
  render: (item: T) => ReactNode
}

export interface CrudFilter {
  name: string
  label: string
  loadOptions: () => Promise<SelectOption[]>
}

interface CrudPageProps<T, TCreate, TUpdate> {
  title: string
  description: string
  /** "sede", "programa"... (para botones y mensajes) */
  entityName: string
  female?: boolean
  service: CrudService<T, TCreate, TUpdate>
  columns: CrudColumn<T>[]
  fields: FieldConfig[]
  emptyValues: FormValues
  toFormValues: (item: T) => FormValues
  toCreate: (values: FormValues) => TCreate
  toUpdate: (values: FormValues) => TUpdate
  filters?: CrudFilter[]
  /** Acciones extra por fila (ej. "Aprendices", "Ver horario") */
  rowActions?: (item: T, reload: () => void) => ReactNode
  /** Botones extra en el encabezado */
  headerActions?: ReactNode
}

// Referencia estable: un [] nuevo en cada render dispararía el efecto sin fin
const NO_FILTERS: CrudFilter[] = []

type ModalState<T> =
  | { mode: 'create' }
  | { mode: 'edit'; item: T }
  | null

/**
 * Página CRUD genérica: listado paginado con filtros, inactivos,
 * crear / editar en modal, desactivar y reactivar.
 * Solo admin y coordinador ven los botones de modificación.
 */
function CrudPage<
  T extends { uuid: string; is_active: boolean },
  TCreate,
  TUpdate,
>({
  title,
  description,
  entityName,
  female = false,
  service,
  columns,
  fields,
  emptyValues,
  toFormValues,
  toCreate,
  toUpdate,
  filters = NO_FILTERS,
  rowActions,
  headerActions,
}: CrudPageProps<T, TCreate, TUpdate>) {
  const { canManage } = usePermissions()

  const [items, setItems] = useState<T[]>([])
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [total, setTotal] = useState(0)

  const [showInactive, setShowInactive] = useState(false)

  const [filterValues, setFilterValues] = useState<Record<string, string>>({})
  const [filterOptions, setFilterOptions] = useState<Record<string, SelectOption[]>>({})

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const [modal, setModal] = useState<ModalState<T>>(null)

  const [reloadKey, setReloadKey] = useState(0)

  const reload = useCallback(() => {
    setReloadKey((key) => key + 1)
  }, [])

  const article = female ? 'la' : 'el'
  const nueva = female ? 'Nueva' : 'Nuevo'

  // Opciones de los filtros
  useEffect(() => {
    let active = true

    async function loadFilters() {
      try {
        const entries = await Promise.all(
          filters.map(async (filter) => [
            filter.name,
            await filter.loadOptions(),
          ] as const),
        )

        if (active) {
          setFilterOptions(Object.fromEntries(entries))
        }
      } catch {
        // Los filtros son opcionales: si fallan, la lista sigue funcionando.
      }
    }

    loadFilters()

    return () => {
      active = false
    }
  }, [filters])

  // Listado
  useEffect(() => {
    let active = true

    async function loadItems() {
      try {
        setLoading(true)
        setError('')

        if (showInactive) {
          const inactive = await service.listInactive()

          if (active) {
            setItems(inactive)
            setPages(1)
            setTotal(inactive.length)
          }

          return
        }

        const response = await service.list({
          page,
          limit: 10,
          ...filterValues,
        })

        if (active) {
          setItems(response.items)
          setPages(Math.max(response.pages, 1))
          setTotal(response.total)
        }
      } catch (loadError) {
        if (active) {
          setError(errorMessage(loadError, `No fue posible obtener los registros.`))
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadItems()

    return () => {
      active = false
    }
  }, [service, page, showInactive, filterValues, reloadKey])

  function handleFilterChange(name: string, value: string) {
    setPage(1)
    setFilterValues((current) => {
      const next = { ...current }

      if (value) {
        next[name] = value
      } else {
        delete next[name]
      }

      return next
    })
  }

  async function handleSubmit(values: FormValues) {
    if (!modal) {
      return
    }

    if (modal.mode === 'create') {
      await service.create(toCreate(values))
      setNotice(`${capitalize(entityName)} cread${female ? 'a' : 'o'} correctamente.`)
    } else {
      await service.update(modal.item.uuid, toUpdate(values))
      setNotice(`${capitalize(entityName)} actualizad${female ? 'a' : 'o'} correctamente.`)
    }

    setModal(null)
    reload()
  }

  async function handleDeactivate(item: T) {
    const confirmed = window.confirm(
      `¿Deseas desactivar ${article} ${entityName}?`,
    )

    if (!confirmed) {
      return
    }

    try {
      setError('')
      setNotice('')

      await service.remove(item.uuid)

      setNotice(`${capitalize(entityName)} desactivad${female ? 'a' : 'o'}.`)
      reload()
    } catch (actionError) {
      setError(errorMessage(actionError, `No fue posible desactivar ${article} ${entityName}.`))
    }
  }

  async function handleActivate(item: T) {
    try {
      setError('')
      setNotice('')

      await service.activate(item.uuid)

      setNotice(`${capitalize(entityName)} activad${female ? 'a' : 'o'}.`)
      reload()
    } catch (actionError) {
      setError(errorMessage(actionError, `No fue posible activar ${article} ${entityName}.`))
    }
  }

  return (
    <section className="crud-page">
      <PageHeader
        title={title}
        description={description}
        actions={
          <>
            {headerActions}

            {canManage && !showInactive && (
              <button
                type="button"
                className="btn btn--primary"
                onClick={() => {
                  setNotice('')
                  setModal({ mode: 'create' })
                }}
              >
                {nueva} {entityName}
              </button>
            )}
          </>
        }
      />

      <div className="crud-page__card">
        <div className="crud-page__toolbar">
          <div className="crud-page__filters">
            {!showInactive && filters.map((filter) => (
              <label key={filter.name} className="crud-page__filter">
                <span>{filter.label}</span>

                <select
                  value={filterValues[filter.name] ?? ''}
                  onChange={(event) =>
                    handleFilterChange(filter.name, event.target.value)
                  }
                >
                  <option value="">Todos</option>

                  {(filterOptions[filter.name] ?? []).map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
            ))}
          </div>

          <div className="crud-page__view-toggle" role="tablist">
            <button
              type="button"
              role="tab"
              aria-selected={!showInactive}
              className={!showInactive ? 'is-active' : ''}
              onClick={() => {
                setShowInactive(false)
                setPage(1)
              }}
            >
              Activos
            </button>

            <button
              type="button"
              role="tab"
              aria-selected={showInactive}
              className={showInactive ? 'is-active' : ''}
              onClick={() => setShowInactive(true)}
            >
              Inactivos
            </button>
          </div>
        </div>

        {notice && <p className="crud-page__notice">{notice}</p>}

        {error && <p className="crud-page__error">{error}</p>}

        {loading && <p className="crud-page__muted">Cargando...</p>}

        {!loading && !error && items.length === 0 && (
          <p className="crud-page__muted">
            {showInactive
              ? 'No hay registros inactivos.'
              : 'No hay registros. Usa el botón de arriba para crear el primero.'}
          </p>
        )}

        {!loading && items.length > 0 && (
          <>
            <div className="crud-page__table-wrapper">
              <table className="crud-page__table">
                <thead>
                  <tr>
                    {columns.map((column) => (
                      <th key={column.header}>{column.header}</th>
                    ))}

                    <th>Estado</th>

                    {(canManage || rowActions) && <th>Acciones</th>}
                  </tr>
                </thead>

                <tbody>
                  {items.map((item) => (
                    <tr key={item.uuid}>
                      {columns.map((column) => (
                        <td key={column.header}>{column.render(item)}</td>
                      ))}

                      <td>
                        <span
                          className={`crud-page__status ${
                            item.is_active
                              ? 'crud-page__status--active'
                              : 'crud-page__status--inactive'
                          }`}
                        >
                          {item.is_active ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>

                      {(canManage || rowActions) && (
                        <td>
                          <div className="crud-page__actions">
                            {item.is_active && rowActions?.(item, reload)}

                            {canManage && item.is_active && (
                              <>
                                <button
                                  type="button"
                                  className="btn btn--secondary btn--small"
                                  onClick={() => {
                                    setNotice('')
                                    setModal({ mode: 'edit', item })
                                  }}
                                >
                                  Editar
                                </button>

                                <button
                                  type="button"
                                  className="btn btn--danger btn--small"
                                  onClick={() => handleDeactivate(item)}
                                >
                                  Desactivar
                                </button>
                              </>
                            )}

                            {canManage && !item.is_active && (
                              <button
                                type="button"
                                className="btn btn--secondary btn--small crud-page__activate"
                                onClick={() => handleActivate(item)}
                              >
                                Activar
                              </button>
                            )}
                          </div>
                        </td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {!showInactive && (
              <div className="crud-page__pagination">
                <button
                  type="button"
                  className="btn btn--secondary btn--small"
                  onClick={() => setPage((current) => current - 1)}
                  disabled={page <= 1}
                >
                  Anterior
                </button>

                <span>
                  Página {page} de {pages} · {total} registro{total === 1 ? '' : 's'}
                </span>

                <button
                  type="button"
                  className="btn btn--secondary btn--small"
                  onClick={() => setPage((current) => current + 1)}
                  disabled={page >= pages}
                >
                  Siguiente
                </button>
              </div>
            )}
          </>
        )}
      </div>

      <Modal
        open={modal !== null}
        title={
          modal?.mode === 'edit'
            ? `Editar ${entityName}`
            : `${nueva} ${entityName}`
        }
        onClose={() => setModal(null)}
      >
        {modal && (
          <EntityForm
            key={modal.mode === 'edit' ? modal.item.uuid : 'create'}
            fields={fields}
            mode={modal.mode}
            initialValues={
              modal.mode === 'edit' ? toFormValues(modal.item) : emptyValues
            }
            onSubmit={handleSubmit}
            onCancel={() => setModal(null)}
          />
        )}
      </Modal>
    </section>
  )
}

function capitalize(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1)
}

export default CrudPage
