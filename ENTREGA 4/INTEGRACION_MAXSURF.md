# INTEGRACIÓN MAXSURF PARA ANÁLISIS DE CUADERNAS

## Objetivo

Documentar cómo utilizar Maxsurf para obtener datos estructurales de la cuaderna maestra del Buque Grupo 9.

## Módulos de Maxsurf Relevantes

### 1. Maxsurf Modeler
**Propósito:** Modelado 3D del casco

**Datos que proporciona para cuadernas:**
- Geometría de la sección transversal en cualquier estación
- Coordenadas de puntos del casco (offsets)
- Área de la sección transversal
- Perímetro mojado
- Centro de área de la sección

**Cómo obtener datos:**
```
1. Abrir el modelo del buque en Maxsurf Modeler
2. Ir a: Analysis → Sections → Section Properties
3. Seleccionar la estación de la cuaderna maestra (aprox. estación 15)
4. Exportar datos a CSV o copiar valores
```

### 2. Maxsurf Stability
**Propósito:** Análisis de estabilidad y flotabilidad

**Datos que proporciona para cuadernas:**
- Presiones hidrostáticas en la sección
- Momentos de inercia transversales
- Centro de flotación
- Metacentro transversal (BM)
- Curvas de estabilidad

**Cómo obtener datos:**
```
1. Abrir el modelo en Maxsurf Stability
2. Definir condición de carga
3. Ir a: Analysis → Hydrostatics
4. Seleccionar la estación de interés
5. Obtener presiones y momentos
```

### 3. Maxsurf Structure (si disponible)
**Propósito:** Análisis estructural FEA

**Datos que proporciona:**
- Esfuerzos en elementos estructurales
- Deformaciones
- Momentos flectores transversales
- Esfuerzos cortantes
- Análisis de fatiga

**Cómo obtener datos:**
```
1. Importar geometría desde Modeler
2. Definir propiedades de materiales
3. Aplicar cargas (hidrostáticas, cubierta, etc.)
4. Ejecutar análisis FEA
5. Exportar resultados
```

## Datos Necesarios para Análisis de Cuaderna

### Geometría de la Sección
- **Coordenadas de puntos del casco** (Y, Z)
- **Área de la sección transversal** (m²)
- **Perímetro mojado** (m)
- **Centro de área** (Y, Z)

### Propiedades Hidrostáticas
- **Calado en la sección** (m)
- **Manga en la línea de flotación** (m)
- **Área sumergida** (m²)
- **Centro de flotación** (LCF)
- **Momento de inercia transversal** (I_T)

### Cargas y Presiones
- **Presión hidrostática** (kPa)
  - Fórmula: p = ρ × g × h
  - ρ = 1.025 t/m³ (agua de mar)
  - g = 9.81 m/s²
  - h = profundidad desde la línea de flotación

- **Cargas de cubierta** (kN/m²)
  - Carga general: 10 kN/m²
  - Contenedores: 15 kN/m²
  - Equipos: según especificación

### Esfuerzos Estructurales
- **Momento flector transversal** (kN·m)
- **Esfuerzo cortante transversal** (kN)
- **Tensiones en elementos** (MPa)
- **Deformaciones** (mm)

## Integración con Python

### Script de Ejemplo: Obtener Datos de Maxsurf

```python
#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "maxsurf_integration"))

from maxsurf_connector import MaxsurfConnector

def obtener_datos_cuaderna(estacion: int = 15):
    """
    Obtiene datos de la cuaderna maestra desde Maxsurf.
    
    Args:
        estacion: Número de estación (0 = popa, 20 = proa)
    
    Returns:
        Dict con datos de la cuaderna
    """
    
    connector = MaxsurfConnector()
    
    # Verificar conexión
    if not connector.ping():
        print("⚠ Maxsurf no disponible - usando datos mock")
        return obtener_datos_mock(estacion)
    
    # Obtener datos hidrostáticos
    hydro_data = connector.get_hydrostatics()
    
    # Obtener geometría de la sección
    section_data = connector.get_section_properties(estacion)
    
    # Calcular presiones
    calado = hydro_data.get('draft_m', 6.20)
    presion_hidrostatica = 1.025 * 9.81 * calado / 1000  # kPa
    
    return {
        'estacion': estacion,
        'geometria': section_data,
        'hidrostática': hydro_data,
        'presiones': {
            'hidrostatica_kPa': presion_hidrostatica,
            'cubierta_kPa': 10.0,
            'total_kPa': presion_hidrostatica + 10.0
        }
    }

def obtener_datos_mock(estacion: int) -> dict:
    """Datos mock para desarrollo sin Maxsurf."""
    return {
        'estacion': estacion,
        'geometria': {
            'area_m2': 85.5,
            'perimetro_m': 38.2,
            'centro_y_m': 0.0,
            'centro_z_m': 3.95
        },
        'hidrostatica': {
            'calado_m': 6.20,
            'manga_flotacion_m': 15.99,
            'area_sumergida_m2': 75.3,
            'lcf_m': 52.6,
            'momento_inercia_m4': 1250.0
        },
        'presiones': {
            'hidrostatica_kPa': 62.3,
            'cubierta_kPa': 10.0,
            'total_kPa': 72.3
        }
    }

if __name__ == '__main__':
    datos = obtener_datos_cuaderna(15)
    
    print("=" * 80)
    print("DATOS DE CUADERNA MAESTRA DESDE MAXSURF")
    print("=" * 80)
    print(f"Estación: {datos['estacion']}")
    print()
    
    print("GEOMETRÍA:")
    for clave, valor in datos['geometria'].items():
        print(f"  {clave}: {valor}")
    print()
    
    print("HIDROSTÁTICA:")
    for clave, valor in datos['hidrostatica'].items():
        print(f"  {clave}: {valor}")
    print()
    
    print("PRESIONES:")
    for clave, valor in datos['presiones'].items():
        print(f"  {clave}: {valor}")
```

## Workflow Completo

### 1. Preparación en Maxsurf
```
1. Abrir modelo del Buque Grupo 9 en Maxsurf Modeler
2. Verificar que la cuaderna maestra está en la estación correcta
3. Exportar geometría del casco (File → Export → DXF)
4. Guardar datos hidrostáticos (Analysis → Export Data)
```

### 2. Análisis en Python
```bash
# Ejecutar análisis completo
python3 herramientas/analizador_plano_cuaderna.py
python3 herramientas/verificador_dnv_cuaderna.py
python3 herramientas/maxsurf_cuaderna_analyzer.py  # Nuevo script
python3 herramientas/generador_reporte_cuaderna.py
```

### 3. Verificación de Resultados
```
1. Revisar REPORTE_CUADERNA_MAESTRA.md
2. Verificar gráficos en graficos/
3. Revisar tablas en tablas/
4. Comparar con datos de Maxsurf
```

## Datos del Buque Grupo 9

### Ubicación de la Cuaderna Maestra
- **Posición longitudinal:** 52.6 m desde popa (mitad de eslora)
- **Estación aproximada:** 15 (de 20 estaciones)
- **Compartimento:** Bodega 2
- **Coordenadas:** X = 52.6 m, Y = 0 (plano diametral)

### Dimensiones en la Cuaderna Maestra
- **Manga en cubierta:** 15.99 m
- **Manga en flotación:** ~15.5 m (estimado)
- **Puntal:** 7.90 m
- **Calado:** 6.20 m
- **Doble fondo:** 1.20 m
- **Doble costado:** 1.80 m

### Cargas Aplicables
- **Presión hidrostática:** 62.3 kPa (a 6.20 m de calado)
- **Carga de cubierta:** 10 kN/m² (carga general)
- **Peso de estructura:** Según material AH36

## Limitaciones Actuales

### Sin Maxsurf Instalado
- Se utilizan datos mock para desarrollo
- Los valores son estimaciones basadas en dimensiones principales
- No se pueden obtener datos reales de presiones y esfuerzos

### Con Maxsurf Instalado
- Requiere licencia válida
- Necesita modelo 3D del buque cargado
- Puede requerir configuración de API/COM

## Próximos Pasos

1. **Implementar script `maxsurf_cuaderna_analyzer.py`**
   - Conectar con Maxsurf API
   - Obtener datos de la sección
   - Calcular esfuerzos y presiones

2. **Integrar con generador de reportes**
   - Añadir sección de análisis Maxsurf
   - Generar gráficos de presiones
   - Incluir tablas de esfuerzos

3. **Validar con datos reales**
   - Comparar con cálculos manuales
   - Verificar contra normativa DNV
   - Ajustar parámetros si es necesario

## Referencias

- **Maxsurf User Manual:** Capítulo 5 - Section Properties
- **Maxsurf Stability Manual:** Capítulo 3 - Hydrostatic Analysis
- **DNV Pt.3 Ch.5:** Casos de carga para análisis estructural
- **SOLAS II-1:** Requisitos de resistencia estructural
