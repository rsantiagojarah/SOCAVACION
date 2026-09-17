"""CSU: HHD tablas 20-22; cociente a/h contrastado con USACE ec.10-6."""
import math
from socavacion.domain.models import CondicionHidraulica, Pilar
from socavacion.domain.results import ComponenteSocavacion, RegimenResult
from socavacion.normative.tables import K1_PILAR


def k2_pilar(theta: float, relacion_l_a: float = 1.0) -> float:
    if not math.isfinite(theta) or not 0 <= theta <= 180 or not math.isfinite(relacion_l_a) or relacion_l_a < 1:
        raise ValueError('CSU requiere ángulo 0..180 grados y l/a >= 1')
    ang = math.radians(min(theta, 180-theta))
    return (math.cos(ang)+min(relacion_l_a,12)*math.sin(ang))**0.65


def calcular_local_pilar(pilar: Pilar, hid: CondicionHidraulica, regimen: RegimenResult):
    theta = min(pilar.angulo_ataque,180-pilar.angulo_ataque)
    if theta and pilar.longitud_l is None:
        raise ValueError('Pilar sesgado requiere longitud_l para K2 (HHD ec.82)')
    relacion = (pilar.longitud_l or pilar.ancho_a)/pilar.ancho_a
    K1 = K1_PILAR[pilar.forma] if theta < 5 else 1.0
    K2 = k2_pilar(pilar.angulo_ataque, relacion)
    if pilar.K4 < 1 and not pilar.fuente_K4.strip():
        raise ValueError('Reducción K4 requiere fuente_K4 con granulometría/cálculo de acorazamiento')
    ys = 2*K1*K2*pilar.K3*pilar.K4*pilar.ancho_a**0.65*hid.y1**0.35*regimen.Fr**0.43
    return ComponenteSocavacion(
        metodo='CSU MTC HHD / USACE', valor=ys,
        formula='ys=2*K1*K2*K3*K4*a^0.65*h^0.35*Fr^0.43; K2=(cos(theta)+min(l/a,12)*sin(theta))^0.65',
        intermedios={'K1':K1,'K2':K2,'K3':pilar.K3,'K4':pilar.K4,'a':pilar.ancho_a,
                     'l_a':relacion,'theta':theta,'h':hid.y1,'V':hid.V1,'Fr1':regimen.Fr,'ys':ys},
        referencias=['CSU81','CSU_CORRECCION','CSU_ALCANCE'],
        notas='HHD ec.81 imprime h/a; se implementa a/h de la fuente CSU USACE ec.10-6.',
        supuestos=['CSU sin truncamiento, decisión conservadora: USACE describe límites 2.4a/3a según Fr para nariz redonda alineada; revisar su aplicabilidad, no imponerlos a todo pilar.'],
        unidades={'K1':'1','K2':'1','K3':'1','K4':'1','a':'m','l_a':'1','theta':'grados','h':'m','V':'m/s','Fr1':'1','ys':'m'},
        fuentes_datos={**hid.fuentes,'K4':pilar.fuente_K4 or 'K4=1: sin reducción por armadura'},
    )
