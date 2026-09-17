# Informe de Análisis de Socavación

**Proyecto:** Puente Rio Ejemplo  
**Fecha:** 2026-09-13 22:49  
**Norma:** Manual de Puentes MTC 2018 (Art. 1.2, 1.2.3a, 1.2.4, 1.2.6) / HEC-18

---

## 1. Caudales de cálculo

| Condición | Caudal (m³/s) |
|-----------|---------------|
| Diseño socavación | 850.00 |
| Verificación socavación | 1200.00 |

---

## 2. Socavación total por estribo (10.8)

| Estribo | y_s Q100 (m) | y_s Q500 (m) | **y_s diseño (m)** | Z lecho actual | Z lecho soc | Z cim mín |
|---------|--------------|--------------|---------------------|----------------|-------------|-----------|
| E-I | 37.050 | 40.742 | **40.742** | 2450.300 | 2409.558 | 2408.558 |
| E-D | 38.101 | 41.668 | **41.668** | 2450.100 | 2408.432 | 2407.432 |


---

## 3. Desglose por componente


### Q100 — Diseño (Q = 850.0 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 6.832 | 0.596 | 29.622 | 37.050 | lecho_vivo | Lischtvan-Lebediev |
| E-D | 7.201 | 0.540 | 30.360 | 38.101 | lecho_vivo | Lischtvan-Lebediev |





### Q500 — Verificación (Q = 1200.0 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 8.516 | 1.317 | 30.909 | 40.742 | lecho_vivo | Lischtvan-Lebediev |
| E-D | 8.991 | 1.258 | 31.418 | 41.668 | lecho_vivo | Lischtvan-Lebediev |






---

## 4. Clasificación del cauce (10.2)

- **Tipo:** degradacion
- **y_sg largo plazo:** 0.500 m
  
- **Notas:** Cauce aluvial degradante

---

## 5. Cimentación recomendada (10.10)

- **Tipo:** superficial
- **Reserva superficial:** 1.00 m (Art. 1.2.4) cuando aplica material erosionable

---

## 6. Compatibilidad geológico-geotécnica (10.11)

| Ítem | Hidráulica | Geotecnia | Compatible |
|------|------------|-----------|------------|
| Cota lecho socavado | Z_soc min = 2408.43 m | Sondaje fondo = 2445.00 m | No |
| Material residual bajo prisma | D50 hidráulico en cauce | Grava arenosa densa | Sí |
| Tipo de cimentación | superficial | Recomendación geotécnica alineada | Sí |
| Reserva 1.00 m (Art. 1.2.4) | Z_cim_min = 2407.43 m | Competente a 2445.00 m | No |
| Roca / erosionabilidad | Material erosionable asumido | No roca resistente declarada | Sí |


**Conclusión:** Incompatibilidades detectadas: Cota lecho socavado, Reserva 1.00 m (Art. 1.2.4).

---

## 7. Referencias

1. MTC (2018). *Manual de Puentes*. Art. 1.2, 1.2.2a, 1.2.3, 1.2.3a, 1.2.4, 1.2.5, 1.2.6, 1.3.3, 2.4.3.8.3.4.
2. FHWA HEC-18. *Evaluating Scour at Bridges*.
3. FHWA HEC-20. *Stream Stability at Highway Structures*.
4. Lischtvan–Lebediev; Neill; Lacey (socavación general).

---

*Generado por socavacion v1.0*