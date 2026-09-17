"""Cotas de lecho socavado y cimentación (10.9–10.10)."""

from __future__ import annotations

from socavacion.domain.enums import TipoCimentacion
from socavacion.domain.models import DatosGeotecnia
from socavacion.normative.constants import RESERVA_CIMENTACION_M


def calcular_cotas_estribo(
    z_lecho: float,
    y_s: float,
    reserva_m: float = RESERVA_CIMENTACION_M,
    reserva_superficial: bool = True,
) -> dict[str, float | None]:
    z_soc = z_lecho - y_s
    z_cim = z_soc - reserva_m if reserva_superficial else None
    return {"Z_lecho_soc": z_soc, "Z_cim_min": z_cim}


def longitud_efectiva_pilotes(z_lecho_soc: float, z_punta: float) -> float:
    """L_efectiva = Z_lecho_soc - Z_punta (positiva hacia abajo en profundidad)."""
    return z_lecho_soc - z_punta


def verificar_zapata_pilotes(z_encepado: float, z_lecho_contraido: float) -> bool:
    """Cara superior zapata debe quedar bajo lecho contraído (Art. 1.2.4)."""
    return z_encepado < z_lecho_contraido


def requiere_reserva(geotecnia: DatosGeotecnia) -> bool:
    return geotecnia.evaluar and geotecnia.tipo_cimentacion == TipoCimentacion.SUPERFICIAL
