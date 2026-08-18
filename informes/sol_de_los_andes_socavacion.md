# Informe de Análisis de Socavación

**Proyecto:** sol de los andes  
**Fecha:** 2026-08-18 18:01  
**Norma:** Manual de Puentes MTC 2018 (Art. 1.2, 1.2.3a, 1.2.4, 1.2.6) / HEC-18

---

## 1. Caudales de cálculo

| Condición | Caudal (m³/s) |
|-----------|---------------|
| Diseño socavación | 100.00 |
| Verificación socavación | 500.00 |

---

## 2. Socavación total por estribo (10.8)

| Estribo | y_s Q100 (m) | y_s Q500 (m) | **y_s diseño (m)** | Z lecho actual | Z lecho soc | Z cim mín |
|---------|--------------|--------------|---------------------|----------------|-------------|-----------|
| E-I | 9.619 | 15.144 | **15.144** | 100.000 | 84.856 | 83.856 |
| E-D | 9.810 | 9.810 | **9.810** | 100.000 | 90.190 | 89.190 |


---

## 3. Desglose por componente


### Q100 — Diseño (Q = 100.0 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 5.810 | 0.000 | 3.809 | 9.619 | agua_clara | Neill |
| E-D | 5.810 | 0.000 | 4.000 | 9.810 | agua_clara | Neill |





### Q500 — Verificación (Q = 500.0 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 11.335 | 0.000 | 3.809 | 15.144 | agua_clara | Neill |
| E-D | 5.810 | 0.000 | 4.000 | 9.810 | agua_clara | Neill |






---

## 4. Clasificación del cauce (10.2)

- **Tipo:** estable
- **y_sg largo plazo:** 0.000 m


---

## 5. Cimentación recomendada (10.10)

- **Tipo:** superficial
- **Reserva superficial:** 1.00 m (Art. 1.2.4) cuando aplica material erosionable

---

## 6. Compatibilidad geológico-geotécnica (10.11)

| Ítem | Hidráulica | Geotecnia | Compatible |
|------|------------|-----------|------------|
| Cota lecho socavado | Z_soc min = 84.86 m | Sondaje fondo = 100.00 m | No |
| Material residual bajo prisma | D50 hidráulico en cauce | Estrato competente declarado | Sí |
| Tipo de cimentación | superficial | Recomendación geotécnica alineada | Sí |
| Reserva 1.00 m (Art. 1.2.4) | Z_cim_min = 83.86 m | Competente a 100.00 m | No |
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