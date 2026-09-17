"""Agregación de métodos de socavación general."""

from __future__ import annotations

from socavacion.core.general import lischtvan
from socavacion.domain.results import ComponenteSocavacion, ResultadoGeneral
from socavacion.normative.mu import factor_mu


def calcular_general(
    Q: float,
    hidraulica,
    d50_m: float,
    d50_mm: float,
    y_sg_lp: float,
    q1: float | None = None,
    q2: float | None = None,
) -> ResultadoGeneral:
    r_lischtvan = lischtvan.calcular_mtc_hhd(
        Q=hidraulica.Q_ll if hidraulica.Q_ll is not None else Q,
        h_m=hidraulica.h_m_ll or hidraulica.y1,
        B=hidraulica.B_ll or hidraulica.W1,
        dm_mm=hidraulica.Dm_mm or d50_mm,
        beta=hidraulica.beta,
        mu=factor_mu(hidraulica.luz_libre, hidraulica.V_mu if hidraulica.V_mu is not None else hidraulica.V1) if hidraulica.luz_libre is not None else hidraulica.mu,
        phi=hidraulica.phi,
        x=hidraulica.exponente_x,
        h_local=hidraulica.h_local,
        alpha=hidraulica.alpha,
    )
    r_lischtvan.fuentes_datos = dict(hidraulica.fuentes)
    if hidraulica.luz_libre is not None:
        r_lischtvan.referencias.append('MU13')
        r_lischtvan.intermedios.update(luz_libre=hidraulica.luz_libre, V_mu=hidraulica.V_mu if hidraulica.V_mu is not None else hidraulica.V1)
        r_lischtvan.unidades.update(luz_libre='m', V_mu='m/s')
        if hidraulica.V_mu is None:
            r_lischtvan.supuestos.append('V_mu=V1: se asume velocidad media de sección; validar, especialmente si V1 es local del pilar.')
    if hidraulica.Dm_mm is None:
        r_lischtvan.supuestos.append('Dm=D50 por falta de Dm explícito; no es equivalencia normativa.')
    for campo in ('beta','phi','exponente_x') + (() if hidraulica.luz_libre is not None else ('mu',)):
        if campo not in hidraulica.model_fields_set:
            r_lischtvan.supuestos.append(f'{campo} predeterminado; requiere sustento.')
    r_neill = ComponenteSocavacion('No evaluado (legado Neill)', 0, 'No participa en el cálculo MTC')
    r_lacey = ComponenteSocavacion('No evaluado (legado Lacey)', 0, 'No participa en el cálculo MTC')

    # El método MTC HHD ya incluye la contracción. Neill y Lacey quedan
    # como campos históricos no evaluados, no como una envolvente mezclada.
    gobernante = r_lischtvan
    y_sg_avenida = r_lischtvan.valor
    y_sg_lp_efectivo = max(y_sg_lp, 0.0)  # agradación no reduce diseño
    y_sg_total = y_sg_lp_efectivo + y_sg_avenida

    return ResultadoGeneral(
        y_sg_lp=y_sg_lp_efectivo,
        y_sg_lischtvan=r_lischtvan,
        y_sg_neill=r_neill,
        y_sg_lacey=r_lacey,
        y_sg_avenida=y_sg_avenida,
        y_sg_total=y_sg_total,
        metodo_gobernante=gobernante.metodo,
    )
