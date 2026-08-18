"""Socavación general — Lacey (control cauces aluviales)."""

from __future__ import annotations

import math

from socavacion.core.general import ContextoGeneral
from socavacion.domain.results import ComponenteSocavacion


def calcular(ctx: ContextoGeneral) -> ComponenteSocavacion:
    f = 1.76 * math.sqrt(ctx.d50_mm)
    if f <= 0:
        return ComponenteSocavacion(
            metodo="Lacey",
            valor=0.0,
            formula="R = 0.47*(Q/f)^(1/3); y_sg = max(R - y0, 0)",
            intermedios={"f": f},
        )
    R = 0.47 * ((ctx.Q / f) ** (1 / 3))
    y_sg = max(R - ctx.y0, 0.0)
    return ComponenteSocavacion(
        metodo="Lacey",
        valor=y_sg,
        formula="R = 0.47*(Q/f)^(1/3); y_sg = max(R - y0, 0)",
        intermedios={"f": f, "R": R},
    )
