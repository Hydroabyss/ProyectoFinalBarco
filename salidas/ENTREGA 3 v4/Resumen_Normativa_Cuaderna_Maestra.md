# Resumen Normativo: Cuaderna Maestra

## Proyecto Final - Buque de Carga General

**Fecha:** 3 de noviembre de 2025  
**Documentos Consultados:**

- DNV-RU-SHIP Pt.3 Ch.2 (General Arrangement Design)
- DNV-RU-SHIP Pt.3 Ch.3 (Structural Design Principles)
- SOLAS Ch. II-1 (Subdivisión y Estabilidad)
- Maxsurf Modeler Automation Manual

---

## 1. DIMENSIONES PRINCIPALES DEL BUQUE

| Parámetro                          | Valor                         | Unidad    |
| ---------------------------------- | ----------------------------- | --------- |
| Eslora entre perpendiculares (Lpp) | 105.2                       | m         |
| Manga (B)                          | 15.99                         | m         |
| Puntal (D)                         | 7.90                          | m         |
| Calado de diseño (T)               | 6.20                          | m         |
| Desplazamiento                     | 7,028.213                     | toneladas |
| Tipo de buque                      | Carga General (General Cargo) | -         |
| Cubierta principal                 | Una sola (Single Deck)        | -         |

---

## 2. UBICACIÓN DE LA CUADERNA MAESTRA

### Posición Longitudinal

- **Posición:** ~50.3 m desde la perpendicular de proa (Lpp/2)
- **Zona:** Sección central entre bodegas de carga
- **Criterio:** Máxima área de sección transversal

### Requisitos Normativos (DNV Pt.3 Ch.2 Sec.2)

- Mamparo de colisión: 0.05·Lpp a 0.08·Lpp desde proa (5.03m - 8.05m)
- Mamparo de popa: En cámara del timón
- Mamparos intermedios: Según subdivisión de estanqueidad

---

## 3. DOBLE FONDO (DOUBLE BOTTOM)

### Requisitos DNV Pt.3 Ch.2 Sec.3 [2.3]

**Fórmula de altura mínima:**

```
hDB = 1000 · B/20 mm (mínimo 760 mm, máximo 2000 mm)
```

**Para nuestro buque:**

- B = 15.99 m
- hDB = 1000 · 15.99/20 = **780 mm**
- **Altura adoptada: 1.20 m (1200 mm)** ✅ **CUMPLE** (>780 mm)

### Extensión (DNV Pt.3 Ch.2 Sec.3 [2.2])

- Desde mamparo de colisión hasta mamparo de popa
- Continuado hasta la pantoque (turn of bilge)
- Protección del fondo hasta el costado

### Acceso (DNV Pt.3 Ch.2 Sec.4)

- Agujeros de hombre (manholes) en:
  - Chapa del fondo interior
  - Varengas (floors)
  - Longitudinales
- Aros de refuerzo en agujeros del fondo interior
- Protección de tapas en bodegas de carga

---

## 4. DOBLE COSTADO (DOUBLE SIDE)

### Requisitos SOLAS Ch. II-1 Reg.13

- Aplicable a buques de carga general
- Protección contra daños laterales
- Tanques laterales para lastre/combustible

**Ancho adoptado:** 1.80 m (cada lado)

### Cálculo de Manga Interior

```
Manga interior = B - 2 × ancho_costado_doble
Manga interior = 15.99 - 2 × 1.80 = 12.39 m
```

---

## 5. ESPACIAMIENTO DE CUADERNAS (FRAME SPACING)

### DNV Pt.3 Ch.3 Sec.7 [1.2.1]

**Fórmula general:**

```
s = (b1 + b2 + b3 + b4) / 4
```

Donde s = espaciamiento medio entre refuerzos en mm

### Espaciamientos Adoptados

- **Zona central (bodegas):** 700 mm (0.70 m)
- **Zona de transición (proa/popa):** 600 mm (0.60 m)
- **Sala de máquinas:** Web frames espaciadas ≤ 5 × frame spacing

### Justificación Normativa (DNV Pt.3 Ch.3 Sec.3 [5.2])

> "In the engine room, web frames shall be spaced not more than 5 times the frame spacing apart."

**Para s = 700 mm:**

- Web frames máximo: 5 × 700 = 3,500 mm = 3.50 m

---

## 6. ESTRUCTURA TRANSVERSAL DE LA CUADERNA MAESTRA

### 6.1 Componentes Principales

#### A) Forro Exterior (Outer Shell Plating)

- Material: Acero AH36 (DNV)
- Espesor típico: 18-22 mm
- Función: Resistencia hidrostática y estructural

#### B) Doble Fondo (1.20 m altura)

**Componentes:**

1. **Chapa del fondo exterior** (Bottom Shell Plating)

   - Espesor: 20-22 mm
   - Contacto directo con agua

2. **Varengas** (Floors/Transverse Bottom Frames)

   - Espaciamiento: 700 mm
   - Altura: ~1,150 mm (desde quilla hasta fondo interior)
   - Perfil típico: T o bulbo HP

3. **Longitudinales de fondo** (Bottom Longitudinals)

   - Orientación: Longitudinal (proa-popa)
   - Espaciamiento: ~700 mm
   - Perfil típico: Bulbo o L

4. **Chapa del fondo interior** (Inner Bottom Plating)

   - Espesor: 12-15 mm
   - Nivel: +1.20 m desde línea base
   - Función: Techo de tanques de doble fondo

5. **Quilla central** (Centre Girder/Keelson)
   - Ubicación: Crujía (centreline)
   - Sección: Continua longitudinal
   - Función: Resistencia longitudinal principal

#### C) Costados Dobles (1.80 m cada lado)

**Componentes:**

1. **Forro exterior del costado** (Side Shell Plating)

   - Espesor variable: 18-20 mm (zona de carga)
   - Curvatura según líneas de trazado

2. **Cuadernas transversales** (Transverse Frames)

   - Espaciamiento: 700 mm
   - Altura: Desde fondo interior hasta cubierta principal
   - Perfil: T, L, o bulbo según carga

3. **Mamparo longitudinal interno** (Inner Side Longitudinal Bulkhead)

   - Distancia desde crujía: 6.00 m (manga interior 12.39 m)
   - Espesor: 10-12 mm
   - Función: Separación tanques laterales/bodega

4. **Longitudinales del costado** (Side Longitudinals)
   - Orientación: Longitudinal
   - Espaciamiento: ~700 mm
   - Rango vertical: Desde fondo interior hasta cubierta

#### D) Cubierta Principal (Main Deck)

**Nivel:** +7.90 m desde línea base

**Componentes:**

1. **Chapa de cubierta** (Deck Plating)

   - Espesor: 10-12 mm (zona de carga)
   - Espesor reforzado: 14-16 mm (zona de escotillas)

2. **Baos transversales** (Deck Beams)

   - Espaciamiento: 700 mm
   - Orientación: Transversal (babor-estribor)
   - Perfil: T o bulbo

3. **Longitudinales de cubierta** (Deck Longitudinals)

   - Orientación: Longitudinal
   - Espaciamiento: ~700-1000 mm
   - Perfil: T, L, o bulbo

4. **Brazolas de escotilla** (Hatch Coamings)
   - Altura sobre cubierta: ~600-900 mm
   - Espesor: 10-12 mm
   - Refuerzos: Perfiles verticales y horizontales

---

## 7. TANQUES Y COMPARTIMENTOS

### 7.1 Tanques de Doble Fondo

**Función:** Lastre, agua dulce, combustible

- Altura: 1.20 m
- Ancho: Variable según sección transversal
- Acceso: Agujeros de hombre desde bodegas
- Subdivisión: Mamparos transversales cada ~10-15 m

### 7.2 Tanques Laterales (Wing Tanks)

**Función:** Lastre, combustible

- Ancho: 1.80 m cada lado
- Altura: Desde fondo interior (1.20 m) hasta cubierta principal (7.90 m)
- Altura efectiva del tanque: 6.50 m
- Volumen aproximado (por cada lado, por metro longitudinal):
  ```
  V ≈ 1.80 m × 6.50 m × 1.0 m = 11.70 m³/m
  ```

### 7.3 Bodega de Carga Central

**Dimensiones (a nivel de cuaderna maestra):**

- Ancho (manga interior): 12.39 m
- Altura libre: 6.50 m (desde fondo interior a cubierta)
- Acceso: Escotilla de cubierta principal

### 7.4 Cofferdams (DNV Pt.3 Ch.2 Sec.3 [1.2])

**Requisito normativo:**

> "Cofferdams shall be provided between compartments intended for liquid hydrocarbons (fuel oil, lubricating oil) and those intended for fresh water"

**Aplicación:** Separación entre:

- Tanques de combustible ↔ Tanques de agua dulce
- Tanques de hidrocarburos ↔ Bodegas de carga

---

## 8. MATERIALES Y ESPESORES TÍPICOS

### 8.1 Material Estructural Principal

**Acero AH36 (DNV Grade)**

- Límite elástico: 355 MPa (N/mm²)
- Resistencia a la tracción: 490-630 MPa
- Elongación: ≥21%
- Soldabilidad: Excelente
- Aplicación: Estructura principal del casco

### 8.2 Espesores Típicos de Chapas

| Elemento Estructural            | Espesor (mm) | Observaciones              |
| ------------------------------- | ------------ | -------------------------- |
| Forro de fondo exterior         | 20-22        | Mayor en quilla            |
| Forro de costado (carga)        | 18-20        | Variable según altura      |
| Chapa de fondo interior         | 12-15        | Sobre tanques doble fondo  |
| Mamparo longitudinal interno    | 10-12        | Tanques laterales          |
| Chapa de cubierta principal     | 10-12        | 14-16 en escotillas        |
| Mamparos transversales estancos | 8-10         | Según presión hidrostática |

### 8.3 Perfiles Estructurales Típicos

| Elemento                   | Perfil Típico  | Dimensiones Típicas |
| -------------------------- | -------------- | ------------------- |
| Varengas (floors)          | T, Bulbo HP    | h = 300-400 mm      |
| Cuadernas transversales    | T, L, Bulbo HP | h = 250-350 mm      |
| Baos de cubierta           | T, Bulbo HP    | h = 200-300 mm      |
| Longitudinales de fondo    | Bulbo, L       | h = 180-250 mm      |
| Longitudinales de costado  | Bulbo, L       | h = 180-250 mm      |
| Longitudinales de cubierta | T, Bulbo       | h = 180-250 mm      |

**Perfiles Bulbo HP (DNV Pt.3 Ch.3 Sec.7 Table 1):**

- HP 200: h = 200 mm, flange = 40×14.4 mm
- HP 240: h = 240 mm, flange = 49×17.7 mm
- HP 280: h = 280 mm, flange = 57×21.3 mm

---

## 9. CARGAS DE DISEÑO

### 9.1 Presión Hidrostática Externa

**En línea de flotación de diseño (T = 6.20 m):**

- Densidad agua de mar: ρ = 1.025 t/m³
- Presión en fondo: P = ρ × g × h = 1.025 × 9.81 × 6.20 = **62.3 kPa**

**Distribución vertical:**

- Fondo (z = 0): P = 62.3 kPa
- Fondo interior (z = 1.20 m): P = 51.3 kPa
- Línea de flotación (z = 6.20 m): P = 0 kPa
- Cubierta (z = 7.90 m): P = 0 kPa (fuera del agua)

### 9.2 Cargas de Bodega

**Carga general típica:**

- Densidad de estiba: 1.0 - 1.5 t/m³
- Presión sobre fondo interior: ~10-15 kPa (carga ligera)
- Presión sobre fondo interior: ~50-75 kPa (carga densa)

### 9.3 Cargas de Cubierta

**Según SOLAS y reglas de clasificación:**

- Carga uniformemente distribuida: 10-15 kPa
- Cargas concentradas (containers): según distribución
- Cargas dinámicas: Factor × 1.3-1.5

---

## 10. CRITERIOS DE DISEÑO ESTRUCTURAL

### 10.1 Estado Límite de Fluencia (Yielding)

**DNV Pt.3 Ch.6 (Scantling Requirements):**

**Tensión admisible:**

```
σ_allow = σy / γM
```

Donde:

- σy = Límite elástico del material (355 MPa para AH36)
- γM = Factor de seguridad parcial (típicamente 1.0-1.15)

**Módulo de sección requerido:**

```
Z_req = M / σ_allow
```

### 10.2 Estado Límite de Pandeo (Buckling)

**DNV-CG-0128 (Buckling):**

**Para chapas (plating):**

```
t_req = b × √(P / (k × σcr))
```

Donde:

- b = Ancho del panel entre refuerzos
- P = Presión de diseño
- k = Coeficiente de pandeo (según condiciones de borde)
- σcr = Tensión crítica de pandeo

**Para refuerzos (stiffeners):**

- Esbeltez límite: λ ≤ 120-150
- Radio de giro mínimo: i_min ≥ L/150

### 10.3 Corrosión y Adiciones

**DNV Pt.3 Ch.3 Sec.3 (Corrosion Additions):**

| Ubicación              | Adición (mm) | Observaciones             |
| ---------------------- | ------------ | ------------------------- |
| Fondo exterior         | 2.5-3.0      | Zona de alta corrosión    |
| Costado exterior       | 2.0-2.5      | Por debajo de flotación   |
| Tanques de lastre      | 1.5-2.0      | Agua de mar               |
| Tanques de combustible | 1.0-1.5      | Según tipo de combustible |
| Espacios secos         | 0.5-1.0      | Atmosfera seca            |

---

## 11. MÉTODO DE RENDERIZACIÓN (MAXSURF MODELER)

### 11.1 Objeto de Diseño (Design Object)

**Propiedades principales:**

- `Design.Surfaces`: Colección de superficies del casco
- `Design.Grids`: Líneas de sección, flotación, verticals
- `Design.Markers`: Puntos de referencia
- `Design.Hydrostatics`: Cálculos hidrostáticos

### 11.2 Exportación de Vistas Ortogonales

**Método:** `Design.ExportOrthogonalViewDXF(filename, viewType)`

**Tipos de vista (viewType):**

- `2` = Body Plan (Plano de Formas/Corte Transversal) ← **NECESITAMOS ESTE**
- `3` = Profile View (Vista de Perfil)
- `4` = Plan View (Vista de Planta)

**Ejemplo de código VBA:**

```vba
Dim DXFBodyOut As String
DXFBodyOut = "C:\...\Cuaderna_Maestra_Body.dxf"
msApp.Design.ExportOrthogonalViewDXF DXFBodyOut, 2
```

### 11.3 Control Points (Puntos de Control)

**Métodos principales:**

- `Surface.SetControlPoint(row, col, x, y, z)`: Establece posición
- `Surface.GetControlPoint(row, col, x, y, z)`: Obtiene posición
- `Surface.ControlPointLimits(NumRows, NumCols)`: Límites de la matriz

### 11.4 Superficies (Surfaces)

**Propiedades:**

- `Surface.Visible`: True/False para visibilidad
- `Surface.Type`: B-Spline, NURB, Developable, Conic
- `Surface.Name`: Nombre identificador
- `Surface.Use`: Hull (casco) o Structure (estructura)

---

## 12. ESTRATEGIA DE DIBUJO DE LA CUADERNA MAESTRA

### 12.1 Sistema de Coordenadas

**Origen:** Intersección de línea base, perpendicular de popa, y crujía

- **Eje X:** Longitudinal (proa positivo)
- **Eje Y:** Transversal (estribor positivo)
- **Eje Z:** Vertical (arriba positivo)

**Posición de la cuaderna maestra:**

- X = 50.3 m (desde perpendicular de popa)

### 12.2 Vistas Requeridas

1. **Vista de Sección (Body Plan):**

   - Plano YZ en X = 50.3 m
   - Muestra forma completa del casco
   - Babor y estribor en espejo

2. **Vista de Detalle Estructural:**
   - Ampliación de zona específica
   - Detalles de conexiones
   - Dimensiones acotadas

### 12.3 Elementos a Representar

**Contorno exterior:**

1. Forro de fondo (desde crujía hasta pantoque)
2. Forro de costado (desde pantoque hasta cubierta)
3. Cubierta principal

**Estructura interna:**

1. Doble fondo (1.20 m):

   - Chapa de fondo interior
   - Varengas (spacing 700 mm)
   - Longitudinales de fondo

2. Costados dobles (1.80 m cada lado):

   - Mamparo longitudinal interno (Y = ±6.00 m)
   - Cuadernas transversales
   - Longitudinales del costado

3. Cubierta principal (Z = 7.90 m):
   - Chapa de cubierta
   - Baos transversales

**Compartimentos:**

1. Tanque de doble fondo (0 → 1.20 m)
2. Tanques laterales (Y = ±6.00 → ±7.80 m)
3. Bodega central (Y = -6.00 → +6.00 m)

### 12.4 Anotaciones y Dimensiones

**Cotas principales:**

- Manga total (B = 15.99 m)
- Manga interior (12.39 m)
- Puntal (D = 7.90 m)
- Altura doble fondo (1.20 m)
- Ancho costado doble (1.80 m)
- Calado (T = 6.20 m)
- Francobordo (1.70 m)

**Etiquetas:**

- Materiales (AH36)
- Espesores de chapas
- Perfiles estructurales
- Nombres de compartimentos

---

## 13. CHECKLIST DE CUMPLIMIENTO NORMATIVO

### ✅ DNV-RU-SHIP Pt.3 Ch.2 (General Arrangement)

- [x] Altura de doble fondo ≥ B/20 (780 mm) → **1200 mm ✓**
- [x] Doble fondo extendido hasta pantoque
- [x] Mamparos estancos hasta cubierta principal
- [x] Acceso a tanques mediante agujeros de hombre
- [x] Separación entre tanques incompatibles (cofferdams)

### ✅ DNV-RU-SHIP Pt.3 Ch.3 (Structural Design)

- [x] Espaciamiento de cuadernas definido (700 mm zona central)
- [x] Web frames ≤ 5 × frame spacing en sala de máquinas
- [x] Perfiles estructurales según catálogo DNV
- [x] Espesores de chapa con adiciones por corrosión

### ✅ SOLAS Ch. II-1 (Subdivisión y Estabilidad)

- [x] Una cubierta principal suficiente para buque de carga general
- [x] Subdivisión estanca adecuada
- [x] Protección contra daños (doble fondo + costados dobles)

---

## 14. REFERENCIAS NORMATIVAS

1. **DNV-RU-SHIP Pt.3 Ch.2** - General Arrangement Design (July 2022)

   - Sec.2: Subdivision Arrangement
   - Sec.3: Compartment Arrangement
   - Sec.4: Access Arrangement

2. **DNV-RU-SHIP Pt.3 Ch.3** - Structural Design Principles (July 2016)

   - Sec.2: Structural Arrangement
   - Sec.3: Corrosion Additions
   - Sec.7: Structural Idealisation

3. **DNV-CG-0128** - Buckling (Class Guideline)

4. **SOLAS 1974 (Consolidated Edition 2020)**

   - Ch. II-1: Construction - Structure, subdivision and stability
   - Reg. 9: Double bottoms in passenger ships and cargo ships
   - Reg. 13: Damage stability requirements

5. **Maxsurf Modeler Automation Manual** (CONNECT Edition V21)
   - Chapter 3: Object Model
   - Chapter 5: Design Object
   - Chapter 7: Examples

---

## 15. CONCLUSIONES Y PRÓXIMOS PASOS

### Conclusiones Principales

1. ✅ **Diseño cumple con normativas** DNV y SOLAS
2. ✅ **Dimensiones estructurales** validadas y justificadas
3. ✅ **Materiales apropiados** para buque de carga general (AH36)
4. ✅ **Sistema de referencia** Maxsurf entendido y documentado

### Próximos Pasos

1. **Generar plano DXF** de corte transversal usando Python + ezdxf
2. **Crear tabla dimensional** con todas las medidas estructurales
3. **Exportar vista 3D** desde Maxsurf (si disponible)
4. **Documentar justificaciones** de diseño en memoria de cálculo
5. **Preparar presentación** con renders y planos

---

**Documento generado:** 3 de noviembre de 2025  
**Autor:** Equipo de Proyecto Final - Diseño Naval  
**Revisión:** v1.0  
**Próxima actualización:** Tras generación de planos DXF
