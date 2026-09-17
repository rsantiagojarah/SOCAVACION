# Informe de Análisis de Socavación

**Proyecto:** Puente Rio Ejemplo  
**Fecha:** 2026-09-17 10:55  
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
| E-I | 22.317 | 25.166 | **25.166** | 2450.300 | 2425.134 | 2424.134 |
| E-D | 21.409 | 24.076 | **24.076** | 2450.100 | 2426.024 | 2425.024 |


---

## 3. Desglose por componente


### Q100 — Diseño (Q = 850.0 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 6.535 | 0.000 | 15.783 | 22.317 | lecho_vivo | Lischtvan-Levediev MTC HHD (general + contracción) |
| E-D | 6.249 | 0.000 | 15.160 | 21.409 | lecho_vivo | Lischtvan-Levediev MTC HHD (general + contracción) |





### Q500 — Verificación (Q = 1200.0 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 7.714 | 0.000 | 17.451 | 25.166 | lecho_vivo | Lischtvan-Levediev MTC HHD (general + contracción) |
| E-D | 7.353 | 0.000 | 16.723 | 24.076 | lecho_vivo | Lischtvan-Levediev MTC HHD (general + contracción) |






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
| Cota lecho socavado | Z_soc min = 2425.13 m | Sondaje fondo = 2445.00 m | No |
| Material residual bajo prisma | D50 hidráulico en cauce | Grava arenosa densa | Sí |
| Tipo de cimentación | superficial | Recomendación geotécnica alineada | Sí |
| Reserva 1.00 m (Art. 1.2.4) | Z_cim_min = 2424.13 m | Competente a 2445.00 m | No |
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