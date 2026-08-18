"""Socavación general — Neill (verificación)."""

from __future__ import annotations

from socavacion.core.general import ContextoGeneral
from socavacion.domain.results import ComponenteSocavacion


def calcular(ctx: ContextoGeneral, q1: float | None = None, q2: float | None = None) -> ComponenteSocavacion:
    q1_val = q1 if q1 is not None else ctx.q
    q2_val = q2 if q2 is not None else ctx.q
    if q1_val <= 0:
        y_sg = 0.0
        y2 = ctx.y1
    else:
        ratio = q2_val / q1_val
        y2 = ctx.y1 * (ratio ** (6 / 7))
        y_sg = max(y2 - ctx.y1, 0.0)
    return ComponenteSocavacion(
        metodo="Neill",
        valor=y_sg,
        formula="y2/y1 = (q2/q1)^(6/7); y_sg = max(y2 - y1, 0)",
        intermedios={"y2": y2, "q1": q1_val, "q2": q2_val},
    )
