"""Socavación por contracción — Laursen HEC-18."""

from __future__ import annotations

from socavacion.domain.enums import RegimenLecho
from socavacion.domain.models import CondicionHidraulica
from socavacion.domain.results import ComponenteSocavacion, RegimenResult
from socavacion.normative.constants import DM_FACTOR, KU_CONTRACCION_CLARA, TOLERANCIA_ANCHO_CONTRACCION


def _contraccion_lecho_vivo(
    hid: CondicionHidraulica, regimen: RegimenResult
) -> ComponenteSocavacion:
    k1 = regimen.k1_contraccion
    ratio_q = hid.Q2 / hid.Q1
    ratio_w = hid.W1 / hid.W2
    y2 = hid.y1 * (ratio_q ** (6 / 7)) * (ratio_w ** k1)
    y_sc = max(y2 - hid.y0, 0.0)
    return ComponenteSocavacion(
        metodo="Laursen lecho vivo",
        valor=y_sc,
        formula="y2/y1 = (Q2/Q1)^(6/7)*(W1/W2)^k1; y_sc = max(y2-y0,0)",
        intermedios={"y2": y2, "k1": k1, "ratio_q": ratio_q, "ratio_w": ratio_w},
    )


def _contraccion_agua_clara(hid: CondicionHidraulica, dm_m: float) -> ComponenteSocavacion:
    numerador = KU_CONTRACCION_CLARA * (hid.Q2 ** 2)
    denominador = (dm_m ** (2 / 3)) * (hid.W2 ** 2)
    y2 = (numerador / denominador) ** (3 / 7)
    y_sc = max(y2 - hid.y0, 0.0)
    return ComponenteSocavacion(
        metodo="Laursen agua clara",
        valor=y_sc,
        formula="y2 = [Ku*Q2²/(Dm^(2/3)*W2²)]^(3/7); y_sc = max(y2-y0,0)",
        intermedios={"y2": y2, "Dm": dm_m},
    )


def calcular_contraccion(
    hid: CondicionHidraulica,
    regimen: RegimenResult,
    d50_m: float,
) -> tuple[ComponenteSocavacion, list[str]]:
    """Calcula y_sc; retorna advertencias."""
    advertencias: list[str] = []
    if abs(hid.W2 - hid.W1) / hid.W1 < TOLERANCIA_ANCHO_CONTRACCION:
        advertencias.append("W2 ≈ W1: contracción nula por geometría")
        return (
            ComponenteSocavacion(
                metodo="Sin contracción",
                valor=0.0,
                formula="W2 ≈ W1",
                notas="Puente no estrecha el cauce",
            ),
            advertencias,
        )

    dm_m = DM_FACTOR * d50_m
    if regimen.regimen == RegimenLecho.LECHO_VIVO:
        return _contraccion_lecho_vivo(hid, regimen), advertencias

    claro = _contraccion_agua_clara(hid, dm_m)
    vivo = _contraccion_lecho_vivo(hid, regimen)
    if claro.valor > vivo.valor:
        advertencias.append("Agua clara excedió lecho vivo: se adopta lecho vivo")
        return vivo, advertencias
    return claro, advertencias
