"""Controles del alcance LL granular y de la evidencia de entrada."""
from socavacion.domain.models import Proyecto
from socavacion.domain.observations import resumir_advertencias


def validar_proyecto(proyecto: Proyecto) -> list[str]:
    pendientes = []
    if proyecto.metodo_calculo == 'froehlich':
        from socavacion.input.hec_ras import validar_froehlich
        return validar_froehlich(proyecto)
    if proyecto.datos_prueba:
        if proyecto.modo != 'preliminar':
            raise ValueError('Un proyecto marcado datos_prueba debe mantenerse en modo preliminar; no certifica un diseño real.')
    if proyecto.material_lecho != 'granular':
        raise ValueError('Este motor implementa LL granular ec.59; cohesivos/roca requieren otro análisis.')
    if proyecto.flujo != 'libre' or not proyecto.lecho_homogeneo:
        raise ValueError('Fuera de alcance: requiere flujo libre y lecho homogéneo; estudiar presión, detritos o estratos por separado.')
    if proyecto.Q500 < proyecto.Q100:
        raise ValueError('Q500 < Q100: corregir la hidrología antes del cálculo.')
    if len({p.nombre for p in proyecto.pilares}) != len(proyecto.pilares):
        raise ValueError('Nombres de pilares duplicados.')
    if proyecto.Q_ot is not None and proyecto.T_ot is None:
        raise ValueError('Q_ot requiere T_ot y qot independiente en cada apoyo.')
    if proyecto.Q_ot is None and proyecto.T_ot is not None:
        raise ValueError('T_ot requiere Q_ot.')
    if proyecto.Q_ot is None and not proyecto.justificacion_sin_desbordamiento.strip():
        pendientes.append('Falta justificacion_sin_desbordamiento (MP 1.2.3a).')
    campos_proyecto = ['hidrologia', 'topografia', 'largo_plazo']
    if proyecto.geotecnia.evaluar:
        campos_proyecto.append('geotecnia')
        if proyecto.geotecnia.cota_sondaje_min is None:
            pendientes.append('Falta cota de sondaje para la evaluación geotécnica solicitada.')
    for campo in campos_proyecto:
        if not proyecto.fuentes.get(campo, '').strip():
            pendientes.append(f'Falta fuente del proyecto: {campo}.')
    for apoyo in [*proyecto.estribos(), *proyecto.pilares]:
        nombre = getattr(apoyo, 'nombre', None) or apoyo.lado.value
        if apoyo.D50_mm is None:
            raise ValueError(f'{nombre}: el cálculo completo histórico requiere D50.')
        if hasattr(apoyo, 'metodo_local') and apoyo.Z_lecho is None:
            raise ValueError(f'{nombre}: el cálculo completo histórico requiere Z_lecho.')
        if getattr(apoyo, 'Z_lecho', None) is None:
            pendientes.append(f'{nombre}: falta Z_lecho.')
        eventos = [('q100',proyecto.Q100),('q500',proyecto.Q500)]
        if proyecto.Q_ot is not None:
            eventos.append(('qot',proyecto.Q_ot))
        for etiqueta, Q in eventos:
            hid = getattr(apoyo, etiqueta)
            if hid is None:
                raise ValueError(f'{nombre}: falta hidráulica {etiqueta}; no reutilizar Q100/Q500.')
            if any(getattr(hid, k) is None for k in ('y1', 'V1', 'W1', 'W2', 'y0')):
                raise ValueError(f'{nombre}/{etiqueta}: faltan parámetros del cálculo completo histórico.')
            if hid.Qe is not None and hid.Qe > Q:
                raise ValueError(f'{nombre}/{etiqueta}: Qe supera el caudal total.')
            if hid.Q_ll is not None and hid.Q_ll > Q:
                raise ValueError(f'{nombre}/{etiqueta}: Q_ll supera el caudal total.')
            necesarios = ['beta','phi','exponente_x','Dm_mm','h_local']
            if hid.alpha is None:
                necesarios += ['Q_ll','B_ll','h_m_ll']
            if hid.luz_libre is None:
                necesarios += ['mu']
            else:
                necesarios += ['V_mu']
            for campo in necesarios:
                if campo not in hid.model_fields_set or getattr(hid, campo) is None:
                    pendientes.append(f'{nombre}/{etiqueta}: falta dato explícito {campo}.')
            fuentes = ['hidraulica','granulometria','beta','exponente_x','phi','geometria']
            fuentes += ['luz_libre'] if hid.luz_libre is not None else ['mu']
            fuentes += ['alpha'] if hid.alpha is not None else ['cierre_alpha']
            if hasattr(apoyo,'metodo_local'):
                fuentes.append('local')
                if apoyo.metodo_local == 'froehlich':
                    if hid.Qe is None or hid.Qe <= 0 or (hid.Ae if hid.Ae is not None else apoyo.Ae) <= 0:
                        pendientes.append(f'{nombre}/{etiqueta}: Froehlich requiere Qe>0 y Ae>0; no extrapolar a ausencia de obstrucción.')
            else:
                fuentes.append('pilar')
            for campo in fuentes:
                if not hid.fuentes.get(campo, '').strip():
                    pendientes.append(f'{nombre}/{etiqueta}: falta fuente {campo}.')
            if hid.luz_libre is not None and 'mu' in hid.model_fields_set:
                pendientes.append(f'{nombre}/{etiqueta}: mu manual ignorado; gobierna Tabla 13 con luz_libre/V_mu.')
    if proyecto.geotecnia.tipo_cimentacion.value == 'sobre_roca' and not proyecto.geotecnia.roca_resistente:
        raise ValueError('Cimentación sobre roca requiere roca_resistente sustentada.')
    if proyecto.modo == 'trazable' and pendientes:
        raise ValueError('Datos insuficientes para modo trazable:\n' + '\n'.join(resumir_advertencias(pendientes)))
    if proyecto.datos_prueba:
        pendientes.insert(0, 'DATOS DE PRUEBA SINTÉTICOS: valores y fuentes de ejemplo; NO utilizar para diseño ni construcción.')
    return pendientes
