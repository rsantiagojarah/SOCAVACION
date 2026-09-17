"""Generación de memorias de cálculo Word para análisis de socavación.

Registro uniforme de ecuaciones, sustituciones, fuentes y resultados.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from docx import Document
from docx.shared import Pt

from socavacion.domain.models import Proyecto
from socavacion.domain.results import ResultadoCompleto
from socavacion.report import docx_calcs, docx_sections
from socavacion.report.trace import guardar_auditoria
from socavacion.report.docx_format import (
    body,
    bottom_border,
    configure_document,
    configure_header_footer,
    enforce_uniform_typography,
    format_run,
    table,
)
from socavacion.report.docx_style import FILENAME_PREFIX, TEAL

REF_MTC = "Manual de Puentes MTC 2018"


def generate_socavacion_docx(
    resultado: ResultadoCompleto,
    proyecto: Proyecto,
    output_path: str | Path,
) -> Path:
    """Crea la memoria Word y devuelve su ruta absoluta."""
    path = Path(output_path).expanduser().resolve()
    if path.suffix.lower() != ".docx":
        path = path.with_suffix(".docx")
    path.parent.mkdir(parents=True, exist_ok=True)

    document = Document()
    configure_document(document)
    configure_header_footer(document)

    if proyecto.metodo_calculo == 'froehlich':
        _contenido_froehlich(document, resultado, proyecto)
        enforce_uniform_typography(document)
        document.save(path)
        guardar_auditoria(resultado, path)
        return path

    _cover(document, resultado, proyecto)
    _contents(document)
    docx_sections.bases(document)
    docx_sections.datos_entrada(document, proyecto)
    docx_sections.caudales(document, resultado, proyecto)
    docx_sections.regimen(document, resultado, proyecto)
    docx_calcs.socavacion_general(document, resultado, proyecto)
    docx_calcs.socavacion_contraccion(document, resultado, proyecto)
    docx_calcs.socavacion_local(document, resultado, proyecto)
    docx_calcs.socavacion_total(document, resultado)
    docx_sections.geotecnia(document, resultado)
    docx_sections.referencias(document)
    docx_sections.auditoria(document, resultado)

    enforce_uniform_typography(document)
    document.save(path)
    guardar_auditoria(resultado, path)
    return path


def _contenido_froehlich(document, resultado, proyecto):
    """Memoria parcial sin apartados ni resultados ficticios de LL o cimentación."""
    import json
    from socavacion.report.trace import componentes, lineas_componente
    document.add_heading('Socavación local en estribos — Froehlich', 0)
    body(document, f'Proyecto: {proyecto.nombre}. Modo: {proyecto.modo}.')
    body(document, resultado.auditoria['alcance'])
    body(document, 'MTC HHD: ecuaciones 92–94 y Tabla 27, pp.148–151. MP 1.2.3a: '
         'el cálculo integral requiere además los componentes general y de contracción, aquí NO EVALUADOS.')
    document.add_heading('1. Datos y procedimiento', 1)
    body(document, 'Datos manuales de HEC-RAS, sin sección rectangular impuesta ni franjas. '
         'Q y A pertenecen a la misma sección activa de aproximación. Ae, Qe y L corresponden '
         'al flujo obstruido aguas arriba por cada estribo. R se registra y no interviene en la fórmula.')
    body(document, 'he=Ae/L; Ve=Qe/Ae; Fre=Ve/sqrt(9.81 he); '
         'Ktheta=(theta/90)^0.13; Kf según forma, Tabla 27. '
         'ys=he[2.27 Kf Ktheta (L/he)^0.43 Fre^0.61+1]. Se conserva +1 para diseño.')
    for nombre, componente in componentes(resultado):
        document.add_heading(nombre, 2)
        for linea in lineas_componente(componente):
            body(document, linea)
    document.add_heading('2. Envolventes exclusivamente locales', 1)
    table(document, ('Estribo', 'Q100/Qot local m', 'Q500/Qot local m', 'Máximo local m'),
          [(e.lado.value, f'{e.y_s_100:.3f} ({e.escenario_diseno})',
            f'{e.y_s_500:.3f} ({e.escenario_verificacion})', f'{e.y_s_diseno:.3f}')
           for e in resultado.estribos_finales], widths=(35,47,47,38))
    body(document, 'Se considera Qot de menor retorno si resulta más severo localmente '
         '(T_ot<100/T_ot<500). No se calculan socavación total, cotas finales ni cimentación. '
         'Los componentes no evaluados son null en la auditoría, no cero.')
    document.add_heading('3. Auditoría y entradas reproducibles', 1)
    for clave in ('version_metodo', 'entrada_sha256', 'fuente_codigo_sha256'):
        body(document, f'{clave}: {resultado.auditoria[clave]}')
    for ref, contenido in resultado.auditoria['referencias'].items():
        body(document, f'{ref}: {contenido}')
    for clave, doc in resultado.auditoria['documentos'].items():
        body(document, f'{clave}: {doc["archivo"]}; SHA256 {doc["sha256_actual"]}; coincide: {doc["coincide"]}')
    for aviso in resultado.advertencias_globales:
        body(document, aviso)
    for linea in json.dumps(resultado.auditoria['entrada'], ensure_ascii=False, indent=2).splitlines():
        body(document, linea)


def select_socavacion_docx_save_path(
    resultado: ResultadoCompleto | None = None,
    proyecto: Proyecto | None = None,
    *,
    initial_dir: Path | None = None,
) -> Path | None:
    """Abre diálogo nativo para guardar la memoria Word."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as exc:
        raise RuntimeError("Tkinter no está disponible para elegir el destino Word.") from exc

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    default_name = f"{FILENAME_PREFIX}_{datetime.now():%Y%m%d_%H%M}.docx"
    kwargs = {
        "parent": root,
        "title": "Guardar memoria de cálculo de socavación",
        "defaultextension": ".docx",
        "initialfile": default_name,
        "filetypes": (("Documento de Word", "*.docx"),),
    }
    if initial_dir is not None:
        kwargs["initialdir"] = str(initial_dir)
    try:
        selected = filedialog.asksaveasfilename(**kwargs)
    finally:
        root.destroy()
    return Path(selected) if selected else None


def generate_socavacion_docx_with_dialog(
    resultado: ResultadoCompleto,
    proyecto: Proyecto,
    *,
    initial_dir: Path | None = None,
) -> Path | None:
    """Solicita destino y genera la memoria Word."""
    path = select_socavacion_docx_save_path(resultado, proyecto, initial_dir=initial_dir)
    if path is None:
        print("Generación de la memoria Word cancelada por el usuario.")
        return None
    generated = generate_socavacion_docx(resultado, proyecto, path)
    print(f"Memoria Word guardada en: {generated}")
    return generated


def _cover(document: Document, resultado: ResultadoCompleto, proyecto: Proyecto) -> None:
    par = document.add_paragraph()
    par.paragraph_format.space_after = Pt(34)
    run = par.add_run("INGENIERÍA ESTRUCTURAL")
    format_run(run, 11, bold=True)
    bottom_border(par, TEAL, 16)

    par = document.add_paragraph(style="Title")
    par.add_run("Memoria de cálculo\nde socavación en puentes")

    par = document.add_paragraph(style="Subtitle")
    par.add_run(
        "Socavación general con contracción · local en apoyos · cotas de referencia · "
        "compatibilidad geotécnica"
    )

    par = document.add_paragraph()
    par.paragraph_format.space_before = Pt(32)
    par.paragraph_format.space_after = Pt(4)
    run = par.add_run(f"CÁLCULO {proyecto.modo.upper()} — SUJETO A REVISIÓN PROFESIONAL")
    format_run(run, 11, bold=True)

    table(
        document,
        ("Dato", "Descripción"),
        (
            ("Proyecto", proyecto.nombre),
            ("Q100 base", f"{resultado.Q_diseno:.2f} m³/s"),
            ("Q500 base", f"{resultado.Q_verif:.2f} m³/s"),
            ("Fuentes", f"{REF_MTC}; Manual HHD MTC; corrección CSU: USACE"),
            ("Alcance", "Lecho granular; LL + largo plazo + local por apoyo"),
            ("Fecha de emisión", datetime.now().strftime("%d/%m/%Y")),
        ),
        widths=(42, 125),
        accent=True,
    )

    par = document.add_paragraph()
    par.paragraph_format.space_before = Pt(30)
    run = par.add_run(
        "La presente memoria desarrolla las expresiones, leyendas, sustituciones numéricas, "
        "resultados y criterios técnicos del análisis de socavación según el Manual de "
        "Puentes MTC 2018 y el Manual de Hidrología, Hidráulica y Drenaje MTC, "
        "dentro del alcance y las decisiones documentadas. No constituye aprobación del diseño."
    )
    format_run(run, 11, italic=True)
    document.add_page_break()


def _contents(document: Document) -> None:
    document.add_heading("Contenido", level=1)
    body(
        document,
        "La memoria se organiza siguiendo la secuencia del procedimiento de cálculo. Los "
        "títulos conservan estilos jerárquicos de Word para permitir navegación desde el "
        "panel de títulos.",
    )
    table(
        document,
        ("Sección", "Contenido desarrollado"),
        (
            ("1", "Bases de diseño y componentes evaluados"),
            ("2", "Datos de entrada del proyecto"),
            ("3", "Caudales de cálculo"),
            ("4", "Régimen del lecho"),
            ("5", "Socavación general"),
            ("6", "Socavación por contracción"),
            ("7", "Socavación local en estribos y pilares"),
            ("8", "Socavación total y cimentación"),
            ("9", "Compatibilidad geológico-geotécnica"),
            ("10", "Referencias normativas"),
            ("11", "Auditoría y observaciones"),
        ),
        widths=(25, 142),
        accent=True,
    )
    document.add_page_break()
