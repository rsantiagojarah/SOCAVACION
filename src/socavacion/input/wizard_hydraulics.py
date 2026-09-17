"""Formulario hidráulico completo por apoyo y avenida, sin datos ficticios."""
import typer
from socavacion.domain.models import CondicionHidraulica
from socavacion.input.prompts import numero, opcion, fuentes


def leer_hidraulica(etiqueta, Q, *, estricto, metodo='froehlich', base=None,
                    L_base=None, Ae_base=None):
    typer.echo(f'\n--- {etiqueta}: Q total = {Q:g} m³/s ---')
    # No convertir los valores por defecto de un modelo antiguo en datos confirmados.
    previo = base.model_dump(exclude_unset=True) if base is not None else {}
    datos = dict(previo)

    def pedir(campo, label, *, necesario=True, fallback=None, **limites):
        valor = numero(f'{campo} — {label}', default=previo.get(campo, fallback),
                       opcional=not necesario, **limites)
        if valor is None:
            datos.pop(campo, None)
        else:
            datos[campo] = valor
        return valor

    for campo, label in [('y1','tirante aguas arriba (m)'), ('V1','velocidad aguas arriba (m/s)'),
                         ('W1','ancho de sección aguas arriba (m)'), ('W2','ancho hidráulico bajo puente (m)'),
                         ('y0','tirante bajo puente antes de socavación (m)'), ('Sf','pendiente de energía (m/m)')]:
        pedir(campo, label, positivo=campo not in ('V1','Sf'), minimo=0)
    typer.echo('LL: Dm no se identifica automáticamente con D50. En preliminar, Enter deja pendientes los parámetros desconocidos.')
    for campo, label, limites in [
        ('Dm_mm','diámetro característico del lecho (mm)', {'positivo':True}),
        ('h_local','tirante original de la franja/apoyo (m)', {'positivo':True}),
        ('beta','coeficiente de frecuencia sustentado', {'positivo':True}),
        ('phi','factor de transporte sustentado', {'minimo':1}),
        ('exponente_x','z granular, nombre histórico x', {'positivo':True}),
    ]:
        pedir(campo, label, necesario=estricto, **limites)
    cierre = opcion('Coeficiente alpha LL', ['seccion','externo'],
                    default='externo' if previo.get('alpha') is not None else 'seccion')
    if cierre == 'seccion':
        datos.pop('alpha', None)
        for campo, label in [('Q_ll','caudal de la sección LL (m³/s)'), ('B_ll','ancho de esa sección (m)'),
                             ('h_m_ll','tirante medio de esa sección (m)')]:
            pedir(campo,label,necesario=estricto,positivo=True, maximo=Q if campo=='Q_ll' else None)
    else:
        pedir('alpha','coeficiente externo SIN mu incorporado', positivo=True)
        for campo in ('Q_ll','B_ll','h_m_ll'):
            datos.pop(campo, None)
    contraccion = opcion('Factor mu', ['tabla','manual'], default='tabla' if previo.get('luz_libre') is not None else 'manual')
    if contraccion == 'tabla':
        datos.pop('mu', None)
        pedir('luz_libre','luz mínima entre apoyos, NO ancho total (m)', minimo=10,maximo=200)
        pedir('V_mu','velocidad media de sección para Tabla 13 (m/s)',minimo=0)
    else:
        datos.pop('luz_libre', None)
        datos.pop('V_mu', None)
        pedir('mu','factor externo sustentado (0 < mu <= 1)', necesario=estricto,positivo=True,maximo=1)
    if metodo == 'froehlich':
        typer.echo('Froehlich: Qe es el flujo obstruido por ESTE estribo; no el caudal Q1 del río.')
        for campo in ('h_pie','V_pie'):
            datos.pop(campo,None)
        pedir('L_obstruida','longitud proyectada normal al flujo (m)', positivo=True, fallback=L_base)
        pedir('Ae','área obstruida por este estribo en esta avenida (m²)',positivo=True,
              necesario=estricto, fallback=Ae_base if Ae_base and Ae_base>0 else None)
        pedir('Qe','caudal obstruido por este estribo (m³/s)',positivo=True,maximo=Q,necesario=estricto)
    elif metodo == 'hire':
        for campo in ('Ae','Qe'):
            datos.pop(campo,None)
        L = pedir('L_obstruida','longitud proyectada normal al flujo (m)',positivo=True,fallback=L_base)
        while True:
            h = pedir('h_pie','tirante al pie del estribo (m)',positivo=True)
            if L/h > 25:
                break
            typer.echo('HIRE requiere L/h_pie > 25 en este motor. Corrija datos reales o cambie de método; no ajuste valores para forzar cumplimiento.')
            if not typer.confirm('¿Desea corregir L y h_pie?',default=False):
                raise typer.Abort()
            L = pedir('L_obstruida','longitud proyectada normal al flujo (m)',positivo=True)
        pedir('V_pie','velocidad al pie (m/s)',minimo=0)
    else:
        typer.echo('CSU: y1 y V1 deben representar el flujo directamente aguas arriba del pilar.')
    campos = ['hidraulica','granulometria','beta','exponente_x','phi','geometria',
              'luz_libre' if contraccion=='tabla' else 'mu',
              'alpha' if cierre=='externo' else 'cierre_alpha',
              'pilar' if metodo=='csu' else 'local']
    datos['fuentes'] = fuentes(campos,estricto=estricto,anteriores=previo.get('fuentes'))
    hid = CondicionHidraulica.model_validate(datos)
    # Q1/Q2 históricos sólo se resuelven para el evento actual; Qe es independiente.
    hid.resolver_q(Q)
    return hid
