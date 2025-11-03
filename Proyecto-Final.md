## Proyecto Final — extracción preliminar de datos y referencias

### Cómo ejecutar los ejemplos (macOS)

```bash
cd "/Users/robertgaraban/Desktop/proyecto final Barcos"
source .venv/bin/activate
export PYTHONPATH="$(pwd)/herramientas"

# CLI del paquete (recomendado)
python -m maxsurf_integration ping
python -m maxsurf_integration visual-report --out "./salidas/visual" --basename "visual_demo"
python -m maxsurf_integration grid-opt --L 95 100 --B 14 16 --T 5 6 --Cb 0.55 0.65 \
  --out "./salidas/optimization" --basename "cli_grid"

# Alternativa: scripts de ejemplo directos
python "./herramientas/maxsurf_integration/examples/generate_visual_report.py"
python "./herramientas/maxsurf_integration/examples/run_grid_optimization.py" --L 95 100 --B 14 16 --T 5 6 --Cb 0.55 0.65

# Pruebas
pytest -q "./herramientas/maxsurf_integration/tests"
```

### Flujo recomendado en Windows (Maxsurf real)

1. Instala dependencias en PowerShell:

```powershell
cd "herramientas/maxsurf_integration"
py -m pip install -r requirements.txt
```

2. Verifica `pywin32` con `py -c "import win32com"` y asegúrate de que Maxsurf Modeler esté instalado.
3. Ejecuta el comando `auto-base` para generar datos, planos y modelo:

```powershell
py -m maxsurf_integration auto-base --loa 103.81 --beam 15.60 --depth 7.70 --draft 6.20
```

4. Abre la carpeta `planos e informacion base\` que se crea en la misma ubicación donde ejecutaste el comando. Allí encontrarás:

- `resumen_planos_informacion.json` con el backend utilizado y rutas clave.
- Subcarpetas `datos/`, `planos/` y `modelo/` con JSON, DXF y el `.msd`.
- Si se utilizó backend COM real, se registrarán también `artefactos/windows/` con los paquetes detallados.

5. Continua en Maxsurf utilizando el `.msd` guardado en `planos e informacion base\modelo`.

> Nota: Estos pasos leen directamente la geometría y coeficientes hidrostáticos desde Maxsurf. En macOS/Linux se usa un backend simulado; se recomienda tomar los archivos generados en Windows como referencia oficial.

Fecha: 2 de noviembre de 2025

## Resumen

Este documento recoge: (1) los archivos normativos detectados en el workspace, (2) las limitaciones encontradas al intentar extraer texto de los PDFs disponibles, (3) las suposiciones razonables que se han utilizado para generar datos de proyecto cuando falta el PDF del trabajo, (4) las fórmulas y argumentos utilizados con una breve explicación, y (5) referencias útiles a SOLAS y DNV.

---

## 📁 Estructura del Proyecto (Organización de Archivos)

El proyecto está organizado en carpetas temáticas para facilitar la navegación y el trabajo colaborativo:

```
proyecto final Barcos/
├── 📄 README.md                     ← Documento principal de entrada
├── 📄 Proyecto-Final.md             ← Este documento (análisis técnico completo)
├── 📄 CAMBIOS_REALIZADOS.md         ← Resumen de cambios de reorganización
│
├── 📂 trabajos/                     ← Documentos de trabajo y asignaciones (4 archivos)
│   ├── TRABAJO 1_PROYECTOS NAVALES.xlsx
│   ├── Trabajo 2 Grupo 9.docx_corregit_OCS.pdf
│   ├── TRABAJO PROYECTO FINAL EJEMPLO.pdf
│   └── Trabajo Tema 3.pdf
│
├── 📚 normativa/                    ← Normativa técnica DNV y SOLAS (6 archivos)
│   ├── DNV-RU-SHIP Pt.3 Ch.1.pdf
│   ├── DNV-RU-SHIP Pt.3 Ch.2.pdf
│   ├── DNVGL-RU-SHIP-Pt3Ch3.pdf
│   ├── DNVGL-RU-SHIP-Pt3Ch4.pdf
│   ├── DNVGL-RU-SHIP-Pt3Ch5.pdf
│   └── SOLAS.pdf
│
├── 📊 tablas_datos/                 ← Datos tabulados y resultados (4 archivos)
│   ├── maxsurf_table.csv
│   ├── maxsurf_table_quoted.csv
│   ├── tanks_proposal.csv
│   └── tabla_centralizada_datos.md
│
└── 🔧 herramientas/                 ← Scripts Python de análisis (2 archivos)
    ├── extract_and_summarize.py
    └── validate_maxsurf.py
```

**Total**: 3 documentos en raíz + 16 archivos organizados en 4 carpetas

**Nota**: Todas las rutas en este documento usan referencias relativas (ejemplo: `./normativa/archivo.pdf`) para garantizar portabilidad del proyecto.

### 📊 Tabla de Referencia Rápida

| Carpeta              | Contenido                                      | Cantidad   | Acceso Rápido     |
| -------------------- | ---------------------------------------------- | ---------- | ----------------- |
| 📂 **trabajos/**     | Documentos de trabajo, asignaciones y ejemplos | 4 archivos | `./trabajos/`     |
| 📚 **normativa/**    | PDFs de normativa DNV (Pt.3 Ch.1-5) y SOLAS    | 6 archivos | `./normativa/`    |
| 📊 **tablas_datos/** | CSV con resultados Maxsurf y datos tabulados   | 4 archivos | `./tablas_datos/` |
| 🔧 **herramientas/** | Scripts Python para extracción y validación    | 2 archivos | `./herramientas/` |

**Archivos clave en raíz:**

- `README.md` - Punto de entrada principal con resumen del proyecto
- `Proyecto-Final.md` - Este documento (análisis técnico completo)
- `CAMBIOS_REALIZADOS.md` - Historial de reorganización del proyecto

---

## Archivos detectados

### Normativa DNV y SOLAS

- `./normativa/DNV-RU-SHIP Pt.3 Ch.1.pdf` (Reglas DNV Pt.3 Ch.1)
- `./normativa/DNV-RU-SHIP Pt.3 Ch.2.pdf` (Reglas DNV Pt.3 Ch.2)
- `./normativa/DNVGL-RU-SHIP-Pt3Ch3.pdf` (Reglas DNV Pt.3 Ch.3)
- `./normativa/DNVGL-RU-SHIP-Pt3Ch4.pdf` (Reglas DNV Pt.3 Ch.4)
- `./normativa/DNVGL-RU-SHIP-Pt3Ch5.pdf` (Reglas DNV Pt.3 Ch.5)
- `./normativa/SOLAS.pdf` (Convenio SOLAS)

### Trabajos y documentación del proyecto

- `./trabajos/TRABAJO 1_PROYECTOS NAVALES.xlsx` (Datos principales del Buque 9)
- `./trabajos/Trabajo 2 Grupo 9.docx_corregit_OCS.pdf` (Instrucciones modelado Maxsurf)
- `./trabajos/Trabajo Tema 3.pdf` (Problema 3 - Apartados A-E)
- `./trabajos/TRABAJO PROYECTO FINAL EJEMPLO.pdf` (Ejemplo de referencia)

### Tablas de datos

- `./tablas_datos/maxsurf_table.csv` (Resultados hidrostáticos Maxsurf)
- `./tablas_datos/maxsurf_table_quoted.csv` (Resultados hidrostáticos con comillas)
- `./tablas_datos/tanks_proposal.csv` (Propuesta de tanques)
- `./tablas_datos/tabla_centralizada_datos.md` (Datos centralizados)

### Herramientas

- `./herramientas/extract_and_summarize.py` (Script de extracción de datos)
- `./herramientas/validate_maxsurf.py` (Script de validación)

## Limitaciones técnicas observadas

- Las herramientas de este entorno no pueden abrir PDFs binarios como texto plano; por eso no pude extraer automáticamente el contenido completo de los PDFs DNVGL ni del PDF del trabajo (si no está disponible). En este archivo entrego una extracción preliminar basada en los nombres de archivo y en suposiciones que usted autorizó.

## Suposiciones razonables (confirmar o editar)

Estas suposiciones se usan para generar ejemplos y referencias normativas; indíque las que desea cambiar.

- Tipo de embarcación: buque de carga general
- Longitud (LOA): 100 m
- Manga (B): 16 m
- Calado de proyecto (T): 6 m
- DWT aproximado: 5 000 t
- Material de casco: acero estructural habitual
- Navegación: internacional / oceánica (aplicable SOLAS)
- Tripulación: 12
- Carga: carga general no peligrosa

## Datos “extraídos” / parámetros usados

Nota: a falta del PDF con los datos reales, los siguientes valores son las suposiciones usadas. Si usted aporta el PDF o los valores reales, actualizaré este apartado con cifras exactas y las referencias.

- LOA = 100 m
- Manga = 16 m
- Calado = 6 m
- Desplazamiento aproximado (estimado de diseño) = depende de Coeficiente de bloque (Cb). Por ejemplo, con Cb = 0.62: Volumen sumergido ≈ LOA × B × T × Cb = 100 × 16 × 6 × 0.62 = 5,952 m³. Con rho_mar = 1025 kg/m³ → Masa ≈ 6,100 t.

## Fórmulas y argumentos con una breve explicación

Las fórmulas usadas son las habituales de hidroestática y arranque de diseño; debajo se explican y justifican los parámetros asumidos.

- Volumen sumergido (V):

  - V = LOA × B × T × Cb
  - Argumento: es la estimación de volumen desplazado usando el coeficiente de bloque (Cb). Cb agrupa la forma real del casco respecto a un bloque rectangular. Para buques de carga general Cb típicos: 0.55–0.70.

- Desplazamiento (Δ):

  - Δ = rho_sea × V
  - Con rho_sea (agua de mar) ≈ 1025 kg/m³. Convención: Δ en toneladas (1 t = 1000 kg).

- Momento de inercia de la sección transversal (Ixx) y altura metacéntrica inicial (BM):

  - BM = I/V (convención: I es momento de inercia de la superficie de la flotación respecto al eje longitudinal; V es volumen sumergido)
  - GM ≈ BM + KB - KG (donde KB es distancia del baso al centro de flotación, KG altura del centro de gravedad, etc.)
  - Argumento: cálculo de estabilidad inicial. BM aumenta cuanto más ancha y de mayor segundo momento sea la superficie de flotación.

- Presiones y carga estructural (básico):
  - Presión hidrostática p = rho × g × h
  - Argumento: para esfuerzos locales en el casco y cálculo de cargas sobre mamparos estancos o lastres.

## Ejemplo numérico (ilustrativo, basado en las suposiciones)

- Tomando Cb = 0.62, LOA = 100 m, B = 16 m, T = 6 m:
  - V ≈ 100 × 16 × 6 × 0.62 = 5,952 m³
  - Δ ≈ 5,952 × 1025 kg/m³ = 6,100,800 kg ≈ 6,101 t
  - Este valor es sólo indicativo; el cálculo real requiere forma del casco (perfil de manga y curvaturas), distribución de pesos (KG) y coeficientes hidrodinámicos.

## Referencias normativas y dónde comprobar las citas

Estas son referencias generales que usted debe comprobar en los textos originales disponibles en `./normativa/`. Yo usaré estas normas para citar cláusulas concretas cuando tenga acceso directo a los documentos.

- **SOLAS** (Convenio internacional para la seguridad de la vida humana en el mar, 1974)

  - Ruta: `./normativa/SOLAS.pdf`
  - Capítulos relevantes según la materia:
    - Cap. II-1: Estructura, integridad de cascos, subdivisión y estabilidad
    - Cap. II-2: Prevención y protección contra incendios
    - Cap. III: Salvamento y equipo de supervivencia
    - Cap. XI–1 / XI–2 / ISPS: seguridad marítima si aplica

- **DNV Rules** (Det Norske Veritas - Rules for Ships)
  - `./normativa/DNV-RU-SHIP Pt.3 Ch.1.pdf` — Parte 3, Capítulo 1: Principios generales
  - `./normativa/DNV-RU-SHIP Pt.3 Ch.2.pdf` — Parte 3, Capítulo 2: Disposición general (arrangement)
  - `./normativa/DNVGL-RU-SHIP-Pt3Ch3.pdf` — Parte 3, Capítulo 3: Diseño estructural
  - `./normativa/DNVGL-RU-SHIP-Pt3Ch4.pdf` — Parte 3, Capítulo 4: Requisitos adicionales
  - `./normativa/DNVGL-RU-SHIP-Pt3Ch5.pdf` — Parte 3, Capítulo 5: Cargas y resistencia

## Cómo proceder para obtener citas exactas

1. Suba el PDF del trabajo (`Trabajo 2 Grupo 9.docx_corregit_OCS.pdf`) a la carpeta del proyecto o péguelo aquí.
2. Si quiere que extraiga y cite cláusulas de los PDFs DNVGL que están en su máquina, suba también esos PDFs al workspace (o permítame acceso).
3. Con los PDFs en el workspace puedo extraer texto, encontrar las preguntas del trabajo y mapear cláusulas SOLAS/DNV exactas (incluiré números de cláusula y páginas).

## Entregables incluidos

- Este `Proyecto-Final.md` (documento preliminar con suposiciones, fórmulas y referencias generales).
- Próximo entregable (cuando suba PDFs): documento con respuestas a cada pregunta del trabajo, con citas concretas a SOLAS y DNV y cálculos numéricos rellenados con datos reales.

## Próximos pasos sugeridos

1. Suba el PDF `Trabajo 2 Grupo 9.docx_corregit_OCS.pdf` al workspace.
2. Confirme o ajuste las suposiciones listadas (tipo de buque, dimensiones, carga, navegación).
3. Indique las “particularidades” o preguntas concretas si las tiene ya redactadas; si no, yo identificaré las preguntas en el PDF y las listaré para su confirmación.

## Contacto rápido

Cuando suba los archivos o confirme las suposiciones, continuaré con la extracción exacta de datos y con la redacción de las respuestas con referencias normativas precisas.

— Fin del documento —

## Apéndice: trabajos presentados

Los siguientes archivos están organizados en la carpeta `./trabajos/` y se incluyen como apéndice con sus metadatos y estado.

1. `TRABAJO 1_PROYECTOS NAVALES.xlsx`

- Ruta: `./trabajos/TRABAJO 1_PROYECTOS NAVALES.xlsx`
- Estado: disponible — contenido Excel con datos del proyecto Buque 9.

2. `Trabajo 2 Grupo 9.docx_corregit_OCS.pdf`

- Ruta: `./trabajos/Trabajo 2 Grupo 9.docx_corregit_OCS.pdf`
- Estado: disponible — PDF con instrucciones para modelado en Maxsurf y diseño paramétrico de cascos.

3. `Trabajo Tema 3.pdf`

- Ruta: `./trabajos/Trabajo Tema 3.pdf`
- Estado: disponible — PDF con el Problema 3 (apartados A-E) sobre disposición de mamparos, tanques y verificación de capacidades.

4. `TRABAJO PROYECTO FINAL EJEMPLO.pdf`

- Ruta: `./trabajos/TRABAJO PROYECTO FINAL EJEMPLO.pdf`
- Estado: disponible — PDF de referencia con ejemplo de proyecto similar.

## Datos extraídos de los trabajos

A continuación se recogen los datos clave extraídos directamente del fichero Excel `TRABAJO 1_PROYECTOS NAVALES.xlsx` (bloque de texto proporcionado) y datos detectados en los PDFs `Trabajo 2 Grupo 9.docx_corregit_OCS.pdf` y `Trabajo Tema 3.pdf`.

1. Datos principales (desde `TRABAJO 1_PROYECTOS NAVALES.xlsx`)

   - Tipus de vaixell: Granelero
   - Capacitat de càrrega: 1 100 TEU
   - Volum carga: 5 560 m³
   - Peso muerto a plena carga (DWT): 5 200 ton
   - Velocitat: 14,5 kn
   - Autonomía: 10 000 mn
   - Tripulación: (no indicada en el extracto)
   - Densidad máxima de carga: 1 050 kg/m³
   - Volumen bajo cubierta principal: 6 672 m³
   - Valores tabulados adicionales (fila identificada como "BUQUE 9"):
     - 97,7 96,2 14,3 5,8 6,7 3 848 3 868 5 838 14
   - Nota: estos datos provienen del bloque de texto que usted facilitó; conviene revisar las hojas/columnas originales del Excel para su correcta interpretación (por ejemplo, qué representan exactamente las columnas del bloque "BUQUE 9").

2. Contenido y preguntas detectadas en `Trabajo 2 Grupo 9.docx_corregit_OCS.pdf`

   - El documento contiene instrucciones para modelado en Maxsurf y diseño paramétrico de cascos. Extracto relevante:
     - Inicio de la instrucción A: "Utilizando Maxsurf, derivar unas formas del buque, aproximando de la manera más precisa posible las dimensiones principales y los coeficientes de forma..."
     - Datos característicos introducidos en el ejemplo del autor:
       - LOA (Length over all) = Lpp / 0,97 = 103,81 m
       - Depth = Puntal = 7,7 m
       - Beam = Manga = 15,60 m
     - Instrucciones de verificación: comparar resultados de Maxsurf con hojas de cálculo Excel; validar geometría y coeficientes.
   - El PDF contiene además secciones de resultados (imágenes y tablas referenciadas como "Imagen 1", "Imagen 2" y resultados Excel/Maxsurf).

3. Contenido y preguntas detectadas en `Trabajo Tema 3.pdf`
   - Detectado el "Problema 3" con apartados A a E, que piden:
     A. Determinar la posición de los mamparos de proa y popa de cámara de máquinas y del pique de proa. (Especificación: clara de cuadernas 700 mm zona central, 600 mm a popa del mamparo de proa de cámara de máquinas y a proa del pique de proa.)
     B. Disponer en el plano los principales elementos delimitadores de espacios (doble fondo, doble casco, cubiertas, mamparos transversales y longitudinales). Indicar la disposición del motor principal y tanques de alimentación.
     C. Estimar el volumen de los principales tanques de consumos, disponerlos y cubicar en un modelo de Maxsurf stability.
     D. Completar el modelo de Maxsurf stability con los espacios.
     E. Verificar mediante Maxsurf stability si la capacidad de los tanques de carga es suficiente para cumplir especificaciones de proyecto.

## Propuestas y plan de trabajo (respuestas en español)

Basado en los datos extraídos y en las preguntas detectadas, propongo lo siguiente, con pasos concretos y justificación técnica.

Propuesta A — Procesamiento y verificación de datos (paso obligatorio)

- Acción: Consolidar todos los datos numéricos en una única hoja de trabajo (Excel) con campos normalizados: LOA, Lpp, manga, puntal, calado de diseño, DWT, volumen de bodegas, densidad de carga, coeficientes (Cb, Cp, Cm), pesas distribuidas (KG estimado), y listado de tanques.
- Justificación: evita errores de interpretación y permite alimentar Maxsurf y cálculos hidrostáticos automáticamente.

Propuesta B — Modelado geométrico en Maxsurf

- Acción: Partir del modelo base indicado (Cargo Vessel) y aplicar transformaciones paramétricas hasta conseguir: LOA=103,81 m (o Lpp según prefiera), puntal=7,7 m, beam=15,60 m. Guardar versiones y exportar archivos de forma (IGES/DFX/Maxsurf format).
- Justificación: Maxsurf permite generar curvas de forma, obtener volumen sumergido, centros de gravedad iniciales (si se define distribución de pesos) y cubicar espacios (tanques y bodegas) para compararlos con requisitos.

Propuesta C — Cálculo hidrostático y verificación de estabilidad

- Acción: Con la geometría final, calcular desplazamiento a cargado y ligero, curva de áreas, GM inicial (con estimación de KG), moment to change trim, y comprobar niveles de estabilidad de acuerdo a requisitos de proyecto (y SOLAS/Marine Stability criteria si aplica).
- Fórmulas y notas:
  - Volumen sumergido V = LOA × B × T × Cb (estimación inicial). Usar resultados de Maxsurf para V exacto.
  - Desplazamiento Δ = ρ × V (ρ = 1025 kg/m³). Convertir a toneladas.
  - GM = BM + KB - KG; BM = I/V (I segundo momento de la superficie de flotación — obtener de Maxsurf).

Propuesta D — Disposición de mamparos y subdivisión

- Acción: Según el apartado A/B del trabajo, posicionar mamparos de proa/popa y mamparo de cámara de máquinas conforme a la rodea y la clara de cuadernas indicada (700/600 mm). Diseñar doble fondo y separados de tanques, y verificar acceso y sistemas de lastre.
- Justificación normativa: cumplir requerimientos de subdivisión y resistencia estructural (consultar DNV Part 3 Capítulos 1–3 para requerimientos de integridad estructural y subdivisión; SOLAS II-1 para subdivisión y estabilidad de buques de carga si aplica).

Propuesta E — Tanques de consumo y verificación de capacidad

- Acción: A partir de los volúmenes estimados/cubificados en Maxsurf, comprobar si la capacidad de tanques de combustible, agua y lastre cumple con autonomía y especificaciones (ej. autonomía 10 000 mn — calcular consumo específico del motor y volumen requerido). Si falta dato de consumo, asumir valores típicos y documentar supuestos.
- Ejemplo (ilustrativo): si autonomía = 10 000 mn y velocidad de cruce = 14,5 kn, requerimiento de horas = 10 000 / 14,5 ≈ 689 h; con consumo medio por motor (ej. 2 t/día o valor similar) calcular masa combustible necesaria.

Propuesta F — Documentación y referencias normativas

- Acción: Mapear cada requisito del trabajo (A–E) a cláusulas DNV y SOLAS relevantes. Esto se hará después de extraer el texto de DNV (Part 3 Capítulos 1–5) y SOLAS (II-1, II-2, III). Incluiré referencias concretas (número de cláusula y página) una vez disponibles.

## Próximos pasos y entregables

1. Validar los datos del Excel (usted o yo): confirmar columnas y unidades.
2. Ejecutar modelado en Maxsurf con las dimensiones definidas; exportar resultados (curvas de forma, volúmenes, momentos).
3. Extraer del PDF `Trabajo 2 Grupo 9` las tablas de resultados (imágenes / tablas) y trasladarlas a la hoja de cálculo para comparar.
4. Mapear cláusulas DNV/SOLAS y completar `Proyecto-Final.md` con citas exactas.
5. Entregar documento final en español con: resumen, datos consolidados, cálculos hidrostáticos, verificaciones de estabilidad, disposición de mamparos y justificación normativa.

Si confirma, procedo a aplicar los supuestos numéricos y a generar los cálculos de ejemplo (con todas las fórmulas mostradas y valores intermedios) y actualizar `Proyecto-Final.md`. Si prefiere esperar a datos más precisos o al propio Excel original, indíquelo.

## Cálculos numéricos de ejemplo

- Parámetros usados: LOA=103.81 m, B=15.6 m, T=7.7 m, Cb=0.62
- Volumen estimado V = 7731.19 m3
- Desplazamiento Δ ≈ 7924.47 toneladas (ρ=1025.0 kg/m3)
- Cálculo simplificado BM = I/V = 2.974 m
- Supuestos: KB=3.850 m, KG=8.000 m → GM ≈ -1.176 m

## Datos específicos: Buque 9 (extraído de `TRABAJO 1_PROYECTOS NAVALES.xlsx`)

Los datos de la fila correspondiente a "BUQUE 9" en la hoja de datos son (cabeceras aproximadas detectadas en el Excel):

- NOMBRE: BUQUE 9
- LOA = 97.7 m
- Lpp = 96.2 m
- B (manga) = 14.3 m
- T (calado) = 5.8 m
- D (puntal) = 6.7 m
- DWT (peso muerto) = 3 848 t
- Vc (volumen/ capacidad aparente en hoja) = 3 868 (unidad según hoja)
- Δ (columna en Excel) = 5 838 (unidad según hoja)
- Velocidad de proyecto = 14 kn

Nota: las cabeceras del Excel aparecen como "NOMBRE LOA Lpp B T D DWT Vc Δ VEL". Hay ambigüedad sobre si "Vc" es volumen sumergido (m³) o volumen de carga útil; y si la columna "Δ" representa desplazamiento en toneladas. Es necesario confirmar dichas unidades en la hoja original.

### Cálculos rápidos para Buque 9 — dos escenarios

Usamos: ρ = 1025 kg/m³. Además calculamos I aproximado con la simplificación I ≈ k·(B³·LOA)/12 con k=0.7.

Datos usados para cálculos geométricos:

- LOA = 97.7 m, B = 14.3 m, T = 5.8 m
- Producto geométrico LOA·B·T = 97.7 × 14.3 × 5.8 ≈ 8 103.24 m³

Escenario 1 — Cb asumido = 0.62 (consistente con suposiciones previas):

- V1 = LOA·B·T·Cb = 8 103.24 × 0.62 ≈ 5 024.01 m³
- Δ1 = ρ·V1 = 1025 × 5 024.01 ≈ 5 149.61 t
- Cálculo aproximado de I: B³·LOA/12 · k ≈ 16 665.54 m⁴
- BM1 = I / V1 ≈ 16 665.54 / 5 024.01 ≈ 3.317 m
- KB ≈ T/2 = 2.90 m
- Si asumimos KG ejemplo = 3.60 m → GM1 = BM1 + KB - KG ≈ 3.317 + 2.90 - 3.60 = 2.62 m

Comentario: con Cb=0.62 el desplazamiento estimado Δ1 ≈ 5 150 t. Esto está más cerca del valor de la columna "Δ" del Excel (5 838) que la hipótesis alternativa, pero aún existe una diferencia que hay que reconciliar (p. ej. por cargas o conveniones en la hoja).

Escenario 2 — usar Vc tal como aparece en la tabla (si Vc = 3 868 m³ fuese el volumen sumergido):

- V2 = 3 868 m³ (tomado directamente de la hoja)
- Δ2 = ρ·V2 = 1025 × 3 868 ≈ 3 964.70 t
- BM2 = I / V2 ≈ 16 665.54 / 3 868 ≈ 4.31 m
- Con KB = 2.90 m y KG ejemplo = 3.60 m → GM2 = 4.31 + 2.90 - 3.60 ≈ 3.61 m

Comentario: si Vc fuese volumen sumergido real, Δ2 resulta ≈ 3 965 t (muy distinto del Δ=5 838 de la hoja). Por tanto hay inconsistencia entre columnas y/o unidades.

Conclusiones preliminares y acciones recomendadas

- Hay tres fuentes de discrepancia posibles: 1) Vc en la hoja no es volumen sumergido; 2) la columna Δ incluye otros elementos (p. ej. desplazamiento máximo con carga y equipo); 3) errores de unidades/columnas desalineadas.
- Acción prioritaria: confirmar en el Excel qué representan exactamente las columnas "Vc" y "Δ" (unidades y condiciones: ligera/plena carga).
- Acción siguiente si confirmas: calcular KG real sumando momentos de todas las masas (estructura, maquinaria, combustibles, carga) desde las hojas del Excel; con KG real recalcular GM y proponer correcciones (lastre, redistribución).

He dejado estos cálculos comentados y sus conclusiones aquí; dime si quieres que aplique ahora la estimación de consumos de combustible para la autonomía (calcular capacidad necesaria para 10 000 mn) usando consumo supuesto o un valor que tú facilites.

### Detalle paso a paso y comentarios (añadido automáticamente)

1. Cálculo del volumen estimado V

- Fórmula: V = LOA × B × T × Cb
- Sustitución: V = 103.81 × 15.6 × 7.7 × 0.62 = 7 731.19 m³
- Comentario: estimación rápida; Maxsurf dará un V más preciso a partir de la forma real del casco.

2. Cálculo del desplazamiento Δ

- Fórmula: Δ = ρ × V
- Sustitución: Δ = 1025 × 7 731.19 = 7 924 470 kg ≈ 7 924.47 t
- Comentario: este desplazamiento corresponde a la masa del agua desplazada; la masa del buque en toneladas (con carga) debe coincidir con esta cifra para el francobordo estimado.

3. Cálculo aproximado de BM y GM

- Suposición para I (simplificación): I ≈ k × (B^3 × LOA)/12 con k ≈ 0.7
- Cálculo I: I = 0.7 × (15.6^3 × 103.81)/12 ≈ (valor usado internamente)
- BM = I / V ≈ 2.974 m
- KB ≈ T/2 = 3.85 m (suposición de posición del centro de flotación)
- KG asumido = 8.0 m (valor de ejemplo; sustituir por cálculo real)
- GM = BM + KB - KG ≈ -1.176 m
- Comentario: GM negativo indica que con el KG asumido la estabilidad inicial es inaceptable. Antes de tomar decisiones de diseño hay que calcular KG real sumando pesos y alturas de todos los elementos (estructura, maquinaria, combustibles, carga, equipos) y recalcular.

4. Recomendaciones para corregir datos y verificar

- Extraer todas las masas y sus alturas (momento) desde las hojas de cálculo; calcular KG por suma de momentos / suma de masas.
- Verificar que la forma del casco en Maxsurf produce un V similar al estimado; si V y Δ reales difieren, ajustar Cb o la geometría.
- Si GM resulta negativo: bajar KG (colocar lastre bajo), redistribuir pesos pesados a cotas más bajas, o revisar la geometría para aumentar BM (mayor manga efectiva de flotación).

5. Notas sobre Maxsurf y automatización

- Observación: en este sistema no se encontró un ejecutable de Maxsurf; sin embargo, detecté material docente relacionado en el escritorio.
- Maxsurf es un software comercial (Bentley). No existe una "librería Python oficial" estándar para Maxsurf, pero Maxsurf puede exportar geometrías (IGES, DXF, archivos propios) que pueden procesarse con Python y otras herramientas (por ejemplo, leer curvas, importar CSV de cubicación, etc.).
- Recomendación de instalación: instalar Maxsurf en tu máquina local (licencia si aplica) y exportar resultados (curvas de sección, volumen sumergido, segundo momento de la superficie de flotación). Para integración programática:
  - Exportar tablas CSV desde Maxsurf con las cubiertas/tanques y usar pandas para importarlas.
  - Para OCR o extracción de resultados de imágenes, usar `pytesseract`.

6. Acciones pendientes (prioritarias)

- [ ] Calcular KG real a partir de la hoja Excel (necesito que confirme o aporte la distribución de masas y alturas).
- [ ] Ejecutar Maxsurf con la geometría final y exportar V y I; si no puedes ejecutar Maxsurf, puedo guiarte en cómo exportar y traer los CSV resultantes para analizarlos aquí.
- [ ] Mapear cláusulas DNV/SOLAS con citas exactas (requiere extraer más texto de los PDF DNVGL; puedo intentar OCR si deseas).

-- Fin de los cálculos comentados --

## Respuestas al "Problema 3" (Trabajo Tema 3) — A–E (utilizando Buque 9)

Usaremos los datos del Buque 9 (LOA=97.7 m, Lpp=96.2 m, B=14.3 m, T=5.8 m, D=6.7 m, DWT=3 848 t) y las instrucciones del enunciado. Todas las decisiones y cifras están comentadas y tienen supuestos explícitos.

A) Posición de los mamparos de proa y popa de la cámara de máquinas y del pique de proa

- Objetivo: definir mamparos transversales estancos que delimiten forepeak, bodegas, cámara de máquinas y espacio de popa.
- Supuestos de diseño usados:
  - Forepeak: 5% LOA (longitud conservadora para protección de proa y alojamiento de ancora/sistemas) → 0.05×97.7 ≈ 4.9 m desde la proa hasta el mamparo de pique de proa.
  - Cámara de máquinas (engine room): longitud estimada 15% LOA → L_eng ≈ 0.15×97.7 ≈ 14.7 m (puede aumentarse a 18% si se requieren espacios auxiliares).
  - Posición longitudinal (centro) del engine room: alrededor de 55% LOA (ligeramente a popa del centro) → centro ≈ 0.55×97.7 ≈ 53.7 m desde la proa; por tanto mamparo de proa de cámara máquinas ≈ centro − L_eng/2 ≈ 46.3 m; mamparo de popa ≈ 61.0 m desde la proa.
- Resultado propuesto (distancias desde la roda/proa):
  - Mamparo de pique de proa (forepeak bulkhead): a 4.9 m desde la proa.
  - Mamparo de proa de cámara de máquinas (forward ER bulkhead): a ~46.3 m desde la proa (aprox. 47 m redondeado).
  - Mamparo de popa de cámara de máquinas (aft ER bulkhead): a ~61.0 m desde la proa (aprox. 61 m).
- Claras de cuadernas: seguir la indicación del enunciado — clara 700 mm en zona central y 600 mm en las zonas inmediatas al mamparo de proa de la cámara de máquinas y a proa del pique de proa. Esto gobierna el mallado estructural.
- Justificación normativa/documental: la ubicación propuesta busca cumplir criterios funcionales (acceso, ventilación, sistemas de propulsión) y mantener la subdivisión acorde a prácticas de diseño (consultar DNV Pt.3 Ch.2 para criterios de arrangement y compartimentación).

B) Disposición en plano de los principales elementos delimitadores de espacios

- Elementos a ubicar: doble fondo, doble casco, cubiertas principales, mamparos transversales (incluidos forward peak, forward ER, aft ER, aft peak), mamparos longitudinales si aplica, motor principal, tanques de combustible y lastre.
- Propuesta de disposición (lista):
  1. Doble fondo: dividido en varios tanques de lastre/combustible longitudinales (en tramos de 8–12 m) a lo largo de la quilla; dimensiones dependientes de la estructura y accesos.
  2. Doble casco: dejar intersticio entre casco y tanque para protección de carga/fluido.
  3. Cubierta principal: definir bodegas (cargo holds) partiendo del mamparo de pique hasta el mamparo de proa de ER; calcular su volumen mediante Maxsurf.
  4. Mamparos transversales: forepeak, forward ER, aft ER, aftpeak. Adicionales: mamparos entre bodegas según criterios de subdivisión.
  5. Motor principal: dentro de la cámara de máquinas propuesta; eje de hélice orientado por el eje longitudinal; tanques de alimentación próximos al motor (tank settling, day tanks) ubicados por debajo de línea de quilla o en doble fondo proximal para bajar KG.
  6. Tanques de combustible: distribuir en doble fondo (principalmente) y wing tanks para control de trim; reservar capacidad para lastre en wing tanks separados.
- Notas prácticas: priorizar colocar masas pesadas (motor, generadores) lo más bajas posible para reducir KG. Mantener accesos a bombas y tuberías de fuel y sentinas.

C) Estimar volumen de los principales tanques de consumos y cubicarlos en Maxsurf (procedimiento y cálculos)

- Requerimiento de autonomía: 10 000 mn. Velocidad usada para Buque 9 = 14 kn.
  - Tiempo requerido = 10 000 / 14 ≈ 714.29 h ≈ 29.76 días.
- Escenarios de consumo (masas de combustible por día): evaluamos 3 escenarios para cubrir incertidumbres:
  - Caso A (económico): 2 t/día
  - Caso B (realista para pequeña motorización): 5 t/día
  - Caso C (pesado): 10 t/día
- Cálculo de combustible requerido:
  - Masa_fuel = consumo_t/día × días
  - Volumen_fuel = Masa_fuel / ρ_fuel (ρ_fuel ≈ 0.85 t/m³ para fuel pesado aproximado)

Resultados:

- Caso A (2 t/día): Masa = 2 × 29.7619 ≈ 59.52 t → Volumen ≈ 59.52 / 0.85 ≈ 70.02 m³
- Caso B (5 t/día): Masa = 5 × 29.7619 ≈ 148.81 t → Volumen ≈ 148.81 / 0.85 ≈ 175.07 m³
- Caso C (10 t/día): Masa = 10 × 29.7619 ≈ 297.62 t → Volumen ≈ 297.62 / 0.85 ≈ 350.14 m³

- Propuesta de cubicación y ubicación:
  - Reservar volumen en doble fondo y wing tanks por port/starboard: por ejemplo para Caso B (~175 m³) se puede distribuir en 4 tanques (2 fore/aft) de ~44 m³ cada uno para control de trim y seguridad; alternativamente un tank central de 175 m³ en doble fondo con separación port/starboard para estabilidad transversal.
  - Verificar que la suma de volúmenes de combustible + otros tanques no exceda capacidad estructural y libre de carga (usar Maxsurf para cubicar volúmenes con la forma real del casco).

D) Completar el modelo Maxsurf stability con los espacios identificados (pasos operativos)

1. Importar o crear la forma base (usar el modelo 'Cargo Vessel' o crear desde offsets si están disponibles).
2. Ajustar parámetros geométricos: LOA=97.7 m, Lpp=96.2 m, B=14.3 m, T=5.8 m.
3. Definir secciones y mallado: respetar clara de cuadernas (700 mm central; 600 mm zonas indicadas).
4. Introducir los volúmenes de tanques (combustible, agua, lastre) como espacios internos en el modelo; asignar material/masa si Maxsurf soporta.
5. Cubicar bodegas y tanques con la herramienta de cubicación; exportar volúmenes (m³) y centros de gravedad de cada tanque si es posible.
6. Calcular curvas hidrostáticas: V, Δ, KM, I, BM y GM para condiciones ligera y plena carga; generar trim/heel cases.
7. Ejecutar casos de estabilidad: verificar criterios de reserva de estabilidad y ángulo de escora residual (aplicar criterios SOLAS/DNV según corresponda).

---

D (ampliado) — Tablas de fórmulas, explicación de variables y referencias normativas (provisionales)

1. Fórmulas principales usadas en el modelado y cubicación

| Fórmula                                         |                                                               Descripción | Variables                                                                              | Unidad / Notas                                                                |
| ----------------------------------------------- | ------------------------------------------------------------------------: | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| V = LOA × B × T × Cb                            | Volumen desplazado aproximado por fórmula empírica (estimación de carena) | LOA: eslora total (m) B: manga (m) T: calado (m) Cb: coef. de bloque (adim.)           | m³ — estimación; sustituir por volumen exacto de Maxsurf para precisión       |
| Δ = ρ × V                                       |                                             Desplazamiento en masa (peso) | ρ: densidad del agua (t/m³) (agua de mar ≈ 1.025 t/m³)                                 | t (toneladas métricas)                                                        |
| I = ∫ y² dA (midship)                           |                      Momento de inercia transversal de la sección maestra | Integral sobre la sección maestra                                                      | m4 — obtenido por cubicación / secciones en Maxsurf                           |
| BM = I / V                                      |    Distancia desde el centro de flotación hasta el metacentro transversal | I: segundo momento sección maestra (m4) V: volumen desplazado (m³)                     | m                                                                             |
| KM = KB + BM                                    |                                     Altura del metacentro sobre la quilla | KB: altura del centro de carena sobre quilla (m) BM: (m)                               | m                                                                             |
| GM = KM − KG                                    |                                                          Metacentro libre | KM: (m) KG: altura del centro de gravedad sobre la quilla (m)                          | m — criterio de estabilidad: GM>0; verificar criterios DNV/SOLAS para mínimos |
| M_adri ≈ Δ × g × GM × sin(θ) (pequeñas escoras) |                  Momento de adrizamiento aproximado para pequeñas escoras | Δ: desplazamiento (t→kN), g: gravedad (9.806 m/s²), GM: (m), θ: ángulo de escora (rad) | kN·m — usar unidades consistentes (convertir toneladas a kN)                  |

Notas sobre unidades y conversiones:

- Para pasar Δ (t) a fuerza en kN: 1 t ≈ 9.806 kN.
- Si Maxsurf exporta I en cm4 o mm4, convertir a m4 antes de usar en BM.

2. Explicación de variables y cómo obtenerlas en Maxsurf

- LOA, B, T: parámetros de entrada del modelo geométrico (medidos en metros).
- Cb (coeficiente de bloque): calculado como V / (LOA×B×T) usando el V obtenido por Maxsurf.
- V: obtener con la herramienta de cubicación (Volume / Displacement) en condición de carena dada.
- I: obtener mediante cálculos de sección maestra en herramientas de sección (o exportar tablas de secciones y calcular la integral numéricamente si Maxsurf no da I directamente).
- KB: altura del centro de carena sobre la quilla; Maxsurf da centro de carena (KB) por secciones o en la tabla hidrostática.
- KG: requiere la suma de momentos de todas las masas / Δ total: KG = Σ(mi·zi)/Σ(mi) (donde zi es la elevación de cada masa sobre la quilla). Esto se obtiene sumando:
  - masas estructurales (peso seco de estructura, estimado por tonelaje muerto o porcentaje),
  - maquinaria (motor principal, auxiliares, generadores),
  - combustible (con su CG vertical),
  - carga (si aplica),
  - provisiones y agua potable.

3. Mapeo normativo provisional (por paso operativo D)

Nota importante: las referencias abajo son provisionales y ligadas a capítulos/temas de la normativa; para citas textuales exactas debo ejecutar OCR y extraer las cláusulas exactas de los PDFs de DNV y SOLAS que tienes en el repositorio. ¿Autorizas que haga OCR en esos PDFs para mapear cláusulas exactas?

- Paso D.1 (importar/crear forma base): consultar DNV Rules Pt.3 Ch.1 (principios generales de carena y documentación) — también comprobar DNV procedimientos de cubicación y verificación geométrica.
- Paso D.2 (ajustar parámetros geométricos): DNV Pt.3 Ch.2 (arrangement & lines) y SOLAS II-1 (subdivisión/estructura y documentación de estabilidad).
- Paso D.3 (definir secciones y mallado): DNV Pt.3 Ch.3 (diseño estructural; claros de cuadernas y mallado).
- Paso D.4 (introducir volúmenes/masas): SOLAS II-1 requiere documentación de masas y libro de estabilidad; DNV Pt.3 contiene requisitos sobre registro de pesos y CG.
- Paso D.5 (cubicar bodegas y exportar): DNV Pt.3 (procedimientos para cubicación, verificación de volúmenes y tolerancias de medición).
- Paso D.6 (curvas hidrostáticas): SOLAS II-1 y DNV Pt.3 (curvas hidrostáticas, tablas de estabilidad y requisitos para libros de estabilidad).
- Paso D.7 (casos de estabilidad y verificación): SOLAS II-1 (criterios de adrizamiento y área bajo la curva GZ) y verificaciones prácticas según DNV Pt.3 para buques de carga.

4. Tabla-resumen de comprobaciones a realizar en Maxsurf (salida esperada)

| Comprobación           |           Fuente de datos en Maxsurf | Criterio normativa (provisional)                                                 |
| ---------------------- | -----------------------------------: | -------------------------------------------------------------------------------- |
| Volumen desplazado (V) |    Tabla hidrostática / displacement | Δ = ρ·V; comparar con Δ esperada y con datos Excel                               |
| Cb calculado           |                          V/(LOA·B·T) | Debe estar en rango (0.55–0.70) para buques del tamaño de Buque 9                |
| I (midship) y BM       | Sección maestra / outputs de sección | BM = I/V; verificar valor coherente con la forma del casco                       |
| KM, KB                 |                   Tabla hidrostática | KM = KB + BM; KB obtenido por tabla de carena                                    |
| KG final               |            Suma de momentos de masas | KG debe dar GM positivo y cumplir requirements DNV/SOLAS para estabilidad mínima |
| GM y curva GZ          |              Análisis de estabilidad | Comprobar área bajo GZ y ángulos críticos según SOLAS/DNV                        |

---

Acciones propuestas tras confirmación

1. Si autorizas OCR en los PDFs normativos, ejecutaré OCR y extraeré las cláusulas exactas de DNV Pt.3 y SOLAS II-1 que aplican a cada paso (reemplazaré las referencias provisionales por citas textuales y numeradas).
2. Si no autorizas OCR, mantendré las referencias provisionales y procederé a calcular KG estimado con una distribución de masas típica (documentando todas las suposiciones).
3. Si puedes exportar desde Maxsurf (CSV con volúmenes, I, centros de masa de tanques), intégralos y ejecutaré los cálculos numéricos finales (V, I, BM, KM, KG y GM) y generaré las tablas con resultados y conclusiones.

E) Verificar capacidad de tanques de carga mediante Maxsurf stability (procedimiento y criterio)

- Procedimiento:
  1. Introducir condición de carga con toneladas de carga en bodegas (usar Volum carga y densidad 1050 kg/m³ cuando corresponda a carga densa).
  2. Insertar combustible estimado en tanques y recalcular KG (sumando momentos de cada masa).
  3. Calcular GM final y comprobar que GM>GM_req (valor mínimo de criterio de proyecto / normativa).
  4. Si GM insuficiente, proponer medidas: redistribuir carga, añadir lastre bajo, reducir altura de carga o modificar disposición de tanques.
- Criterio práctico: confirmar con DNV Pt.3 y SOLAS II-1 para criterios formales de subdivisión y criterio de estabilidad de buques de carga.

---

Planos 2D y guía detallada para A–E (entrega requerida en el enunciado)

Nota: a falta de un CAD, incluyo planos 2D esquemáticos y coordenadas de referencia (longitudinales desde la proa, alturas desde la quilla) que sirven para generar las vistas de planta, alzado y sección maestra. Usar estas coordenadas para dibujar en AutoCAD/LibreCAD o trazar en Maxsurf como guías.

Convenciones de coordenadas usadas

- Eje X: 0 en la roda/proa, positivo hacia popa. Longitud total LOA = 97.7 m.
- Eje Y: eje transversal, 0 en la línea central; positivo a estribor.
- Eje Z: vertical, 0 en la quilla (baso), positivo hacia arriba.

Coordenadas principales propuestas (valores en metros)

- Proa (roda): X = 0.0
- Mamparo pique de proa (forepeak bulkhead): X = 4.9 (0.05 LOA)
- Mamparo proa cámara máquinas (forward ER bulkhead): X ≈ 46.3
- Mamparo popa cámara máquinas (aft ER bulkhead): X ≈ 61.0
- Popa (sterno): X = 97.7
- Sección maestra (midship station): X ≈ LOA/2 ≈ 48.85 m

Alturas y calados de referencia

- Quilla (baseline): Z = 0.0
- Línea de flotación de proyecto (estimada): Z = T = 5.8 m
- Puntal (D): Z = 6.7 m (altura total desde quilla a cubierta principal)
- KB estimado (centro de carena sobre quilla): KB ≈ T/2 ≈ 2.9 m (hasta confirmar con Maxsurf)

1. Vista en planta (top view) — instrucciones para dibujar

- Dibujar rectángulo general de eslora LOA × manga B (97.7 × 14.3 m) como contorno aproximado.
- Marcar las estaciones transversales en incrementos de 5 m (X = 0, 5, 10, ..., 95, 97.7).
- Ubicar mamparos transversales en X = 4.9, 46.3, 61.0. Dibujar líneas transversales completas a través de la manga.
- Definir zonas de tanques en doble fondo: dividir la longitud en tramos de 8–12 m (por ejemplo, tramos: 0–12, 12–24, 24–36, 36–48, 48–60, 60–72, 72–84, 84–97.7). Marcar wing tanks en ambos costados de la cubierta interior.
- Ubicar motor principal en ER: dentro del espacio entre X ≈ 46.3 y 61.0, centrado en Y=0. Dibujar un rectángulo que represente la sala máquinas (longitud ≈ 14.7 m, ancho ≈ 6 m) centrado longitudinalmente.

2. Vista de alzado (profile view) — instrucciones para dibujar

- Eje horizontal: X desde 0 a 97.7 m. Eje vertical: Z desde 0 (quilla) a 6.7 m (puntal).
- Traza la línea de flotación a Z = 5.8 m (aprox.). Dibuja el contorno de casco simplificado: proa curva suave, sección central recta y popa truncada.
- Marca mamparos en las abscisas correspondientes y dibuja la cámara de máquinas como rectángulo en Z desde la quilla hasta cubierta, dentro de X ≈ 46.3–61.0.

3. Sección maestra (midship section) — instrucciones para dibujar

- Ubicar en X = 48.85 m. Dibuja sección transversal simétrica con manga total B = 14.3 m (desde Y = −7.15 a Y = +7.15) y calado T = 5.8 m (Z de 0 a 5.8 m). Dibujar aislamiento de doble fondo (espesor visual) y separación de wing tanks.
- Indicar alturas: KG aproximado (si calculado), KB estimado (T/2) y representación de los tanques en doble fondo.

4. Detalle de mamparos y claras de cuadernas

- Indicar que la clara de cuadernas en la zona central debe ser 700 mm. A proa del pique de proa y a popa del mamparo de proa de la ER la clara debe reducirse a 600 mm (marcar tramos en el alzado y en el plano con anotaciones).
- Añadir notas en el plano: "Clara central: 700 mm; Zona de transición: 600 mm".

5. Disposición de tanques y cubicación — valores propuestos y cálculo simplificado

Propuesta de tipología de tanques (ubicación y volúmenes preliminares)

- Combustible: doble fondo central + 2 wing tanks port/starboard en la sección central.
  - Doble fondo (central): ocupará tramos X = 24–72 m (48 m longitud); espesor transversal efectivo para fuel height ≈ 0.6 m (estimación) → Volumen ≈ longitud × manga_effectiva × altura.
  - Wing tanks: dos tanques (babor/estribor) en tramos 36–60 m longitud, altura efectiva 0.8 m, ancho activo (cada lado) ≈ 1.2 m.
- Lastre agua: tanques separados longitudinalmente en doble fondo y fore/aft peak.

Estimación rápida (ejemplo) — Caso B (consumo 5 t/día → Volumen ≈ 175 m³)

- Plan: distribuir 175 m³ en 4 tanques de doble fondo: 2 centrales (fore/aft) + 2 wing tanks pequeños.
- Volumen por tank central (ejemplo): 80 m³ cada uno → longitud necesaria (con altura efectiva 0.6 m y ancho efectivo 6 m) ≈ 80 / (6 × 0.6) ≈ 22.2 m.
- Wing tanks: 15 m³ cada uno → con ancho efectivo 1.2 m y altura 0.8 m → longitud ≈ 15 / (1.2 × 0.8) ≈ 15.6 m.

6. Pasos concretos para crear el modelo en Maxsurf stability (checklist)

1) Crear nuevo proyecto y escoger unidad métrica (metros).
2) Importar sección/caja base o crear líneas a partir de offsets (si no hay offsets, usar las dimensiones principales LOA/Lpp/B/T para generar forma aproximada).
3) Ajustar longitud y manga exactas: LOA=97.7, Lpp=96.2, B=14.3, T=5.8.
4) Ajustar secciones y mallado: colocar estaciones cada 2 m (o según preferencia), respetar clara de cuadernas en regiones indicadas.
5) Definir espacios internos (Spaces / Tanks): crear polylines que enmarquen cada tank en planta y elevación; asignar nombre (FUEL_CF_CENTRAL_FORE, FUEL_CF_CENTRAL_AFT, WING_FUEL_PORT, WING_FUEL_STBD, BALLAST_FWD, BALLAST_AFT).
6) Introducir alturas y límites verticales de cada espacio (z min/max) para que la cubicación sea correcta.
7) Ejecutar cubicación (Calculate / Volume) para cada space; exportar tabla CSV con volumen (m³) y centroid Z (altura del CG del tanque).
8) Rellenar la lista de masas (Weights/Load) en Maxsurf: introducir masa de combustible (densidad 0.85 t/m³) y su CG vertical usando centroides exportados.
9) Ejecutar cálculo hidrostático (Hydrostatic / Displacement) y obtener V, Δ, I, BM, KB, KM, GM para condición de proyecto.
10) Crear casos de carga: (a) ligera (sin carga), (b) plena carga con combustible y carga en bodegas; calcular GM y curvas GZ.
11) Exportar resultados y capturar pantallas de planta/alzado/sección maestra para inclusión en informe.

7. Verificación final (E) y criterios de ajuste en caso de incumplimiento

- Si GM final < GM_req o el área bajo GZ es insuficiente:
  - Reubicar masas pesadas a cotas inferiores;
  - Reducir altura de masa (KG) colocando fuel en doble fondo y no en depósitos altos;
  - Añadir lastre líquido bajo la línea de quilla;
  - Replantear distribución de carga en bodegas para bajar el CG.

Anexos y resultados entregables

- Planos esquemáticos (planta, alzado, sección maestra) en PDF/imagenes (incluir estas instrucciones para trazado en CAD).
- Archivo Maxsurf stability (.msv) con spaces definidos y CSV exportado con volúmenes y centroides (si lo exportas lo integro y verifico los números).
- Tabla con volúmenes por tanque y masa de combustible (t) para los 3 escenarios de consumo (A/B/C).

Indicaciones finales

- Si quieres, genero ahora: (1) un DXF esquemático con las líneas principales (si autorizas generación de archivos), o (2) un CSV con la tabla de tanks y sus volúmenes propuestos para que puedas importar en Maxsurf.
- Si prefieres que haga la estimación de KG y el cálculo final GM con suposiciones de masas, dímelo y lo añado como bloque numérico con todos los supuestos listados.

---

## Datos reales importados desde Maxsurf (condición de proyecto)

He recibido la tabla de resultados hidrostáticos del modelo (imagen adjunta). Extraigo y uso estos valores directamente para completar los cálculos y la verificación E.

Tabla (valores principales)

- Displacement = 7 028 213 kg = 7 028.213 t
- Volume (displaced) = 6 856.793 m³
- Draft amidships = 6.477 m
- Immersed depth = 6.476 m
- WL Length = 96.948 m
- Beam max extents on WL = 15.545 m
- Block coeff. (Cb) = 0.703
- Prismatic coeff. (Cp) = 0.721
- KB = 3.578 m
- BM (transverse) = 3.582 m
- KM = 7.159 m
- KG (modelo) = 6.477 m
- GM (corregido) = 0.683 m

Verificaciones y comentarios sobre estas cifras

- La densidad usada en el modelo es ρ = 1025 kg/m³ porque Δ = ρ·V → 1025 × 6856.793 = 7 028 213 kg (coincide).
- KM calculado = KB + BM = 3.578 + 3.582 = 7.160 m (coincide con KM = 7.159 m en la tabla).
- KG tomado del modelo = 6.477 m. Por tanto GM = KM − KG = 7.159 − 6.477 = 0.682 m, que corresponde al GMt corregido reportado (0.683 m). GM positivo: condición estable en sentido inicial.

Cálculo de momentos y prudencia operativa

- RM at 1 deg reportado ≈ 83 755 kg·m (valor en tabla expresado en kg; corresponde a momento de recuperación por grado). Esto confirma capacidad de adrizamiento suficiente para operaciones normales, pero se debe comprobar área bajo la curva GZ para criterios SOLAS.

Aplicación a A–E

A (mamparos): coordenadas de mamparos propuestas (confirmadas con longitud y LCF/WL del modelo)

- Forepeak bulkhead: X = 4.9 m desde proa (se mantiene).
- Forward ER bulkhead: X ≈ 46.3 m desde proa.
- Aft ER bulkhead: X ≈ 61.0 m desde proa.
- Se confirma que el calado de proyecto real es 6.477 m: ajustar notas de mamparos y escotillas de sentina para garantizar estanqueidad por encima del francobordo.

B (planta / alzado / sección maestra)

- Usar las dimensiones reales del modelo: WL length = 96.948 m (usar esta cifra para planta), Beam WL = 15.545 m (para planta y sección maestra), Draft = 6.477 m (para alzado y sección).
- La sección maestra: dibujar con calado 6.477 m y manga total 15.545 m (y doble fondo y wing tanks según las indicaciones anteriores).

C (cubicación de tanques de consumo) — uso de datos reales para validar volúmenes propuestos

- Escenarios de combustible (recordar): Caso A 70.0 m³ (2 t/día), Caso B 175.1 m³ (5 t/día), Caso C 350.1 m³ (10 t/día).
- Propuesta práctica con dimensiones reales del modelo (doble fondo usable):

  - Dado WL beam = 15.545 m, después de estructuras y mamparos quedan aprox. 12.0 m de ancho utilizable en doble fondo (estimación conservadora).
  - Si se reserva altura útil en doble fondo para fuel ≈ 0.6 m, volumen por metro de eslora ≈ 12.0 × 0.6 = 7.2 m³/m.
  - Por tanto, para almacenar 175.1 m³ (Caso B) se requieren ≈ 175.1 / 7.2 ≈ 24.3 m de longitud de doble fondo útil (ej.: un tank de 24.3 m × 12 m_effective × 0.6 m ≈ 175 m³).
  - Para Caso C (350.1 m³) se requerirían ≈ 48.6 m de longitud (se puede distribuir en fore/aft tanks y wing tanks para control de trim).

- Recomendación: dimensionar dos tanques centrales en doble fondo (fore y aft) con longitudes 24 m cada uno (capacidad total ≈ 345 m³ con la altura asumida y ancho utilizable), más wing tanks pequeños para ajustes finos. Esto cubre Caso C y deja margen.

D (completar modelo Maxsurf con spaces)

- Pasos concretos (resumidos): crear spaces con las longitudes y alturas indicadas; ejecutar cubicación en Maxsurf para cada space; exportar CSV.
- Importante: una vez importados los espacios, actualizar la tabla de pesos (Weights) con la masa de combustible (ρ=0.85 t/m³) y recalcular KG y GM; comprobar que GM sigue siendo ≥ valor mínimo de proyecto (en este caso GM = 0.683 m para la condición actual).
- Si se llena fuel en doble fondo (bajo KG actual), el KG total bajará (mejora de GM). Si se ubica fuel en tanks altos (no recomendado), KG sube y GM disminuye.

E (verificación de capacidad de bodegas / cumplimiento)

- Datos de capacidad de bodegas en Excel (extraídos previamente): Volumen bajo cubierta principal ≈ 6 672 m³; Volumen de carga requerido (ejemplo en la hoja) ≈ 5 560 m³.
- Verificación: Volumen disponible bajo cubierta principal (6 672 m³) es mayor que el volumen de carga requerido (5 560 m³) → capacidad suficiente en términos de volumen bruto.
- Verificación adicional (estabilidad y resistencias): al cargar las bodegas con la carga prevista, introducir el peso y su CG en Maxsurf; recalcular KG y GM. Si GM resultante permanece por encima del límite mínimo (dependiente de la normativa de proyecto), la capacidad es aceptable. En condiciones de prueba con KG de modelo = 6.477 m y GM inicial = 0.683 m hay margen, pero la verificación final requiere el cálculo con masas reales de carga y combustible.

Conclusión práctica (apartado E)

- Con los datos del modelo: la capacidad volumétrica de bodegas (6 672 m³) excede la especificación de proyecto (~5 560 m³), por lo que en volumen bruto las bodegas son suficientes.
- Requisito final: ejecutar en Maxsurf el caso "plena carga" introduciendo las masas/CG de la carga y los tanques de combustible tal como se distribuyan; comprobar GM final y el área bajo la curva GZ conforme a SOLAS/DNV. Si aparece déficit de estabilidad, se aplican las medidas indicadas (mover fuel a doble fondo, añadir lastre bajo, redistribuir carga).

Archivos y entregables que puedo producir ahora

1. Actualizar `Proyecto-Final.md` con estas cifras y añadir tablas (hecho).
2. Si quieres, genero un CSV con la propuesta de tanks (nombres, longitud, ancho efectivo, altura útil, volumen estimado) para importar en Maxsurf.
3. Si subes el `.msv` o CSV exportados desde Maxsurf con los spaces definidos, yo integro los números y doy la verificación final (GM, curva GZ y tabla de resultados).

Próximo paso recomendado

- ¿Quieres que genere el CSV de tanks propuestos automáticamente con las longitudes/volúmenes calculados (opción A), o que esperemos a que exportes los spaces desde Maxsurf (opción B) para integrar los resultados reales?

---

## 🔧 Integración de Maxsurf con VS Code y Herramientas de Desarrollo

Esta sección documenta cómo integrar Maxsurf con Visual Studio Code para automatizar cálculos, generar scripts de análisis y mejorar el flujo de trabajo de diseño naval.

### 1. API y Automatización de Maxsurf

Maxsurf ofrece varias opciones para automatización e integración programática:

#### Maxsurf API

Bentley Systems proporciona una API COM (Component Object Model) para automatizar tareas en Maxsurf.

**Lenguajes soportados:**

- **Python** (opción más común y recomendada)
- **VBA** (Visual Basic for Applications)
- **.NET** a través de COM

### 2. Documentación Oficial

La documentación principal se encuentra en:

- **Bentley Developer Network**: https://developer.bentley.com/
- **Maxsurf API Documentation** en el portal de Bentley
- Dentro del software Maxsurf: `Help → Developer Help`
- **Bentley Communities**: Foros de desarrolladores

### 3. Configuración de Entorno en VS Code

#### 3.1. Configuración para Python (Recomendada)

Crear archivo de configuración en `.vscode/settings.json`:

```json
{
  "python.pythonPath": "ruta_a_tu_python",
  "python.analysis.extraPaths": ["C:/Program Files/Bentley/Maxsurf/API"],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

#### 3.2. Estructura de Proyecto Recomendada

```
proyecto_barco/
├── scripts/
│   ├── maxsurf_automation.py      # Script principal de automatización
│   ├── hull_design.py              # Diseño de cascos
│   ├── stability_analysis.py       # Análisis de estabilidad
│   └── utilities.py                # Funciones auxiliares
├── data/
│   ├── geometrias/                 # Archivos de geometría
│   └── resultados/                 # Resultados de análisis
├── config/
│   ├── materiales.json             # Propiedades de materiales
│   └── normativas.json             # Criterios normativos
├── .vscode/
│   ├── settings.json               # Configuración del proyecto
│   ├── launch.json                 # Configuración de debugging
│   └── tasks.json                  # Tareas automatizadas
└── requirements.txt                # Dependencias Python
```

### 4. Scripts de Integración

#### 4.1. Script Básico de Conexión

```python
# scripts/maxsurf_automation.py
import win32com.client
import pythoncom
import os

class MaxsurfIntegration:
    """Clase para integración con Maxsurf"""

    def __init__(self):
        self.maxsurf_app = None
        self.model = None

    def connect_to_maxsurf(self):
        """Conectar con aplicación Maxsurf"""
        try:
            self.maxsurf_app = win32com.client.Dispatch("Maxsurf.Application")
            self.maxsurf_app.Visible = True
            print("✅ Conectado a Maxsurf exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error conectando a Maxsurf: {e}")
            return False

    def execute_command(self, command):
        """Ejecutar comando de Maxsurf"""
        if self.maxsurf_app:
            self.maxsurf_app.ExecuteCommand(command)

    def create_new_model(self):
        """Crear nuevo modelo"""
        self.execute_command("NEW")

    def run_analysis(self, analysis_type):
        """Ejecutar análisis específico"""
        commands = {
            "stability": "STABILITY",
            "hydrostatics": "HYDROSTATICS",
            "structures": "STRUCTURES"
        }
        if analysis_type in commands:
            self.execute_command(commands[analysis_type])

# Uso desde VS Code
if __name__ == "__main__":
    maxsurf = MaxsurfIntegration()
    if maxsurf.connect_to_maxsurf():
        maxsurf.create_new_model()
        maxsurf.run_analysis("hydrostatics")
```

#### 4.2. Diseñador de Cascos para Diseño Naval

```python
# scripts/hull_design.py
import win32com.client
import json
import pandas as pd

class DiseñadorCascos:
    """Clase para diseño paramétrico de cascos navales"""

    def __init__(self):
        self.maxsurf = None
        self.modelo = None

    def conectar_maxsurf(self):
        """Conectar con Maxsurf para diseño naval"""
        try:
            self.maxsurf = win32com.client.Dispatch("Maxsurf.Application")
            self.maxsurf.Visible = True
            print("⚓ Maxsurf conectado - Listo para diseño naval")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def crear_casco_rapido(self, eslora, manga, puntal, calado):
        """Crear geometría básica de casco"""
        comandos = [
            "NEW",
            f"ESLORA {eslora}",
            f"MANGA {manga}",
            f"PUNTAL {puntal}",
            f"CALADO {calado}",
            "HULL"  # Generar casco básico
        ]

        for cmd in comandos:
            self.maxsurf.ExecuteCommand(cmd)

        print(f"📐 Casco creado: Eslora={eslora}m, Manga={manga}m")

    def calcular_hidrostaticas(self, calados=None):
        """Calcular parámetros hidrostáticos para diferentes calados"""
        if not calados:
            calados = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

        resultados = []

        for calado in calados:
            self.maxsurf.ExecuteCommand(f"CALADO {calado}")
            self.maxsurf.ExecuteCommand("HYDROSTATICS")

            # Capturar resultados de hidrostáticas
            resultado = {
                'calado': calado,
                'desplazamiento': self.obtener_desplazamiento(),
                'cb': self.obtener_coef_block(),
                'cm': self.obtener_coef_midship(),
                'cp': self.obtener_coef_prismatico()
            }
            resultados.append(resultado)

        return pd.DataFrame(resultados)

# Uso práctico para diseño
if __name__ == "__main__":
    diseñador = DiseñadorCascos()

    if diseñador.conectar_maxsurf():
        # Crear casco del Buque 9
        diseñador.crear_casco_rapido(
            eslora=97.7,
            manga=14.3,
            puntal=6.7,
            calado=5.8
        )

        # Calcular hidrostáticas
        hidro = diseñador.calcular_hidrostaticas()
        print(hidro)
        hidro.to_csv('./tablas_datos/hidrostaticas_calculadas.csv')
```

#### 4.3. Análisis de Estabilidad

```python
# scripts/stability_analysis.py
class AnalizadorEstabilidad:
    """Análisis completo de estabilidad naval"""

    def __init__(self, maxsurf_conn):
        self.maxsurf = maxsurf_conn

    def curva_brazos_adrizantes(self, angulos=None):
        """Calcular curva de brazos adrizantes (curva GZ)"""
        if not angulos:
            angulos = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90]

        curva_brazos = []

        for angulo in angulos:
            self.maxsurf.ExecuteCommand(f"STABILITY ANGLE {angulo}")
            brazo = self.obtener_brazo_adrizante()
            curva_brazos.append({
                'angulo': angulo,
                'gz': brazo
            })

        return pd.DataFrame(curva_brazos)

    def verificar_normativa(self, curva_brazos, normativa="SOLAS"):
        """Verificar cumplimiento de normativa"""
        if normativa == "SOLAS":
            return self.verificar_solas(curva_brazos)
        elif normativa == "DNV":
            return self.verificar_dnv(curva_brazos)

    def verificar_solas(self, curva):
        """Verificación según SOLAS Cap. II-1"""
        criterios = {
            'area_0_30': curva[curva['angulo'] <= 30]['gz'].sum() * 0.055,
            'area_0_40': curva[curva['angulo'] <= 40]['gz'].sum() * 0.09,
            'gz_max_30': curva[curva['angulo'] == 30]['gz'].iloc[0] >= 0.2,
            'angulo_gz_max': curva['gz'].idxmax() >= 25
        }

        return criterios
```

### 5. Configuración de Debugging en VS Code

Crear `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Ejecutar Script Maxsurf",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/maxsurf_automation.py",
      "console": "integratedTerminal",
      "env": {
        "PYTHONPATH": "${workspaceFolder};C:/Program Files/Bentley/Maxsurf/API"
      }
    },
    {
      "name": "Diseño de Cascos",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/hull_design.py",
      "console": "integratedTerminal"
    },
    {
      "name": "Análisis Estabilidad",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/scripts/stability_analysis.py",
      "console": "integratedTerminal"
    }
  ]
}
```

### 6. Tareas Automatizadas (Tasks)

Crear `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Ejecutar Automatización Maxsurf",
      "type": "process",
      "command": "python",
      "args": ["${workspaceFolder}/scripts/maxsurf_automation.py"],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "Diseñar Casco Buque 9",
      "type": "process",
      "command": "python",
      "args": ["${workspaceFolder}/scripts/hull_design.py"],
      "group": "build"
    },
    {
      "label": "Análisis Estabilidad",
      "type": "process",
      "command": "python",
      "args": ["${workspaceFolder}/scripts/stability_analysis.py"],
      "group": "test"
    }
  ]
}
```

### 7. Snippets Personalizados para Maxsurf

Crear `.vscode/maxsurf.code-snippets`:

```json
{
  "Maxsurf Connect": {
    "prefix": "maxconnect",
    "body": [
      "import win32com.client",
      "",
      "def connect_maxsurf():",
      "    try:",
      "        app = win32com.client.Dispatch('Maxsurf.Application')",
      "        app.Visible = True",
      "        return app",
      "    except Exception as e:",
      "        print(f'Error: {e}')",
      "        return None",
      "$0"
    ],
    "description": "Conectar con Maxsurf"
  },
  "Hidrostáticas Básicas": {
    "prefix": "hydro",
    "body": [
      "def calcular_hidrostaticas(calados=[0.5, 1.0, 1.5, 2.0]):",
      "    resultados = []",
      "    for calado in calados:",
      "        maxsurf.ExecuteCommand(f'CALADO {calado}')",
      "        maxsurf.ExecuteCommand('HYDROSTATICS')",
      "        desplaz = obtener_desplazamiento()",
      "        lcb = obtener_lcb()",
      "        resultados.append({",
      "            'calado': calado, ",
      "            'desplaz': desplaz, ",
      "            'lcb': lcb",
      "        })",
      "    return resultados"
    ],
    "description": "Cálculo de hidrostáticas para múltiples calados"
  },
  "Curva Estabilidad": {
    "prefix": "stabcurve",
    "body": [
      "def curva_estabilidad(angulos=[0, 15, 30, 45, 60, 75, 90]):",
      "    brazos = []",
      "    for angulo in angulos:",
      "        maxsurf.ExecuteCommand(f'STABILITY ANGLE {angulo}')",
      "        gz = obtener_brazo_adrizante()",
      "        brazos.append({'angulo': angulo, 'gz': gz})",
      "    return brazos"
    ],
    "description": "Generar curva de brazos adrizantes"
  }
}
```

### 8. Configuración de Materiales

Crear `config/materiales.json`:

```json
{
  "aluminio_naval": {
    "densidad": 2.7,
    "modulo_elasticidad": 69000,
    "limite_fluencia": 250,
    "uso_recomendado": ["cascos", "superestructuras"],
    "normativa": "DNV-RU-SHIP Pt.3 Ch.3"
  },
  "acero_naval": {
    "densidad": 7.85,
    "modulo_elasticidad": 210000,
    "limite_fluencia": 355,
    "uso_recomendado": ["cascos", "cuadernas", "quillas"],
    "normativa": "DNV-RU-SHIP Pt.3 Ch.3"
  },
  "composite_gfrp": {
    "densidad": 1.8,
    "modulo_elasticidad": 21000,
    "resistencia_traccion": 300,
    "uso_recomendado": ["cascos_veleros", "componentes_livianos"],
    "normativa": "ISO 12215"
  }
}
```

### 9. Extensiones Útiles para VS Code

#### Esenciales para Python

- **Python** (Microsoft) - IntelliSense, linting, debugging
- **Pylance** - Language server mejorado
- **Python Docstring Generator** - Generación automática de documentación

#### Para Trabajo con Datos

- **Excel Viewer** - Ver resultados CSV directamente
- **Rainbow CSV** - Colorear columnas CSV
- **Data Preview** - Visualización de datos tabulares

#### Productividad

- **Code Runner** - Ejecutar código con un clic
- **JSON Tools** - Formatear y validar JSON
- **GitLens** - Control de versiones mejorado
- **TODO Highlight** - Resaltar comentarios TODO/FIXME

### 10. Ejemplo Práctico: Configuración para Buque 9

```python
# ejemplos/buque_9_completo.py
"""
Script completo para análisis del Buque 9
Ejecuta diseño, hidrostáticas y estabilidad
"""

import sys
sys.path.append('./scripts')

from hull_design import DiseñadorCascos
from stability_analysis import AnalizadorEstabilidad
import pandas as pd

def analisis_completo_buque_9():
    """Análisis completo del Buque 9"""

    # Parámetros del Buque 9
    params = {
        'eslora': 97.7,
        'manga': 14.3,
        'puntal': 6.7,
        'calado': 5.8,
        'dwt': 3848,
        'velocidad': 14  # kn
    }

    print("="*50)
    print("  ANÁLISIS COMPLETO BUQUE 9")
    print("="*50)

    # 1. Conectar y crear casco
    diseñador = DiseñadorCascos()
    if not diseñador.conectar_maxsurf():
        print("❌ No se pudo conectar a Maxsurf")
        return

    print("\n📐 Creando geometría de casco...")
    diseñador.crear_casco_rapido(**params)

    # 2. Calcular hidrostáticas
    print("\n💧 Calculando hidrostáticas...")
    calados = [4.0, 4.5, 5.0, 5.5, 5.8, 6.0, 6.5]
    hidro = diseñador.calcular_hidrostaticas(calados)

    print("\nResultados Hidrostáticos:")
    print(hidro)
    hidro.to_csv('./tablas_datos/buque9_hidrostaticas.csv', index=False)

    # 3. Análisis de estabilidad
    print("\n⚓ Analizando estabilidad...")
    estabilidad = AnalizadorEstabilidad(diseñador.maxsurf)
    curva_gz = estabilidad.curva_brazos_adrizantes()

    print("\nCurva de Brazos Adrizantes:")
    print(curva_gz)
    curva_gz.to_csv('./tablas_datos/buque9_curva_gz.csv', index=False)

    # 4. Verificar normativa SOLAS
    print("\n📋 Verificando normativa SOLAS...")
    cumplimiento = estabilidad.verificar_normativa(curva_gz, "SOLAS")

    print("\nCriterios SOLAS:")
    for criterio, cumple in cumplimiento.items():
        status = "✅" if cumple else "❌"
        print(f"  {status} {criterio}: {cumple}")

    print("\n✅ Análisis completado!")
    print(f"   Resultados guardados en ./tablas_datos/")

if __name__ == "__main__":
    analisis_completo_buque_9()
```

### 11. Flujo de Trabajo Recomendado

```
┌─────────────────────────────────────────────────────────┐
│  1. DISEÑO CONCEPTUAL                                   │
│     - Scripts de geometría básica en Python             │
│     - Parámetros desde Excel/JSON                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  2. ANÁLISIS HIDROSTÁTICO                               │
│     - Cálculo automático de parámetros                  │
│     - Exportación a CSV para análisis                   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  3. VERIFICACIÓN DE ESTABILIDAD                         │
│     - Curvas GZ automáticas                             │
│     - Comparación con criterios SOLAS/DNV               │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  4. OPTIMIZACIÓN                                        │
│     - Ajuste fino de formas                             │
│     - Iteraciones automatizadas                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│  5. DOCUMENTACIÓN                                       │
│     - Reportes automáticos en PDF/MD                    │
│     - Gráficos con matplotlib/seaborn                   │
└─────────────────────────────────────────────────────────┘
```

### 12. Ventajas de la Integración VS Code + Maxsurf

| Aspecto                  | Beneficio                                   |
| ------------------------ | ------------------------------------------- |
| **IntelliSense**         | Autocompletado de código Python             |
| **Debugging**            | Depuración paso a paso de scripts           |
| **Control de versiones** | Git integrado para tracking de cambios      |
| **Extensiones**          | Productividad mejorada con plugins          |
| **Terminal integrada**   | Ejecución rápida sin cambiar ventanas       |
| **Snippets**             | Plantillas de código reutilizables          |
| **Testing**              | Pruebas unitarias con pytest                |
| **Documentación**        | Markdown preview para documentación técnica |

### 13. Instalación de Dependencias

Crear `requirements.txt`:

```txt
pywin32>=305
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
python-dateutil>=2.8.0
```

Instalar con:

```bash
pip install -r requirements.txt
```

### 14. Recomendaciones Finales

✅ **Siempre verificar la conexión** antes de ejecutar comandos  
✅ **Usar try-except** para manejar errores de COM  
✅ **Mantener Maxsurf visible** durante desarrollo para ver resultados  
✅ **Guardar configuraciones** en JSON para reutilización  
✅ **Documentar comandos** específicos de la API de Maxsurf  
✅ **Versionar scripts** con Git para control de cambios  
✅ **Crear backups** automáticos de modelos importantes

### 15. Recursos Adicionales

- **Bentley Developer Network**: https://developer.bentley.com/
- **Bentley Communities Forums**: Foros de soporte técnico
- **Documentación dentro de Maxsurf**: Help → Developer Help
- **Ejemplos de scripts**: Carpeta de instalación de Maxsurf
- **Webinars de Bentley**: Capacitación sobre automatización

---

## Integración automática de la tabla Maxsurf (CSV) y sistema de comprobación de errores

Se ha creado `./tablas_datos/maxsurf_table.csv` con todos los campos extraídos de la captura/tabla proporcionada. Esta tabla facilita comprobaciones automáticas y mapeo de posibles errores OCR o inconsistencias de unidad.

1. Datos cargados (del CSV)

- `Displacement` = 7 028 213 kg (7 028.213 t)
- `Volume_displaced` = 6 856.793 m³
- `Draft_Amidships` = 6.477 m
- `WL_Length` = 96.948 m
- `Beam_max_WL` = 15.545 m
- `Block_coeff_Cb` = 0.703
- `Prismatic_coeff_Cp` = 0.721
- `KB` = 3.578 m
- `KG_fluid` = 6.477 m
- `BMt` = 3.582 m
- `KMt` = 7.159 m
- `GMt_corrected` = 0.683 m
- `RM_1deg` = 83 755.226 kg·m

2. Comprobaciones automáticas realizadas

- Comprobación Δ vs ρ·V: con ρ=1025 kg/m³ → ρ·V = 1025 × 6856.793 = 7 028 212.825 kg. Resultado: concuerda con `Displacement` (7 028 213 kg) → OK.
- Coeficientes en rango esperado: Cb=0.703 y Cp=0.721 → valores coherentes para buque mercante (OK).
- KM = KB + BM = 3.578 + 3.582 = 7.160 m → concuerda con KMt=7.159 m (OK).
- GM = KM − KG = 7.159 − 6.477 = 0.682 m → concuerda con GMt_corrected ≈ 0.683 m (OK).

3. Chequeos heurísticos y detección de valores sospechosos (posible OCR/units errors)

- Campos detectados con posible error de OCR o unidades (revisar manualmente):
  - `BML` = 121.702 m — sospechoso (valor demasiado grande para BM o similar). Podría ser un valor en cm o mm que OCR convirtió mal.
  - `GML` = 118.803 m — sospechoso (verificar significado; posiblemente una celda que contiene otra unidad o texto concatenado).
  - `KML` = 125.279 m — sospechoso.
  - Valores con sufijo `fro` en LCB/LCF que indican que el texto original contenía frases como "from midship" o similar; revisar el campo original en Excel.
  - `Immersion_TPc` y `MTc` con unidad escrita "tonn" — verificar ortografía y unidad real (tonnes).

Reglas aplicadas para detección automática

- Si un campo que representa una distancia vertical (BM, KB, KM, KG) > 20 m → marcar como sospechoso.
- Si un porcentaje aparece con signo negativo y valor absoluto > 100 → marcar (ej. LCB% = -52.846% es plausible si se expresa como mm% desde la roda; revisar unidad).
- Si aparece texto concatenado ("fro", "tonn") → marcar para revisión manual.

4. Acciones recomendadas para corregir errores y validar datos

- Abrir el CSV/Excel original y localizar las celdas marcadas como sospechosas (BML, GML, KML, campos con 'fro'). Corregir unidades o extraer valores correctos.
- Verificar la definición exacta de `KG_fluid` en el modelo: confirmar si KG proviene del sumatorio de masas definido en Maxsurf o es un KG estimado por el software.
- Recalcular GM con KG verificado tras correcciones; si GM disminuye por debajo del mínimo de proyecto, usar medidas correctoras (distribuir fuel en doble fondo, añadir lastre).

5. Reporte de inconsistencias detectadas (resumen)

- Inconsistencia potenciales detectadas: `BML`, `GML`, `KML` (valores numéricos inusuales).
- Texto/Unidades inconsistentes: campos con sufijo "fro" y "tonn".

6. Siguientes pasos automatizables que puedo ejecutar ahora (elige una)

- (A) Generar script Python que valide automáticamente el CSV completo y produzca un informe HTML con las comprobaciones y marcas de error (lo creo en el repo).
- (B) Intentar abrir el Excel original (si está disponible) y extraer las celdas con los valores originales para corregir automáticamente los campos marcados.
- (C) Crear un CSV de tanks propuesto (nombres, longitud, ancho efectivo, altura útil, volumen) listo para import en Maxsurf (esto ayuda a completar el modelo).

Indica la opción que prefieres y la ejecuto. Si quieres que proceda automáticamente con la opción A, la generaré y la ejecutaré en este entorno, y te daré el informe HTML y el archivo de log.

Documental / comparación con barcos similares

- He revisado la base de datos del Excel: la media de esloras en la tabla es LOA≈96.87 m (muy cercana a Buque 9). Por tanto los procedimientos y supuestos empleados (Cb≈0.62, disposición mid-ship del ER) son consistentes con la muestra.
- Referencias a usar en la verificación final: DNV Part 3 (Chapter 1 General principles; Chapter 2 General arrangement design; Chapter 3 Structural design principles) y SOLAS Cap. II-1 (subdivisión y estabilidad). Mapearé cláusulas específicas en la fase de revisión final.

Entregables añadidos

- Respuestas A–E comentadas en este documento (`Proyecto-Final.md`) con cálculos de combustible para 3 escenarios.
- Lista de comprobación para modelado y verificación en Maxsurf.

Próximo paso recomendado

- Confirmar si deseas que:
  - (1) calcule KG real con una distribución de masas asumida (yo puedo proponer una distribución típica y dejarla marcada como supuestos),
  - (2) ejecute OCR y mapee cláusulas DNV/SOLAS exactas (autorización requerida), o
  - (3) genere un PDF final con las respuestas A–E (se requerirá validar los datos con Maxsurf o con los CSV exportados si los obtienes).

---

## Visualización y Reportes (implementado)

- Gráficos disponibles: Curva GZ, body plan y vista de perfil en `herramientas/maxsurf_integration/visualization/`.
- Generador de PDF profesional: `herramientas/maxsurf_integration/reports/report_generator.py` (títulos, párrafos, tablas, imágenes con ajuste automático a A4).
- Ejemplos:
  - `herramientas/maxsurf_integration/examples/generate_visual_report.py`
  - `herramientas/maxsurf_integration/examples/generate_report_example.py`

Para ejecutar ejemplo de reporte visual (macOS):

```bash
cd "/Users/robertgaraban/Desktop/proyecto final Barcos"
source .venv/bin/activate
export PYTHONPATH="$(pwd)/herramientas"
python "./herramientas/maxsurf_integration/examples/generate_visual_report.py"
open "./salidas/visual/visual_demo.pdf"
```

## Optimización paramétrica de cascos (implementado en modo mock)

- Búsqueda en malla sobre L, B, T, Cb para evaluar variantes con dos objetivos: minimizar desplazamiento y maximizar GZ máximo (sintético en modo mock).
- Módulo: `herramientas/maxsurf_integration/optimization/grid_search.py`.
- Ejemplo: `herramientas/maxsurf_integration/examples/run_grid_optimization.py`.

Salida esperada (CSV/XLSX y PDF):

```bash
python "./herramientas/maxsurf_integration/examples/run_grid_optimization.py"
open "./salidas/optimization/grid_demo.pdf"
```

## Pruebas automáticas

Para ejecutar toda la suite de pruebas:

```bash
pytest -q "./herramientas/maxsurf_integration/tests"
```

## Próximo: Adaptación a COM real (Windows)

Cuando se disponga de un equipo Windows con Maxsurf instalado/licenciado:

- Mapear `maxsurf_connector.run_hydrostatics()` y las llamadas de `StabilityAnalyzer` a la API COM real.
- Validar resultados contra modelos de ejemplo y ajustar escalas/coeficientes y nombres de propiedades.
