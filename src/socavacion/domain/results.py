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
    referencias: list[str] = field(default_factory=list)
    unidades: dict[str, str] = field(default_factory=dict)
    fuentes_datos: dict[str, str] = field(default_factory=dict)
    supuestos: list[str] = field(default_factory=list)


@dataclass
class RegimenResult:
    """Resultado de detección de régimen del lecho."""

    regimen: RegimenLecho
    Vc: float
    V1: float
    Fr: float
    V_star: float | None
    omega: float | None
    k1_contraccion: float | None


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
    regimen: RegimenResult | None
    general: ResultadoGeneral | None
    y_sc: ComponenteSocavacion | None
    y_sl: ComponenteSocavacion
    y_s_total: float | None
    advertencias: list[str] = field(default_factory=list)
    escenario: str = ''


@dataclass
class ResultadoPilarCaudal:
    nombre: str
    condicion: CondicionCaudal
    y_sp: ComponenteSocavacion
    regimen: RegimenLecho
    general: ResultadoGeneral | None = None
    y_s_total: float = 0.0
    Z_lecho_soc: float | None = None
    escenario: str = ''


@dataclass
class ResultadoCaudal:
    condicion: CondicionCaudal
    Q: float
    estribos: list[ResultadoEstriboCaudal]
    pilares: list[ResultadoPilarCaudal]
    escenario: str = ''


@dataclass
class ResultadoEstriboFinal:
    lado: LadoEstribo
    y_s_100: float
    y_s_500: float
    y_s_diseno: float
    Z_lecho_actual: float | None
    Z_lecho_soc: float | None
    Z_cim_min: float | None
    componentes_100: ResultadoEstriboCaudal | None = None
    componentes_500: ResultadoEstriboCaudal | None = None
    escenario_diseno: str = 'Q100'
    escenario_verificacion: str = 'Q500'


@dataclass
class ResultadoPilarFinal:
    nombre: str
    y_s_diseno: float
    y_s_verificacion: float
    y_s_max: float
    Z_lecho_soc: float | None
    Z_cim_limite: float | None
    escenario_diseno: str
    escenario_verificacion: str


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
    pilares_finales: list[ResultadoPilarFinal] = field(default_factory=list)
    auditoria: dict = field(default_factory=dict)
