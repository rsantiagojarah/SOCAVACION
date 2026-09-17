"""Tests socavación local estribos."""

from socavacion.core.local_abutment import calcular_local_estribo, k2_angulo
from socavacion.core.regime import detectar_regimen
from socavacion.domain.enums import FormaEstribo, LadoEstribo
from socavacion.domain.models import CondicionHidraulica, Estribo


def test_k2_perpendicular():
    assert abs(k2_angulo(90.0) - 1.0) < 1e-6


def test_froehlich_estribo_corto():
    hid = CondicionHidraulica(
        y1=3.2, V1=2.1, W1=45, W2=38, Q1=800, Q2=800, y0=3.0, Sf=0.002
    )
    est = Estribo(
        lado=LadoEstribo.IZQUIERDO,
        D50_mm=2.5,
        Z_lecho=2450.0,
        q100=hid,
        q500=hid,
        L_prima=12.0,
        Ae=85.0,
        forma=FormaEstribo.MURO_VERTICAL,
        angulo_ataque=90.0,
    )
    reg = detectar_regimen(hid.V1, hid.y1, est.D50_m, hid.Sf)
    y_sl, _ = calcular_local_estribo(est, hid, reg)
    assert y_sl.valor > 0
    assert y_sl.metodo.startswith("Froehlich HEC-18")


def test_ae_cero_usa_y1_y_v1():
    hid = CondicionHidraulica(
        y1=1.82, V1=5.9298, W1=12.5, W2=12.5, Q1=135.06, Q2=135.06, y0=1.82, Sf=0.045
    )
    est = Estribo(
        lado=LadoEstribo.IZQUIERDO,
        D50_mm=2.95,
        Z_lecho=2000.0,
        q100=hid,
        q500=hid,
        L_prima=12.5,
        Ae=0.0,
        forma=FormaEstribo.MURO_VERTICAL,
        angulo_ataque=90.0,
    )
    reg = detectar_regimen(hid.V1, hid.y1, est.D50_m, hid.Sf)
    y_sl, _ = calcular_local_estribo(est, hid, reg)
    assert y_sl.valor > 0
    assert abs(y_sl.intermedios["ya"] - hid.y1) < 1e-9
