"""Visualización de resultados en terminal con tablas ASCII."""

from __future__ import annotations

from socavacion.cli.ascii_tables import boxed_table, key_value_table
from socavacion.domain.enums import CondicionCaudal, LadoEstribo
from socavacion.domain.results import ResultadoCompleto
from socavacion.domain.observations import resumir_advertencias


def _tabla_resumen(resultado: ResultadoCompleto) -> list[str]:
    rows = []
    for e in resultado.estribos_finales:
        label = "Izquierdo" if e.lado == LadoEstribo.IZQUIERDO else "Derecho"
        z_cim = f"{e.Z_cim_min:.3f}" if e.Z_cim_min is not None else "—"
        rows.append(
            (
                label,
                f"{e.y_s_100:.3f}",
                f"{e.y_s_500:.3f}",
                f"{e.y_s_diseno:.3f}",
                f"{e.Z_lecho_soc:.3f}",
                z_cim,
            )
        )
    return boxed_table(
        ("Estribo", "Env. diseño (m)", "Env. comprob. (m)", "Máximo (m)", "Z lecho soc (m)", "Z zapata <= (m)"),
        rows,
        aligns=("left", "right", "right", "right", "right", "right"),
        title="Resumen ejecutivo — Socavación de diseño",
    )


def _tabla_desglose(resultado: ResultadoCompleto) -> list[str]:
    lines: list[str] = []
    for caudal in resultado.caudales:
        cond_label = caudal.escenario
        rows = []
        for r in caudal.estribos:
            label = "E-I" if r.lado == LadoEstribo.IZQUIERDO else "E-D"
            rows.append(
                (
                    label,
                    r.regimen.regimen.value,
                    f"{r.general.y_sg_total:.3f}",
                    f"{r.y_sc.valor:.3f}",
                    f"{r.y_sl.valor:.3f}",
                    f"{r.y_s_total:.3f}",
                    r.general.metodo_gobernante,
                )
            )
        lines.extend(
            boxed_table(
                ("Estribo", "Régimen", "y_sg (m)", "y_sc (m)", "y_sl (m)", "y_s (m)", "Método general"),
                rows,
                aligns=("left", "left", "right", "right", "right", "right", "left"),
                title=f"Desglose — {cond_label}  Q = {caudal.Q:.1f} m³/s",
            )
        )
        lines.append("")
    return lines


def _tabla_geotecnia(resultado: ResultadoCompleto) -> list[str]:
    rows = []
    for item in resultado.geotecnia.items:
        ok = "Sí" if item.compatible else "No"
        rows.append((item.item, item.hidraulica, item.geotecnia, ok))
    lines = boxed_table(
        ("Ítem", "Hidráulica", "Geotecnia", "¿OK?"),
        rows,
        aligns=("left", "left", "left", "center"),
        title="Compatibilidad geotecnia (10.11)",
    )
    lines.append("")
    lines.append(f"Conclusión: {resultado.geotecnia.conclusion}")
    return lines


def mostrar_resultados(resultado: ResultadoCompleto) -> None:
    if resultado.auditoria.get('metodo_calculo') == 'froehlich':
        _mostrar_froehlich(resultado)
        return
    lines: list[str] = []
    lines.append(f"\nProyecto: {resultado.proyecto_nombre}")
    lines.append(
        f"Q100 base = {resultado.Q_diseno:.1f} m³/s  |  "
        f"Q500 base = {resultado.Q_verif:.1f} m³/s"
    )
    lines.append("")
    lines.extend(_tabla_resumen(resultado))
    lines.append("")
    lines.extend(_tabla_desglose(resultado))
    lines.append('Contracción independiente = 0: ya incluida en LL mediante mu, no ausencia física.')
    for p in resultado.pilares_finales:
        lines.append(f'Pilar {p.nombre}: diseño={p.y_s_diseno:.3f} m ({p.escenario_diseno}); '
                     f'comprobación={p.y_s_verificacion:.3f} m ({p.escenario_verificacion}); '
                     f'Z socavado={p.Z_lecho_soc}; Z zapata <= {p.Z_cim_limite}')
    for e in resultado.estribos_finales:
        lines.append(f'Estribo {e.lado.value}: gobiernan {e.escenario_diseno} (diseño), '
                     f'{e.escenario_verificacion} (comprobación).')
    lines.append(f"Modo: {resultado.auditoria['modo']}; versión: {resultado.auditoria['version_metodo']}")
    lines.extend(_tabla_geotecnia(resultado))

    todas_adv: list[str] = list(resultado.advertencias_globales)
    hipotesis: list[str] = []
    for c in resultado.caudales:
        for e in c.estribos:
            evento = {'Q100':'q100', 'Q500':'q500', 'Qot':'qot'}[c.escenario]
            for a in e.advertencias:
                destino = hipotesis if a.startswith('Cierre alpha=') else todas_adv
                destino.append(f'{e.lado.value}/{evento}: {a}')
        for p in c.pilares:
            evento = {'Q100':'q100', 'Q500':'q500', 'Qot':'qot'}[c.escenario]
            for a in p.general.y_sg_lischtvan.supuestos + p.y_sp.supuestos:
                destino = hipotesis if a.startswith(('Cierre alpha=', 'CSU sin truncamiento')) else todas_adv
                destino.append(f'{p.nombre}/{evento}: {a}')
    if todas_adv:
        lines.append("")
        lines.append('Advertencias (agrupadas por apoyo y avenida):')
        lines.extend(resumir_advertencias(todas_adv))
        lines.append('Revise datos y fuentes pendientes antes de usar el resultado para diseño.')
    if hipotesis:
        lines.append('')
        lines.append('Hipótesis del método (revisar aplicabilidad; no son campos omitidos):')
        lines.extend(resumir_advertencias(hipotesis))

    print("\n".join(lines))


def _mostrar_froehlich(resultado):
    lines = [f'\nProyecto: {resultado.proyecto_nombre}', resultado.auditoria['alcance']]
    for c in resultado.caudales:
        rows = []
        for e in c.estribos:
            v = e.y_sl.intermedios
            rows.append((e.lado.value, f'{v["Ae"]:.3f}', f'{v["Qe"]:.3f}',
                         f'{v["L_prima"]:.3f}', f'{v["ya"]:.3f}', f'{v["Ve"]:.3f}',
                         f'{v["Fr_a"]:.3f}', f'{e.y_sl.valor:.3f}'))
        lines.extend(boxed_table(('Estribo', 'Ae m2', 'Qe m3/s', 'L m', 'he m', 'Ve m/s', 'Fre', 'ys LOCAL m'),
                                rows, title=f'Froehlich {c.escenario}: Q={c.Q:.3f} m³/s'))
    rows = [(e.lado.value, f'{e.y_s_100:.3f} ({e.escenario_diseno})',
             f'{e.y_s_500:.3f} ({e.escenario_verificacion})', f'{e.y_s_diseno:.3f}') for e in resultado.estribos_finales]
    lines.extend(boxed_table(('Estribo', 'Env. LOCAL Q100/Qot', 'Env. LOCAL Q500/Qot', 'Máximo LOCAL m'),
                            rows, title='Resumen — sólo socavación local'))
    lines.append('R se registra, pero no interviene en Froehlich. No se ha calculado socavación total ni cimentación.')
    lines.extend(resumir_advertencias(resultado.advertencias_globales))
    print('\n'.join(lines))


__all__ = ["mostrar_resultados", "boxed_table", "key_value_table"]
