"""Un mismo registro de cálculo para Markdown, Word y JSON."""
from dataclasses import asdict
import json
from pathlib import Path
from socavacion.normative.references import REFERENCIAS


def componentes(resultado):
    for c in resultado.caudales:
        for e in c.estribos:
            nombre = f'{c.escenario} / estribo {e.lado.value}'
            if e.general is not None:
                yield nombre, e.general.y_sg_lischtvan
            if e.y_sc is not None:
                yield nombre, e.y_sc
            yield nombre, e.y_sl
        for p in c.pilares:
            nombre = f'{c.escenario} / pilar {p.nombre}'
            yield nombre, p.general.y_sg_lischtvan
            yield nombre, p.y_sp


def lineas_componente(comp):
    out = [comp.metodo, comp.formula]
    for k, valor in comp.intermedios.items():
        out.append(f'{k} = {valor:.10g} {comp.unidades.get(k, "")}')
    out.append(f'Resultado = {comp.valor:.10g} m')
    out += [f'Referencia {r}: {REFERENCIAS[r]}' for r in comp.referencias]
    out += [f'Dato {k}: {v}' for k, v in comp.fuentes_datos.items()]
    out += [f'Supuesto: {s}' for s in comp.supuestos]
    if comp.notas:
        out.append(comp.notas)
    return out


def anexo_markdown(resultado):
    out = ['\n\n## Registro trazable', '',
           f"Versión: {resultado.auditoria['version_metodo']}. Modo: {resultado.auditoria['modo']}.",
           f"SHA256 entrada: `{resultado.auditoria['entrada_sha256']}`.",
           f"SHA256 código: `{resultado.auditoria['fuente_codigo_sha256']}`.",
           resultado.auditoria['alcance'], '', '### Fuentes contrastadas', '']
    for clave, d in resultado.auditoria['documentos'].items():
        out += [f"{clave}: {d['archivo']}; SHA256 `{d['sha256_actual']}`; coincide: {d['coincide']}.", '']
    out += ['### Observaciones y datos pendientes', '']
    if not resultado.advertencias_globales:
        out += ['Sin campos pendientes detectados; esto no valida la evidencia ni elimina los supuestos de cada componente.', '']
    out += [f'- {a}' for a in dict.fromkeys(resultado.advertencias_globales)]
    for nombre, comp in componentes(resultado):
        out += ['', f'### {nombre}: {comp.metodo}', '']
        out += [line + '  ' for line in lineas_componente(comp)]
    out += ['', '### Entradas reproducibles (JSON)', '', '```json',
            json.dumps(resultado.auditoria['entrada'], ensure_ascii=False, indent=2, allow_nan=False), '```']
    return '\n'.join(out) + '\n'


def guardar_auditoria(resultado, ruta):
    path = Path(ruta).with_suffix('.auditoria.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(resultado), ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    return path
