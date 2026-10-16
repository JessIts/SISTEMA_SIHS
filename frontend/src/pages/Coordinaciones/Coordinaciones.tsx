import CrudPage, { type CrudColumn } from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { coordinacionesService } from '../../services/academic.service'
import type { Coordinacion } from '../../types/academic.types'
import { list, text } from '../../utils/form'
import { opcionesSedes } from '../../utils/options'

const columns: CrudColumn<Coordinacion>[] = [
  { header: 'Coordinación', render: (item) => <strong>{item.nombre}</strong> },
  {
    header: 'Sedes',
    render: (item) =>
      item.sedes.length > 0
        ? item.sedes.map((sede) => sede.nombre).join(', ')
        : '—',
  },
]

const fields: FieldConfig[] = [
  { name: 'nombre', label: 'Nombre', required: true, minLength: 2, maxLength: 150, fullWidth: true },
  { name: 'sedes_uuids', label: 'Sedes donde opera', type: 'multiselect', loadOptions: opcionesSedes },
]

function toPayload(values: FormValues) {
  return {
    nombre: text(values, 'nombre'),
    sedes_uuids: list(values, 'sedes_uuids'),
  }
}

function Coordinaciones() {
  return (
    <CrudPage
      title="Coordinaciones"
      description="Coordinaciones académicas y las sedes en las que operan."
      entityName="coordinación"
      female
      service={coordinacionesService}
      columns={columns}
      fields={fields}
      emptyValues={{ nombre: '', sedes_uuids: [] }}
      toFormValues={(item) => ({
        nombre: item.nombre,
        sedes_uuids: item.sedes.map((sede) => sede.uuid),
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default Coordinaciones
