"""Ingreso manual HEC-RAS para Froehlich; sin LL, pilares ni franjas."""
import math
from socavacion.domain.models import CondicionHidraulica
from socavacion.domain.observations import resumir_advertencias


ALCANCE = ('SOLO SOCAVACIÓN LOCAL por Froehlich en estribos. Socavación general, '
           'contracción y largo plazo NO EVALUADOS, no son cero. No determina '
           'socavación total, cota del lecho final ni profundidad de cimentación.')


def hidraulica_froehlich(*, Q, A, Ae, Qe, L, R=None, fuentes=None):
    """A y Q totales: control/contexto; Ae, Qe y L manuales: fórmula local."""
    if not all(math.isfinite(v) and v > 0 for v in (Q, A, Ae, Qe, L)):
        raise ValueError('Froehlich requiere Q, A, Ae, Qe y L positivos y finitos; no extrapolar a ausencia de obstrucción.')
    if Ae > A or Qe > Q:
        raise ValueError('El área/caudal obstruido Ae/Qe no puede superar A/Q de la sección.')
    datos = dict(area_hidraulica=A, Ae=Ae, Qe=Qe, L_obstruida=L,
                 fuentes=dict(fuentes or {}))
    if R is not None:
        datos['radio_hidraulico'] = R
    return CondicionHidraulica(**datos)


def validar_froehlich(proyecto):
    if proyecto.pilares or any(e.metodo_local != 'froehlich' for e in proyecto.estribos()):
        raise ValueError('Sólo Froehlich: no admite pilares ni HIRE; revise el alcance del archivo.')
    if proyecto.flujo != 'libre' or proyecto.material_lecho != 'granular' or not proyecto.lecho_homogeneo:
        raise ValueError('Fuera de alcance: flujo libre y lecho granular homogéneo; no aplicar a presión, detritos/huaycos, roca o cohesivos.')
    if proyecto.geotecnia.evaluar or proyecto.cauce.y_sg_lp != 0:
        raise ValueError('Sólo Froehlich: geotecnia debe quedar evaluar=false y no se incorpora largo plazo.')
    if proyecto.Q500 < proyecto.Q100:
        raise ValueError('Q500 < Q100: revisar hidrología.')
    if (proyecto.Q_ot is None) != (proyecto.T_ot is None):
        raise ValueError('Q_ot y T_ot se ingresan juntos, con hidráulica independiente.')
    if proyecto.datos_prueba and proyecto.modo != 'preliminar':
        raise ValueError('datos_prueba requiere modo preliminar.')
    pendientes = []
    if not proyecto.fuentes.get('hidrologia', '').strip():
        pendientes.append('Falta fuente del proyecto: hidrologia.')
    if proyecto.Q_ot is None and not proyecto.justificacion_sin_desbordamiento.strip():
        pendientes.append('Falta justificacion_sin_desbordamiento (MP 1.2.3a).')
    eventos = [('q100', proyecto.Q100), ('q500', proyecto.Q500)]
    if proyecto.Q_ot is not None:
        eventos.append(('qot', proyecto.Q_ot))
    for evento, Q in eventos:
        condiciones = []
        for e in proyecto.estribos():
            h = getattr(e, evento)
            if h is None:
                raise ValueError(f'{e.lado.value}/{evento}: falta hidráulica independiente.')
            for campo in ('area_hidraulica', 'Ae', 'Qe', 'L_obstruida'):
                v = getattr(h, campo)
                if v is None or not math.isfinite(v) or v <= 0:
                    raise ValueError(f'{e.lado.value}/{evento}: {campo} debe ser explícito y >0; no se estima por franjas.')
            if h.Ae > h.area_hidraulica or h.Qe > Q:
                raise ValueError(f'{e.lado.value}/{evento}: Ae>A o Qe>Q; revisar dominio hidráulico.')
            for campo in ('hidraulica', 'geometria', 'local'):
                if not h.fuentes.get(campo, '').strip():
                    pendientes.append(f'{e.lado.value}/{evento}: falta fuente {campo}.')
            condiciones.append(h)
        a, b = condiciones
        if not math.isclose(a.area_hidraulica, b.area_hidraulica, rel_tol=1e-8):
            raise ValueError(f'{evento}: ambos estribos deben referir a la misma sección total de aproximación A/Q.')
        if a.Ae+b.Ae > a.area_hidraulica*(1+1e-9) or a.Qe+b.Qe > Q*(1+1e-9):
            raise ValueError(f'{evento}: suma Ae o Qe de ambos estribos supera A o Q; revise solapamientos.')
    if proyecto.modo == 'trazable' and pendientes:
        raise ValueError('Datos insuficientes para modo trazable:\n' + '\n'.join(resumir_advertencias(pendientes)))
    if proyecto.datos_prueba:
        pendientes.insert(0, 'DATOS DE PRUEBA SINTÉTICOS: no usar para diseño ni construcción.')
    return [ALCANCE, *pendientes]
