import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { actividadesService } from '../../services/academic.service'
import type { ActividadAprendizaje } from '../../types/academic.types'
import { integer, text } from '../../utils/form'
import { opcionesResultados } from '../../utils/options'

const columns: CrudColumn<ActividadAprendizaje>[] = [
  { header: 'Código', render: (item) => <strong>{item.codigo}</strong> },
  { header: 'Actividad', render: (item) => <span className="crud-page__clamp">{item.descripcion}</span> },
  { header: 'Tipo', render: (item) => item.tipo },
  { header: 'Duración', render: (item) => `${item.duracion_minutos} min` },
  { header: 'Resultado', render: (item) => item.resultado.codigo },
]

const fields: FieldConfig[] = [
  { name: 'resultado_uuid', label: 'Resultado de aprendizaje', type: 'select', required: true, loadOptions: opcionesResultados, fullWidth: true },
  { name: 'codigo', label: 'Código', required: true, maxLength: 50, placeholder: 'ACT-01' },
  { name: 'tipo', label: 'Tipo', required: true, maxLength: 50, placeholder: 'TALLER' },
  { name: 'duracion_minutos', label: 'Duración (minutos)', type: 'number', required: true, min: 1 },
  { name: 'descripcion', label: 'Descripción', type: 'textarea', required: true, minLength: 3 },
]

const filters: CrudFilter[] = [
  { name: 'resultado_uuid', label: 'Resultado', loadOptions: opcionesResultados },
]

function toPayload(values: FormValues) {
  return {
    resultado_uuid: text(values, 'resultado_uuid'),
    codigo: text(values, 'codigo'),
    descripcion: text(values, 'descripcion'),
    tipo: text(values, 'tipo'),
    duracion_minutos: integer(values, 'duracion_minutos'),
  }
}

function ActividadesAprendizaje() {
  return (
    <CrudPage
      title="Actividades de aprendizaje"
      description="Actividades con las que se desarrolla cada resultado."
      entityName="actividad"
      female
      service={actividadesService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ resultado_uuid: '', codigo: '', tipo: '', duracion_minutos: '', descripcion: '' }}
      toFormValues={(item) => ({
        resultado_uuid: item.resultado.uuid,
        codigo: item.codigo,
        tipo: item.tipo,
        duracion_minutos: String(item.duracion_minutos),
        descripcion: item.descripcion,
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default ActividadesAprendizaje
