"""Interpolación lineal en tablas normativas."""

from __future__ import annotations


def interpolar_lineal(x: float, tabla: list[tuple[float, ...]], col_y: int = 1) -> float:
    """Interpola columna col_y respecto a la primera columna de la tabla."""
    if not tabla:
        raise ValueError("Tabla vacía")

    if x <= tabla[0][0]:
        return tabla[0][col_y]
    if x >= tabla[-1][0]:
        return tabla[-1][col_y]

    for i in range(len(tabla) - 1):
        x0, y0 = tabla[i][0], tabla[i][col_y]
        x1, y1 = tabla[i + 1][0], tabla[i + 1][col_y]
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)

    return tabla[-1][col_y]


def interpolar_doble(
    x: float, tabla: list[tuple[float, float, float]]
) -> tuple[float, float]:
    """Interpola columnas x y A de tabla Lischtvan para D50 dado."""
    col_x = interpolar_lineal(x, tabla, col_y=1)
    col_a = interpolar_lineal(x, tabla, col_y=2)
    return col_x, col_a
