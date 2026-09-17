"""Identificadores estables, localizadores y huellas de los PDF contrastados."""
from pathlib import Path
import hashlib

VERSION = 'MTC-FROEHLICH-3.0'
DOCUMENTOS = {
    'HHD': {'archivo': 'Manual de hidrologiay drenaje MTC.pdf',
            'sha256': '0a1bdcd7c94016760642de91baf4d6e317e4cc85c529dfefae9a6bf76c8dcd88'},
    'MP': {'archivo': 'Manual de Puentes MTC 2018 (PGA).pdf',
           'sha256': '46d37849141b3acef44bdae112496dafbb5d6813dc008d5495c2f2bb760936b1'},
}
REFERENCIAS = {
    'LL59': 'HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm',
    'MU13': 'HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación',
    'F92': 'HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151',
    'H103': 'HHD §b.3.2.6, ecuación 103, páginas impresas/PDF 156-157',
    'CSU81': 'HHD §b.3.1.10, ecuaciones 81-82, Tablas 20-22, páginas impresas/PDF 136-138; ver discrepancia CSU',
    'CSU_CORRECCION': 'USACE HEC-RAS Hydraulic Reference Manual 4.1, ecuación 10-6: a^0.65*y1^0.35; https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_4.1_Reference_Manual.pdf',
    'CSU_ALCANCE': 'USACE HEC-RAS 6.4, Computing Pier Scour With The CSU Equation: límites restringidos a nariz redonda alineada; este motor conserva resultado sin truncamiento. https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.4/estimating-scour-at-bridges/computing-local-scour-at-piers/computing-pier-scour-with-the-csu-equation',
    'MP123a': 'MP artículo 1.2.3a, página impresa 47 / PDF 51: escenarios y suma por apoyo',
    'MP124': 'MP artículo 1.2.4, páginas impresas 47-48 / PDF 51-52: cimentaciones',
    'MP243834': 'MP artículo 2.4.3.8.3.4, página impresa 104 / PDF 108: estados límite',
}


def verificar_documentos():
    folder = Path(__file__).resolve().parents[3] / 'normativos'
    resultado = {}
    for clave, meta in DOCUMENTOS.items():
        path = folder / meta['archivo']
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        resultado[clave] = {**meta, 'ruta': str(path), 'sha256_actual': actual,
                           'coincide': actual == meta['sha256']}
    return resultado
