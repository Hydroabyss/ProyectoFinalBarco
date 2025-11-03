# Guía del Corte Transversal - Cuaderna Maestra

## Información del Plano

**Archivo DXF:** `Corte_Transversal_Cuaderna_Maestra_Detallado.dxf`  
**Fecha de generación:** 3 de noviembre de 2025  
**Posición:** 50.3 m desde perpendicular de proa (Lpp/2)

---

## Descripción General

Este plano muestra el **corte transversal completo** de la cuaderna maestra del buque de carga general, incluyendo:

### ✅ Elementos Representados

1. **Contorno Exterior del Casco**
   - Forro de fondo (flat bottom)
   - Pantoque (bilge) con radio de curvatura realista (~0.80 m)
   - Forro de costado vertical
   - Cubierta principal

2. **Doble Fondo (h = 1.20 m)**
   - Chapa de fondo exterior (22 mm)
   - Varengas (transverse floors) con perfil T
   - Longitudinales de fondo
   - Chapa de fondo interior (14 mm)
   - Tanque de doble fondo para lastre/combustible

3. **Costados Dobles (w = 1.80 m cada lado)**
   - Forro de costado exterior (20 mm)
   - Cuadernas transversales con perfil T
   - Longitudinales de costado
   - Mamparos longitudinales internos (12 mm)
   - Wing tanks para combustible/lastre

4. **Bodega de Carga Central**
   - Ancho interior: 12.39 m
   - Altura libre: ~6.50 m (desde fondo interior a cubierta)
   - Volumen aproximado: ~78 m³ por metro de eslora

5. **Cubierta Principal (z = 7.90 m)**
   - Chapa de cubierta (12 mm estándar, 16 mm en escotillas)
   - Baos transversales con perfil T invertido
   - Refuerzos estructurales

---

## Capas del Dibujo (Layers)

| Capa | Color | Descripción | Uso |
|------|-------|-------------|-----|
| `CASCO_EXTERIOR` | Blanco (7) | Forro exterior | Contorno principal del casco |
| `ESTRUCTURA_PRIMARIA` | Rojo (1) | Varengas, cuadernas, baos | Estructura transversal principal |
| `ESTRUCTURA_SECUNDARIA` | Verde (3) | Longitudinales | Refuerzos longitudinales |
| `MAMPAROS` | Azul (5) | Mamparos internos | Separación de compartimentos |
| `TANQUES` | Cyan (4) | Límites de tanques | Zonas de almacenamiento |
| `LINEA_AGUA` | Magenta (6) | Línea de flotación | T = 6.20 m |
| `COTAS` | Amarillo (2) | Dimensiones | Acotación del plano |
| `TEXTO` | Gris (8) | Etiquetas y cajetín | Información textual |
| `EJES` | Gris claro (9) | Líneas de referencia | Base line, centerline |

---

## Dimensiones Principales

### Manga (Beam)
- **Manga total:** 15.99 m
- **Manga interior:** 12.39 m
- **Costado doble:** 1.80 m (cada lado)

### Puntal y Calado (Depth & Draft)
- **Puntal moldeado:** 7.90 m
- **Calado de diseño:** 6.20 m
- **Francobordo:** 1.70 m
- **Doble fondo:** 1.20 m

### Espaciamiento Estructural
- **Cuadernas (frames):** 0.70 m (700 mm)
- **Longitudinales:** Variable según zona

---

## Normativa Aplicada

### DNV-RU-SHIP Pt.3 Ch.2 - General Arrangement
- **Sec.3 [2.3]:** Altura mínima de doble fondo
  - Fórmula: hDB = B/20 = 15.99/20 = **0.78 m**
  - Adoptado: **1.20 m** ✅ (cumple y excede requisito)

- **Sec.3 [2.2]:** Extensión del doble fondo
  - Desde mamparo de colisión hasta mamparo de popa
  - Continuado hasta pantoque (turn of bilge) ✅

### DNV-RU-SHIP Pt.3 Ch.3 - Structural Design
- **Sec.2:** Arreglo estructural
- **Sec.7:** Idealización estructural
  - Espaciamiento de cuadernas: 0.70 m
  - Perfiles estructurales: T, Bulbo HP, L

### SOLAS Ch. II-1 - Construction
- **Reg.9:** Double bottoms in cargo ships ✅
- **Reg.13:** Damage stability requirements
  - Protección lateral mediante costados dobles ✅

---

## Materiales Estructurales

### Acero AH36
- **Límite elástico:** 355 MPa (N/mm²)
- **Resistencia a tracción:** 490-630 MPa
- **Elongación:** ≥21%
- **Aplicación:** Estructura principal del casco

### Espesores de Chapas
- Fondo exterior: 22 mm
- Costado: 20 mm
- Fondo interior: 14 mm
- Mamparos internos: 12 mm
- Cubierta: 12-16 mm

---

## Cómo Usar Este Plano

### Visualización en CAD
1. Abrir `Corte_Transversal_Cuaderna_Maestra_Detallado.dxf` en AutoCAD, QCAD, FreeCAD o similar
2. Activar/desactivar capas según necesidad de análisis
3. Usar layer `EJES` para referencias de medición
4. Layer `COTAS` muestra todas las dimensiones principales

### Análisis Estructural
- **Varengas (floors):** Color rojo, cada ~0.70 m transversalmente
- **Longitudinales:** Marcadores verdes, vista frontal
- **Cuadernas:** Perfiles verticales en costados
- **Baos:** Perfiles invertidos bajo cubierta

### Tanques y Compartimentos
- **Doble fondo:** Entre z=0 y z=1.20 m
- **Wing tanks:** Entre mamparos longitudinales y costado exterior
- **Bodega central:** Entre mamparos longitudinales internos

---

## Archivos Complementarios

1. **`Dimensiones_Estructurales_Detalladas.csv`**
   - Tabla detallada con todas las dimensiones
   - Referencias normativas para cada elemento
   - Valores calculados y adoptados

2. **`Resumen_Normativa_Cuaderna_Maestra.md`**
   - Resumen completo de normativa aplicada
   - Justificación de diseño estructural
   - Referencias DNV, SOLAS, y Maxsurf

---

## Notas Importantes

⚠️ **Este plano representa la cuaderna maestra en su posición de máxima sección transversal**

📍 **Posición:** 50.3 m desde proa (Lpp/2)

🔍 **Escala recomendada de impresión:** 1:50

📐 **Sistema de coordenadas:**
- Origen: Intersección de baseline, centerline, y perpendicular de popa
- Eje Y: Transversal (estribor positivo)
- Eje Z: Vertical (arriba positivo)

---

## Contacto y Revisiones

**Proyecto:** Diseño Naval - Buque de Carga General  
**Fecha:** 3 de noviembre de 2025  
**Revisión:** v1.0  
**Estado:** Preliminar - Sujeto a aprobación

---

*Generado automáticamente por el sistema de diseño naval*
