# Socavación local en estribos — Froehlich / HEC-RAS manual

El ingreso nuevo calcula **sólo Froehlich en estribos**, con datos ingresados manualmente de HEC-RAS. No calcula LL, pilares ni franjas, y no impone una sección rectangular. El alcance implementado es flujo libre de agua y lecho granular homogéneo: una torrentera con detritos/huayco o un puente a presión requiere otro análisis.

Resultado: **socavación local**, no socavación total ni profundidad de cimentación. General, contracción y largo plazo quedan **NO EVALUADOS**, no cero. Las fórmulas se contrastaron con los PDF locales MTC.

La especificación rectora es [METODO_SOCAVACION_MTC_TRAZABLE.md](normativos/METODO_SOCAVACION_MTC_TRAZABLE.md): contiene páginas, ecuaciones, unidades, decisiones de implementación, discrepancias y limitaciones. No constituye aprobación de un proyecto ni verificación de vigencia legal.

## Instalación

Python 3.10+; dependencias en pyproject.toml.

```powershell
pip install -e ".[dev]"
```

## Ejecución reproducible

```powershell
python -B -m socavacion calc ejemplos/froehlich_hec_ras.yaml --quiet --export output/froehlich/ejemplo.md
python -B -m socavacion word ejemplos/froehlich_hec_ras.yaml -o output/froehlich/ejemplo.docx
```

Cada informe genera además un archivo `.auditoria.json` con entradas, fuentes declaradas, fórmulas, unidades, resultados y huellas SHA256 de manuales/código/entrada. El ejemplo es sintético; no usar sus cotas para construir. Mantener ambos PDF indicados por el usuario en `normativos/`.

- `modo: preliminar`: permite supuestos, mostrando los datos pendientes.
- `modo: trazable`: exige datos y fuentes explícitos y comprueba la identidad de los PDF; no autentica las evidencias declaradas ni certifica seguridad.

## Ingreso interactivo y proyectos existentes

### Pruebas rápidas con valores por defecto

Ejecutar un caso completo automáticamente, sin preguntas ni diálogo Word:

```powershell
python -B -m socavacion --demo
```

El ingreso normal ya muestra los valores por defecto entre corchetes. Enter los acepta; también puede escribir otro valor. No es necesario añadir `--ejemplo`:

```powershell
python -B -m socavacion
```

El ejemplo usa Q100=55.778 m³/s, Q500=87.392412 m³/s, A100=18 m², A500=28 m² y dos estribos asimétricos, **sin pilares**. Ae, Qe y L son datos sintéticos independientes; no se generan por reparto rectangular. R100=0.9 m y R500=1.2 m son sólo datos informativos. Las fuentes se identifican como ejemplos, no como un modelo HEC-RAS real. No evalúa desbordamiento por defecto.

El formulario normal, `ingresar`, `calc` sin archivo y `wizard` muestran estos valores. `--ejemplo` sigue disponible como alias explícito. Por ejemplo: `Q100 (m³/s) [55.778]:` y `Q500 (m³/s) [87.392412]:`.

El demo automático y el formulario precargado usan modo preliminar y guardan `datos_prueba: true` en el registro. Modificar valores no elimina esa marca. Los informes advierten que los datos son sintéticos y no se pueden usar para diseño/construcción. Para un proyecto real, usar `--en-blanco` o completar su archivo existente; no se reemplazan los valores de archivos existentes por el ejemplo. No combinar `--demo`/`--ejemplo`/`--en-blanco` con un archivo en `calc`.

Para elegir dónde exportar una prueba automática:

```powershell
python -B -m socavacion calc --demo --export informes/prueba_rapida.md
```

### Datos del proyecto

El formulario predeterminado pide únicamente:

- Por evento: Q total y área hidráulica activa A de la misma sección de aproximación; radio hidráulico R opcional.
- Por estribo: forma y ángulo theta (90° normal al flujo).
- Por estribo **y evento**: longitud obstruida proyectada L, área obstruida Ae y caudal obstruido Qe.
- Referencia del modelo/plan, River/Reach, RS y perfiles; referencia geométrica de los apoyos. Si no se evalúa desbordamiento, su justificación queda explícita o pendiente.

No se piden pendiente, Manning, ancho rectangular, Dm, D50, beta, mu, phi, exponente de LL ni datos de pilares. Kf se obtiene de la Tabla 27 y Ktheta=(theta/90)^0.13 de la ecuación 93. **Ae no es el área total A; Qe no es el caudal total Q.** Deben corresponder a la zona obstruida por cada estribo aguas arriba. Si faltan, el programa se detiene: no los inventa ni los reparte por franjas.

Secuencia de cálculo: he=Ae/L → Ve=Qe/Ae → Fre=Ve/sqrt(9.81 he) → ys=he[2.27 Kf Ktheta (L/he)^0.43 Fre^0.61+1]. Se conserva el término +1 de diseño. Cada estribo y avenida tienen sus propios datos. R=A/P se guarda y se muestra en la auditoría, **no interviene en Froehlich ni sustituye he**. Q/A sólo se muestra como velocidad informativa de sección; no sustituye Ve. No se resuelve hidráulica ni se reconstruye el perfil del río.

Para ingresar datos reales en el formulario básico sin valores sintéticos:

```powershell
python -B -m socavacion --en-blanco
```

Para habilitar elección de modo preliminar/trazable en un proyecto real:

```powershell
python -B -m socavacion --avanzado --en-blanco
```

`--avanzado` en un proyecto nuevo mantiene exclusivamente Froehlich; no activa LL, HIRE ni pilares. Los proyectos de prueba siguen siendo preliminares. `completar` reconoce el formato Froehlich y conserva sus datos. Los archivos históricos de cálculo completo se conservan con su alcance original, indicando ARCHIVO HISTÓRICO al editarlos: no se transforman ni descartan componentes silenciosamente.

Para completar un YAML/JSON anterior, con sus valores actuales mostrados para confirmar o modificar:

```powershell
python -B -m socavacion completar mi_proyecto.yaml --quiet
```

Se guarda una copia `mi_proyecto_completado.yaml`. Si el destino ya existe se solicita confirmación. `--quiet` evita las tablas finales y el diálogo Word, pero mantiene las preguntas de ingreso. Para elegir rutas:

```powershell
python -B -m socavacion completar mi_proyecto.yaml -o revisado.yaml --export informes/revisado.md --quiet
```

Enter acepta un valor mostrado; cuando un campo opcional no tiene valor, Enter lo deja pendiente. `?` permite quitar el valor de un campo opcional. Se acepta coma o punto decimal, sin separadores de miles. Valores no finitos, fuera de rango u opciones inválidas se vuelven a preguntar sin reiniciar todo el formulario. En modo trazable los datos y fuentes requeridos no se pueden omitir; si aún no se conocen, usar preliminar. La entrada nunca inventa fuentes ni presenta un valor predeterminado de LL como confirmado.

Las advertencias se agrupan de forma estable por proyecto/apoyo/avenida, separando datos de fuentes pendientes. Las hipótesis propias del método se muestran aparte. El detalle original sigue disponible en los informes y la auditoría JSON.

Use [froehlich_hec_ras.yaml](ejemplos/froehlich_hec_ras.yaml) como ejemplo del formato actual. `metodo_calculo: froehlich` identifica inequívocamente este alcance; `geotecnia.evaluar: false`. Los formatos anteriores y su motor completo siguen disponibles sólo para reproducir estudios históricos; no son el ingreso predeterminado.

## Método activo

Froehlich: HHD ecuaciones 92–94 y Tabla 27, pp.148–151. Q100, Q500 y desbordamiento se calculan con hidráulicas independientes; gobierna mayor **socavación local** por estribo, no mayor caudal. El MP 1.2.3a exige además los otros componentes para evaluar el puente integralmente: este modo sólo atiende el componente local solicitado.

La auditoría almacena `general`, `y_sc`, `y_s_total` y cotas como `null` (no evaluados). Los campos históricos de envolvente `y_s_100/y_s_500/y_s_diseno` representan aquí sólo el resultado local. No existe resultado de cimentación ni aprobación del diseño. El programa no valida C=0.55 ni produce un modelo de flujo.

## Pruebas

```powershell
python -B -m pytest -q -p no:cacheprovider
```

Pruebas del flujo actual: [test_froehlich_hec_ras.py](tests/test_froehlich_hec_ras.py). Se mantienen regresiones del motor histórico para preservar sus archivos.
