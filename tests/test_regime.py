"""Tests de régimen del lecho."""

from socavacion.core.regime import detectar_regimen, velocidad_critica
from socavacion.domain.enums import RegimenLecho


def test_velocidad_critica_positiva():
    Vc = velocidad_critica(y=3.0, d50_m=0.0025)
    assert Vc > 0


def test_lecho_vivo_cuando_v_mayor_vc():
    d50 = 0.0025
    y = 3.0
    Vc = velocidad_critica(y, d50)
    r = detectar_regimen(V1=Vc + 0.5, y1=y, d50_m=d50, sf=0.002)
    assert r.regimen == RegimenLecho.LECHO_VIVO


def test_agua_clara_cuando_v_menor_vc():
    d50 = 0.0025
    y = 3.0
    Vc = velocidad_critica(y, d50)
    r = detectar_regimen(V1=Vc - 0.1, y1=y, d50_m=d50, sf=0.002)
    assert r.regimen == RegimenLecho.AGUA_CLARA
