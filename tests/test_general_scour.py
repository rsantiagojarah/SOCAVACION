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


def test_lischtvan_mtc_hhd_trazable_y_sin_doble_contraccion():
    r = lischtvan.calcular_mtc_hhd(
        Q=87.392412,
        h_m=1.371399,
        B=12.50,
        dm_mm=2.95,
        beta=1.05,
        mu=0.89,
        phi=1.0,
        x=0.38,
    )
    assert r.metodo.startswith("Lischtvan-Levediev MTC HHD")
    assert r.valor > 0
    assert r.intermedios["alpha_c"] > 0
    assert r.intermedios["Hs"] > r.intermedios["h_m"]
    assert "Tabla 29" in r.notas
