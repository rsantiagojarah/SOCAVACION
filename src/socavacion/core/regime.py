"""Detección de régimen del lecho: Vc, Fr, V*/ω, k1 contracción."""

from __future__ import annotations

import math

from socavacion.domain.enums import RegimenLecho
from socavacion.domain.results import RegimenResult
from socavacion.normative.constants import G, KU_VC, NU_AGUA
from socavacion.normative.tables import K1_CONTRACCION_BOUNDS


def velocidad_critica(y: float, d50_m: float) -> float:
    """Vc = Ku * y^(1/6) * D50^(1/3) — HEC-18."""
    return KU_VC * (y ** (1 / 6)) * (d50_m ** (1 / 3))


def numero_froude(V: float, y: float) -> float:
    return V / math.sqrt(G * y)


def velocidad_corte(y: float, sf: float) -> float:
    """V* = sqrt(g * y * Sf)."""
    return math.sqrt(G * y * sf)


def velocidad_caida(d50_m: float) -> float:
    """ω aproximado (Rubey simplificado para arenas/gravas)."""
    if d50_m <= 0:
        return 0.0
    # Fórmula Rubey simplificada HEC-18 para partículas > 0.1 mm
    d_cm = d50_m * 100
    if d50_m < 0.0001:
        return (G / (18 * NU_AGUA)) * (d50_m ** 2)
    return 0.045 * (d_cm ** 0.5) * (1 - math.exp(-12.5 * d50_m))


def k1_contraccion(v_star: float, omega: float) -> float:
    """Exponente k1 Laursen según V*/ω."""
    if omega <= 0:
        return 0.69
    ratio = v_star / omega
    if ratio < 0.50:
        return 0.59
    if ratio > 2.0:
        return 0.69
    # Interpolar 0.59 → 0.69 entre 0.50 y 2.0
    t = (ratio - 0.50) / (2.0 - 0.50)
    return 0.59 + t * (0.69 - 0.59)


def detectar_regimen(
    V1: float, y1: float, d50_m: float, sf: float | None, *, calcular_legacy: bool = True
) -> RegimenResult:
    """Clasifica lecho vivo vs agua clara."""
    Vc = velocidad_critica(y1, d50_m)
    regimen = RegimenLecho.LECHO_VIVO if V1 > Vc else RegimenLecho.AGUA_CLARA
    Fr = numero_froude(V1, y1)
    v_star = velocidad_corte(y1, sf) if sf is not None else None
    # El motor LL trazable no utiliza estas aproximaciones históricas de Laursen.
    omega = velocidad_caida(d50_m) if calcular_legacy else None
    k1 = k1_contraccion(v_star, omega) if calcular_legacy and v_star is not None else None
    return RegimenResult(
        regimen=regimen,
        Vc=Vc,
        V1=V1,
        Fr=Fr,
        V_star=v_star,
        omega=omega,
        k1_contraccion=k1,
    )
