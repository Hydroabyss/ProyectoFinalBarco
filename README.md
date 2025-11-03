# ProyectoFinalBarco

## Proyecto Final - Diseño Naval (Buque 9)

## Estructura del Proyecto

Este proyecto contiene toda la documentación, datos y herramientas necesarias para el diseño y análisis del Buque 9 (granelero de 97.7 m de eslora).

### 📁 Organización de Carpetas

```
proyecto final Barcos/
├── README.md                    # Este archivo
├── Proyecto-Final.md            # Documento principal con todos los cálculos y análisis
│
├── trabajos/                    # Documentos de trabajo y asignaciones
│   ├── TRABAJO 1_PROYECTOS NAVALES.xlsx
│   ├── Trabajo 2 Grupo 9.docx_corregit_OCS.pdf
│   ├── Trabajo Tema 3.pdf
│   └── TRABAJO PROYECTO FINAL EJEMPLO.pdf
│
├── normativa/                   # Normativa técnica aplicable
│   ├── DNV-RU-SHIP Pt.3 Ch.1.pdf
│   ├── DNV-RU-SHIP Pt.3 Ch.2.pdf
│   ├── DNVGL-RU-SHIP-Pt3Ch3.pdf
│   ├── DNVGL-RU-SHIP-Pt3Ch4.pdf
│   ├── DNVGL-RU-SHIP-Pt3Ch5.pdf
│   └── SOLAS.pdf
│
├── tablas_datos/                # Datos tabulados y resultados
│   ├── maxsurf_table.csv
│   ├── maxsurf_table_quoted.csv
│   ├── tanks_proposal.csv
│   └── tabla_centralizada_datos.md
│
├── ENTREGA 4/                   # Análisis de Cuaderna Maestra
│   ├── README.md
│   ├── RESUMEN_EJECUTIVO.md
│   ├── REPORTE_CUADERNA_MAESTRA.md
│   ├── INTEGRACION_MAXSURF.md
│   ├── analisis_plano_cuaderna.json
│   ├── verificacion_dnv_cuaderna.json
│   ├── analisis_log.json
│   ├── graficos/
│   └── tablas/
│
└── herramientas/                # Scripts de análisis
    ├── extract_and_summarize.py
    ├── validate_maxsurf.py
    ├── analizador_plano_cuaderna.py
    ├── verificador_dnv_cuaderna.py
    ├── generador_reporte_cuaderna.py
    └── analizar_cuaderna_completo.py
```

## 📊 Datos Principales del Buque 9

### Dimensiones Principales

- **LOA** (Eslora total): 97.7 m
- **Lpp** (Eslora entre perpendiculares): 96.2 m
- **B** (Manga): 14.3 m
- **T** (Calado de proyecto): 5.8 m
- **D** (Puntal): 6.7 m
- **DWT** (Peso muerto): 3,848 t

### Características Operacionales

- **Tipo**: Granelero / Buque de carga general
- **Capacidad**: 1,100 TEU
- **Velocidad**: 14 kn
- **Autonomía**: 10,000 mn
- **Desplazamiento**: ~5,838 t

### Coeficientes de Forma (Maxsurf)

- **Cb** (Coeficiente de bloque): 0.703
- **Cp** (Coeficiente prismático): 0.721

## 🎯 Objetivos del Proyecto

### Problema 3 - Apartados A-E

**A)** Determinación de posición de mamparos:

- Pique de proa
- Cámara de máquinas (proa y popa)
- Claras de cuadernas (700 mm central, 600 mm en transiciones)

**B)** Disposición en plano de elementos delimitadores:

- Doble fondo y doble casco
- Cubiertas principales
- Mamparos transversales y longitudinales
- Motor principal y tanques de alimentación

**C)** Estimación de tanques de consumo:

- 3 escenarios de consumo: 2, 5 y 10 t/día
- Volúmenes requeridos para 10,000 mn de autonomía
- Ubicación en doble fondo y wing tanks

**D)** Modelo Maxsurf Stability:

- Definición de espacios y tanques
- Cálculos hidrostáticos (V, Δ, KB, BM, KM, GM)
- Curvas de estabilidad

**E)** Verificación de capacidades:

- Comprobación de volumen de bodegas vs. especificaciones
- Validación de estabilidad con carga completa
- Criterios SOLAS/DNV

## 🔧 Herramientas

### Scripts Python

- **extract_and_summarize.py**: Extracción de datos de PDFs y Excel
- **validate_maxsurf.py**: Validación de resultados hidrostáticos
- **analizador_plano_cuaderna.py**: Análisis de planos DXF de cuadernas
- **verificador_dnv_cuaderna.py**: Verificación de cumplimiento normativo DNV
- **generador_reporte_cuaderna.py**: Generación de reportes con gráficos y tablas
- **analizar_cuaderna_completo.py**: Script maestro para análisis completo

### Software Requerido

- **Maxsurf**: Modelado de casco y análisis de estabilidad
- **Excel/LibreOffice Calc**: Análisis de datos tabulados
- **Python 3.x**: Ejecución de scripts de validación
- **AutoCAD/DraftSight**: Visualización de planos DXF

### Automatización de planos y datos

Desde PowerShell en Windows puedes generar en un solo paso toda la información base del buque:

```powershell
cd "herramientas/maxsurf_integration"
py -m maxsurf_integration auto-base --loa 97.7 --beam 14.3 --depth 6.7 --draft 5.8
```

El flujo crea la carpeta `planos e informacion base/` junto al proyecto, que incluye:

- `resumen_planos_informacion.json` con el origen de datos (COM real o modo simulado) y rutas clave.
- Subcarpetas `datos/`, `planos/` y `modelo/` con CSV/JSON, archivos DXF y el modelo `.msd` listo para abrir en Maxsurf.
- Si el backend COM estuvo disponible, también se genera `artefactos/windows/` con registros detallados del proceso.

### Análisis de Cuaderna Maestra (ENTREGA 4)

Para ejecutar el análisis completo de la cuaderna maestra:

```bash
python3 herramientas/analizar_cuaderna_completo.py
```

Este script ejecuta automáticamente:

1. Análisis del plano DXF de la cuaderna
2. Verificación de cumplimiento normativo DNV
3. Generación de reportes, gráficos y tablas
4. Creación de resumen ejecutivo

Los resultados se guardan en la carpeta `ENTREGA 4/`:

- **RESUMEN_EJECUTIVO.md**: Resumen con estado general y acciones requeridas
- **REPORTE_CUADERNA_MAESTRA.md**: Reporte completo con análisis detallado
- **INTEGRACION_MAXSURF.md**: Guía de integración con Maxsurf
- **graficos/**: Gráficos de análisis (capas, cumplimiento DNV, geometría)
- **tablas/**: Tablas en formato Excel (capas, verificaciones)

## 📚 Normativa Aplicable

### SOLAS (Safety of Life at Sea)

- Capítulo II-1: Estructura, subdivisión y estabilidad
- Capítulo II-2: Protección contra incendios
- Capítulo III: Equipo de salvamento

### DNV (Det Norske Veritas) - Part 3

- Ch.1: Principios generales
- Ch.2: Disposición general (arrangement)
- Ch.3: Diseño estructural
- Ch.4: Requisitos adicionales
- Ch.5: Cargas y resistencia

## 📝 Documento Principal

Consulte `Proyecto-Final.md` para:

- Análisis detallado y cálculos
- Respuestas completas a los apartados A-E
- Fórmulas y justificaciones técnicas
- Referencias normativas específicas
- Propuestas de diseño y verificaciones

## 🚀 Próximos Pasos

1. ✅ Completar modelo Maxsurf con espacios definidos
2. ✅ Exportar resultados de cubicación (CSV)
3. ✅ Validar GM y curvas GZ
4. ✅ Generar planos 2D (planta, alzado, sección maestra)
5. ✅ Documentar verificaciones finales según SOLAS/DNV
6. ✅ Análisis completo de cuaderna maestra con verificación DNV
7. 🔄 Integración con Maxsurf para análisis estructural avanzado

## 📦 Entregas Completadas

### ENTREGA 4 - Análisis de Cuaderna Maestra

**Estado:** ✅ COMPLETADO (85.7% cumplimiento DNV)

**Contenido:**

- Análisis completo del plano DXF de la cuaderna maestra
- Verificación de cumplimiento normativo DNV Pt.3 Ch.5
- Reportes con gráficos y tablas detalladas
- Documentación de integración con Maxsurf
- Identificación de correcciones necesarias (espesor forro exterior)

**Archivos principales:**

- `ENTREGA 4/RESUMEN_EJECUTIVO.md`
- `ENTREGA 4/REPORTE_CUADERNA_MAESTRA.md`
- `ENTREGA 4/INTEGRACION_MAXSURF.md`

---

**Fecha de actualización**: 11 de noviembre de 2025
**Autor**: Proyecto Final - Diseño Naval
