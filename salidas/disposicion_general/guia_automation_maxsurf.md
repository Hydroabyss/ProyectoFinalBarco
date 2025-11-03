# Guía de Automatización Maxsurf (Modelo `.msd`)

Esta guía describe cómo extraer datos geométricos y planos desde un modelo Maxsurf (`.msd`) para validar los cálculos de volúmenes y dimensiones del buque de práctica.

## 1. Objetivos

- Obtener offsets (coordenadas de secciones transversales) para recalcular volumen y coeficiente de bloque real.
- Exportar vistas ortogonales (body plan, perfil, planta) para verificar forma del casco y mamparos.
- Verificar coherencia entre geometría del casco exterior y el espacio interior (manga interior disponible tras doble costado).

## 2. Métodos de Automation (VBA / COM)

En un entorno Windows con Maxsurf instalado se puede usar VBA (por ejemplo en Excel) o scripts COM.

### 2.1 Exportar Offsets

```vb
' Exporta offsets cada 0.5 m de eslora (ajustar separación según precisión requerida)
Model.ExportOffsets "offsets_0p5m.csv", 0.5
```

Formato típico del archivo: filas por estación longitudinal y columnas con semimangas y alturas. Si la salida incluye solo puntos, se reconstruyen áreas de sección.

### 2.2 Exportar Vistas DXF

```vb
' Body plan (2)
Model.ExportOrthogonalViewDXF "bodyplan.dxf", 2
' Perfil (3)
Model.ExportOrthogonalViewDXF "perfil.dxf", 3
' Planta (4)
Model.ExportOrthogonalViewDXF "planta.dxf", 4
```

### 2.3 Validar Principales

```vb
Dim Lpp As Double, Beam As Double, Depth As Double, Draft As Double
Lpp = Model.LengthBetweenPerpendiculars
Beam = Model.MaxBeam
Depth = Model.Depth
Draft = Model.DesignDraft
```

Comparar estos valores con los de `tabla_referencia.csv` y `resumen_disposicion_actualizado.json`.

## 3. Cálculo del Volumen Real del Casco

1. Leer `offsets_0p5m.csv` en Python.
2. Para cada estación, reconstruir el contorno de la sección y calcular área (A_i).
3. Aplicar integración numérica (Simpson o trapezoidal): `V ≈ Σ A_i * Δx`.
4. Calcular `CB_real = V / (Lpp * B * T)`.
5. Comparar `CB_real` con `CB` usado en cálculos previos (`reporte_volumenes_capacidades.md`).

## 4. Manga Interior Efectiva

Procedimiento:

1. Identificar semimanga en la sección a la altura del doble costado interior.
2. Manga interior = 2 \* (semimanga interior) - (descontar holguras si procede).
3. Usar esta manga interior en fórmula de volumen interior aproximado para mejorar la estimación.

## 5. Verificación de Doble Casco y Doble Fondo

- Altura doble fondo ≥ B/20 (criterio DNV). Comprobar `DDF` del modelo.
- Ancho doble costado (BDc) uniforme o variar según zonas: medir en varias estaciones.
- Continuidad: no debe haber interrupciones significativas en estructura dentro de zona de protección.

## 6. Validación de Cámara de Máquinas

1. A partir de estaciones que delimitan LcM, calcular volumen dentro del borde inferior de cubierta y por encima del doble fondo.
2. Comparar con VCM estimado (ver `dimensionamiento_cm.csv`).

## 7. Integración con Scripts Existentes

- Colocar archivos exportados (`offsets_*.csv`, `bodyplan.dxf`, etc.) en `salidas/disposicion_general/`.
- Extender `analisis_detallado_volumenes.py` para detectar el archivo de offsets y recalcular volumen real.

## 8. Control de Calidad

Checklist rápido:

- [ ] Lpp coincide en Maxsurf y en base de datos.
- [ ] CB recalculado dentro de ±2% del valor de diseño.
- [ ] Doble fondo cumple altura mínima.
- [ ] BDc medido consistente con valor usado en VDc.
- [ ] Volumen de cámara de máquinas razonable (no excede estimación por >15%).
- [ ] Offsets cubren toda la eslora (sin huecos grandes > Δx especificado).

## 9. Próximos Pasos

- Automatizar lanzamiento de Maxsurf y exportación periódica.
- Generar curva de áreas (A(x)) y graficarla para inspección visual.
- Integrar validación de estabilidad (curvas GZ) con masas calculadas.

---

**Nota:** Esta guía es genérica; adaptar nombres de archivos y rutas según entorno real. El script actual no abre `.msd` directamente; depende de exportaciones de Maxsurf.
