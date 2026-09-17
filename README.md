# Socavación — Cálculo según Manual MTC 2018 / HEC-18

Aplicación de terminal en Python para el análisis de socavación en puentes, según el procedimiento del *Manual de Puentes MTC 2018* y métodos HEC-18 / HEC-20.

## Requisitos

- Python 3.10+
- Dependencias: `typer`, `pydantic`, `pyyaml`, `jinja2`, `python-docx`

## Instalación

```bash
cd SOCAVACION
pip install -e ".[dev]"
```

## Uso rápido

**Ingreso en terminal:**

```bash
socavacion
```

Pide los datos, calcula y muestra resultados. Subcomandos opcionales: `socavacion calc archivo.yaml`, `socavacion --help`.

**Desde YAML (opcional, recálculos):**

```bash
python -m socavacion init -o mi_proyecto.yaml
python -m socavacion calc mi_proyecto.yaml
```

**Prueba rápida con valores por defecto:**

```bash
python -m socavacion --demo
python -m socavacion calc --demo
```

**Memoria de cálculo en Word:**

```bash
python -m socavacion calc mi_proyecto.yaml --word informe.docx
python -m socavacion word mi_proyecto.yaml -o informe.docx
```

## Arquitectura

Monolito modular por fases:

| Fase | Módulos |
|------|---------|
| Ingreso | `input/loader`, `input/validator`, `input/wizard` |
| Cálculo | `core/regime`, `core/general/*`, `core/contraction`, `core/local_*`, `core/pipeline` |
| Resultados | `cli/display`, `cli/ascii_tables` |
| Reportes | `report/builder`, `report/docx_builder` |
| Geotecnia | `geotech/compatibility` |

Cada módulo tiene una sola responsabilidad y ≤350 líneas.

## Métodos implementados

- **General:** Lischtvan–Lebediev, Neill, Lacey + degradación LP
- **Contracción:** Laursen (lecho vivo / agua clara)
- **Local estribos:** Froehlich, HIRE, límites HEC-18
- **Local pilares:** CSU HEC-18
- **Totales:** Q100, Q500, max por estribo, cotas de cimentación
- **Geotecnia:** Matriz de compatibilidad 10.11

## Tests

```bash
pytest
```

## Ejemplo incluido

Ver [ejemplos/puente_ejemplo.yaml](ejemplos/puente_ejemplo.yaml).

## Referencias normativas

- Manual de Puentes MTC 2018 (Art. 1.2.x, 1.2.4, 1.2.6, 2.4.3.8.3.4)
- FHWA HEC-18, HEC-20
- Documento interno: `normativos/10_Analisis_de_Socavacion_Proceso_de_Calculo.md`
