# Tabla centralizada de datos del buque y análisis

| Categoría               | Parámetro                       | Símbolo | Valor          | Unidad | Fuente/Referencia                        |
| ----------------------- | ------------------------------- | ------- | -------------- | ------ | ---------------------------------------- |
| Dimensiones principales | Eslora entre perpendiculares    | Lpp     | 105,2          | m      | Resumen_Disposición.json v4              |
|                         | Manga máxima                    | B       | 15,99          | m      | Resumen_Disposición.json v4              |
|                         | Puntal moldeado                 | D       | 7,90           | m      | Resumen_Disposición.json v4              |
|                         | Calado de diseño                | T       | 6,20           | m      | Resumen_Disposición.json v4              |
|                         | Desplazamiento (T = 6,20 m)     | Δ       | 7752,9         | t      | Dimensiones_Estructurales_Detalladas.csv |
|                         | Volumen de carena               | ∇       | 7563,8         | m³     | Δ / ρ (ρ = 1,025 t/m³)                   |
|                         | Superficie mojada estimada      | S       | 2375,8         | m²     | Trabajo 2 Grupo 9, tabla                 |
|                         | Coeficiente de bloque           | Cb      | 0,725          | -      | Resumen_Disposición.json v4              |
|                         | Coeficiente de flotación        | Cwp     | 0,944          | -      | Trabajo 2 Grupo 9, tabla                 |
|                         | Velocidad de servicio           | V       | 14,5           | kn     | Trabajo 2 Grupo 9, tabla                 |
| Hidrostática            | KG inicial                      | KG0     | 6,477          | m      | Cálculo propio                           |
|                         | KM                              | KM      | 7,159          | m      | Cálculo propio                           |
|                         | Desplazamiento                  | Δ       | 7752,9         | t      | Dimensiones_Estructurales_Detalladas.csv |
|                         | Densidad agua                   | ρ       | 1025           | kg/m³  | Trabajo 2 Grupo 9, tabla                 |
|                         | Viscosidad cinemática           | ν       | 1,19E-06       | m²/s   | Trabajo 2 Grupo 9, tabla                 |
| Resistencia (Holtrop)   | Resistencia viscosa             | Cv      | 134,75         | kN     | Trabajo 2 Grupo 9, tabla                 |
|                         | Resistencia apéndices           | Rapp    | 0,00           | kN     | Trabajo 2 Grupo 9, tabla                 |
|                         | Resistencia olas                | Rw      | 74,10          | kN     | Trabajo 2 Grupo 9, tabla                 |
|                         | Resistencia bulbo               | RB      | 68,45          | kN     | Trabajo 2 Grupo 9, tabla                 |
|                         | Resistencia total               | Rtotal  | 312,47         | kN     | Trabajo 2 Grupo 9, tabla                 |
|                         | Potencia remolque               | EHP     | 3128,39        | CV     | Trabajo 2 Grupo 9, tabla                 |
|                         | Potencia remolque               | EHP     | 2330,65        | kW     | Trabajo 2 Grupo 9, tabla                 |
| Propulsión y hélice     | Diámetro hélice                 | D       | 4,4            | m      | Trabajo 2 Grupo 9, tabla                 |
|                         | Número de palas                 | Z       | 5              | -      | Trabajo 2 Grupo 9, tabla                 |
|                         | Rendimiento hélice              | η₀      | 0,71           | -      | Trabajo 2 Grupo 9, tabla                 |
|                         | Rendimiento mecánico línea ejes | ηm      | 0,99           | -      | Trabajo 2 Grupo 9, tabla                 |
|                         | AE/AO                           | AE/AO   | 0,57           | -      | Trabajo 2 Grupo 9, Serie B               |
|                         | P/D                             | P/D     | 1,3            | -      | Trabajo 2 Grupo 9, Serie B               |
|                         | n (rpm)                         | n       | 220            | rpm    | Trabajo 2 Grupo 9, Serie B               |
|                         | KT                              | KT      | 0,4522         | -      | Trabajo 2 Grupo 9, Serie B               |
|                         | KQ                              | KQ      | 0,0838         | -      | Trabajo 2 Grupo 9, Serie B               |
|                         | Empuje generado                 | T       | 2333,3         | kN     | Trabajo 2 Grupo 9, Serie B               |
|                         | Empuje requerido                | T       | 2294,5         | kN     | Trabajo 2 Grupo 9, Serie B               |
| Motor seleccionado      | Modelo                          | -       | Wärtsilä 16V26 | -      | Trabajo 2 Grupo 9, tabla                 |
|                         | Potencia                        | -       | 5440           | kW     | Trabajo 2 Grupo 9, tabla                 |
|                         | Potencia punto M                | -       | 5336,69        | kW     | Trabajo 2 Grupo 9, tabla                 |
| Combustible             | Densidad combustible            | ρ_fuel  | 0,85           | t/m³   | Tabla_03_tanques_combustible.csv         |
|                         | KG doble fondo                  | KG_db   | 0,78           | m      | DNV Pt.3 Ch.2 Sec.3 [2.3]                |
|                         | KG tanques ala                  | KG_wing | 2,0            | m      | Cálculo propio                           |
|                         | Consumo 12 días (carga normal)  | Cdia    | 22,61          | t/día  | Tabla_06_consumo_combustible.csv         |
|                         | Volumen requerido 12 días       | Vreq    | 319,2          | m³     | Consumo / ρ_fuel                         |
|                         | Volumen disponible en tanques   | Vdisp   | 1140,97        | m³     | Tabla_03_tanques_combustible.csv         |
|                         | Margen volumétrico              | Vmargin | 821,77         | m³     | Resumen_Disposición.json v4              |
|                         | Cobertura sobre consumo         | Cob%    | 357,45         | %      | Resumen_Disposición.json v4              |
|                         | Autonomía con tanques llenos    | Diasmax | 42,9           | días   | Vdisp / (Consumo/ρ_fuel)                 |

> Todos los datos han sido extraídos y mapeados de las tablas, imágenes y textos del documento, y de los cálculos realizados en los scripts. Si algún dato adicional es detectado, se añadirá a esta tabla.
