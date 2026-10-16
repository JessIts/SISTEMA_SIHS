import CrudPage, { type CrudColumn } from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { trimestresService } from '../../services/academic.service'
import type { EstadoTrimestre, Trimestre } from '../../types/academic.types'
import { formatPeriodo, formatTrimestre } from '../../utils/format'
import { integer, text } from '../../utils/form'
import { ESTADO_TRIMESTRE_LABELS, toOptions } from '../../utils/labels'

const columns: CrudColumn<Trimestre>[] = [
  { header: 'Trimestre', render: (item) => <strong>{formatTrimestre(item)}</strong> },
  { header: 'Periodo', render: (item) => formatPeriodo(item) },
  { header: 'Etapa', render: (item) => ESTADO_TRIMESTRE_LABELS[item.estado] },
]

const fields: FieldConfig[] = [
  { name: 'anio', label: 'Año', type: 'number', required: true, min: 2000, max: 2100 },
  {
    name: 'numero',
    label: 'Número',
    type: 'select',
    required: true,
    options: [1, 2, 3, 4].map((numero) => ({ value: String(numero), label: `Trimestre ${numero}` })),
  },
  { name: 'fecha_inicio', label: 'Fecha de inicio', type: 'date', required: true },
  { name: 'fecha_fin', label: 'Fecha de fin', type: 'date', required: true },
  {
    name: 'estado',
    label: 'Etapa',
    type: 'select',
    required: true,
    options: toOptions(ESTADO_TRIMESTRE_LABELS),
  },
]

function toPayload(values: FormValues) {
  return {
    anio: integer(values, 'anio'),
    numero: integer(values, 'numero'),
    fecha_inicio: text(values, 'fecha_inicio'),
    fecha_fin: text(values, 'fecha_fin'),
    estado: text(values, 'estado') as EstadoTrimestre,
  }
}

function Trimestres() {
  return (
    <CrudPage
      title="Trimestres"
      description="Periodos del calendario académico. Todas las fichas comparten el mismo calendario."
      entityName="trimestre"
      service={trimestresService}
      columns={columns}
      fields={fields}
      emptyValues={{
        anio: String(new Date().getFullYear()),
        numero: '',
        fecha_inicio: '',
        fecha_fin: '',
        estado: 'planeacion',
      }}
      toFormValues={(item) => ({
        anio: String(item.anio),
        numero: String(item.numero),
        fecha_inicio: item.fecha_inicio,
        fecha_fin: item.fecha_fin,
        estado: item.estado,
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default Trimestres
