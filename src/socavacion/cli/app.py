"""CLI principal — Typer."""

from __future__ import annotations

import shutil
from functools import wraps
from pathlib import Path

import typer

from socavacion.core.pipeline import ejecutar
from socavacion.input.loader import cargar_proyecto
from socavacion.input.validator import validar_proyecto
from socavacion.input.wizard import ejecutar_wizard
from socavacion.cli.display import mostrar_resultados
from socavacion.domain.observations import resumir_advertencias
from socavacion.report.builder import generar_informe
from socavacion.report.docx_builder import (
    generate_socavacion_docx,
    generate_socavacion_docx_with_dialog,
)

app = typer.Typer(
    name="socavacion",
    help="Socavación local por Froehlich — datos HEC-RAS manuales, sólo estribos",
    no_args_is_help=False,
)

_TEMPLATE = Path(__file__).resolve().parents[3] / "ejemplos" / "froehlich_hec_ras.yaml"


def _errores_entrada(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, OSError) as exc:
            typer.echo(f'No se completó la operación:\n{exc}', err=True)
            raise typer.Exit(2) from None
    return wrapped


@app.command("init")
def init_cmd(
    output: Path = typer.Option(
        Path("proyecto.yaml"),
        "--output",
        "-o",
        help="Archivo YAML de salida",
    ),
) -> None:
    """Genera plantilla Froehlich con datos sintéticos marcados como prueba."""
    if not _TEMPLATE.exists():
        typer.echo(f"Plantilla no encontrada: {_TEMPLATE}", err=True)
        raise typer.Exit(1)
    if output.exists():
        if not typer.confirm(f"¿Sobrescribir {output}?"):
            raise typer.Exit(0)
    shutil.copy(_TEMPLATE, output)
    typer.echo(f"Plantilla creada: {output}")
    typer.echo('Froehlich únicamente. Datos sintéticos de prueba: sustituir y sustentar antes de un proyecto real.')


@app.command("validate")
@_errores_entrada
def validate_cmd(
    archivo: Path = typer.Argument(..., help="Archivo YAML del proyecto"),
) -> None:
    """Valida proyecto sin calcular."""
    proyecto = cargar_proyecto(archivo)
    adv = validar_proyecto(proyecto)
    typer.echo(f"Proyecto '{proyecto.nombre}': estructura de entrada aceptada; modo {proyecto.modo}.")
    if adv:
        typer.echo("\nAdvertencias:")
        typer.echo('\n'.join(resumir_advertencias(adv)))
    else:
        typer.echo('Sin pendientes de entrada detectados; esto no certifica las fuentes ni el diseño.')


def _calcular_y_mostrar(
    proyecto,
    export: Path | None,
    quiet: bool,
    word: Path | None = None,
) -> None:
    resultado = ejecutar(proyecto)
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
    elif not quiet and not proyecto.datos_prueba:
        typer.echo("\nAbriendo diálogo para guardar memoria Word...")
        try:
            generate_socavacion_docx_with_dialog(resultado, proyecto)
        except Exception as exc:
            typer.echo(f"No se pudo generar la memoria Word: {exc}", err=True)


def _ingresar_y_calcular(
    export: Path | None = None,
    use_defaults: bool = False,
    word: Path | None = None,
    ejemplo: bool = False,
    en_blanco: bool = False,
    avanzado: bool = False,
) -> None:
    proyecto = ejecutar_wizard(salida=None, use_defaults=use_defaults, ejemplo=ejemplo, en_blanco=en_blanco, avanzado=avanzado)
    _calcular_y_mostrar(proyecto, export=export, quiet=False, word=word)


@app.callback(invoke_without_command=True)
@_errores_entrada
def principal(
    ctx: typer.Context,
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    ejemplo: bool = typer.Option(False, '--ejemplo', help='Formulario con valores de prueba; Enter acepta cada valor'),
    en_blanco: bool = typer.Option(False, '--en-blanco', help='Ingresar datos reales sin precargar el ejemplo'),
    avanzado: bool = typer.Option(False, '--avanzado', help='Habilitar modo trazable en Froehlich; no agrega LL ni pilares'),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Si no hay subcomando, inicia el ingreso en terminal."""
    if ctx.invoked_subcommand is None:
        _ingresar_y_calcular(use_defaults=demo, word=word, ejemplo=ejemplo, en_blanco=en_blanco, avanzado=avanzado)


@app.command("ingresar")
@_errores_entrada
def ingresar_cmd(
    export: Path | None = typer.Option(None, "--export", "-e", help="Ruta informe Markdown"),
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    ejemplo: bool = typer.Option(False, '--ejemplo', help='Mostrar datos de prueba editables con Enter'),
    en_blanco: bool = typer.Option(False, '--en-blanco', help='Formulario sin datos sintéticos precargados'),
    avanzado: bool = typer.Option(False, '--avanzado', help='Habilitar selección de modo trazable para Froehlich'),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Ingresa datos en terminal, calcula y muestra resultados (sin YAML)."""
    _ingresar_y_calcular(export=export, use_defaults=demo, word=word, ejemplo=ejemplo, en_blanco=en_blanco, avanzado=avanzado)


@app.command("calc")
@_errores_entrada
def calc_cmd(
    archivo: Path | None = typer.Argument(
        None,
        help="Archivo YAML. Si se omite, pide los datos en terminal.",
    ),
    export: Path | None = typer.Option(None, "--export", "-e", help="Ruta informe Markdown"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Sin salida en terminal"),
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    ejemplo: bool = typer.Option(False, '--ejemplo', help='Formulario precargado para pruebas'),
    en_blanco: bool = typer.Option(False, '--en-blanco', help='Solicitar datos reales sin precargar el ejemplo'),
    avanzado: bool = typer.Option(False, '--avanzado', help='Habilitar modo trazable; siempre Froehlich en proyectos nuevos'),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Calcula socavación: YAML o ingreso interactivo si no hay archivo."""
    if archivo is not None and (demo or ejemplo or en_blanco):
        raise ValueError('No combine un archivo de proyecto con --demo, --ejemplo o --en-blanco.')
    if archivo is None:
        proyecto = ejecutar_wizard(salida=None, use_defaults=demo, ejemplo=ejemplo, en_blanco=en_blanco, avanzado=avanzado)
    else:
        proyecto = cargar_proyecto(archivo)
    _calcular_y_mostrar(proyecto, export=export, quiet=quiet, word=word)


@app.command("wizard")
@_errores_entrada
def wizard_cmd(
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Opcional: guardar también un YAML",
    ),
    demo: bool = typer.Option(False, "--demo", help="Usar valores por defecto para prueba rápida"),
    ejemplo: bool = typer.Option(False, '--ejemplo', help='Formulario con datos de prueba para aceptar o editar'),
    en_blanco: bool = typer.Option(False, '--en-blanco', help='Ingreso sin valores de ejemplo'),
    avanzado: bool = typer.Option(False, '--avanzado', help='Habilitar selección de modo trazable para Froehlich'),
    word: Path | None = typer.Option(None, "--word", "-w", help="Ruta memoria Word (.docx)"),
) -> None:
    """Ingreso en terminal y cálculo inmediato."""
    proyecto = ejecutar_wizard(salida=output, use_defaults=demo, ejemplo=ejemplo, en_blanco=en_blanco, avanzado=avanzado)
    _calcular_y_mostrar(proyecto, export=None, quiet=False, word=word)


@app.command("word")
@_errores_entrada
def word_cmd(
    archivo: Path = typer.Argument(..., help="Archivo YAML del proyecto"),
    output: Path | None = typer.Option(None, "--output", "-o", help="Ruta memoria Word (.docx)"),
) -> None:
    """Genera memoria Word desde un YAML sin mostrar resultados en terminal."""
    proyecto = cargar_proyecto(archivo)
    resultado = ejecutar(proyecto)
    if output is None:
        generate_socavacion_docx_with_dialog(resultado, proyecto)
    else:
        generate_socavacion_docx(resultado, proyecto, output)
        typer.echo(f"Memoria Word generada: {output}")


@app.command('completar')
@_errores_entrada
def completar_cmd(
    archivo: Path = typer.Argument(..., help='YAML/JSON existente; se conserva como original'),
    output: Path | None = typer.Option(None, '--output', '-o', help='YAML completado; por defecto *_completado.yaml'),
    export: Path | None = typer.Option(None, '--export', '-e', help='Informe Markdown'),
    quiet: bool = typer.Option(False, '--quiet', '-q', help='Sin tablas ni diálogo Word al finalizar'),
    word: Path | None = typer.Option(None, '--word', '-w', help='Memoria Word'),
):
    """Revisa datos actuales, solicita faltantes, guarda una copia y calcula."""
    base = cargar_proyecto(archivo)
    destino = output or archivo.with_name(archivo.stem + '_completado.yaml')
    proyecto = ejecutar_wizard(salida=destino, base=base)
    _calcular_y_mostrar(proyecto, export=export, quiet=quiet, word=word)


if __name__ == "__main__":
    app()
