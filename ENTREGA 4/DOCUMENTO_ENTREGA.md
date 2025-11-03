# ENTREGA 4 · ESTRUCTURA Y DESPLAZAMIENTO  
## Cuaderna maestra – Buque de carga general (Grupo 9)

**Asignatura:** Estructuras Navales · FNB  
**Fecha:** Noviembre 2025  
**Normativa base:** DNV-RU-SHIP Pt.3 / SOLAS II-1  

---

## Resumen ejecutivo
- Se adaptó el plano de cuaderna maestra al buque real (Lpp 105.20 m, B 15.99 m, D 7.90 m, T 6.20 m) verificando capas y geometría en el DXF entregado (`salidas/ENTREGA 3 v4/Corte_Transversal_Cuaderna_Maestra_Detallado.dxf`).
- Las presiones de cálculo para la cuaderna maestra son: fondo 62.34 kPa, costado 31.17 kPa y cubierta 10.00 kPa.
- Elementos críticos: forro exterior (σ_VM 984 MPa, FS 0.36) y módulo resistente global (W_calc 128.29 m³ vs W_DNV 2522.06 m³ → déficit 94.9%).
- Cumplen holgadamente: fondo (FS 1.67), cubierta (FS 6.96), altura de doble fondo (1.20 m ≥ 0.799 m DNV) y ancho de doble costado (1.80 m ≥ 1.066 m SOLAS).
- Se documenta la condición de plena carga usada en Maxsurf (Δ 7 028 t, KG 6.48 m, GMt 0.68 m) y la evaluación simplificada de momentos flectores en aguas tranquilas y con ola H=2.5 m.

---

## 1. Datos del buque

| Parámetro | Valor |
|-----------|-------|
| Eslora entre perpendiculares (Lpp) | 105.20 m |
| Manga (B) | 15.99 m |
| Puntal moldeado (D) | 7.90 m |
| Calado de diseño (T) | 6.20 m |
| Calado de escantillonado | 6.477 m |
| Coeficiente de bloque (Cb) | 0.725 |
| Velocidad de servicio | 14.5 kn |

**Material estructural:** Acero AH36 (σ_y = 355 MPa, E = 206 GPa, ν = 0.30).  
**Espesores de partida:** forro exterior 10.5 mm, fondo 12.0 mm, cubierta principal 8.0 mm (según `herramientas/datos_buque_correctos.py`).  
**Geometría interior:** doble fondo 1.20 m, doble costado 1.80 m, espaciamiento de cuadernas 700 mm en zona central.

**Archivos de datos útiles**
- Hidrostática Maxsurf: `tablas_datos/maxsurf_table.csv`
- Datos consolidados: `tablas_datos/tabla_centralizada_datos.md`
- Verificación normativa: `ENTREGA 4/verificacion_dnv_cuaderna.json`
- Resultados numéricos: `ENTREGA 4/analisis_resistencia.json`

---

## 2. Apartado A · Plano de la cuaderna maestra
1. **Adaptación geométrica**: se escaló el plano de referencia al buque Grupo 9 respetando B=15.99 m, D=7.90 m, h_doble_fondo=1.20 m y b_doble_costado=1.80 m. Se mantuvo la clara de cuadernas 700 mm (600 mm en zonas de transición) y la disposición de refuerzos longitudinales según Trabajo 3.
2. **Verificación de capas**: el análisis automático (`ENTREGA 4/analisis_log.json`) confirmó la presencia de capas de casco, estructura primaria/secundaria, mamparos y línea de agua, sin errores de geometría (75 líneas, 4 arcos, 42 polilíneas).
3. **Planos entregados**:  
   - DXF: `salidas/ENTREGA 3 v4/Corte_Transversal_Cuaderna_Maestra_Detallado.dxf`  
   - Plano de cargas (PNG): `ENTREGA 4/graficos/plano_cargas_cuaderna.png`  
   - Plano de esfuerzos (PNG): `ENTREGA 4/graficos/plano_esfuerzos_cuaderna.png`  
   - Visualizaciones interactivas: `ENTREGA 4/graficos_interactivos/*.html`

---

## 3. Apartado B · Escantillonado longitudinal
### 3.1 Presiones de cálculo (DNV Pt.3 Ch.4)
| Ubicación | Presión | Comentario |
|-----------|---------|------------|
| Fondo | 62.34 kPa | ρ·g·T con ρ=1.025 t/m³ y T=6.20 m |
| Costado | 31.17 kPa | 0.5·ρ·g·T |
| Cubierta | 10.00 kPa | Carga uniformemente distribuida |

### 3.2 Espesores y factores de seguridad
| Elemento | Espesor actual (mm) | FS actual | Espesor requerido para FS=1.5 (mm) | Estado |
|----------|---------------------|-----------|------------------------------------|--------|
| Forro exterior | 10.5 | 0.36 | 43.7 | ❌ No cumple (σ_VM 984 MPa) |
| Fondo | 12.0 | 1.67 | 10.8 | ✓ Cumple |
| Cubierta principal | 8.0 | 6.96 | 1.7 | ✓ Cumple |

> Criterio: FS ∝ t (σ ∝ 1/t). Para forro exterior se requiere al menos 29.1 mm para FS=1.0 y 43.7 mm para FS=1.5.

### 3.3 Módulo resistente global (DNV Pt.3 Ch.3 Sec.2)
- **W_calculado:** 128.29 m³  
- **W_mínimo DNV:** 2522.06 m³  
- **Déficit:** 94.9% → ❌ NO CUMPLE

### 3.4 Recomendaciones de escantillonado
1. **Forro exterior:** elevar espesor a 30–32 mm para cumplir σ_y y a ~44 mm para FS≥1.5; añadir refuerzos longitudinales tipo T para compartir carga.
2. **Módulo resistente:** incorporar refuerzos longitudinales en doble fondo y costados, reducir clara de cuadernas a 0.60 m en zona central y aumentar canto de baos en cubierta principal.
3. **Control normativo:** recalcular con DNV Pt.3 Ch.6 (presión lateral) y actualizar `analisis_resistencia.json` tras cada iteración.

---

## 4. Apartado C · Condición de plena carga en Maxsurf
- **Datos hidrostáticos (Maxsurf Stability):**  
  - Δ = 7 028 213 kg (7028 t) a T = 6.477 m  
  - LWL = 96.948 m, B_WL = 15.545 m, Área WP = 1325.41 m²  
  - KG = 6.477 m, KMt = 7.159 m → GMt = 0.68 m (adrizado)  
  - TPc = 13.585 t/cm, MTc = 83.50 t·m/grad
- **Distribución de pesos aplicada (según enunciado):**  
  - Estructura: 55% del peso en rosca, distribuido A–D según figura de enunciado.  
  - Habilitación: uniforme sobre la eslora de habilitación.  
  - Maquinaria: uniforme en cámara de máquinas.  
  - Equipos: XG ajustado para Trim ≈ 0 en plena carga.
- **Resultado:** condición adrizada (Trim < 0.01 m) y GMt positivo. Los valores anteriores están tabulados en `tablas_datos/maxsurf_table.csv` para trazabilidad.

---

## 5. Apartado D · Momento flector en aguas tranquilas y con ola H=2.5 m
- **Estimación simplificada DNV (script `VerificadorDNV`):**  
  - Coeficiente de ola: 13.84  
  - Momento flector vertical (arrufo, aguas tranquilas + factor 1.2): **11.9×10³ kN·m**  
  - Esfuerzo cortante asociado: **28.3 kN**  
  - Fuente: `salidas/dnv/verificacion_buque_grupo9.json`
- **Condición de ola 2.5 m (recomendación de cálculo):**  
  1. Definir ola sinusoidal H=2.5 m, λ≈Lpp en Maxsurf Stability.  
  2. Evaluar casos hogging/sagging y superponer al momento de aguas tranquilas.  
  3. Exportar curvas de cortante y flector para z=0 y z=D/2; comparar con W_calculado y σ_adm.
- **Observación:** repetir el cálculo una vez ajustados los espesores propuestos en 3.4; el incremento de rigidez longitudinal debería reducir la demanda de σ en forro y aumentar W efectivo.

---

## 6. Apartado E · Resistencia longitudinal (sección central)
- **Alturas mínimas:** doble fondo 1.20 m (≥0.799 m DNV), doble costado 1.80 m (≥1.066 m SOLAS) → cumplen.  
- **Espaciamiento transversales:** 0.70 m en zona central (cumple DNV Pt.3 Ch.3 Sec.2-3).  
- **Espesores:** costado incumple (min DNV 23.7 mm vs 12.0 mm real); cubierta cumple (10 mm ≥ 9.2 mm).  
- **Módulo resistente:** NO cumple (ver 3.3).  
- **Estado global:** 85.7% de checks conformes; se requieren correcciones en forro y módulo resistente antes de certificación.

---

## 7. Archivos entregados
- Documentos: `ENTREGA 4/README.md`, `ENTREGA 4/RESUMEN_EJECUTIVO.md`, `ENTREGA 4/ANALISIS_RESISTENCIA.md`, este `ENTREGA 4/DOCUMENTO_ENTREGA.md`.
- Resultados numéricos: `ENTREGA 4/analisis_resistencia.json`, `ENTREGA 4/verificacion_dnv_cuaderna.json`.
- Planos e imágenes: `ENTREGA 4/graficos/*.png`, `ENTREGA 4/graficos_interactivos/*.html`.
- Logs y tablas: `ENTREGA 4/analisis_log.json`, `ENTREGA 4/tablas/analisis_capas.xlsx`, `ENTREGA 4/tablas/verificaciones_dnv.xlsx`.

---

## 8. Conclusiones y próximos pasos
1. **Crítico:** incrementar espesor de forro exterior y reforzar longitudinalmente hasta alcanzar FS≥1.5 y W ≥ W_DNV.  
2. **Verificación:** repetir los cálculos de presión lateral DNV Pt.3 Ch.6 con los nuevos espesores y actualizar `analisis_resistencia.json`.  
3. **Estabilidad:** mantener KG≈6.5 m y revisar GMt tras cualquier cambio de peso; verificar curvas de flector en Maxsurf con ola H=2.5 m.  
4. **Documentación:** exportar los nuevos planos DXF/PNG y adjuntarlos como anexos A-E para la versión final.

---

```
Comando reproducible
--------------------
python3 herramientas/analizar_cuaderna_completo_v2.py
```
