"""Lecturas de terminal: reintentos locales y ausencia explícita de información."""
import math
import typer


def texto(etiqueta, *, default='', requerido=True):
    while True:
        valor = typer.prompt(etiqueta, default=default, show_default=bool(default)).strip()
        if valor == '?':
            valor = ''
        if valor or not requerido:
            return valor
        typer.echo('Este campo es necesario. Use modo preliminar si aún no dispone de fuentes.')


def numero(etiqueta, *, default=None, opcional=False, minimo=None, maximo=None,
           positivo=False, entero=False):
    """Enter sólo adopta un valor mostrado o deja un opcional sin registrar."""
    while True:
        raw = typer.prompt(etiqueta + (' (Enter: pendiente)' if opcional and default is None else ''),
                           default='' if default is None else str(default), show_default=default is not None)
        if (not raw.strip() or raw.strip() == '?') and opcional:
            return None
        try:
            valor = float(raw.strip().replace(',', '.'))
        except ValueError:
            typer.echo('Ingrese un número; se acepta punto o coma decimal, sin separadores de miles.')
            continue
        if (not math.isfinite(valor) or (positivo and valor <= 0)
                or (minimo is not None and valor < minimo)
                or (maximo is not None and valor > maximo)
                or (entero and not valor.is_integer())):
            typer.echo(f'Valor fuera de rango: finito{", > 0" if positivo else ""}'
                       f'{f", >= {minimo}" if minimo is not None else ""}'
                       f'{f", <= {maximo}" if maximo is not None else ""}'
                       f'{", entero" if entero else ""}. Intente de nuevo.')
            continue
        return int(valor) if entero else valor


def opcion(etiqueta, opciones, *, default):
    while True:
        valor = texto(f'{etiqueta} ({" / ".join(opciones)})', default=default).lower()
        if valor in opciones:
            return valor
        typer.echo('Opción no reconocida. No se sustituirá automáticamente.')


def fuentes(campos, *, estricto, anteriores=None):
    anteriores = anteriores or {}
    salida = dict(anteriores)
    typer.echo('Fuentes: indique informe/ensayo/plano y página o sección; no invente referencias.')
    for campo in campos:
        valor = texto(f'Fuente {campo}', default=anteriores.get(campo, ''), requerido=estricto)
        if valor:
            salida[campo] = valor
        else:
            salida.pop(campo, None)
    return salida
