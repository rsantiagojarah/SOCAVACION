# Procedimiento trazable de socavación de puentes — MTC-FROEHLICH-3.0

## Alcance actual: sólo Froehlich, HEC-RAS manual

Esta actualización sustituye el ingreso rectangular predeterminado por datos manuales de HEC-RAS, exclusivamente para socavación **local en estribos**. No ejecuta Lischtvan–Levediev, HIRE, CSU, franjas ni pilares en los proyectos nuevos. El contenido que sigue bajo «Archivo histórico» documenta el motor anterior, conservado para reproducir sus archivos; no implica que se ejecute en el modo nuevo.

Entradas por avenida: Q total, A hidráulica activa y R opcional de la misma sección de aproximación. Entradas por estribo/avenida: Ae y Qe interceptados aguas arriba, L proyectada normal al flujo. Forma y ángulo son propios de cada estribo. No se supone sección rectangular ni velocidad homogénea entre apoyos. El responsable identifica modelo, plan, River/Reach, RS, perfiles y planos en las fuentes; el programa no autentica esa evidencia.

HHD pp.148–151, ecuaciones 92–94 y Tabla 27:

```
he = Ae/L
Ve = Qe/Ae
Fre = Ve/sqrt(9.81*he)
Ktheta = (theta/90)^0.13
ys = he * [2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61 + 1]
```

Kf: pared vertical 1.00; vertical con aletas 0.82; pendiente hacia el cauce 0.55. Se conserva +1 para diseño, sin topes arbitrarios. **R=A/P se guarda como dato informativo y no interviene en la ecuación.** A total y Q total controlan coherencia y dan Q/A informativo; no sustituyen Ae, Qe, he ni Ve. No se solicitan granulometría, coeficientes LL ni pendiente para evaluar esta fórmula. Su ausencia no demuestra aplicabilidad al material real.

Se requieren L>0, Ae>0, Qe>0; se rechaza ausencia de obstrucción, datos incompletos y sumas obstruidas superiores a A/Q de la sección común. No hay sustitución de Qe por Q, cálculo por franjas ni supuesto rectangular. El alcance se restringe a flujo libre de agua y lecho granular homogéneo; una torrentera con huayco/detritos, presión, roca, cohesivos o estratos requiere otro estudio.

MP art.1.2.3a (p.47 impresa/PDF51) exige considerar también socavación general y por contracción. **Este modo es una evaluación parcial, no socavación total del puente ni conformidad integral.** Se compara la severidad local por evento (Q100/Q500 y Qot de menor retorno si existe). General, contracción, total y cotas quedan `null` (NO EVALUADOS) en la auditoría, nunca cero. No se obtiene profundidad de cimentación. El registro conserva ecuación, coeficientes, sustituciones, unidades, fuentes y SHA256 de entradas, código y manuales.

Archivos principales: `input/wizard_froehlich.py`, `input/hec_ras.py`, rama `metodo_calculo=froehlich` en `core/pipeline.py`, `core/local_abutment.py`. Ejemplo: `ejemplos/froehlich_hec_ras.yaml`. Los informes Markdown y Word tienen una salida específica local, sin tablas de LL ni cimentación.

## Archivo histórico: procedimiento completo MTC-LL-2.1 (no activo en proyectos nuevos)

## Actualización: ingreso básico y revisión de Tabla 13

El formulario predeterminado reduce los datos repetidos mediante una sección rectangular con distribución uniforme confirmada. De Q, B y h obtiene V, alpha y las franjas obstruidas Ae=L*h y Qe=Q*L/B; no sustituye Qe por el caudal total. h_local=hm se registra como hipótesis, no se impone a un modelo hidráulico general. Es un cálculo preliminar de socavación; no solicita Sf ni sondajes ni comprueba geotecnia. Las cotas de cimentación quedan sin evaluar. Para estudios generales usar `--avanzado`; `completar` no transforma estudios existentes al modelo simplificado.

Automáticos: mu (Tabla13), factores geométricos de estribos (Tabla27/ec.93) y pilares (Tablas20–22/ec.82). K3 se selecciona según condición del lecho; dunas medianas adopta el extremo superior 1.2 del intervalo tabulado, criterio explícito. phi=1 y K4=1 son elecciones sin reducción, no una determinación del transporte o acorazamiento. Beta por avenida y z por material siguen siendo externos: no se identificó una tabla utilizable para automatizarlos en las páginas LL revisadas (105–109). No se inventan fuentes ni se declaran coeficientes universales MTC.

La revisión visual ampliada de HHD p.107 corrigió cinco celdas de la transcripción anterior de Tabla13: (V=1.5, luz=30) mu=.99; (2,52) .99; (2.5,42) .98; (2.5,63) .99; (2.5,106) 1.00. Se conserva el valor impreso, incluido su comportamiento no monótono. Los casos anteriores con V>4 m/s y luz=12.5 m no cambian. La versión del registro pasa a MTC-LL-2.1; los archivos de auditoría históricos identifican su código y no se reescriben automáticamente.

Revisión: 17-09-2026. Especificación del motor de este repositorio, contrastada con los dos PDF locales indicados por el usuario. No es un nuevo reglamento ni una certificación de conformidad integral del proyecto. Las ecuaciones hidráulicas se toman del Manual de Hidrología, Hidráulica y Drenaje (HHD); los escenarios, composición y criterios de cimentación, del Manual de Puentes 2018 (MP).

## 1. Fuentes y alcance

Las páginas PDF indicadas son posiciones desde 1 en el visor, no índices desde 0.

| ID del registro | Documento y localizador | Uso en código |
|---|---|---|
| LL59 | HHD §4.1.1.5.4, b.2.2, ecuaciones 58–59, pp.106–108 impresas/PDF | `core/general/lischtvan.py::calcular_mtc_hhd` |
| MU13 | HHD Tabla 13, p.107 impresa/PDF | `normative/mu.py::factor_mu` |
| F92 | HHD b.3.2.4, ecuaciones 92–94, Tabla 27, pp.148–151 impresas/PDF | `core/local_abutment.py` |
| H103 | HHD b.3.2.6, ecuación 103, pp.156–157 impresas/PDF | `core/local_abutment.py` |
| CSU81 | HHD b.3.1.10, ecuaciones 81–82, Tablas 20–22, pp.136–138 impresas/PDF | `core/local_pier.py` |
| CSU_CORRECCION | USACE HEC-RAS 4.1, ecuación 10-6 | Corrección expresa de la razón a/h en CSU |
| MP123a | MP art.1.2.3a, p.47 impresa / PDF51 | Escenarios y suma por apoyo |
| MP124 | MP art.1.2.4, pp.47–48 impresas / PDF51–52 | Cotas y controles geométricos |
| MP243834 | MP art.2.4.3.8.3.4, p.104 impresa / PDF108 | Estados límite |

Identidad de los documentos, comprobada en cada ejecución:

- HHD: `Manual de hidrologiay drenaje MTC.pdf`, SHA256 `0a1bdcd7c94016760642de91baf4d6e317e4cc85c529dfefae9a6bf76c8dcd88`.
- MP: `Manual de Puentes MTC 2018 (PGA).pdf`, SHA256 `46d37849141b3acef44bdae112496dafbb5d6813dc008d5495c2f2bb760936b1`.

El código cubre lecho granular homogéneo y flujo libre. Rechaza entradas declaradas como suelo cohesivo, roca del lecho, estratificación, flujo a presión o detritos. Puede estudiar la erosión de cobertura granular sobre una cimentación en roca, pero NO limita automáticamente la erosión a una cota de roca ni demuestra que esa roca sea resistente. No modela erosión de márgenes, migración del cauce, protecciones, grupos de pilares, cabezales expuestos ni interacciones de hoyos. Estos casos necesitan evaluación adicional.

## 2. Preparación y trazabilidad de los datos

Antes de calcular se deben disponer de hidrología, topografía, geometría del puente, modelo hidráulico, granulometría y estudio morfológico/geotécnico, conforme a MP 1.2.2a y 1.2.5. El motor **recibe** caudales e hidráulica: no genera lluvias, curva de frecuencia, coeficiente racional C, ni resuelve Manning/HEC-RAS. La pendiente del lecho no sustituye automáticamente la pendiente de energía `Sf`.

Cada dato debe tener valor, unidad, localización física, evento y procedencia. En YAML, `fuentes` debe indicar informe/versión, sección o plano, página, muestra o estación, fecha y responsable cuando corresponda. Las agrupaciones permitidas son:

- Proyecto: `hidrologia`, `topografia`, `geotecnia`, `largo_plazo`.
- Cada condición hidráulica: `hidraulica`, `geometria`, `granulometria`, `beta`, `exponente_x`, `phi`, `mu` o `luz_libre`, `alpha` o `cierre_alpha`, y `local` o `pilar`.

El programa comprueba presencia, consistencia básica y rangos; **no abre ni autentica los informes citados en esos campos**. Una cadena de texto no prueba la calidad del dato. El responsable debe revisar evidencia, dominio de aplicación e incertidumbre antes de usar el resultado.

`modo: preliminar` permite supuestos identificados y produce advertencias. `modo: trazable` exige datos y fuentes explícitos, hidráulica independiente del desbordamiento cuando exista y las mismas versiones PDF contrastadas. Ambos modos requieren revisión profesional; “trazable” no significa “aprobado”.

## 3. Escenarios por apoyo

Se calculan Q100 y Q500 con condiciones `q100` y `q500` propias. Si existe desbordamiento se ingresa `Q_ot`, `T_ot` y `qot` para CADA estribo/pilar; no se reutiliza silenciosamente la hidráulica de otra avenida. Si se omite, se requiere `justificacion_sin_desbordamiento` en modo trazable.

Diseño: comparar socavación de Q100 con Qot si T_ot < 100 años. Comprobación: comparar Q500 con Qot si T_ot < 500 años. Seleccionar por **mayor profundidad de socavación en cada apoyo**, no por mayor caudal. Un caudal menor puede generar condiciones hidráulicas más erosivas.

Q100 y Q500 son la elección base implementada para este proyecto. MP permite condiciones establecidas por el propietario y una avenida de comprobación de no más de 500 años; el programa no pretende imponer Q500 universalmente ni cubre otros períodos base configurables. Si se requieren, ampliar escenarios antes de utilizarlo.

## 4. General con contracción: Lischtvan–Levediev granular

HHD ecuación 59:

\[
H_s=\left[\frac{\alpha h^{5/3}}{0.68\,\beta\,\mu\,\varphi\,D_m^{0.28}}\right]^{1/(1+z)},
\qquad d_{LL}=\max(H_s-h,0).
\]

`Hs` es la profundidad total desde la superficie de agua hasta el fondo socavado; el descenso del lecho es `ds=Hs-h`, no Hs. El truncamiento a cero es una decisión conservadora de implementación y se conserva también el valor previo al truncamiento.

| Símbolo | Entrada | Unidad / criterio |
|---|---|---|
| h | `h_local` | m, tirante original de la franja/apoyo |
| hm | `h_m_ll` | m, tirante medio de la sección usada para alpha, NO necesariamente h |
| Q, B | `Q_ll`, `B_ll` | m³/s y m, sección consistente con hm |
| Dm | `Dm_mm` | mm, diámetro característico sustentado; no sustituir por D50 sin evidencia |
| beta | `beta` | coeficiente de frecuencia sustentado para la avenida |
| mu | `mu` o Tabla 13 | 0 < mu <= 1; no aplicarlo dos veces |
| phi | `phi` | >=1, transporte de sedimentos sustentado |
| z | `exponente_x` | adimensional; nombre histórico x, pero corresponde a z granular en ec.59 |

Se admite `alpha` sustentado externamente, **sin mu incluido**. Si no se proporciona se calcula el cierre:

\[
\alpha=Q_{LL}/(B_{LL}h_m^{5/3}),\qquad \alpha_c=\alpha/\mu.
\]

Este cierre representa una distribución LL simplificada y requiere justificación (`fuentes.cierre_alpha`); no se presenta como una ecuación numerada explícita del PDF. Para sección irregular debe justificarse la distribución por franjas o proporcionar alpha externo. En sección rectangular h=hm, se cancela el factor h^(5/3) y Hs depende del caudal unitario Q/B y los coeficientes. Las unidades de alpha de este cierre son m^(1/3)/s.

La ecuación se evalúa con alpha_c sin volver a colocar mu en el denominador. El registro conserva alpha, alpha_c, h, hm, Hs y ds. beta=1.05, z=0.38, Dm=2.95 mm y phi=1 son valores del escenario aportado, **no valores universales prescritos por el MTC**. No se ha automatizado una tabla beta/z no contrastada. Se exige indicar la fuente de esos valores.

### Tabla 13 y discrepancias documentales

Para calcular mu se necesitan `luz_libre` y `V_mu`, velocidad media de la sección. V_mu puede diferir de V1 local del pilar. En varios vanos, usar la luz libre mínima, no el ancho total del río; sin obstáculos se puede ingresar mu=1 con justificación.

La tabla se transcribió del PDF. La interpolación lineal entre nodos es decisión de implementación: luces 10–200 m sin extrapolación, velocidades <1 m/s dan mu=1, y velocidades >=4 m/s usan la fila rotulada >4 del original. Adoptar esa fila exactamente en 4 m/s y la interpolación 3.5–4 son decisiones explícitas, no instrucciones literales del manual. Fuera del rango de luz se necesita mu externo sustentado. No ingresar simultáneamente mu manual y luz_libre en modo trazable.

HHD p.108 define Dm en mm; la Tabla 29 de resumen indica m. Se prioriza la definición junto a ec.59 y NO se convierte Dm a metros en esa ecuación. Para el diagnóstico Vc, en cambio, D50 sí se convierte de mm a m.

El texto exige phi>=1 aunque su expresión empírica en función del peso de mezcla puede dar menos de 1 cerca del agua clara. Para no resolver esa inconsistencia silenciosamente, el motor exige phi externo >=1 y fuente; no estima carga sólida a partir de V/Vc.

## 5. Socavación local

### Estribos: Froehlich

HHD ecuaciones 92–94 y Tabla 27:

\[
h_e=A_e/L,\quad V_e=Q_e/A_e,\quad Fr_e=V_e/\sqrt{g h_e},
\]
\[
d_{local}=h_e[2.27K_f K_\theta(L/h_e)^{0.43}Fr_e^{0.61}+1],
\quad K_\theta=(\theta/90)^{0.13}.
\]

Qe, Ae y L representan la porción de flujo obstruida por ESE estribo, aguas arriba, por avenida. Q1 es el caudal principal y no sustituye Qe. `L_obstruida`, `Ae`, `Qe` por evento tienen prioridad sobre la geometría compartida del estribo. Se conserva +1 para diseño (HHD p.151); se eliminaron recortes arbitrarios 2.4/2.2 que no pertenecen a esta ecuación.

Kf: muro vertical 1; muro con aleros 0.82; talud hacia cauce 0.55. Los nombres históricos talud_2h1v y talud_3h1v se asocian a esa misma categoría: no hay un coeficiente 0.42 sustentado en Tabla 27. Theta se mide según HHD: 90° para estribo normal, menor si inclinado aguas abajo y mayor si inclinado aguas arriba. No confundir con el ángulo del pilar.

El modo preliminar puede usar Ve=V1 si falta Qe, dejando advertencia; el trazable exige Qe>0 y Ae>0. Ausencia de flujo obstruido requiere otro tratamiento, no aplicar automáticamente Froehlich con Qe=0.

### Estribos: HIRE

Selección explícita `metodo_local: hire`; HHD ec.103:

\[
d_{local}=4h_{pie}(K_f/0.55)K_\theta Fr_{pie}^{0.33}.
\]

Requiere `penetra_cauce: true`, `h_pie` y `V_pie` por evento. La penetración en el cauce principal procede de HHD p.156. El programa restringe además L/h_pie>25 como criterio de selección declarado; **no atribuye ese umbral al párrafo HIRE del PDF**, ni cambia automáticamente de Froehlich a HIRE sólo por L/h.

### Pilares: CSU con discrepancia identificada

HHD ec.81 imprime h/a; se implementa la razón a/h contrastada en [USACE HEC-RAS 4.1, ec.10-6](https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_4.1_Reference_Manual.pdf):

\[
d_{local}=2K_1K_2K_3K_4a^{0.65}h^{0.35}Fr^{0.43},
\quad K_2=[\cos\theta+\min(l/a,12)\sin\theta]^{0.65}.
\]

V1 y y1 son los valores directamente aguas arriba del pilar, no una media indiscriminada de cauce y planicies. `ancho_a` es el ancho real de nariz: no proyectarlo por sesgo y aplicar K2 nuevamente. El ángulo se mide respecto del flujo, cero alineado. Pilar sesgado requiere longitud_l. K1 sigue Tabla 20 para ángulo <5° y vale 1 en otro caso. K3=1.1 para lecho plano, hasta 1.3 según forma del lecho; K4=1 sin reducción. Una reducción K4 requiere fuente externa con granulometría y cálculo; el motor no implementa ni verifica el cálculo de armadura completo.

Se conserva CSU **sin truncamiento como decisión conservadora**. [USACE](https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.4/estimating-scour-at-bridges/computing-local-scour-at-piers/computing-pier-scour-with-the-csu-equation) describe límites 2.4a/3a según Fr para nariz redonda alineada; no son límites generales por clasificación agua clara/lecho vivo ni se imponen a pilares sesgados. Para aplicarlos u otras correcciones se requiere ampliar la decisión documentada.

## 6. Total y cimentaciones

Por escenario y por apoyo:

\[
d_{total}=\max(d_{LP},0)+d_{LL,con\ contraccion}+d_{local},
\qquad Z_{soc}=Z_{lecho}-d_{total}.
\]

LP debe proceder de un estudio independiente de degradación del perfil; no duplicar la misma erosión representada por LL. No se fija un rango universal 0.30–1.00 m. La agradación no reduce la profundidad adoptada, decisión conservadora del motor.

El componente independiente de contracción se registra como cero porque está incluido mediante mu; NO significa ausencia física de contracción. No sumar Laursen otra vez. Se suman componentes del mismo apoyo y evento, nunca máximos locales de apoyos distintos. Los pilares incluyen LL+LP+CSU, no sólo CSU.

MP 1.2.4: para zapata superficial se informa el límite `Z_fondo <= Z_soc_max - 1.00 m`. El nombre histórico `Z_cim_min` es un **límite superior de cota**, no una profundidad mínima expresada con signo contrario. Para pilotes se informa longitud desde lecho socavado hasta punta; para cabezal se comprueba cara superior bajo lecho con LL+LP, sin añadir el hoyo local. Esta última referencia usa LL general-contraído como aproximación identificada.

El fondo de un sondaje no demuestra que exista estrato competente a esa cota. Los controles son geométricos/preliminares y no aprueban capacidad portante, resistencia lateral ni estabilidad. Se exige diseño geotécnico y estructural retirando el prisma socavado. Cotas y evaluación geotécnica compartidas entre apoyos deben reemplazarse por controles específicos cuando difieran las cimentaciones.

## 7. Registro de auditoría y reproducción

Cada informe Markdown o Word genera un archivo hermano `.auditoria.json` que contiene:

- Entradas utilizadas, sus fuentes declaradas y modo de cálculo.
- Fórmulas, parámetros/intermedios numéricos, unidades, supuestos y referencias por componente, evento y apoyo.
- Resultados sin redondear para continuar cálculos, envolventes y cotas.
- SHA256 de la entrada JSON canónica, de cada archivo Python y del conjunto de código; SHA256 de ambos PDF.

Para reproducir una ejecución, conservar entrada, versión del repositorio, dependencias y documentos identificados; extraer `auditoria.entrada` como JSON y ejecutar `socavacion calc entrada.json`. Las fuentes PDF se buscan en `normativos` del repositorio; si falta o cambia un PDF, el modo trazable se detiene. El código no verifica actualidad legal o modificaciones normativas posteriores: corresponde al revisor confirmar la edición aplicable al contrato.

Compatibilidad: los campos históricos `y_s_100`/`y_s_500` en resultados finales de estribos contienen ahora las envolventes de diseño/comprobación, identificadas con `escenario_diseno`/`escenario_verificacion`; `y_s_diseno` histórico contiene el máximo de ambas. Q100/Q500 puros permanecen en `caudales`. Las API históricas Neill, Lacey, LL=Aq^x y Laursen se conservan, pero **NO forman parte del motor trazable ni quedan validadas por esta revisión**. Tampoco se usan sus aproximaciones de velocidad de caída.

## 8. Ejemplo y verificación

Ejecutar desde la raíz del repositorio:

```powershell
python -B -m socavacion calc ejemplos/puente_mtc_trazable.yaml --quiet --export output/revision_mtc/ejemplo.md
python -B -m pytest -q -p no:cacheprovider
```

`ejemplos/puente_mtc_trazable.yaml` es un caso SINTÉTICO completo para verificar software. EX-01 identifica caudales de ensayo; EX-02 geometría/cotas inventadas; EX-03 suelo ficticio; EX-04 LP supuesto; EX-05 hidráulica rectangular adoptada; EX-06 coeficientes supuestos; EX-07 flujo obstruido uniforme; EX-08 pilar sintético. Estas etiquetas no remiten a estudios reales. y100=1.1 m es adoptado, no una solución de Manning; y500 reproduce el escenario del usuario. Ningún resultado de ese puente sintético es una recomendación de cimentación real.

Comprobación aritmética independiente del escenario aportado: Q500=87.392412 m³/s; B=12.50 m; h=hm=1.371399 m; Dm=2.95 mm; beta=1.05; z=0.38; phi=1.

| Caso | mu | Hs (m) | Hs-h (m) |
|---|---:|---:|---:|
| Valor conservado | 0.89 | 4.564216 | 3.192817 |
| Luz libre=12.5 m y V>4 m/s | 0.8833333333 | 4.589152 | 3.217753 |

Estos resultados confirman operaciones, no C=0.55 ni Dm ni beta/z. El redondeo 3.25 m no es un factor de seguridad y no es la socavación total del puente. Las pruebas automatizadas contrastan también h distinto de hm, no doble aplicación de mu, Froehlich con Qe, HIRE, CSU/sesgo, escenarios de menor caudal más erosivos, cotas de pilares, rechazo de entradas y reproducción desde JSON/YAML.
