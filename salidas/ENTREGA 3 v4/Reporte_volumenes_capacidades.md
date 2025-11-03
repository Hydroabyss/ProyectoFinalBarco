# Reporte de Volúmenes y Capacidades

Fuente JSON: `Resumen_Disposicion.json`

## Dimensiones principales

- Lpp: 105.2
- Manga B: 15.99
- Manga interior (aprox): 12.39
- Puntal D: 7.9
- Calado T: 6.2
- Coeficiente de bloque CB: 0.7252

## Segmentación longitudinal

| segmento           | inicio_m | fin_m | long_m | espaciamiento_m | cuadernas |
| :----------------- | -------: | ----: | -----: | --------------: | --------: |
| Pique de proa      |        0 |  5.26 |   5.26 |             0.6 |         9 |
| Área de carga      |     5.26 | 73.03 |  67.77 |             0.7 |        97 |
| Cámara de máquinas |    73.03 | 99.07 |  26.04 |             0.6 |        43 |
| Pique de popa      |    99.07 | 105.2 |   6.13 |             0.6 |        10 |

## Volúmenes globales (aproximaciones)

- Volumen bloque (Lpp·B·T·CB): 7563.34112352 m3
- Volumen interior aproximado: 9645.3672 m3
- Volumen doble casco (VDc): 3426.1207543808 m3
- Volumen cámara de máquinas (VCM): 990.5838579 m3

## Tanques y combustible

- Volumen total tanques (sumatoria): 1085.069523600777 m3
- Combustible requerido (con márgenes): 770.8 m3
- Cobertura tanques vs requerido: 140.8%

Notas de combustible y utilización:

- Tipo de combustible considerado: destilado/LSFO/MGO de baja azufre.
- Densidad usada para conversión masa↔volumen: 0.88 t/m³ (rango típico 0.85–0.90 t/m³ según temperatura y especificación).
- Operación recomendada: llenado operativo 85–90% de la capacidad total (≈ 922–977 m³) para cumplir MARPOL, permitir expansión térmica y facilitar retornos.

## Observaciones

- Verificar que LDc y BDc coincidan con la extensión real del doble casco (entre mamparos).
- Ajustar B_interior con medición directa del modelo Maxsurf (Offsets) para precisión.
- Recalcular VDc si DDF varía fuera de cámara de máquinas.
- Validar compatibilidad de VCM con espacio real en modelo 3D.
- Con margen del 40.8 % sobre el requerido, revisar plan de operación (llenado 85–90 %) para mantener peso bajo control.

## Próximos pasos

1. Exportar offsets desde Maxsurf (automatización) para reemplazar aproximaciones de volumen.
2. Incorporar cálculo de curvas de capacidad por calado parcial.
3. Validar doble casco contra normativa DNV (espesor, continuidad).
4. Integrar estabilidad (GZ) con nuevo reparto de pesos/volúmenes.
