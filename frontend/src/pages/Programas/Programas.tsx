import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { programasService } from '../../services/academic.service'
import type { Programa } from '../../types/academic.types'
import { optionalText, text } from '../../utils/form'
import { opcionesCoordinaciones } from '../../utils/options'

const columns: CrudColumn<Programa>[] = [
  { header: 'Código', render: (item) => <strong>{item.codigo}</strong> },
  { header: 'Programa', render: (item) => item.nombre },
  { header: 'Nivel', render: (item) => item.nivel ?? '—' },
  { header: 'Coordinación', render: (item) => item.coordinacion.nombre },
]

const fields: FieldConfig[] = [
  { name: 'codigo', label: 'Código', required: true, maxLength: 30, placeholder: 'PRG-MERC' },
  {
    name: 'nivel',
    label: 'Nivel',
    type: 'select',
    options: [
      { value: 'AUXILIAR', label: 'Auxiliar' },
      { value: 'OPERARIO', label: 'Operario' },
      { value: 'TÉCNICO', label: 'Técnico' },
      { value: 'TECNÓLOGO', label: 'Tecnólogo' },
      { value: 'ESPECIALIZACIÓN', label: 'Especialización' },
    ],
  },
  { name: 'nombre', label: 'Nombre del programa', required: true, minLength: 2, maxLength: 150, fullWidth: true },
  { name: 'coordinacion_uuid', label: 'Coordinación', type: 'select', required: true, loadOptions: opcionesCoordinaciones, fullWidth: true },
]

const filters: CrudFilter[] = [
  { name: 'coordinacion_uuid', label: 'Coordinación', loadOptions: opcionesCoordinaciones },
]

function toPayload(values: FormValues) {
  return {
    codigo: text(values, 'codigo'),
    nombre: text(values, 'nombre'),
    nivel: optionalText(values, 'nivel'),
    coordinacion_uuid: text(values, 'coordinacion_uuid'),
  }
}

function Programas() {
  return (
    <CrudPage
      title="Programas"
      description="Programas de formación de cada coordinación."
      entityName="programa"
      service={programasService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ codigo: '', nombre: '', nivel: '', coordinacion_uuid: '' }}
      toFormValues={(item) => ({
        codigo: item.codigo,
        nombre: item.nombre,
        nivel: item.nivel ?? '',
        coordinacion_uuid: item.coordinacion.uuid,
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default Programas
