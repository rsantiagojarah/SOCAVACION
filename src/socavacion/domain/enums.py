from enum import Enum


class RegimenLecho(str, Enum):
    LECHO_VIVO = "lecho_vivo"
    AGUA_CLARA = "agua_clara"


class FormaEstribo(str, Enum):
    MURO_VERTICAL = "muro_vertical"
    MURO_VERTICAL_ALETAS_45 = "muro_vertical_aletas_45"
    TALUD_2H1V = "talud_2h1v"
    TALUD_3H1V = "talud_3h1v"


class FormaPilar(str, Enum):
    CIRCULAR = "circular"
    CUADRADO = "cuadrado"
    ALAS_RECTAS = "alas_rectas"
    ALAS_REDONDEADAS = "alas_redondeadas"


class TipoCauce(str, Enum):
    ESTABLE = "estable"
    DEGRADACION = "degradacion"
    AGRADACION = "agradacion"


class TipoCimentacion(str, Enum):
    SUPERFICIAL = "superficial"
    PROFUNDA = "profunda"
    ZAPATA_SOBRE_PILOTES = "zapata_sobre_pilotes"
    SOBRE_ROCA = "sobre_roca"


class LadoEstribo(str, Enum):
    IZQUIERDO = "izquierdo"
    DERECHO = "derecho"


class CondicionCaudal(str, Enum):
    DISENO = "diseno"
    VERIFICACION = "verificacion"
