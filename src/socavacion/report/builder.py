"""Generación de informes Markdown."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from socavacion.domain.models import Proyecto
from socavacion.domain.results import ResultadoCompleto

_TEMPLATES = Path(__file__).parent / "templates"


def generar_informe(
    resultado: ResultadoCompleto,
    proyecto: Proyecto,
    ruta: Path,
) -> Path:
    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATES)),
        autoescape=select_autoescape(["md"]),
    )
    tpl = env.get_template("informe.md.j2")
    ruta.parent.mkdir(parents=True, exist_ok=True)
    contenido = tpl.render(
        resultado=resultado,
        proyecto=proyecto,
        fecha=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    ruta.write_text(contenido, encoding="utf-8")
    return ruta
