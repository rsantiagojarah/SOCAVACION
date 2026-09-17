"""Memoria emitida desde los resultados calculados, sin recalcular fórmulas."""
from socavacion.report.docx_format import body, table
from socavacion.report.trace import lineas_componente


def _bloque(document, nombre, comp):
    document.add_heading(nombre, level=2)
    for linea in lineas_componente(comp):
        body(document, linea)


def socavacion_general(document, resultado, proyecto):
    document.add_heading('5. Socavación general con contracción', level=1)
    body(document, 'Lischtvan-Levediev granular, HHD ec.59, p.108. Dm en mm. El término LL incluye la contracción; se suma la degradación de largo plazo sustentada e independiente.')
    for c in resultado.caudales:
        for e in c.estribos:
            _bloque(document, f'{c.escenario}: estribo {e.lado.value}', e.general.y_sg_lischtvan)
            body(document, f'LP={e.general.y_sg_lp:.6f} m; LP+LL={e.general.y_sg_total:.6f} m.')
        for p in c.pilares:
            _bloque(document, f'{c.escenario}: pilar {p.nombre}', p.general.y_sg_lischtvan)
            body(document, f'LP={p.general.y_sg_lp:.6f} m; LP+LL={p.general.y_sg_total:.6f} m.')


def socavacion_contraccion(document, resultado, proyecto):
    document.add_heading('6. Contabilización de la contracción', level=1)
    body(document, 'La contracción se incluye mediante mu en LL. El sumando independiente vale cero por contabilidad, no significa ausencia física de contracción. No se suma Laursen nuevamente.')


def socavacion_local(document, resultado, proyecto):
    document.add_heading('7. Socavación local por apoyo', level=1)
    for c in resultado.caudales:
        for e in c.estribos:
            _bloque(document, f'{c.escenario}: estribo {e.lado.value}', e.y_sl)
        for p in c.pilares:
            _bloque(document, f'{c.escenario}: pilar {p.nombre}', p.y_sp)


def socavacion_total(document, resultado):
    document.add_heading('8. Totales y cotas por apoyo', level=1)
    body(document, 'MP 1.2.3a: total=LP+LL(incluye contracción)+local. Se conserva cada escenario y se compara por profundidad de socavación. Diseño: resistencia/servicio; verificación: evento extremo.')
    for c in resultado.caudales:
        for e in c.estribos:
            body(document, f'{c.escenario} estribo {e.lado.value}: {e.general.y_sg_total:.6f}+{e.y_sl.valor:.6f}={e.y_s_total:.6f} m.')
        for p in c.pilares:
            body(document, f'{c.escenario} pilar {p.nombre}: {p.general.y_sg_total:.6f}+{p.y_sp.valor:.6f}={p.y_s_total:.6f} m.')
    for e in resultado.estribos_finales:
        body(document, f'Estribo {e.lado.value}: diseño {e.escenario_diseno}={e.y_s_100:.6f} m; verificación {e.escenario_verificacion}={e.y_s_500:.6f} m. Zsoc={e.Z_lecho_actual:.6f}-{e.y_s_diseno:.6f}={e.Z_lecho_soc:.6f} m.')
        if e.Z_cim_min is not None:
            body(document, f'Fondo superficial Z <= {e.Z_cim_min:.6f} m (MP 1.2.4; Zsoc-1.00 m).')
    for p in resultado.pilares_finales:
        body(document, f'Pilar {p.nombre}: diseño {p.escenario_diseno}={p.y_s_diseno:.6f} m; verificación {p.escenario_verificacion}={p.y_s_verificacion:.6f} m; máximo={p.y_s_max:.6f} m; Zsoc={p.Z_lecho_soc}; fondo superficial Z <= {p.Z_cim_limite}.')
    body(document, 'La reserva superficial no determina capacidad portante. Las cimentaciones profundas requieren punta, longitud efectiva y estabilidad con el suelo socavado retirado. Sobre roca debe justificarse resistencia a erosión.')
