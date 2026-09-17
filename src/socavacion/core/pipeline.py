"""Orquestador del pipeline de cálculo."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from socavacion.input.validator import validar_proyecto
from socavacion.normative.references import VERSION, REFERENCIAS, verificar_documentos
from socavacion.core.general.aggregator import calcular_general
from socavacion.core.local_abutment import calcular_local_estribo
from socavacion.core.local_pier import calcular_local_pilar
from socavacion.core.long_term import calcular_y_sg_lp
from socavacion.core.regime import detectar_regimen
from socavacion.core.totals import consolidar_estribos, total_estribo
from socavacion.domain.enums import CondicionCaudal
from socavacion.domain.models import CondicionHidraulica, Estribo, Proyecto
from socavacion.domain.results import (
    ResultadoCaudal,
    ResultadoCompleto,
    ResultadoEstriboCaudal,
    ResultadoPilarCaudal,
    ComponenteSocavacion,
    ResultadoPilarFinal,
    ResultadoEstriboFinal,
)
from socavacion.core.elevations import requiere_reserva
from socavacion.geotech.compatibility import evaluar_compatibilidad


def _hidraulica_por_condicion(estribo: Estribo, cond: CondicionCaudal) -> CondicionHidraulica:
    return getattr(estribo, {CondicionCaudal.DISENO:'q100', CondicionCaudal.VERIFICACION:'q500',
                            CondicionCaudal.DESBORDAMIENTO:'qot'}[cond])


def _calcular_caudal(proyecto: Proyecto, cond: CondicionCaudal, Q: float) -> ResultadoCaudal:
    escenario = {CondicionCaudal.DISENO:'Q100', CondicionCaudal.VERIFICACION:'Q500',
                 CondicionCaudal.DESBORDAMIENTO:'Qot'}[cond]
    y_sg_lp, lp_adv = calcular_y_sg_lp(proyecto.cauce)
    resultados_estribo: list[ResultadoEstriboCaudal] = []

    for estribo in proyecto.estribos():
        hid = _hidraulica_por_condicion(estribo, cond)
        if proyecto.metodo_calculo == 'froehlich':
            local, avisos = calcular_local_estribo(estribo, hid, None)
            local.intermedios.update(A_total=hid.area_hidraulica, Q_total=Q,
                                     V_media_seccion=Q/hid.area_hidraulica)
            local.unidades.update(A_total='m2 (control)', Q_total='m3/s (control)',
                                   V_media_seccion='m/s (informativa; no sustituye Ve)')
            if hid.radio_hidraulico is not None:
                local.intermedios['R_informativo'] = hid.radio_hidraulico
                local.unidades['R_informativo'] = 'm (no interviene en Froehlich)'
            resultados_estribo.append(ResultadoEstriboCaudal(
                lado=estribo.lado, condicion=cond, regimen=None, general=None,
                y_sc=None, y_sl=local, y_s_total=None, advertencias=avisos, escenario=escenario))
            continue
        regimen = detectar_regimen(hid.V1, hid.y1, estribo.D50_m, hid.Sf, calcular_legacy=False)
        general = calcular_general(
            Q=Q,
            hidraulica=hid,
            d50_m=estribo.D50_m,
            d50_mm=estribo.D50_mm,
            y_sg_lp=y_sg_lp,
        )
        # La ecuación MTC HHD usada en general ya incluye la contracción.
        y_sc = ComponenteSocavacion(
            metodo="Incluida en Lischtvan-Levediev MTC HHD",
            valor=0.0,
            formula="y_sc independiente = 0; contracción incluida mediante mu",
            intermedios={"mu": general.y_sg_lischtvan.intermedios['mu']},
            notas="Evita doble conteo de la contracción del puente.",
            referencias=['LL59','MP123a'], unidades={'mu':'1'},
        )
        sc_adv: list[str] = []
        y_sl, sl_adv = calcular_local_estribo(estribo, hid, regimen)
        advertencias = lp_adv + sc_adv + sl_adv + general.y_sg_lischtvan.supuestos
        if proyecto.cauce.y_sg_lp < 0 and proyecto.cauce.tipo.value == "agradacion":
            advertencias.append("Agradación: y_sg_lp no reduce diseño")

        resultados_estribo.append(
            ResultadoEstriboCaudal(
                lado=estribo.lado,
                condicion=cond,
                regimen=regimen,
                general=general,
                y_sc=y_sc,
                y_sl=y_sl,
                y_s_total=0.0,
                advertencias=advertencias,
                escenario=escenario,
            )
        )

    resultados_pilar: list[ResultadoPilarCaudal] = []
    for pilar in proyecto.pilares:
        hid = _hidraulica_por_condicion(pilar, cond)
        regimen = detectar_regimen(hid.V1, hid.y1, pilar.D50_m, hid.Sf, calcular_legacy=False)
        y_sp = calcular_local_pilar(pilar, hid, regimen)
        general = calcular_general(Q, hid, pilar.D50_m, pilar.D50_mm, y_sg_lp)
        total = general.y_sg_total + y_sp.valor
        resultados_pilar.append(
            ResultadoPilarCaudal(
                nombre=pilar.nombre,
                condicion=cond,
                y_sp=y_sp,
                regimen=regimen.regimen,
                general=general, y_s_total=total,
                Z_lecho_soc=None if pilar.Z_lecho is None else pilar.Z_lecho-total,
                escenario=escenario,
            )
        )

    for r in resultados_estribo:
        if proyecto.metodo_calculo != 'froehlich':
            r.y_s_total = total_estribo(r)

    return ResultadoCaudal(condicion=cond, Q=Q, estribos=resultados_estribo, pilares=resultados_pilar, escenario=escenario)


def ejecutar(proyecto: Proyecto) -> ResultadoCompleto:
    """Ejecuta pipeline completo Q100/Q500."""
    advertencias_globales = validar_proyecto(proyecto)
    advertencias_globales.extend(proyecto.supuestos)
    documentos = verificar_documentos()
    if not all(d['coincide'] for d in documentos.values()):
        if proyecto.modo == 'trazable':
            raise ValueError('Los manuales locales faltan o cambiaron de SHA256; revisar referencias.')
        advertencias_globales.append('Manuales ausentes o diferentes de la versión contrastada.')
    if proyecto.modo == 'preliminar':
        advertencias_globales.insert(0, 'ESCENARIO PRELIMINAR: incluye supuestos; no constituye aprobación del diseño.')

    r100 = _calcular_caudal(proyecto, CondicionCaudal.DISENO, proyecto.Q_diseno_soc)
    r500 = _calcular_caudal(proyecto, CondicionCaudal.VERIFICACION, proyecto.Q_verif_soc)
    caudales = [r100, r500]
    rot = None
    if proyecto.Q_ot is not None:
        rot = _calcular_caudal(proyecto, CondicionCaudal.DESBORDAMIENTO, proyecto.Q_ot)
        caudales.append(rot)
    # Severidad por socavación en cada apoyo, nunca max(Q100,Qot).
    solo_local = proyecto.metodo_calculo == 'froehlich'
    def severidad(r):
        return r.y_sl.valor if solo_local else r.y_s_total
    seleccion100, seleccion500 = [], []
    for i in range(len(proyecto.estribos())):
        seleccion100.append(max([r100.estribos[i]] + ([rot.estribos[i]] if rot and proyecto.T_ot < 100 else []), key=severidad))
        seleccion500.append(max([r500.estribos[i]] + ([rot.estribos[i]] if rot and proyecto.T_ot < 500 else []), key=severidad))

    reserva = requiere_reserva(proyecto.geotecnia)
    estribos_finales = [ResultadoEstriboFinal(
        lado=e.lado, y_s_100=d.y_sl.valor, y_s_500=v.y_sl.valor,
        y_s_diseno=max(d.y_sl.valor, v.y_sl.valor), Z_lecho_actual=None,
        Z_lecho_soc=None, Z_cim_min=None, componentes_100=d, componentes_500=v,
        escenario_diseno=d.escenario, escenario_verificacion=v.escenario)
        for e, d, v in zip(proyecto.estribos(), seleccion100, seleccion500)] if solo_local else consolidar_estribos(
        proyecto.estribos(),
        seleccion100,
        seleccion500,
        reserva_m=1.0,
        tipo_superficial=reserva,
    )

    pilares_finales = []
    for i, pilar in enumerate(proyecto.pilares):
        diseno = max([r100.pilares[i]] + ([rot.pilares[i]] if rot and proyecto.T_ot < 100 else []), key=lambda r:r.y_s_total)
        verif = max([r500.pilares[i]] + ([rot.pilares[i]] if rot and proyecto.T_ot < 500 else []), key=lambda r:r.y_s_total)
        total = max(diseno.y_s_total, verif.y_s_total)
        z = None if pilar.Z_lecho is None else pilar.Z_lecho-total
        pilares_finales.append(ResultadoPilarFinal(pilar.nombre, diseno.y_s_total, verif.y_s_total, total,
                               z, z-1 if reserva and z is not None else None, diseno.escenario, verif.escenario))
    geo = evaluar_compatibilidad(proyecto, estribos_finales, caudales, pilares_finales)
    entrada = proyecto.model_dump(mode='json', exclude_unset=True)
    firma = hashlib.sha256(json.dumps(entrada, sort_keys=True, ensure_ascii=False, allow_nan=False).encode('utf-8')).hexdigest()
    codigo_raiz = Path(__file__).resolve().parents[1]
    archivos_codigo = {p.relative_to(codigo_raiz).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted(codigo_raiz.rglob('*.py'))}
    auditoria = {'version_metodo':VERSION, 'modo':proyecto.modo, 'entrada_sha256':firma,
                 'entrada':entrada, 'documentos':documentos, 'referencias':REFERENCIAS,
                 'convencion':'ds=max(Hs-h_local,0); LL incluye contracción; total=LP+LL+local del mismo apoyo',
                 'estado_limite':{'diseno':'Resistencia y servicio', 'verificacion':'Evento extremo'},
                 'alcance':'LL granular homogéneo, flujo libre; requiere estudio hidráulico y granulometría; no calcula capacidad ni estabilidad de cimentación',
                 'archivos_codigo': archivos_codigo,
                 'fuente_codigo_sha256': hashlib.sha256(json.dumps(archivos_codigo, sort_keys=True).encode()).hexdigest()}
    auditoria['metodo_calculo'] = proyecto.metodo_calculo
    if solo_local:
        from socavacion.input.hec_ras import ALCANCE
        auditoria.update(alcance=ALCANCE,
                         convencion='y_sl=Froehlich; general, contraccion, y_s_total y cotas = null (NO EVALUADOS). Envolventes sólo locales.',
                         referencias={k: REFERENCIAS[k] for k in ('F92', 'MP123a')},
                         estado_limite={'diseno': 'Envolvente LOCAL Q100/Qot, evaluación parcial',
                                        'verificacion': 'Envolvente LOCAL Q500/Qot, evaluación parcial'})

    return ResultadoCompleto(
        proyecto_nombre=proyecto.nombre,
        Q_diseno=proyecto.Q_diseno_soc,
        Q_verif=proyecto.Q_verif_soc,
        caudales=caudales,
        estribos_finales=estribos_finales,
        geotecnia=geo,
        advertencias_globales=advertencias_globales,
        pilares_finales=pilares_finales, auditoria=auditoria,
    )
