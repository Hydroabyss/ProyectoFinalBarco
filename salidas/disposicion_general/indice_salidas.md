# Índice de salidas de disposición general

Este documento resume los archivos generados por `herramientas/generar_disposicion_general.py`, agrupados por tablas (CSV/XLSX/JSON) y material gráfico (PNG/DXF/PDF).

## Tablas y datos estructurados

| Conjunto                    | Archivo                    | Descripción                                                                   |
| --------------------------- | -------------------------- | ----------------------------------------------------------------------------- |
| Cadena de cuadernas         | `cuadernas.csv`            | Posición de cada cuaderna, paso y zona (proa/central/popa).                   |
| Mamparos principales        | `mamparos.csv`             | Coordenadas longitudinales y notas de cada mamparo.                           |
| Espacios de la disposición  | `espacios.csv`             | Extensión, uso y límites de cada espacio del buque.                           |
| Tanques de consumo / lastre | `tanques.csv`              | Estimaciones de volumen y servicio de cada tanque de doble fondo.             |
| Bodegas de carga            | `bodegas.csv`              | Largo útil y volumen disponible por bodega.                                   |
| Resumen de tanques          | `resumen_tanques.csv`      | Volumen y porcentaje que aporta cada tanque respecto al total.                |
| Balance de combustible      | `balance_combustible.csv`  | Comparativa entre volumen requerido, disponible, margen y porcentajes.        |
| Resumen estructurado        | `resumen_disposicion.json` | Consolidado en formato JSON de mamparos, espacios, tanques y bodegas.         |
| Libro unificado             | `disposicion_general.xlsx` | Hoja de cálculo con todas las tablas anteriores, más resúmenes, por pestañas. |

## Gráficos y planos exportados

| Visualización                                | Archivo                         | Formato                                                      |
| -------------------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| Distribución longitudinal por compartimentos | `distribucion_longitudinal.png` | Imagen en alta resolución para el informe.                   |
| Plano longitudinal para CAD                  | `distribucion_longitudinal.dxf` | Exportación en DXF con capas coloreadas por espacio.         |
| Balance de volúmenes de tanques              | `tanques_consumo.png`           | Gráfico de barras de capacidades de tanques.                 |
| Balance combustible vs. requerimiento        | `balance_combustible.png`       | Comparación del volumen requerido, disponible y margen.      |
| Capacidad útil de bodegas                    | `capacidad_bodegas.png`         | Gráfico comparativo de bodegas vs. requerimiento.            |
| Curva de estabilidad (GZ)                    | `curva_gz.png`                  | Brazo de estabilidad frente al ángulo de escora.             |
| Curva de desplazamiento                      | `curva_desplazamiento.png`      | Desplazamiento vs. calado.                                   |
| Plano de formas                              | `bodyplan.png`                  | Secciones transversales generadas en el modelo hidrostático. |
| Perfil y líneas de agua                      | `perfil.png`                    | Vista lateral del buque de referencia.                       |

## Informe compilado

| Documento          | Archivo                   | Contenido                                                                          |
| ------------------ | ------------------------- | ---------------------------------------------------------------------------------- |
| Informe Problema 3 | `disposicion_general.pdf` | Respuestas detalladas a los apartados A–E con tablas, gráficos y citas normativas. |

> Ubicación: todos los archivos listados se encuentran en `salidas/disposicion_general/`.
