"""Tablas normativas para interpolación."""

from socavacion.domain.enums import FormaEstribo, FormaPilar

# Lischtvan-Lebediev: D50 (mm), x, A
LISCHTVAN_TABLE: list[tuple[float, float, float]] = [
    (0.05, 0.64, 0.70),
    (0.25, 0.68, 0.82),
    (1.0, 0.72, 0.94),
    (2.5, 0.75, 1.03),
    (5.0, 0.78, 1.14),
    (10.0, 0.82, 1.35),
    (25.0, 0.88, 1.65),
    (50.0, 0.92, 2.00),
    (75.0, 0.95, 2.25),
    (100.0, 0.97, 2.50),
    (150.0, 0.98, 2.75),
    (200.0, 0.99, 3.00),
]

# K1 forma estribo (HEC-18)
K1_ESTRIBO: dict[FormaEstribo, float] = {
    FormaEstribo.MURO_VERTICAL: 1.00,
    FormaEstribo.MURO_VERTICAL_ALETAS_45: 0.82,
    FormaEstribo.TALUD_2H1V: 0.55,
    FormaEstribo.TALUD_3H1V: 0.42,
}

# K1 forma pilar (HEC-18 CSU)
K1_PILAR: dict[FormaPilar, float] = {
    FormaPilar.CIRCULAR: 1.0,
    FormaPilar.CUADRADO: 1.1,
    FormaPilar.ALAS_RECTAS: 1.1,
    FormaPilar.ALAS_REDONDEADAS: 1.0,
}

# k1 contracción Laursen vs V*/omega
K1_CONTRACCION_BOUNDS: list[tuple[float, float]] = [
    (0.0, 0.59),
    (0.50, 0.59),
    (2.0, 0.69),
]
