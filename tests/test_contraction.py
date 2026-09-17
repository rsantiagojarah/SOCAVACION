"""Tests socavación por contracción."""

from socavacion.core.contraction import calcular_contraccion
from socavacion.core.regime import detectar_regimen
from socavacion.domain.models import CondicionHidraulica


def _hid(**kw) -> CondicionHidraulica:
    defaults = dict(y1=3.2, V1=2.1, W1=45.0, W2=38.0, Q1=800, Q2=800, y0=3.0, Sf=0.002)
    defaults.update(kw)
    return CondicionHidraulica(**defaults)


def test_contraccion_nula_ancho_similar():
    hid = _hid(W2=44.9)
    reg = detectar_regimen(hid.V1, hid.y1, 0.0025, hid.Sf)
    y_sc, adv = calcular_contraccion(hid, reg, 0.0025)
    assert y_sc.valor == 0.0
    assert any("W2" in a for a in adv)


def test_contraccion_lecho_vivo_positiva():
    hid = _hid()
    reg = detectar_regimen(hid.V1, hid.y1, 0.0025, hid.Sf)
    y_sc, _ = calcular_contraccion(hid, reg, 0.0025)
    assert y_sc.valor >= 0


def test_q1_q2_opcionales_se_resuelven():
    hid = CondicionHidraulica(
        y1=3.2, V1=2.1, W1=45.0, W2=38.0, y0=3.0, Sf=0.002
    )
    hid.resolver_q(800.0)
    assert hid.Q1 == 800.0
    assert hid.Q2 == 800.0
    assert hid.q1 == 800.0 / 45.0
    reg = detectar_regimen(hid.V1, hid.y1, 0.0025, hid.Sf)
    y_sc, _ = calcular_contraccion(hid, reg, 0.0025)
    assert y_sc.valor >= 0
