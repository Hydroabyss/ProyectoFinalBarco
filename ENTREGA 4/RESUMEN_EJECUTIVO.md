# RESUMEN EJECUTIVO
## Análisis de Cuaderna Maestra - Buque Grupo 9

**Fecha:** 2025-11-20 08:53:59

---

## 3. INFORMACIÓN DEL BUQUE

| Parámetro | Valor |
|-----------|-------|
| Nombre | Buque de carga general - Grupo 9 |
| Tipo | Granelero / Carga general |
| Eslora entre perpendiculares (Lpp) | 105.20 m |
| Manga (B) | 15.99 m |
| Puntal (D) | 7.90 m |
| Calado (T) | 6.20 m |
| Material | AH36 |
| Sociedad de Clasificación | DNV |

---

## 2. ANÁLISIS DE RESISTENCIA ESTRUCTURAL

### 2.1 Presiones de Diseño

| Ubicación | Presión (kPa) | Estado |
|-----------|---------------|--------|
| Fondo | 62.34 | ✓ |
| Costado | 31.17 | ✓ |
| Cubierta | 10.00 | ✓ |

### 2.3 Esfuerzos Calculados

#### Forro Exterior
- **Esfuerzo de Von Mises:** 984.05 MPa
- **Factor de Seguridad:** 0.36
- **Estado:** ❌ NO CUMPLE

#### Fondo
- **Esfuerzo:** 212.14 MPa
- **Factor de Seguridad:** 1.67
- **Estado:** ✅ CUMPLE

#### Cubierta Principal
- **Esfuerzo:** 51.04 MPa
- **Factor de Seguridad:** 6.96
- **Estado:** ✅ CUMPLE

### 2.3 Módulo Resistente

- **Calculado:** 128.294 m³
- **Mínimo DNV:** 2522.062 m³
- **Estado:** ❌ NO CUMPLE

---

## 3. CONCLUSIONES

### ⚠️ REQUIERE REVISIÓN

El análisis indica que algunos elementos estructurales requieren revisión para cumplir con la normativa DNV.

**Elementos que no cumplen:**
- **Forro Exterior:** FS = 0.36 (requiere FS ≥ 1.5)
- **Módulo Resistente:** Déficit de 94.9%

**Recomendaciones:**
1. Aumentar el espesor de los elementos que no cumplen
2. Considerar refuerzos estructurales adicionales
3. Revisar el espaciado de cuadernas
4. Evaluar el uso de acero de mayor resistencia

---

## 4. DOCUMENTACIÓN GENERADA

### Reportes
- `ANALISIS_RESISTENCIA.md` - Análisis detallado de resistencia estructural
- `analisis_resistencia.json` - Datos en formato JSON

### Planos
- `graficos/plano_cargas_cuaderna.png` - Distribución de cargas
- `graficos/plano_esfuerzos_cuaderna.png` - Distribución de esfuerzos

---

## 5. DATOS TÉCNICOS

### Estructura de la Cuaderna Maestra

| Elemento | Dimensión | Valor |
|----------|-----------|-------|
| Altura doble fondo | h_df | {self.datos_buque['estructura']['doble_fondo']['altura_m']:.2f} m |
| Ancho doble costado | b_dc | {self.datos_buque['estructura']['doble_costado']['ancho_m']:.2f} m |
| Espaciado cuadernas | s | {self.datos_buque['estructura']['espaciado_cuadernas']['zona_central_mm']:,} mm |

### Espesores

| Elemento | Espesor (mm) |
|----------|--------------|
| Forro exterior | {self.datos_buque['estructura']['espesores']['forro_exterior_mm']} |
| Forro fondo | {self.datos_buque['estructura']['espesores']['forro_fondo_mm']} |
| Cubierta principal | {self.datos_buque['estructura']['espesores']['cubierta_principal_mm']} |
| Mamparos transversales | {self.datos_buque['estructura']['espesores']['mamparos_transversales_mm']} |

| Elemento | Espesor (mm) |
|----------|--------------|
| Forro exterior | {self.datos_buque['estructura']['espesores']['forro_exterior_mm']} |
| Forro fondo | {self.datos_buque['estructura']['espesores']['forro_fondo_mm']} |
| Cubierta principal | {self.datos_buque['estructura']['espesores']['cubierta_principal_mm']} |
| Mamparos transversales | {self.datos_buque['estructura']['espesores']['mamparos_transversales_mm']} |

---

**Generado automáticamente por el Sistema de Análisis de Cuaderna Maestra v2.0**
