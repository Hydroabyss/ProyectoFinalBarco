# Integración Maxsurf con Python 🚢

Sistema completo de automatización para Maxsurf usando Python y la API COM de Windows.

## 📋 Características

- ✅ **Conexión automática** con Maxsurf mediante COM
- 🚢 **Diseño de cascos** paramétrico, incluido flujo “buque base”
- ⚓ **Análisis de estabilidad** con verificación SOLAS
- ⛽ **Diseño de tanques** con cubicación automática
- 📊 **Generación de reportes** en Markdown y JSON
- 🔧 **Configuración VS Code** completa con snippets

## 🛠️ Requisitos

### Software Necesario

- **Maxsurf** (Bentley Systems) - Instalado y licenciado
- **Python 3.8+**
- **Windows** (requerido para API COM)
- **VS Code** (recomendado)

### Dependencias Python

```bash
pip install -r requirements.txt
```

Incluye:

- `pywin32` - API COM de Windows
- `pandas` - Análisis de datos
- `numpy` - Cálculos numéricos
- `matplotlib` - Gráficos
- `reportlab` - Generación de PDFs

## 📁 Estructura

```
maxsurf_integration/
├── __init__.py                    # Paquete principal
├── maxsurf_connector.py           # Conexión con Maxsurf
├── demo_completo.py               # Demo de todas las capacidades
├── requirements.txt               # Dependencias
│
├── hull_design/                   # Diseño de cascos
│   ├── __init__.py
│   └── hull_designer.py
│
├── stability/                     # Análisis de estabilidad
│   ├── __init__.py
│   └── stability_analyzer.py
│
├── tanks/                         # Diseño de tanques
│   ├── __init__.py
│   └── tank_designer.py
│
└── reports/                       # Generación de reportes
    ├── __init__.py
    └── report_generator.py
```

## 🚀 Inicio Rápido

### 1. Instalar Dependencias

```bash
cd herramientas/maxsurf_integration
pip install -r requirements.txt
```

### 2. Ejecutar Demo Completa

```python
python demo_completo.py
```

Esto ejecutará:

1. Conexión con Maxsurf
2. Creación del casco del Buque 9
3. Análisis de estabilidad completo
4. Diseño de tanques
5. Generación de reportes

### 3. Usar en tus Scripts

```python
from herramientas.maxsurf_integration import MaxsurfConnector, HullDesigner

# Conectar con Maxsurf
with MaxsurfConnector(visible=True) as maxsurf:
    if maxsurf.is_connected():
        # Crear diseñador de cascos
        designer = HullDesigner(maxsurf)

        # Crear casco del Buque 9
        designer.crear_casco_buque9()

        # Guardar parámetros
        designer.guardar_parametros("config/mi_buque.json")
```

## 📚 Ejemplos de Uso

### Diseño de Casco Paramétrico

```python
from maxsurf_integration import MaxsurfConnector, HullDesigner

with MaxsurfConnector(visible=True) as maxsurf:
    designer = HullDesigner(maxsurf)

    # Crear casco personalizado
    designer.crear_casco_parametrico(
        loa=120.0,      # Eslora total (m)
        beam=18.0,      # Manga (m)
        draft=7.0,      # Calado (m)
        cb=0.68,        # Coeficiente de bloque
        tipo="Granelero"
    )
```

## Visualización y reportes

- Gráficos disponibles: curvas GZ, plano de formas y perfil (`visualization/plots.py`).
- Generador de PDF: `reports/report_generator.py` (títulos, párrafos, tablas e imágenes con autoajuste).
- Ejemplos listos para usar:
  - `examples/generate_visual_report.py`
  - `examples/generate_report_example.py`

## Optimización paramétrica

- Búsqueda en malla sobre L, B, T y Cb (minimiza desplazamiento y maximiza un GZ sintético).
- Implementación principal: `optimization/grid_search.py`.
- Ejemplo: `examples/run_grid_optimization.py` (produce CSV/XLSX y un PDF comparativo).

## Cómo ejecutar los ejemplos

1. Activa el entorno virtual y exporta `PYTHONPATH` apuntando a `herramientas`.
2. Lanza el script o la CLI que necesites. Algunos ejemplos:

```
# CLI del paquete
python -m maxsurf_integration ping
python -m maxsurf_integration base-ship --loa 103.81 --beam 15.60 --draft 6.20 --depth 7.70
python -m maxsurf_integration visual-report --out ./salidas/visual --basename visual_demo
python -m maxsurf_integration grid-opt --L 95 100 --B 14 16 --T 5 6 --Cb 0.55 0.65 \
        --out ./salidas/optimization --basename cli_grid

# Ejemplos directos
python ./herramientas/maxsurf_integration/examples/generate_visual_report.py
python ./herramientas/maxsurf_integration/examples/run_grid_optimization.py
```

### Opciones de la CLI

- `visual-report`:
  - `--out`: directorio de salida (default: `./salidas/visual`)
  - `--basename`: nombre base del PDF (default: `visual_demo`)
- `grid-opt`:
  - `--L`, `--B`, `--T`, `--Cb`: listas de valores numéricos
  - `--out`: directorio de salida (default: `./salidas/optimization`)
  - `--basename`: prefijo de los archivos CSV/XLSX y PDF (default: `cli_grid`)
- `base-ship`:
  - `--loa`, `--beam`, `--depth`, `--draft`: dimensiones objetivo (m)
  - `--ratio-loa-lpp`: relación LOA/Lpp (default 0.97)
  - `--out`: directorio para JSON/CSV (default: `./salidas/base_ship`)
  - `--dxf-out`: directorio para DXF (default: `./salidas/autocad_base`)
  - `--skip-planos`: omite planos DXF (útil si no hay AutoCAD)
  - `--no-csv`: omite CSV resumen
- `auto-base`:
  - Ejecuta la automatización completa y crea la carpeta `planos e informacion base` (o la indicada con `--out`).
  - Reutiliza el flujo de Windows cuando hay COM disponible y cae a mock en macOS/Linux.
  - Útil para centralizar JSON/CSV, DXF y modelo `.msd` en un solo lugar.
- `windows-bundle`:
  - Ejecuta todo el flujo recomendado en Windows (JSON/CSV, DXF reales, `.msd`, git-lfs).
  - Acepta los mismos parámetros geométricos (`--loa`, `--beam`, `--depth`, `--draft`, `--ratio-loa-lpp`).
  - Directorios personalizables con `--out`, `--dxf-out`, `--msd-out` y `--archive`.
  - Usa `--skip-git-lfs` si no quieres registrar `*.msd` en git-lfs.

## 📦 Carpeta “planos e informacion base”

El comando `python -m maxsurf_integration auto-base` genera una estructura auto-contenida con:

- `datos/` → JSON y CSV del buque base.
- `planos/` → DXF del plano de construcción, líneas y cuadernas.
- `modelo/` → Modelo `.msd` (o placeholder en modo mock).
- `artefactos/` → Solo cuando se ejecuta con backend COM (incluye `bundle_summary.json`).
- `resumen_planos_informacion.json` → Manifest con metadatos y rutas.

En macOS/Linux el flujo usa el backend mock, pero mantiene la misma estructura para facilitar la sincronización con resultados reales generados en Windows.

## 🪟 Guía rápida — Windows con Maxsurf real (COM)

1. **Instalar requisitos**
   ```powershell
   cd herramientas\maxsurf_integration
   py -m pip install -r requirements.txt
   ```
2. **Verificar pywin32**: tras instalar, ejecuta `py -c "import win32com"` para asegurar que la API COM está disponible.
3. **Ejecutar el comando único**:
   ```powershell
   py -m maxsurf_integration auto-base --loa 103.81 --beam 15.60 --depth 7.70 --draft 6.20
   ```
   El comando intenta usar el backend COM (vía `windows-bundle`) y deja todo organizado en `planos e informacion base/`.
4. **Revisar artefactos**:

- `planos e informacion base\resumen_planos_informacion.json` — resumen principal.
- `planos e informacion base\datos` — JSON/CSV listos para versionar.
- `planos e informacion base\planos` — DXF generados con Maxsurf real.
- `planos e informacion base\modelo` — modelo `.msd` para iterar en Maxsurf.
- (Opcional) `planos e informacion base\artefactos` — copia detallada del bundle original.

5. **Abrir en Maxsurf** (opcional): si deseas continuar la edición, abre el `.msd` en Maxsurf Modeler y guarda versiones adicionales si lo consideras necesario.

> 💡 En Windows el backend COM proporciona coeficientes y geometría reales de Maxsurf. Los campos `backend` en el JSON mostrarán `"com"` confirmando la lectura directa.

## 🍎 Notas y limitaciones en macOS/Linux

- Maxsurf no expone API COM en macOS/Linux; el conector usa un **backend mock** para cálculos rápidos.
- Los comandos `base-ship` y `grid-opt` siguen funcionando y generan DXF mediante `ezdxf`, pero los resultados hidrostáticos son aproximados.
- Para obtener datos reales:
  - Ejecuta los mismos comandos en una máquina Windows con Maxsurf.
  - Copia los directorios `salidas/base_ship` y `salidas/autocad_base` de Windows de vuelta al proyecto macOS.
- El mock documenta en `notas[]` del JSON cómo replicar el flujo en Windows.

## Pruebas

- Ejecutar todos los tests:

```
pytest -q ./herramientas/maxsurf_integration/tests
```

## 🖊️ Integración AutoCAD (DXF offline/COM)

- macOS/Linux: generación DXF offline con `ezdxf` (no requiere AutoCAD).
- Windows: si AutoCAD está disponible, la conexión COM puede activarse (pendiente de mapeo completo).

### CLI

```
# Generar plano de construcción
python -m maxsurf_integration autocad construction --L 12 --B 3.8 --T 1.8 --out ./salidas/autocad

# Generar plano de líneas
python -m maxsurf_integration autocad lines --L 12 --B 3.8 --T 1.8 --out ./salidas/autocad

# Generar plano de cuadernas (rejilla)
python -m maxsurf_integration autocad frames --L 12 --B 3.8 --T 1.8 --out ./salidas/autocad

# Generar todos
python -m maxsurf_integration autocad all --L 12 --B 3.8 --T 1.8 --out ./salidas/autocad
```

### Tareas VS Code

- Run: AutoCAD (DXF offline demo)
- Run: AutoCAD (Plano de Líneas)
- Run: AutoCAD (Cuadernas)
- Run: AutoCAD (Todos)

### Notas

- En macOS verás logs informativos de fuentes de `ezdxf`; son inofensivos.
- En Windows, si `win32com` está disponible y AutoCAD está instalado, `conectar_autocad()` abrirá AutoCAD.

### Análisis de Estabilidad

```python
from maxsurf_integration import MaxsurfConnector, StabilityAnalyzer

with MaxsurfConnector(visible=True) as maxsurf:
    analyzer = StabilityAnalyzer(maxsurf)

    # Análisis completo
    resultados = analyzer.analisis_completo_buque9()

    # Verificar cumplimiento SOLAS
    if resultados['cumplimiento_solas']['cumple_solas']:
        print("✅ Cumple normativa SOLAS")

    # Generar reporte
    reporte = analyzer.generar_reporte_estabilidad()
    print(reporte)
```

### Diseño de Tanques

```python
from maxsurf_integration import MaxsurfConnector, TankDesigner

with MaxsurfConnector(visible=True) as maxsurf:
    designer = TankDesigner(maxsurf)

    # Calcular combustible necesario
    req = designer.calcular_volumen_combustible(
        autonomia_nm=10000,
        velocidad_kn=14,
        consumo_diario_ton=5.0
    )

    # Diseñar tanques del Buque 9
    tanques = designer.diseñar_tanques_buque9(
        escenario_consumo='realista'  # 'economico', 'realista', 'pesado'
    )

    # Exportar diseño
    designer.exportar_tanques("tanques.csv", formato='csv')
```

## 🔧 Configuración VS Code

El proyecto incluye configuración completa para VS Code:

### Tareas Disponibles

- `Test: Conectar con Maxsurf`
- `Crear Casco Buque 9`
- `Análisis de Estabilidad Buque 9`
- `Diseñar Tanques Buque 9`
- `Instalar Dependencias Maxsurf`

**Usar:** `Cmd+Shift+P` → `Tasks: Run Task`

### Configuraciones de Debug

- Python: Maxsurf Connector
- Python: Hull Designer
- Python: Stability Analyzer
- Python: Tank Designer
- Python: Current File

**Usar:** `F5` para iniciar debug

### Snippets Personalizados

- `maxconnect` - Conexión con Maxsurf
- `hullsetup` - Configurar diseñador de cascos
- `stabanalysis` - Análisis de estabilidad
- `tankdesign` - Diseño de tanques
- `buque9` - Parámetros del Buque 9
- `hydro` - Cálculos hidrostáticos
- `gzcurve` - Curva GZ

**Usar:** Escribir el prefijo y presionar `Tab`

## 📊 Datos del Buque 9

```python
BUQUE9 = {
    'LOA': 97.7,          # Eslora total (m)
    'Lpp': 96.2,          # Eslora entre perpendiculares (m)
    'beam': 14.3,         # Manga (m)
    'draft': 5.8,         # Calado de proyecto (m)
    'depth': 6.7,         # Puntal (m)
    'DWT': 3848,          # Peso muerto (t)
    'Cb': 0.703,          # Coeficiente de bloque
    'Cp': 0.721,          # Coeficiente prismático
    'velocidad': 14,      # Velocidad (kn)
    'autonomia': 10000,   # Autonomía (nm)
    'tipo': 'Granelero'
}
```

## 📈 Resultados Generados

El sistema genera automáticamente:

### Archivos de Configuración (config/)

- `buque9_params.json` - Parámetros del casco
- `tanques_buque9.json` - Diseño de tanques

### Datos Tabulados (tablas_datos/)

- `estabilidad_buque9.json` - Resultados de estabilidad
- `tanques_buque9.csv` - Lista de tanques con volúmenes

### Modelos Maxsurf

- `buque9_modelo.msd` - Modelo completo de Maxsurf

## ⚠️ Notas Importantes

### Limitaciones de la API

Los comandos exactos de Maxsurf pueden variar según la versión. Los scripts actuales usan comandos genéricos que deben adaptarse a la API específica de tu instalación.

### Obtener Datos de Maxsurf

Para obtener resultados reales (GM, GZ, volúmenes), es necesario:

1. Consultar la documentación de la API de Maxsurf
2. Usar los métodos específicos del objeto COM
3. Adaptar las funciones placeholder en el código

### Recursos Adicionales

- **Bentley Developer Network:** https://developer.bentley.com/
- **Documentación Maxsurf:** Help → Developer Help (dentro de Maxsurf)
- **Comunidad Bentley:** Forums y soporte técnico

## 🐛 Solución de Problemas

### Error: "No se puede conectar con Maxsurf"

✅ Verificar que Maxsurf esté instalado  
✅ Verificar que pywin32 esté instalado: `pip install pywin32`  
✅ Ejecutar el script desde Windows (no WSL)

### Error: "ImportError: No module named 'win32com'"

```bash
pip install pywin32
python -m pywin32_postinstall -install
```

### Error: "Comando no reconocido"

Los comandos de Maxsurf pueden variar. Consultar:

1. Documentación de tu versión de Maxsurf
2. Help → Developer Help
3. Bentley Developer Network

## 📞 Soporte

Para problemas específicos de la API de Maxsurf:

- **Soporte Bentley:** https://communities.bentley.com/
- **Documentación:** Dentro de Maxsurf (Help → Developer Help)

## 📝 Licencia

Este código es parte del Proyecto Final - Diseño Naval.  
Fecha: 2 de noviembre de 2025

---

**¡Listo para automatizar tu diseño naval! 🚀⚓**
