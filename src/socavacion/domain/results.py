"""Modelos de resultados de cálculo."""

from __future__ import annotations

from dataclasses import dataclass, field

from socavacion.domain.enums import (
    CondicionCaudal,
    LadoEstribo,
    RegimenLecho,
)


@dataclass
class ComponenteSocavacion:
    """Resultado trazable de un método de cálculo."""

    metodo: str
    valor: float
    formula: str
    intermedios: dict[str, float] = field(default_factory=dict)
    notas: str = ""


@dataclass
class RegimenResult:
    """Resultado de detección de régimen del lecho."""

    regimen: RegimenLecho
    Vc: float
    V1: float
    Fr: float
    V_star: float
    omega: float
    k1_contraccion: float


@dataclass
class ResultadoGeneral:
    y_sg_lp: float
    y_sg_lischtvan: ComponenteSocavacion
    y_sg_neill: ComponenteSocavacion
    y_sg_lacey: ComponenteSocavacion
    y_sg_avenida: float
    y_sg_total: float
    metodo_gobernante: str


@dataclass
class ResultadoEstriboCaudal:
    lado: LadoEstribo
    condicion: CondicionCaudal
    regimen: RegimenResult
    general: ResultadoGeneral
    y_sc: ComponenteSocavacion
    y_sl: ComponenteSocavacion
    y_s_total: float
    advertencias: list[str] = field(default_factory=list)


@dataclass
class ResultadoPilarCaudal:
    nombre: str
    condicion: CondicionCaudal
    y_sp: ComponenteSocavacion
    regimen: RegimenLecho


@dataclass
class ResultadoCaudal:
    condicion: CondicionCaudal
    Q: float
    estribos: list[ResultadoEstriboCaudal]
    pilares: list[ResultadoPilarCaudal]


@dataclass
class ResultadoEstriboFinal:
    lado: LadoEstribo
    y_s_100: float
    y_s_500: float
    y_s_diseno: float
    Z_lecho_actual: float
    Z_lecho_soc: float
    Z_cim_min: float | None
    componentes_100: ResultadoEstriboCaudal | None = None
    componentes_500: ResultadoEstriboCaudal | None = None


@dataclass
class ItemCompatibilidad:
    item: str
    hidraulica: str
    geotecnia: str
    compatible: bool
    accion: str = ""


@dataclass
class ResultadoGeotecnia:
    items: list[ItemCompatibilidad]
    compatible_global: bool
    conclusion: str


@dataclass
class ResultadoCompleto:
    proyecto_nombre: str
    Q_diseno: float
    Q_verif: float
    caudales: list[ResultadoCaudal]
    estribos_finales: list[ResultadoEstriboFinal]
    geotecnia: ResultadoGeotecnia
    advertencias_globales: list[str] = field(default_factory=list)
