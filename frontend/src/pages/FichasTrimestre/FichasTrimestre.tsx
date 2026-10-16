import { Link } from 'react-router-dom'

import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig } from '../../components/crud/EntityForm/EntityForm'

import { fichasTrimestreService } from '../../services/academic.service'
import type { FichaTrimestre } from '../../types/academic.types'
import { formatPeriodo, formatTrimestre } from '../../utils/format'
import { integer, text } from '../../utils/form'
import { opcionesFichas, opcionesTrimestres } from '../../utils/options'

const columns: CrudColumn<FichaTrimestre>[] = [
  { header: 'Ficha', render: (item) => <strong>{item.ficha.codigo}</strong> },
  {
    header: 'Trimestre',
    render: (item) => (
      <>
        {formatTrimestre(item.trimestre)}
        <span className="crud-page__secondary">{formatPeriodo(item.trimestre)}</span>
      </>
    ),
  },
  { header: 'Trimestre de formación', render: (item) => `${item.trimestre_ficha}_TRM` },
  { header: 'Horas / semana', render: (item) => `${item.horas_semanales} h` },
]

const fields: FieldConfig[] = [
  { name: 'ficha_uuid', label: 'Ficha', type: 'select', required: true, loadOptions: opcionesFichas, createOnly: true, fullWidth: true },
  { name: 'trimestre_uuid', label: 'Trimestre del calendario', type: 'select', required: true, loadOptions: opcionesTrimestres, createOnly: true, fullWidth: true },
  {
    name: 'trimestre_ficha',
    label: 'Trimestre de formación',
    type: 'number',
    required: true,
    min: 1,
    max: 20,
    help: 'En qué trimestre va la ficha (el "7" de 7_TRM).',
  },
  { name: 'horas_semanales', label: 'Horas asignadas por semana', type: 'number', required: true, min: 1, max: 60 },
]

const filters: CrudFilter[] = [
  { name: 'ficha_uuid', label: 'Ficha', loadOptions: opcionesFichas },
  { name: 'trimestre_uuid', label: 'Trimestre', loadOptions: opcionesTrimestres },
]

function FichasTrimestre() {
  return (
    <CrudPage
      title="Fichas por trimestre"
      description="Programa cada ficha en un trimestre del calendario con sus horas semanales. Es el encabezado del horario."
      entityName="programación"
      female
      service={fichasTrimestreService}
      columns={columns}
      fields={fields}
      filters={filters}
      emptyValues={{ ficha_uuid: '', trimestre_uuid: '', trimestre_ficha: '', horas_semanales: '' }}
      toFormValues={(item) => ({
        ficha_uuid: item.ficha.uuid,
        trimestre_uuid: item.trimestre.uuid,
        trimestre_ficha: String(item.trimestre_ficha),
        horas_semanales: String(item.horas_semanales),
      })}
      toCreate={(values) => ({
        ficha_uuid: text(values, 'ficha_uuid'),
        trimestre_uuid: text(values, 'trimestre_uuid'),
        trimestre_ficha: integer(values, 'trimestre_ficha'),
        horas_semanales: integer(values, 'horas_semanales'),
      })}
      toUpdate={(values) => ({
        trimestre_ficha: integer(values, 'trimestre_ficha'),
        horas_semanales: integer(values, 'horas_semanales'),
      })}
      rowActions={(item) => (
        <Link
          to={`/gestion/horarios?ficha_trimestre=${item.uuid}`}
          className="btn btn--secondary btn--small"
        >
          Horario
        </Link>
      )}
    />
  )
}

export default FichasTrimestre
