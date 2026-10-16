import { useState } from 'react'

import CrudPage, {
  type CrudColumn,
  type CrudFilter,
} from '../../components/crud/CrudPage/CrudPage'
import type { FieldConfig, FormValues } from '../../components/crud/EntityForm/EntityForm'
import Modal from '../../components/ui/Modal/Modal'

import { fichasService } from '../../services/academic.service'
import type {
  EstadoFicha,
  Ficha,
  ModalidadFicha,
} from '../../types/academic.types'
import { formatDate } from '../../utils/format'
import { text } from '../../utils/form'
import {
  ESTADO_FICHA_LABELS,
  MODALIDAD_FICHA_LABELS,
  toOptions,
} from '../../utils/labels'
import { opcionesJornadas, opcionesProgramas } from '../../utils/options'

import FichaAprendices from './FichaAprendices'

const columns: CrudColumn<Ficha>[] = [
  { header: 'Ficha', render: (item) => <strong>{item.codigo}</strong> },
  {
    header: 'Programa',
    render: (item) => (
      <>
        {item.programa.nombre}
        <span className="crud-page__secondary">{item.programa.codigo}</span>
      </>
    ),
  },
  { header: 'Jornada', render: (item) => item.jornada.nombre },
  { header: 'Modalidad', render: (item) => MODALIDAD_FICHA_LABELS[item.modalidad] },
  {
    header: 'Formación',
    render: (item) => (
      <>
        {formatDate(item.fecha_inicio)} – {formatDate(item.fecha_fin)}
        <span className="crud-page__secondary">{ESTADO_FICHA_LABELS[item.estado]}</span>
      </>
    ),
  },
]

const fields: FieldConfig[] = [
  { name: 'codigo', label: 'Código de ficha', required: true, minLength: 3, maxLength: 20, placeholder: '3141665' },
  { name: 'jornada_uuid', label: 'Jornada', type: 'select', required: true, loadOptions: opcionesJornadas },
  { name: 'programa_uuid', label: 'Programa', type: 'select', required: true, loadOptions: opcionesProgramas, fullWidth: true },
  { name: 'modalidad', label: 'Modalidad', type: 'select', required: true, options: toOptions(MODALIDAD_FICHA_LABELS) },
  { name: 'estado', label: 'Estado', type: 'select', required: true, options: toOptions(ESTADO_FICHA_LABELS) },
  { name: 'fecha_inicio', label: 'Inicio de formación', type: 'date', required: true },
  { name: 'fecha_fin', label: 'Fin de formación', type: 'date', required: true },
]

const filters: CrudFilter[] = [
  { name: 'programa_uuid', label: 'Programa', loadOptions: opcionesProgramas },
  { name: 'jornada_uuid', label: 'Jornada', loadOptions: opcionesJornadas },
]

function toPayload(values: FormValues) {
  return {
    codigo: text(values, 'codigo'),
    programa_uuid: text(values, 'programa_uuid'),
    jornada_uuid: text(values, 'jornada_uuid'),
    modalidad: text(values, 'modalidad') as ModalidadFicha,
    estado: text(values, 'estado') as EstadoFicha,
    fecha_inicio: text(values, 'fecha_inicio'),
    fecha_fin: text(values, 'fecha_fin'),
  }
}

function Fichas() {
  const [fichaAprendices, setFichaAprendices] = useState<Ficha | null>(null)

  return (
    <>
      <CrudPage
        title="Fichas"
        description="Grupos de formación. Desde aquí también se asignan sus aprendices."
        entityName="ficha"
        female
        service={fichasService}
        columns={columns}
        fields={fields}
        filters={filters}
        emptyValues={{
          codigo: '',
          programa_uuid: '',
          jornada_uuid: '',
          modalidad: 'presencial',
          estado: 'en_formacion',
          fecha_inicio: '',
          fecha_fin: '',
        }}
        toFormValues={(item) => ({
          codigo: item.codigo,
          programa_uuid: item.programa.uuid,
          jornada_uuid: item.jornada.uuid,
          modalidad: item.modalidad,
          estado: item.estado,
          fecha_inicio: item.fecha_inicio,
          fecha_fin: item.fecha_fin,
        })}
        toCreate={toPayload}
        toUpdate={toPayload}
        rowActions={(item) => (
          <button
            type="button"
            className="btn btn--secondary btn--small"
            onClick={() => setFichaAprendices(item)}
          >
            Aprendices
          </button>
        )}
      />

      <Modal
        open={fichaAprendices !== null}
        title={`Aprendices de la ficha ${fichaAprendices?.codigo ?? ''}`}
        description={fichaAprendices?.programa.nombre}
        onClose={() => setFichaAprendices(null)}
        size="lg"
      >
        {fichaAprendices && <FichaAprendices ficha={fichaAprendices} />}
      </Modal>
    </>
  )
}

export default Fichas
