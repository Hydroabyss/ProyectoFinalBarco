# Extractos normativos utilizados

Este anexo recoge texto íntegro de las normas citadas en el informe automático, tomado de los documentos proporcionados en la carpeta `normativa/`, y relaciona cada exigencia con las dimensiones actualizadas del buque (noviembre 2025).

## Resumen dimensional aplicado

- **Eslora total (LoA) = 107,0 m** → medida sobre los planos y extendida +1,8 m hacia popa desde el eje de la pala del timón conforme DNV Pt.3 Ch.1/Ch.2.
- **Longitud entre perpendiculares = 105,2 m** → suma de tramos `Lfp + Área de carga + Ler + Lap`; es la longitud de regla utilizada por DNV para tablas de subdivisión.
- **Manga máxima (B) = 15,99 m** → valor exterior en la zona central; sustituye la manga moldeada de 15,6 m en verificaciones normativas.
- **Puntal (D) = 7,9 m** → dato estructural actualizado.
- **Calado de proyecto (T) = 6,2 m**.

> Nota: Las verificaciones geométricas (holguras de timón y sobresalientes) se basan en LoA, mientras que los requisitos de subdivisión y doble fondo usan la longitud entre perpendiculares y la manga máxima B.

### Consecuencias inmediatas sobre las normas

- **Altura de doble fondo** (DNV Pt.3 Ch.2 Sec.3 [2.3]): con B = 15.99 m ⇒ h<sub>DB</sub> ≥ 0.80 m. El diseño adopta 1.20 m ⇒ ✔ margen de 0.40 m.
- **Número mínimo de mamparos** (DNV Pt.3 Ch.2 Sec.2 [1.1.4]): para L ≥ 105 m se requiere al menos 5 mamparos transversales estancos. La disposición actual (pique proa, mamparos C.M., pique popa + subdivisiones intermedias) mantiene cumplimiento.
- **Protección lateral** (SOLAS Regla 9 + DNV Pt.3 Ch.2 Sec.3): verificar continuidad de doble costado ≥ 1,80 m a cada banda con la nueva manga máxima; pendiente confirmar con offsets.

## DNV Pt.3 Ch.2 Sec.2 [1.1.1-1.1.6]

```text
SECTION 2 SUBDIVISION ARRANGEMENT
1 Watertight bulkhead arrangement
1.1 Number and disposition of watertight bulkheads
1.1.1 All ships shall have at least the following transverse watertight bulkheads:
a) one collision bulkhead
b) one aft peak bulkhead
c) one bulkhead at each end of the engine room.
1.1.2 In the case of ships with an electrical propulsion plant, both the generator room and the engine room shall be enclosed by watertight bulkheads.
1.1.3 In addition to the requirements of [1.1.1] and [1.1.2], the number and disposition of bulkheads shall be arranged to suit the requirements for transverse strength, subdivision, floodability and damage stability, and shall be in accordance with the requirements of national regulations.
1.1.4 For vessels where no damage stability calculations have been carried out the total number of watertight transverse bulkheads shall not be less than given in Table 1.
1.1.5 The watertight bulkheads shall extend to the bulkhead deck.
1.1.6 For ships with a continuous deck below the freeboard deck and where the draught is less than the depth to this second deck, all bulkheads except the collision bulkhead may terminate at the second deck. In such cases the engine casing between second and bulkhead deck shall be arranged as a watertight structure, and the second deck shall be watertight outside the casing above the engine room.
```

## DNV Pt.3 Ch.2 Sec.3 [2.2-3.1]

```text
2.2 Extent of double bottom
For passenger vessels and cargo ships other than tankers, a double bottom shall be fitted, extending from the collision bulkhead to the aft peak bulkhead, as far as this is practicable and compatible with the design and proper working of the ship.
2.3 Height of double bottom
Where a double bottom is required to be fitted the inner bottom shall be continued out to the ship side in such a manner as to protect the bottom to the turn of bilge. Such protection will be deemed satisfactory if the inner bottom is not lower at any part than a plane parallel with the keel line and which is located not less than a vertical distance hDB measured from the keel line, in mm, as calculated by the formula: hDB = 1000 · B/20, minimum 760 mm. The height, hDB, need not be taken more than 2000 mm. The height, hDB, shall be sufficient to give good access to all parts of the double bottom. For ships with large rise of floor, the minimum height may have to be increased after special consideration.
2.4 Small wells in double bottom tank
Small wells constructed in the double bottom, in connection with the drainage arrangements of holds, shall not extend in depth more than necessary. For ships with length LLL 80 m or above the vertical distance from the bottom of such a well to a plane coinciding with the keel line shall not be less than 500 mm or half the required double bottom height. Other wells, e.g. for lubricating oil under main engines, may be permitted if the arrangement gives protection equivalent to that afforded by a double bottom complying with this regulation.
3.1 General
The fore peak and other compartments located forward of the collision bulkhead shall not be arranged for the carriage of fuel oil or other flammable products.
```

## SOLAS 1974 Cap. II-1 Regla 26 (Generalidades)

```text
Regla 26 — Generalidades
1 Las máquinas, las calderas y otros recipientes a presión, así como los correspondientes sistemas de tuberías y accesorios, responderán a un proyecto y a una construcción adecuados para el servicio a que estén destinados e irán instalados y protegidos de modo que se reduzca al mínimo todo peligro para las personas que pueda haber a bordo, considerándose en este sentido como proceda las piezas móviles, las superficies calientes y otros riesgos. En el proyecto se tendrán en cuenta los materiales de construcción utilizados, los fines a que el equipo esté destinado, las condiciones de trabajo a que habrá de estar sometido y las condiciones ambientales de a bordo.
2 La Administración prestará atención especial a la seguridad funcional de los elementos esenciales de propulsión montados como componentes únicos y podrá exigir que el buque tenga una fuente independiente de potencia propulsora que le permita alcanzar una velocidad normal de navegación, sobre todo si no se ajusta a una disposición clásica.
3 Se proveerán medios que permitan mantener o restablecer el funcionamiento normal de las máquinas propulsoras aun cuando se inutilice una de las máquinas auxiliares esenciales. Se prestará atención especial a los defectos de funcionamiento que puedan darse en: un grupo electrógeno que sirva de fuente de energía eléctrica principal; las fuentes de abastecimiento de vapor; los sistemas proveedores del agua de alimentación de las calderas; los sistemas de alimentación de combustible líquido para calderas o motores; las fuentes de presión del aceite lubricante; las fuentes de presión del agua; una bomba para agua de condensación y los medios destinados a mantener el vacío de los condensadores; los dispositivos mecánicos de abastecimiento de aire para calderas; un compresor y un depósito de aire para fines de arranque o de control; y los medios hidráulicos, neumáticos y eléctricos de mando de las máquinas propulsoras principales, incluidas las hélices de paso variable. No obstante, habida cuenta de las necesarias consideraciones generales de seguridad, la Administración podrá aceptar una reducción parcial en la capacidad propulsora en relación con la necesaria para el funcionamiento normal.
4 Se proveerán medios que aseguren que se puede poner en funcionamiento las máquinas sin ayuda exterior partiendo de la condición de buque apagado.
5 Todas las calderas, todos los componentes de las máquinas y todos los sistemas de vapor, hidráulicos, neumáticos o de cualquier otra índole, así como los accesorios correspondientes, que hayan de soportar presiones internas, serán sometidos a pruebas adecuadas, entre ellas una de presión, antes de que entren en servicio por primera vez.
6 Las máquinas propulsoras principales y todas las máquinas auxiliares esenciales a fines de propulsión y seguridad del buque instaladas a bordo responderán a un proyecto tal que puedan funcionar cuando el buque esté adrizado o cuando esté inclinado hacia cualquiera de ambas bandas con ángulos de escora de 15° como máximo en estado estático y de 22,5° en estado dinámico (de balance) y, a la vez, con una inclinación dinámica (por cabeceo) de 7,5° a proa o popa. La Administración podrá permitir que varíen estos ángulos teniendo en cuenta el tipo, las dimensiones y las condiciones de servicio del buque.
7 Se tomarán las disposiciones oportunas para facilitar la limpieza, la inspección y el mantenimiento de las máquinas principales y auxiliares de propulsión, con inclusión de calderas y recipientes a presión.
8 Se prestará atención especial al proyecto, la construcción y la instalación de los sistemas de las máquinas propulsoras, de modo que ninguna de las vibraciones que puedan producir sea causa de tensiones excesivas en dichas máquinas en las condiciones de servicio normales.
9 Las juntas de dilatación no metálicas de los sistemas de tuberías, si están situadas en un sistema que atraviesa el costado del buque y tanto el punto de penetración como la junta de dilatación no metálica se hallan por debajo de la línea de máxima carga, deberán inspeccionarse en el marco de los reconocimientos prescritos en la Regla I/10 a) y reemplazarse cuando sea necesario o con la frecuencia que recomiende el fabricante.
10 Las instrucciones de uso y mantenimiento de las máquinas del buque y del equipo esencial para el funcionamiento del buque en condiciones de seguridad, así como los planos de dichas máquinas y equipo, estarán redactados en un idioma comprensible para los oficiales y tripulantes que deban entender dicha información para desempeñar sus tareas.
11 Las tuberías de respiración de los tanques de combustible líquido de servicio, los tanques de sedimentación y los tanques de aceite lubricante estarán ubicadas y dispuestas de tal forma que en el caso de que una se rompa ello no entrañe directamente el riesgo de que entre agua de mar o de lluvia. Todo buque nuevo estará provisto de dos tanques de combustible líquido de servicio destinados a cada tipo de combustible utilizado a bordo para la propulsión y los sistemas esenciales, o de medios equivalentes, cuya capacidad mínima de suministro sea de ocho horas para una potencia continua máxima de la planta propulsora y una carga normal de funcionamiento en el mar de la planta electrógena.
```

## SOLAS 1974 Cap. II-1 Regla 13 (fragmento)

```text
Regla 13 — Integridad de los mamparos y disposiciones generales
10 Se instalarán mamparos estancos hasta la cubierta de cierre de los buques de pasaje y la cubierta de francobordo de los buques de carga que separen a proa y a popa el espacio de máquinas de los espacios de carga y de alojamiento. Habrá asimismo instalado un mamparo del pique de popa que será estanco hasta la cubierta de cierre o la cubierta de francobordo. El mamparo del pique de popa podrá, sin embargo, formar bayoneta por debajo de la cubierta de cierre o la cubierta de francobordo, a condición de que con ello no disminuya el grado de seguridad del buque en lo que respecta al compartimentado.
11 En todos los casos, las bocinas irán encerradas en espacios estancos de volumen reducido.
```

---

**Fórmulas reglamentarias de apoyo**

```text
DNV Pt.3 Ch.2 Sec.3 [2.3]: Altura de doble fondo h_DB = 1000 · B / 20, con límites h_DB,min = 0,76 m y h_DB,max = 2,00 m.
DNV Pt.4 Ch.6 Sec.3: Dimensionamiento genérico de tanques V = L · B_ef · H · η, con η = 0,92 para doble fondo y η = 0,88 para tanques de ala.
```
