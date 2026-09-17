"""CLI principal — Typer."""

from __future__ import annotations

import shutil
from pathlib import Path

import typer

from socavacion.core.pipeline import ejecutar
from socavacion.input.loader import cargar_proyecto
from socavacion.input.validator import validar_proyecto
from socavacion.input.wizard import ejecutar_wizard
from socavacion.cli.display import mostrar_resultados
from socavacion.report.builder import generar_informe
from socavacion.report.docx_builder import (
    generate_socavacion_docx,
    generate_socavacion_docx_with_dialog,
)

app = typer.Typer(
    name="socavacion",
    help="Cálculo de socavación — Manual MTC 2018 / HEC-18",
    no_args_is_help=False,
)

_TEMPLATE = Path(__file__).resolve().parents[3] / "templates" / "proyecto.template.yaml"


@app.command("init")
def init_cmd(
    output: Path = typer.Option(
        Path("proyecto.yaml"),
        "--output",
        "-o",
        help="Archivo YAML de salida",
    ),
) -> None:
    """Genera plantilla de proyecto YAML."""
    if not _TEMPLATE.exists():
        typer.echo(f"Plantilla no encontrada: {_TEMPLATE}", err=True)
        raise typer.Exit(1)
    if output.exists():
        if not typer.confirm(f"¿Sobrescribir {output}?"):
            raise typer.Exit(0)
    shutil.copy(_TEMPLATE, output)
    typer.echo(f"Plantilla creada: {output}")


@app.command("validate")
def validate_cmd(
    archivo: Path = typer.Argument(..., help="Archivo YAML del proyecto"),
) -> None:
    """Valida proyecto sin calcular."""
    proyecto = cargar_proyecto(archivo)
    adv = validar_proyecto(proyecto)
    typer.echo(f"Proyecto '{proyecto.nombre}' válido.")
    if adv:
        typer.echo("\nAdvertencias:")
        for a in adv:
            typer.echo(f"  • {a}")


def _calcular_y_mostrar(
    proyecto,
    export: Path | None,
    quiet: bool,
    word: Path | None = None,
) -> None:
    adv = validar_proyecto(proyecto)
    resultado = ejecutar(proyecto)
    resultado.advertencias_globales.extend(adv)
    if not quiet:
        mostrar_resultados(resultado)
    ruta_informe = export or Path("informes") / f"{proyecto.nombre.replace(' ', '_')}_socavacion.md"
    generar_informe(resultado, proyecto, ruta_informe)
    if not quiet:
        typer.echo(f"\nInforme generado: {ruta_informe}")

    if word is not None:
        generate_socavacion_docx(resultado, proyecto, word)
        if not quiet:
            typer.echo(f"Memoria Word: {word}")
    elif not quiet:
        typer.echo("\nAbriendo diálogo para guardar memoria Word...")
        try:
            generate_socavacion_docx_with_dialog(resultado, proyecto)
        except Exception as exc:
            typer.echo(f"No se pudo generar la memoria Word: {exc}", err=True)


def _ingresar_y_calcular(
    export: Path | None = None,
    use_defaults: bool = False,
    word: Path | None = None,
) -> None:
    proyecto = ejecutar_wizard(salida=None, use_defaults=use_defaults)
    _calcular_y_mostrar(proyecto, export=export, quiet=False, word=word)


@app.callback(invoke_without_command=True)
def principal(
    ctx: typer.Context,
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Si no hay subcomando, inicia el ingreso en terminal."""
    if ctx.invoked_subcommand is None:
        _ingresar_y_calcular(use_defaults=demo, word=word)


@app.command("ingresar")
def ingresar_cmd(
    export: Path | None = typer.Option(None, "--export", "-e", help="Ruta informe Markdown"),
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Ingresa datos en terminal, calcula y muestra resultados (sin YAML)."""
    _ingresar_y_calcular(export=export, use_defaults=demo, word=word)


@app.command("calc")
def calc_cmd(
    archivo: Path | None = typer.Argument(
        None,
        help="Archivo YAML. Si se omite, pide los datos en terminal.",
    ),
    export: Path | None = typer.Option(None, "--export", "-e", help="Ruta informe Markdown"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Sin salida en terminal"),
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Calcula socavación: YAML o ingreso interactivo si no hay archivo."""
    if archivo is None:
        proyecto = ejecutar_wizard(salida=None, use_defaults=demo)
    else:
        proyecto = cargar_proyecto(archivo)
    _calcular_y_mostrar(proyecto, export=export, quiet=quiet, word=word)


@app.command("wizard")
def wizard_cmd(
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Opcional: guardar también un YAML",
    ),
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Ingreso en terminal y cálculo inmediato."""
    proyecto = ejecutar_wizard(salida=output, use_defaults=demo)
    _calcular_y_mostrar(proyecto, export=None, quiet=False, word=word)


@app.command("word")
def word_cmd(
    archivo: Path = typer.Argument(..., help="Archivo YAML del proyecto"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Ruta memoria Word (.docx)"),
) -> None:
    """Genera memoria Word desde un YAML sin mostrar resultados en terminal."""
    proyecto = cargar_proyecto(archivo)
    adv = validar_proyecto(proyecto)
    resultado = ejecutar(proyecto)
    resultado.advertencias_globales.extend(adv)
    if output is None:
        generate_socavacion_docx_with_dialog(resultado, proyecto)
    else:
        generate_socavacion_docx(resultado, proyecto, output)
        typer.echo(f"Memoria Word generada: {output}")


if __name__ == "__main__":
    app()
