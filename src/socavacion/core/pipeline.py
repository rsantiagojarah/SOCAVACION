"""Orquestador del pipeline de cálculo."""

from __future__ import annotations

from socavacion.core.contraction import calcular_contraccion
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
)
from socavacion.core.elevations import requiere_reserva
from socavacion.geotech.compatibility import evaluar_compatibilidad


def _hidraulica_por_condicion(estribo: Estribo, cond: CondicionCaudal) -> CondicionHidraulica:
    return estribo.q100 if cond == CondicionCaudal.DISENO else estribo.q500


def _calcular_caudal(proyecto: Proyecto, cond: CondicionCaudal, Q: float) -> ResultadoCaudal:
    y_sg_lp, lp_adv = calcular_y_sg_lp(proyecto.cauce)
    resultados_estribo: list[ResultadoEstriboCaudal] = []

    for estribo in proyecto.estribos():
        hid = _hidraulica_por_condicion(estribo, cond)
        regimen = detectar_regimen(hid.V1, hid.y1, estribo.D50_m, hid.Sf)
        general = calcular_general(
            Q=Q,
            hidraulica=hid,
            d50_m=estribo.D50_m,
            d50_mm=estribo.D50_mm,
            y_sg_lp=y_sg_lp,
            q1=hid.q1,
            q2=hid.q2,
        )
        y_sc, sc_adv = calcular_contraccion(hid, regimen, estribo.D50_m)
        y_sl, sl_adv = calcular_local_estribo(estribo, hid, regimen)
        advertencias = lp_adv + sc_adv + sl_adv
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
            )
        )

    resultados_pilar: list[ResultadoPilarCaudal] = []
    for pilar in proyecto.pilares:
        hid = pilar.q100 if cond == CondicionCaudal.DISENO else pilar.q500
        regimen = detectar_regimen(hid.V1, hid.y1, pilar.D50_m, hid.Sf)
        y_sp = calcular_local_pilar(pilar, hid, regimen)
        resultados_pilar.append(
            ResultadoPilarCaudal(
                nombre=pilar.nombre,
                condicion=cond,
                y_sp=y_sp,
                regimen=regimen.regimen,
            )
        )

    for r in resultados_estribo:
        r.y_s_total = total_estribo(r)

    return ResultadoCaudal(condicion=cond, Q=Q, estribos=resultados_estribo, pilares=resultados_pilar)


def ejecutar(proyecto: Proyecto) -> ResultadoCompleto:
    """Ejecuta pipeline completo Q100/Q500."""
    advertencias_globales: list[str] = []

    r100 = _calcular_caudal(proyecto, CondicionCaudal.DISENO, proyecto.Q_diseno_soc)
    r500 = _calcular_caudal(proyecto, CondicionCaudal.VERIFICACION, proyecto.Q_verif_soc)

    reserva = requiere_reserva(proyecto.geotecnia)
    estribos_finales = consolidar_estribos(
        proyecto.estribos(),
        r100.estribos,
        r500.estribos,
        reserva_m=1.0,
        tipo_superficial=reserva,
    )

    geo = evaluar_compatibilidad(proyecto, estribos_finales)

    return ResultadoCompleto(
        proyecto_nombre=proyecto.nombre,
        Q_diseno=proyecto.Q_diseno_soc,
        Q_verif=proyecto.Q_verif_soc,
        caudales=[r100, r500],
        estribos_finales=estribos_finales,
        geotecnia=geo,
        advertencias_globales=advertencias_globales,
    )
