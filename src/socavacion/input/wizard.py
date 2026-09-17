"""Ingreso completo y edición asistida de proyectos preliminares/trazables."""
from pathlib import Path
import typer
from socavacion.domain.enums import FormaEstribo, FormaPilar, TipoCimentacion
from socavacion.domain.models import Proyecto, Estribo, Pilar, DatosGeotecnia, ClasificacionCauce
from socavacion.input.loader import guardar_proyecto
from socavacion.input.prompts import numero, texto, opcion, fuentes
from socavacion.input.wizard_hydraulics import leer_hidraulica
from socavacion.input.validator import validar_proyecto
from socavacion.input.demo import cargar_datos_prueba

_USE_DEFAULTS = False

def set_use_defaults(enabled=True):
    global _USE_DEFAULTS
    _USE_DEFAULTS = enabled

def get_use_defaults():
    return _USE_DEFAULTS

def _leer_float(prompt, default=None, *, minimo=None):
    if _USE_DEFAULTS and default is not None:
        return default
    return numero(prompt, default=default, minimo=minimo)

def _dato(base, campo, default=None):
    if base is None:
        return default
    valor = getattr(base, campo, default)
    return valor.value if hasattr(valor, 'value') else valor

def _eventos(apoyo, eventos, estricto, metodo, L=None, Ae=None):
    return {campo: leer_hidraulica(
        f'{getattr(apoyo, "nombre", "")} {etiqueta}'.strip(), Q,
        estricto=estricto, metodo=metodo, base=getattr(apoyo,campo,None),
        L_base=L, Ae_base=Ae)
        for campo, etiqueta, Q in eventos}

def _leer_estribo(lado, eventos, estricto, base=None):
    typer.echo(f'\n=== Estribo {lado} ===')
    datos=base.model_dump(exclude_unset=True) if base else {}
    datos.update(lado=lado)
    datos['D50_mm']=numero('D50 del estribo (mm)',default=_dato(base,'D50_mm'),positivo=True)
    datos['Z_lecho']=numero('Cota lecho del estribo (m s.n.m.)',default=_dato(base,'Z_lecho'))
    datos['forma']=opcion('Forma estribo',[f.value for f in FormaEstribo],default=_dato(base,'forma','muro_vertical'))
    datos['angulo_ataque']=numero('Ángulo del estribo (90 = normal al flujo)',default=_dato(base,'angulo_ataque',90),positivo=True,maximo=180)
    datos['L_prima']=numero('Longitud obstruida de referencia L (m)',default=_dato(base,'L_prima'),positivo=True)
    datos['metodo_local']=opcion('Método local estribo',['froehlich','hire'],default=_dato(base,'metodo_local','froehlich'))
    if datos['metodo_local']=='hire':
        datos['penetra_cauce']=typer.confirm('¿El estribo penetra en el cauce principal?',default=_dato(base,'penetra_cauce',False))
        if not datos['penetra_cauce']:
            typer.echo('HIRE no aplica sin penetración en el cauce principal; se solicitarán datos de Froehlich.')
            datos['metodo_local']='froehlich'
    datos.setdefault('Ae',0.0)  # Ae efectivo se pide por avenida; cero NO representa un estudio.
    datos.pop('qot',None)
    datos.update(_eventos(base,eventos,estricto,datos['metodo_local'],datos['L_prima'],_dato(base,'Ae')))
    return Estribo.model_validate(datos)

def _leer_pilar(indice, eventos, estricto, nombres, base=None):
    typer.echo(f'\n=== Pilar {indice} ===')
    datos=base.model_dump(exclude_unset=True) if base else {}
    while True:
        nombre=texto('Nombre del pilar',default=_dato(base,'nombre',f'P{indice}'))
        if nombre not in nombres:
            break
        typer.echo('Nombre ya utilizado; identifique cada pilar de forma única.')
    datos['nombre']=nombre
    datos['D50_mm']=numero('D50 del pilar (mm)',default=_dato(base,'D50_mm'),positivo=True)
    datos['Z_lecho']=numero('Cota lecho del pilar (m s.n.m.)',default=_dato(base,'Z_lecho'))
    datos['ancho_a']=numero('Ancho real a del pilar (m)',default=_dato(base,'ancho_a'),positivo=True)
    datos['forma']=opcion('Forma pilar',[f.value for f in FormaPilar],default=_dato(base,'forma','circular'))
    datos['angulo_ataque']=numero('Ángulo del pilar (0 = alineado)',default=_dato(base,'angulo_ataque',0),minimo=0,maximo=180)
    datos['longitud_l']=numero('Longitud real l del pilar (m)',default=_dato(base,'longitud_l'),
                               minimo=datos['ancho_a'],opcional=datos['angulo_ataque'] in (0,180))
    datos['K3']=numero('K3 según forma del lecho (1.1 a 1.3)',default=_dato(base,'K3',1.1),minimo=1.1,maximo=1.3)
    datos['K4']=numero('K4 (1 = sin reducción por armadura)',default=_dato(base,'K4',1),positivo=True,maximo=1)
    if datos['K4']<1:
        datos['fuente_K4']=texto('Fuente del cálculo de K4 y granulometría',default=_dato(base,'fuente_K4',''))
    datos.pop('qot',None)
    datos.update(_eventos(base,eventos,estricto,'csu'))
    return Pilar.model_validate(datos)

def _leer_geotecnia(estricto, base=None):
    typer.echo('\n--- Geotecnia: controles preliminares ---')
    datos=base.model_dump(exclude_unset=True) if base else {}
    datos['evaluar']=True
    datos['cota_sondaje_min']=numero('Cota fondo sondaje (m s.n.m.)',default=_dato(base,'cota_sondaje_min'))
    datos['hay_estrato_competente']=typer.confirm('¿Hay estrato competente sustentado?',default=_dato(base,'hay_estrato_competente',False))
    datos['roca_resistente']=typer.confirm('¿Roca resistente sustentada?',default=_dato(base,'roca_resistente',False))
    while True:
        tipo=opcion('Tipo cimentación',[t.value for t in TipoCimentacion],default=_dato(base,'tipo_cimentacion','superficial'))
        if tipo!='sobre_roca' or datos['roca_resistente']:
            break
        typer.echo('Sobre roca requiere resistencia a erosión sustentada. Revise el tipo o el estudio.')
    datos['tipo_cimentacion']=tipo
    datos['descripcion_estrato']=texto('Descripción del estrato',default=_dato(base,'descripcion_estrato',''),requerido=estricto)
    for campo,label,aplica in [
        ('Z_punta_pilotes','Cota punta pilotes (m)',tipo in ('profunda','zapata_sobre_pilotes')),
        ('Z_encepado_zapata','Cota cara SUPERIOR del cabezal (m)',tipo=='zapata_sobre_pilotes')]:
        if aplica:
            datos[campo]=numero(label,default=_dato(base,campo),opcional=not estricto)
        else:
            datos.pop(campo,None)
    return DatosGeotecnia.model_validate(datos)

def _guardar(proyecto, salida):
    path=Path(salida)
    if path.suffix.lower() not in ('.yaml','.yml'):
        raise ValueError('El destino del formulario debe ser .yaml o .yml.')
    if path.exists() and not typer.confirm(f'¿Sobrescribir {path}?',default=False):
        typer.echo('No se sobrescribió el archivo; los datos permanecen en esta ejecución.')
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    guardar_proyecto(proyecto,path)
    typer.echo(f'Proyecto guardado en {path}')

def ejecutar_wizard(salida: Path | None = None, use_defaults=False, *, base: Proyecto | None = None, ejemplo=False, en_blanco=False, avanzado=False):
    """Demo aislado; fuera del demo sólo datos ingresados/confirmados por el usuario."""
    global _USE_DEFAULTS
    _USE_DEFAULTS=use_defaults
    if en_blanco and (use_defaults or ejemplo or base is not None):
        raise ValueError('--en-blanco no se combina con demo, ejemplo ni proyecto existente.')
    if (use_defaults and ejemplo) or (base is not None and (use_defaults or ejemplo)):
        raise ValueError('Elija demo automático, formulario de ejemplo o proyecto existente; no mezcle entradas.')
    if use_defaults:
        from socavacion.input.wizard_froehlich import datos_prueba_froehlich
        proyecto=datos_prueba_froehlich()
        typer.echo('Modo demo: datos ilustrativos, NO un proyecto sustentado.')
        if salida is not None:
            _guardar(proyecto,salida)
        return proyecto
    if base is None or base.metodo_calculo == 'froehlich':
        from socavacion.input.wizard_froehlich import ejecutar_froehlich, datos_prueba_froehlich
        return ejecutar_froehlich(base if base is not None else None if en_blanco else datos_prueba_froehlich(), salida, avanzado)
    typer.echo('ARCHIVO HISTÓRICO: se conserva su método completo anterior; no se convierte silenciosamente a Froehlich.')
    if ejemplo or (base is None and not en_blanco):
        base=cargar_datos_prueba()
        typer.echo('FORMULARIO DE PRUEBA: Enter acepta cada valor sintético. Puede modificarlo; seguirá marcado como prueba.')
    typer.echo('Ingreso de datos — método MTC trazable\n'
               'Enter acepta un valor mostrado. En preliminar, Enter sin valor deja un pendiente.\n'
               'Use ? para dejar pendiente un opcional o retirar un valor opcional mostrado.\n'
               'Se acepta coma decimal. No ingrese coeficientes o fuentes ficticios para eliminar avisos.')
    es_prueba=_dato(base,'datos_prueba',False)
    if es_prueba:
        modo='preliminar'
        typer.echo('Modo preliminar de prueba. Para datos reales use --en-blanco o complete su archivo existente.')
    else:
        modo=opcion('Modo',['preliminar','trazable'],default=_dato(base,'modo','preliminar'))
    estricto=modo=='trazable'
    if estricto:
        typer.echo('Modo trazable: datos y fuentes obligatorios. Si aún faltan, use preliminar; Ctrl+C cancela.')
    nombre=texto('Nombre del proyecto',default=_dato(base,'nombre',''))
    material=opcion('Material del lecho',['granular','cohesivo','roca'],default=_dato(base,'material_lecho','granular'))
    flujo=opcion('Flujo',['libre','presion','detritos'],default=_dato(base,'flujo','libre'))
    homogeneo=typer.confirm('¿El lecho se puede modelar como homogéneo?',default=_dato(base,'lecho_homogeneo',True))
    if material!='granular' or flujo!='libre' or not homogeneo:
        raise ValueError('Fuera de alcance: este motor requiere lecho granular homogéneo y flujo libre.')
    Q100=numero('Q100 (m³/s)',default=_dato(base,'Q100'),positivo=True)
    Q500=numero('Q500 (m³/s)',default=_dato(base,'Q500'),positivo=True,minimo=Q100)
    Q_ot=numero('Q desbordamiento (m³/s)',default=_dato(base,'Q_ot'),positivo=True,opcional=True)
    T_ot=numero('T del desbordamiento (años)',default=_dato(base,'T_ot'),positivo=True,maximo=500) if Q_ot is not None else None
    justificacion=texto('Justificación de no evaluar desbordamiento',default=_dato(base,'justificacion_sin_desbordamiento',''),
                        requerido=estricto) if Q_ot is None else ''
    fp=fuentes(['hidrologia','topografia','geotecnia','largo_plazo'],estricto=estricto,anteriores=_dato(base,'fuentes',{}))
    cauce_base=_dato(base,'cauce')
    tipo=opcion('Tipo de cauce',['estable','degradacion','agradacion'],default=_dato(cauce_base,'tipo','estable'))
    lp=numero('Degradación de largo plazo LP (m; negativa para agradación)',default=_dato(cauce_base,'y_sg_lp'))
    cauce=ClasificacionCauce(tipo=tipo,y_sg_lp=lp,notas=texto('Notas morfológicas',default=_dato(cauce_base,'notas',''),requerido=False))
    eventos=[('q100','Q100',Q100),('q500','Q500',Q500)]
    if Q_ot is not None:
        eventos.append(('qot','Qot',Q_ot))
        typer.echo('Se solicitará hidráulica Qot INDEPENDIENTE en todos los apoyos.')
    izq=_leer_estribo('izquierdo',eventos,estricto,_dato(base,'estribo_izquierdo'))
    der=_leer_estribo('derecho',eventos,estricto,_dato(base,'estribo_derecho'))
    anteriores=_dato(base,'pilares',[])
    while True:
        cantidad=numero('Número de pilares intermedios',default=len(anteriores),minimo=0,entero=True)
        if cantidad>=len(anteriores) or typer.confirm('¿Confirma retirar pilares del proyecto editado?',default=False):
            break
    pilares=[]
    for i in range(cantidad):
        pilares.append(_leer_pilar(i+1,eventos,estricto,{p.nombre for p in pilares},anteriores[i] if i<len(anteriores) else None))
    geo=_leer_geotecnia(estricto,_dato(base,'geotecnia'))
    proyecto=Proyecto(nombre=nombre,modo=modo,datos_prueba=es_prueba,material_lecho=material,flujo=flujo,lecho_homogeneo=homogeneo,
                      Q100=Q100,Q500=Q500,Q_ot=Q_ot,T_ot=T_ot,fuentes=fp,
                      justificacion_sin_desbordamiento=justificacion,cauce=cauce,
                      estribo_izquierdo=izq,estribo_derecho=der,pilares=pilares,geotecnia=geo)
    validar_proyecto(proyecto)
    if salida is None:
        destino=texto('Guardar entrada YAML (ruta; Enter para no guardar)',requerido=False)
        salida=Path(destino) if destino else None
    if salida is not None:
        _guardar(proyecto,salida)
    return proyecto
