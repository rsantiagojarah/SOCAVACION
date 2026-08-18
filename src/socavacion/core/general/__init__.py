"""Contexto compartido para métodos de socavación general."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from socavacion.domain.results import ComponenteSocavacion


@dataclass
class ContextoGeneral:
    Q: float
    y0: float
    y1: float
    W: float
    q: float
    d50_m: float
    d50_mm: float


class MetodoSocavacionGeneral(Protocol):
    nombre: str

    def calcular(self, ctx: ContextoGeneral) -> ComponenteSocavacion: ...
