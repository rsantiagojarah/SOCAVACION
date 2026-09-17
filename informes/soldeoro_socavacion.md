# Informe de Análisis de Socavación

**Proyecto:** soldeoro  
**Fecha:** 2026-09-17 09:54  
**Norma:** Manual de Puentes MTC 2018 (Art. 1.2, 1.2.3a, 1.2.4, 1.2.6) / HEC-18

---

## 1. Caudales de cálculo

| Condición | Caudal (m³/s) |
|-----------|---------------|
| Diseño socavación | 136.50 |
| Verificación socavación | 136.50 |

---

## 2. Socavación total por estribo (10.8)

| Estribo | y_s Q100 (m) | y_s Q500 (m) | **y_s diseño (m)** | Z lecho actual | Z lecho soc | Z cim mín |
|---------|--------------|--------------|---------------------|----------------|-------------|-----------|
| E-I | 14.330 | 14.330 | **14.330** | 2000.000 | 1985.670 | 1984.670 |
| E-D | 14.330 | 14.330 | **14.330** | 2000.000 | 1985.670 | 1984.670 |


---

## 3. Desglose por componente


### Q100 — Diseño (Q = 136.5 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 6.388 | 0.000 | 7.942 | 14.330 | lecho_vivo | Lischtvan-Lebediev |
| E-D | 6.388 | 0.000 | 7.942 | 14.330 | lecho_vivo | Lischtvan-Lebediev |





### Q500 — Verificación (Q = 136.5 m³/s)

| Estribo | y_sg (m) | y_sc (m) | y_sl (m) | y_s (m) | Régimen | Método general |
|---------|----------|----------|----------|---------|---------|----------------|
| E-I | 6.388 | 0.000 | 7.942 | 14.330 | lecho_vivo | Lischtvan-Lebediev |
| E-D | 6.388 | 0.000 | 7.942 | 14.330 | lecho_vivo | Lischtvan-Lebediev |






---

## 4. Clasificación del cauce (10.2)

- **Tipo:** degradacion
- **y_sg largo plazo:** 1.820 m


---

## 5. Cimentación recomendada (10.10)

- **Tipo:** superficial
- **Reserva superficial:** 1.00 m (Art. 1.2.4) cuando aplica material erosionable

---

## 6. Compatibilidad geológico-geotécnica (10.11)

| Ítem | Hidráulica | Geotecnia | Compatible |
|------|------------|-----------|------------|
| Cota lecho socavado | Z_soc min = 1985.67 m | Sondaje fondo = 1996.00 m | No |
| Material residual bajo prisma | D50 hidráulico en cauce | Estrato competente declarado | Sí |
| Tipo de cimentación | superficial | Recomendación geotécnica alineada | Sí |
| Reserva 1.00 m (Art. 1.2.4) | Z_cim_min = 1984.67 m | Competente a 1996.00 m | No |
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