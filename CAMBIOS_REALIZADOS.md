# Cambios Realizados - Organización del Proyecto

**Fecha**: 6 de noviembre de 2025  
**Acción**: Plano longitudinal detallado e integración avanzada con AutoCAD

---

## [2024-11-06] - Plano Longitudinal Detallado e Integración AutoCAD

### ✅ Añadido

- **Generador de plano mejorado** (`herramientas/generar_plano_longitudinal_detallado.py`)

  - ⚓ Doble fondo compartimentado con divisiones internas (4 compartimentos DB-1 a DB-4)
  - 🔲 Mamparos estancos con refuerzos estructurales (palmejares horizontales + refuerzos verticales)
  - 🔄 Sistema completo de propulsión:
    - Eje propulsor Ø0.45m con línea central visible
    - Bocina (stern tube) 8.5m longitud x Ø0.80m
    - Chumaceras (shaft bearings) en 2 posiciones estratégicas
    - Hélice Ø4.20m de 4 palas con representación esquemática en perfil
    - Timón compensado tipo semi-balanced (5.5m altura x 2.8m cuerda)
  - ⚙️ Motor MAN 6S50ME-C detallado:
    - 6 cilindros individuales representados con círculos
    - Línea de cigüeñal visible
    - Fundación estructural 0.30m espesor
  - 🔌 3x Generadores CAT 3512C con sección motor/generador diferenciada
  - ⛽ Tanques de servicio diario (FO y LO) en plataforma alta
  - 🔧 Sistemas de tuberías principales (FO Ø200mm, SW Ø300mm)
  - 📊 Sección transversal de referencia (escala 0.4) mostrando doble fondo y doble costado
  - 📐 24 capas organizadas profesionalmente con colores y tipos de línea estándar

- **Módulo de integración AutoCAD** (`herramientas/integracion_autocad_motores.py`)

  - 🔌 Clase `AutoCADEngineIntegration` con COM API de Windows
  - 📚 Biblioteca completa de motores marinos:
    - MAN 6S50ME-C (8500 kW @ 127 RPM, 6 cilindros, 145 ton)
    - Wärtsilä 16V26 (5440 kW @ 1000 RPM, 16 cilindros, 98 ton)
    - CAT 3512C (500 kW @ 1800 RPM, 12 cilindros, 12.5 ton)
  - 📋 Datos técnicos completos por motor:
    - Dimensiones exactas (L x W x H en metros)
    - Peso, potencia, RPM, SFOC
    - Requisitos de fundación (espesor mm, refuerzos HEB, pernos M36/M30/M24)
    - Referencias a modelos 3D (STEP/IGES desde fabricantes)
  - 🏗️ Clase `EngineRoomDesigner`:
    - Creación automática de capas con colores ACI
    - Inserción de equipos con posicionamiento 3D
    - Anotaciones técnicas automáticas
    - Generación completa de sala de máquinas
  - 💾 Exportación a JSON de configuraciones (`engine_configurations.json`)

- **Documentación completa** (`INTEGRACION_AUTOCAD_README.md`)
  - 📖 Guía de uso multiplataforma (macOS/Linux/Windows)
  - 🔄 Workflow completo: DXF → AutoCAD → Modelos 3D
  - 🎨 Referencia de capas (24 capas) con colores ACI y tipos de línea
  - 📐 Datos técnicos del buque y sala de máquinas
  - 🎓 Casos de uso (diseño preliminar, ingeniería de detalle, documentación)
  - 🚀 Roadmap de mejoras futuras

### 🛠️ Validado

- ✅ **Plano DXF detallado:** Generación exitosa con todas las geometrías verificadas
- ✅ **Sistema de propulsión:** Eje, bocina, chumaceras, hélice y timón correctamente posicionados
- ✅ **Refuerzos estructurales:** Palmejares horizontales cada 2m y refuerzos verticales en mamparos
- ✅ **Compartimentos:** Doble fondo dividido en 4 tanques (DB-1, DB-2, DB-3, DB-4)
- ✅ **Motor principal:** 6 cilindros individuales + línea de cigüeñal + fundación
- ✅ **Configuraciones:** Exportadas correctamente a `engine_configurations.json`
- ✅ **Compatibilidad:** DXF R2010 compatible con AutoCAD, LibreCAD, QCAD

### 📊 Elementos del Plano

- **Entidades estructurales:** ~120 líneas/polilíneas (casco, mamparos, cubiertas, refuerzos)
- **Sistema propulsión:** ~40 entidades (eje, bocina, chumaceras, hélice 4 palas, timón)
- **Equipos:** ~35 entidades (motor 6 cilindros, 3 generadores, tanques)
- **Sistemas:** ~20 entidades (tuberías, ventilación)
- **Anotaciones:** ~50 textos + dimensiones
- **Total estimado:** ~265 entidades en 24 capas organizadas

### 🔧 Notas Técnicas

- **Integración COM:** Solo funcional en Windows con AutoCAD instalado + pywin32
- **macOS/Linux:** Generación de DXF + JSON para referencia (sin conexión AutoCAD)
- **Modelos 3D:** STEP/IGES disponibles en portales técnicos de fabricantes (requiere credenciales)
- **Referencias normativas:**
  - DNV-RU-SHIP Pt.3 Ch.2 Sec.3 (doble fondo 1.2m)
  - ISO 3046-1 (correcciones ambientales motores)
  - Catálogos Wärtsilä, MAN, Caterpillar (curvas SFOC)

---

## [2024-11-06] - Optimización de Cálculos de Combustible

### ✅ Añadido

- **Calculadora avanzada de consumo** (`herramientas/calculos_combustible_optimizados.py`)
  - Curvas SFOC reales de Wärtsilä 16V26 (185-210 g/kWh según carga)
  - Datos de generadores CAT 3512C (201.5 g/kWh @ 75% carga)
  - Factores de corrección ambiental ISO 3046-1
  - Cálculo de autonomía con tanques reales (377.6 m³)

### 🛠️ Resultados Validados

- **Navegación @ 14.5 nudos:**

  - Motor principal: 1,482.44 kg/h (SFOC 185 g/kWh @ 90% carga)
  - Generadores (2 unidades @ 40%): 122.11 kg/h
  - **Total: 1,604.55 kg/h**

- **Puerto:**

  - 1 generador @ 40% carga: 41.91 kg/h
  - Consumo diario: 1,005.89 kg/día

- **Autonomía:**
  - Rango: **2,755 NM** (7.9 días @ 14.5 nudos)
  - Combustible disponible: 304,912 kg (377.6 m³ @ 808 kg/m³)

---

**Fecha**: 6 de noviembre de 2025  
**Acción**: Generación de plano longitudinal profesional de la sala de máquinas

---

### ✅ Ajustes principales

- Nuevo script `herramientas/generar_plano_longitudinal_sala_maquinas.py` que genera un DXF profesional con vista longitudinal completa de la sala de máquinas.
- Plano incluye: perfil del casco, mamparos estancos, cubiertas (principal, tank top, plataforma), doble fondo con tanques, motor principal diesel 6S50ME-C con 6 cilindros representados, 3 generadores auxiliares, caldera y bombas principales.
- Sistema de capas profesionales con colores estándar navales: CASCO (rojo), ESTRUCTURA (verde), CUBIERTAS (cian), MOTOR_PRINCIPAL (amarillo), GENERADORES (magenta), EQUIPOS_AUX (azul), TANQUES_DB (naranja), TANQUES_WING (verde claro).
- Dimensiones principales acotadas y leyenda con información del buque.
- Archivo generado: `salidas/disposicion_general/Plano_Longitudinal_Sala_Maquinas.dxf` (26 KB, 61 entidades).
- Documentación completa en `salidas/disposicion_general/README_Plano_Longitudinal.md`.

### 🛠️ Validación

- DXF válido (versión R2010/AC1024) verificado con ezdxf.
- 61 entidades correctamente posicionadas: 15 líneas, 6 polilíneas, 10 círculos, 27 textos, 3 cotas.
- 12 capas profesionales con colores estándar de la industria naval.
- Extensión del dibujo: 19.0 m x 8.2 m (coordenadas verificadas).
- Compatible con AutoCAD, LibreCAD, QCAD y otros visores DXF estándar.

---

**Fecha**: 6 de noviembre de 2025  
**Acción**: Integración real de `Maxsurf` y AutoCAD con flujo automatizadombios Realizados - Organización del Proyecto

**Fecha**: 6 de noviembre de 2025  
**Acción**: Integración real de Maxsurf y AutoCAD con flujo automatizado

---

### ✅ Ajustes principales

- Nuevo módulo `herramientas/maxsurf_integration/workflows/cad_pipeline.py` que conecta con la herramienta de diseño naval `Maxsurf` mediante `MaxsurfConnector`, genera el DXF de la sala de máquinas con datos reales y ofrece un modo de respaldo simulado cuando la API COM no está disponible.
- Clase `AutoCADExporter` para importar el DXF desde AutoCAD vía COM, aplicar estilos profesionales, insertar cajetín y exportar a PDF automáticamente.
- Configuración opcional mediante `config/cad_integration.json` (ruta de cajetín, límites de sala de máquinas, nombres de archivos) y creación del directorio `salidas/integracion_cad/` con `metadata_sala_maquinas.json` de respaldo.
- Exportación del flujo desde `maxsurf_integration.workflows.__init__` para facilitar su uso posterior en otros scripts y cuadernos.

### 🛠️ Validación

- Prueba local ejecutando `python -m compileall herramientas/maxsurf_integration/workflows/cad_pipeline.py` (sin errores).
- Ejecución manual del flujo en macOS verificando que cae en modo simulado para la herramienta `Maxsurf` y que omite AutoCAD cuando COM no está disponible, generando el DXF y los metadatos de referencia.

---

**Fecha**: 3 de noviembre de 2025  
**Acción**: Generación de plano y documentación de la cuaderna maestra

---

### ✅ Ajustes principales

- Nuevo script `herramientas/generar_cuaderna_maestra.py` que produce el DXF con vistas de sección, planta y perfil, además de la tabla de dimensiones, especificación de materiales y PDF resumen.
- Incorporación de `Plano_Cuaderna_Maestra.dxf` en `salidas/ENTREGA 3`, con representación del doble fondo (1.20 m), doble costado (1.80 m), cubiertas, tanques y mamparos según Trabajo 3 Grupo 9.
- Creación de `Tabla_Cuaderna_Maestra.csv`, `Materiales_Cuaderna_Maestra.md` y `Cuaderna_Maestra.pdf` para documentar dimensiones clave, material AH36 y la síntesis para revisión.
- Actualización de `salidas/ENTREGA 3/README.md` y `Guia_Cuaderna_Maestra.md` para reflejar los nuevos artefactos y el flujo recomendado de modelado CAD.

### 🛠️ Validación

- Script ejecutado en entorno virtual (`.venv`) sin errores, generando los archivos en la carpeta `salidas/ENTREGA 3`.
- Revisión manual del DXF en visor compatible (LibreCAD) para confirmar capas y etiquetado.

---

**Fecha**: 3 de noviembre de 2025  
**Acción**: Actualización normativa y enriquecimiento de las salidas del Problema 3

---

### ✅ Ajustes principales

- Traducción al español de los extractos normativos DNV/SOLAS incluidos en el guion automático y en `extractos_normativos.md`.
- Inclusión de fórmulas reglamentarias y referencias directas en el PDF generado.
- Cálculo de la altura mínima de doble fondo conforme a DNV Pt.3 Ch.2 Sec.3 (h_DB = 1000·B/20) y actualización de los tanques asociados.
- Nuevas métricas agregadas: `resumen_tanques.csv`, `balance_combustible.csv` (con porcentajes), gráfico `balance_combustible.png` y hojas adicionales en `disposicion_general.xlsx`.
- Gráficos reforzados con etiquetas en formato español (coma decimal) y leyendas actualizadas.
- `resumen_disposicion.json` ahora emplea claves en español y guarda la información de margen de combustible.
- Actualización de `tabla_centralizada_datos.md` para reflejar la nueva altura normativa del doble fondo.

### 🛠️ Validación

- Script `herramientas/generar_disposicion_general.py` ejecutado tras los cambios para regenerar todo el material.
- Índice de salidas (`salidas/disposicion_general/indice_salidas.md`) ampliado para documentar los nuevos archivos.

---

**Fecha**: 2 de noviembre de 2025  
**Acción**: Reorganización completa del espacio de trabajo y corrección de rutas

---

## 📋 Resumen de Cambios

### 1. Creación de Estructura de Carpetas

Se crearon 4 carpetas principales para organizar todos los archivos del proyecto:

```
proyecto final Barcos/
├── trabajos/          ← Documentos de trabajo y asignaciones
├── normativa/         ← PDFs de normativa DNV y SOLAS
├── tablas_datos/      ← Archivos CSV y tablas de datos
└── herramientas/      ← Scripts Python de análisis
```

### 2. Reorganización de Archivos

#### 📂 Carpeta `trabajos/` (4 archivos)

Movidos desde la raíz:

- ✅ `TRABAJO 1_PROYECTOS NAVALES.xlsx`
- ✅ `Trabajo 2 Grupo 9.docx_corregit_OCS.pdf`
- ✅ `TRABAJO PROYECTO FINAL EJEMPLO.pdf`
- ✅ `Trabajo Tema 3.pdf`

#### 📚 Carpeta `normativa/` (6 archivos)

Movidos desde la raíz:

- ✅ `DNV-RU-SHIP Pt.3 Ch.1.pdf`
- ✅ `DNV-RU-SHIP Pt.3 Ch.2.pdf`
- ✅ `DNVGL-RU-SHIP-Pt3Ch3.pdf`
- ✅ `DNVGL-RU-SHIP-Pt3Ch4.pdf`
- ✅ `DNVGL-RU-SHIP-Pt3Ch5.pdf`
- ✅ `SOLAS.pdf`

#### 📊 Carpeta `tablas_datos/` (4 archivos)

Movidos desde la raíz:

- ✅ `maxsurf_table.csv`
- ✅ `maxsurf_table_quoted.csv`
- ✅ `tanks_proposal.csv`
- ✅ `tabla_centralizada_datos.md`

#### 🔧 Carpeta `herramientas/` (2 archivos)

Movidos desde la raíz:

- ✅ `extract_and_summarize.py`
- ✅ `validate_maxsurf.py`

### 3. Actualización de Rutas en Documentación

#### Archivo: `Proyecto-Final.md`

**Sección "Archivos detectados"** - ✅ ACTUALIZADO

- ❌ ANTES: `/Users/robertgaraban/Downloads/DNVGL Examen 2020/...`
- ✅ AHORA: `./normativa/DNV-RU-SHIP Pt.3 Ch.X.pdf`

**Sección "Apéndice: trabajos presentados"** - ✅ ACTUALIZADO

- ❌ ANTES: `/Users/robertgaraban/Downloads/...`
- ✅ AHORA: `./trabajos/...`

**Sección "Referencias normativas"** - ✅ ACTUALIZADO

- Agregadas rutas relativas completas para todos los PDFs de normativa
- Añadido el archivo `DNVGL-RU-SHIP-Pt3Ch4.pdf` que faltaba en la lista

**Sección "Integración automática de tabla del software `Maxsurf`"** - ✅ ACTUALIZADO

- ❌ ANTES: `maxsurf_table.csv`
- ✅ AHORA: `./tablas_datos/maxsurf_table.csv`

### 4. Nuevos Archivos Creados

#### ✨ `README.md`

Documento principal con:

- Estructura completa del proyecto
- Datos principales del Buque 9
- Objetivos del Problema 3 (apartados A-E)
- Referencias a normativa aplicable
- Instrucciones de uso de herramientas
- Próximos pasos recomendados

#### ✨ `CAMBIOS_REALIZADOS.md` (este archivo)

Documentación de todos los cambios realizados en la reorganización

---

## 🎯 Beneficios de la Reorganización

### ✅ Mejor organización

- Archivos agrupados por tipo y función
- Fácil navegación por el proyecto
- Estructura ampliable para futuros añadidos

### ✅ Rutas relativas correctas

- Todas las referencias usan rutas relativas (`./carpeta/archivo`)
- Portabilidad: el proyecto funciona en cualquier ubicación
- No más rutas absolutas rotas

### ✅ Documentación completa

- README.md como punto de entrada
- Resumen visual de la estructura
- Referencias actualizadas en Proyecto-Final.md

### ✅ Facilita el trabajo colaborativo

- Estructura clara y profesional
- Fácil de compartir y versionar (git)
- Documentación actualizada y coherente

---

## 📝 Archivos en la Raíz (después de reorganización)

```
proyecto final Barcos/
├── README.md                    ← Documento principal de entrada
├── Proyecto-Final.md            ← Análisis técnico completo
├── CAMBIOS_REALIZADOS.md        ← Este archivo
├── trabajos/                    ← 4 archivos
├── normativa/                   ← 6 archivos
├── tablas_datos/                ← 4 archivos
└── herramientas/                ← 2 archivos
```

**Total**: 3 archivos en raíz + 4 carpetas con 16 archivos organizados

---

## 🔍 Verificación de Cambios

Para verificar que todos los archivos están en su lugar correcto:

```bash
# Desde la terminal, en la carpeta del proyecto:
cd "proyecto final Barcos"

# Ver estructura:
ls -R

# Contar archivos por carpeta:
echo "Trabajos: $(ls trabajos/ | wc -l)"
echo "Normativa: $(ls normativa/ | wc -l)"
echo "Tablas: $(ls tablas_datos/ | wc -l)"
echo "Herramientas: $(ls herramientas/ | wc -l)"
```

---

## ✅ Estado Final

| Categoría             | Archivos | Estado          |
| --------------------- | -------- | --------------- |
| 📂 Trabajos           | 4        | ✅ Organizados  |
| 📚 Normativa          | 6        | ✅ Organizados  |
| 📊 Tablas datos       | 4        | ✅ Organizados  |
| 🔧 Herramientas       | 2        | ✅ Organizados  |
| 📄 Documentación raíz | 3        | ✅ Actualizados |
| 🔗 Referencias        | Todas    | ✅ Corregidas   |

---

**Todo listo para continuar con el desarrollo del proyecto! ✨**
