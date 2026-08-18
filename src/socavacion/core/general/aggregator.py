"""Agregación de métodos de socavación general."""

from __future__ import annotations

from socavacion.core.general import ContextoGeneral
from socavacion.core.general import lacey, lischtvan, neill
from socavacion.domain.results import ComponenteSocavacion, ResultadoGeneral


def calcular_general(
    Q: float,
    hidraulica,
    d50_m: float,
    d50_mm: float,
    y_sg_lp: float,
    q1: float | None = None,
    q2: float | None = None,
) -> ResultadoGeneral:
    ctx = ContextoGeneral(
        Q=Q,
        y0=hidraulica.y0,
        y1=hidraulica.y1,
        W=hidraulica.W1,
        q=hidraulica.q1,
        d50_m=d50_m,
        d50_mm=d50_mm,
    )
    r_lischtvan = lischtvan.calcular(ctx)
    r_neill = neill.calcular(ctx, q1=q1, q2=q2)
    r_lacey = lacey.calcular(ctx)

    candidatos = [r_lischtvan, r_neill, r_lacey]
    gobernante = max(candidatos, key=lambda c: c.valor)
    y_sg_avenida = gobernante.valor
    y_sg_lp_efectivo = max(y_sg_lp, 0.0)  # agradación no reduce diseño
    y_sg_total = y_sg_lp_efectivo + y_sg_avenida

    return ResultadoGeneral(
        y_sg_lp=y_sg_lp_efectivo,
        y_sg_lischtvan=r_lischtvan,
        y_sg_neill=r_neill,
        y_sg_lacey=r_lacey,
        y_sg_avenida=y_sg_avenida,
        y_sg_total=y_sg_total,
        metodo_gobernante=gobernante.metodo,
    )
