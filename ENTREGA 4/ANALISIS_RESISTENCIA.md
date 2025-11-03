# ANÁLISIS DE RESISTENCIA ESTRUCTURAL
## Cuaderna Maestra - Buque Grupo 9

**Fecha:** 1762889340.450857

---

## 1. DATOS DEL BUQUE

### Dimensiones Principales
- **Eslora entre perpendiculares (Lpp):** 105.20 m
- **Manga (B):** 15.99 m
- **Puntal (D):** 7.90 m
- **Calado (T):** 6.20 m

### Material: AH36
- **Límite elástico:** 355 MPa
- **Módulo de Young:** 206 GPa
- **Coeficiente de Poisson:** 0.3

---

## 2. PRESIONES DE DISEÑO

| Ubicación | Presión (kPa) |
|-----------|---------------|
| Fondo | 62.34 |
| Costado | 31.17 |
| Cubierta | 10.00 |
| Bodega | 0.05 |

---

## 3. ESFUERZOS CALCULADOS

### Forro Exterior
- **Esfuerzo longitudinal:** 1039.04 MPa
- **Esfuerzo transversal:** 121.22 MPa
- **Esfuerzo de Von Mises:** 984.05 MPa
- **Factor de seguridad:** 0.36
- **Estado:** ❌ NO CUMPLE

### Fondo
- **Esfuerzo:** 212.14 MPa
- **Factor de seguridad:** 1.67
- **Estado:** ✅ CUMPLE

### Cubierta Principal
- **Esfuerzo:** 51.04 MPa
- **Factor de seguridad:** 6.96
- **Estado:** ✅ CUMPLE

---

## 4. MÓDULO RESISTENTE

- **Módulo resistente calculado:** 128.294 m³
- **Módulo resistente mínimo DNV:** 2522.062 m³
- **Margen:** -94.9%
- **Estado:** ❌ NO CUMPLE

---

## 5. CONCLUSIONES

### ⚠️ REQUIERE REVISIÓN

Algunos elementos no cumplen con los requisitos de resistencia.

**Acciones requeridas:**
- Aumentar espesor del forro exterior
- Aumentar el módulo resistente de la sección

---

## 6. PLANOS GENERADOS

- Plano de cargas: `graficos/plano_cargas_cuaderna.png`
- Plano de esfuerzos: `graficos/plano_esfuerzos_cuaderna.png`

---

**Generado automáticamente por el Sistema de Análisis de Resistencia Estructural**
