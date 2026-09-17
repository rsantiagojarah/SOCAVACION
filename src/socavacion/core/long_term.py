"""Degradación / agradación de largo plazo (10.2)."""

from __future__ import annotations

from socavacion.domain.enums import TipoCauce
from socavacion.domain.models import ClasificacionCauce


def calcular_y_sg_lp(cauce: ClasificacionCauce) -> tuple[float, list[str]]:
    """Retorna y_sg_LP efectivo para diseño y advertencias."""
    advertencias: list[str] = []
    y_lp = cauce.y_sg_lp

    if cauce.tipo == TipoCauce.AGRADACION and y_lp < 0:
        advertencias.append(
            "Agradación detectada: no se descuenta del diseño (criterio conservador de implementación)."
        )
        return 0.0, advertencias

    if cauce.tipo == TipoCauce.ESTABLE:
        return max(y_lp, 0.0), advertencias

    if cauce.tipo == TipoCauce.DEGRADACION:
        if y_lp <= 0:
            advertencias.append(
                "Cauce degradante sin y_sg_lp: requiere estudio morfológico; no se asigna un rango sin sustento."
            )
        return max(y_lp, 0.0), advertencias

    return max(y_lp, 0.0), advertencias
