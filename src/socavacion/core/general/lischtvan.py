"""Socavación general — Lischtvan-Lebediev."""

from __future__ import annotations

import math

from socavacion.core.general import ContextoGeneral
from socavacion.core.interpolation import interpolar_doble
from socavacion.domain.results import ComponenteSocavacion
from socavacion.normative.tables import LISCHTVAN_TABLE


def calcular(ctx: ContextoGeneral) -> ComponenteSocavacion:
    """API histórica no contrastada con ec.59: fuera del motor MTC-LL-2.0."""
    x_exp, A = interpolar_doble(ctx.d50_mm, LISCHTVAN_TABLE)
    h_sg = A * (ctx.q ** x_exp)
    y_sg = max(h_sg - ctx.y0, 0.0)
    return ComponenteSocavacion(
        metodo="Lischtvan-Lebediev",
        valor=y_sg,
        formula="h_sg = A * q^x; y_sg = max(h_sg - y0, 0)",
        intermedios={"A": A, "x": x_exp, "h_sg": h_sg, "q": ctx.q},
    )


def calcular_mtc_hhd(
    *,
    Q: float,
    h_m: float,
    B: float,
    dm_mm: float,
    beta: float,
    mu: float,
    phi: float,
    x: float,
    h_local: float | None = None,
    alpha: float | None = None,
) -> ComponenteSocavacion:
    """Lischtvan-Levediev granular, MTC HHD ecuación (59), Dm en mm.

    El resultado incluye el efecto de contracción mediante ``mu``; por ello
    no debe sumarse una socavación de contracción independiente.
    """
    h = h_m if h_local is None else h_local
    if not all(math.isfinite(v) and v > 0 for v in (Q, h_m, B, dm_mm, beta, mu, phi, x, h)):
        raise ValueError('LL requiere valores positivos y finitos')
    if mu > 1 or phi < 1:
        raise ValueError('LL requiere 0 < mu <= 1 y phi >= 1')
    if alpha is not None and (not math.isfinite(alpha) or alpha <= 0):
        raise ValueError('alpha debe ser positivo, finito y no incluir mu')
    alpha_base = Q / (B * h_m ** (5/3)) if alpha is None else alpha
    alpha_c = alpha_base / mu
    hs = (
        alpha_c * (h ** (5 / 3))
        / (0.68 * beta * phi * (dm_mm ** 0.28))
    ) ** (1 / (1 + x))
    ds = max(hs - h, 0.0)
    return ComponenteSocavacion(
        metodo="Lischtvan-Levediev MTC HHD (general + contracción)",
        valor=ds,
        formula=(
            "Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); "
            "alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)"
        ),
        intermedios={
            "Q": Q, "h_m": h_m, "B": B, "Dm_mm": dm_mm,
            "beta": beta, "mu": mu, "phi": phi, "x": x,
            "alpha_c": alpha_c, "Hs": hs, "ds": ds,
            "h": h, "alpha": alpha_base, "descenso_sin_truncar": hs-h,
        },
        notas=(
            "MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; "
            "no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio."
        ),
        referencias=['LL59'],
        unidades={'Q':'m3/s', 'h_m':'m', 'h':'m', 'B':'m', 'Dm_mm':'mm',
                  'beta':'1', 'mu':'1', 'phi':'1', 'x':'1 (z granular)',
                  'alpha':'m^(1/3)/s (cierre SI)', 'alpha_c':'m^(1/3)/s (cierre SI)',
                  'Hs':'m', 'ds':'m', 'descenso_sin_truncar':'m'},
        supuestos=(['Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.'] if alpha is None else [])
                  + (['h local = hm; simplificación rectangular.'] if h_local is None else []),
    )
