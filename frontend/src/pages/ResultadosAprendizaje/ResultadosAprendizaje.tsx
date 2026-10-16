import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'

import { resultadosService } from '../../services/academic.service'
import type { ResultadoAprendizaje } from '../../types/academic.types'
import { text } from '../../utils/form'
import { opcionesCompetencias, opcionesProgramas } from '../../utils/options'

const columns: CrudColumn<ResultadoAprendizaje>[] = [
  { header: 'Código', render: (item) => <strong>{item.codigo}</strong> },
  { header: 'Resultado (temática)', render: (item) => <span className="crud-page__clamp">{item.descripcion}</span> },
  {
    header: 'Competencia',
    render: (item) => (
      <>
        {item.competencia.codigo}
        <span className="crud-page__secondary crud-page__clamp">{item.competencia.descripcion}</span>
      </>
    ),
  },
]

const fields: FieldConfig[] = [
  { name: 'competencia_uuid', label: 'Competencia', type: 'select', required: true, loadOptions: opcionesCompetencias, fullWidth: true },
  { name: 'codigo', label: 'Código', required: true, maxLength: 50, placeholder: '15' },
  {
    name: 'descripcion',
    label: 'Descripción',
    type: 'textarea',
    required: true,
    minLength: 3,
    help: 'Es la "temática" que aparece en cada casilla del horario.',
  },
]

const filters: CrudFilter[] = [
  { name: 'programa_uuid', label: 'Programa', loadOptions: opcionesProgramas },
  { name: 'competencia_uuid', label: 'Competencia', loadOptions: opcionesCompetencias },
]

function toPayload(values: FormValues) {
  return {
    competencia_uuid: text(values, 'competencia_uuid'),
    codigo: text(values, 'codigo'),
    descripcion: text(values, 'descripcion'),
  }
}

function ResultadosAprendizaje() {
  return (
    <CrudPage
      title="Resultados de aprendizaje"
      description="Resultados de cada competencia; son las temáticas que se asignan en el horario."
      entityName="resultado"
      service={resultadosService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ competencia_uuid: '', codigo: '', descripcion: '' }}
      toFormValues={(item) => ({
        competencia_uuid: item.competencia.uuid,
        codigo: item.codigo,
        descripcion: item.descripcion,
      })}
      toCreate={toPayload}
      toUpdate={toPayload}
    />
  )
}

export default ResultadosAprendizaje
