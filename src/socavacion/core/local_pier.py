"""Socavación local en pilares — CSU HEC-18."""

from __future__ import annotations

import math

from socavacion.domain.enums import RegimenLecho
from socavacion.domain.models import CondicionHidraulica, Pilar
from socavacion.domain.results import ComponenteSocavacion, RegimenResult
from socavacion.normative.tables import K1_PILAR


def k2_pilar(theta: float) -> float:
    """K2 ataque para pilares: cos²(θ) para θ en grados."""
    rad = math.radians(theta)
    return math.cos(rad) ** 2


def calcular_local_pilar(
    pilar: Pilar,
    hid: CondicionHidraulica,
    regimen: RegimenResult,
) -> ComponenteSocavacion:
    K1 = K1_PILAR[pilar.forma]
    K2 = k2_pilar(pilar.angulo_ataque)
    K3 = pilar.K3
    K4 = pilar.K4
    y1 = hid.y1
    Fr1 = regimen.Fr
    a = pilar.ancho_a

    y_sp = y1 * 2.0 * K1 * K2 * K3 * K4 * ((a / y1) ** 0.65) * (Fr1 ** 0.43)

    if regimen.regimen == RegimenLecho.LECHO_VIVO:
        limite = 2.4 * a
    else:
        limite = 3.0 * a

    notas = ""
    if y_sp > limite:
        y_sp = limite
        notas = f"Límite HEC-18 aplicado ({limite:.3f} m)"

    return ComponenteSocavacion(
        metodo="CSU HEC-18",
        valor=y_sp,
        formula="ysp/y1 = 2.0*K1*K2*K3*K4*(a/y1)^0.65*Fr1^0.43",
        intermedios={"K1": K1, "K2": K2, "K3": K3, "K4": K4, "Fr1": Fr1, "limite": limite},
        notas=notas,
    )
