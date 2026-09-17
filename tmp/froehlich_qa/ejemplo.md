# Socavación local en estribos — Froehlich

Proyecto: Demo Froehlich HEC-RAS. Modo: preliminar. Fecha: 2026-09-17 13:39.

SOLO SOCAVACIÓN LOCAL por Froehlich en estribos. Socavación general, contracción y largo plazo NO EVALUADOS, no son cero. No determina socavación total, cota del lecho final ni profundidad de cimentación.

Método: MTC HHD, ecuaciones 92–94 y Tabla 27, pp.148–151.
Entrada manual de HEC-RAS; no se reconstruye la sección ni se calculan franjas.

## Procedimiento

1. Introducir Q y A de la misma sección activa de aproximación y evento. R es opcional e informativo.
2. Introducir L, Ae y Qe del flujo obstruido aguas arriba por cada estribo; no usar automáticamente el área o el caudal total.
3. Calcular he=Ae/L, Ve=Qe/Ae, Fre=Ve/sqrt(9.81 he).
4. Seleccionar Kf por forma (Tabla 27); Ktheta=(theta/90)^0.13 (ec.93).
5. Calcular ys=he[2.27 Kf Ktheta (L/he)^0.43 Fre^0.61 + 1] (ec.92, término +1 conservado).

R=A/P no sustituye he=Ae/L. La velocidad Q/A de sección tampoco sustituye Ve.

## Resultados locales por evento

| Evento | Estribo | he (m) | Ve (m/s) | Fre | Socavación local ys (m) |
|---|---|---:|---:|---:|---:|
| Q100 | izquierdo | 1.500000 | 2.666667 | 0.695166 | 4.586845 |
| Q100 | derecho | 1.222222 | 2.272727 | 0.656353 | 3.269075 |
| Q500 | izquierdo | 1.800000 | 2.888889 | 0.687480 | 5.544329 |
| Q500 | derecho | 1.600000 | 2.812500 | 0.709901 | 4.219461 |


## Envolventes exclusivamente locales

| Estribo | Q100/Qot local (m), evento | Q500/Qot local (m), evento | Máximo local (m) |
|---|---|---|---:|
| izquierdo | 4.586845, Q100 | 5.544329, Q500 | 5.544329 |
| derecho | 3.269075, Q100 | 4.219461, Q500 | 4.219461 |


MP 1.2.3a exige considerar también socavación general y contracción para evaluar la socavación total del puente.
Esta memoria sólo cubre el componente local solicitado. No verifica integralmente el diseño.
Si se incluye desbordamiento, se compara su severidad local para T_ot<100/T_ot<500, respectivamente.

Los campos históricos y_s_100/y_s_500/y_s_diseno de la auditoría representan aquí envolventes **locales**;
y_s_total, general, contracción y cotas se guardan como null (no evaluados), no como ceros.

Geotecnia: NO EVALUADA. No se calculan cotas ni reservas de cimentación.

## Registro trazable

Versión: MTC-FROEHLICH-3.0. Modo: preliminar.
SHA256 entrada: `bcb9af8e615a9664c6866e0d9996788d0e7fe8804fc95671181fcb0ea98e11a9`.
SHA256 código: `080c445b90fa149e3ab1c9adfaac0dd9bb4c12d65c939adbb03fb2c0e391dc14`.
SOLO SOCAVACIÓN LOCAL por Froehlich en estribos. Socavación general, contracción y largo plazo NO EVALUADOS, no son cero. No determina socavación total, cota del lecho final ni profundidad de cimentación.

### Fuentes contrastadas

HHD: Manual de hidrologiay drenaje MTC.pdf; SHA256 `0a1bdcd7c94016760642de91baf4d6e317e4cc85c529dfefae9a6bf76c8dcd88`; coincide: True.

MP: Manual de Puentes MTC 2018 (PGA).pdf; SHA256 `46d37849141b3acef44bdae112496dafbb5d6813dc008d5495c2f2bb760936b1`; coincide: True.

### Observaciones y datos pendientes

- ESCENARIO PRELIMINAR: incluye supuestos; no constituye aprobación del diseño.
- SOLO SOCAVACIÓN LOCAL por Froehlich en estribos. Socavación general, contracción y largo plazo NO EVALUADOS, no son cero. No determina socavación total, cota del lecho final ni profundidad de cimentación.
- DATOS DE PRUEBA SINTÉTICOS: no usar para diseño ni construcción.

### Q100 / estribo izquierdo: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 1 1  
K2 = 1 1  
theta = 90 grados  
Fr_a = 0.6951661218 1  
L_prima = 2 m  
ya = 1.5 m  
Ve = 2.666666667 m/s  
Ae = 3 m2  
Qe = 8 m3/s  
ys = 4.586844969 m  
A_total = 18 m2 (control)  
Q_total = 55.778 m3/s (control)  
V_media_seccion = 3.098777778 m/s (informativa; no sustituye Ve)  
R_informativo = 0.9 m (no interviene en Froehlich)  
Resultado = 4.586844969 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-F: sección y perfil sintéticos, no HEC-RAS real  
Dato geometria: EX-F: geometría sintética, sin levantamiento  
Dato local: EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q100 / estribo derecho: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 0.82 1  
K2 = 0.9848048349 1  
theta = 80 grados  
Fr_a = 0.6563533889 1  
L_prima = 1.8 m  
ya = 1.222222222 m  
Ve = 2.272727273 m/s  
Ae = 2.2 m2  
Qe = 5 m3/s  
ys = 3.269075325 m  
A_total = 18 m2 (control)  
Q_total = 55.778 m3/s (control)  
V_media_seccion = 3.098777778 m/s (informativa; no sustituye Ve)  
R_informativo = 0.9 m (no interviene en Froehlich)  
Resultado = 3.269075325 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-F: sección y perfil sintéticos, no HEC-RAS real  
Dato geometria: EX-F: geometría sintética, sin levantamiento  
Dato local: EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q500 / estribo izquierdo: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 1 1  
K2 = 1 1  
theta = 90 grados  
Fr_a = 0.6874800222 1  
L_prima = 2.5 m  
ya = 1.8 m  
Ve = 2.888888889 m/s  
Ae = 4.5 m2  
Qe = 13 m3/s  
ys = 5.544329323 m  
A_total = 28 m2 (control)  
Q_total = 87.392412 m3/s (control)  
V_media_seccion = 3.121157571 m/s (informativa; no sustituye Ve)  
R_informativo = 1.2 m (no interviene en Froehlich)  
Resultado = 5.544329323 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-F: sección y perfil sintéticos, no HEC-RAS real  
Dato geometria: EX-F: geometría sintética, sin levantamiento  
Dato local: EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Q500 / estribo derecho: Froehlich HEC-18 / MTC HHD

Froehlich HEC-18 / MTC HHD  
ys=he*[2.27*Kf*Ktheta*(L/he)^0.43*Fre^0.61+1]; he=Ae/L; Ve=Qe/Ae  
K1 = 0.82 1  
K2 = 0.9848048349 1  
theta = 80 grados  
Fr_a = 0.7099014056 1  
L_prima = 2 m  
ya = 1.6 m  
Ve = 2.8125 m/s  
Ae = 3.2 m2  
Qe = 9 m3/s  
ys = 4.219461212 m  
A_total = 28 m2 (control)  
Q_total = 87.392412 m3/s (control)  
V_media_seccion = 3.121157571 m/s (informativa; no sustituye Ve)  
R_informativo = 1.2 m (no interviene en Froehlich)  
Resultado = 4.219461212 m  
Referencia F92: HHD §b.3.2.4, ecuaciones 92-94, Tabla 27, páginas impresas/PDF 148-151  
Dato hidraulica: EX-F: sección y perfil sintéticos, no HEC-RAS real  
Dato geometria: EX-F: geometría sintética, sin levantamiento  
Dato local: EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas  
Se conserva +1 de Froehlich para diseño. Sin recorte 2.4/2.2 no sustentado.  

### Entradas reproducibles (JSON)

```json
{
  "nombre": "Demo Froehlich HEC-RAS",
  "Q100": 55.778,
  "Q500": 87.392412,
  "modo": "preliminar",
  "datos_prueba": true,
  "entrada_hidraulica": "hec_ras",
  "metodo_calculo": "froehlich",
  "fuentes": {
    "hidrologia": "EX-F: prueba de software, no estudio hidrológico"
  },
  "justificacion_sin_desbordamiento": "EX-F: omitido únicamente en el ensayo de software",
  "estribo_izquierdo": {
    "lado": "izquierdo",
    "q100": {
      "area_hidraulica": 18.0,
      "radio_hidraulico": 0.9,
      "Ae": 3.0,
      "Qe": 8.0,
      "L_obstruida": 2.0,
      "fuentes": {
        "hidraulica": "EX-F: sección y perfil sintéticos, no HEC-RAS real",
        "geometria": "EX-F: geometría sintética, sin levantamiento",
        "local": "EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas"
      }
    },
    "q500": {
      "area_hidraulica": 28.0,
      "radio_hidraulico": 1.2,
      "Ae": 4.5,
      "Qe": 13.0,
      "L_obstruida": 2.5,
      "fuentes": {
        "hidraulica": "EX-F: sección y perfil sintéticos, no HEC-RAS real",
        "geometria": "EX-F: geometría sintética, sin levantamiento",
        "local": "EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas"
      }
    },
    "L_prima": 2.0,
    "Ae": 3.0,
    "forma": "muro_vertical",
    "angulo_ataque": 90.0
  },
  "estribo_derecho": {
    "lado": "derecho",
    "q100": {
      "area_hidraulica": 18.0,
      "radio_hidraulico": 0.9,
      "Ae": 2.2,
      "Qe": 5.0,
      "L_obstruida": 1.8,
      "fuentes": {
        "hidraulica": "EX-F: sección y perfil sintéticos, no HEC-RAS real",
        "geometria": "EX-F: geometría sintética, sin levantamiento",
        "local": "EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas"
      }
    },
    "q500": {
      "area_hidraulica": 28.0,
      "radio_hidraulico": 1.2,
      "Ae": 3.2,
      "Qe": 9.0,
      "L_obstruida": 2.0,
      "fuentes": {
        "hidraulica": "EX-F: sección y perfil sintéticos, no HEC-RAS real",
        "geometria": "EX-F: geometría sintética, sin levantamiento",
        "local": "EX-F: Ae/Qe/L elegidos para ensayo, no derivados por franjas"
      }
    },
    "L_prima": 1.8,
    "Ae": 2.2,
    "forma": "muro_vertical_aletas_45",
    "angulo_ataque": 80.0
  },
  "pilares": [],
  "cauce": {},
  "geotecnia": {
    "evaluar": false,
    "hay_estrato_competente": false
  }
}
```
