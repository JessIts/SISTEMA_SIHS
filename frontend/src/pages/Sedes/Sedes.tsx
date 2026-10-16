import CrudPage, { type CrudColumn } from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig } from '../../components/crud/EntityForm/EntityForm'

import { sedesService } from '../../services/academic.service'
import type { Sede } from '../../types/academic.types'
import { text } from '../../utils/form'

const columns: CrudColumn<Sede>[] = [
  { header: 'Nombre', render: (sede) => <strong>{sede.nombre}</strong> },
  { header: 'Dirección', render: (sede) => sede.direccion },
  { header: 'Tipo', render: (sede) => sede.tipo },
]

const fields: FieldConfig[] = [
  { name: 'nombre', label: 'Nombre', required: true, minLength: 2, maxLength: 150, placeholder: 'Sede Fontibón' },
  { name: 'direccion', label: 'Dirección', required: true, minLength: 3, maxLength: 255, placeholder: 'Cl 19A # 96c-40' },
  {
    name: 'tipo',
    label: 'Tipo',
    type: 'select',
    required: true,
    options: [
      { value: 'PRINCIPAL', label: 'Principal' },
      { value: 'SECUNDARIA', label: 'Secundaria' },
    ],
  },
]

function Sedes() {
  return (
    <CrudPage
      title="Sedes"
      description="Sedes del centro de formación y su dirección."
      entityName="sede"
      female
      service={sedesService}
      columns={columns}
      fields={fields}
      emptyValues={{ nombre: '', direccion: '', tipo: 'SECUNDARIA' }}
      toFormValues={(sede) => ({ nombre: sede.nombre, direccion: sede.direccion, tipo: sede.tipo })}
      toCreate={(values) => ({
        nombre: text(values, 'nombre'),
        direccion: text(values, 'direccion'),
        tipo: text(values, 'tipo'),
      })}
      toUpdate={(values) => ({
        nombre: text(values, 'nombre'),
        direccion: text(values, 'direccion'),
        tipo: text(values, 'tipo'),
      })}
    />
  )
}

export default Sedes
