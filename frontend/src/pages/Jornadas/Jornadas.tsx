import CrudPage, { type CrudColumn } from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { jornadasService } from '../../services/academic.service'
import type { Jornada } from '../../types/academic.types'
import { text } from '../../utils/form'

const columns: CrudColumn<Jornada>[] = [
  { header: 'Jornada', render: (item) => <strong>{item.nombre}</strong> },
]

const fields: FieldConfig[] = [
  { name: 'nombre', label: 'Nombre', required: true, minLength: 2, maxLength: 30, placeholder: 'TARDE', fullWidth: true },
]

function toPayload(values: FormValues) {
  return { nombre: text(values, 'nombre') }
}

function Jornadas() {
  return (
    <CrudPage
      title="Jornadas"
      description="Bloques del día (mañana, tarde, noche) que agrupan las franjas del horario."
      entityName="jornada"
      female
      service={jornadasService}
      columns={columns}
      fields={fields}
      emptyValues={{ nombre: '' }}
      toFormValues={(item) => ({ nombre: item.nombre })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default Jornadas
