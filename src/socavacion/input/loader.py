"""Carga de proyectos desde YAML/JSON."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from socavacion.domain.models import Proyecto


def cargar_proyecto(ruta: Path) -> Proyecto:
    texto = ruta.read_text(encoding="utf-8")
    if ruta.suffix.lower() in (".yaml", ".yml"):
        datos = yaml.safe_load(texto)
    elif ruta.suffix.lower() == ".json":
        datos = json.loads(texto)
    else:
        raise ValueError(f"Formato no soportado: {ruta.suffix}")

    if "proyecto" in datos:
        root = datos["proyecto"]
        root["estribo_izquierdo"] = _merge_estribo(datos.get("estribo_izquierdo", {}), "izquierdo")
        root["estribo_derecho"] = _merge_estribo(datos.get("estribo_derecho", {}), "derecho")
        root["pilares"] = datos.get("pilares", [])
        root["geotecnia"] = datos.get("geotecnia", {})
        root["cauce"] = datos.get("cauce", root.get("cauce", {}))
        proyecto = Proyecto.model_validate(root)
    else:
        proyecto = Proyecto.model_validate(datos)

    _resolver_caudales_hidraulica(proyecto)
    return proyecto


def _resolver_caudales_hidraulica(proyecto: Proyecto) -> None:
    """Completa Q1/Q2 de condiciones hidráulicas desde Q100/Q500 del proyecto."""
    for est in proyecto.estribos():
        est.q100.resolver_q(proyecto.Q100)
        est.q500.resolver_q(proyecto.Q500)
    for pilar in proyecto.pilares:
        pilar.q100.resolver_q(proyecto.Q100)
        pilar.q500.resolver_q(proyecto.Q500)


def _merge_estribo(data: dict, lado: str) -> dict:
    out = dict(data)
    out["lado"] = lado
    return out


def guardar_proyecto(proyecto: Proyecto, ruta: Path) -> None:
    payload = {
        "proyecto": {
            "nombre": proyecto.nombre,
            "Q100": proyecto.Q100,
            "Q500": proyecto.Q500,
            "Q_ot": proyecto.Q_ot,
        },
        "cauce": proyecto.cauce.model_dump(),
        "estribo_izquierdo": proyecto.estribo_izquierdo.model_dump(),
        "estribo_derecho": proyecto.estribo_derecho.model_dump(),
        "pilares": [p.model_dump() for p in proyecto.pilares],
        "geotecnia": proyecto.geotecnia.model_dump(),
    }
    ruta.write_text(
        yaml.dump(payload, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )
