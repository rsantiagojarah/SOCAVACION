"""Formulario reducido: Froehlich con resultados HEC-RAS ingresados manualmente."""
import typer
from socavacion.domain.enums import FormaEstribo
from socavacion.domain.models import Proyecto, Estribo, DatosGeotecnia
from socavacion.input.prompts import numero, texto, opcion
from socavacion.input.hec_ras import hidraulica_froehlich, validar_froehlich, ALCANCE


def datos_prueba_froehlich():
    """Caso sintético asimétrico; no deriva Qe ni Ae de geometría rectangular."""
    fuente = 'EX-F: ejemplo sintético de software; NO resultado de un modelo HEC-RAS real'
    fuentes = dict(hidraulica=fuente, geometria=fuente, local=fuente)
    estribos = []
    for lado, forma, angulo, valores in [
        ('izquierdo', 'muro_vertical', 90, [(3.0, 8.0, 2.0), (4.5, 13.0, 2.5)]),
        ('derecho', 'muro_vertical_aletas_45', 80, [(2.2, 5.0, 1.8), (3.2, 9.0, 2.0)]),
    ]:
        condiciones = {}
        for evento, Q, A, R, (Ae, Qe, L) in zip(
            ['q100', 'q500'], [55.778, 87.392412], [18.0, 28.0], [0.9, 1.2], valores
        ):
            condiciones[evento] = hidraulica_froehlich(Q=Q, A=A, R=R, Ae=Ae, Qe=Qe, L=L, fuentes=fuentes)
        estribos.append(Estribo(lado=lado, forma=forma, angulo_ataque=angulo,
                               L_prima=valores[0][2], Ae=valores[0][0], **condiciones))
    return Proyecto(nombre='Demo', Q100=55.778, Q500=87.392412, datos_prueba=True,
        metodo_calculo='froehlich', entrada_hidraulica='hec_ras',
        estribo_izquierdo=estribos[0], estribo_derecho=estribos[1],
        geotecnia=DatosGeotecnia(evaluar=False, hay_estrato_competente=False),
        fuentes={'hidrologia': fuente},
        justificacion_sin_desbordamiento='EX-F: se omite sólo en esta prueba de software; no es justificación de proyecto.')


def ejecutar_froehlich(base=None, salida=None, avanzado=False):
    def dato(obj, campo, default=None):
        return getattr(obj, campo, default) if obj is not None else default
    prueba = bool(base and base.datos_prueba)
    typer.echo('\nFROEHLICH — SÓLO ESTRIBOS. Datos manuales de HEC-RAS, sin franjas ni sección rectangular.\n'
               'A y R corresponden a la sección total de aproximación; Ae/Qe/L al flujo obstruido por CADA estribo.\n'
               'Ae no es el área total y Qe no es Q total. R es opcional e informativo.\n'
               'Kf se obtiene por forma (Tabla 27) y Ktheta por ángulo (ec.93).\n' + ALCANCE)
    if prueba:
        typer.echo('DATOS DE PRUEBA: Enter acepta los valores sintéticos mostrados; no son datos de campo.')
    nombre = texto('Nombre del proyecto', default=dato(base, 'nombre', ''))
    if not typer.confirm('¿Confirma flujo libre de agua en lecho granular homogéneo, sin presión ni huayco/detritos?', default=base is not None and base.flujo == 'libre' and base.material_lecho == 'granular' and base.lecho_homogeneo):
        raise ValueError('El método no aplica sin confirmar las condiciones de alcance; revisar el estudio hidráulico.')
    q100 = numero('Q100 (m³/s)', default=dato(base, 'Q100'), positivo=True)
    q500 = numero('Q500 (m³/s)', default=dato(base, 'Q500'), positivo=True, minimo=q100)
    qot = numero('Q desbordamiento (m³/s)', default=dato(base, 'Q_ot'), positivo=True, opcional=True)
    tot = numero('T desbordamiento (años)', default=dato(base, 'T_ot'), positivo=True, maximo=500) if qot is not None else None
    eventos = [('q100', q100), ('q500', q500)] + ([('qot', qot)] if qot is not None else [])
    modo = dato(base, 'modo', 'preliminar')
    if avanzado and not prueba:
        modo = opcion('Modo', ['preliminar', 'trazable'], default=modo)
    secciones = {}
    for evento, Q in eventos:
        anterior = dato(dato(base, 'estribo_izquierdo'), evento)
        A = numero(f'{evento}: área hidráulica TOTAL activa A (m²)', default=dato(anterior, 'area_hidraulica'), positivo=True)
        R = numero(f'{evento}: radio hidráulico R (m, sólo registro)', default=dato(anterior, 'radio_hidraulico'), positivo=True, opcional=True)
        secciones[evento] = (A, R)
        typer.echo(f'  Velocidad media de sección Q/A = {Q/A:.4f} m/s (no sustituye Ve).')
    estribos = []
    for lado in ('izquierdo', 'derecho'):
        anterior = dato(base, 'estribo_' + lado)
        typer.echo(f'\nEstribo {lado}: datos de la zona obstruida aguas arriba.')
        forma_base = dato(anterior, 'forma')
        forma = opcion('Forma', [f.value for f in FormaEstribo], default=forma_base.value if forma_base else 'muro_vertical')
        theta = numero('Ángulo theta (grados; 90=normal al flujo)', default=dato(anterior, 'angulo_ataque', 90), positivo=True, maximo=180)
        condiciones = {}
        for evento, Q in eventos:
            hprev = dato(anterior, evento)
            A, R = secciones[evento]
            L = numero(f'{lado}/{evento}: longitud obstruida proyectada L (m)', default=dato(hprev, 'L_obstruida'), positivo=True)
            Ae = numero(f'{lado}/{evento}: área OBSTRUIDA Ae (m²)', default=dato(hprev, 'Ae'), positivo=True, maximo=A)
            Qe = numero(f'{lado}/{evento}: caudal OBSTRUIDO Qe (m³/s)', default=dato(hprev, 'Qe'), positivo=True, maximo=Q)
            condiciones[evento] = hidraulica_froehlich(Q=Q, A=A, R=R, Ae=Ae, Qe=Qe, L=L)
        estribos.append(Estribo(lado=lado, forma=forma, angulo_ataque=theta,
                               L_prima=condiciones['q100'].L_obstruida, Ae=condiciones['q100'].Ae, **condiciones))
    fuente_previa = dato(base, 'fuentes', {}).get('hidrologia', '')
    fuente = texto('Fuente hidráulica (modelo/plan HEC-RAS, River/Reach, RS, perfiles; Q, A, R y Ae/Qe)',
                   default=fuente_previa, requerido=modo == 'trazable')
    geometria_previa = base.estribo_izquierdo.q100.fuentes.get('geometria', '') if base else ''
    geometria = texto('Fuente geometría (plano/sección, L, forma y ángulo de cada estribo)',
                      default=geometria_previa, requerido=modo == 'trazable')
    justificacion = texto('Justificación de no evaluar desbordamiento',
                         default=dato(base, 'justificacion_sin_desbordamiento', ''),
                         requerido=modo == 'trazable') if qot is None else ''
    for e in estribos:
        for evento, _ in eventos:
            getattr(e, evento).fuentes = {k:v for k,v in dict(hidraulica=fuente, local=fuente, geometria=geometria).items() if v}
    proyecto = Proyecto(nombre=nombre, Q100=q100, Q500=q500, Q_ot=qot, T_ot=tot,
        modo=modo, datos_prueba=prueba, metodo_calculo='froehlich', entrada_hidraulica='hec_ras',
        estribo_izquierdo=estribos[0], estribo_derecho=estribos[1],
        geotecnia=DatosGeotecnia(evaluar=False, hay_estrato_competente=False),
        fuentes={'hidrologia': fuente} if fuente else {}, justificacion_sin_desbordamiento=justificacion)
    validar_froehlich(proyecto)
    if salida is None:
        salida = texto('Guardar entrada YAML (ruta; Enter para no guardar)', requerido=False) or None
    if salida is not None:
        from socavacion.input.wizard import _guardar
        _guardar(proyecto, salida)
    return proyecto
