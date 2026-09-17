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

_USE_DEFAULTS = False


def set_use_defaults(enabled: bool = True) -> None:
    """Activa/desactiva el modo demo: los prompts devuelven su valor por defecto."""
    global _USE_DEFAULTS
    _USE_DEFAULTS = enabled


def get_use_defaults() -> bool:
    """Indica si el modo demo está activo."""
    return _USE_DEFAULTS


def _leer_float(prompt: str, default: float | None = None) -> float:
    if _USE_DEFAULTS and default is not None:
        return default
    while True:
        raw = typer.prompt(prompt, default=str(default) if default is not None else None)
        try:
            return float(raw)
        except ValueError:
            typer.echo("Valor numérico inválido, intente de nuevo.")


def _leer_hidraulica(etiqueta: str) -> CondicionHidraulica:
    typer.echo(f"\n--- Hidráulica {etiqueta} ---")
    if etiqueta == "Q100":
        defaults = dict(y1=3.20, V1=2.10, W1=45.0, W2=38.0, y0=3.00)
    elif etiqueta == "Q500":
        defaults = dict(y1=4.10, V1=2.80, W1=48.0, W2=38.0, y0=3.50)
    else:
        defaults = dict(y1=3.20, V1=2.10, W1=45.0, W2=38.0, y0=3.00)
    return CondicionHidraulica(
        y1=_leer_float("Tirante y1 (m)", default=defaults["y1"]),
        V1=_leer_float("Velocidad V1 (m/s)", default=defaults["V1"]),
        W1=_leer_float("Ancho W1 (m)", default=defaults["W1"]),
        W2=_leer_float("Luz W2 (m)", default=defaults["W2"]),
        y0=_leer_float("Tirante y0 contraída (m)", default=defaults["y0"]),
        Sf=_leer_float("Pendiente Sf (m/m)", default=0.002),
    )


def _leer_forma_estribo() -> FormaEstribo:
    if _USE_DEFAULTS:
        return FormaEstribo.MURO_VERTICAL
    opciones = "/".join(f.value for f in FormaEstribo)
    raw = typer.prompt(f"Forma ({opciones})", default=FormaEstribo.MURO_VERTICAL.value)
    try:
        return FormaEstribo(raw)
    except ValueError:
        typer.echo("Forma no reconocida; se usa muro_vertical.")
        return FormaEstribo.MURO_VERTICAL


def _leer_estribo(lado: LadoEstribo) -> Estribo:
    typer.echo(f"\n=== Estribo {lado.value} ===")
    default_d50 = 2.5 if lado == LadoEstribo.IZQUIERDO else 3.0
    default_z = 2450.30 if lado == LadoEstribo.IZQUIERDO else 2450.10
    default_l_prima = 12.0 if lado == LadoEstribo.IZQUIERDO else 10.0
    default_ae = 85.0 if lado == LadoEstribo.IZQUIERDO else 72.0
    return Estribo(
        lado=lado,
        D50_mm=_leer_float("D50 (mm)", default=default_d50),
        Z_lecho=_leer_float("Cota lecho Z (m s.n.m.)", default=default_z),
        q100=_leer_hidraulica("Q100"),
        q500=_leer_hidraulica("Q500"),
        L_prima=_leer_float("Longitud embalse L' (m)", default=default_l_prima),
        Ae=_leer_float("Área obstruida Ae (m²)", default=default_ae),
        forma=_leer_forma_estribo(),
        angulo_ataque=_leer_float("Ángulo ataque (°)", default=90.0),
    )


def ejecutar_wizard(salida: Path | None = None, use_defaults: bool = False) -> Proyecto:
    global _USE_DEFAULTS
    _USE_DEFAULTS = use_defaults

    typer.echo("Ingreso de datos — Manual MTC 2018\n")
    if _USE_DEFAULTS:
        typer.echo("Modo demo: se usan valores por defecto.\n")

    nombre = "Demo" if _USE_DEFAULTS else typer.prompt("Nombre del proyecto")
    Q100 = _leer_float("Q100 (m³/s)", default=850.0)
    Q500 = _leer_float("Q500 (m³/s)", default=1200.0)
    q_ot_raw = "" if _USE_DEFAULTS else typer.prompt("Q desbordamiento (Enter para omitir)", default="")
    Q_ot = float(q_ot_raw) if q_ot_raw.strip() else None

    tipo_raw = "estable" if _USE_DEFAULTS else typer.prompt("Tipo cauce (estable/degradacion/agradacion)", default="estable")
    y_lp = _leer_float("y_sg largo plazo (m)", default=0.0)
    cauce = ClasificacionCauce(tipo=TipoCauce(tipo_raw), y_sg_lp=y_lp)

    est_izq = _leer_estribo(LadoEstribo.IZQUIERDO)
    est_der = _leer_estribo(LadoEstribo.DERECHO)

    typer.echo("\n--- Geotecnia ---")
    geo = DatosGeotecnia(
        cota_sondaje_min=_leer_float("Cota fondo sondaje (m s.n.m.)", default=2445.0),
        hay_estrato_competente=(True if _USE_DEFAULTS else typer.confirm("¿Hay estrato competente?", default=True)),
        roca_resistente=(False if _USE_DEFAULTS else typer.confirm("¿Roca resistente?", default=False)),
        tipo_cimentacion=TipoCimentacion(
            "superficial" if _USE_DEFAULTS else typer.prompt(
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

    # Q1/Q2 de cada condición hidráulica se toman de Q100/Q500 del proyecto
    # cuando no se ingresan explícitamente (evita datos repetidos).
    for est in proyecto.estribos():
        est.q100.resolver_q(proyecto.Q100)
        est.q500.resolver_q(proyecto.Q500)

    if salida is not None:
        guardar_proyecto(proyecto, salida)
        typer.echo(f"\nProyecto guardado en {salida}")
    return proyecto
