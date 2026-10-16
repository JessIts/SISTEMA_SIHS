import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { ambientesService } from '../../services/academic.service'
import type { Ambiente } from '../../types/academic.types'
import { optionalInteger, text } from '../../utils/form'
import { opcionesSedes } from '../../utils/options'

const columns: CrudColumn<Ambiente>[] = [
  { header: 'Ambiente', render: (item) => <strong>{item.nombre}</strong> },
  { header: 'Sede', render: (item) => item.sede.nombre },
  { header: 'Capacidad', render: (item) => item.capacidad ?? '—' },
]

const fields: FieldConfig[] = [
  { name: 'sede_uuid', label: 'Sede', type: 'select', required: true, loadOptions: opcionesSedes },
  { name: 'nombre', label: 'Nombre', required: true, maxLength: 100, placeholder: '202 A' },
  { name: 'capacidad', label: 'Capacidad', type: 'number', min: 1, placeholder: '30' },
]

const filters: CrudFilter[] = [
  { name: 'sede_uuid', label: 'Sede', loadOptions: opcionesSedes },
]

function toPayload(values: FormValues) {
  return {
    sede_uuid: text(values, 'sede_uuid'),
    nombre: text(values, 'nombre'),
    capacidad: optionalInteger(values, 'capacidad'),
  }
}

function Ambientes() {
  return (
    <CrudPage
      title="Ambientes"
      description="Salones y espacios de formación de cada sede."
      entityName="ambiente"
      service={ambientesService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ sede_uuid: '', nombre: '', capacidad: '' }}
      toFormValues={(item) => ({
        sede_uuid: item.sede.uuid,
        nombre: item.nombre,
        capacidad: item.capacidad?.toString() ?? '',
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default Ambientes
