"""Consolidación de totales por estribo y caudal."""

from __future__ import annotations

from socavacion.domain.enums import CondicionCaudal, LadoEstribo
from socavacion.domain.models import Estribo
from socavacion.domain.results import ResultadoEstriboCaudal, ResultadoEstriboFinal


def total_estribo(res: ResultadoEstriboCaudal) -> float:
    """y_s = y_sg + y_sc + y_sl."""
    if res.general is None or res.y_sc is None:
        raise ValueError('Socavación total no evaluada: Froehlich sólo proporciona el componente local.')
    return res.general.y_sg_total + res.y_sc.valor + res.y_sl.valor


def consolidar_estribos(
    estribos: list[Estribo],
    resultados_100: list[ResultadoEstriboCaudal],
    resultados_500: list[ResultadoEstriboCaudal],
    reserva_m: float,
    tipo_superficial: bool,
) -> list[ResultadoEstriboFinal]:
    """Combina Q100 y Q500; calcula cotas."""
    from socavacion.core.elevations import calcular_cotas_estribo

    finales: list[ResultadoEstriboFinal] = []
    map_100 = {r.lado: r for r in resultados_100}
    map_500 = {r.lado: r for r in resultados_500}

    for est in estribos:
        r100 = map_100[est.lado]
        r500 = map_500[est.lado]
        y100 = total_estribo(r100)
        y500 = total_estribo(r500)
        y_diseno = max(y100, y500)
        cotas = calcular_cotas_estribo(
            est.Z_lecho, y_diseno, reserva_m, tipo_superficial
        )
        finales.append(
            ResultadoEstriboFinal(
                lado=est.lado,
                y_s_100=y100,
                y_s_500=y500,
                y_s_diseno=y_diseno,
                Z_lecho_actual=est.Z_lecho,
                Z_lecho_soc=cotas["Z_lecho_soc"],
                Z_cim_min=cotas.get("Z_cim_min"),
                componentes_100=r100,
                componentes_500=r500,
                escenario_diseno=r100.escenario,
                escenario_verificacion=r500.escenario,
            )
        )
    return finales
