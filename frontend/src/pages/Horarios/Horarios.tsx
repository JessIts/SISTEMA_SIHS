import { useCallback, useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

import PageHeader from '../../components/common/PageHeader/PageHeader'
import HorarioGrid from '../../components/horario/HorarioGrid/HorarioGrid'
import HorarioHeader from '../../components/horario/HorarioHeader/HorarioHeader'
import { ClaseFicha } from '../../components/horario/ClaseContent/ClaseContent'
import Modal from '../../components/ui/Modal/Modal'

import {
  ambientesService,
  fichasService,
  fichasTrimestreService,
  getGrillaHorario,
  horariosService,
  resultadosService,
} from '../../services/academic.service'
import type {
  ClaseCelda,
  FichaTrimestre,
  GridCell,
  GridRow,
  HorarioGrilla,
} from '../../types/academic.types'
import { errorMessage, formatTime, formatTrimestre } from '../../utils/format'
import { toSelectOptions } from '../../utils/form'
import { opcionesInstructores } from '../../utils/options'

import HorarioForm, {
  type HorarioFormOptions,
  type HorarioFormValues,
} from './HorarioForm'

import './Horarios.css'

type Editor =
  | { mode: 'create'; values: HorarioFormValues; titulo: string }
  | { mode: 'edit'; uuid: string; values: HorarioFormValues; titulo: string }
  | null

type Catalogos = Pick<HorarioFormOptions, 'resultados' | 'instructores' | 'ambientes'>

const EMPTY_CATALOGOS: Catalogos = {
  resultados: [],
  instructores: [],
  ambientes: [],
}

/**
 * Editor del horario de una ficha en un trimestre.
 * Clic en una casilla vacía -> asignar clase; en una ocupada -> editar / eliminar.
 */
function Horarios() {
  const [searchParams, setSearchParams] = useSearchParams()
  const selected = searchParams.get('ficha_trimestre') ?? ''

  const [programaciones, setProgramaciones] = useState<FichaTrimestre[]>([])
  const [grilla, setGrilla] = useState<HorarioGrilla | null>(null)
  const [catalogos, setCatalogos] = useState<Catalogos>(EMPTY_CATALOGOS)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  const [editor, setEditor] = useState<Editor>(null)

  // 1) Programaciones disponibles (ficha + trimestre)
  useEffect(() => {
    let active = true

    async function load() {
      try {
        const items = await fichasTrimestreService.listAll()

        if (active) {
          setProgramaciones(items)

          if (items.length === 0) {
            setLoading(false)
          }
        }
      } catch (loadError) {
        if (active) {
          setError(errorMessage(loadError, 'No fue posible cargar las fichas programadas.'))
          setLoading(false)
        }
      }
    }

    load()

    return () => {
      active = false
    }
  }, [])

  // Si no viene una en la URL, se abre la primera
  useEffect(() => {
    if (!selected && programaciones.length > 0) {
      setSearchParams({ ficha_trimestre: programaciones[0].uuid }, { replace: true })
    }
  }, [selected, programaciones, setSearchParams])

  const programacion = useMemo(
    () => programaciones.find((item) => item.uuid === selected),
    [programaciones, selected],
  )

  // 2) Grilla de la programación seleccionada
  const loadGrilla = useCallback(async () => {
    if (!selected) {
      return
    }

    try {
      setLoading(true)
      setError('')

      setGrilla(await getGrillaHorario(selected))
    } catch (loadError) {
      setGrilla(null)
      setError(errorMessage(loadError, 'No fue posible cargar el horario.'))
    } finally {
      setLoading(false)
    }
  }, [selected])

  useEffect(() => {
    void loadGrilla()
  }, [loadGrilla])

  // 3) Opciones del formulario: temáticas del programa de la ficha,
  //    instructores y ambientes (se cargan una vez por ficha)
  const fichaUuid = programacion?.ficha.uuid

  useEffect(() => {
    if (!fichaUuid) {
      return
    }

    let active = true

    async function loadOptions(uuid: string) {
      try {
        const ficha = await fichasService.get(uuid)

        const [resultados, instructores, ambientes] = await Promise.all([
          resultadosService.listAll({ programa_uuid: ficha.programa.uuid }),
          opcionesInstructores(),
          ambientesService.listAll(),
        ])

        if (active) {
          setCatalogos({
            resultados: toSelectOptions(
              resultados,
              (resultado) => `${resultado.codigo}. ${resultado.descripcion}`,
            ),
            instructores,
            ambientes: toSelectOptions(
              ambientes,
              (ambiente) => `${ambiente.nombre} · ${ambiente.sede.nombre}`,
            ),
          })
        }
      } catch (loadError) {
        if (active) {
          setError(errorMessage(loadError, 'No fue posible cargar las opciones del horario.'))
        }
      }
    }

    void loadOptions(fichaUuid)

    return () => {
      active = false
    }
  }, [fichaUuid])

  // Días y franjas salen de la misma grilla
  const options = useMemo<HorarioFormOptions>(() => ({
    ...catalogos,
    dias: grilla ? toSelectOptions(grilla.dias, (dia) => dia.nombre) : [],
    franjas: grilla
      ? grilla.jornadas.flatMap((jornada) =>
          jornada.franjas.map((row) => ({
            value: row.franja_uuid,
            label: `${formatTime(row.hora_inicio)} – ${formatTime(row.hora_fin)} (${jornada.jornada})`,
          })),
        )
      : [],
  }), [catalogos, grilla])

  async function handleCellClick(row: GridRow<ClaseCelda>, cell: GridCell<ClaseCelda>) {
    if (!grilla) {
      return
    }

    setNotice('')

    const dia = grilla.dias.find((item) => item.numero === cell.dia_numero)
    const titulo = `${cell.dia} · ${formatTime(row.hora_inicio)} – ${formatTime(row.hora_fin)}`

    if (!cell.clase) {
      setEditor({
        mode: 'create',
        titulo,
        values: {
          dia_uuid: dia?.uuid ?? '',
          franja_uuid: row.franja_uuid,
          resultado_uuid: '',
          instructor_uuid: '',
          modalidad: 'presencial',
          ambiente_uuid: '',
          observacion: '',
        },
      })
      return
    }

    try {
      const horario = await horariosService.get(cell.clase.horario_uuid)

      setEditor({
        mode: 'edit',
        uuid: horario.uuid,
        titulo,
        values: {
          dia_uuid: horario.dia.uuid,
          franja_uuid: horario.franja.uuid,
          resultado_uuid: horario.resultado.uuid,
          instructor_uuid: horario.instructor.uuid,
          modalidad: horario.modalidad,
          ambiente_uuid: horario.ambiente?.uuid ?? '',
          observacion: horario.observacion ?? '',
        },
      })
    } catch (loadError) {
      setError(errorMessage(loadError, 'No fue posible abrir la clase.'))
    }
  }

  async function handleSubmit(values: HorarioFormValues) {
    if (!editor) {
      return
    }

    const payload = {
      dia_uuid: values.dia_uuid,
      franja_uuid: values.franja_uuid,
      resultado_uuid: values.resultado_uuid,
      instructor_uuid: values.instructor_uuid,
      modalidad: values.modalidad,
      ambiente_uuid: values.modalidad === 'presencial' ? values.ambiente_uuid : null,
      observacion: values.observacion.trim() || null,
    }

    if (editor.mode === 'create') {
      await horariosService.create({ ...payload, ficha_trimestre_uuid: selected })
      setNotice('Clase asignada correctamente.')
    } else {
      await horariosService.update(editor.uuid, payload)
      setNotice('Clase actualizada correctamente.')
    }

    setEditor(null)
    await loadGrilla()
  }

  async function handleDelete() {
    if (editor?.mode !== 'edit') {
      return
    }

    await horariosService.remove(editor.uuid)

    setEditor(null)
    setNotice('Clase eliminada. La casilla quedó libre.')
    await loadGrilla()
  }

  return (
    <section className="horarios-page">
      <PageHeader
        title="Horarios"
        description="Arma el horario de cada ficha. Haz clic en una casilla para asignar o editar la clase."
        actions={
          <Link to="/gestion/fichas-trimestre" className="btn btn--secondary">
            Programar ficha en trimestre
          </Link>
        }
      />

      <div className="horarios-page__card">
        <label className="horarios-page__selector">
          <span>Ficha y trimestre</span>

          <select
            value={selected}
            onChange={(event) => {
              setNotice('')
              setSearchParams({ ficha_trimestre: event.target.value })
            }}
            disabled={programaciones.length === 0}
          >
            {programaciones.length === 0 && <option value="">No hay fichas programadas</option>}

            {programaciones.map((item) => (
              <option key={item.uuid} value={item.uuid}>
                Ficha {item.ficha.codigo} · {item.trimestre_ficha}_TRM · {formatTrimestre(item.trimestre)}
              </option>
            ))}
          </select>
        </label>

        {notice && <p className="horarios-page__notice">{notice}</p>}
        {error && <p className="horarios-page__error">{error}</p>}

        {!loading && programaciones.length === 0 && !error && (
          <p className="horarios-page__muted">
            Primero programa una ficha en un trimestre desde{' '}
            <Link to="/gestion/fichas-trimestre">Fichas por trimestre</Link>.
          </p>
        )}

        {loading && <p className="horarios-page__muted">Cargando horario...</p>}

        {!loading && grilla && (
          <>
            <HorarioHeader encabezado={grilla.encabezado} />

            <HorarioGrid
              dias={grilla.dias}
              jornadas={grilla.jornadas}
              renderClase={(clase) => <ClaseFicha clase={clase} />}
              onCellClick={(row, cell) => void handleCellClick(row, cell)}
            />
          </>
        )}
      </div>

      <Modal
        open={editor !== null}
        title={editor?.mode === 'edit' ? 'Editar clase' : 'Asignar clase'}
        description={editor ? `Ficha ${grilla?.encabezado.ficha ?? ''} · ${editor.titulo}` : undefined}
        onClose={() => setEditor(null)}
      >
        {editor && (
          <HorarioForm
            key={editor.mode === 'edit' ? editor.uuid : `${editor.values.dia_uuid}-${editor.values.franja_uuid}`}
            initialValues={editor.values}
            options={options}
            isEdit={editor.mode === 'edit'}
            onSubmit={handleSubmit}
            onDelete={handleDelete}
            onCancel={() => setEditor(null)}
          />
        )}
      </Modal>
    </section>
  )
}

export default Horarios
