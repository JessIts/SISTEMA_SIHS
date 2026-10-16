import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { franjasService } from '../../services/academic.service'
import type { FranjaHoraria } from '../../types/academic.types'
import { formatTime } from '../../utils/format'
import { integer, text } from '../../utils/form'
import { opcionesJornadas } from '../../utils/options'

const columns: CrudColumn<FranjaHoraria>[] = [
  { header: 'Orden', render: (item) => item.orden },
  {
    header: 'Franja',
    render: (item) => <strong>{formatTime(item.hora_inicio)} – {formatTime(item.hora_fin)}</strong>,
  },
  { header: 'Jornada', render: (item) => item.jornada.nombre },
]

const fields: FieldConfig[] = [
  { name: 'jornada_uuid', label: 'Jornada', type: 'select', required: true, loadOptions: opcionesJornadas },
  {
    name: 'orden',
    label: 'Orden',
    type: 'number',
    required: true,
    min: 1,
    max: 999,
    help: 'Posición de la fila en el horario (1 = primera).',
  },
  { name: 'hora_inicio', label: 'Hora de inicio', type: 'time', required: true },
  { name: 'hora_fin', label: 'Hora de fin', type: 'time', required: true },
]

const filters: CrudFilter[] = [
  { name: 'jornada_uuid', label: 'Jornada', loadOptions: opcionesJornadas },
]

function toPayload(values: FormValues) {
  return {
    jornada_uuid: text(values, 'jornada_uuid'),
    hora_inicio: text(values, 'hora_inicio'),
    hora_fin: text(values, 'hora_fin'),
    orden: integer(values, 'orden'),
  }
}

function FranjasHorarias() {
  return (
    <CrudPage
      title="Franjas horarias"
      description="Filas del horario: cada franja tiene hora de inicio, fin y jornada."
      entityName="franja"
      female
      service={franjasService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ jornada_uuid: '', orden: '', hora_inicio: '', hora_fin: '' }}
      toFormValues={(item) => ({
        jornada_uuid: item.jornada.uuid,
        orden: String(item.orden),
        hora_inicio: formatTime(item.hora_inicio),
        hora_fin: formatTime(item.hora_fin),
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default FranjasHorarias
