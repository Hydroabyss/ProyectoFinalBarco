# GUÍA DE USO - Sistema de Análisis de Cuadernas

## 🚀 Inicio Rápido

### Análisis Completo (Recomendado)

Para ejecutar el análisis completo de la cuaderna maestra en un solo comando:

```bash
python3 herramientas/analizar_cuaderna_completo.py
```

Este comando ejecuta automáticamente:
1. ✅ Análisis del plano DXF
2. ✅ Verificación normativa DNV
3. ✅ Generación de reportes y gráficos
4. ✅ Creación de resumen ejecutivo

**Tiempo estimado:** ~2-3 segundos

**Resultados:** Todos los archivos se guardan en `ENTREGA 4/`

---

## 📋 Análisis Individual

Si prefieres ejecutar cada análisis por separado:

### 1. Análisis del Plano DXF

```bash
python3 herramientas/analizador_plano_cuaderna.py
```

**Qué hace:**
- Lee el archivo DXF de la cuaderna maestra
- Identifica capas y entidades
- Extrae dimensiones principales
- Detecta errores y advertencias

**Salida:**
- `ENTREGA 4/analisis_plano_cuaderna.json`
- Resumen en consola

### 2. Verificación Normativa DNV

```bash
python3 herramientas/verificador_dnv_cuaderna.py
```

**Qué hace:**
- Verifica mamparos estancos
- Verifica doble fondo y doble costado
- Verifica refuerzos transversales
- Verifica espesores de planchas
- Verifica módulo resistente
- Verifica cargas aplicadas

**Salida:**
- `ENTREGA 4/verificacion_dnv_cuaderna.json`
- Resumen en consola

### 3. Generación de Reportes

```bash
python3 herramientas/generador_reporte_cuaderna.py
```

**Qué hace:**
- Genera reporte completo en Markdown
- Crea gráficos (PNG)
- Genera tablas (Excel)
- Integra todos los análisis

**Salida:**
- `ENTREGA 4/REPORTE_CUADERNA_MAESTRA.md`
- `ENTREGA 4/graficos/*.png`
- `ENTREGA 4/tablas/*.xlsx`

---

## 📁 Estructura de Salida

Después de ejecutar el análisis, encontrarás:

```
ENTREGA 4/
├── RESUMEN_EJECUTIVO.md              # ⭐ Empieza aquí
├── REPORTE_CUADERNA_MAESTRA.md       # Reporte completo
├── INTEGRACION_MAXSURF.md            # Guía de Maxsurf
├── README.md                         # Documentación general
│
├── analisis_plano_cuaderna.json      # Datos del análisis
├── verificacion_dnv_cuaderna.json    # Datos de verificación
├── analisis_log.json                 # Log de ejecución
│
├── graficos/
│   ├── analisis_capas.png
│   ├── cumplimiento_dnv.png
│   └── geometria_cuaderna.png
│
└── tablas/
    ├── analisis_capas.xlsx
    └── verificaciones_dnv.xlsx
```

---

## 📖 Cómo Leer los Resultados

### 1. Resumen Ejecutivo (Empieza aquí)

**Archivo:** `RESUMEN_EJECUTIVO.md`

**Contenido:**
- ✅ Estado general (APROBADO / REQUIERE CORRECCIONES)
- 📊 Resultados principales
- 📐 Dimensiones principales
- ⚠️ Acciones requeridas
- 📝 Próximos pasos

**Tiempo de lectura:** 2-3 minutos

### 2. Reporte Completo

**Archivo:** `REPORTE_CUADERNA_MAESTRA.md`

**Contenido:**
- Análisis detallado del plano
- Verificaciones normativas completas
- Gráficos y tablas
- Conclusiones y recomendaciones

**Tiempo de lectura:** 10-15 minutos

### 3. Gráficos

**Carpeta:** `graficos/`

**Archivos:**
- `analisis_capas.png`: Distribución de entidades por capa
- `cumplimiento_dnv.png`: Estado de verificaciones normativas
- `geometria_cuaderna.png`: Dimensiones principales

### 4. Tablas Excel

**Carpeta:** `tablas/`

**Archivos:**
- `analisis_capas.xlsx`: Detalle de capas y entidades
- `verificaciones_dnv.xlsx`: Detalle de verificaciones normativas

---

## 🔧 Configuración

### Requisitos del Sistema

- **Python:** 3.8 o superior
- **Sistema operativo:** Windows, macOS, Linux
- **Memoria RAM:** 2 GB mínimo
- **Espacio en disco:** 100 MB

### Instalación de Dependencias

```bash
pip install ezdxf matplotlib openpyxl pandas
```

**Dependencias:**
- `ezdxf`: Lectura de archivos DXF
- `matplotlib`: Generación de gráficos
- `openpyxl`: Generación de archivos Excel
- `pandas`: Manipulación de datos

### Verificar Instalación

```bash
python3 -c "import ezdxf, matplotlib, openpyxl, pandas; print('✓ Todas las dependencias instaladas')"
```

---

## 🎯 Casos de Uso

### Caso 1: Primera Vez

**Objetivo:** Analizar la cuaderna maestra por primera vez

**Pasos:**
1. Instalar dependencias (ver arriba)
2. Ejecutar análisis completo:
   ```bash
   python3 herramientas/analizar_cuaderna_completo.py
   ```
3. Leer `RESUMEN_EJECUTIVO.md`
4. Revisar gráficos en `graficos/`
5. Leer `REPORTE_CUADERNA_MAESTRA.md` para detalles

### Caso 2: Después de Correcciones

**Objetivo:** Re-analizar después de corregir errores

**Pasos:**
1. Actualizar el archivo DXF con las correcciones
2. Ejecutar análisis completo:
   ```bash
   python3 herramientas/analizar_cuaderna_completo.py
   ```
3. Comparar resultados con análisis anterior
4. Verificar que los errores se corrigieron

### Caso 3: Análisis Parcial

**Objetivo:** Solo verificar cumplimiento DNV

**Pasos:**
1. Ejecutar solo el verificador:
   ```bash
   python3 herramientas/verificador_dnv_cuaderna.py
   ```
2. Revisar `verificacion_dnv_cuaderna.json`

### Caso 4: Generar Solo Reportes

**Objetivo:** Regenerar reportes sin re-analizar

**Pasos:**
1. Asegurarse de que existen los archivos JSON
2. Ejecutar generador de reportes:
   ```bash
   python3 herramientas/generador_reporte_cuaderna.py
   ```

---

## 🐛 Solución de Problemas

### Error: "No module named 'ezdxf'"

**Causa:** Falta instalar dependencias

**Solución:**
```bash
pip install ezdxf matplotlib openpyxl pandas
```

### Error: "FileNotFoundError: Corte_Transversal_Cuaderna_Maestra_Detallado - V2.dxf"

**Causa:** El archivo DXF no está en la ubicación esperada

**Solución:**
1. Verificar que el archivo existe en la carpeta raíz del proyecto
2. O modificar la ruta en el script:
   ```python
   archivo_dxf = "ruta/al/archivo.dxf"
   ```

### Error: "Permission denied" al guardar archivos

**Causa:** No hay permisos de escritura en la carpeta

**Solución:**
```bash
chmod -R 755 "ENTREGA 4"
```

### Los gráficos no se generan

**Causa:** Problema con matplotlib backend

**Solución:**
```bash
export MPLBACKEND=Agg
python3 herramientas/generador_reporte_cuaderna.py
```

### Resultados incorrectos

**Causa:** Datos del buque desactualizados

**Solución:**
1. Verificar datos en `herramientas/verificador_dnv_cuaderna.py`
2. Actualizar dimensiones principales:
   ```python
   datos_buque = {
       'eslora': 97.7,
       'manga': 14.3,
       'puntal': 6.7,
       'calado': 5.8
   }
   ```

---

## 📊 Interpretación de Resultados

### Estado General

| Estado | Significado | Acción |
|--------|-------------|--------|
| ✅ APROBADO | Cumple todos los requisitos | Continuar con siguiente fase |
| ⚠️ APROBADO CON OBSERVACIONES | Cumple >80% requisitos | Corregir observaciones menores |
| ❌ REQUIERE CORRECCIONES | Cumple <80% requisitos | Rediseñar elementos críticos |

### Cumplimiento DNV

| Porcentaje | Interpretación |
|------------|----------------|
| 100% | Excelente - Cumple todos los requisitos |
| 85-99% | Bueno - Requiere correcciones menores |
| 70-84% | Regular - Requiere correcciones importantes |
| <70% | Insuficiente - Requiere rediseño |

### Verificaciones Individuales

| Verificación | Crítica | Descripción |
|--------------|---------|-------------|
| Mamparos | ⚠️ Alta | Seguridad de compartimentación |
| Doble Fondo | ⚠️ Alta | Protección contra varada |
| Doble Costado | ⚠️ Alta | Protección contra colisión |
| Refuerzos | ⚠️ Media | Resistencia estructural |
| Espesores | ⚠️ Alta | Resistencia a cargas |
| Módulo Resistente | ⚠️ Alta | Resistencia a flexión |
| Cargas | ⚠️ Media | Capacidad de carga |

---

## 🔄 Workflow Recomendado

### Fase 1: Análisis Inicial
1. Ejecutar análisis completo
2. Leer resumen ejecutivo
3. Identificar problemas críticos

### Fase 2: Correcciones
1. Corregir errores identificados
2. Actualizar plano DXF
3. Re-ejecutar análisis

### Fase 3: Validación
1. Verificar que todos los errores se corrigieron
2. Revisar cumplimiento DNV (debe ser >95%)
3. Generar reportes finales

### Fase 4: Integración Maxsurf
1. Exportar datos a Maxsurf
2. Ejecutar análisis FEA
3. Validar resultados

### Fase 5: Documentación
1. Compilar todos los reportes
2. Añadir conclusiones
3. Preparar presentación

---

## 📞 Soporte

### Documentación Adicional

- `README.md`: Documentación general del proyecto
- `INTEGRACION_MAXSURF.md`: Guía de integración con Maxsurf
- `REPORTE_CUADERNA_MAESTRA.md`: Reporte completo

### Referencias Normativas

- **DNV-RU-SHIP Part 3:** Structural Design
- **SOLAS Chapter II-1:** Construction - Structure

### Archivos de Ejemplo

- `analisis_plano_cuaderna.json`: Ejemplo de salida del analizador
- `verificacion_dnv_cuaderna.json`: Ejemplo de salida del verificador

---

## 🎓 Glosario

| Término | Definición |
|---------|------------|
| **Cuaderna maestra** | Sección transversal del buque en su punto más ancho |
| **DNV** | Det Norske Veritas - Sociedad de clasificación |
| **DXF** | Drawing Exchange Format - Formato de archivo CAD |
| **Mamparo estanco** | Pared que divide compartimentos del buque |
| **Doble fondo** | Espacio entre el fondo exterior e interior |
| **Doble costado** | Espacio entre el costado exterior e interior |
| **Módulo resistente** | Propiedad geométrica que mide resistencia a flexión |
| **Escantillón** | Dimensiones de elementos estructurales |

---

## ✅ Checklist de Verificación

Antes de considerar el análisis completo, verifica:

- [ ] Análisis del plano ejecutado sin errores
- [ ] Verificación DNV ejecutada sin errores
- [ ] Reportes generados correctamente
- [ ] Gráficos creados (3 archivos PNG)
- [ ] Tablas creadas (2 archivos Excel)
- [ ] Resumen ejecutivo revisado
- [ ] Errores críticos identificados
- [ ] Plan de correcciones definido
- [ ] Cumplimiento DNV >85%
- [ ] Documentación completa

---

**Última actualización:** 11 de noviembre de 2025
**Versión:** 1.0
