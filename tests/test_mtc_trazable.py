"""Casos independientes para el motor MTC y su registro reproducible."""
import json
import math
from pathlib import Path

import pytest
from pydantic import ValidationError

from socavacion.core.general.lischtvan import calcular_mtc_hhd
from socavacion.core.local_abutment import calcular_local_estribo
from socavacion.core.local_pier import calcular_local_pilar, k2_pilar
from socavacion.core.pipeline import ejecutar
from socavacion.core.regime import detectar_regimen
from socavacion.domain.models import CondicionHidraulica, Proyecto
from socavacion.input.loader import cargar_proyecto, guardar_proyecto
from socavacion.input.validator import validar_proyecto
from socavacion.normative.mu import factor_mu, LUZ, FILAS, VELOCIDAD
from socavacion.normative.references import REFERENCIAS
from socavacion.report.builder import generar_informe
from socavacion.report.trace import componentes

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def proyecto():
    return cargar_proyecto(ROOT / 'ejemplos/puente_mtc_trazable.yaml')

def ll(**changes):
    args = dict(Q=87.392412, h_m=1.371399, B=12.5, dm_mm=2.95,
                beta=1.05, mu=.89, phi=1, x=.38, h_local=1.371399)
    args.update(changes)
    return calcular_mtc_hhd(**args)

def test_ll_caso_usuario_valor_y_unidades():
    r = ll()
    assert r.intermedios['Hs'] == pytest.approx(4.564216, abs=1e-6)
    assert r.valor == pytest.approx(3.192817, abs=1e-6)
    assert r.unidades['Dm_mm'] == 'mm'
    assert r.intermedios['alpha_c'] == pytest.approx(4.640527, abs=1e-6)

def test_ll_h_local_distinto_de_tirante_medio():
    r = ll(h_local=2)
    alpha = 87.392412/(12.5*1.371399**(5/3))
    hs = (alpha*2**(5/3)/(.68*1.05*.89*2.95**.28))**(1/1.38)
    assert r.valor == pytest.approx(hs-2)
    assert ll(h_local=2, alpha=alpha).valor == pytest.approx(r.valor)
    assert ll(h_local=2, alpha=alpha, h_m=9, B=3).valor == pytest.approx(r.valor)

def test_ll_no_socavacion_negativa():
    r = ll(Q=.01)
    assert r.valor == 0
    assert r.intermedios['descenso_sin_truncar'] < 0

@pytest.mark.parametrize('changes', [{'mu':0}, {'mu':1.1}, {'phi':.9}, {'dm_mm':0},
                                    {'Q':float('inf')}, {'h_local':float('nan')}, {'alpha':-1}])
def test_ll_rechaza_entradas_invalidas(changes):
    with pytest.raises(ValueError):
        ll(**changes)

def test_mu_nodos_interpolacion_y_limites():
    for v, row in zip(VELOCIDAD, FILAS):
        for luz, esperado in zip(LUZ, row):
            assert factor_mu(luz, v) == pytest.approx(esperado)
    assert factor_mu(12.5,5.1) == pytest.approx(.8833333333333333)
    assert ll(mu=factor_mu(12.5,5.1)).valor == pytest.approx(3.217753, abs=1e-5)
    assert factor_mu(12.5,.5) == 1
    assert factor_mu(11.5,1.25) == pytest.approx((.96+.97+.94+.96)/4)
    with pytest.raises(ValueError):
        factor_mu(9,2)

def test_froehlich_usa_qe_no_q1_sin_tope(proyecto):
    est = proyecto.estribo_izquierdo
    hid = est.q500
    hid.Q1 = 5000  # ajeno al flujo obstruido
    reg = detectar_regimen(hid.V1,hid.y1,est.D50_m,hid.Sf)
    r, _ = calcular_local_estribo(est,hid,reg)
    he, ve = hid.Ae/hid.L_obstruida, hid.Qe/hid.Ae
    esperado = he*(2.27*(hid.L_obstruida/he)**.43*(ve/math.sqrt(9.81*he))**.61+1)
    assert r.valor == pytest.approx(esperado)
    assert r.valor > 2.4*he
    assert r.intermedios['Ve'] == pytest.approx(ve)

def test_hire_aplicacion_y_ecuacion(proyecto):
    est = proyecto.estribo_izquierdo
    est.metodo_local = 'hire'
    hid = est.q100
    reg = detectar_regimen(hid.V1,hid.y1,est.D50_m,hid.Sf)
    with pytest.raises(ValueError, match='HIRE requiere'):
        calcular_local_estribo(est,hid,reg)
    est.penetra_cauce = True
    hid.h_pie, hid.V_pie, hid.L_obstruida = 1,2,30
    r, _ = calcular_local_estribo(est,hid,reg)
    assert r.valor == pytest.approx(4/.55*(2/math.sqrt(9.81))**.33)
    hid.L_obstruida = 25
    with pytest.raises(ValueError, match='L/h'):
        calcular_local_estribo(est,hid,reg)

def test_csu_sesgo_formula_y_armadura(proyecto):
    p = proyecto.pilares[0]
    h = p.q500
    reg = detectar_regimen(h.V1,h.y1,p.D50_m,h.Sf)
    r = calcular_local_pilar(p,h,reg)
    k2 = (math.cos(math.radians(10))+3/.8*math.sin(math.radians(10)))**.65
    assert r.valor == pytest.approx(2*k2*1.1*.8**.65*h.y1**.35*reg.Fr**.43)
    assert k2 > 1
    assert k2_pilar(90,20) == pytest.approx(12**.65)
    assert k2_pilar(0,3) == 1
    assert 'CSU_CORRECCION' in r.referencias
    p.K4=.8
    with pytest.raises(ValueError, match='fuente_K4'):
        calcular_local_pilar(p,h,reg)

def test_totales_por_apoyo_sin_doble_contraccion(proyecto):
    r = ejecutar(proyecto)
    assert all(d['coincide'] for d in r.auditoria['documentos'].values())
    for c in r.caudales:
        for e in c.estribos:
            assert e.y_sc.valor == 0
            assert e.y_s_total == pytest.approx(.2+e.general.y_sg_lischtvan.valor+e.y_sl.valor)
            assert e.regimen.omega is None
        p=c.pilares[0]
        assert p.y_s_total == pytest.approx(.2+p.general.y_sg_lischtvan.valor+p.y_sp.valor)
        assert p.Z_lecho_soc == pytest.approx(99.8-p.y_s_total)
    final = r.pilares_finales[0]
    assert final.Z_cim_limite == pytest.approx(99.8-final.y_s_max-1)
    for _, comp in componentes(r):
        assert comp.referencias
        assert all(ref in REFERENCIAS for ref in comp.referencias)
        assert set(comp.intermedios) <= set(comp.unidades)

def test_desbordamiento_menor_caudal_puede_gobernar(proyecto):
    proyecto.Q_ot, proyecto.T_ot = 40, 50
    for apoyo in [*proyecto.estribos(), *proyecto.pilares]:
        h = apoyo.q100.model_copy(deep=True)
        h.Q_ll,h.Q1,h.Q2 = 40,40,40
        h.B_ll=3  # contracción mayor en evento de desbordamiento de ensayo
        apoyo.qot=h
    r=ejecutar(proyecto)
    assert len(r.caudales)==3
    assert all(e.escenario_diseno=='Qot' for e in r.estribos_finales)
    assert all(e.escenario_verificacion=='Qot' for e in r.estribos_finales)
    assert r.pilares_finales[0].escenario_verificacion=='Qot'
    # Si T_ot=200 no se incluye en el conjunto de diseño Q100.
    proyecto.T_ot=200
    r=ejecutar(proyecto)
    assert all(e.escenario_diseno=='Q100' for e in r.estribos_finales)
    assert all(e.escenario_verificacion=='Qot' for e in r.estribos_finales)

def test_trazable_rechaza_datos_y_fuentes_incompletos(proyecto):
    assert validar_proyecto(proyecto)==[]
    proyecto.estribo_izquierdo.q100.fuentes.pop('beta')
    with pytest.raises(ValueError, match='Fuentes pendientes: beta'):
        ejecutar(proyecto)
    proyecto.modo='preliminar'
    assert any('fuente beta' in w for w in ejecutar(proyecto).advertencias_globales)

def test_desbordamiento_exige_hidraulica_independiente(proyecto):
    proyecto.Q_ot,proyecto.T_ot = 40,50
    with pytest.raises(ValueError,match='falta hidráulica qot'):
        ejecutar(proyecto)

@pytest.mark.parametrize('material', ['roca','cohesivo'])
def test_rechaza_material_fuera_alcance(proyecto,material):
    proyecto.material_lecho=material
    with pytest.raises(ValueError,match='otro análisis'):
        ejecutar(proyecto)

def test_rechaza_presion_y_nan(proyecto):
    proyecto.flujo='presion'
    with pytest.raises(ValueError,match='Fuera de alcance'):
        ejecutar(proyecto)
    d=proyecto.estribo_izquierdo.q100.model_dump()
    d['V1']=float('nan')
    with pytest.raises(ValidationError):
        CondicionHidraulica.model_validate(d)

def test_exportacion_auditoria_reproducible(proyecto,tmp_path):
    r=ejecutar(proyecto)
    md=generar_informe(r,proyecto,tmp_path/'caso.md')
    registro=json.loads(md.with_suffix('.auditoria.json').read_text(encoding='utf-8'))
    p2=Proyecto.model_validate(registro['auditoria']['entrada'])
    r2=ejecutar(p2)
    assert r2.auditoria['entrada_sha256']==r.auditoria['entrada_sha256']
    assert r2.estribos_finales==r.estribos_finales
    assert len(r.auditoria['fuente_codigo_sha256'])==64
    assert 'ec.59' in md.read_text(encoding='utf-8')
    assert 'CSU_CORRECCION' in md.read_text(encoding='utf-8')
    yaml_path=tmp_path/'entrada.yaml'
    guardar_proyecto(proyecto,yaml_path)
    assert ejecutar(cargar_proyecto(yaml_path)).estribos_finales==r.estribos_finales

def test_word_sin_formulas_antiguas_y_con_json(proyecto,tmp_path):
    from docx import Document
    from socavacion.report.docx_builder import generate_socavacion_docx
    r=ejecutar(proyecto)
    path=generate_socavacion_docx(r,proyecto,tmp_path/'caso.docx')
    texto='\n'.join(p.text for p in Document(path).paragraphs)
    assert 'max(Q' not in texto
    assert 'fuente_codigo_sha256' in texto
    assert 'P1 sintético' in texto
    assert 'Qe=' in texto
    assert path.with_suffix('.auditoria.json').exists()

def test_cambio_de_pdf_detiene_trazable(proyecto,monkeypatch):
    from socavacion.core import pipeline
    docs=pipeline.verificar_documentos()
    docs['HHD']['coincide']=False
    monkeypatch.setattr(pipeline,'verificar_documentos',lambda:docs)
    with pytest.raises(ValueError,match='SHA256'):
        ejecutar(proyecto)
    proyecto.modo='preliminar'
    assert any('Manuales ausentes' in a for a in ejecutar(proyecto).advertencias_globales)

def test_mu_usa_media_seccion_no_velocidad_local(proyecto):
    h=proyecto.pilares[0].q500
    h.V1=1
    h.V_mu=5
    r=ejecutar(proyecto).caudales[1].pilares[0]
    assert r.general.y_sg_lischtvan.intermedios['mu']==pytest.approx(.8833333333333333)
    assert r.y_sp.intermedios['V']==1

def test_cabezal_referencia_contraccion_no_hoyo_local(proyecto):
    from socavacion.domain.enums import TipoCimentacion
    proyecto.geotecnia.tipo_cimentacion=TipoCimentacion.ZAPATA_SOBRE_PILOTES
    proyecto.geotecnia.Z_encepado_zapata=95
    proyecto.geotecnia.Z_punta_pilotes=80
    r=ejecutar(proyecto)
    assert all(e.Z_cim_min is None for e in r.estribos_finales)
    assert r.pilares_finales[0].Z_cim_limite is None
    # 95 queda por encima del hoyo local máximo pero bajo el lecho LL+LP.
    assert r.estribos_finales[0].Z_lecho_soc < 95
    assert next(i for i in r.geotecnia.items if i.item=='Zapata sobre pilotes').compatible

def test_coeficientes_no_explicitados_no_pasan_trazable(proyecto):
    h=proyecto.estribo_izquierdo.q100.model_dump(exclude_unset=True)
    h.pop('beta')
    proyecto.estribo_izquierdo.q100=CondicionHidraulica.model_validate(h)
    with pytest.raises(ValueError,match='Datos pendientes: beta'):
        ejecutar(proyecto)
