"""Un único conjunto completo y reproducible para pruebas, nunca datos de campo."""
from pathlib import Path
from socavacion.input.loader import cargar_proyecto


def cargar_datos_prueba():
    path = Path(__file__).resolve().parents[3] / 'ejemplos' / 'puente_mtc_trazable.yaml'
    proyecto = cargar_proyecto(path)
    proyecto.nombre = 'Demo'
    proyecto.modo = 'preliminar'
    proyecto.datos_prueba = True
    return proyecto
