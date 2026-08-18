"""Asistente interactivo de ingreso de datos en terminal."""

from __future__ import annotations

from pathlib import Path

import typer

from socavacion.domain.enums import FormaEstribo, LadoEstribo, TipoCauce, TipoCimentacion
from socavacion.domain.models import (
    ClasificacionCauce,
    CondicionHidraulica,
    DatosGeotecnia,
    Estribo,
    Proyecto,
)
from socavacion.input.loader import guardar_proyecto


def _leer_float(prompt: str, default: float | None = None) -> float:
    while True:
        raw = typer.prompt(prompt, default=str(default) if default is not None else None)
        try:
            return float(raw)
        except ValueError:
            typer.echo("Valor numérico inválido, intente de nuevo.")


def _leer_hidraulica(etiqueta: str) -> CondicionHidraulica:
    typer.echo(f"\n--- Hidráulica {etiqueta} ---")
    return CondicionHidraulica(
        y1=_leer_float("Tirante y1 (m)"),
        V1=_leer_float("Velocidad V1 (m/s)"),
        W1=_leer_float("Ancho W1 (m)"),
        W2=_leer_float("Luz W2 (m)"),
        Q1=_leer_float("Caudal Q1 (m³/s)"),
        Q2=_leer_float("Caudal Q2 (m³/s)"),
        y0=_leer_float("Tirante y0 contraída (m)"),
        Sf=_leer_float("Pendiente Sf (m/m)", default=0.002),
    )


def _leer_forma_estribo() -> FormaEstribo:
    opciones = "/".join(f.value for f in FormaEstribo)
    raw = typer.prompt(f"Forma ({opciones})", default=FormaEstribo.MURO_VERTICAL.value)
    try:
        return FormaEstribo(raw)
    except ValueError:
        typer.echo("Forma no reconocida; se usa muro_vertical.")
        return FormaEstribo.MURO_VERTICAL


def _leer_estribo(lado: LadoEstribo) -> Estribo:
    typer.echo(f"\n=== Estribo {lado.value} ===")
    return Estribo(
        lado=lado,
        D50_mm=_leer_float("D50 (mm)"),
        Z_lecho=_leer_float("Cota lecho Z (m s.n.m.)"),
        q100=_leer_hidraulica("Q100"),
        q500=_leer_hidraulica("Q500"),
        L_prima=_leer_float("Longitud embalse L' (m)"),
        Ae=_leer_float("Área obstruida Ae (m²)"),
        forma=_leer_forma_estribo(),
        angulo_ataque=_leer_float("Ángulo ataque (°)", default=90.0),
    )


def ejecutar_wizard(salida: Path | None = None) -> Proyecto:
    typer.echo("Ingreso de datos — Manual MTC 2018\n")
    nombre = typer.prompt("Nombre del proyecto")
    Q100 = _leer_float("Q100 (m³/s)")
    Q500 = _leer_float("Q500 (m³/s)")
    q_ot_raw = typer.prompt("Q desbordamiento (Enter para omitir)", default="")
    Q_ot = float(q_ot_raw) if q_ot_raw.strip() else None

    tipo_raw = typer.prompt("Tipo cauce (estable/degradacion/agradacion)", default="estable")
    y_lp = _leer_float("y_sg largo plazo (m)", default=0.0)
    cauce = ClasificacionCauce(tipo=TipoCauce(tipo_raw), y_sg_lp=y_lp)

    est_izq = _leer_estribo(LadoEstribo.IZQUIERDO)
    est_der = _leer_estribo(LadoEstribo.DERECHO)

    typer.echo("\n--- Geotecnia ---")
    geo = DatosGeotecnia(
        cota_sondaje_min=_leer_float("Cota fondo sondaje (m s.n.m.)"),
        hay_estrato_competente=typer.confirm("¿Hay estrato competente?", default=True),
        roca_resistente=typer.confirm("¿Roca resistente?", default=False),
        tipo_cimentacion=TipoCimentacion(
            typer.prompt(
                "Tipo cimentación (superficial/profunda/zapata_sobre_pilotes/sobre_roca)",
                default="superficial",
            )
        ),
    )

    proyecto = Proyecto(
        nombre=nombre,
        Q100=Q100,
        Q500=Q500,
        Q_ot=Q_ot,
        estribo_izquierdo=est_izq,
        estribo_derecho=est_der,
        pilares=[],
        cauce=cauce,
        geotecnia=geo,
    )
    if salida is not None:
        guardar_proyecto(proyecto, salida)
        typer.echo(f"\nProyecto guardado en {salida}")
    return proyecto
