"""Test integración pipeline."""

from pathlib import Path

from socavacion.core.pipeline import ejecutar
from socavacion.input.loader import cargar_proyecto
from socavacion.core.long_term import calcular_y_sg_lp
from socavacion.domain.enums import TipoCauce
from socavacion.domain.models import ClasificacionCauce


EJEMPLO = Path(__file__).resolve().parents[1] / "ejemplos" / "puente_ejemplo.yaml"


def test_cargar_ejemplo():
    p = cargar_proyecto(EJEMPLO)
    assert p.nombre == "Puente Rio Ejemplo"
    assert p.Q100 == 850.0


def test_pipeline_completo():
    p = cargar_proyecto(EJEMPLO)
    r = ejecutar(p)
    assert len(r.estribos_finales) == 2
    for e in r.estribos_finales:
        assert e.y_s_diseno >= 0
        assert e.Z_lecho_soc < e.Z_lecho_actual


def test_agradacion_no_reduce():
    y, adv = calcular_y_sg_lp(ClasificacionCauce(tipo=TipoCauce.AGRADACION, y_sg_lp=-0.5))
    assert y == 0.0
    assert len(adv) > 0
