"""Presentación determinista y compacta; conserva todos los avisos originales."""
import re


def resumir_advertencias(advertencias):
    grupos = {}
    for aviso in dict.fromkeys(advertencias):
        match = re.match(r'^(.+/(?:q100|q500|qot)): (.*)$', aviso)
        grupo, mensaje = match.groups() if match else ('Proyecto / generales', aviso)
        entrada = grupos.setdefault(grupo, {'datos':[], 'fuentes':[], 'otros':[]})
        if mensaje.startswith('falta dato explícito '):
            entrada['datos'].append(mensaje.removeprefix('falta dato explícito ').rstrip('.'))
        elif mensaje.startswith('falta fuente '):
            entrada['fuentes'].append(mensaje.removeprefix('falta fuente ').rstrip('.'))
        elif mensaje.startswith('Falta fuente del proyecto: '):
            entrada['fuentes'].append(mensaje.removeprefix('Falta fuente del proyecto: ').rstrip('.'))
        else:
            entrada['otros'].append(mensaje)
    out = []
    for grupo in sorted(grupos, key=lambda k:(k!='Proyecto / generales', k)):
        entrada=grupos[grupo]
        out.append(f'  {grupo}:')
        if entrada['datos']:
            out.append('    Datos pendientes: ' + ', '.join(sorted(set(entrada['datos']))) + '.')
        if entrada['fuentes']:
            out.append('    Fuentes pendientes: ' + ', '.join(sorted(set(entrada['fuentes']))) + '.')
        out.extend('    • '+s for s in sorted(set(entrada['otros'])))
    return out
