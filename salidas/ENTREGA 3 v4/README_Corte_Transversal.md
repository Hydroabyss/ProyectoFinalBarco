# 📐 Corte Transversal Detallado - Cuaderna Maestra

## ✅ Archivos Generados

### 1. **Plano DXF Principal**

📄 `Corte_Transversal_Cuaderna_Maestra_Detallado.dxf` (57.1 KB)

**Vista transversal completa** de la cuaderna maestra con:

#### 🔷 Contorno del Casco

- Forro de fondo plano (22 mm de espesor)
- Pantoque curva realista (radio ~0.80 m)
- Forro de costado vertical (20 mm)
- Cubierta principal (12-16 mm)

#### 🔧 Estructura de Doble Fondo (h = 1.20 m)

- **Varengas** (transverse floors) con perfil T:
  - Altura: 400 mm
  - Alma: 12 mm
  - Ala: 150×20 mm
- **Longitudinales de fondo** (vista frontal)
  - Altura: 200 mm
- **Chapa de fondo interior**: 14 mm

#### 🔧 Costados Dobles (w = 1.80 m cada lado)

- **Cuadernas transversales** con perfil T:
  - Altura: 300 mm
  - Alma: 10 mm
  - Ala: 120×16 mm
- **Longitudinales de costado**
  - Altura: 200 mm
- **Mamparos longitudinales internos**: 12 mm

#### 🔧 Estructura de Cubierta (z = 7.90 m)

- **Baos transversales** con perfil T invertido:
  - Altura: 250 mm
  - Alma: 10 mm
  - Ala: 100×14 mm

#### 🏷️ Compartimentos

- **Tanque de Doble Fondo** (0 → 1.20 m)
- **Wing Tanks Laterales** (estribor y babor)
- **Bodega de Carga Central** (12.00 m de ancho)

#### 📏 Dimensiones Acotadas

- Manga total: 15.99 m
- Manga interior: 12.39 m
- Puntal: 7.90 m
- Calado: 6.20 m
- Francobordo: 1.70 m
- Doble fondo: 1.20 m
- Costado doble: 1.80 m

---

### 2. **Tabla de Dimensiones**

📄 `Dimensiones_Estructurales_Detalladas.csv`

Tabla completa con **40+ filas** de datos estructurales:

| Categoría               | Elemento                  | Valor            | Normativa     |
| ----------------------- | ------------------------- | ---------------- | ------------- |
| Dimensiones principales | Lpp, B, D, T              | -                | Medido        |
| Compartimentación       | Doble fondo, costados     | 1.20 m, 1.80 m   | DNV/SOLAS     |
| Espesores de chapas     | Fondo, costado, cubierta  | 22, 20, 12-16 mm | DNV Pt.3 Ch.6 |
| Perfiles estructurales  | Varengas, cuadernas, baos | Detallado        | DNV Pt.3 Ch.3 |
| Material                | Acero AH36                | σy=355 MPa       | DNV           |

---

### 3. **Documento Guía**

📄 `Guia_Corte_Transversal.md`

Documentación completa de 200+ líneas:

- ✅ Descripción de todos los elementos
- ✅ Organización por capas (layers)
- ✅ Normativa aplicada (DNV, SOLAS)
- ✅ Materiales y espesores
- ✅ Instrucciones de uso del plano
- ✅ Referencias técnicas

---

### 4. **Resumen Normativo**

📄 `Resumen_Normativa_Cuaderna_Maestra.md` (ya existente)

Documento de 515 líneas con:

- 📖 Extractos de DNV-RU-SHIP Pt.3 Ch.2 y Ch.3
- 📖 Requisitos SOLAS Ch. II-1
- 📖 Manual Maxsurf Modeler Automation
- 📖 Justificación de todas las dimensiones

---

## 🎨 Capas del Dibujo DXF

| Capa                    | Color             | Tipo Línea  | Contenido                  |
| ----------------------- | ----------------- | ----------- | -------------------------- |
| `CASCO_EXTERIOR`        | ⚪ Blanco (7)     | Continua    | Forro exterior del casco   |
| `ESTRUCTURA_PRIMARIA`   | 🔴 Rojo (1)       | Continua    | Varengas, cuadernas, baos  |
| `ESTRUCTURA_SECUNDARIA` | 🟢 Verde (3)      | Continua    | Longitudinales             |
| `MAMPAROS`              | 🔵 Azul (5)       | Continua    | Mamparos internos          |
| `TANQUES`               | 🔵 Cyan (4)       | Continua    | Límites de tanques         |
| `LINEA_AGUA`            | 🟣 Magenta (6)    | Discontinua | Línea de flotación T=6.20m |
| `COTAS`                 | 🟡 Amarillo (2)   | Continua    | Dimensiones y acotación    |
| `TEXTO`                 | ⚫ Gris (8)       | Continua    | Etiquetas y cajetín        |
| `EJES`                  | ⚫ Gris claro (9) | Eje         | Baseline, centerline       |

---

## 🔍 Características del Diseño

### ✅ Cumplimiento Normativo

#### DNV-RU-SHIP Pt.3 Ch.2 Sec.3

- **Altura mínima doble fondo:** hDB = B/20 = 0.78 m
- **Adoptado:** 1.20 m ✅ **(excede requisito en 54%)**

#### DNV-RU-SHIP Pt.3 Ch.3

- **Espaciamiento de cuadernas:** 0.70 m (zona central)
- **Perfiles estructurales:** T, Bulbo HP, L según catálogo

#### SOLAS Ch. II-1

- **Reg.9:** Double bottoms ✅
- **Reg.13:** Damage stability (costados dobles) ✅

### 📊 Datos Técnicos

**Posición de la Cuaderna Maestra:**

- 50.3 m desde perpendicular de proa (Lpp/2)
- Zona de máxima sección transversal

**Material Estructural:**

- Acero **AH36** (DNV Grade)
- Límite elástico: 355 MPa
- Resistencia: 490-630 MPa

**Espaciamiento Estructural:**

- Cuadernas: 700 mm (zona central)
- Cuadernas: 600 mm (proa/popa)

---

## 🖥️ Cómo Visualizar

### Opción 1: AutoCAD / DraftSight / BricsCAD

```bash
# Abrir el archivo DXF directamente
open "Corte_Transversal_Cuaderna_Maestra_Detallado.dxf"
```

### Opción 2: QCAD (Open Source)

1. Descargar: https://qcad.org
2. Abrir el archivo DXF
3. Ver → Capas para activar/desactivar elementos

### Opción 3: FreeCAD

```bash
# Instalar FreeCAD
brew install --cask freecad

# Abrir en FreeCAD
freecad "Corte_Transversal_Cuaderna_Maestra_Detallado.dxf"
```

### Opción 4: Visualizador Online

- https://sharecad.org (subir DXF)
- https://www.autodesk.com/viewers (Autodesk Viewer)

---

## 📐 Diferencias con el Script Anterior

### ❌ Script Antiguo (`generar_cuaderna_maestra.py`)

- ✗ Vistas simplificadas (alzado, planta, sección)
- ✗ Sin estructura interna detallada
- ✗ Sin perfiles estructurales realistas
- ✗ Sin pantoque curva
- ✗ Problemas con posicionamiento de texto

### ✅ Script Nuevo (`generar_corte_transversal_detallado.py`)

- ✓ **Corte transversal completo y realista**
- ✓ **Pantoque curva** con radio de 0.80 m
- ✓ **Varengas, cuadernas y baos** con perfiles T detallados
- ✓ **Longitudinales** representados correctamente
- ✓ **Mamparos internos** con espesores reales
- ✓ **Tanques y compartimentos** claramente delimitados
- ✓ **Cotas completas** de todas las dimensiones
- ✓ **Cajetín profesional** con información del plano
- ✓ **Sistema de capas organizado**
- ✓ **Documentación completa** (CSV + MD)

---

## 🚀 Mejoras Realizadas

### 1. **Geometría Realista**

- Pantoque curva (no líneas rectas)
- Transición suave fondo → costado
- Espesores de chapa visibles

### 2. **Estructura Detallada**

- Varengas con perfil T (alma + ala)
- Cuadernas transversales en costados
- Baos de cubierta con perfil T invertido
- Longitudinales como marcadores frontales

### 3. **Organización Profesional**

- 9 capas con colores estándar
- Lineweights diferenciados
- Tipos de línea apropiados

### 4. **Documentación Completa**

- Tabla CSV con 40+ dimensiones
- Guía de 200+ líneas
- Referencias normativas verificadas

---

## 📝 Notas Importantes

⚠️ **El plano representa la cuaderna maestra en posición de máxima sección**

📍 **Coordenadas:**

- Origen: Intersección baseline/centerline/AP
- Eje Y: Transversal (estribor positivo)
- Eje Z: Vertical (arriba positivo)

🔍 **Escala recomendada:** 1:50 para impresión

📏 **Sistema de unidades:** Metros (m)

---

## 🎯 Próximos Pasos

1. **Abrir y revisar** el archivo DXF en un visualizador CAD
2. **Verificar** todas las dimensiones con la tabla CSV
3. **Consultar** el documento guía para detalles específicos
4. **Validar** cumplimiento normativo con el resumen
5. **Presentar** el plano para aprobación

---

## 📞 Soporte

**Archivos generados:**

- ✅ `Corte_Transversal_Cuaderna_Maestra_Detallado.dxf`
- ✅ `Dimensiones_Estructurales_Detalladas.csv`
- ✅ `Guia_Corte_Transversal.md`
- ✅ `Resumen_Normativa_Cuaderna_Maestra.md`

**Generado:** 3 de noviembre de 2025  
**Revisión:** v2.0 (Completo y Detallado)  
**Estado:** ✅ Listo para revisión

---

_🚢 Proyecto Final - Diseño Naval - Buque de Carga General_
