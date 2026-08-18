"""Tests socavación general."""

from socavacion.core.general import ContextoGeneral
from socavacion.core.general import lischtvan, neill, lacey
from socavacion.core.interpolation import interpolar_doble
from socavacion.normative.tables import LISCHTVAN_TABLE


def test_interpolacion_lischtvan_tabla_exacta():
    x, a = interpolar_doble(1.0, LISCHTVAN_TABLE)
    assert x == 0.72
    assert a == 0.94


def test_lischtvan_no_negativo():
    ctx = ContextoGeneral(Q=800, y0=3.0, y1=3.2, W=45, q=17.78, d50_m=0.0025, d50_mm=2.5)
    r = lischtvan.calcular(ctx)
    assert r.valor >= 0


def test_neill_sin_contraccion_cero():
    ctx = ContextoGeneral(Q=800, y0=3.0, y1=3.2, W=45, q=17.78, d50_m=0.0025, d50_mm=2.5)
    r = neill.calcular(ctx, q1=17.78, q2=17.78)
    assert r.valor == 0.0


def test_lacey_positivo():
    ctx = ContextoGeneral(Q=850, y0=3.0, y1=3.2, W=45, q=18.89, d50_m=0.0025, d50_mm=2.5)
    r = lacey.calcular(ctx)
    assert r.valor >= 0
