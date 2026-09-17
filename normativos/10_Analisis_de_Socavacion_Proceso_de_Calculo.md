# 10. ANÁLISIS DE SOCAVACIÓN

> DOCUMENTO HISTÓRICO NO RECTOR DEL MOTOR ACTUAL. Contiene criterios y fórmulas que no se deben usar como especificación de MTC-LL-2.0. Consultar [METODO_SOCAVACION_MTC_TRAZABLE.md](METODO_SOCAVACION_MTC_TRAZABLE.md), que identifica correcciones, fuentes y alcance. No sumar Laursen al LL con mu del motor vigente.

**Norma de referencia:** *Manual de Puentes MTC 2018*, Art. 1.2, 1.2.2a, 1.2.3, 1.2.3a, 1.2.4, 1.2.5, 1.2.6, 1.3.3 y 2.4.3.8.3.4 (AASHTO LRFD 2.6.4.4 / 3.7.5).  
**Métodos de cálculo:** HEC-18 (FHWA), HEC-20 y métodos complementarios de hidráulica fluvial (Lischtvan–Lebediev, Neill, Lacey).

---

## Criterio normativo MTC 2018 (Art. 1.2.3a)

La socavación de las fundaciones se investiga para **dos condiciones**:

| Condición | Caudal | Estado límite | Reserva |
|-----------|--------|---------------|---------|
| **Inundación de diseño** | La más severa entre \(T = 100\) años o una inundación de desbordamiento de menor recurrencia, si es más severa | Resistencia y Servicio | Sí. El material del prisma de socavación **no se considera** en el diseño |
| **Inundación de verificación (extraordinaria)** | No mayor de \(T = 500\) años, o desbordamiento de menor recurrencia si es más severa | Evento extremo | No se exige reserva adicional a la de estabilidad |

**Componentes obligatorios** (Art. 1.2.3a y 1.2.2):

\[
y_{s,\text{total}} = y_{sg} + y_{sc} + y_{sl}
\]

Donde:

- \(y_{sg}\): socavación general (variación del perfil longitudinal **sin** el puente).
- \(y_{sc}\): socavación por contracción (estribos en el cauce).
- \(y_{sl}\): socavación local (estribos y, si existen, pilares).

Si el tramo está cerca de confluencia, lago o mar, los cálculos se hacen con **niveles mínimos** en la desembocadura.

---

## Secuencia de cálculo

```text
1. Recopilar datos hidráulicos (HEC-RAS) y granulométricos
2. Clasificar el cauce (estable / degradación / agradación)  →  y_sg de largo plazo
3. Calcular socavación general de avenida                 →  y_sg
4. Distinguir lecho vivo vs. agua clara (Vc)
5. Calcular socavación por contracción                    →  y_sc
6. Calcular socavación local en estribos                  →  y_sl
7. Sumar para Q diseño (T=100) y Q extraordinario (T=500)
8. Obtener profundidad total por estribo
9. Calcular cota del lecho socavado
10. Fijar cota mínima de cimentación (Art. 1.2.4)
11. Verificar compatibilidad geológica-geotécnica
```

---

## 10.1 Información hidráulica y granulométrica utilizada

### 10.1.1 Datos de entrada hidráulicos

Provenientes del modelamiento del perfil de flujo (HEC-RAS o similar, Art. 1.2.2) en la sección del eje del puente, **sin puente** y **con puente**.

| Símbolo | Descripción | Unidad | Origen |
|---------|-------------|--------|--------|
| \(Q_{100}\) | Caudal de diseño para socavación | m³/s | Hidrología, \(T = 100\) años |
| \(Q_{500}\) | Caudal de verificación / extraordinario | m³/s | Hidrología, \(T = 500\) años |
| \(Q_{ot}\) | Caudal de desbordamiento (overtopping), si existe | m³/s | HEC-RAS |
| \(y_1\), \(Y\) | Tirante medio en la sección de aproximación | m | HEC-RAS |
| \(V_1\) | Velocidad media de aproximación | m/s | HEC-RAS |
| \(A_1\) | Área hidráulica de aproximación | m² | HEC-RAS |
| \(W_1\) o \(B_1\) | Ancho superficial de aproximación | m | HEC-RAS |
| \(q_1 = Q/W_1\) | Caudal unitario de aproximación | m²/s | Cálculo |
| \(W_2\) o \(B_2\) | Ancho bajo el puente (luz hidráulica) | m | Geometría del puente |
| \(Q_1\) | Caudal en el cauce principal, aproximación | m³/s | HEC-RAS |
| \(Q_2\) | Caudal que pasa por el cauce contraído | m³/s | HEC-RAS |
| \(S_f\) | Pendiente de la línea de energía | m/m | HEC-RAS |
| \(n\) | Coeficiente de Manning | — | Campo / calibración |
| \(Fr = V/\sqrt{gy}\) | Número de Froude | — | Cálculo |
| NAME | Nivel de aguas máximas extraordinarias | m s.n.m. | HEC-RAS, \(Q_{500}\) o el que defina el NAME |
| NAM | Nivel de aguas máximas (diseño) | m s.n.m. | HEC-RAS, \(Q_{100}\) |
| \(Z_{lecho}\) | Cota actual del lecho en cada estribo | m s.n.m. | Topografía |

**Regla de selección del caudal de cálculo (Art. 1.2.3a):**

\[
Q_{\text{diseño, soc}} = \max(Q_{100},\; Q_{ot}\text{ si es más severo})
\]

\[
Q_{\text{verif, soc}} = \max(Q_{500},\; Q_{ot}\text{ si es más severo y } T \le 500)
\]

> El periodo de retorno de la **cimentación** debe ser mayor que el usado para dimensionar el área de flujo confinada por el puente (Art. 1.2.2 y 1.2.3).

### 10.1.2 Datos granulométricos (Art. 1.2.2a)

**Muestreo mínimo:** cuatro puntos, una vez definido el eje:

1. Estribo izquierdo, en el eje.
2. Estribo derecho, en el eje.
3. \(B\) metros aguas arriba (\(B\) = ancho promedio del río).
4. \(0.5B\) metros aguas abajo.

En cada punto: prospección a cielo abierto **≥ 3.00 m**, muestra representativa de cada estrato.  
Si hay apoyos intermedios, muestrear en concordancia con Geología y Geotecnia.

| Símbolo | Descripción | Unidad |
|---------|-------------|--------|
| \(D_{16}\), \(D_{50}\), \(D_{84}\), \(D_{90}\) | Diámetros característicos | m o mm |
| \(D_m = 1.25\,D_{50}\) | Diámetro medio HEC-18 | m |
| \(\gamma_s\) | Peso específico del material | kN/m³ |
| \(G_s\) | Gravedad específica | — |
| \(\sigma = \sqrt{D_{84}/D_{16}}\) | Gradación | — |

**Peso específico típico** si no hay ensayo: \(\gamma_s = 26.5\) kN/m³ (\(G_s \approx 2.65\)).

### 10.1.3 Tabla resumen a completar en el estudio

| Parámetro | Estribo izquierdo | Estribo derecho | Eje / cauce |
|-----------|-------------------|-----------------|-------------|
| \(D_{50}\) (mm) | | | |
| \(D_{90}\) (mm) | | | |
| \(Z_{lecho}\) (m s.n.m.) | | | |
| \(y\) para \(Q_{100}\) (m) | | | |
| \(V\) para \(Q_{100}\) (m/s) | | | |
| \(y\) para \(Q_{500}\) (m) | | | |
| \(V\) para \(Q_{500}\) (m/s) | | | |

---

## 10.2 Estabilidad, degradación o agradación del cauce

Objetivo: cuantificar la **socavación (o depósito) de largo plazo** \(y_{sg,LP}\), independiente de la avenida de diseño. Es parte de la socavación general (Art. 1.2.3a).

### 10.2.1 Clasificación morfológica (Art. 1.2.2 y 1.2.5)

Evaluar en campo y gabinete:

- Tipo de cauce: recto, meándrico, trenzado, anastomosado.
- Llanuras de inundación, abanicos, deltas.
- Historial erosivo, meandros, evidencias de socavación en puentes vecinos.
- Aporte de escombros, palizadas, huaycos (Art. 1.2.1).
- Balance de Lane:

\[
Q_s \cdot D_{50} \;\propto\; Q_w \cdot S
\]

| Resultado | Interpretación | \(y_{sg,LP}\) |
|-----------|----------------|---------------|
| Aumento de \(Q_w\) o \(S\), o disminución de \(Q_s\) o \(D_{50}\) | **Degradación** (erosión de largo plazo) | Valor positivo, bajar el lecho |
| Disminución de \(Q_w\) o \(S\), o aumento de \(Q_s\) o \(D_{50}\) | **Agradación** (depósito) | Valor negativo; **no se usa para reducir** la socavación de diseño |
| Equilibrio | **Cauce estable** | \(y_{sg,LP} = 0\) |

### 10.2.2 Estimación de la degradación de largo plazo

Opciones, de mayor a menor rigor:

1. **Comparación de batimetrías / secciones históricas** (preferible):

\[
y_{sg,LP} = Z_{\text{lecho, antiguo}} - Z_{\text{lecho, actual}}
\quad \text{(promedio anual} \times \text{vida útil)}
\]

2. **HEC-20 / HEC-RAS sediment transport** (si hay datos de transporte).
3. **Criterio ingenieril conservador** cuando no hay datos: en cauces aluviales degradantes de costa/sierra, adoptar un rango de **0.30 a 1.00 m** justificado por geomorfología, **nunca menor que 0** para diseño.

> La agradación **no se descuenta** de \(y_{s,total}\) de diseño. Solo se reporta como fenómeno.

---

## 10.3 Socavación general

Es la erosión del lecho por la avenida, **sin** la presencia del puente (Art. 1.2.3a). Se calcula para \(Q_{100}\) y \(Q_{500}\).

### 10.3.1 Velocidad crítica y régimen del lecho (HEC-18)

\[
V_c = K_u \, y^{1/6} \, D_{50}^{1/3}
\]

- \(V_c\): velocidad crítica de inicio de movimiento (m/s).
- \(y\): tirante (m).
- \(D_{50}\): en metros.
- \(K_u = 6.19\) (SI).

| Comparación | Régimen | Implicación |
|-------------|---------|-------------|
| \(V > V_c\) | **Lecho vivo** (live-bed) | Hay transporte; la fosa tiende a rellenarse al bajar la avenida |
| \(V < V_c\) | **Agua clara** (clear-water) | No hay relleno; la fosa permanece |

### 10.3.2 Método de Lischtvan–Lebediev (uso habitual en Perú)

Tirante de equilibrio tras la socavación general:

\[
h_{sg} = A \cdot q^{x}
\]

\[
y_{sg} = h_{sg} - y_0 \qquad (y_{sg} \ge 0)
\]

- \(q = Q/W\): caudal unitario (m²/s).
- \(y_0\): tirante actual (m).
- \(A\), \(x\): función de \(D_{50}\) (tabla siguiente; interpolar).

| \(D_{50}\) (mm) | \(x\) | \(A\) |
|-----------------|-------|-------|
| 0.05 | 0.64 | 0.70 |
| 0.25 | 0.68 | 0.82 |
| 1.0 | 0.72 | 0.94 |
| 2.5 | 0.75 | 1.03 |
| 5.0 | 0.78 | 1.14 |
| 10 | 0.82 | 1.35 |
| 25 | 0.88 | 1.65 |
| 50 | 0.92 | 2.00 |
| 75 | 0.95 | 2.25 |
| 100 | 0.97 | 2.50 |
| 150 | 0.98 | 2.75 |
| 200 | 0.99 | 3.00 |

### 10.3.3 Método de Neill (verificación)

\[
\frac{y_2}{y_1} = \left(\frac{q_2}{q_1}\right)^{6/7}
\]

\[
y_{sg} = y_2 - y_1 \qquad (y_{sg} \ge 0)
\]

En cauce no contraído \(q_2 = q_1\) ⇒ \(y_{sg} = 0\) por este método; entonces la socavación general queda en el término de largo plazo y/o Lischtvan–Lebediev.

### 10.3.4 Método de Lacey (cauces aluviales, control)

\[
f = 1.76\sqrt{D_{50}} \qquad (D_{50}\text{ en mm})
\]

\[
R = 0.47\left(\frac{Q}{f}\right)^{1/3}
\]

\[
y_{sg} = R - y_0 \qquad (y_{sg} \ge 0)
\]

### 10.3.5 Valor de diseño de la socavación general

\[
y_{sg,\text{diseño}} = y_{sg,LP} + \max(y_{sg,\text{Lischtvan}},\; y_{sg,\text{Neill}},\; y_{sg,\text{Lacey}})
\]

Adoptar el **mayor valor razonable** y justificarlo. No promediar hacia abajo.

---

## 10.4 Socavación por contracción

Debida a la reducción de la sección por los estribos (Art. 1.2.3a). Método **Laursen / HEC-18**.

### 10.4.1 ¿Hay contracción?

Si \(W_2 \approx W_1\) (el puente no estrecha el cauce de avenida) ⇒ \(y_{sc} = 0\).  
El MTC exige calcularla cuando los estribos se ubican **en el cauce**.

### 10.4.2 Contracción en lecho vivo (Laursen)

Condición: \(V_1 > V_c\) en la aproximación.

\[
\frac{y_2}{y_1} = \left(\frac{Q_2}{Q_1}\right)^{6/7}\left(\frac{W_1}{W_2}\right)^{k_1}
\]

\[
y_{sc} = y_2 - y_0
\]

- \(y_1\): tirante medio en el cauce principal de aproximación (m).
- \(y_0\): tirante existente en la sección contraída, antes de la socavación (m).
- \(Q_1\): caudal en el cauce principal de aproximación (m³/s).
- \(Q_2\): caudal que pasa por el puente en el cauce contraído (m³/s).
- \(W_1\): ancho del cauce principal de aproximación (m).
- \(W_2\): ancho del cauce contraído bajo el puente (m).

Exponente \(k_1\) (función de \(V_*/\omega\)):

| \(V_*/\omega\) | \(k_1\) | Modo de transporte |
|----------------|---------|---------------------|
| < 0.50 | 0.59 | Mayormente contacto |
| 0.50 – 2.0 | interpolar 0.59 → 0.69 | Mixto |
| > 2.0 | 0.69 | Mayormente suspensión |

Velocidad de corte y velocidad de caída:

\[
V_* = \sqrt{g\, y_1\, S_f}
\]

\[
\omega \approx \frac{g}{18\nu}D_{50}^{2} \quad (D_{50} < 0.1\,\text{mm, Stokes})
\]

Para arenas y gravas usar diagrama de Richardson–McNown o fórmula de Rubey.

### 10.4.3 Contracción en agua clara (Laursen)

Condición: \(V_1 < V_c\).

\[
y_2 = \left[\frac{K_u\, Q_2^{2}}{D_m^{2/3}\, W_2^{2}}\right]^{3/7}
\]

\[
y_{sc} = y_2 - y_0 \qquad (y_{sc} \ge 0)
\]

- \(K_u = 0.025\) (SI, \(D_m\) en m, \(Q\) en m³/s, \(W\) en m).
- \(D_m = 1.25\, D_{50}\) (m).

**Límite:** \(y_{sc}\) en agua clara no debe superar el valor de lecho vivo equivalente. Si lo supera, usar el de lecho vivo.

### 10.4.4 Casos especiales

- **Contracción Comp. 1** (estribos en llanura, cauce principal no estrecha): usar \(W_1\), \(W_2\) del cauce principal.
- **Comp. 2** (estribos en el cauce principal): \(W_2\) = luz libre entre estribos (descontar espesor de pilares).
- **Comp. 3** (cauce muy ancho, estribos lejos): \(y_{sc}\) suele ser pequeña; verificar con HEC-RAS.

Si hay zapata sobre pilotes, el MTC (Art. 1.2.4) exige que la **cara superior de la zapata** quede por debajo de \(y_{sc}\), para no generar socavación local adicional.

---

## 10.5 Socavación local en los estribos

Método **HEC-18**. Calcular para cada estribo (izquierdo y derecho), porque \(L'\), \(y_a\) y \(Fr_a\) suelen diferir.

### 10.5.1 Longitud de embalse del estribo \(L'\)

\[
L' = \frac{A_e}{y_a}
\]

- \(A_e\): área de flujo obstruida por el estribo y su terraplén, en la sección de aproximación (m²).
- \(y_a\): tirante medio en la zona obstruida (m).

Si el estribo está en el cauce principal:

\[
L' \approx L_{\text{estribo}} + L_{\text{terraplén en el flujo}}
\]

medida perpendicular al flujo.

### 10.5.2 Número de Froude en el estribo

\[
Fr_a = \frac{V_e}{\sqrt{g\, y_a}}
\]

\(V_e = Q_e / A_e\): velocidad media del flujo obstruido.

### 10.5.3 Ecuación de Froehlich (HEC-18) — uso general

Aplicar cuando \(L'/y_a \le 25\):

\[
\frac{y_{sl}}{y_a} = 2.27\, K_1\, K_2 \left(\frac{L'}{y_a}\right)^{0.43} Fr_a^{0.61} + 1
\]

El término \(+1\) es el **envolvente** de diseño (HEC-18). Luego:

\[
y_{sl} = y_a \left[ 2.27\, K_1\, K_2 \left(\frac{L'}{y_a}\right)^{0.43} Fr_a^{0.61} + 1 \right]
\]

**\(K_1\) — forma del estribo**

| Forma | \(K_1\) |
|-------|---------|
| Estribo de muro vertical (wingwall vertical) | 1.00 |
| Estribo de muro vertical con aletas a 45° | 0.82 |
| Estribo de talud (spill-through) 2H:1V | 0.55 |
| Estribo de talud 3H:1V | ≈ 0.42 |

**\(K_2\) — ángulo de ataque**

\[
K_2 = \left(\frac{\theta}{90}\right)^{0.13}
\]

- \(\theta\): ángulo entre el eje del terraplén y el flujo (90° = estribo perpendicular).
- \(\theta > 90°\): estribo “apunta” aguas arriba (más severo).
- \(\theta < 90°\): menos severo.

### 10.5.4 Ecuación HIRE (HEC-18) — estribos largos

Aplicar cuando \(L'/y_1 > 25\):

\[
\frac{y_{sl}}{y_1} = 4\, Fr^{1/3} \frac{K_1}{0.55}\, K_2
\]

\(y_1\), \(Fr\): tirante y Froude en el cauce principal de aproximación junto al estribo.

### 10.5.5 Límite superior (HEC-18)

\[
y_{sl} \le 2.4\, K_1 \left(\frac{K_2}{0.55}\right) y_a \qquad \text{(lecho vivo)}
\]

\[
y_{sl} \le 2.2\, K_1 \left(\frac{K_2}{0.55}\right) y_a \qquad \text{(agua clara)}
\]

Si el valor calculado supera el límite, adoptar el límite.

### 10.5.6 Corrección por granulometría (opcional, conservadora)

En lechos gruesos (\(D_{50} > 2\) mm) algunos proyectistas aplican un factor \(K_4 < 1\) análogo al de pilares. **No reducir** \(y_{sl}\) salvo justificación explícita; el MTC prioriza la seguridad de la cimentación (Art. 1.2.3).

### 10.5.7 Si existen pilares

Aunque el numeral 10.5 pide estribos, el Art. 1.2.3a exige también socavación local en pilares (ecuación CSU / HEC-18):

\[
\frac{y_{s,\text{pil}}}{y_1} = 2.0\, K_1 K_2 K_3 K_4 \left(\frac{a}{y_1}\right)^{0.65} Fr_1^{0.43}
\]

\[
y_{s,\text{pil}} \le 2.4\, a \quad (\text{lecho vivo}), \qquad y_{s,\text{pil}} \le 3.0\, a \quad (\text{agua clara})
\]

- \(a\): ancho del pilar proyectado (m).
- \(K_1\) forma, \(K_2\) ataque, \(K_3\) lecho, \(K_4\) armadura del lecho.

---

## 10.6 Socavación total para el caudal de diseño

Caudal: \(Q_{\text{diseño, soc}}\) (en general \(Q_{100}\)).  
Estado límite: **Resistencia y Servicio** (Art. 2.4.3.8.3.4).  
El material encima de la línea de socavación total **se retira** del modelo de fundación.

Para cada estribo:

\[
y_{s,100} = y_{sg,100} + y_{sc,100} + y_{sl,100}
\]

| Componente | Estribo izquierdo (m) | Estribo derecho (m) |
|------------|----------------------|---------------------|
| Socavación general \(y_{sg,100}\) | | |
| Socavación por contracción \(y_{sc,100}\) | | |
| Socavación local \(y_{sl,100}\) | | |
| **Total \(y_{s,100}\)** | | |

---

## 10.7 Socavación total para el caudal extraordinario

Caudal: \(Q_{\text{verif, soc}}\) (en general \(Q_{500}\)).  
Estado límite: **Evento extremo** (Art. 1.2.3a y 2.4.3.8.3.4).  
No se exige reserva geotécnica adicional a la de estabilidad.

Repetir 10.3 a 10.5 con los parámetros hidráulicos de \(Q_{500}\):

\[
y_{s,500} = y_{sg,500} + y_{sc,500} + y_{sl,500}
\]

| Componente | Estribo izquierdo (m) | Estribo derecho (m) |
|------------|----------------------|---------------------|
| Socavación general \(y_{sg,500}\) | | |
| Socavación por contracción \(y_{sc,500}\) | | |
| Socavación local \(y_{sl,500}\) | | |
| **Total \(y_{s,500}\)** | | |

> \(y_{s,500}\) suele ser mayor que \(y_{s,100}\). La cota de cimentación se fija con el **máximo**.

---

## 10.8 Profundidad total de socavación por estribo

\[
y_{s,\text{estribo}} = \max(y_{s,100},\; y_{s,500})
\]

Reportar por separado:

| Estribo | \(y_{s,100}\) (m) | \(y_{s,500}\) (m) | **\(y_{s}\) de diseño (m)** |
|---------|-------------------|-------------------|------------------------------|
| Izquierdo (E-I) | | | \(\max\) |
| Derecho (E-D) | | | \(\max\) |

Esta es la **profundidad de socavación potencial total** exigida en el informe (Art. 1.2.6).

---

## 10.9 Cota final del lecho socavado

\[
Z_{\text{lecho, soc}} = Z_{\text{lecho, actual}} - y_{s,\text{estribo}}
\]

| Estribo | \(Z_{\text{lecho, actual}}\) (m s.n.m.) | \(y_{s}\) (m) | \(Z_{\text{lecho, soc}}\) (m s.n.m.) |
|---------|------------------------------------------|---------------|--------------------------------------|
| E-I | | | |
| E-D | | | |

Dibujar en el perfil del puente:

1. Lecho actual.
2. Línea de socavación general + contracción (nivel del lecho contraído).
3. Línea de socavación total (general + contracción + local) en cada apoyo.

---

## 10.10 Cota mínima recomendada de cimentación

Según Art. 1.2.4 del *Manual de Puentes MTC 2018*.

### 10.10.1 Cimentación superficial (zapata)

El fondo de la cimentación debe quedar **por debajo** de la socavación máxima, con **no menos de 1.00 m** de reserva:

\[
Z_{\text{cim, min}} = Z_{\text{lecho, soc}} - 1.00\,\text{m}
\]

Si apoya en **roca buena, resistente a la socavación**: se cimenta sobre la roca manteniendo su integridad (no aplica el 1.00 m en material erosionable, pero sí la verificación de que la roca no es erosionable).

### 10.10.2 Cimentación profunda (pilotes hincados, pilotes perforados)

La **longitud efectiva** del pilote se mide desde el nivel de socavación total máxima hasta la punta:

\[
L_{\text{efectiva}} = Z_{\text{lecho, soc}} - Z_{\text{punta}}
\]

La capacidad geotécnica (punta + fuste) se calcula **ignorando** el suelo dentro del prisma de socavación.

### 10.10.3 Zapata sobre pilotes

La cara superior de la zapata debe quedar **por debajo de la socavación por contracción** \(y_{sc}\) (Art. 1.2.4), para no obstruir el flujo ni generar socavación local extra.

### 10.10.4 Tabla de recomendación

| Estribo | Tipo de cimentación | \(Z_{\text{lecho, soc}}\) | Reserva (m) | **\(Z_{\text{cim, min}}\)** (m s.n.m.) |
|---------|---------------------|---------------------------|-------------|----------------------------------------|
| E-I | Superficial / profunda | | 1.00 (si superficial) | |
| E-D | Superficial / profunda | | 1.00 (si superficial) | |

Esta cota es la **profundidad mínima de desplante recomendable de los apoyos** (Art. 1.2.1 y 1.2.6).

---

## 10.11 Compatibilidad con el estudio geológico y geotécnico

El MTC exige diseño conjunto hidráulico–geotécnico–estructural (Art. 1.2.4 y 1.3.3). El nivel de cimentación debe estar **por debajo** de la socavación estimada.

### 10.11.1 Verificaciones

1. **Estratigrafía vs. \(Z_{\text{lecho, soc}}\)**  
   Identificar el material que queda **después** de retirar el prisma de socavación (SPT, clasificación SUCS, roca).

2. **Erosionabilidad del estrato de apoyo**
   - Suelos granulares / cohesivos blandos: erosionables → aplicar 10.10.1 o 10.10.2.
   - Roca meteorizada o fracturada: tratar como erosionable salvo ensayo / criterio geológico.
   - Roca sana: cimentación sobre roca; diseñar para no dañar la masa.

3. **Capacidad portante y estabilidad** con el lecho ya socavado:
   - Superficial: capacidad y deslizamiento/volteo con empotramiento reducido.
   - Profunda: fuste nulo desde \(Z_{\text{lecho}}\) hasta \(Z_{\text{lecho, soc}}\); revisar \(L_{\text{efectiva}}\), pandeo y \(P\)-\(\Delta\).

4. **Licuación y subpresión** (Art. 1.3.3): el diseño de la subestructura incluye socavación **y** subpresión.

5. **Consistencia de granulometría**  
   \(D_{50}\) hidráulico (calicatas de cauce, Art. 1.2.2a) vs. \(D_{50}\) de sondajes geotécnicos. Si el estrato profundo es más fino, **recalcular** \(y_{sg}\) y \(y_{sc}\) con el material más erosionable del prisma.

6. **Profundidad de exploración** (Art. 2.8.0.3)  
   Los sondajes deben superar la cota de socavación total más la longitud de empotramiento. Si el sondaje termina encima de \(Z_{\text{cim, min}}\), **no hay compatibilidad**: falta exploración.

### 10.11.2 Matriz de compatibilidad

| Ítem | Hidráulica | Geotecnia | ¿Compatible? |
|------|------------|-----------|--------------|
| Cota de lecho socavado | \(Z_{\text{lecho, soc}}\) | ¿Hay sondaje bajo esa cota? | Sí / No |
| Material residual | \(D_{50}\) del prisma | SPT / SUCS / RQD bajo \(Z_{\text{lecho, soc}}\) | Sí / No |
| Tipo de cimentación | Superficial vs. profunda según 10.10 | Recomendación geotécnica | Sí / No |
| Reserva 1.00 m | Art. 1.2.4 | Estrato competente a \(Z_{\text{cim, min}}\) | Sí / No |
| Zapata sobre pilotes | Cara superior < lecho contraído | Nivel de encepado | Sí / No |
| Roca | ¿Resistente a socavación? | Informe geológico | Sí / No |

Si algún ítem es **No**, se ajusta la cota de cimentación, el tipo de fundación o se profundizan los sondajes. No se reduce la socavación hidráulica para “hacerla calzar” con un sondaje corto.

---

## Hoja de cálculo compacta (por estribo y por caudal)

```text
DATOS
  Q, y1, V1, W1, W2, Q1, Q2, y0, Sf, D50, L', ya, Ve, K1, K2, Z_lecho

RÉGIMEN
  Vc = 6.19 * y1^(1/6) * D50^(1/3)     # D50 en metros
  si V1 > Vc → lecho vivo; si no → agua clara

GENERAL
  y_sg_LP = ...                        # 10.2
  y_sg_av = max(Lischtvan, Neill, Lacey)
  y_sg    = y_sg_LP + y_sg_av

CONTRACCIÓN
  lecho vivo: y2/y1 = (Q2/Q1)^(6/7) * (W1/W2)^k1
  agua clara: y2    = [0.025 * Q2^2 / (Dm^(2/3) * W2^2)]^(3/7)
  y_sc = max(y2 - y0, 0)

LOCAL ESTRIBO
  si L'/ya ≤ 25:  Froehlich (con +1)
  si L'/y1 > 25:  HIRE
  aplicar límite HEC-18
  y_sl = ...

TOTAL
  ys = y_sg + y_sc + y_sl

COTAS
  Z_lecho_soc = Z_lecho - ys
  Z_cim_min   = Z_lecho_soc - 1.00     # solo superficial
```

Repetir para \(Q_{100}\) y \(Q_{500}\). La cimentación usa \(\max(y_{s,100}, y_{s,500})\).

---

## Entregables mínimos del capítulo (Art. 1.2.6)

- Profundidad de socavación potencial total por apoyo y por caudal.
- Profundidad mínima recomendable de la cimentación según tipo.
- Perfil con lecho actual, lecho contraído y lecho de socavación total.
- Conclusión de compatibilidad con Geología y Geotecnia.
- Obras de protección / encauzamiento, si \(y_{s}\) o la movilidad del cauce lo exigen.

---

## Referencias normativas usadas en este procedimiento

1. MTC (2018). *Manual de Puentes*. Art. 1.2, 1.2.2a, 1.2.3, 1.2.3a, 1.2.4, 1.2.5, 1.2.6, 1.3.3, 2.4.3.8.3.4, 2.1.4.3.3.1.
2. AASHTO LRFD Bridge Design Specifications, Art. 2.6.4.4 y 3.7.5 (citados por el Manual MTC).
3. FHWA HEC-18. *Evaluating Scour at Bridges* (contracción Laursen; estribos Froehlich y HIRE; pilares CSU).
4. FHWA HEC-20. *Stream Stability at Highway Structures* (degradación / agradación).
5. Lischtvan–Lebediev; Neill; Lacey (socavación general en cauces aluviales, práctica peruana).
