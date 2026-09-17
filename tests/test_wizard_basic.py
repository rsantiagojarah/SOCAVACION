"""Datos mínimos, derivaciones explícitas y alcance limitado del formulario básico."""
import pytest
from socavacion.input.wizard import ejecutar_wizard
from socavacion.input.wizard_basic import hidraulica_rectangular
from socavacion.core.pipeline import ejecutar
from socavacion.input.validator import validar_proyecto
from socavacion.normative.mu import factor_mu


def aceptar_defaults(monkeypatch):
    preguntas=[]
    def prompt(label,**kw):
        preguntas.append(label)
        return str(kw.get('default',''))
    def confirm(label,**kw):
        preguntas.append(label)
        return kw.get('default',False)
    monkeypatch.setattr('typer.prompt',prompt)
    monkeypatch.setattr('typer.confirm',confirm)
    return preguntas


def test_nuevo_ingreso_reducido_no_pide_ll_ni_pilares(monkeypatch):
    preguntas=aceptar_defaults(monkeypatch)
    p=ejecutar_wizard()
    basico=len(preguntas)
    assert basico<=35
    assert not any('Fuente beta' in x or 'Pendiente' in x for x in preguntas)
    preguntas.clear()
    ejecutar_wizard(avanzado=True)
    assert len(preguntas)<=35
    assert not any('beta' in x or 'pilares' in x or 'Dm' in x for x in preguntas)
    assert p.metodo_calculo == 'froehlich'


def test_deriva_hidraulica_y_franjas_sin_igualar_qe_a_qtotal():
    hid=hidraulica_rectangular(Q=100,B=20,h=2,dm=3,z=.38,beta=1.05,luz=12,
                              fuentes={'geometria':'Ensayo'},L=3)
    assert hid.V1==2.5
    assert hid.Ae==6
    assert hid.Qe==15
    assert hid.h_local==hid.h_m_ll==2
    assert hid.Sf is None
    assert 'mu' not in hid.model_fields_set
    assert hid.luz_libre==12
    assert hid.fuentes['geometria']=='Ensayo'


def test_basico_no_aprueba_geotecnia_ni_cota_cimentacion(monkeypatch):
    aceptar_defaults(monkeypatch)
    p=ejecutar_wizard()
    r=ejecutar(p)
    assert p.geotecnia.cota_sondaje_min is None
    assert not p.geotecnia.evaluar
    assert not r.geotecnia.compatible_global
    assert 'NO EVALUADA' in r.geotecnia.conclusion
    assert all(e.Z_cim_min is None for e in r.estribos_finales)
    assert all(p.Z_cim_limite is None for p in r.pilares_finales)
    assert all(e.regimen is None for c in r.caudales for e in c.estribos)
    assert not any('Qe=Q*L/B' in s for s in r.advertencias_globales)
    assert all(e.y_s_total is None for c in r.caudales for e in c.estribos)
    assert not any('falta dato explícito' in s for s in validar_proyecto(p))


def test_no_aplica_uniformidad_sin_confirmacion(monkeypatch):
    monkeypatch.setattr('typer.prompt',lambda *a,**k:k.get('default',''))
    monkeypatch.setattr('typer.confirm',lambda *a,**k:False)
    with pytest.raises(ValueError,match='no aplica'):
        ejecutar_wizard()


@pytest.mark.parametrize('L',[0,21])
def test_rechaza_franjas_invalidas(L):
    with pytest.raises(ValueError):
        hidraulica_rectangular(Q=100,B=20,h=2,dm=3,z=.38,beta=1.05,luz=12,fuentes={},L=L)


@pytest.mark.parametrize('luz,velocidad,mu',[(30,1.5,.99),(52,2,.99),(42,2.5,.98),(63,2.5,.99),(106,2.5,1)])
def test_mu_celdas_contrastadas_con_imagen_ampliada(luz,velocidad,mu):
    # HHD p.107 Tabla13: prueba independiente de la matriz usada en el código.
    assert factor_mu(luz,velocidad)==mu
