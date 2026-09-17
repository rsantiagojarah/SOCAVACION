"""Pruebas de terminal reales: respuestas por stdin, no sólo modelos prefabricados."""
import json
from pathlib import Path
import pytest
from typer.testing import CliRunner

from socavacion.cli.app import app
from socavacion.domain.observations import resumir_advertencias
from socavacion.input.loader import cargar_proyecto, guardar_proyecto
from socavacion.input.prompts import numero, opcion
from socavacion.input.validator import validar_proyecto
from socavacion.input.wizard_hydraulics import leer_hidraulica
from test_froehlich_hec_ras import respuestas_froehlich

ROOT=Path(__file__).resolve().parents[1]
runner=CliRunner()


def respuestas_hid(Q, *, metodo='froehlich', tabla=False, alpha=False, pendientes=False):
    # Hidráulica básica y cinco coeficientes/tirantes de LL.
    out=['1','4','20','15','1','0,002']
    out+=['','','','',''] if pendientes else ['2,95','1','1,05','1','0,38']
    out+=['externo','4'] if alpha else ['seccion',str(Q),'20','1']
    out+=['tabla','12,5','4'] if tabla else ['manual','' if pendientes else '0,9']
    if metodo=='froehlich':
        out+=['2','2','' if pendientes else '5']
    elif metodo=='hire':
        out+=['30','1','2']
    out+=['']*9 if pendientes else ['Informe de ensayo, sección 1']*9
    return out


def respuestas_proyecto(path, *, modo='trazable', ot=False, pilares=True, pendientes=False):
    caudales=[80,100]+([60] if ot else [])
    out=[modo,'Prueba formulario','granular','libre','y','80','100']
    out+=['60','50'] if ot else ['', '' if pendientes else 'Rasante no rebasada, modelo sección 2']
    out+=['']*4 if pendientes else ['Estudio de ensayo, sección 1']*4
    out+=['estable','0','']
    for _ in range(2):
        out+=['2,95','100','muro_vertical','90','2','froehlich']
        for Q in caudales:
            out+=respuestas_hid(Q,pendientes=pendientes)
    out+=['1' if pilares else '0']
    if pilares:
        out+=['P1','2,95','100','1','circular','10','3','1,1','1']
        for Q in caudales:
            out+=respuestas_hid(Q,metodo='csu',tabla=True,alpha=True)
    out+=['80','y','n','superficial','Grava de ensayo',str(path)]
    return '\n'.join(out)+'\n'


@pytest.mark.parametrize('ot',[False,True])
def test_ingreso_real_trazable_y_exportacion(tmp_path,ot):
    entrada=tmp_path/'nuevo.yaml'
    reporte=tmp_path/'nuevo.md'
    result=runner.invoke(app,['calc','--avanzado','--en-blanco','--quiet','--export',str(reporte)],
                         input=respuestas_froehlich(entrada,ot=ot))
    assert result.exit_code==0, result.output
    proyecto=cargar_proyecto(entrada)
    assert proyecto.modo=='trazable'
    assert len(validar_proyecto(proyecto))==1  # Aviso de alcance parcial, sin faltantes.
    assert proyecto.estribo_izquierdo.q100.Qe==5
    assert not proyecto.pilares
    assert proyecto.metodo_calculo=='froehlich'
    assert 'mu' not in proyecto.estribo_izquierdo.q100.model_fields_set
    registro=json.loads(reporte.with_suffix('.auditoria.json').read_text(encoding='utf-8'))
    assert len(registro['caudales'])==(3 if ot else 2)
    if ot:
        assert proyecto.T_ot==50
        assert proyecto.estribo_derecho.qot.Qe==5
        assert proyecto.estribo_derecho.qot.radio_hidraulico==1.2


def test_preliminar_deja_pendientes_sin_inventar_fuentes(tmp_path):
    entrada=tmp_path/'pendiente.yaml'
    result=runner.invoke(app,['calc','--avanzado','--en-blanco','--quiet','--export',str(tmp_path/'pendiente.md')],
                         input=respuestas_froehlich(entrada,modo='preliminar',pendientes=True))
    assert result.exit_code==0, result.output
    proyecto=cargar_proyecto(entrada)
    assert proyecto.fuentes=={}
    assert proyecto.estribo_izquierdo.q100.fuentes=={}
    assert 'beta' not in proyecto.estribo_izquierdo.q100.model_fields_set
    assert proyecto.estribo_izquierdo.q100.Qe == 5
    assert any('fuente' in aviso for aviso in validar_proyecto(proyecto))
    assert not any('beta' in aviso for aviso in validar_proyecto(proyecto))


def test_completar_archivo_real_sin_modificar_original(tmp_path):
    proyecto=cargar_proyecto(ROOT/'ejemplos/puente_mtc_trazable.yaml')
    entrada=tmp_path/'original.yaml'
    guardar_proyecto(proyecto,entrada)
    original=entrada.read_bytes()
    # Todos los valores/fuentes se muestran como valores anteriores a confirmar.
    result=runner.invoke(app,['completar',str(entrada),'--quiet','--export',str(tmp_path/'completado.md')],
                         input='\n'*250)
    assert result.exit_code==0, result.output
    completado=cargar_proyecto(tmp_path/'original_completado.yaml')
    assert validar_proyecto(completado)==[]
    assert entrada.read_bytes()==original
    assert completado.Q500==proyecto.Q500
    assert completado.estribo_derecho.q500.Dm_mm==proyecto.estribo_derecho.q500.Dm_mm


def test_reintentos_numericos_y_coma(monkeypatch):
    answers=iter(['nan','inf','-1','0','abc','1,25'])
    monkeypatch.setattr('typer.prompt',lambda *a,**k:next(answers))
    assert numero('valor',positivo=True,maximo=2)==1.25


def test_reintento_entero_opcion_y_borrado_opcional(monkeypatch):
    answers=iter(['1.5','2','inexistente','trazable','?'])
    monkeypatch.setattr('typer.prompt',lambda *a,**k:next(answers))
    assert numero('cantidad',entero=True,minimo=0)==2
    assert opcion('modo',['preliminar','trazable'],default='preliminar')=='trazable'
    assert numero('Qot',default=50,opcional=True) is None


def test_hire_solicita_hidraulica_al_pie(monkeypatch):
    answers=iter(respuestas_hid(100,metodo='hire'))
    monkeypatch.setattr('typer.prompt',lambda *a,**k:next(answers))
    hid=leer_hidraulica('Q100',100,estricto=True,metodo='hire')
    assert hid.h_pie==1 and hid.V_pie==2 and hid.L_obstruida==30


def test_errores_cli_sin_traceback(tmp_path):
    result=runner.invoke(app,['calc',str(tmp_path/'no_existe.yaml'),'--quiet'])
    assert result.exit_code==2
    assert 'No se completó' in result.output
    assert 'Traceback' not in result.output


def test_avisos_agrupados_deterministas_y_sin_perdidas():
    mensajes=['izquierdo/q100: falta dato explícito beta.',
              'izquierdo/q100: falta dato explícito phi.',
              'izquierdo/q100: falta fuente beta.',
              'Falta fuente del proyecto: hidrologia.',
              'izquierdo/q100: Qe no disponible.',
              'derecho/q500: falta fuente local.']
    lineas=resumir_advertencias(mensajes+mensajes)
    assert lineas==resumir_advertencias(list(reversed(mensajes)))
    assert lineas.count('  izquierdo/q100:')==1
    assert '    Datos pendientes: beta, phi.' in lineas
    assert '    Fuentes pendientes: beta.' in lineas
    assert any('Qe no disponible' in s for s in lineas)


def test_no_sobrescribe_yaml_sin_confirmacion(tmp_path):
    destino=tmp_path/'protegido.yaml'
    destino.write_text('contenido del usuario',encoding='utf-8')
    respuestas=respuestas_froehlich(destino)+'n\n'
    result=runner.invoke(app,['calc','--avanzado','--en-blanco','--quiet','--export',str(tmp_path/'salida.md')],input=respuestas)
    assert result.exit_code==0,result.output
    assert destino.read_text(encoding='utf-8')=='contenido del usuario'


def test_completar_entrada_antigua_con_datos_y_fuentes_nuevos(tmp_path):
    proyecto=cargar_proyecto(ROOT/'ejemplos/puente_ejemplo.yaml')
    entrada=tmp_path/'antiguo.yaml'
    guardar_proyecto(proyecto,entrada)
    original=entrada.read_bytes()
    # El comando proporciona ya el destino: no hay pregunta de guardado al final.
    respuestas=respuestas_proyecto('IGNORADO',pilares=False).splitlines()[:-1]
    result=runner.invoke(app,['completar',str(entrada),'--quiet','--export',str(tmp_path/'actualizado.md')],
                         input='\n'.join(respuestas)+'\n')
    assert result.exit_code==0,result.output
    completo=cargar_proyecto(tmp_path/'antiguo_completado.yaml')
    assert validar_proyecto(completo)==[]
    assert completo.modo=='trazable'
    assert completo.estribo_izquierdo.q100.Qe==5
    assert entrada.read_bytes()==original


def test_hipotesis_del_metodo_no_se_presentan_como_campos_faltantes(capsys):
    from socavacion.core.pipeline import ejecutar
    from socavacion.cli.display import mostrar_resultados
    p=cargar_proyecto(ROOT/'ejemplos/puente_mtc_trazable.yaml')
    mostrar_resultados(ejecutar(p))
    salida=capsys.readouterr().out
    assert 'Hipótesis del método' in salida
    assert 'Advertencias (agrupadas' not in salida
    assert 'CSU sin truncamiento' in salida


def test_campo_trazable_no_admite_omision(monkeypatch):
    from socavacion.input.prompts import texto
    answers=iter(['','?','Informe H-01, página 5'])
    monkeypatch.setattr('typer.prompt',lambda *a,**k:next(answers))
    assert texto('Fuente beta',requerido=True)=='Informe H-01, página 5'


def test_error_de_formato_no_sustituye_forma_silenciosamente(monkeypatch):
    answers=iter(['noexiste','muro_vertical'])
    monkeypatch.setattr('typer.prompt',lambda *a,**k:next(answers))
    assert opcion('Forma',['muro_vertical','talud_2h1v'],default='muro_vertical')=='muro_vertical'
