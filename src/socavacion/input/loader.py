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
        return Proyecto.model_validate(root)

    return Proyecto.model_validate(datos)


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
