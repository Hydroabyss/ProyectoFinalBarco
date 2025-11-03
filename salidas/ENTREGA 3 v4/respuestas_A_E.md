# Respuestas Apartados A–E (Problema 3)

## A. Ubicación de mamparos principales

| Elemento                            | Posición (m) | Referencia                                    |
| ----------------------------------- | ------------ | --------------------------------------------- |
| Mamparo de colisión (pique de proa) | 6.0          | Trabajo 3 · claridad 0.6 m / cuadernas 700 mm |
| Mamparo proa cámara de máquinas     | 82.0         | Segmentación `Tabla_02_espacios.csv`          |
| Mamparo popa cámara de máquinas     | 97.0         | Segmentación `Tabla_02_espacios.csv`          |
| Mamparo de pique de popa            | 105.2        | Segmentación `Tabla_02_espacios.csv`          |

- Se mantiene la clara de cuadernas solicitada: 0.70 m en zona central, 0.60 m en las transiciones.
- Con LPP = 105.2 m se garantizan ≥5 mamparos estancos conforme DNV Pt.3 Ch.2 Sec.2.

## B. Disposición general y elementos de cierre

- **Doble fondo:** altura constante 1.20 m (≥ h<sub>DB,min</sub> = 0.80 m) desde mamparo de colisión hasta pique de popa.
- **Doble costado:** 1.80 m por banda, con mamparos longitudinales internos que dejan manga interior 12.39 m.
- **Cubiertas:**
  - Cubierta principal a z = 7.90 m.
  - Cubierta secundaria (hipótesis trabajo) en z = 5.20 m.
- **Mamparos transversales:** ubicaciones de la tabla anterior más subdivisiones interiores en bodegas conforme a carga.
- **Motor principal:** centrado entre mamparos 82–97 m; longitud efectiva 15 m.
- **Tanques de alimentación:**
  - Tanque diario (vol. 4.62 m³) a proa del motor (90–92 m).
  - Tanques de ala babor/estribor (107.28 m³ c/u) entre 83–95 m, conectados a sala de máquinas.

## C. Volúmenes de tanques de consumo

- Volumen total disponible: **1 140.97 m³** (`Figura_02_capacidades_tanques.csv`).
- Consumo objetivo actualizado (motor principal 16V26 + auxiliares + servicios) para 30 días de autonomía: **30 612 kg/día = 30.612 t/día**, equivalente a **34.01 m³/día** con densidad de cálculo 0.90 t/m³ (`Tabla_06_consumo_combustible.csv`).
  - Motor principal: **25.85 t/d (84.4 %)** → **28.72 m³/d**.
  - Generadores auxiliares: **4.09 t/d (13.4 %)** → **4.54 m³/d**.
  - Servicios y pérdidas: **0.68 t/d (2.2 %)** → **0.75 m³/d**.
- Requerimiento para 30 días: **918.36 t** → **1 020.4 m³**.
- Margen neto con el volumen disponible: **+120.6 m³** (11.8 % sobre el requerido). Operar con llenados 85–90 % (≈ 969–1 027 m³) para cumplir MARPOL y reservar 40–50 m³ para retornos y mezclas.
- Tipo de combustible y densidad: destilado/LSFO/MGO con densidad de cálculo **0.90 t/m³**.

## D. Modelado de espacios en `Maxsurf`

- Importar la geometría actualizada (`Figura_06_bodyplan.png`, `Plano_01_distribucion_longitudinal.dxf`).
- Definir zonas siguiendo `Tabla_02_espacios.csv` (pique proa, bodegas 1–3, sala de máquinas, pique popa).
- Asignar densidades:
  - Bodegas: 1 050 kg/m³ (carga general).
  - Tanques FO: 850 kg/m³.
  - Lastres: 1 025 kg/m³.
- Validar curva GZ (`Figura_05_curva_gz.png`) con cargamentos extremos.

## E. Capacidad de bodegas vs. especificación

| Bodega               | Volumen útil (m³) |
| -------------------- | ----------------- |
| 1                    | 1 848.65          |
| 2                    | 1 848.65          |
| 3                    | 1 506.30          |
| **Total disponible** | **5 203.60**      |

- Requerimiento proyecto: **≥ 5 000 m³**.
- Cumplimiento: margen positivo **+203.6 m³ (4.1 %)**.
- Recomendar verificar accesibilidad a escotillas tras ajuste de manga interior (12.39 m).

## Conclusiones y acciones

1. La disposición longitudinal y los tanques cumplen con DNV/SOLAS tras actualizar B = 15.99 m y LPP = 105.2 m.
2. Se debe actualizar la rotulación en planos DWG/DXF antes de la entrega final (valores heredados 15.60 m).
3. Ejecutar `herramientas/verificar_calidad.py` para validar CSV/JSON antes de generar PDF definitivo.
