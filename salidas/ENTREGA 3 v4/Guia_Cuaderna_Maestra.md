# Guía para definir la cuaderna maestra

Esta nota resume los datos mínimos que debemos solicitar y los criterios normativos (DNV/SOLAS) a tener en cuenta antes de dibujar y comprobar la cuaderna maestra del buque de carga general del Proyecto Final. También recoge recomendaciones prácticas para el modelado en AutoCAD y para la verificación posterior en los módulos de Estructura y Estabilidad del software Maxsurf.

## 1. Datos imprescindibles a solicitar

| Categoría                          | Descripción                                                                                                                                  | Motivo                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Geometría básica                   | LOA, LPP, manga en cubierta, manga en la línea de flotación, calado de proyecto, puntal, arrufo en cubierta principal                        | Define los ejes y la envolvente dimensional de la cuaderna maestra.         |
| Coordenadas de la cuaderna maestra | Distancia longitudinal desde la roda (X), referencias en plano de formas (estación), desplazamientos (offsets) en tablas de formas si existe | Permite alinear el plano de cuadernas del CAD con la sección maestra real.  |
| Separación de cuadernas            | Clara central 700 mm y 600 mm en las zonas de transición (según enunciado) + confirmación de si la cuaderna maestra es del bloque central    | Determina el paso entre elementos estructurales y la cuantía de refuerzos.  |
| Espesores de plancha               | Forro exterior, forro interior de doble fondo, cubierta principal, cubiertas parciales, refuerzos longitudinales                             | Necesarios para calcular módulos resistentes y pesos.                       |
| Refuerzos transversales            | Geometría de baos, refuerzos de cubierta, carlingas, codastes, longitud y orientación                                                        | Afecta a la rigidez de la cuaderna y a la continuidad estructural.          |
| Refuerzos longitudinales           | Barrotes de doble fondo, longitudinales de costado, largueros, refuerzos de cubiertas                                                        | Necesarios para determinar cómo se empotran/atraviesan la cuaderna maestra. |
| Soportes y penetraciones           | Penetraciones para tuberías, puertas estancas, aberturas de ventilación, soportes de maquinaria                                              | Cambian la distribución de esfuerzos y requieren refuerzos locales.         |
| Cotas de espacios                  | Alturas y anchos de bodegas, pasillos, doble fondo, tanques de ala, longitud de cámara de máquinas en la cuaderna                            | Importante para validar contra requisitos volumétricos y accesibilidad.     |
| Cargas de cálculo                  | Presión hidrostática de proyecto, cargas de lastre, cargas de cubierta (contenedores, carga general), cargas de equipo (grúas, escotillas)   | Requeridas para dimensionar refuerzos según DNV Pt.3 Ch.3 y Ch.5.           |
| Datos de peso                      | Masa y centro de gravedad de equipos instalados en la cuaderna (maquinaria, tuberías principales, lastre fijo)                               | Ayudan a evaluar el equilibrio local y el momento flector transversal.      |
| Condiciones de servicio            | Categoría de navegación, estado de carga crítico, calado en aguas de proyecto                                                                | Determina qué reglas SOLAS y DNV aplican y los márgenes de seguridad.       |

> **Nota:** si alguna magnitud no está disponible, deje explícita la hipótesis elegida para poder ajustar más adelante.

## 2. Referencias normativas relevantes

| Norma                              | Capítulo / Regla                                 | Aplicación a la cuaderna maestra                                                                          |
| ---------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| DNV Pt.3 Ch.2 Sec.2 [1.1.1-1.1.6]  | Disposición mínima de mamparos estancos          | Verifica que la cuaderna maestra queda entre los mamparos reglamentarios y no invade espacios prohibidos. |
| DNV Pt.3 Ch.2 Sec.3 [2.2-2.4]      | Altura y continuidad del doble fondo             | Define alturas mínimas del doble fondo bajo la cuaderna y limitaciones de pozos.                          |
| DNV Pt.3 Ch.3 Sec.2-3              | Dimensionamiento de elementos transversales      | Criterios de módulo resistente, esbeltez y continuidad de los refuerzos transversales.                    |
| DNV Pt.3 Ch.3 Sec.4                | Reglas para costados y cubiertas                 | Clasifica zonas expuestas (costado, cubierta principal) y los espesores mínimos.                          |
| DNV Pt.3 Ch.5 Sec.1-2              | Casos de carga para estructuras                  | Combina presión hidrostática + cargas de cubierta + cargas concentradas.                                  |
| SOLAS 1974 Cap. II-1 Regla 13 y 26 | Integridad de mamparos y seguridad de maquinaria | Alinea la cuaderna con la envolvente de espacios estancos y equipos esenciales.                           |

Recomendación: anotar en el plano cada referencia empleada (p. ej., "DNV Pt.3 Ch.3 Sec.2 201" para barras de costado) para facilitar la trazabilidad durante la revisión.

## 3. Requisitos geométricos mínimos

1. **Sistema de ejes**
   - X = 0 en proa, positivo hacia popa.
   - Y = 0 en el plano diametral, positivo a estribor.
   - Z = 0 en la línea de quilla (línea base), positivo hacia arriba.
2. **Claras de cuadernas**
   - 700 mm en el bloque central donde se ubique la cuaderna maestra.
   - 600 mm en las zonas inmediatamente a proa del pique de proa y a popa del mamparo de proa de la cámara de máquinas. Si la cuaderna maestra se localiza en esas zonas, ajustar la separación.
3. **Doble fondo**
   - Altura mínima h<sub>DB</sub> = `max(760 mm, 1000 · B / 20)` con límite superior 2000 mm. Para B = 14.3 m → h<sub>DB</sub> ≈ 715 mm, pero se adopta 760 mm por regla.
   - Extender el doble fondo hasta el trancanil para protección, salvo zonas de máquinas con pozos autorizados.
4. **Cubierta principal**
   - Grosor mínimo según DNV Pt.3 Ch.3 Sec.4 (introducir el valor una vez se conozca el espesor requerido por cálculo). Indicar la bóveda y el arrufo si aplica.
5. **Tanques de ala y espacios laterales**
   - Marcar cotas interiores disponibles para tanques de combustible/lastre con la altura útil y la separación respecto a la cuaderna.

## 4. Contenido mínimo del plano de cuaderna maestra

- Perfil del forro exterior con espesores anotados.
- Límites del doble fondo y longitud efectiva de topas y longitudinales.
- Baos y refuerzos de cubierta (sección, espesor, distancia al centro).
- Longitudinales de costado (dimensión, separación vertical, continuidad).
- Refuerzos de puntal (elementos parciales, largueros) y posibles refuerzos de la cámara de máquinas.
- Datos de soldadura o tipo de unión cuando sea relevante (DNV Pt.3 Ch.3 Sec.1).
- Penetraciones y aberturas relevantes (puertas, tuberías, escotillas) con sus refuerzos locales.
- Notas sobre galvanización/protección si se requieren (p. ej., en tanques de combustible).

## 5. Orientaciones para el modelado en AutoCAD

1. **Plantillas y capas**
   - Capa `Ejes` para líneas de referencia (baseline, centreline, cubiertas).
   - Capa `Forro` para platas y costados.
   - Capa `Refuerzos` para baos, varengas y longitudinales.
   - Capa `Anotaciones` para textos y cotas.
   - Utilizar unidades en metros con precisión de 0.001.
2. **Procedimiento sugerido**
   - Insertar el contorno exterior (body plan o spline) importado desde Maxsurf (`Figura_06_bodyplan.png` o `Plano_01_distribucion_longitudinal.dxf`).
   - Dibujar el doble fondo con su altura h<sub>DB</sub> y ancho útil deducido de `Tabla_03_tanques_combustible.csv`.
   - Añadir baos de cubierta con camber: usar arco centrado en centreline, altura según especificación.
   - Colocar varengas y refuerzos transversales cada 0.7 m (o 0.6 m en zonas de transición). Etiquetar "Varenga tipo A/B" según espesor.
   - Integrar longitudinales: representar cortes (pasando por la cuaderna) e indicar continuidad mediante símbolos.
   - Documentar penetraciones: dibujar recortes y añadir refuerzos perimetrales (placas collarín).
3. **Exportaciones**
   - Guardar en DWG y DXF (versión 2013) para compatibilidad con herramientas externas.
   - Generar PDF a escala 1:50 en A4 o A3 incluyendo cartela con datos de proyecto.

## 6. Validaciones recomendadas

- **Comprobación de módulo resistente**: calcular `Z = I / y_max` usando los espesores reales y comparar con el requerido por DNV Pt.3 Ch.3 Sec.2.
- **Chequeo de tensiones**: verificar que `σ = M / Z` no supera `f_d = σ_y / γ_M`. Si falta `M`, estimar con la envolvente de cargas proporcionada (hidrostática + carga de cubierta).
- **Compatibilidad con tanques**: cruzar con `Figura_02_capacidades_tanques.csv` y `Tabla_03_tanques_combustible.csv` para garantizar que no se invaden espacios reservados.
- **Alineación con mamparos**: comprobar que las uniones con los mamparos principales (ver `Tabla_01_mamparos.csv`) disponen de refuerzo adecuado y continuidad de los longitudinales.
- **Accesibilidad y mantenimiento**: confirmar que se cumplen los pasillos y accesos mínimos según DNV Pt.3 Ch.2 Sec.4 (inspección), dejando aberturas de hombre si corresponde.

## 7. Entregables esperados

1. Plano de cuaderna maestra (DWG/DXF) con capas separadas y cartela.
2. PDF listo para impresión con escala, cotas y leyenda normativa.
3. Hoja de cálculo (o pestaña adicional en `Anexo_Tablas_Disposicion.xlsx`) con el resumen de espesores, secciones y verificaciones (Z requerido vs. disponible).
4. Nota técnica breve indicando suposiciones, referencias y conclusiones de las comprobaciones (puede integrarse en `Extractos_Normativos.md` o nuevo apéndice).

---

**Próximos pasos sugeridos**

1. Confirmar datos pendientes de la tabla anterior con el grupo de diseño (especialmente espesores y cargas de cubierta).
2. Incorporar la geometría definitiva de la cuaderna maestra en AutoCAD siguiendo el flujo del apartado 5.
3. Validar con un análisis rápido en Maxsurf Structure u otra herramienta FEM la tensión máxima y el margen respecto al límite de fluencia.
4. Actualizar el repositorio con los nuevos planos y resultados, junto con un registro de cambios en `CAMBIOS_REALIZADOS.md`.
