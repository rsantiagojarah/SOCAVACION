"""Secciones documentales basadas en escenarios y referencias verificadas."""
from __future__ import annotations
import json
from docx import Document
from socavacion.domain.enums import CondicionCaudal, LadoEstribo
from socavacion.normative.references import REFERENCIAS
from socavacion.report.docx_format import body, comment, table

LADO_LARGO = {LadoEstribo.IZQUIERDO: "izquierdo", LadoEstribo.DERECHO: "derecho"}
LADO_CORTO = {LadoEstribo.IZQUIERDO: "E-I", LadoEstribo.DERECHO: "E-D"}

def hidraulica_de(apoyo, cond):
    return {CondicionCaudal.DISENO: apoyo.q100, CondicionCaudal.VERIFICACION: apoyo.q500,
            CondicionCaudal.DESBORDAMIENTO: apoyo.qot}[cond]

def etiqueta_caudal(caudal):
    return f"{caudal.escenario} — Q = {caudal.Q:.3f} m³/s"

def bases(document: Document):
    document.add_heading("1. Bases y alcance del cálculo", level=1)
    body(document, "Procedimiento para lecho granular: Lischtvan–Levediev (LL) con contracción "
         "incorporada mediante mu, más degradación de largo plazo no duplicada, más socavación "
         "local en el mismo apoyo. Estribos: Froehlich o HIRE; pilares: CSU. "
         "No se suma nuevamente Laursen ni se adopta una envolvente de LL, Neill y Lacey.")
    body(document, "Fuentes: Manual de Hidrología, Hidráulica y Drenaje MTC y Manual de Puentes "
         "MTC 2018. La discrepancia impresa de CSU se resuelve expresamente con USACE HEC-RAS "
         "4.1, ecuación 10-6. Las referencias precisas se presentan al final y junto al cálculo.")
    comment(document, "El modo trazable controla identificación de datos y fuentes declaradas; "
            "no certifica su veracidad ni sustituye revisión profesional. No cubre roca, "
            "suelos cohesivos, flujo a presión, detritos ni estratificación. No calcula capacidad "
            "portante, estabilidad ni resistencia estructural de la cimentación.")

def datos_entrada(document, proyecto):
    document.add_heading("2. Datos de entrada reproducibles", level=1)
    body(document, "Los siguientes datos son el registro completo usado por el cálculo. "
         "Las fuentes son declaraciones del autor del estudio, no verificaciones de campo.")
    # Un párrafo por línea permite dividir el anexo sin filas de altura excesiva.
    for line in json.dumps(proyecto.model_dump(mode="json"), ensure_ascii=False, indent=2).splitlines():
        body(document, line)

def caudales(document, resultado, proyecto):
    document.add_heading("3. Escenarios hidráulicos y selección", level=1)
    body(document, "Se calcula cada evento de forma independiente. Según MP 1.2.3a, el evento "
         "de desbordamiento de menor retorno se incluye si produce mayor socavación: "
         "T_ot < 100 años para diseño y T_ot < 500 años para comprobación. Se compara la "
         "socavación, no solamente el caudal; la envolvente se obtiene por apoyo.")
    table(document, ("Escenario", "Q (m³/s)"),
          [(c.escenario, f"{c.Q:.6g}") for c in resultado.caudales], widths=(95,72))
    body(document, "Q100 y Q500 son las bases implementadas. Si el proyecto exige un período "
         "superior, se necesita una evaluación adicional fuera de estos dos escenarios base. "
         "Los estados límite se revisan según MP 2.4.3.8.3.4.")

def regimen(document, resultado, proyecto):
    document.add_heading("4. Diagnóstico de movilidad y flujo", level=1)
    body(document, "Vc = 6.19 y1^(1/6) D50^(1/3), con D50 en metros; Fr = V1/sqrt(g y1). "
         "La comparación V1/Vc es un diagnóstico simplificado, no demuestra por sí sola la "
         "carga sólida real. No se utiliza aquí para seleccionar una contracción independiente.")
    rows = []
    for c in resultado.caudales:
        for e in c.estribos:
            r = e.regimen
            rows.append((c.escenario, e.lado.value, f"{r.V1:.3f}", f"{r.Vc:.3f}", f"{r.Fr:.3f}"))
    table(document, ("Evento", "Estribo", "V1 m/s", "Vc m/s", "Fr"), rows,
          widths=(32,45,30,30,30))

def geotecnia(document, resultado):
    document.add_heading("9. Controles geométricos y geotécnicos preliminares", level=1)
    body(document, "MP 1.2.4: zapata superficial al menos 1 m bajo la máxima socavación; "
         "pilotes referidos al lecho socavado; parte superior del cabezal bajo la socavación "
         "por contracción. Estos controles no constituyen diseño geotécnico.")
    table(document, ("Ítem", "Hidráulica", "Geotecnia", "¿OK?"),
          [(i.item, i.hidraulica, i.geotecnia, "Sí" if i.compatible else "No")
           for i in resultado.geotecnia.items], widths=(36,56,56,19))
    comment(document, resultado.geotecnia.conclusion)

def referencias(document):
    document.add_heading("10. Referencias y decisiones de implementación", level=1)
    for key, value in REFERENCIAS.items():
        body(document, f"{key}: {value}")

def auditoria(document, resultado):
    document.add_heading("11. Auditoría y observaciones", level=1)
    for key in ("version_metodo", "modo", "entrada_sha256", "fuente_codigo_sha256", "alcance"):
        body(document, f"{key}: {resultado.auditoria[key]}")
    for key, value in resultado.auditoria["documentos"].items():
        body(document, f"{key}: {value['archivo']}; SHA256: {value['sha256_actual']}; "
             f"coincide con documento revisado: {value['coincide']}")
    for warning in dict.fromkeys(resultado.advertencias_globales):
        body(document, warning)
