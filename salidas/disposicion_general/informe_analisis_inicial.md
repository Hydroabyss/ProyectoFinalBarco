# Análisis inicial de datos – Disposición General

Fecha: 2025-11-06 12:15

Fuente Excel: salidas/disposicion_general/Trabajo Tema 3.xlsx

## Dimensiones principales (SI)

- Eslora total (LOA): 107.0
- Eslora entre perpendiculares (Lpp): 105.2
- Manga (B): 15.99
- Puntal (D): 7.9
- Calado (T): 6.2

## Segmentación longitudinal (m)

- Lfp (Pique de proa): 5.26
- Área de carga: 67.77
- Ler (Cámara de máquinas): 26.04
- Lap (Pique de popa): 6.13
- Lpp (suma segmentos): 105.2

## Mamparos – posiciones desde PP de proa (m)

- Mamparo del pique de proa: 5.26
- Mamparo de proa de C.M.: 73.03
- Mamparo de popa de C.M.: 99.07
- PP popa (fin Lpp): 105.2

## Cuadernas (resumen)

- Espaciamiento en zona central (área de carga): 0.7 m
- Espaciamiento en extremos (pique proa/popa y C.M.): 0.6 m

Se han generado los archivos:

- `tabla_general_disposicion.csv`
- `cuadernas_calculadas.csv`

- `cuadernas_origen_popa.csv` (origen en AP)

## Verificaciones de coherencia

- La suma de segmentos coincide con Lpp esperado del Excel.
- Los conteos de cuadernas se aproximan a long/espaciamiento.
- Todas las unidades están en SI (m, m³, t).

## Volumen de doble casco (VDc)

- Cálculo según: VDc = 2.14·LDc·BDc·(D−DDF)·(0.82·CB + 0.217)
- Ver `volumen_doble_casco.csv` para insumos y resultado.

## Dimensionamiento de combustible por autonomía

- Masas y volúmenes calculados con Ce/Cea/Cec y densidad.
- Incluye márgenes de sedimentación/utilización.
- Ver `dimensionamiento_combustible.csv`.

## Estimación de LcM y VCM (carguero)

- LcM = C1·PB10 + C2 (PB10 = P_kW/10).
- VCM = 0.85·LcM·B·(D−DDF_CM)·CB.
- Ver `dimensionamiento_cm.csv`.

## Próximos pasos propuestos

1. Actualizar `resumen_disposicion.json` → `espacios` con los nuevos inicios/finales (según tabla).
2. Regenerar `disposicion_general.pdf` y la gráfica longitudinal con los mamparos actualizados.
3. Recalcular volúmenes de tanques y bodegas si cambiaron longitudes efectivas.
4. Sincronizar Maxsurf (.msd) usando estos valores como referencia (Automation opcional).
5. Validar estabilidad (curvas GZ) y desplazamiento con los nuevos datos.
