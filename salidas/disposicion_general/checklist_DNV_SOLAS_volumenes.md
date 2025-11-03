# Checklist DNV / SOLAS – Volúmenes y Protección Estructural

Este documento cruza los resultados de volúmenes y segmentación con requisitos típicos DNV y SOLAS relevantes para un carguero general con doble casco/doble fondo.

## 1. Dimensiones Principales

- Lpp verificada contra segmentos (Lfp + Área + Ler + Lap). ✔
- LOA pendiente de confirmación final (si se adopta versión extendida). ☐

## 2. Doble Fondo (DNV Pt.3 Ch.2 / SOLAS Reg.9)

- Altura mínima: h ≥ B/20. Con B=15.6 → B/20=0.78 m.
- Altura adoptada (proyecto): 1.20 m (> mínimo). ✔
- Extensión: entre mamparo de pique de proa y mamparo previo a cámara de máquinas (confirmar continuidad). ☐

## 3. Doble Costado (SOLAS / protección lateral)

- Ancho típico adoptado: ~1.8 m cada lado (verificar en offsets). ☐
- Volumen doble casco calculado (VDc) presente. ✔
- Integridad: sin penetraciones grandes (puertas, huecos) fuera de permitidas. ☐

## 4. Cámara de Máquinas

- Longitud LcM coherente con segmentación (26.04 m actual). ✔
- Volumen VCM estimado con fórmula carguero (ver `dimensionamiento_cm.csv`). ✔
- Verificación geométrica pendiente con offsets reales. ☐

## 5. Tanques y Combustible

- Volumen total tanques ≥ volumen requerido para autonomía. (Recalcular cuando `dimensionamiento_combustible.csv` tenga valor válido). ☐
- Factores de utilización y sedimentación aplicados (sí, 3% y 95%). ✔
- Clasificación de tanques (fuel / lastre / servicio) clara en `tanques.csv`. ✔

## 6. Coeficientes de Forma

- CB usado (0.55) dentro de rango típico cargueros (0.55–0.75). ✔
- CP y Csm si disponibles deben compararse con calado de diseño. ☐
- Recalcular CB real con offsets. ☐

## 7. Mamparos Estancos

- Posiciones: pique proa (5.26 m), proa C.M. (73.03 m), popa C.M. (99.07 m), pique popa (105.20 m). ✔
- Distancias cumplen espaciamiento y zonas críticas (proa/popa). ✔
- Validar que cámara de máquinas no invade zona de pique de popa más allá de tolerancias. ☐

## 8. Espaciamiento de Cuadernas

- Zona central: 0.70 m (97 cuadernas). ✔
- Extremos y C.M.: 0.60 m (segmentos proa, C.M. y popa). ✔
- Revisión de rigidez (momento flector) futura con perfiles reales. ☐

## 9. Estabilidad (a integrar)

- Curvas GZ existentes (`curva_gz.png`) deben recalcularse si volúmenes cambian. ☐
- Centro de carena y centros de masa ajustados con nuevo CB. ☐

## 10. Conformidad Documental

- `informe_analisis_inicial.md` incluye segmentación y mamparos. ✔
- `reporte_volumenes_capacidades.md` incluye volúmenes base. ✔
- Falta integrar evidencia de offsets reales. ☐

## 11. Acciones Requeridas

| Acción                                             | Prioridad | Estado    |
| -------------------------------------------------- | --------- | --------- |
| Confirmar LOA definitiva                           | Alta      | Pendiente |
| Exportar offsets y recalcular CB                   | Alta      | Pendiente |
| Validar BDc en modelo                              | Alta      | Pendiente |
| Recalcular combustible requerido (Ce/P reales)     | Media     | Pendiente |
| Actualizar estabilidad tras nuevo volumen          | Media     | Pendiente |
| Verificar penetraciones en doble casco             | Media     | Pendiente |
| Revisar continuidad doble fondo bajo C.M.          | Media     | Pendiente |
| Clasificar tanques (carga vs fuel vs lastre) final | Media     | Parcial   |
| Integrar curva áreas A(x)                          | Baja      | Pendiente |

## 12. Conclusión Inicial

El buque cumple preliminarmente alturas y disposición de doble fondo y segmentación de mamparos; falta verificación geométrica fina vía offsets para consolidar coeficientes y volúmenes exactos. Autonomía y combustible requieren parámetros definitivos de consumos para cierre.
