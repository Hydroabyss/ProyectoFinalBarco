# Integración Avanzada con AutoCAD y Modelos 3D de Motores Marinos

## 📋 Descripción General

Este proyecto incluye herramientas profesionales para la generación automática de planos de sala de máquinas con integración opcional a AutoCAD mediante COM API.

## 🎯 Características Principales

### 1. Plano Longitudinal Detallado (Multiplataforma)

**Archivo:** `herramientas/generar_plano_longitudinal_detallado.py`

Genera planos DXF profesionales con:

- ✅ **Estructura del casco:**

  - Doble fondo compartimentado (altura 1.2m según DNV)
  - Mamparos estancos con refuerzos estructurales
  - Cubiertas: tanques (2.0m), plataforma baja (3.2m), plataforma alta (5.5m), principal (7.9m)
  - Refuerzos: palmejares horizontales y refuerzos verticales

- ✅ **Sistema de propulsión completo:**

  - Eje propulsor Ø0.45m con línea central
  - Bocina (stern tube) de 8.5m con Ø0.80m
  - Chumaceras (shaft bearings) en 2 posiciones
  - Hélice de 4 palas con Ø4.20m
  - Timón compensado tipo semi-balanced

- ✅ **Equipos principales:**

  - Motor MAN 6S50ME-C (8500 kW @ 127 RPM)
    - 6 cilindros representados
    - Fundación estructural
    - Línea de cigüeñal
  - 3x Generadores CAT 3512C (500 kW c/u)

- ✅ **Tanques y sistemas:**

  - Tanques de servicio diario (FO y LO)
  - Tuberías principales (combustible Ø200, agua de mar Ø300)
  - Sistema de ventilación

- ✅ **Documentación técnica:**
  - Sección transversal de referencia
  - Leyenda completa con datos técnicos
  - Cotas principales
  - 24 capas organizadas por color y tipo de línea

**Uso:**

```bash
python herramientas/generar_plano_longitudinal_detallado.py
```

**Salida:** `salidas/disposicion_general/Plano_Longitudinal_Sala_Maquinas_Detallado.dxf`

---

### 2. Integración AutoCAD COM (Solo Windows)

**Archivo:** `herramientas/integracion_autocad_motores.py`

Módulo de integración con AutoCAD mediante COM API para:

- 🔌 **Conexión directa con AutoCAD:**

  ```python
  from integracion_autocad_motores import AutoCADEngineIntegration

  autocad = AutoCADEngineIntegration()
  if autocad.connect_autocad():
      # Trabajar con AutoCAD
      autocad.create_layer("MOTOR_PRINCIPAL", color=2)
      autocad.add_text("MAN 6S50ME-C", (10.0, 5.0, 2.0), height=0.3)
  ```

- 📦 **Biblioteca de motores marinos:**

  - MAN 6S50ME-C (8500 kW)
  - Wärtsilä 16V26 (5440 kW)
  - CAT 3512C (500 kW)

  Con datos completos:

  - Dimensiones (L x W x H)
  - Peso y potencia
  - SFOC (consumo específico)
  - Requisitos de fundación
  - Referencias a modelos 3D (STEP/IGES)

- 🏗️ **Diseñador de sala de máquinas:**

  ```python
  from integracion_autocad_motores import EngineRoomDesigner

  designer = EngineRoomDesigner()
  summary = designer.generate_complete_engine_room(
      main_engine_model="MAN_6S50ME-C",
      generator_model="CAT_3512C",
      room_length=15.0,
      room_beam=15.99,
      room_height=7.90,
  )
  ```

**Requisitos (Windows únicamente):**

```bash
pip install pywin32
```

**Nota:** En macOS, el módulo exporta las configuraciones a JSON para referencia.

---

## 📊 Configuraciones de Motores Disponibles

### Motor Principal: MAN 6S50ME-C

```
Fabricante: MAN Energy Solutions
Potencia: 8500 kW @ 127 RPM
Cilindros: 6 en línea
Dimensiones: 8.5 x 3.2 x 4.1 m (L x W x H)
Peso: 145 toneladas
SFOC: 185 g/kWh @ 90% carga
Fundación: 600mm espesor, HEB400, tornillos M36x300
```

### Generadores: CAT 3512C (x3)

```
Fabricante: Caterpillar
Potencia: 500 kW @ 1800 RPM (c/u)
Potencia total: 1500 kW
Cilindros: 12 en V
Dimensiones: 3.5 x 1.8 x 2.6 m (L x W x H)
Peso: 12.5 toneladas (c/u)
SFOC: 201.5 g/kWh @ 75% carga
```

### Alternativa: Wärtsilä 16V26

```
Fabricante: Wärtsilä
Potencia: 5440 kW @ 1000 RPM
Cilindros: 16 en V
Dimensiones: 6.8 x 2.9 x 3.6 m
Peso: 98 toneladas
SFOC: 192 g/kWh
```

---

## 🛠️ Estructura de Archivos Generados

```
proyecto_final_barcos/
├── herramientas/
│   ├── generar_plano_longitudinal_detallado.py   # Generador DXF detallado
│   ├── integracion_autocad_motores.py             # COM API AutoCAD
│   └── calculos_combustible_optimizados.py        # Cálculos con datos reales
├── salidas/
│   └── disposicion_general/
│       ├── Plano_Longitudinal_Sala_Maquinas_Detallado.dxf
│       └── README_Plano_Longitudinal.md
└── engine_configurations.json                     # Configuraciones exportadas
```

---

## 🎨 Capas del Plano DXF

| Capa                | Color | Linetype   | Uso                          |
| ------------------- | ----- | ---------- | ---------------------------- |
| CASCO               | 1     | Continuous | Perfil del casco             |
| ESTRUCTURA          | 3     | Continuous | Elementos estructurales      |
| MAMPAROS            | 3     | Continuous | Mamparos estancos            |
| REFUERZOS           | 8     | Continuous | Palmejares y refuerzos       |
| CUBIERTAS           | 4     | Continuous | Cubiertas y plataformas      |
| EJE_PROPULSOR       | 1     | CENTER     | Línea de eje y eje propulsor |
| BOCINA              | 5     | Continuous | Stern tube y chumaceras      |
| HELICE              | 2     | Continuous | Hélice de 4 palas            |
| TIMON               | 6     | Continuous | Timón compensado             |
| MOTOR_PRINCIPAL     | 2     | Continuous | Motor MAN 6S50ME-C           |
| FUNDACION_MOTOR     | 8     | Continuous | Fundación del motor          |
| GENERADORES         | 6     | Continuous | 3x CAT 3512C                 |
| DOBLE_FONDO         | 30    | Continuous | Compartimentos doble fondo   |
| TANQUES_SERVICIO    | 40    | DASHED     | Tanques FO y LO diarios      |
| TUBERIAS            | 4     | DASHED     | Tuberías principales         |
| SECCION_TRANSVERSAL | 1     | Continuous | Vista transversal referencia |
| TEXTOS              | 0     | Continuous | Etiquetas y anotaciones      |
| COTAS               | 0     | Continuous | Dimensiones                  |

---

## 📐 Datos Técnicos del Buque

```
Eslora entre perpendiculares (LPP): 105.2 m
Manga (B): 15.99 m
Puntal (D): 7.90 m
Calado de diseño (T): 6.20 m
Coeficiente de bloque (Cb): 0.7252

Sala de Máquinas:
- Posición: 8.20 - 23.20 m desde PP popa
- Longitud: 15.0 m
- Altura doble fondo: 1.20 m (DNV Pt.3 Ch.2)
- Ancho doble costado: 1.80 m por banda

Sistema Propulsivo:
- Eje propulsor: Ø0.45 m
- Hélice: Ø4.20 m, 4 palas, paso fijo
- Timón: 5.50 m altura, 2.80 m cuerda
- Bocina: 8.5 m longitud, Ø0.80 m

Capacidad Combustible:
- Tanques doble fondo: 149.96 m³
- Tanques wing (2x): 113.31 m³ c/u
- Total: 377.6 m³ (≈304 toneladas)
- Autonomía: 2,755 NM @ 14.5 nudos
```

---

## 🔧 Instalación y Uso

### Requisitos Base (macOS/Linux/Windows)

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install ezdxf
```

### Generar Plano Detallado

```bash
python herramientas/generar_plano_longitudinal_detallado.py
```

### Integración AutoCAD (Solo Windows)

```bash
# Instalar pywin32
pip install pywin32

# Ejecutar integración
python herramientas/integracion_autocad_motores.py
```

### Exportar Configuraciones

El script `integracion_autocad_motores.py` genera automáticamente:

```json
// engine_configurations.json
{
  "MAN_6S50ME-C": {
    "model": "6S50ME-C",
    "manufacturer": "MAN Energy Solutions",
    "power_kw": 8500.0,
    "rpm": 127.0,
    "dimensions_m": {
      "length": 8.5,
      "width": 3.2,
      "height": 4.1
    },
    "foundation": {
      "thickness_mm": 600.0,
      "reinforcement": "HEB400",
      "bolts": "M36x300"
    }
  }
}
```

---

## 🌐 API de Fabricantes (Conceptual)

El módulo incluye estructura para integración con APIs de fabricantes:

```python
class MarineEngineAPI:
    """Integración con APIs de fabricantes (ejemplo conceptual)"""

    def get_engine_3d_model(self, engine_model: str):
        """Descargar modelo 3D desde fabricante"""
        # Wärtsilä, MAN, Caterpillar tienen portales técnicos
        pass

    def get_engine_technical_data(self, engine_model: str):
        """Obtener hojas de datos actualizadas"""
        pass
```

**Nota:** Las APIs reales requieren credenciales y acuerdos con fabricantes.

---

## 📚 Referencias Técnicas

- **DNV-RU-SHIP Pt.3 Ch.2:** Diseño estructural (dobles fondos, refuerzos)
- **ISO 3046-1:** Correcciones ambientales para motores
- **Wärtsilä Engine Catalogue:** Curvas SFOC reales
- **MAN Diesel & Turbo:** Especificaciones motores de dos tiempos
- **Caterpillar Marine:** Datos generadores diésel

---

## ⚙️ Workflow Completo

### 1. Generar Plano Base (macOS/Linux/Windows)

```bash
python herramientas/generar_plano_longitudinal_detallado.py
```

### 2. Abrir en Visor CAD

- **Windows:** AutoCAD, DraftSight, LibreCAD
- **macOS:** LibreCAD, QCAD
- **Online:** Autodesk Viewer, ShareCAD

### 3. Integración Avanzada (Solo Windows + AutoCAD)

```python
from integracion_autocad_motores import EngineRoomDesigner

designer = EngineRoomDesigner()

# Conectar AutoCAD
if designer.autocad.connect_autocad():

    # Crear capas
    designer.setup_layers()

    # Insertar motor principal
    designer.insert_main_engine(
        "MAN_6S50ME-C",
        position=(12.0, 0.0, 1.5)  # x, y, z en metros
    )

    # Insertar generadores
    for i in range(3):
        designer.insert_main_engine(
            "CAT_3512C",
            position=(10.0 + i*4.5, -3.0, 1.2)
        )
```

### 4. Importar Modelos 3D (Si disponibles)

```python
# Modelos STEP/IGES desde fabricantes
autocad.import_step_file("models/man_6s50me_c.step")
```

---

## 🎓 Casos de Uso

### Diseño Preliminar

- Usar generador DXF para layout inicial
- Validar espaciado de equipos
- Calcular centros de gravedad

### Ingeniería de Detalle

- Integrar con AutoCAD para modelado 3D
- Añadir sistemas de tuberías completos
- Generar isométricos

### Documentación

- Exportar planos a PDF
- Generar listas de materiales
- Crear manuales técnicos

---

## 🚀 Mejoras Futuras

- [ ] Soporte para modelos 3D nativos (STEP/IGES)
- [ ] Integración con Maxsurf para hidrostática
- [ ] Cálculo automático de tuberías
- [ ] Generación de secciones transversales múltiples
- [ ] Exportación a formatos BIM (IFC)
- [ ] API REST para acceso remoto
- [ ] Interfaz web para configuración

---

## 📞 Soporte

Para consultas técnicas sobre:

- **Generación DXF:** Revisar `generar_plano_longitudinal_detallado.py`
- **Integración AutoCAD:** Consultar documentación COM API de Autodesk
- **Datos de motores:** Verificar catálogos de fabricantes

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico de ingeniería naval.

---

**Generado:** 6 de noviembre de 2025  
**Versión:** 2.0 - Planos Detallados con Integración AutoCAD
