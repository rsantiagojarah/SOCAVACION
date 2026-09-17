# Cálculo de socavación por apoyo

Proyecto: Ejemplo sintético MTC trazable

Modo: trazable

Fecha: 2026-09-17 11:17

Procedimiento: LL granular MTC HHD ec.59 + local Froehlich/HIRE/CSU. MP 2018 artículos 1.2.3a, 1.2.4 y 2.4.3.8.3.4.

## Escenarios independientes


### Q100: 55.778 m³/s

| Apoyo | LP + LL (m) | Local (m) | Total (m) |
|---|---:|---:|---:|
| Estribo izquierdo | 2.533798 | 4.772455 | 7.306254 |
| Estribo derecho | 2.533798 | 4.772455 | 7.306254 |
| Pilar P1 sintético | 2.533798 | 2.966719 | 5.500517 |


### Q500: 87.392412 m³/s

| Apoyo | LP + LL (m) | Local (m) | Total (m) |
|---|---:|---:|---:|
| Estribo izquierdo | 3.417753 | 5.847213 | 9.264966 |
| Estribo derecho | 3.417753 | 5.847213 | 9.264966 |
| Pilar P1 sintético | 3.417753 | 3.371930 | 6.789683 |



LL incluye contracción. El cero del sumando de contracción independiente evita doble conteo; no significa contracción física nula.
LP es degradación independiente, sustentada; la agradación no reduce el diseño (criterio conservador de implementación).

## Envolventes por apoyo

| Apoyo | Diseño (m), escenario | Verificación (m), escenario | Z lecho socavado (m) | Límite fondo superficial Z <= (m) |
|---|---|---|---:|---:|
| Estribo izquierdo | 7.306254, Q100 | 9.264966, Q500 | 90.735034 | 89.735034 |
| Estribo derecho | 7.306254, Q100 | 9.264966, Q500 | 90.735034 | 89.735034 |
| Pilar P1 sintético | 5.500517, Q100 | 6.789683, Q500 | 93.010317 | 92.010317 |


Diseño: resistencia y servicio. Verificación: evento extremo. La cimentación requiere comprobación geotécnica y estructural.
Las etiquetas internas y_s_100/y_s_500 representan envolventes de cada condición; el desglose anterior conserva Q100 y Q500 originales.

## Compatibilidad geotécnica preliminar

| Control | Hidráulica | Geotecnia | Satisface |
|---|---|---|---|
| Cotas de pilares | Lecho y total por pilar | Cotas disponibles | Sí |
| Cota lecho socavado | Z_soc min = 90.74 m | Sondaje fondo = 85.00 m | Sí |
| Material residual bajo prisma | D50 hidráulico en cauce | EX-03: estrato ficticio, sin perforación ni ensayos reales. | Sí |
| Sondaje alcanza límite zapata (Art. 1.2.4) | Z_cim_min = 89.74 m | Fondo sondaje 85.00 m; no prueba competencia | Sí |
| Roca / erosionabilidad | Material erosionable asumido | No roca resistente declarada | Sí |


Controles geométricos preliminares satisfechos; falta verificar capacidad portante y estabilidad con el prisma retirado.

## Registro trazable

Versión: MTC-LL-2.0. Modo: trazable.
SHA256 entrada: `8118e2d2d297163c97417818b4615ba09a4ee8d0616f96dd9a650bf5060b4528`.
SHA256 código: `6cef5e8452685f499818c2bec3db64bcdc4138174e128834d1a9e015ddd5046e`.
LL granular homogéneo, flujo libre; requiere estudio hidráulico y granulometría; no calcula capacidad ni estabilidad de cimentación

### Fuentes contrastadas

HHD: Manual de hidrologiay drenaje MTC.pdf; SHA256 `0a1bdcd7c94016760642de91baf4d6e317e4cc85c529dfefae9a6bf76c8dcd88`; coincide: True.

MP: Manual de Puentes MTC 2018 (PGA).pdf; SHA256 `46d37849141b3acef44bdae112496dafbb5d6813dc008d5495c2f2bb760936b1`; coincide: True.

### Observaciones y datos pendientes

Sin campos pendientes detectados; esto no valida la evidencia ni elimina los supuestos de cada componente.


### Q100 / estribo izquierdo: Lischtvan-Levediev MTC HHD (general + contracción)

Lischtvan-Levediev MTC HHD (general + contracción)  
Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)  
Q = 55.778 m3/s  
h_m = 1.1 m  
B = 12.5 m  
Dm_mm = 2.95 mm  
beta = 1 1  
mu = 0.8833333333 1  
phi = 1 1  
x = 0.38 1 (z granular)  
alpha_c = 4.309635075 m^(1/3)/s (cierre SI)  
Hs = 3.433798474 m  
ds = 2.333798474 m  
h = 1.1 m  
alpha = 3.806844316 m^(1/3)/s (cierre SI)  
descenso_sin_truncar = 2.333798474 m  
luz_libre = 12.5 m  
V_mu = 4.056581818 m/s  
Resultado = 2.333798474 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MU13: HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Supuesto: Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.  
MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio.  

### Q100 / estribo izquierdo: Incluida en Lischtvan-Levediev MTC HHD

Incluida en Lischtvan-Levediev MTC HHD  
y_sc independiente = 0; contracción incluida mediante mu  
mu = 0.8833333333 1  
Resultado = 0 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MP123a: MP artículo 1.2.3a, página impresa 47 / PDF 51: escenarios y suma por apoyo  
Evita doble conteo de la contracción del puente.  

### Q100 / estribo izquierdo: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 1 1  
K2 = 1 1  
theta = 90 grados  
Fr_a = 1.234893184 1  
L_prima = 2 m  
ya = 1.1 m  
Ve = 4.056581818 m/s  
Ae = 2.2 m2  
Qe = 8.92448 m3/s  
ys = 4.772455279 m  
Resultado = 4.772455279 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q100 / estribo derecho: Lischtvan-Levediev MTC HHD (general + contracción)

Lischtvan-Levediev MTC HHD (general + contracción)  
Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)  
Q = 55.778 m3/s  
h_m = 1.1 m  
B = 12.5 m  
Dm_mm = 2.95 mm  
beta = 1 1  
mu = 0.8833333333 1  
phi = 1 1  
x = 0.38 1 (z granular)  
alpha_c = 4.309635075 m^(1/3)/s (cierre SI)  
Hs = 3.433798474 m  
ds = 2.333798474 m  
h = 1.1 m  
alpha = 3.806844316 m^(1/3)/s (cierre SI)  
descenso_sin_truncar = 2.333798474 m  
luz_libre = 12.5 m  
V_mu = 4.056581818 m/s  
Resultado = 2.333798474 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MU13: HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Supuesto: Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.  
MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio.  

### Q100 / estribo derecho: Incluida en Lischtvan-Levediev MTC HHD

Incluida en Lischtvan-Levediev MTC HHD  
y_sc independiente = 0; contracción incluida mediante mu  
mu = 0.8833333333 1  
Resultado = 0 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MP123a: MP artículo 1.2.3a, página impresa 47 / PDF 51: escenarios y suma por apoyo  
Evita doble conteo de la contracción del puente.  

### Q100 / estribo derecho: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 1 1  
K2 = 1 1  
theta = 90 grados  
Fr_a = 1.234893184 1  
L_prima = 2 m  
ya = 1.1 m  
Ve = 4.056581818 m/s  
Ae = 2.2 m2  
Qe = 8.92448 m3/s  
ys = 4.772455279 m  
Resultado = 4.772455279 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q100 / pilar P1 sintético: Lischtvan-Levediev MTC HHD (general + contracción)

Lischtvan-Levediev MTC HHD (general + contracción)  
Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)  
Q = 55.778 m3/s  
h_m = 1.1 m  
B = 12.5 m  
Dm_mm = 2.95 mm  
beta = 1 1  
mu = 0.8833333333 1  
phi = 1 1  
x = 0.38 1 (z granular)  
alpha_c = 4.309635075 m^(1/3)/s (cierre SI)  
Hs = 3.433798474 m  
ds = 2.333798474 m  
h = 1.1 m  
alpha = 3.806844316 m^(1/3)/s (cierre SI)  
descenso_sin_truncar = 2.333798474 m  
luz_libre = 12.5 m  
V_mu = 4.056581818 m/s  
Resultado = 2.333798474 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MU13: HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Supuesto: Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.  
MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio.  

### Q100 / pilar P1 sintético: CSU MTC HHD / USACE

CSU MTC HHD / USACE  
ys=2*K1*K2*K3*K4*a^0.65*h^0.35*Fr^0.43; K2=(cos(theta)+min(l/a,12)*sin(theta))^0.65  
K1 = 1 1  
K2 = 1.37707358 1  
K3 = 1.1 1  
K4 = 1 1  
a = 0.8 m  
l_a = 3.75 1  
theta = 10 grados  
h = 1.1 m  
V = 4.056581818 m/s  
Fr1 = 1.234893184 1  
ys = 2.966718895 m  
Resultado = 2.966718895 m  
Referencia CSU81: HHD §b.3.1.10, ecuaciones 81-82, Tablas 20-22, páginas impresas/PDF 136-138; ver discrepancia CSU  
Referencia CSU_CORRECCION: USACE HEC-RAS Hydraulic Reference Manual 4.1, ecuación 10-6: a^0.65*y1^0.35; https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_4.1_Reference_Manual.pdf  
Referencia CSU_ALCANCE: USACE HEC-RAS 6.4, Computing Pier Scour With The CSU Equation: límites restringidos a nariz redonda alineada; este motor conserva resultado sin truncamiento. https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.4/estimating-scour-at-bridges/computing-local-scour-at-piers/computing-pier-scour-with-the-csu-equation  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Dato K4: K4=1: sin reducción por armadura  
Supuesto: CSU sin truncamiento, decisión conservadora: USACE describe límites 2.4a/3a según Fr para nariz redonda alineada; revisar su aplicabilidad, no imponerlos a todo pilar.  
HHD ec.81 imprime h/a; se implementa a/h de la fuente CSU USACE ec.10-6.  

### Q500 / estribo izquierdo: Lischtvan-Levediev MTC HHD (general + contracción)

Lischtvan-Levediev MTC HHD (general + contracción)  
Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)  
Q = 87.392412 m3/s  
h_m = 1.371399 m  
B = 12.5 m  
Dm_mm = 2.95 mm  
beta = 1.05 1  
mu = 0.8833333333 1  
phi = 1 1  
x = 0.38 1 (z granular)  
alpha_c = 4.675550078 m^(1/3)/s (cierre SI)  
Hs = 4.589151593 m  
ds = 3.217752593 m  
h = 1.371399 m  
alpha = 4.130069236 m^(1/3)/s (cierre SI)  
descenso_sin_truncar = 3.217752593 m  
luz_libre = 12.5 m  
V_mu = 5.098000626 m/s  
Resultado = 3.217752593 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MU13: HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Supuesto: Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.  
MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio.  

### Q500 / estribo izquierdo: Incluida en Lischtvan-Levediev MTC HHD

Incluida en Lischtvan-Levediev MTC HHD  
y_sc independiente = 0; contracción incluida mediante mu  
mu = 0.8833333333 1  
Resultado = 0 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MP123a: MP artículo 1.2.3a, página impresa 47 / PDF 51: escenarios y suma por apoyo  
Evita doble conteo de la contracción del puente.  

### Q500 / estribo izquierdo: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 1 1  
K2 = 1 1  
theta = 90 grados  
Fr_a = 1.389899717 1  
L_prima = 2 m  
ya = 1.371399 m  
Ve = 5.098000626 m/s  
Ae = 2.742798 m2  
Qe = 13.98278592 m3/s  
ys = 5.847213224 m  
Resultado = 5.847213224 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q500 / estribo derecho: Lischtvan-Levediev MTC HHD (general + contracción)

Lischtvan-Levediev MTC HHD (general + contracción)  
Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)  
Q = 87.392412 m3/s  
h_m = 1.371399 m  
B = 12.5 m  
Dm_mm = 2.95 mm  
beta = 1.05 1  
mu = 0.8833333333 1  
phi = 1 1  
x = 0.38 1 (z granular)  
alpha_c = 4.675550078 m^(1/3)/s (cierre SI)  
Hs = 4.589151593 m  
ds = 3.217752593 m  
h = 1.371399 m  
alpha = 4.130069236 m^(1/3)/s (cierre SI)  
descenso_sin_truncar = 3.217752593 m  
luz_libre = 12.5 m  
V_mu = 5.098000626 m/s  
Resultado = 3.217752593 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MU13: HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Supuesto: Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.  
MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio.  

### Q500 / estribo derecho: Incluida en Lischtvan-Levediev MTC HHD

Incluida en Lischtvan-Levediev MTC HHD  
y_sc independiente = 0; contracción incluida mediante mu  
mu = 0.8833333333 1  
Resultado = 0 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MP123a: MP artículo 1.2.3a, página impresa 47 / PDF 51: escenarios y suma por apoyo  
Evita doble conteo de la contracción del puente.  

### Q500 / estribo derecho: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 1 1  
K2 = 1 1  
theta = 90 grados  
Fr_a = 1.389899717 1  
L_prima = 2 m  
ya = 1.371399 m  
Ve = 5.098000626 m/s  
Ae = 2.742798 m2  
Qe = 13.98278592 m3/s  
ys = 5.847213224 m  
Resultado = 5.847213224 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q500 / pilar P1 sintético: Lischtvan-Levediev MTC HHD (general + contracción)

Lischtvan-Levediev MTC HHD (general + contracción)  
Hs = [alpha_c*h^(5/3)/(0.68*beta*phi*Dm^0.28)]^(1/(1+x)); alpha_c = alpha/mu; alpha = Q/(B*hm^(5/3)) o dato sustentado; ds = max(Hs-h,0)  
Q = 87.392412 m3/s  
h_m = 1.371399 m  
B = 12.5 m  
Dm_mm = 2.95 mm  
beta = 1.05 1  
mu = 0.8833333333 1  
phi = 1 1  
x = 0.38 1 (z granular)  
alpha_c = 4.675550078 m^(1/3)/s (cierre SI)  
Hs = 4.589151593 m  
ds = 3.217752593 m  
h = 1.371399 m  
alpha = 4.130069236 m^(1/3)/s (cierre SI)  
descenso_sin_truncar = 3.217752593 m  
luz_libre = 12.5 m  
V_mu = 5.098000626 m/s  
Resultado = 3.217752593 m  
Referencia LL59: HHD §4.1.1.5.4 b.2.2, ecuación 59, página impresa/PDF 108; Dm en mm  
Referencia MU13: HHD Tabla 13, página impresa/PDF 107; interpolación lineal es criterio de implementación  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Supuesto: Cierre alpha=Q/(B*hm^(5/3)); distribución LL homogénea, sustentación requerida.  
MTC HHD: ecuación 59 p.108; Dm en mm, no en m como dice la Tabla 29. Incluye contracción del puente; no sumar y_sc de Laursen. Validar beta, mu, phi y Dm con el estudio.  

### Q500 / pilar P1 sintético: CSU MTC HHD / USACE

CSU MTC HHD / USACE  
ys=2*K1*K2*K3*K4*a^0.65*h^0.35*Fr^0.43; K2=(cos(theta)+min(l/a,12)*sin(theta))^0.65  
K1 = 1 1  
K2 = 1.37707358 1  
K3 = 1.1 1  
K4 = 1 1  
a = 0.8 m  
l_a = 3.75 1  
theta = 10 grados  
h = 1.371399 m  
V = 5.098000626 m/s  
Fr1 = 1.389899717 1  
ys = 3.371929992 m  
Resultado = 3.371929992 m  
Referencia CSU81: HHD §b.3.1.10, ecuaciones 81-82, Tablas 20-22, páginas impresas/PDF 136-138; ver discrepancia CSU  
Referencia CSU_CORRECCION: USACE HEC-RAS Hydraulic Reference Manual 4.1, ecuación 10-6: a^0.65*y1^0.35; https://www.hec.usace.army.mil/software/hec-ras/documentation/HEC-RAS_4.1_Reference_Manual.pdf  
Referencia CSU_ALCANCE: USACE HEC-RAS 6.4, Computing Pier Scour With The CSU Equation: límites restringidos a nariz redonda alineada; este motor conserva resultado sin truncamiento. https://www.hec.usace.army.mil/confluence/rasdocs/ras1dtechref/6.4/estimating-scour-at-bridges/computing-local-scour-at-piers/computing-pier-scour-with-the-csu-equation  
Dato hidraulica: EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.  
Dato geometria: EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.  
Dato granulometria: EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.  
Dato beta: EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.  
Dato exponente_x: EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.  
Dato phi: EX-06: phi=1 supuesto, sin estudio de carga sólida real.  
Dato luz_libre: EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).  
Dato cierre_alpha: EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.  
Dato local: EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.  
Dato pilar: EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura.  
Dato K4: K4=1: sin reducción por armadura  
Supuesto: CSU sin truncamiento, decisión conservadora: USACE describe límites 2.4a/3a según Fr para nariz redonda alineada; revisar su aplicabilidad, no imponerlos a todo pilar.  
HHD ec.81 imprime h/a; se implementa a/h de la fuente CSU USACE ec.10-6.  

### Entradas reproducibles (JSON)

```json
{
  "nombre": "Ejemplo sintético MTC trazable",
  "Q100": 55.778,
  "Q500": 87.392412,
  "Q_ot": null,
  "modo": "trazable",
  "material_lecho": "granular",
  "flujo": "libre",
  "lecho_homogeneo": true,
  "fuentes": {
    "hidrologia": "EX-01: caudales de ensayo tomados del escenario C=0.55 aportado por el usuario, sin validar hidrología.",
    "topografia": "EX-02: sección sintética rectangular B=12.5 m; cotas inventadas para verificar operaciones.",
    "geotecnia": "EX-03: lecho granular homogéneo ficticio; Dm=2.95 mm y D50=2.5 mm independientes.",
    "largo_plazo": "EX-04: LP=0.20 m supuesto sintético independiente de LL, no predicción morfológica."
  },
  "justificacion_sin_desbordamiento": "EX-01: se excluye desbordamiento sólo para este ensayo de software; estudiar rasante en proyecto real.",
  "estribo_izquierdo": {
    "lado": "izquierdo",
    "D50_mm": 2.5,
    "Z_lecho": 100.0,
    "q100": {
      "y1": 1.1,
      "V1": 4.05658181818,
      "W1": 12.5,
      "W2": 12.5,
      "Q1": 55.778,
      "Q2": 55.778,
      "y0": 1.1,
      "Sf": 0.045,
      "beta": 1.0,
      "phi": 1.0,
      "exponente_x": 0.38,
      "Dm_mm": 2.95,
      "h_local": 1.1,
      "Q_ll": 55.778,
      "B_ll": 12.5,
      "h_m_ll": 1.1,
      "luz_libre": 12.5,
      "V_mu": 4.05658181818,
      "Ae": 2.2,
      "Qe": 8.92448,
      "L_obstruida": 2.0,
      "fuentes": {
        "hidraulica": "EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.",
        "geometria": "EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.",
        "granulometria": "EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.",
        "beta": "EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.",
        "exponente_x": "EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.",
        "phi": "EX-06: phi=1 supuesto, sin estudio de carga sólida real.",
        "luz_libre": "EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).",
        "cierre_alpha": "EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.",
        "local": "EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.",
        "pilar": "EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura."
      }
    },
    "q500": {
      "y1": 1.371399,
      "V1": 5.09800062564,
      "W1": 12.5,
      "W2": 12.5,
      "Q1": 87.392412,
      "Q2": 87.392412,
      "y0": 1.371399,
      "Sf": 0.045,
      "beta": 1.05,
      "phi": 1.0,
      "exponente_x": 0.38,
      "Dm_mm": 2.95,
      "h_local": 1.371399,
      "Q_ll": 87.392412,
      "B_ll": 12.5,
      "h_m_ll": 1.371399,
      "luz_libre": 12.5,
      "V_mu": 5.09800062564,
      "Ae": 2.742798,
      "Qe": 13.98278592,
      "L_obstruida": 2.0,
      "fuentes": {
        "hidraulica": "EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.",
        "geometria": "EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.",
        "granulometria": "EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.",
        "beta": "EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.",
        "exponente_x": "EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.",
        "phi": "EX-06: phi=1 supuesto, sin estudio de carga sólida real.",
        "luz_libre": "EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).",
        "cierre_alpha": "EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.",
        "local": "EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.",
        "pilar": "EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura."
      }
    },
    "metodo_local": "froehlich",
    "L_prima": 2.0,
    "Ae": 2.0,
    "forma": "muro_vertical",
    "angulo_ataque": 90.0
  },
  "estribo_derecho": {
    "lado": "derecho",
    "D50_mm": 2.5,
    "Z_lecho": 100.0,
    "q100": {
      "y1": 1.1,
      "V1": 4.05658181818,
      "W1": 12.5,
      "W2": 12.5,
      "Q1": 55.778,
      "Q2": 55.778,
      "y0": 1.1,
      "Sf": 0.045,
      "beta": 1.0,
      "phi": 1.0,
      "exponente_x": 0.38,
      "Dm_mm": 2.95,
      "h_local": 1.1,
      "Q_ll": 55.778,
      "B_ll": 12.5,
      "h_m_ll": 1.1,
      "luz_libre": 12.5,
      "V_mu": 4.05658181818,
      "Ae": 2.2,
      "Qe": 8.92448,
      "L_obstruida": 2.0,
      "fuentes": {
        "hidraulica": "EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.",
        "geometria": "EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.",
        "granulometria": "EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.",
        "beta": "EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.",
        "exponente_x": "EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.",
        "phi": "EX-06: phi=1 supuesto, sin estudio de carga sólida real.",
        "luz_libre": "EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).",
        "cierre_alpha": "EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.",
        "local": "EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.",
        "pilar": "EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura."
      }
    },
    "q500": {
      "y1": 1.371399,
      "V1": 5.09800062564,
      "W1": 12.5,
      "W2": 12.5,
      "Q1": 87.392412,
      "Q2": 87.392412,
      "y0": 1.371399,
      "Sf": 0.045,
      "beta": 1.05,
      "phi": 1.0,
      "exponente_x": 0.38,
      "Dm_mm": 2.95,
      "h_local": 1.371399,
      "Q_ll": 87.392412,
      "B_ll": 12.5,
      "h_m_ll": 1.371399,
      "luz_libre": 12.5,
      "V_mu": 5.09800062564,
      "Ae": 2.742798,
      "Qe": 13.98278592,
      "L_obstruida": 2.0,
      "fuentes": {
        "hidraulica": "EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.",
        "geometria": "EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.",
        "granulometria": "EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.",
        "beta": "EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.",
        "exponente_x": "EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.",
        "phi": "EX-06: phi=1 supuesto, sin estudio de carga sólida real.",
        "luz_libre": "EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).",
        "cierre_alpha": "EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.",
        "local": "EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.",
        "pilar": "EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura."
      }
    },
    "metodo_local": "froehlich",
    "L_prima": 2.0,
    "Ae": 2.0,
    "forma": "muro_vertical",
    "angulo_ataque": 90.0
  },
  "pilares": [
    {
      "nombre": "P1 sintético",
      "ancho_a": 0.8,
      "forma": "circular",
      "angulo_ataque": 10.0,
      "q100": {
        "y1": 1.1,
        "V1": 4.05658181818,
        "W1": 12.5,
        "W2": 12.5,
        "Q1": 55.778,
        "Q2": 55.778,
        "y0": 1.1,
        "Sf": 0.045,
        "beta": 1.0,
        "phi": 1.0,
        "exponente_x": 0.38,
        "Dm_mm": 2.95,
        "h_local": 1.1,
        "Q_ll": 55.778,
        "B_ll": 12.5,
        "h_m_ll": 1.1,
        "luz_libre": 12.5,
        "V_mu": 4.05658181818,
        "Ae": 2.2,
        "Qe": 8.92448,
        "L_obstruida": 2.0,
        "fuentes": {
          "hidraulica": "EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.",
          "geometria": "EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.",
          "granulometria": "EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.",
          "beta": "EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.",
          "exponente_x": "EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.",
          "phi": "EX-06: phi=1 supuesto, sin estudio de carga sólida real.",
          "luz_libre": "EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).",
          "cierre_alpha": "EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.",
          "local": "EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.",
          "pilar": "EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura."
        }
      },
      "q500": {
        "y1": 1.371399,
        "V1": 5.09800062564,
        "W1": 12.5,
        "W2": 12.5,
        "Q1": 87.392412,
        "Q2": 87.392412,
        "y0": 1.371399,
        "Sf": 0.045,
        "beta": 1.05,
        "phi": 1.0,
        "exponente_x": 0.38,
        "Dm_mm": 2.95,
        "h_local": 1.371399,
        "Q_ll": 87.392412,
        "B_ll": 12.5,
        "h_m_ll": 1.371399,
        "luz_libre": 12.5,
        "V_mu": 5.09800062564,
        "Ae": 2.742798,
        "Qe": 13.98278592,
        "L_obstruida": 2.0,
        "fuentes": {
          "hidraulica": "EX-05: y100=1.1 m; y500=1.371399 m; V=Q/(12.5*y); Sf=0.045 adoptado. No modelo de puente.",
          "geometria": "EX-02: ancho rectangular 12.5 m; h_local=hm; L obstruida=2 m por estribo.",
          "granulometria": "EX-03: Dm=2.95 mm ficticio, distinto del D50=2.5 mm.",
          "beta": "EX-06: beta100=1.00 y beta500=1.05 son supuestos de prueba, no tabla de frecuencia validada.",
          "exponente_x": "EX-06: z=0.38 asumido para reproducir escenario; falta curva granulométrica real.",
          "phi": "EX-06: phi=1 supuesto, sin estudio de carga sólida real.",
          "luz_libre": "EX-02: luz libre mínima 12.5 m ficticia; mu calculado con Tabla 13 HHD p.107 y V_mu=Q/(12.5*y).",
          "cierre_alpha": "EX-05: cierre rectangular alpha=Q/(B*hm^(5/3)), mismo caudal/ancho/tirante por sección.",
          "local": "EX-07: Ae=L*y; Qe=Ae*V1 por distribución uniforme sintética, no Q1 del cauce completo.",
          "pilar": "EX-08: a=0.8 m, l=3 m, nariz circular, theta=10 grados, K3=1.1 lecho plano, K4=1 sin armadura."
        }
      },
      "Z_lecho": 99.8,
      "longitud_l": 3.0,
      "D50_mm": 2.5,
      "K3": 1.1,
      "K4": 1.0
    }
  ],
  "cauce": {
    "tipo": "degradacion",
    "y_sg_lp": 0.2,
    "notas": "EX-04: dato sintético; no utilizar para cimentación real."
  },
  "geotecnia": {
    "cota_sondaje_min": 85.0,
    "hay_estrato_competente": true,
    "roca_resistente": false,
    "tipo_cimentacion": "superficial",
    "descripcion_estrato": "EX-03: estrato ficticio, sin perforación ni ensayos reales."
  }
}
```
