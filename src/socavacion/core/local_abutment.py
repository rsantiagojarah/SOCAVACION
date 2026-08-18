"""Socavación local en estribos — Froehlich, HIRE, límites HEC-18."""

from __future__ import annotations

import math

from socavacion.domain.enums import FormaEstribo, RegimenLecho
from socavacion.domain.models import CondicionHidraulica, Estribo
from socavacion.domain.results import ComponenteSocavacion, RegimenResult
from socavacion.normative.constants import G, LIMITE_FROEHLICH
from socavacion.normative.tables import K1_ESTRIBO


def k2_angulo(theta_grados: float) -> float:
    """K2 = (θ/90)^0.13"""
    return (theta_grados / 90.0) ** 0.13


def _froehlich(ya: float, L_prima: float, Fr_a: float, K1: float, K2: float) -> float:
    ratio = L_prima / ya
    return ya * (2.27 * K1 * K2 * (ratio ** 0.43) * (Fr_a ** 0.61) + 1.0)


def _hire(y1: float, Fr: float, K1: float, K2: float) -> float:
    return y1 * 4.0 * (Fr ** (1 / 3)) * (K1 / 0.55) * K2


def _limite_hec18(ya: float, K1: float, K2: float, regimen: RegimenLecho) -> float:
    factor = 2.4 if regimen == RegimenLecho.LECHO_VIVO else 2.2
    return factor * K1 * (K2 / 0.55) * ya


def calcular_local_estribo(
    estribo: Estribo,
    hid: CondicionHidraulica,
    regimen: RegimenResult,
) -> tuple[ComponenteSocavacion, list[str]]:
    advertencias: list[str] = []
    K1 = K1_ESTRIBO[estribo.forma]
    K2 = k2_angulo(estribo.angulo_ataque)
    ya = hid.y1
    ya_obstruida = estribo.Ae / max(estribo.L_prima, 1e-6)
    ya_eff = max(ya_obstruida, ya)
    Ve = hid.Q1 / max(estribo.Ae, 1e-6) if estribo.Ae > 0 else hid.V1
    Fr_a = Ve / math.sqrt(G * ya_eff) if ya_eff > 0 else 0.0

    ratio_ly = estribo.L_prima / ya_eff if ya_eff > 0 else 0.0
    if ratio_ly <= LIMITE_FROEHLICH:
        y_sl = _froehlich(ya_eff, estribo.L_prima, Fr_a, K1, K2)
        metodo = "Froehlich HEC-18"
        formula = "ysl/ya = 2.27*K1*K2*(L'/ya)^0.43*Fr_a^0.61 + 1"
    else:
        y_sl = _hire(hid.y1, regimen.Fr, K1, K2)
        metodo = "HIRE HEC-18"
        formula = "ysl/y1 = 4*Fr^(1/3)*K1/0.55*K2"

    limite = _limite_hec18(ya_eff, K1, K2, regimen.regimen)
    if y_sl > limite:
        advertencias.append(f"Límite HEC-18 aplicado ({limite:.3f} m)")
        y_sl = limite

    return (
        ComponenteSocavacion(
            metodo=metodo,
            valor=y_sl,
            formula=formula,
            intermedios={
                "K1": K1,
                "K2": K2,
                "Fr_a": Fr_a,
                "L_prima": estribo.L_prima,
                "ya": ya_eff,
                "limite": limite,
            },
        ),
        advertencias,
    )
