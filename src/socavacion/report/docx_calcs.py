"""Secciones de cálculo de la memoria: general, contracción, local y totales."""

from __future__ import annotations

from docx import Document

from socavacion.core.local_abutment import _froehlich, _hire
from socavacion.domain.models import Proyecto
from socavacion.domain.results import ResultadoCompleto
from socavacion.normative.constants import KU_CONTRACCION_CLARA
from socavacion.report.docx_format import body, calc_block
from socavacion.report.docx_sections import (
    LADO_LARGO,
    etiqueta_caudal,
    hidraulica_de,
    tabla_resumen_totales,
)

REF_GENERAL = "Manual de Puentes MTC 2018, Art. 1.2.3a; FHWA HEC-18, Cap. 6."
REF_CONTRACCION = "FHWA HEC-18, Cap. 6.4 (socavación por contracción, Laursen)."
REF_LOCAL = "FHWA HEC-18, Cap. 7 (Froehlich y HIRE); Manual de Puentes MTC 2018."
REF_TOTALES = "Manual de Puentes MTC 2018, Arts. 1.2.4 y 2.4.3.8.3.4."


def socavacion_general(document: Document, resultado: ResultadoCompleto, proyecto: Proyecto) -> None:
    document.add_heading("5. Socavación general", level=1)
    body(
        document,
        "La socavación general representa la degradación del fondo del cauce bajo la avenida. "
        "Se evalúa con los métodos de Lischtvan-Lebediev, Neill y Lacey, se adopta el mayor "
        "valor de avenida y se suma la degradación de largo plazo del cauce.",
    )
    estribos = {e.lado: e for e in proyecto.estribos()}
    for idx, caudal in enumerate(resultado.caudales):
        document.add_heading(f"5.{idx + 1} {etiqueta_caudal(caudal)}", level=2)
        for r in caudal.estribos:
            est = estribos[r.lado]
            hid = hidraulica_de(est, caudal.condicion)
            g = r.general
            li = g.y_sg_lischtvan.intermedios
            ne = g.y_sg_neill.intermedios
            la = g.y_sg_lacey.intermedios
            r_lacey = la.get("R", 0.0)
            calc_block(
                document,
                f"Socavación general — estribo {LADO_LARGO[r.lado]}",
                (
                    "h_{sg} = A · q^x",
                    "y_{sg,L} = h_{sg} − y_0",
                    "y_2 = y_1 · (q_2/q_1)^(6/7)",
                    "y_{sg,N} = y_2 − y_1",
                    "f = 1.76 · D_{50}^(1/2)",
                    "R = 0.47 · (Q/f)^(1/3)",
                    "y_{sg,La} = R − y_0",
                    "y_{sg} = y_{sg,lp} + y_{sg,av}",
                ),
                "h_sg: profundidad de flujo tras la socavación general (Lischtvan-Lebediev); "
                "A, x: coeficientes según la granulometría D_50; "
                "q: caudal específico del cauce; "
                "y_0: tirante existente en la sección; "
                "y_2: tirante de equilibrio (Neill); "
                "q_1, q_2: caudales específicos aguas arriba y en la sección; "
                "f: factor de limo de Lacey; "
                "R: profundidad de régimen de Lacey; "
                "Q: caudal de la avenida; "
                "y_{sg,lp}: degradación de largo plazo; "
                "y_{sg,av}: socavación de avenida adoptada, la mayor de los tres métodos",
                (
                    f"A = {li['A']:.4f}\n"
                    f"x = {li['x']:.3f}\n"
                    f"q = {li['q']:.3f} m²/s\n"
                    f"h_{{sg}} = {li['A']:.4f} · {li['q']:.3f}^({li['x']:.3f}) = {li['h_sg']:.3f} m\n"
                    f"y_{{sg,L}} = max({li['h_sg']:.3f} − {hid.y0:.3f}, 0) = {g.y_sg_lischtvan.valor:.3f} m\n"
                    f"y_2 = {hid.y1:.3f} · ({ne['q2']:.3f}/{ne['q1']:.3f})^(6/7) = {ne['y2']:.3f} m\n"
                    f"y_{{sg,N}} = max({ne['y2']:.3f} − {hid.y1:.3f}, 0) = {g.y_sg_neill.valor:.3f} m\n"
                    f"f = 1.76 · {est.D50_mm:.3f}^(1/2) = {la['f']:.3f}\n"
                    f"R = 0.47 · ({caudal.Q:.1f}/{la['f']:.3f})^(1/3) = {r_lacey:.3f} m\n"
                    f"y_{{sg,La}} = max({r_lacey:.3f} − {hid.y0:.3f}, 0) = {g.y_sg_lacey.valor:.3f} m\n"
                    f"y_{{sg}} = {g.y_sg_lp:.3f} + {g.y_sg_avenida:.3f} = {g.y_sg_total:.3f} m"
                ),
                (
                    f"la socavación general total del estribo {LADO_LARGO[r.lado]} es "
                    f"{g.y_sg_total:.3f} m; gobierna el método {g.metodo_gobernante}."
                ),
                "De los tres métodos se adopta el mayor valor de avenida; la agradación de "
                "largo plazo no reduce el diseño.",
                REF_GENERAL,
            )


def socavacion_contraccion(document: Document, resultado: ResultadoCompleto, proyecto: Proyecto) -> None:
    document.add_heading("6. Socavación por contracción", level=1)
    body(
        document,
        "La socavación por contracción se produce por el estrechamiento del flujo al pasar "
        "bajo el puente. Se evalúa con el método de Laursen según el régimen del lecho.",
    )
    estribos = {e.lado: e for e in proyecto.estribos()}
    for idx, caudal in enumerate(resultado.caudales):
        document.add_heading(f"6.{idx + 1} {etiqueta_caudal(caudal)}", level=2)
        for r in caudal.estribos:
            est = estribos[r.lado]
            hid = hidraulica_de(est, caudal.condicion)
            q1 = hid.Q1 if hid.Q1 is not None else caudal.Q
            q2 = hid.Q2 if hid.Q2 is not None else caudal.Q
            metodo = r.y_sc.metodo
            inter = r.y_sc.intermedios
            advert = " ".join(r.advertencias) if r.advertencias else metodo
            if metodo == "Sin contracción":
                calc_block(
                    document,
                    f"Contracción — estribo {LADO_LARGO[r.lado]}",
                    ("W_2 ≈ W_1", "y_{sc} = 0"),
                    "W_2: luz hidráulica bajo el puente; "
                    "W_1: ancho del cauce de aproximación",
                    f"W_1 = {hid.W1:.2f} m\nW_2 = {hid.W2:.2f} m",
                    "el puente no estrecha el cauce; la socavación por contracción es nula.",
                    "La diferencia relativa de anchos es menor que el 5% (tolerancia adoptada).",
                    REF_CONTRACCION,
                )
            elif metodo == "Laursen lecho vivo":
                calc_block(
                    document,
                    f"Contracción — estribo {LADO_LARGO[r.lado]}",
                    (
                        "y_2 = y_1 · (Q_2/Q_1)^(6/7) · (W_1/W_2)^(k_1)",
                        "y_{sc} = y_2 − y_0",
                    ),
                    "y_2: tirante de equilibrio en la sección contraída; "
                    "y_1: tirante medio de aproximación; "
                    "Q_1, Q_2: caudales en el cauce y en la sección contraída; "
                    "W_1, W_2: ancho del cauce y luz hidráulica bajo el puente; "
                    "k_1: exponente de Laursen según V_*/ω; "
                    "y_0: tirante existente bajo el puente",
                    (
                        f"k_1 = {inter['k1']:.3f}\n"
                        f"y_2 = {hid.y1:.3f} · ({q2:.1f}/{q1:.1f})^(6/7) · "
                        f"({hid.W1:.2f}/{hid.W2:.2f})^({inter['k1']:.3f}) = {inter['y2']:.3f} m\n"
                        f"y_{{sc}} = max({inter['y2']:.3f} − {hid.y0:.3f}, 0) = {r.y_sc.valor:.3f} m"
                    ),
                    (
                        f"la socavación por contracción del estribo {LADO_LARGO[r.lado]} es "
                        f"{r.y_sc.valor:.3f} m."
                    ),
                    advert,
                    REF_CONTRACCION,
                )
            else:
                calc_block(
                    document,
                    f"Contracción — estribo {LADO_LARGO[r.lado]}",
                    (
                        "D_m = 1.25 · D_{50}",
                        "y_2 = (K_u · Q_2^2 / (D_m^(2/3) · W_2^2))^(3/7)",
                        "y_{sc} = y_2 − y_0",
                    ),
                    "D_m: diámetro efectivo del material (1.25 D_50); "
                    "K_u: coeficiente 0.025 en el sistema SI; "
                    "Q_2: caudal en la sección contraída; "
                    "W_2: luz hidráulica bajo el puente; "
                    "y_2: tirante de equilibrio; "
                    "y_0: tirante existente bajo el puente",
                    (
                        f"D_m = 1.25 · {est.D50_m:.4f} = {inter['Dm']:.4f} m\n"
                        f"y_2 = ({KU_CONTRACCION_CLARA} · {q2:.1f}^2 / "
                        f"({inter['Dm']:.4f}^(2/3) · {hid.W2:.2f}^2))^(3/7) = {inter['y2']:.3f} m\n"
                        f"y_{{sc}} = max({inter['y2']:.3f} − {hid.y0:.3f}, 0) = {r.y_sc.valor:.3f} m"
                    ),
                    (
                        f"la socavación por contracción del estribo {LADO_LARGO[r.lado]} es "
                        f"{r.y_sc.valor:.3f} m."
                    ),
                    advert,
                    REF_CONTRACCION,
                )


def socavacion_local(document: Document, resultado: ResultadoCompleto, proyecto: Proyecto) -> None:
    document.add_heading("7. Socavación local en estribos", level=1)
    body(
        document,
        "La socavación local en estribos se evalúa con los métodos de Froehlich y HIRE de "
        "HEC-18 según la relación L′/y_a, y se limita al máximo normativo.",
    )
    estribos = {e.lado: e for e in proyecto.estribos()}
    for idx, caudal in enumerate(resultado.caudales):
        document.add_heading(f"7.{idx + 1} {etiqueta_caudal(caudal)}", level=2)
        for r in caudal.estribos:
            est = estribos[r.lado]
            hid = hidraulica_de(est, caudal.condicion)
            i = r.y_sl.intermedios
            limitado = any("Límite HEC-18" in a for a in r.advertencias)
            factor_limite = 2.4 if r.regimen.regimen.value == "lecho_vivo" else 2.2
            base_lines = [
                f"K_1 = {i['K1']:.3f}",
                f"K_2 = ({est.angulo_ataque:.1f}/90)^(0.13) = {i['K2']:.3f}",
            ]
            if r.y_sl.metodo.startswith("Froehlich"):
                ve = (hid.Q1 if hid.Q1 is not None else caudal.Q) / max(est.Ae, 1e-6)
                y_pre = _froehlich(i["ya"], est.L_prima, i["Fr_a"], i["K1"], i["K2"])
                formulas = (
                    "K_2 = (θ/90)^(0.13)",
                    "y_{sl} = y_a · (2.27 · K_1 · K_2 · (L′/y_a)^(0.43) · F_{ra}^(0.61) + 1)",
                )
                legend = (
                    "K_1: factor de forma del estribo; "
                    "K_2: factor de corrección por ángulo de ataque; "
                    "θ: ángulo entre el flujo y el eje del estribo; "
                    "y_a: tirante efectivo en el estribo, el mayor entre y_1 y A_e/L′; "
                    "L′: longitud del estribo; "
                    "F_{ra}: número de Froude asociado al tirante efectivo"
                )
                lines = base_lines + [
                    f"y_a = max({est.Ae:.2f}/{est.L_prima:.2f}, {hid.y1:.3f}) = {i['ya']:.3f} m",
                    f"F_{{ra}} = {ve:.3f} / √(9.81 · {i['ya']:.3f}) = {i['Fr_a']:.3f}",
                    f"L′/y_a = {est.L_prima:.2f} / {i['ya']:.3f} = {est.L_prima / i['ya']:.2f} ≤ 25",
                    (
                        f"y_{{sl}} = {i['ya']:.3f} · (2.27 · {i['K1']:.3f} · {i['K2']:.3f} · "
                        f"({est.L_prima:.2f}/{i['ya']:.3f})^(0.43) · {i['Fr_a']:.3f}^(0.61) + 1) "
                        f"= {y_pre:.3f} m"
                    ),
                ]
            else:
                y_pre = _hire(hid.y1, r.regimen.Fr, i["K1"], i["K2"])
                formulas = (
                    "K_2 = (θ/90)^(0.13)",
                    "y_{sl} = 4 · y_1 · F_r^(1/3) · (K_1/0.55) · K_2",
                )
                legend = (
                    "K_1: factor de forma del estribo; "
                    "K_2: factor de corrección por ángulo de ataque; "
                    "θ: ángulo entre el flujo y el eje del estribo; "
                    "y_1: tirante de aproximación; "
                    "F_r: número de Froude de aproximación"
                )
                lines = base_lines + [
                    f"L′/y_a = {est.L_prima:.2f} / {i['ya']:.3f} = {est.L_prima / i['ya']:.2f} > 25",
                    (
                        f"y_{{sl}} = 4 · {hid.y1:.3f} · {r.regimen.Fr:.3f}^(1/3) · "
                        f"({i['K1']:.3f}/0.55) · {i['K2']:.3f} = {y_pre:.3f} m"
                    ),
                ]
            if limitado:
                lines.append(
                    f"y_{{sl,max}} = {factor_limite} · {i['K1']:.3f} · ({i['K2']:.3f}/0.55) · "
                    f"{i['ya']:.3f} = {i['limite']:.3f} m"
                )
                lines.append("El valor calculado excede el máximo HEC-18; se adopta el límite.")
            ratio = est.L_prima / i["ya"]
            criterio = "≤ 25: rango Froehlich." if ratio <= 25.0 else "> 25: rango HIRE."
            calc_block(
                document,
                f"Socavación local — estribo {LADO_LARGO[r.lado]}",
                formulas,
                legend,
                "\n".join(lines),
                (
                    f"la socavación local del estribo {LADO_LARGO[r.lado]} es "
                    f"{r.y_sl.valor:.3f} m ({r.y_sl.metodo})."
                ),
                f"L′/y_a = {ratio:.2f} {criterio}",
                REF_LOCAL,
            )


def socavacion_total(document: Document, resultado: ResultadoCompleto) -> None:
    document.add_heading("8. Socavación total y cimentación", level=1)
    body(
        document,
        "La socavación total se obtiene sumando los componentes general, por contracción y "
        "local. La socavación de diseño es la envolvente de Q100 y Q500; con ella se obtiene "
        "la cota del lecho socavado y la cota mínima de cimentación.",
    )
    for e in resultado.estribos_finales:
        lado = LADO_LARGO[e.lado]
        c100 = e.componentes_100
        c500 = e.componentes_500
        formulas = [
            "y_s = y_{sg} + y_{sc} + y_{sl}",
            "Z_{soc} = Z_{lecho} − y_s",
        ]
        if e.Z_cim_min is not None:
            formulas.append("Z_{cim} = Z_{soc} − R")
        lines = [
            f"y_{{s,100}} = {c100.general.y_sg_total:.3f} + {c100.y_sc.valor:.3f} + "
            f"{c100.y_sl.valor:.3f} = {e.y_s_100:.3f} m",
            f"y_{{s,500}} = {c500.general.y_sg_total:.3f} + {c500.y_sc.valor:.3f} + "
            f"{c500.y_sl.valor:.3f} = {e.y_s_500:.3f} m",
            f"y_s = max({e.y_s_100:.3f}, {e.y_s_500:.3f}) = {e.y_s_diseno:.3f} m",
            f"Z_{{soc}} = {e.Z_lecho_actual:.3f} − {e.y_s_diseno:.3f} = {e.Z_lecho_soc:.3f} m",
        ]
        if e.Z_cim_min is not None:
            lines.append(f"Z_{{cim}} = {e.Z_lecho_soc:.3f} − 1.00 = {e.Z_cim_min:.3f} m")
            result = (
                f"la cota mínima de cimentación del estribo {lado} es "
                f"{e.Z_cim_min:.3f} m s.n.m."
            )
        else:
            result = (
                f"la cota del lecho socavado del estribo {lado} es "
                f"{e.Z_lecho_soc:.3f} m s.n.m."
            )
        calc_block(
            document,
            f"Socavación total — estribo {lado}",
            tuple(formulas),
            "y_s: socavación total del estribo; "
            "y_{sg}, y_{sc}, y_{sl}: componentes general, de contracción y local; "
            "Z_{soc}: cota del lecho socavado; "
            "Z_{lecho}: cota actual del lecho; "
            "Z_{cim}: cota mínima de cimentación; "
            "R: reserva mínima reglamentaria de 1.00 m",
            "\n".join(lines),
            result,
            "La socavación de diseño es la mayor entre Q100 y Q500; la reserva de 1.00 m "
            "corresponde a cimentación superficial (Art. 1.2.4).",
            REF_TOTALES,
        )
    tabla_resumen_totales(document, resultado)
