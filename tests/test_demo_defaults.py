"""Datos precargados: Enter, ejecución automática y separación de datos reales."""
import json
from pathlib import Path
import pytest
from typer.testing import CliRunner
from socavacion.cli.app import app
from socavacion.input.demo import cargar_datos_prueba
from socavacion.input.validator import validar_proyecto
from socavacion.input.loader import cargar_proyecto, guardar_proyecto

runner = CliRunner()


def test_demo_completo_no_genera_cascada_de_pendientes():
    p=cargar_datos_prueba()
    avisos=validar_proyecto(p)
    assert len(avisos)==1
    assert 'DATOS DE PRUEBA' in avisos[0]
    assert p.modo=='preliminar'
    assert p.estribo_izquierdo.q500.Dm_mm==2.95
    assert p.estribo_derecho.q100.Qe>0
    assert len(p.pilares)==1


def test_demo_automatico_sin_preguntas_ni_dialogo(tmp_path,monkeypatch):
    def no_dialogo(*args,**kwargs):
        pytest.fail('Una prueba rápida no debe abrir diálogo Word')
    monkeypatch.setattr('socavacion.cli.app.generate_socavacion_docx_with_dialog',no_dialogo)
    destino=tmp_path/'demo.md'
    result=runner.invoke(app,['calc','--demo','--export',str(destino)])
    assert result.exit_code==0,result.output
    assert 'DATOS DE PRUEBA' in result.output
    assert 'falta dato explícito' not in result.output
    registro=json.loads(destino.with_suffix('.auditoria.json').read_text(encoding='utf-8'))
    assert registro['auditoria']['entrada']['datos_prueba'] is True


def test_formulario_precargado_acepta_solo_enter(tmp_path):
    destino=tmp_path/'enter.md'
    result=runner.invoke(app,['calc','--ejemplo','--quiet','--export',str(destino)],input='\n'*250)
    assert result.exit_code==0,result.output
    assert '[55.778]' in result.output
    registro=json.loads(destino.with_suffix('.auditoria.json').read_text(encoding='utf-8'))
    assert registro['auditoria']['entrada']['datos_prueba'] is True
    assert registro['Q_verif']==87.392412


def test_marca_prueba_se_conserva_al_guardar(tmp_path):
    p=cargar_datos_prueba()
    path=tmp_path/'demo.yaml'
    guardar_proyecto(p,path)
    assert cargar_proyecto(path).datos_prueba
    p.modo='trazable'
    with pytest.raises(ValueError,match='datos_prueba'):
        validar_proyecto(p)


@pytest.mark.parametrize('args',[
    ['calc','--demo','--ejemplo'],
    ['calc','proyecto_real.yaml','--demo'],
    ['calc','proyecto_real.yaml','--ejemplo'],
])
def test_no_mezcla_pruebas_con_entradas_reales(args):
    result=runner.invoke(app,args)
    assert result.exit_code==2
    assert 'No se completó' in result.output


def test_cada_demo_es_independiente():
    a=cargar_datos_prueba()
    a.estribo_izquierdo.q100.beta=99
    b=cargar_datos_prueba()
    assert b.estribo_izquierdo.q100.beta==1


@pytest.mark.parametrize('comando',[[],['ingresar'],['calc'],['wizard']])
def test_ingreso_normal_muestra_valores_y_acepta_enter(tmp_path,monkeypatch,comando):
    monkeypatch.chdir(tmp_path)
    result=runner.invoke(app,comando,input='\n'*250)
    assert result.exit_code==0,result.output
    assert 'Q100 (m³/s) [55.778]' in result.output
    assert 'Q500 (m³/s) [87.392412]' in result.output
    assert 'Ingrese un número' not in result.output
    assert 'DATOS DE PRUEBA' in result.output


def test_se_puede_modificar_un_valor_mostrado(tmp_path):
    destino=tmp_path/'editado.md'
    # Nombre, confirmación de sección rectangular, Q100, Q500.
    entrada='\n'*2+'60\n90\n'+'\n'*245
    result=runner.invoke(app,['calc','--quiet','--export',str(destino)],input=entrada)
    assert result.exit_code==0,result.output
    registro=json.loads(destino.with_suffix('.auditoria.json').read_text(encoding='utf-8'))
    assert registro['Q_diseno']==60
    assert registro['Q_verif']==90


def test_no_mezcla_en_blanco_con_ejemplo():
    result=runner.invoke(app,['calc','--en-blanco','--ejemplo'])
    assert result.exit_code==2
