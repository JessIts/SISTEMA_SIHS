import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { competenciasService } from '../../services/academic.service'
import type { Competencia } from '../../types/academic.types'
import { text } from '../../utils/form'
import { opcionesProgramas } from '../../utils/options'

const columns: CrudColumn<Competencia>[] = [
  { header: 'Código', render: (item) => <strong>{item.codigo}</strong> },
  { header: 'Descripción', render: (item) => <span className="crud-page__clamp">{item.descripcion}</span> },
  {
    header: 'Programa',
    render: (item) => (
      <>
        {item.programa.codigo}
        <span className="crud-page__secondary">{item.programa.nombre}</span>
      </>
    ),
  },
]

const fields: FieldConfig[] = [
  { name: 'programa_uuid', label: 'Programa', type: 'select', required: true, loadOptions: opcionesProgramas, fullWidth: true },
  { name: 'codigo', label: 'Código', required: true, maxLength: 50, placeholder: 'COMP-01' },
  { name: 'descripcion', label: 'Descripción', type: 'textarea', required: true, minLength: 3 },
]

const filters: CrudFilter[] = [
  { name: 'programa_uuid', label: 'Programa', loadOptions: opcionesProgramas },
]

function toPayload(values: FormValues) {
  return {
    programa_uuid: text(values, 'programa_uuid'),
    codigo: text(values, 'codigo'),
    descripcion: text(values, 'descripcion'),
  }
}

function Competencias() {
  return (
    <CrudPage
      title="Competencias"
      description="Competencias que componen cada programa de formación."
      entityName="competencia"
      female
      service={competenciasService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ programa_uuid: '', codigo: '', descripcion: '' }}
      toFormValues={(item) => ({
        programa_uuid: item.programa.uuid,
        codigo: item.codigo,
        descripcion: item.descripcion,
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default Competencias
