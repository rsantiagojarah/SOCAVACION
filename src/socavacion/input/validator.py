"""Validaciones adicionales MTC."""

from __future__ import annotations

from socavacion.domain.models import Proyecto
from socavacion.normative.constants import TOLERANCIA_ANCHO_CONTRACCION


def validar_proyecto(proyecto: Proyecto) -> list[str]:
    """Retorna lista de advertencias (vacía si todo OK)."""
    advertencias: list[str] = []

    if proyecto.Q500 < proyecto.Q100:
        advertencias.append("Q500 < Q100: verificar periodos de retorno")

    for est in proyecto.estribos():
        for etiqueta, hid in [("Q100", est.q100), ("Q500", est.q500)]:
            if abs(hid.W2 - hid.W1) / hid.W1 < TOLERANCIA_ANCHO_CONTRACCION:
                advertencias.append(
                    f"Estribo {est.lado.value} {etiqueta}: W2≈W1, contracción nula"
                )

    if proyecto.cauce.tipo.value == "agradacion" and proyecto.cauce.y_sg_lp < 0:
        advertencias.append("Agradación: y_sg_lp negativo no reduce diseño")

    if proyecto.geotecnia.tipo_cimentacion.value == "zapata_sobre_pilotes":
        if proyecto.geotecnia.Z_encepado_zapata is None:
            advertencias.append("Zapata sobre pilotes: falta Z_encepado_zapata")

    if proyecto.geotecnia.tipo_cimentacion.value == "profunda":
        if proyecto.geotecnia.Z_punta_pilotes is None:
            advertencias.append("Cimentación profunda: falta Z_punta_pilotes")

    return advertencias
