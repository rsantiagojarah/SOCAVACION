"""Modelos de entrada del proyecto."""

from __future__ import annotations

from pydantic import BaseModel as PydanticBaseModel, ConfigDict, Field, field_validator
from typing import Literal


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(allow_inf_nan=False, extra='forbid')

from socavacion.domain.enums import (
    FormaEstribo,
    FormaPilar,
    LadoEstribo,
    TipoCauce,
    TipoCimentacion,
)
from socavacion.normative.constants import GAMMA_S_DEFAULT, GS_DEFAULT


class CondicionHidraulica(BaseModel):
    """Parámetros hidráulicos para un caudal (Q100 o Q500).

    Q1 y Q2 son opcionales; si no se ingresan, se resuelven automáticamente
    a partir del caudal total del proyecto (Q100 o Q500) para evitar
    duplicar datos de entrada.
    """

    y1: float | None = Field(None, gt=0, description="Tirante medio aproximación (m); no requerido por Froehlich con Ae/Qe/L")
    V1: float | None = Field(None, ge=0, description="Velocidad media aproximación (m/s)")
    W1: float | None = Field(None, gt=0, description="Ancho cauce aproximación (m)")
    W2: float | None = Field(None, gt=0, description="Luz hidráulica bajo puente (m)")
    Q1: float | None = Field(
        None,
        gt=0,
        description="Caudal cauce principal aproximación (m³/s); por defecto=Q_total",
    )
    Q2: float | None = Field(
        None,
        gt=0,
        description="Caudal sección contraída (m³/s); por defecto=Q_total",
    )
    y0: float | None = Field(None, gt=0, description="Tirante contraída antes socavación (m)")
    Sf: float | None = Field(None, ge=0, description="Pendiente línea de energía (m/m); opcional si no se calcula velocidad de corte")
    area_hidraulica: float | None = Field(None, gt=0, description="Área activa total de aproximación ingresada desde HEC-RAS (m2), mismo dominio que Q del evento")
    radio_hidraulico: float | None = Field(None, gt=0, description="R=A/P de HEC-RAS (m), sólo informativo; no sustituye hm=A/B")
    # Parámetros explícitos del método Lischtvan-Levediev MTC HHD.
    beta: float = Field(1.0, gt=0, description="Coeficiente de frecuencia MTC")
    mu: float = Field(1.0, gt=0, le=1.0, description="Factor de contracción MTC")
    phi: float = Field(1.0, ge=1, description="Factor de transporte MTC")
    exponente_x: float = Field(0.38, gt=0, description="z granular ec.59; alias histórico x; 0.38 sólo preliminar")
    Dm_mm: float | None = Field(None, gt=0, description="Diámetro característico MTC (mm)")
    h_local: float | None = Field(None, gt=0, description="Tirante original en el apoyo/franja LL (m)")
    alpha: float | None = Field(None, gt=0, description="Coeficiente LL sin mu; requiere fuente")
    Q_ll: float | None = Field(None, gt=0, description="Caudal de la sección LL; coherente con B_ll y h_m_ll")
    B_ll: float | None = Field(None, gt=0)
    h_m_ll: float | None = Field(None, gt=0)
    luz_libre: float | None = Field(None, ge=10, le=200, description="Luz libre mínima, Tabla 13, m")
    V_mu: float | None = Field(None, ge=0, description="Velocidad media de sección para Tabla 13, distinta de la velocidad local del pilar (m/s)")
    Ae: float | None = Field(None, gt=0, description="Área obstruida por este estribo para esta avenida (m2)")
    Qe: float | None = Field(None, ge=0, description="Caudal obstruido por este estribo (m3/s)")
    L_obstruida: float | None = Field(None, gt=0)
    h_pie: float | None = Field(None, gt=0)
    V_pie: float | None = Field(None, ge=0)
    fuentes: dict[str, str] = Field(default_factory=dict, description="Documento/página/sección de cada dato y coeficiente")

    def resolver_q(self, Q_total: float) -> None:
        """Asigna Q1 y Q2 desde Q_total cuando no fueron ingresados."""
        if self.Q1 is None:
            self.Q1 = Q_total
        if self.Q2 is None:
            self.Q2 = Q_total

    @property
    def q1(self) -> float:
        if self.Q1 is None:
            raise ValueError("Q1 no resuelto; llamar resolver_q(Q_total) primero")
        return self.Q1 / self.W1

    @property
    def q2(self) -> float:
        if self.Q2 is None:
            raise ValueError("Q2 no resuelto; llamar resolver_q(Q_total) primero")
        return self.Q2 / self.W2


class Estribo(BaseModel):
    """Datos de un estribo (izquierdo o derecho)."""

    lado: LadoEstribo
    D50_mm: float | None = Field(None, gt=0, description="D50 granulometría (mm); no requerido en Froehlich")
    Z_lecho: float | None = Field(None, description="Cota lecho actual (m s.n.m.)")
    q100: CondicionHidraulica
    q500: CondicionHidraulica
    qot: CondicionHidraulica | None = None
    metodo_local: Literal['froehlich', 'hire'] = 'froehlich'
    penetra_cauce: bool = False
    L_prima: float = Field(..., gt=0, description="Longitud de flujo obstruida, proyectada normal al flujo (m)")
    Ae: float = Field(
        ...,
        ge=0,
        description="Área flujo obstruida (m²); 0 si el estribo no obstruye el cauce",
    )
    forma: FormaEstribo = FormaEstribo.MURO_VERTICAL
    angulo_ataque: float = Field(90.0, gt=0, le=180, description="Grados")
    gamma_s: float = Field(GAMMA_S_DEFAULT, gt=0)
    Gs: float = Field(GS_DEFAULT, gt=0)

    @property
    def D50_m(self) -> float | None:
        return None if self.D50_mm is None else self.D50_mm / 1000.0

    @property
    def Dm_m(self) -> float | None:
        return None if self.D50_m is None else 1.25 * self.D50_m


class Pilar(BaseModel):
    """Datos de un pilar intermedio."""

    nombre: str = "Pilar 1"
    ancho_a: float = Field(..., gt=0, description="Ancho real de nariz del pilar (m), sin proyección por sesgo")
    forma: FormaPilar = FormaPilar.CIRCULAR
    angulo_ataque: float = Field(0.0, ge=0, le=180)
    q100: CondicionHidraulica
    q500: CondicionHidraulica
    qot: CondicionHidraulica | None = None
    Z_lecho: float | None = None
    longitud_l: float | None = Field(None, gt=0, description="Longitud real, no ancho proyectado (m)")
    D50_mm: float = Field(..., gt=0)
    K3: float = Field(1.1, ge=1.1, le=1.3, description="Tabla 22: 1.1 lecho plano/agua clara, hasta 1.3 dunas")
    K4: float = Field(1.0, gt=0, le=1, description="Sin reducción por armadura por defecto")
    fuente_K4: str = ''

    @property
    def D50_m(self) -> float:
        return self.D50_mm / 1000.0


class ClasificacionCauce(BaseModel):
    """Clasificación morfológica del cauce (10.2)."""

    tipo: TipoCauce = TipoCauce.ESTABLE
    y_sg_lp: float = Field(0.0, description="Degradación largo plazo (m); negativo si agradación")
    notas: str = ""


class DatosGeotecnia(BaseModel):
    """Datos para matriz de compatibilidad (10.11)."""

    evaluar: bool = True
    cota_sondaje_min: float | None = Field(None, description="Cota fondo sondaje más profundo (m s.n.m.)")
    hay_estrato_competente: bool = True
    roca_resistente: bool = False
    tipo_cimentacion: TipoCimentacion = TipoCimentacion.SUPERFICIAL
    Z_punta_pilotes: float | None = Field(None, description="Cota punta pilotes (m s.n.m.)")
    Z_encepado_zapata: float | None = Field(None, description="Cota cara superior zapata pilotes")
    D50_geotecnico_mm: float | None = None
    descripcion_estrato: str = ""


class Proyecto(BaseModel):
    """Proyecto completo de análisis de socavación."""

    nombre: str
    Q100: float = Field(..., gt=0, description="Caudal diseño T=100 (m³/s)")
    Q500: float = Field(..., gt=0, description="Caudal verificación T=500 (m³/s)")
    Q_ot: float | None = Field(None, gt=0, description="Caudal desbordamiento")
    T_ot: float | None = Field(None, gt=0, le=500)
    modo: Literal['preliminar', 'trazable'] = 'preliminar'
    datos_prueba: bool = False
    entrada_hidraulica: Literal['legacy', 'hec_ras'] = 'legacy'
    metodo_calculo: Literal['completo_legacy', 'froehlich'] = 'completo_legacy'
    supuestos: list[str] = Field(default_factory=list)
    material_lecho: Literal['granular', 'cohesivo', 'roca'] = 'granular'
    flujo: Literal['libre', 'presion', 'detritos'] = 'libre'
    lecho_homogeneo: bool = True
    fuentes: dict[str, str] = Field(default_factory=dict)
    justificacion_sin_desbordamiento: str = ''
    estribo_izquierdo: Estribo
    estribo_derecho: Estribo
    pilares: list[Pilar] = Field(default_factory=list)
    cauce: ClasificacionCauce = Field(default_factory=ClasificacionCauce)
    geotecnia: DatosGeotecnia

    @field_validator("estribo_izquierdo")
    @classmethod
    def _lado_izq(cls, v: Estribo) -> Estribo:
        if v.lado != LadoEstribo.IZQUIERDO:
            raise ValueError("estribo_izquierdo debe tener lado='izquierdo'")
        return v

    @field_validator("estribo_derecho")
    @classmethod
    def _lado_der(cls, v: Estribo) -> Estribo:
        if v.lado != LadoEstribo.DERECHO:
            raise ValueError("estribo_derecho debe tener lado='derecho'")
        return v

    @property
    def Q_diseno_soc(self) -> float:
        return self.Q100

    @property
    def Q_verif_soc(self) -> float:
        return self.Q500

    def estribos(self) -> list[Estribo]:
        return [self.estribo_izquierdo, self.estribo_derecho]
