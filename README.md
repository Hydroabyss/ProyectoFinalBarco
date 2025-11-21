# Proyecto Final Buque 9 – Repositorio Integral

Este repositorio concentra **toda la documentación técnica, scripts y salidas** del Proyecto Final de Ingeniería Naval (Grupo 9). Incluye desde las memorias de cálculo y las entregas oficiales hasta los pipelines que automatizan la generación de planos, reportes y verificaciones frente a normas DNV/SOLAS.

## Visión general

| Bloque | Qué contiene |
| --- | --- |
| **Documentación principal** | `Proyecto-Final.md`, `PROYECTO_COMPLETADO.md`, `CAMBIOS_REALIZADOS.md`, `RESUMEN_INTEGRACION.py` y resúmenes ejecutivos asociados. |
| **Entregas** | `salidas/ENTREGA 3` y `salidas/ENTREGA 3 v4` (disposición general) + `ENTREGA 4` (cuaderna maestra, reporte final). |
| **Scripts & automatización** | `herramientas/` con los analizadores DXF/CSV, integración Maxsurf, generación de reportes, validaciones DNV, exportadores AutoCAD, etc. |
| **Datos y normativa** | `tablas_datos/`, `normativa/`, `recursos/` y archivos externos (PDF, DXF, imágenes de referencia). |
| **Proyectos auxiliares** | `Calculo-de-Estructuras-Navales-FNB/` (notebooks de cálculo estructural) y `libredwg/` (librería completa usada para manipular DWG/DXF sin AutoCAD). |

> **Nota:** El repositorio contiene múltiples archivos pesados (DXF, PDF, HTML interactivos). Si necesitas clonar en equipos con espacio limitado considera usar `git clone --filter=blob:none` y descargar solo lo imprescindible.

---

## Organización de carpetas destacada

```
.
├── Calculo-de-Estructuras-Navales-FNB/   # Notebooks y scripts de cálculo estructural (versión completa, no submódulo)
├── config/                               # Plantillas Pandoc, configuraciones CLI y estilos
├── ENTREGA 4/                            # Última entrega (cuaderna maestra, dashboards, DOCX/PDF)
├── herramientas/                         # Scripts Python para análisis, reportes, DXF, maxsurf_integration...
│   └── maxsurf_integration/              # CLI modular para generar bases de datos, tanques, reportes y bundles
├── libredwg/                             # Copia local del proyecto LibreDWG para exportar/validar DWG sin AutoCAD
├── normativa/                            # Reglamentos DNV, SOLAS y anexos normativos en PDF
├── recursos/, tablas_datos/, trabajos/   # Imágenes, tablas auxiliares y documentación académica original
├── salidas/                              # Resultados públicos: DXF, PDF, CSV, dashboards interactivos
│   ├── ENTREGA 3/ y ENTREGA 3 v4/        # Revisión de disposición general (versiones intermedias/finales)
│   ├── disposicion_general/              # Cálculos intermedios, debug y archivos “working”
│   ├── autocad*/, base_ship/, dnv/, ...  # Otras ejecuciones (planos base, paquetes DNV, optimizaciones)
└── scripts/, config/, documentos auxiliares
```

---

## Flujo recomendado de trabajo

1. **Revisión documental:** inicia con `Proyecto-Final.md` y `PROYECTO_COMPLETADO.md` para entender el estado del buque y las hipótesis vigentes. `CAMBIOS_REALIZADOS.md` sirve como bitácora rápida.
2. **Datos de referencia:** las tablas consolidadas (`tablas_datos/tabla_centralizada_datos.md`, CSV de tanques, coeficientes, etc.) alimentan los scripts.
3. **Automatización / Scripts Python:** dentro de `herramientas/` encontrarás desde utilidades simples (`extract_and_summarize.py`) hasta workflows complejos como:

   ```bash
   # Ejecutar pipeline completo de análisis de cuaderna (usa DXF, norma DNV y genera reportes)
   python3 herramientas/analizar_cuaderna_completo.py

   # Generar base de datos mock desde Maxsurf (define casco, espacios y tanques)
   cd herramientas/maxsurf_integration
   python3 -m maxsurf_integration auto-base \
     --loa 97.7 --beam 14.3 --depth 6.7 --draft 5.8
   ```

4. **Validaciones normativas:** `herramientas/verificador_dnv_cuaderna.py`, `herramientas/maxsurf_integration/dnv_verification/*` y los reportes en `salidas/dnv/` documentan los checks contra DNV Pt.3 Ch.5, SOLAS II-1 y criterios de estabilidad.
5. **Generación de planos / visualizaciones:** 
   - DXF oficiales en `salidas/autocad/`, `salidas/disposicion_general/`, `ENTREGA 4/graficos_interactivos/`.
   - Para renderizar nuevos DXF sin AutoCAD puedes utilizar LibreDWG (`libredwg/`) o los scripts `herramientas/generar_*`.

---

## Entregas y reportes

| Entrega | Ubicación | Contenido clave |
| --- | --- | --- |
| **ENTREGA 3** (versión original y v4) | `salidas/ENTREGA 3*/` | Disposición general, cubicación de tanques/bodegas, tablas CSV, guía de criterios A‑E. |
| **ENTREGA 4** | `ENTREGA 4/` | Reporte final de cuaderna maestra (DOCX, MD, PDF), dashboards HTML, planillas de verificación DNV, logs de análisis. |
| **Resumen ejecutivo** | `ENTREGA 4/RESUMEN_EJECUTIVO.md` | Estado global, porcentajes de cumplimiento y pendientes. |
| **Integración Maxsurf** | `ENTREGA 4/INTEGRACION_MAXSURF.md` y `herramientas/maxsurf_integration/RESUMEN_COMPLETADO.md` | Pasos para reproducir la cubicación y comunicación COM/Mock con Maxsurf. |

Cada entrega incluye la evidencia gráfica (PNG, DXF, PDF) y las tablas base (CSV/Excel) para auditoría. Los dashboards interactivos (`ENTREGA 4/graficos_interactivos/*.html`) permiten explorar capas, presiones y esfuerzos de la cuaderna maestra.

---

## Dependencias y requisitos

- **Python 3.9+** con librerías estándar (`pandas`, `numpy`, `matplotlib`, etc.). El archivo `herramientas/maxsurf_integration/requirements.txt` sirve como base.
- **LibreDWG / DWG soportado:** vendorizado en `libredwg/` para generar o validar DWG sin instalar AutoCAD.
- **Maxsurf (opcional):** si se desea conectividad real, establecer `MAXSURF_MOCK=false` y contar con el COM disponible. En modo mock los datos se generan a partir de los CSV suministrados.
- **Herramientas externas:** Pandoc para convertir Markdown ↔ DOCX/HTML (`config/pandoc_entrega4.css`), AutoCAD/LibreCAD si necesitas abrir DXF nativamente.

**Inicialización rápida del entorno Python:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r herramientas/maxsurf_integration/requirements.txt
```

---

## Mantenimiento y buenas prácticas

- **Cambios voluminosos:** antes de subir nuevas ejecuciones revisa si los DXF/HTML ya existen; renómbralos con sufijos de versión (`_v5`, fecha ISO) para no sobrescribir evidencia previa.
- **Archivos grandes:** notebooks y DXF superan los 5‑20 MB. Considera Git LFS cuando corresponda o elimina archivos temporales en `salidas/disposicion_general/*debug*` si no se necesitan.
- **Bitácora:** utiliza `CAMBIOS_REALIZADOS.md` para anotar correcciones relevantes (p.ej. ajuste de espesores, nuevas curvas GZ).
- **Normativa:** la carpeta `normativa/` contiene las referencias oficiales. Cada script/report se enlaza a la sección DNV/SOLAS correspondiente para facilitar auditorías.

---

## Estado actual

- ✅ Entregas 3 y 4 consolidadas con soportes gráficos.
- ✅ Pipelines Python reproducibles (sin dependencias externas ocultas).
- ✅ Integraciones (Maxsurf mock, LibreDWG) incluidas en el repositorio.
- 🔄 Pendiente: limpieza/optimización del peso del repo y eventual migración de binarios a LFS si la colaboración se vuelve masiva.

> Para consultas o ajustes específicos (nuevas verificaciones, generación de reportes adicionales, refuerzo del README, etc.) abre un issue o documenta los cambios en `CAMBIOS_REALIZADOS.md`.

---

**Última actualización:** noviembre 2025 · **Responsables:** Equipo Proyecto Final – Ingeniería en Sistemas / Diseño Naval (Grupo 9)  
**Contacto interno:** verificar en los documentos `RESUMEN_TECNICO_FINAL` o en los metadatos de Maxsurf.
