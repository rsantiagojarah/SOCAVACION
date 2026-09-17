"""Tabla 13 HHD p.107, transcrita de la imagen del PDF identificado."""
import math
from bisect import bisect_right

LUZ = [10,13,16,18,21,25,30,42,52,63,106,124,200]
VELOCIDAD = [1,1.5,2,2.5,3,3.5,4]
FILAS = [
    [.96,.97,.98,.98,.99,.99,.99,1,1,1,1,1,1],
    [.94,.96,.97,.97,.97,.98,.99,.99,.99,.99,1,1,1],
    [.93,.94,.95,.96,.97,.97,.98,.98,.99,.99,.99,.99,1],
    [.90,.93,.94,.95,.96,.96,.97,.98,.98,.99,1,.99,1],
    [.89,.91,.93,.94,.95,.96,.96,.97,.98,.98,.99,.99,.99],
    [.87,.90,.92,.93,.94,.95,.96,.97,.98,.98,.99,.99,.99],
    [.85,.89,.91,.92,.93,.94,.95,.96,.97,.98,.99,.99,.99],
]

def interpolar(x, xs, ys):
    i = min(max(bisect_right(xs, x)-1, 0), len(xs)-2)
    return ys[i] + (ys[i+1]-ys[i])*(x-xs[i])/(xs[i+1]-xs[i])

def factor_mu(luz: float, velocidad: float) -> float:
    if not math.isfinite(luz) or not math.isfinite(velocidad) or not 10 <= luz <= 200 or velocidad < 0:
        raise ValueError('Tabla 13: luz entre 10 y 200 m, velocidad finita no negativa; no extrapolar')
    if velocidad < 1:
        return 1.0
    # La fila impresa dice >4.0; en 4.0 se adopta esa fila (criterio conservador documentado).
    valores = [interpolar(luz, LUZ, fila) for fila in FILAS]
    return interpolar(min(velocidad, 4), VELOCIDAD, valores)
