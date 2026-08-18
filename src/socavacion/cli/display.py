"""Visualización de resultados en terminal con Rich."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from socavacion.domain.enums import CondicionCaudal, LadoEstribo
from socavacion.domain.results import ResultadoCompleto

console = Console()


def _tabla_resumen(resultado: ResultadoCompleto) -> None:
    t = Table(title="Resumen ejecutivo — Socavación de diseño")
    t.add_column("Estribo")
    t.add_column("y_s Q100 (m)", justify="right")
    t.add_column("y_s Q500 (m)", justify="right")
    t.add_column("y_s diseño (m)", justify="right", style="bold")
    t.add_column("Z lecho soc (m)", justify="right")
    t.add_column("Z cim min (m)", justify="right")

    for e in resultado.estribos_finales:
        label = "Izquierdo" if e.lado == LadoEstribo.IZQUIERDO else "Derecho"
        z_cim = f"{e.Z_cim_min:.3f}" if e.Z_cim_min is not None else "—"
        t.add_row(
            label,
            f"{e.y_s_100:.3f}",
            f"{e.y_s_500:.3f}",
            f"{e.y_s_diseno:.3f}",
            f"{e.Z_lecho_soc:.3f}",
            z_cim,
        )
    console.print(t)


def _tabla_desglose(resultado: ResultadoCompleto) -> None:
    for cond_label, cond in [("Q100 (diseño)", CondicionCaudal.DISENO), ("Q500 (verif.)", CondicionCaudal.VERIFICACION)]:
        caudal = next(c for c in resultado.caudales if c.condicion == cond)
        t = Table(title=f"Desglose — {cond_label}  Q = {caudal.Q:.1f} m³/s")
        t.add_column("Estribo")
        t.add_column("Régimen")
        t.add_column("y_sg (m)", justify="right")
        t.add_column("y_sc (m)", justify="right")
        t.add_column("y_sl (m)", justify="right")
        t.add_column("y_s (m)", justify="right", style="bold")
        t.add_column("Método general")

        for r in caudal.estribos:
            label = "E-I" if r.lado == LadoEstribo.IZQUIERDO else "E-D"
            t.add_row(
                label,
                r.regimen.regimen.value,
                f"{r.general.y_sg_total:.3f}",
                f"{r.y_sc.valor:.3f}",
                f"{r.y_sl.valor:.3f}",
                f"{r.y_s_total:.3f}",
                r.general.metodo_gobernante,
            )
        console.print(t)


def _tabla_geotecnia(resultado: ResultadoCompleto) -> None:
    t = Table(title="Compatibilidad geotecnia (10.11)")
    t.add_column("Ítem")
    t.add_column("Hidráulica")
    t.add_column("Geotecnia")
    t.add_column("¿OK?")
    for item in resultado.geotecnia.items:
        ok = "[green]Sí[/]" if item.compatible else "[red]No[/]"
        t.add_row(item.item, item.hidraulica, item.geotecnia, ok)
    console.print(t)
    console.print(f"\nConclusión: {resultado.geotecnia.conclusion}")


def mostrar_resultados(resultado: ResultadoCompleto) -> None:
    console.print(f"\n[bold]Proyecto:[/] {resultado.proyecto_nombre}")
    console.print(
        f"Q diseño soc = {resultado.Q_diseno:.1f} m³/s  |  "
        f"Q verif soc = {resultado.Q_verif:.1f} m³/s\n"
    )
    _tabla_resumen(resultado)
    console.print()
    _tabla_desglose(resultado)
    console.print()
    _tabla_geotecnia(resultado)

    todas_adv: list[str] = list(resultado.advertencias_globales)
    for c in resultado.caudales:
        for e in c.estribos:
            todas_adv.extend(e.advertencias)
    if todas_adv:
        console.print("\n[yellow]Advertencias:[/]")
        for a in set(todas_adv):
            console.print(f"  • {a}")
