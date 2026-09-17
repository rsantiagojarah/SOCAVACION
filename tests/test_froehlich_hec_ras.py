"""Froehlich exclusivo: HEC-RAS manual, sin LL, sin franjas ni cimentación."""
import json
import math
from pathlib import Path
import pytest
from typer.testing import CliRunner
from socavacion.cli.app import app
from socavacion.core.pipeline import ejecutar
from socavacion.input.hec_ras import hidraulica_froehlich
from socavacion.input.wizard_froehlich import datos_prueba_froehlich
from socavacion.input.validator import validar_proyecto
from socavacion.input.loader import cargar_proyecto, guardar_proyecto

runner = CliRunner()


def respuestas_froehlich(path, *, ot=False, pendientes=False, modo='trazable'):
    out = ['Prueba Froehlich', 'y', '80', '100']
    out += ['60', '50'] if ot else ['']
    out += [modo]
    for _ in range(3 if ot else 2):
        out += ['30', '1,2']
    for _ in range(2):
        out += ['muro_vertical', '90']
        for _ in range(3 if ot else 2):
            out += ['2', '3', '5']
    out += ['', ''] if pendientes else ['Modelo prueba; plan P; River R; Reach T; RS100; perfiles Q100/Q500/Qot', 'Plano prueba P-01']
    if not ot:
        out += ['' if pendientes else 'Prueba: rasante no rebasada según modelo citado']
    out += [str(path)]
    return '\n'.join(out) + '\n'


def test_formula_independiente_y_componentes_no_evaluados(monkeypatch):
    def prohibido(*a, **kw):
        pytest.fail('No debe ejecutarse LL ni diagnóstico granulométrico')
    monkeypatch.setattr('socavacion.core.pipeline.calcular_general', prohibido)
    monkeypatch.setattr('socavacion.core.pipeline.detectar_regimen', prohibido)
    p = datos_prueba_froehlich()
    r = ejecutar(p)
    he, ve = 3/2, 8/3
    fre = ve / math.sqrt(9.81*he)
    esperado = he*(2.27*(2/he)**.43*fre**.61+1)
    e = r.caudales[0].estribos[0]
    assert e.y_sl.valor == pytest.approx(esperado)
    assert e.y_sl.intermedios['Ve'] != pytest.approx(p.Q100/18)
    assert e.general is None and e.y_sc is None and e.y_s_total is None
    assert not r.pilares_finales
    assert all(e.Z_cim_min is None and e.Z_lecho_soc is None for e in r.estribos_finales)
    assert r.auditoria['referencias'].keys() == {'F92', 'MP123a'}


def test_radio_y_area_total_no_sustituyen_datos_locales():
    p = datos_prueba_froehlich()
    a = ejecutar(p)
    for e in p.estribos():
        e.q100.radio_hidraulico = 99
        e.q100.area_hidraulica = 100
    b = ejecutar(p)
    assert b.caudales[0].estribos[0].y_sl.valor == a.caudales[0].estribos[0].y_sl.valor
    assert b.caudales[0].estribos[0].y_sl.intermedios['R_informativo'] == 99
    assert b.auditoria['entrada_sha256'] != a.auditoria['entrada_sha256']


def test_radio_opcional_y_prohibe_total_incompleto():
    from socavacion.core.totals import total_estribo
    p = datos_prueba_froehlich()
    for e in p.estribos():
        e.q100.radio_hidraulico = None
    r = ejecutar(p)
    assert 'R_informativo' not in r.caudales[0].estribos[0].y_sl.intermedios
    with pytest.raises(ValueError, match='total no evaluada'):
        total_estribo(r.caudales[0].estribos[0])


def test_init_crea_solo_froehlich(tmp_path):
    archivo = tmp_path/'nuevo.yaml'
    r = runner.invoke(app, ['init', '-o', str(archivo)])
    assert r.exit_code == 0, r.output
    p = cargar_proyecto(archivo)
    assert p.metodo_calculo == 'froehlich' and p.datos_prueba
    assert not p.pilares
    assert ejecutar(p).caudales[0].estribos[0].general is None


@pytest.mark.parametrize('campo,valor', [('Qe', None), ('Qe', 0), ('Ae', None), ('L_obstruida', None), ('area_hidraulica', None)])
def test_no_inventa_datos_obstruidos(campo, valor):
    p = datos_prueba_froehlich()
    setattr(p.estribo_derecho.q100, campo, valor)
    with pytest.raises(ValueError, match=campo):
        ejecutar(p)


def test_sumas_obstruidas_no_superan_seccion():
    p = datos_prueba_froehlich()
    for e in p.estribos():
        e.q100.Qe = 30
    with pytest.raises(ValueError, match='suma'):
        ejecutar(p)


@pytest.mark.parametrize('campo,valor', [('R', -1), ('R', float('nan')), ('Ae', 21), ('Qe', 101), ('L', 0)])
def test_rechaza_datos_invalidos(campo, valor):
    args = dict(Q=100, A=20, Ae=3, Qe=8, L=2, R=1)
    args[campo] = valor
    with pytest.raises(ValueError):
        hidraulica_froehlich(**args)


@pytest.mark.parametrize('flujo', ['presion', 'detritos'])
def test_torrentera_no_admite_huaycos_ni_presion(flujo):
    p = datos_prueba_froehlich()
    p.flujo = flujo
    with pytest.raises(ValueError, match='Fuera de alcance'):
        ejecutar(p)


def test_no_hire_ni_pilares():
    p = datos_prueba_froehlich()
    p.estribo_derecho.metodo_local = 'hire'
    with pytest.raises(ValueError, match='no admite pilares ni HIRE'):
        ejecutar(p)
    p = datos_prueba_froehlich()
    historico = cargar_proyecto(Path(__file__).resolve().parents[1]/'ejemplos/puente_mtc_trazable.yaml')
    p.pilares = historico.pilares
    with pytest.raises(ValueError, match='no admite pilares ni HIRE'):
        ejecutar(p)


def test_roundtrip_radio_y_fuentes_y_solo_froehlich(tmp_path):
    p = datos_prueba_froehlich()
    path = tmp_path/'manual.yaml'
    guardar_proyecto(p, path)
    q = cargar_proyecto(path)
    assert q.metodo_calculo == 'froehlich'
    assert q.estribo_izquierdo.q500.radio_hidraulico == 1.2
    assert q.estribo_izquierdo.q500.Q_ll is None
    assert q.estribo_izquierdo.D50_mm is None
    assert ejecutar(p).caudales == ejecutar(q).caudales


def test_exportaciones_sin_ll_ni_total_ficticio(tmp_path):
    destino = tmp_path/'f.md'
    word = tmp_path/'f.docx'
    r = runner.invoke(app, ['calc', '--demo', '--quiet', '--export', str(destino), '--word', str(word)])
    assert r.exit_code == 0, r.output
    texto = destino.read_text(encoding='utf-8')
    assert 'R_informativo' in texto and 'F92' in texto
    assert 'LL59' not in texto and 'CSU81' not in texto
    j = json.loads(destino.with_suffix('.auditoria.json').read_text(encoding='utf-8'))
    assert j['caudales'][0]['estribos'][0]['y_s_total'] is None
    from docx import Document
    d = Document(word)
    contenido = '\n'.join(x.text for x in d.paragraphs)
    assert 'Froehlich' in contenido and 'R_informativo' in contenido
    assert 'Lischtvan' not in contenido and 'LL59' not in contenido


def test_completar_nuevo_formato_conserva_original_y_no_pide_ll(tmp_path):
    path = tmp_path/'entrada.yaml'
    guardar_proyecto(datos_prueba_froehlich(), path)
    original = path.read_bytes()
    r = runner.invoke(app, ['completar', str(path), '--quiet', '--export', str(tmp_path/'c.md')], input='\n'*60)
    assert r.exit_code == 0, r.output
    assert path.read_bytes() == original
    assert 'beta' not in r.output and 'Número de pilares' not in r.output
    assert cargar_proyecto(path.with_stem('entrada_completado')).metodo_calculo == 'froehlich'


def test_desbordamiento_gobierna_por_socavacion_no_por_Q():
    p = datos_prueba_froehlich()
    p.Q_ot, p.T_ot = 40, 50
    for e in p.estribos():
        e.qot = hidraulica_froehlich(Q=40, A=5, Ae=1, Qe=18, L=8)
    r = ejecutar(p)
    assert all(e.escenario_diseno == 'Qot' and e.escenario_verificacion == 'Qot' for e in r.estribos_finales)
