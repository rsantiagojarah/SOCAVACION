"""Visualización de resultados en terminal con tablas ASCII."""

from __future__ import annotations

from socavacion.cli.ascii_tables import boxed_table, key_value_table
from socavacion.domain.enums import CondicionCaudal, LadoEstribo
from socavacion.domain.results import ResultadoCompleto


def _tabla_resumen(resultado: ResultadoCompleto) -> list[str]:
    rows = []
    for e in resultado.estribos_finales:
        label = "Izquierdo" if e.lado == LadoEstribo.IZQUIERDO else "Derecho"
        z_cim = f"{e.Z_cim_min:.3f}" if e.Z_cim_min is not None else "—"
        rows.append(
            (
                label,
                f"{e.y_s_100:.3f}",
                f"{e.y_s_500:.3f}",
                f"{e.y_s_diseno:.3f}",
                f"{e.Z_lecho_soc:.3f}",
                z_cim,
            )
        )
    return boxed_table(
        ("Estribo", "y_s Q100 (m)", "y_s Q500 (m)", "y_s diseño (m)", "Z lecho soc (m)", "Z cim min (m)"),
        rows,
        aligns=("left", "right", "right", "right", "right", "right"),
        title="Resumen ejecutivo — Socavación de diseño",
    )


def _tabla_desglose(resultado: ResultadoCompleto) -> list[str]:
    lines: list[str] = []
    for cond_label, cond in [
        ("Q100 (diseño)", CondicionCaudal.DISENO),
        ("Q500 (verif.)", CondicionCaudal.VERIFICACION),
    ]:
        caudal = next(c for c in resultado.caudales if c.condicion == cond)
        rows = []
        for r in caudal.estribos:
            label = "E-I" if r.lado == LadoEstribo.IZQUIERDO else "E-D"
            rows.append(
                (
                    label,
                    r.regimen.regimen.value,
                    f"{r.general.y_sg_total:.3f}",
                    f"{r.y_sc.valor:.3f}",
                    f"{r.y_sl.valor:.3f}",
                    f"{r.y_s_total:.3f}",
                    r.general.metodo_gobernante,
                )
            )
        lines.extend(
            boxed_table(
                ("Estribo", "Régimen", "y_sg (m)", "y_sc (m)", "y_sl (m)", "y_s (m)", "Método general"),
                rows,
                aligns=("left", "left", "right", "right", "right", "right", "left"),
                title=f"Desglose — {cond_label}  Q = {caudal.Q:.1f} m³/s",
            )
        )
        lines.append("")
    return lines


def _tabla_geotecnia(resultado: ResultadoCompleto) -> list[str]:
    rows = []
    for item in resultado.geotecnia.items:
        ok = "Sí" if item.compatible else "No"
        rows.append((item.item, item.hidraulica, item.geotecnia, ok))
    lines = boxed_table(
        ("Ítem", "Hidráulica", "Geotecnia", "¿OK?"),
        rows,
        aligns=("left", "left", "left", "center"),
        title="Compatibilidad geotecnia (10.11)",
    )
    lines.append("")
    lines.append(f"Conclusión: {resultado.geotecnia.conclusion}")
    return lines


def mostrar_resultados(resultado: ResultadoCompleto) -> None:
    lines: list[str] = []
    lines.append(f"\nProyecto: {resultado.proyecto_nombre}")
    lines.append(
        f"Q diseño soc = {resultado.Q_diseno:.1f} m³/s  |  "
        f"Q verif soc = {resultado.Q_verif:.1f} m³/s"
    )
    lines.append("")
    lines.extend(_tabla_resumen(resultado))
    lines.append("")
    lines.extend(_tabla_desglose(resultado))
    lines.extend(_tabla_geotecnia(resultado))

    todas_adv: list[str] = list(resultado.advertencias_globales)
    for c in resultado.caudales:
        for e in c.estribos:
            todas_adv.extend(e.advertencias)
    if todas_adv:
        lines.append("")
        lines.append("Advertencias:")
        for a in set(todas_adv):
            lines.append(f"  • {a}")

    print("\n".join(lines))


__all__ = ["mostrar_resultados", "boxed_table", "key_value_table"]
