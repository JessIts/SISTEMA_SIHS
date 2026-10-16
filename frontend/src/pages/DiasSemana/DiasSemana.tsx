import CrudPage, { type CrudColumn } from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { diasService } from '../../services/academic.service'
import type { DiaSemana } from '../../types/academic.types'
import { integer, text } from '../../utils/form'

const columns: CrudColumn<DiaSemana>[] = [
  { header: 'Número', render: (item) => item.numero },
  { header: 'Día', render: (item) => <strong>{item.nombre}</strong> },
]

const fields: FieldConfig[] = [
  {
    name: 'numero',
    label: 'Número',
    type: 'number',
    required: true,
    min: 1,
    max: 7,
    help: '1 = lunes ... 7 = domingo',
  },
  { name: 'nombre', label: 'Nombre', required: true, minLength: 3, maxLength: 15, placeholder: 'LUNES' },
]

function toPayload(values: FormValues) {
  return {
    numero: integer(values, 'numero'),
    nombre: text(values, 'nombre'),
  }
}

function DiasSemana() {
  return (
    <CrudPage
      title="Días de la semana"
      description="Columnas del horario. Solo los días activos aparecen en los horarios."
      entityName="día"
      service={diasService}
      columns={columns}
      fields={fields}
      emptyValues={{ numero: '', nombre: '' }}
      toFormValues={(item) => ({ numero: String(item.numero), nombre: item.nombre })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default DiasSemana
