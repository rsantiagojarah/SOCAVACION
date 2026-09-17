"""Matriz de compatibilidad geológico-geotécnica (10.11)."""

from __future__ import annotations

from socavacion.core.elevations import longitud_efectiva_pilotes, verificar_zapata_pilotes
from socavacion.domain.enums import TipoCimentacion
from socavacion.domain.models import Proyecto
from socavacion.domain.results import (
    ItemCompatibilidad,
    ResultadoEstriboFinal,
    ResultadoGeotecnia,
)


def evaluar_compatibilidad(
    proyecto: Proyecto,
    estribos: list[ResultadoEstriboFinal],
    caudales=None,
    pilares=None,
) -> ResultadoGeotecnia:
    geo = proyecto.geotecnia
    if not geo.evaluar or geo.cota_sondaje_min is None:
        return ResultadoGeotecnia(
            items=[ItemCompatibilidad('Evaluación geotécnica', 'No realizada',
                   'Se requieren datos de cimentación y exploración', False)],
            compatible_global=False,
            conclusion='Geotecnia NO EVALUADA: este resultado sólo estima socavación; no determina una cimentación apta.',
        )
    items: list[ItemCompatibilidad] = []

    cotas = [e.Z_lecho_soc for e in estribos] + [p.Z_lecho_soc for p in pilares or [] if p.Z_lecho_soc is not None]
    z_soc_min = min(cotas)
    z_cim_min = min(
        (e.Z_cim_min for e in estribos if e.Z_cim_min is not None),
        default=z_soc_min - 1.0,
    )

    if pilares:
        z_cim_min = min([z_cim_min] + [p.Z_cim_limite for p in pilares if p.Z_cim_limite is not None])
        items.append(ItemCompatibilidad('Cotas de pilares', 'Lecho y total por pilar',
                                       'Cotas disponibles', all(p.Z_lecho_soc is not None for p in pilares)))
    # 1. Sondaje bajo cota socavada
    sondaje_ok = geo.cota_sondaje_min <= z_soc_min
    items.append(
        ItemCompatibilidad(
            item="Cota lecho socavado",
            hidraulica=f"Z_soc min = {z_soc_min:.2f} m",
            geotecnia=f"Sondaje fondo = {geo.cota_sondaje_min:.2f} m",
            compatible=sondaje_ok,
            accion="" if sondaje_ok else "Profundizar sondajes bajo Z_lecho_soc",
        )
    )

    # 2. Material bajo prisma
    mat_ok = geo.hay_estrato_competente
    items.append(
        ItemCompatibilidad(
            item="Material residual bajo prisma",
            hidraulica=f"D50 hidráulico en cauce",
            geotecnia=geo.descripcion_estrato or "Estrato competente declarado",
            compatible=mat_ok,
            accion="" if mat_ok else "Verificar estrato de apoyo bajo Z_lecho_soc",
        )
    )

    # 4. Reserva 1.00 m
    if geo.tipo_cimentacion == TipoCimentacion.SUPERFICIAL:
        reserva_ok = geo.cota_sondaje_min <= z_cim_min
        items.append(
            ItemCompatibilidad(
                item="Sondaje alcanza límite zapata (Art. 1.2.4)",
                hidraulica=f"Z_cim_min = {z_cim_min:.2f} m",
                geotecnia=f"Fondo sondaje {geo.cota_sondaje_min:.2f} m; no prueba competencia",
                compatible=reserva_ok,
                accion="" if reserva_ok else "Profundizar exploración; definir cota real de zapata",
            )
        )

    # 5. Zapata sobre pilotes
    if geo.tipo_cimentacion == TipoCimentacion.ZAPATA_SOBRE_PILOTES:
        z_enc = geo.Z_encepado_zapata
        lechos = []
        if caudales:
            for c in caudales:
                for est, r in zip(proyecto.estribos(), c.estribos):
                    lechos.append(est.Z_lecho-r.general.y_sg_total)
                for pil, r in zip(proyecto.pilares, c.pilares):
                    if pil.Z_lecho is not None:
                        lechos.append(pil.Z_lecho-r.general.y_sg_total)
        z_contraido = min(lechos) if lechos else min(e.Z_lecho_actual-max(e.componentes_100.general.y_sg_total,e.componentes_500.general.y_sg_total) for e in estribos)
        zap_ok = z_enc is not None and verificar_zapata_pilotes(z_enc, z_contraido)
        items.append(
            ItemCompatibilidad(
                item="Zapata sobre pilotes",
                hidraulica=f"Lecho contraído ≈ {z_contraido:.2f} m",
                geotecnia=f"Encepado = {z_enc:.2f} m" if z_enc is not None else "Sin dato",
                compatible=zap_ok,
                accion="" if zap_ok else "Bajar encepado bajo lecho contraído",
            )
        )

    # 6. Roca
    if geo.roca_resistente:
        items.append(
            ItemCompatibilidad(
                item="Roca resistente a socavación",
                hidraulica="Cimentación sobre roca",
                geotecnia="Roca resistente declarada por usuario; requiere sustento",
                compatible=True,
            )
        )
    else:
        items.append(
            ItemCompatibilidad(
                item="Roca / erosionabilidad",
                hidraulica="Material erosionable asumido",
                geotecnia="No roca resistente declarada",
                compatible=not geo.roca_resistente,
            )
        )

    # 7. Pilotes — longitud efectiva
    if geo.tipo_cimentacion in (TipoCimentacion.PROFUNDA, TipoCimentacion.ZAPATA_SOBRE_PILOTES) and geo.Z_punta_pilotes is None:
        items.append(ItemCompatibilidad('Longitud efectiva pilotes', 'Requiere punta', 'Sin dato', False))
    if geo.tipo_cimentacion in (TipoCimentacion.PROFUNDA, TipoCimentacion.ZAPATA_SOBRE_PILOTES) and geo.Z_punta_pilotes is not None:
        L_eff = longitud_efectiva_pilotes(z_soc_min, geo.Z_punta_pilotes)
        pil_ok = L_eff > 0
        items.append(
            ItemCompatibilidad(
                item="Longitud efectiva pilotes",
                hidraulica=f"L_eff = {L_eff:.2f} m desde Z_soc",
                geotecnia=f"Punta a {geo.Z_punta_pilotes:.2f} m",
                compatible=pil_ok,
                accion="" if pil_ok else "Aumentar longitud de pilotes",
            )
        )

    compatible_global = all(i.compatible for i in items)
    if compatible_global:
        conclusion = "Controles geométricos preliminares satisfechos; falta verificar capacidad portante y estabilidad con el prisma retirado."
    else:
        incompatibles = [i.item for i in items if not i.compatible]
        conclusion = f"Incompatibilidades detectadas: {', '.join(incompatibles)}."

    return ResultadoGeotecnia(
        items=items,
        compatible_global=compatible_global,
        conclusion=conclusion,
    )
