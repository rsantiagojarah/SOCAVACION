"""Modelos de entrada del proyecto."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from socavacion.domain.enums import (
    FormaEstribo,
    FormaPilar,
    LadoEstribo,
    TipoCauce,
    TipoCimentacion,
)
from socavacion.normative.constants import GAMMA_S_DEFAULT, GS_DEFAULT


class CondicionHidraulica(BaseModel):
    """Parámetros hidráulicos para un caudal (Q100 o Q500)."""

    y1: float = Field(..., gt=0, description="Tirante medio aproximación (m)")
    V1: float = Field(..., ge=0, description="Velocidad media aproximación (m/s)")
    W1: float = Field(..., gt=0, description="Ancho cauce aproximación (m)")
    W2: float = Field(..., gt=0, description="Luz hidráulica bajo puente (m)")
    Q1: float = Field(..., gt=0, description="Caudal cauce principal aproximación (m³/s)")
    Q2: float = Field(..., gt=0, description="Caudal sección contraída (m³/s)")
    y0: float = Field(..., gt=0, description="Tirante contraída antes socavación (m)")
    Sf: float = Field(..., ge=0, description="Pendiente línea de energía (m/m)")

    @property
    def q1(self) -> float:
        return self.Q1 / self.W1

    @property
    def q2(self) -> float:
        return self.Q2 / self.W2


class Estribo(BaseModel):
    """Datos de un estribo (izquierdo o derecho)."""

    lado: LadoEstribo
    D50_mm: float = Field(..., gt=0, description="D50 granulometría (mm)")
    Z_lecho: float = Field(..., description="Cota lecho actual (m s.n.m.)")
    q100: CondicionHidraulica
    q500: CondicionHidraulica
    L_prima: float = Field(..., gt=0, description="Longitud embalse (m)")
    Ae: float = Field(..., gt=0, description="Área flujo obstruida (m²)")
    forma: FormaEstribo = FormaEstribo.MURO_VERTICAL
    angulo_ataque: float = Field(90.0, gt=0, le=180, description="Grados")
    gamma_s: float = Field(GAMMA_S_DEFAULT, gt=0)
    Gs: float = Field(GS_DEFAULT, gt=0)

    @property
    def D50_m(self) -> float:
        return self.D50_mm / 1000.0

    @property
    def Dm_m(self) -> float:
        return 1.25 * self.D50_m


class Pilar(BaseModel):
    """Datos de un pilar intermedio."""

    nombre: str = "Pilar 1"
    ancho_a: float = Field(..., gt=0, description="Ancho proyectado (m)")
    forma: FormaPilar = FormaPilar.CIRCULAR
    angulo_ataque: float = Field(0.0, ge=0, le=180)
    q100: CondicionHidraulica
    q500: CondicionHidraulica
    D50_mm: float = Field(..., gt=0)
    K3: float = Field(1.0, gt=0, description="Factor lecho (1.0 lecho vivo, 1.1 agua clara)")
    K4: float = Field(1.0, gt=0, description="Factor armadura lecho")

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

    cota_sondaje_min: float = Field(..., description="Cota fondo sondaje más profundo (m s.n.m.)")
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
        if self.Q_ot is not None:
            return max(self.Q100, self.Q_ot)
        return self.Q100

    @property
    def Q_verif_soc(self) -> float:
        if self.Q_ot is not None:
            return max(self.Q500, self.Q_ot)
        return self.Q500

    def estribos(self) -> list[Estribo]:
        return [self.estribo_izquierdo, self.estribo_derecho]
