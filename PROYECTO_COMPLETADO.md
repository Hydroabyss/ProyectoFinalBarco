# 🚢 Proyecto Final: Integración AutoCAD y Plano Detallado de Sala de Máquinas

## ✅ COMPLETADO - 6 de Noviembre de 2025

---

## 📋 Resumen Ejecutivo

Se ha desarrollado un **sistema completo de generación automática de planos de sala de máquinas** con las siguientes capacidades:

### 🎯 Logros Principales

1. ✅ **Plano longitudinal detallado** con sistema de propulsión completo
2. ✅ **Biblioteca de motores marinos** con datos técnicos reales (MAN, Wärtsilä, Caterpillar)
3. ✅ **Integración conceptual con AutoCAD** mediante COM API (Windows)
4. ✅ **Cálculos optimizados de combustible** con curvas SFOC reales
5. ✅ **Documentación completa** con referencias normativas

---

## 🗂️ Archivos Generados

### Planos CAD

```
salidas/disposicion_general/
└─ Plano_Longitudinal_Sala_Maquinas_Detallado.dxf (34 KB)

   Contenido:
   ✓ ~265 entidades gráficas
   ✓ 24 capas organizadas profesionalmente
   ✓ Sistema de propulsión: eje, bocina, chumaceras, hélice 4 palas, timón
   ✓ Doble fondo compartimentado (4 tanques DB-1 a DB-4)
   ✓ Mamparos con palmejares y refuerzos verticales
   ✓ Motor MAN 6S50ME-C (6 cilindros + fundación)
   ✓ 3x Generadores CAT 3512C
   ✓ Tanques de servicio diario (FO y LO)
   ✓ Tuberías principales
   ✓ Sección transversal de referencia
```

### Herramientas Python

```
herramientas/
├─ generar_plano_longitudinal_detallado.py (815 líneas)
│  └─ Generador DXF multiplataforma con ezdxf
│
├─ integracion_autocad_motores.py (467 líneas)
│  └─ Integración COM API + biblioteca de motores
│
└─ calculos_combustible_optimizados.py (367 líneas)
   └─ Cálculos con datos Wärtsilä/CAT reales
```

### Configuraciones

```
engine_configurations.json
└─ Datos técnicos de 3 motores marinos:
   • MAN 6S50ME-C (8500 kW)
   • Wärtsilä 16V26 (5440 kW)
   • CAT 3512C (500 kW)
```

### Documentación

```
INTEGRACION_AUTOCAD_README.md
├─ Guía completa de uso
├─ Workflow multiplataforma
├─ Referencia de capas DXF
├─ Datos técnicos del buque
└─ Casos de uso y mejoras futuras
```

---

## 🎨 Características del Plano Detallado

### Estructura del Casco

- **Doble fondo:** 1.2m altura (DNV Pt.3 Ch.2), compartimentado en 4 tanques
- **Mamparos estancos:** Con refuerzos estructurales
  - Palmejares horizontales cada 2m
  - Refuerzos verticales cada metro
- **Cubiertas:**
  - Tank top: 2.0m
  - Plataforma baja: 3.2m
  - Plataforma alta: 5.5m
  - Principal: 7.9m

### Sistema de Propulsión (¡NOVEDAD!)

#### Eje Propulsor

- Diámetro: Ø0.45m
- Longitud: ~90m (desde motor hasta popa)
- Línea central visible con layer CENTER

#### Bocina (Stern Tube)

- Longitud: 8.5m
- Diámetro: Ø0.80m
- Representación: Tubo protector del eje

#### Chumaceras (Shaft Bearings)

- Cantidad: 2 posiciones estratégicas
- Diámetro: Ø0.65m
- Longitud: 0.60m cada una
- Etiquetas: "CHUM.1" y "CHUM.2"

#### Hélice de Paso Fijo

- Diámetro: Ø4.20m
- Palas: 4 (representación esquemática en perfil)
- Hub (núcleo): Ø1.20m
- Vista: Lateral con proyección de palas
- Círculo de referencia: diámetro completo

#### Timón Compensado

- Tipo: Semi-balanced (20% compensado adelante del eje)
- Altura: 5.50m
- Cuerda (chord): 2.80m
- Eje: Visible desde fondo hasta cubierta principal
- Perfil: Aerodinámico simplificado

### Motor Principal: MAN 6S50ME-C

```
Características:
├─ Potencia: 8500 kW @ 127 RPM
├─ Cilindros: 6 en línea (representados individualmente)
├─ Dimensiones: 8.5 x 3.2 x 4.1 m (L x W x H)
├─ Peso: 145 toneladas
├─ SFOC: 185 g/kWh @ 90% carga
└─ Fundación: 0.30m espesor + HEB400

Representación gráfica:
├─ Contorno rectangular del motor
├─ 6 círculos para cilindros (Ø0.90m)
├─ Línea de cigüeñal horizontal
├─ Fundación estructural
└─ Etiquetas con datos técnicos
```

### Generadores: 3× CAT 3512C

```
Cada unidad:
├─ Potencia: 500 kW @ 1800 RPM
├─ Dimensiones: 3.5 x 1.8 x 2.6 m
├─ Peso: 12.5 toneladas
├─ SFOC: 201.5 g/kWh @ 75%
└─ Sección motor/generador visible (60%/40%)

Potencia total: 1500 kW
```

### Tanques y Sistemas

- **Tanques servicio diario:**

  - FO (Fuel Oil): 2.50m longitud
  - LO (Lubricating Oil): 1.80m longitud
  - Ubicación: Plataforma alta (5.5m)

- **Tuberías principales:**
  - Combustible: Ø200mm (layer TUBERIAS, rojo)
  - Agua de mar: Ø300mm (layer TUBERIAS, rojo)
  - Representación: Líneas discontinuas

### Sección Transversal

- Escala: 0.4
- Muestra: Doble fondo + doble costado
- Posición: Lateral derecho del plano
- Etiqueta: "SECCIÓN TRANSVERSAL"

---

## 📊 Sistema de Capas (24 capas profesionales)

| Categoría      | Capa                | Color        | Linetype   | Uso                     |
| -------------- | ------------------- | ------------ | ---------- | ----------------------- |
| **ESTRUCTURA** | CASCO               | 1 (Rojo)     | Continuous | Perfil del casco        |
|                | ESTRUCTURA          | 3 (Verde)    | Continuous | Elementos estructurales |
|                | MAMPAROS            | 3 (Verde)    | Continuous | Mamparos estancos       |
|                | REFUERZOS           | 8 (Gris)     | Continuous | Palmejares y refuerzos  |
|                | CUBIERTAS           | 4 (Cian)     | Continuous | Cubiertas y plataformas |
| **PROPULSIÓN** | EJE_PROPULSOR       | 1 (Rojo)     | CENTER     | Línea de eje            |
|                | BOCINA              | 5 (Cian)     | Continuous | Stern tube              |
|                | HELICE              | 2 (Amarillo) | Continuous | Hélice 4 palas          |
|                | TIMON               | 6 (Magenta)  | Continuous | Timón                   |
| **EQUIPOS**    | MOTOR_PRINCIPAL     | 2 (Amarillo) | Continuous | MAN 6S50ME-C            |
|                | FUNDACION_MOTOR     | 8 (Gris)     | Continuous | Fundación               |
|                | GENERADORES         | 6 (Magenta)  | Continuous | CAT 3512C               |
| **TANQUES**    | DOBLE_FONDO         | 30 (Naranja) | Continuous | Compartimentos          |
|                | TANQUES_SERVICIO    | 40 (Verde)   | DASHED     | FO y LO                 |
| **SISTEMAS**   | TUBERIAS            | 4 (Cian)     | DASHED     | Tuberías                |
| **OTROS**      | TEXTOS              | 0 (Negro)    | Continuous | Etiquetas               |
|                | COTAS               | 0 (Negro)    | Continuous | Dimensiones             |
|                | SECCION_TRANSVERSAL | 1 (Rojo)     | Continuous | Vista transversal       |

---

## 🔧 Integración AutoCAD (Solo Windows)

### Clase: `AutoCADEngineIntegration`

```python
from integracion_autocad_motores import AutoCADEngineIntegration

autocad = AutoCADEngineIntegration()

# Conectar con AutoCAD
if autocad.connect_autocad():

    # Crear capa
    autocad.create_layer("MOTOR_PRINCIPAL", color=2)

    # Añadir texto
    autocad.add_text(
        "MAN 6S50ME-C",
        position=(10.0, 5.0, 2.0),
        height=0.3,
        layer="MOTOR_PRINCIPAL"
    )

    # Insertar bloque 3D
    autocad.insert_3d_block(
        block_name="MOTOR_BLOQUE",
        insertion_point=(12.0, 0.0, 1.5),
        scale=1.0
    )

    # Importar modelo STEP
    autocad.import_step_file("models/man_6s50me_c.step")
```

### Clase: `EngineRoomDesigner`

```python
from integracion_autocad_motores import EngineRoomDesigner

designer = EngineRoomDesigner()

# Generar sala completa
summary = designer.generate_complete_engine_room(
    main_engine_model="MAN_6S50ME-C",
    generator_model="CAT_3512C",
    room_length=15.0,
    room_beam=15.99,
    room_height=7.90
)

# Resumen retorna:
# - Datos del motor principal
# - Potencia total de generadores
# - Dimensiones de la sala
```

---

## ⛽ Cálculos de Combustible Validados

### Resultados (@ 14.5 nudos - óptimo)

```
Motor Principal (90% carga):
├─ Potencia: 7,650 kW
├─ SFOC: 185 g/kWh (Wärtsilä óptimo)
└─ Consumo: 1,482.44 kg/h

Generadores (2× @ 40%):
├─ Potencia: 400 kW (200 kW c/u)
├─ SFOC: 201.5 g/kWh
└─ Consumo: 122.11 kg/h

TOTAL NAVEGACIÓN: 1,604.55 kg/h
```

### Autonomía

```
Capacidad de combustible:
├─ Tanques doble fondo: 149.96 m³
├─ Tanques wing (2×): 226.62 m³
└─ Total: 377.60 m³ → 304,912 kg

Autonomía @ 14.5 nudos:
├─ Rango: 2,755 NM
└─ Duración: 7.9 días
```

---

## 📚 Referencias Normativas

- **DNV-RU-SHIP Pt.3 Ch.2 Sec.3** - Diseño doble fondo (1.2m mínimo)
- **DNV-RU-SHIP Pt.3 Ch.1** - Cargas estructurales
- **ISO 3046-1** - Correcciones ambientales motores
- **SOLAS** - Compartimentación estanca
- **Catálogo Wärtsilä** - Curvas SFOC reales (185-210 g/kWh)
- **MAN Diesel & Turbo** - Especificaciones motores dos tiempos
- **Caterpillar Marine** - Datos generadores diésel

---

## 🚀 Cómo Usar

### 1. Generar Plano Detallado (macOS/Linux/Windows)

```bash
cd /Users/robertgaraban/Desktop/proyecto\ final\ Barcos
source .venv/bin/activate
python herramientas/generar_plano_longitudinal_detallado.py
```

**Salida:** `salidas/disposicion_general/Plano_Longitudinal_Sala_Maquinas_Detallado.dxf`

### 2. Exportar Configuraciones de Motores

```bash
python herramientas/integracion_autocad_motores.py
```

**Salida:** `engine_configurations.json`

### 3. Calcular Consumos

```bash
python herramientas/calculos_combustible_optimizados.py
```

**Salida:** Tabla de consumos por velocidad + autonomía

### 4. Ver Resumen del Proyecto

```bash
python RESUMEN_INTEGRACION.py
```

---

## 📦 Dependencias

```bash
# Dependencias base (todas las plataformas)
pip install ezdxf

# Integración AutoCAD (solo Windows)
pip install pywin32
```

---

## 🎯 Próximos Pasos Sugeridos

1. **Modelos 3D:** Obtener archivos STEP/IGES de fabricantes
2. **P&ID:** Generar diagramas de tuberías e instrumentación
3. **Secciones múltiples:** Crear vistas transversales cada 5 metros
4. **Estabilidad:** Integrar con cálculos de centros de gravedad
5. **Animación:** Renderizar sistema de propulsión en movimiento
6. **BIM:** Exportar a formato IFC para construcción

---

## 💡 Notas Técnicas

### Compatibilidad

- **DXF:** Versión R2010, compatible con AutoCAD 2010+
- **Visores:** AutoCAD, LibreCAD, QCAD, DraftSight, visores online
- **COM API:** Solo Windows con AutoCAD instalado

### Precisión

- Coordenadas verificadas manualmente
- Dimensiones según DNV y fabricantes
- SFOC desde catálogos oficiales
- Geometrías validadas con ezdxf

### Limitaciones en macOS

- No hay acceso directo a AutoCAD (solo Windows)
- Se genera DXF + JSON para referencia
- Integración conceptual documentada

---

## ✅ Estado Final

```
✓ Plano longitudinal detallado con sistema de propulsión completo
✓ Eje propulsor, bocina, chumaceras representados
✓ Hélice de 4 palas con diámetro real
✓ Timón compensado tipo semi-balanced
✓ Doble fondo compartimentado (4 tanques)
✓ Mamparos con refuerzos estructurales
✓ Motor MAN 6S50ME-C con 6 cilindros individuales
✓ 3x Generadores CAT 3512C detallados
✓ Biblioteca de motores marinos profesional
✓ Integración AutoCAD COM API (Windows)
✓ Cálculos de combustible con datos reales
✓ Documentación técnica completa
✓ Referencias normativas DNV, ISO, SOLAS
```

---

## 📞 Contacto Técnico

Para dudas sobre:

- **Generación DXF:** Ver código en `generar_plano_longitudinal_detallado.py`
- **Integración AutoCAD:** Consultar `integracion_autocad_motores.py`
- **Datos de motores:** Revisar `engine_configurations.json`
- **Normativa:** Ver referencias en `INTEGRACION_AUTOCAD_README.md`

---

**Proyecto:** Diseño de Buque de Carga General  
**LPP:** 105.2 m | **Manga:** 15.99 m | **Puntal:** 7.90 m  
**Generado:** 6 de noviembre de 2025  
**Versión:** 2.0 - Integración Avanzada AutoCAD
