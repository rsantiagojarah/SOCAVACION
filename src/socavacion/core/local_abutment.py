"""Estribos: HHD ec.92-94 y 103; sin topes no sustentados."""
import math
from socavacion.domain.models import CondicionHidraulica, Estribo
from socavacion.domain.results import ComponenteSocavacion, RegimenResult
from socavacion.normative.constants import G
from socavacion.normative.tables import K1_ESTRIBO


def k2_angulo(theta_grados: float) -> float:
    return (theta_grados / 90.0) ** 0.13


def _froehlich(ya, L_prima, Fr_a, K1, K2):
    return ya * (2.27*K1*K2*(L_prima/ya)**0.43*Fr_a**0.61 + 1)


def _hire(y1, Fr, K1, K2):
    return 4*y1*(Fr**0.33)*(K1/0.55)*K2


def calcular_local_estribo(estribo: Estribo, hid: CondicionHidraulica,
                          regimen: RegimenResult | None):
    supuestos = []
    K1, K2 = K1_ESTRIBO[estribo.forma], k2_angulo(estribo.angulo_ataque)
    L = hid.L_obstruida if hid.L_obstruida is not None else estribo.L_prima
    Ae = hid.Ae if hid.Ae is not None else estribo.Ae
    if estribo.metodo_local == 'hire':
        if not estribo.penetra_cauce or hid.h_pie is None or hid.V_pie is None:
            raise ValueError('HIRE requiere penetra_cauce y h_pie/V_pie por avenida (HHD pp.156-157)')
        ya, Ve = hid.h_pie, hid.V_pie
        if L/ya <= 25:
            raise ValueError('HIRE: aplicación restringida en esta implementación a L/h > 25')
        Fr = Ve/math.sqrt(G*ya)
        ys = _hire(ya, Fr, K1, K2)
        metodo, formula, ref = 'HIRE MTC HHD', 'ys=4*h_pie*(Kf/0.55)*Ktheta*Fr^0.33', 'H103'
    else:
        ya = Ae/L if Ae > 0 else hid.y1
        if Ae <= 0:
            supuestos.append('Ae=0: h_e=y1 y Ve=V1, aproximación preliminar; falta definir flujo obstruido.')
        if hid.Qe is not None and Ae > 0:
            Ve = hid.Qe/Ae
        else:
            Ve = hid.V1
            supuestos.append('Qe no disponible: Ve=V1 supuesto preliminar; Q1 no sustituye Qe.')
        Fr = Ve/math.sqrt(G*ya)
        ys = _froehlich(ya, L, Fr, K1, K2)
        metodo, formula, ref = 'Froehlich HEC-18 / MTC HHD', 'ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae', 'F92'
    return ComponenteSocavacion(
        metodo=metodo, valor=ys, formula=formula,
        intermedios={'K1':K1,'K2':K2,'theta':estribo.angulo_ataque,'Fr_a':Fr,'L_prima':L,'ya':ya,'Ve':Ve,'Ae':Ae,
                     'Qe':hid.Qe if hid.Qe is not None else Ve*Ae, 'ys':ys},
        notas=('HIRE: selección explícita; restricción L/h>25 de esta implementación.' if estribo.metodo_local == 'hire'
               else 'Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.'),
        referencias=[ref], supuestos=supuestos, fuentes_datos=dict(hid.fuentes),
        unidades={'K1':'1','K2':'1','theta':'grados','Fr_a':'1','L_prima':'m','ya':'m','Ve':'m/s','Ae':'m2','Qe':'m3/s','ys':'m'},
    ), supuestos
