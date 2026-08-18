"""Socavación general — Lischtvan-Lebediev."""

from __future__ import annotations

from socavacion.core.general import ContextoGeneral
from socavacion.core.interpolation import interpolar_doble
from socavacion.domain.results import ComponenteSocavacion
from socavacion.normative.tables import LISCHTVAN_TABLE


def calcular(ctx: ContextoGeneral) -> ComponenteSocavacion:
    x_exp, A = interpolar_doble(ctx.d50_mm, LISCHTVAN_TABLE)
    h_sg = A * (ctx.q ** x_exp)
    y_sg = max(h_sg - ctx.y0, 0.0)
    return ComponenteSocavacion(
        metodo="Lischtvan-Lebediev",
        valor=y_sg,
        formula="h_sg = A * q^x; y_sg = max(h_sg - y0, 0)",
        intermedios={"A": A, "x": x_exp, "h_sg": h_sg, "q": ctx.q},
    )
