"""
Generador de Plano Longitudinal MEJORADO de Sala de Máquinas
============================================================

Versión profesional con:
- Doble fondo detallado con compartimentación
- Mamparos estancos con refuerzos estructurales
- Eje propulsor con bocina y chumaceras
- Hélice de paso fijo (4 palas)
- Timón compensado
- Motor principal con fundación
- Tanques de servicio diario
- Sistema de tuberías principales
- Sección transversal de referencia
- Datos técnicos basados en Wärtsilä/MAN

Basado en configuraciones reales de buques petroleros.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence
import math

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment

from utils_dxf import save_dxf_with_extents


# ===== CONFIGURACIÓN DEL PROYECTO =====
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "salidas" / "disposicion_general"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DXF_OUTPUT = OUTPUT_DIR / "Plano_Longitudinal_Sala_Maquinas_Detallado.dxf"

# ===== DIMENSIONES PRINCIPALES DEL BUQUE =====
LPP = 105.2  # m eslora entre perpendiculares
BEAM = 15.99  # m manga
DEPTH = 7.90  # m puntal
DRAFT = 6.20  # m calado de diseño

# ===== SALA DE MÁQUINAS =====
ENGINE_ROOM_START = 8.20  # m desde PP de popa
ENGINE_ROOM_END = 23.20  # m desde PP de popa
ENGINE_ROOM_LENGTH = ENGINE_ROOM_END - ENGINE_ROOM_START  # 15.0 m

# ===== ESTRUCTURA DETALLADA =====
DOUBLE_BOTTOM_HEIGHT = 1.20  # m altura según DNV
DOUBLE_SIDE_WIDTH = 1.80  # m ancho por banda
TANK_TOP_HEIGHT = 2.00  # m cubierta de tanques
MAIN_DECK_HEIGHT = DEPTH  # m cubierta principal
PLATFORM_1_HEIGHT = 3.20  # m plataforma baja
PLATFORM_2_HEIGHT = 5.50  # m plataforma alta

# Mamparos
BULKHEAD_THICKNESS = 0.12  # m espesor mamparo estanco

# ===== MOTOR PRINCIPAL  Wärtsilä 16V26 =====
MOTOR_LENGTH = 8.50  # m
MOTOR_WIDTH = 3.20  # m
MOTOR_HEIGHT = 4.00  # m
MOTOR_START = ENGINE_ROOM_START + 4.00
MOTOR_BASE_HEIGHT = DOUBLE_BOTTOM_HEIGHT + 0.30  # sobre fundación
MOTOR_CYLINDERS = 6
MOTOR_POWER_KW = 8500
MOTOR_RPM = 127

# Fundación motor
FOUNDATION_HEIGHT = 0.30  # m
FOUNDATION_WIDTH = MOTOR_WIDTH + 0.80  # m

# ===== EJE PROPULSOR =====
SHAFT_DIAMETER = 0.45  # m diámetro eje
SHAFT_START = MOTOR_START + MOTOR_LENGTH  # desde motor
SHAFT_END = LPP + 2.0  # sale del casco
SHAFT_CENTER_HEIGHT = MOTOR_BASE_HEIGHT + MOTOR_HEIGHT * 0.5  # altura línea eje

# Bocina (stern tube)
STERN_TUBE_START = LPP - 8.0
STERN_TUBE_END = LPP + 0.5
STERN_TUBE_DIAMETER = 0.80  # m

# Chumaceras (shaft bearings)
BEARING_1_POS = SHAFT_START + 1.0
BEARING_2_POS = STERN_TUBE_START + 2.0
BEARING_LENGTH = 0.60  # m
BEARING_DIAMETER = 0.65  # m

# ===== HÉLICE =====
PROPELLER_POS = LPP + 1.80  # m desde PP popa
PROPELLER_DIAMETER = 4.20  # m
PROPELLER_BLADES = 4
PROPELLER_HUB_DIAMETER = 1.20  # m

# ===== TIMÓN =====
RUDDER_POS = LPP + 3.50  # m desde PP popa
RUDDER_HEIGHT = 5.50  # m
RUDDER_CHORD = 2.80  # m (longitud del perfil)
RUDDER_THICKNESS = 0.30  # m espesor máximo

# ===== GENERADORES AUXILIARES =====
GEN1_START = ENGINE_ROOM_START + 1.50
GEN2_START = GEN1_START + 4.50
GEN3_START = GEN2_START + 4.50
GEN_LENGTH = 3.50  # m
GEN_WIDTH = 1.80  # m
GEN_HEIGHT = 2.60  # m
GEN_BASE_HEIGHT = DOUBLE_BOTTOM_HEIGHT

# ===== TANQUES DE SERVICIO DIARIO =====
SERVICE_TANK_FO_START = ENGINE_ROOM_END - 4.0
SERVICE_TANK_FO_LENGTH = 2.50
SERVICE_TANK_FO_HEIGHT = 1.80
SERVICE_TANK_LO_START = SERVICE_TANK_FO_START + SERVICE_TANK_FO_LENGTH + 0.50
SERVICE_TANK_LO_LENGTH = 1.80

# ===== ESCALA Y OFFSETS =====
SCALE = 1.0
MARGIN = 3.0

# ===== EXTENSOS POR DEFECTO PARA CONFIGURACIÓN AUTOCAD =====
DEFAULT_X_MIN = ENGINE_ROOM_START - 5.0
DEFAULT_X_MAX = RUDDER_POS + RUDDER_CHORD + 5.0
DEFAULT_Y_MIN = -3.5
DEFAULT_Y_MAX = MAIN_DECK_HEIGHT + 3.0
def _add_text(
    msp: ezdxf.layouts.Modelspace,
    text: str,
    position: Sequence[float],
    *,
    height: float = 0.25,
    layer: str = "TEXTOS",
    align: TextEntityAlignment = TextEntityAlignment.LEFT,
    rotation: float = 0.0,
) -> None:
    """Añade texto con rotación opcional y COLOR ROJO OSCURO VISIBLE."""
    entity = msp.add_text(text, dxfattribs={
        "height": height,
        "layer": layer,
        "color": 1  # ROJO - MUY VISIBLE en cualquier fondo
    })
    entity.set_placement(position, align=align)
    if rotation != 0.0:
        entity.dxf.rotation = rotation


def _create_layers(doc: ezdxf.EzdxfDocument) -> None:
    """Crea capas profesionales optimizadas para visibilidad."""
    layers = {
        # Capas estructurales
        "CASCO": (1, "Continuous", 50),  # (color, linetype, lineweight)
        "ESTRUCTURA": (3, "Continuous", 35),
        "MAMPAROS": (3, "Continuous", 40),
        "CUBIERTAS": (4, "Continuous", 30),
        "REFUERZOS": (5, "Continuous", 18),  # CAMBIADO de 8 a 5 (cyan) - MÁS VISIBLE
        # Propulsión
        "EJE_PROPULSOR": (1, "CENTER", 35),
        "HELICE": (2, "Continuous", 40),
        "TIMON": (6, "Continuous", 35),
        "BOCINA": (5, "Continuous", 25),
        # Equipos
        "MOTOR_PRINCIPAL": (2, "Continuous", 40),
        "FUNDACION_MOTOR": (9, "Continuous", 25),  # CAMBIADO de 8 a 9 (gris claro) - MÁS VISIBLE
        "GENERADORES": (6, "Continuous", 30),
        "EQUIPOS_AUX": (5, "Continuous", 20),
        # Tanques
        "DOBLE_FONDO": (30, "Continuous", 25),
        "TANQUES_SERVICIO": (40, "DASHED", 20),
        "TANQUES_WING": (40, "DASHED", 18),
        # Sistemas
        "TUBERIAS": (4, "DASHED", 13),
        "VENTILACION": (6, "DASHED", 13),  # CAMBIADO de 7 a 6 (magenta) - MÁS VISIBLE
        # Anotaciones - ROJO PARA MÁXIMA VISIBILIDAD
        "TEXTOS": (1, "Continuous", 13),  # ROJO - visible en blanco y oscuro
        "COTAS": (1, "Continuous", 13),   # ROJO
        "LEYENDA": (1, "Continuous", 13), # ROJO
        "EJES": (9, "CENTER", 13),  # CAMBIADO de 8 a 9 (gris claro) - MÁS VISIBLE
        "SECCION_TRANSVERSAL": (1, "Continuous", 25),
    }
    
    for name, (color, linetype, lineweight) in layers.items():
        if name in doc.layers:
            try:
                doc.layers.remove(name)
            except:
                pass
        layer = doc.layers.add(name=name)
        layer.color = color
        layer.dxf.linetype = linetype
        layer.dxf.lineweight = lineweight


def draw_detailed_hull_profile(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja perfil detallado del casco con doble fondo estructurado."""
    # Línea base (quilla)
    msp.add_line(
        (ENGINE_ROOM_START, 0.0),
        (ENGINE_ROOM_END, 0.0),
        dxfattribs={"layer": "CASCO"},
    )
    
    # Cubierta principal
    msp.add_line(
        (ENGINE_ROOM_START, MAIN_DECK_HEIGHT),
        (ENGINE_ROOM_END, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "CUBIERTAS"},
    )
    
    # Cubierta de tanques (tank top)
    msp.add_line(
        (ENGINE_ROOM_START, TANK_TOP_HEIGHT),
        (ENGINE_ROOM_END, TANK_TOP_HEIGHT),
        dxfattribs={"layer": "CUBIERTAS"},
    )
    
    # Plataformas intermedias
    for height, label in [(PLATFORM_1_HEIGHT, "PLAT. BAJA"), (PLATFORM_2_HEIGHT, "PLAT. ALTA")]:
        msp.add_line(
            (ENGINE_ROOM_START, height),
            (ENGINE_ROOM_END, height),
            dxfattribs={"layer": "CUBIERTAS"},
        )
        _add_text(msp, label, (ENGINE_ROOM_START + 0.5, height + 0.2), height=0.20)
    
    # Costados del casco
    for x in [ENGINE_ROOM_START, ENGINE_ROOM_END]:
        msp.add_line((x, 0.0), (x, MAIN_DECK_HEIGHT), dxfattribs={"layer": "CASCO"})


def draw_detailed_double_bottom(msp: ezdxf.layouts.Modelspace) -> None:
    """Doble fondo con compartimentación detallada."""
    # Contorno principal
    db_outline = [
        (ENGINE_ROOM_START, 0.0),
        (ENGINE_ROOM_START, DOUBLE_BOTTOM_HEIGHT),
        (ENGINE_ROOM_END, DOUBLE_BOTTOM_HEIGHT),
        (ENGINE_ROOM_END, 0.0),
    ]
    msp.add_lwpolyline(db_outline, dxfattribs={"layer": "DOBLE_FONDO", "closed": True})
    
    # Divisiones longitudinales (fondos internos)
    centerline_offset_1 = DOUBLE_BOTTOM_HEIGHT * 0.35
    centerline_offset_2 = DOUBLE_BOTTOM_HEIGHT * 0.70
    
    for y in [centerline_offset_1, centerline_offset_2]:
        msp.add_line(
            (ENGINE_ROOM_START, y),
            (ENGINE_ROOM_END, y),
            dxfattribs={"layer": "DOBLE_FONDO"},
        )
    
    # Divisiones transversales (mamparos internos tanques)
    num_compartments = 4
    compartment_length = ENGINE_ROOM_LENGTH / num_compartments
    
    for i in range(1, num_compartments):
        x = ENGINE_ROOM_START + i * compartment_length
        msp.add_line(
            (x, 0.0),
            (x, DOUBLE_BOTTOM_HEIGHT),
            dxfattribs={"layer": "DOBLE_FONDO"},
        )
        # Etiqueta compartimento
        _add_text(
            msp,
            f"DB-{i}",
            (x - compartment_length/2, DOUBLE_BOTTOM_HEIGHT * 0.5),
            height=0.18,
            align=TextEntityAlignment.MIDDLE_CENTER,
        )
    
    # Refuerzos estructurales (vagras)
    for i in range(0, int(ENGINE_ROOM_LENGTH) + 1, 2):
        x = ENGINE_ROOM_START + i
        if ENGINE_ROOM_START < x < ENGINE_ROOM_END:
            msp.add_line(
                (x, 0.0),
                (x, DOUBLE_BOTTOM_HEIGHT * 0.25),
                dxfattribs={"layer": "REFUERZOS"},
            )


def draw_reinforced_bulkheads(msp: ezdxf.layouts.Modelspace) -> None:
    """Mamparos estancos con refuerzos estructurales."""
    for x, label in [(ENGINE_ROOM_START, "MAMPARO POPA"), (ENGINE_ROOM_END, "MAMPARO PROA")]:
        # Mamparo principal
        msp.add_line(
            (x, 0.0),
            (x, MAIN_DECK_HEIGHT),
            dxfattribs={"layer": "MAMPAROS"},
        )
        
        # Refuerzos horizontales (palmejares)
        for y in [1.5, 3.5, 5.5]:
            if y < MAIN_DECK_HEIGHT:
                offset = 0.08 if x == ENGINE_ROOM_START else -0.08
                msp.add_line(
                    (x + offset, y - 0.15),
                    (x + offset, y + 0.15),
                    dxfattribs={"layer": "REFUERZOS"},
                )
        
        # Refuerzos verticales
        for i in range(-2, 3):
            y_start = DOUBLE_BOTTOM_HEIGHT + 0.5
            y_end = MAIN_DECK_HEIGHT - 0.5
            offset_y = i * 1.0
            
            if 0 < y_start + offset_y < y_end:
                offset_x = 0.06 if x == ENGINE_ROOM_START else -0.06
                msp.add_line(
                    (x + offset_x, y_start),
                    (x + offset_x, y_end),
                    dxfattribs={"layer": "REFUERZOS"},
                )
        
        # Etiqueta
        side = -2.5 if x == ENGINE_ROOM_START else 2.5
        _add_text(
            msp,
            label,
            (x + side, MAIN_DECK_HEIGHT / 2),
            height=0.30,
            align=TextEntityAlignment.MIDDLE_RIGHT if side < 0 else TextEntityAlignment.MIDDLE_LEFT,
        )


def draw_main_engine_detailed(msp: ezdxf.layouts.Modelspace) -> None:
    """Motor principal con fundación y detalles mecánicos."""
    motor_end = MOTOR_START + MOTOR_LENGTH
    motor_top = MOTOR_BASE_HEIGHT + MOTOR_HEIGHT
    
    # Fundación
    foundation_points = [
        (MOTOR_START - 0.40, DOUBLE_BOTTOM_HEIGHT),
        (MOTOR_START - 0.40, MOTOR_BASE_HEIGHT),
        (motor_end + 0.40, MOTOR_BASE_HEIGHT),
        (motor_end + 0.40, DOUBLE_BOTTOM_HEIGHT),
    ]
    msp.add_lwpolyline(foundation_points, dxfattribs={"layer": "FUNDACION_MOTOR", "closed": True})
    
    # Contorno motor
    motor_points = [
        (MOTOR_START, MOTOR_BASE_HEIGHT),
        (MOTOR_START, motor_top),
        (motor_end, motor_top),
        (motor_end, MOTOR_BASE_HEIGHT),
    ]
    msp.add_lwpolyline(motor_points, dxfattribs={"layer": "MOTOR_PRINCIPAL", "closed": True})
    
    # Línea de cigüeñal
    crankshaft_y = MOTOR_BASE_HEIGHT + MOTOR_HEIGHT * 0.45
    msp.add_line(
        (MOTOR_START, crankshaft_y),
        (motor_end, crankshaft_y),
        dxfattribs={"layer": "MOTOR_PRINCIPAL"},
    )
    
    # Cilindros (6 unidades)
    cylinder_spacing = MOTOR_LENGTH / (MOTOR_CYLINDERS + 1)
    for i in range(1, MOTOR_CYLINDERS + 1):
        cyl_x = MOTOR_START + i * cylinder_spacing
        cyl_radius = 0.45
        
        # Círculo cilindro
        msp.add_circle(
            (cyl_x, crankshaft_y),
            radius=cyl_radius,
            dxfattribs={"layer": "MOTOR_PRINCIPAL"},
        )
        
        # Número cilindro
        _add_text(
            msp,
            str(i),
            (cyl_x, crankshaft_y),
            height=0.25,
            align=TextEntityAlignment.MIDDLE_CENTER,
        )
    
    # Etiquetas
    _add_text(
        msp,
        "MAN 6S50ME-C",
        (MOTOR_START + MOTOR_LENGTH / 2, motor_top + 0.3),
        height=0.35,
        align=TextEntityAlignment.BOTTOM_CENTER,
    )
    _add_text(
        msp,
        f"{MOTOR_POWER_KW} kW @ {MOTOR_RPM} RPM",
        (MOTOR_START + MOTOR_LENGTH / 2, motor_top + 0.75),
        height=0.25,
        align=TextEntityAlignment.BOTTOM_CENTER,
    )


def draw_propulsion_shaft_system(msp: ezdxf.layouts.Modelspace) -> None:
    """Sistema completo de eje propulsor con bocina y chumaceras."""
    # Línea del eje principal
    msp.add_line(
        (SHAFT_START, SHAFT_CENTER_HEIGHT),
        (SHAFT_END, SHAFT_CENTER_HEIGHT),
        dxfattribs={"layer": "EJE_PROPULSOR"},
    )
    
    # Representación del eje (rectángulo delgado)
    shaft_half_dia = SHAFT_DIAMETER / 2
    shaft_rect = [
        (SHAFT_START, SHAFT_CENTER_HEIGHT - shaft_half_dia),
        (SHAFT_START, SHAFT_CENTER_HEIGHT + shaft_half_dia),
        (PROPELLER_POS - 0.5, SHAFT_CENTER_HEIGHT + shaft_half_dia),
        (PROPELLER_POS - 0.5, SHAFT_CENTER_HEIGHT - shaft_half_dia),
    ]
    msp.add_lwpolyline(shaft_rect, dxfattribs={"layer": "EJE_PROPULSOR", "closed": True})
    
    # Bocina (stern tube)
    stern_tube_half = STERN_TUBE_DIAMETER / 2
    tube_outline = [
        (STERN_TUBE_START, SHAFT_CENTER_HEIGHT - stern_tube_half),
        (STERN_TUBE_START, SHAFT_CENTER_HEIGHT + stern_tube_half),
        (STERN_TUBE_END, SHAFT_CENTER_HEIGHT + stern_tube_half),
        (STERN_TUBE_END, SHAFT_CENTER_HEIGHT - stern_tube_half),
    ]
    msp.add_lwpolyline(tube_outline, dxfattribs={"layer": "BOCINA", "closed": True})
    
    _add_text(msp, "BOCINA", (STERN_TUBE_START + 1.0, SHAFT_CENTER_HEIGHT - 1.2), height=0.22)
    
    # Chumaceras (shaft bearings)
    for bearing_x, label in [(BEARING_1_POS, "CHUM.1"), (BEARING_2_POS, "CHUM.2")]:
        bearing_half = BEARING_DIAMETER / 2
        bearing_outline = [
            (bearing_x, SHAFT_CENTER_HEIGHT - bearing_half),
            (bearing_x, SHAFT_CENTER_HEIGHT + bearing_half),
            (bearing_x + BEARING_LENGTH, SHAFT_CENTER_HEIGHT + bearing_half),
            (bearing_x + BEARING_LENGTH, SHAFT_CENTER_HEIGHT - bearing_half),
        ]
        msp.add_lwpolyline(bearing_outline, dxfattribs={"layer": "BOCINA", "closed": True})
        _add_text(msp, label, (bearing_x, SHAFT_CENTER_HEIGHT + bearing_half + 0.3), height=0.18)


def draw_propeller(msp: ezdxf.layouts.Modelspace) -> None:
    """Hélice de paso fijo con 4 palas."""
    prop_radius = PROPELLER_DIAMETER / 2
    hub_radius = PROPELLER_HUB_DIAMETER / 2
    
    # Hub (núcleo)
    msp.add_circle(
        (PROPELLER_POS, SHAFT_CENTER_HEIGHT),
        radius=hub_radius,
        dxfattribs={"layer": "HELICE"},
    )
    
    # Palas (representación esquemática en vista lateral)
    blade_angles = [0, 90, 180, 270]  # grados
    
    for angle in blade_angles:
        rad = math.radians(angle)
        # Proyección en 2D (vista lateral simplificada)
        if angle in [0, 180]:  # Palas visibles en perfil
            blade_tip_x = PROPELLER_POS + prop_radius * 0.3 * math.cos(rad)
            blade_tip_y = SHAFT_CENTER_HEIGHT + prop_radius * math.sin(rad)
            
            # Contorno de pala (elipse simplificada)
            blade_points = [
                (PROPELLER_POS, SHAFT_CENTER_HEIGHT),
                (blade_tip_x, blade_tip_y),
                (PROPELLER_POS + prop_radius * 0.15, blade_tip_y * 0.95),
            ]
            msp.add_lwpolyline(blade_points, dxfattribs={"layer": "HELICE"})
    
    # Círculo de diámetro completo (referencia)
    msp.add_circle(
        (PROPELLER_POS, SHAFT_CENTER_HEIGHT),
        radius=prop_radius,
        dxfattribs={"layer": "HELICE"},
    )
    
    # Etiqueta
    _add_text(
        msp,
        f"HÉLICE Ø{PROPELLER_DIAMETER}m",
        (PROPELLER_POS, SHAFT_CENTER_HEIGHT - prop_radius - 0.5),
        height=0.28,
        align=TextEntityAlignment.TOP_CENTER,
    )
    _add_text(
        msp,
        f"{PROPELLER_BLADES} PALAS",
        (PROPELLER_POS, SHAFT_CENTER_HEIGHT - prop_radius - 0.9),
        height=0.22,
        align=TextEntityAlignment.TOP_CENTER,
    )


def draw_rudder(msp: ezdxf.layouts.Modelspace) -> None:
    """Timón compensado tipo semi-balanced."""
    rudder_bottom = DRAFT - RUDDER_HEIGHT
    rudder_top = DRAFT
    
    # Perfil aerodinámico del timón (simplificado)
    rudder_points = [
        # Parte delantera (20% compensado adelante del eje)
        (RUDDER_POS - RUDDER_CHORD * 0.20, rudder_bottom),
        (RUDDER_POS - RUDDER_CHORD * 0.20, rudder_top),
        # Eje del timón
        (RUDDER_POS, rudder_top),
        (RUDDER_POS, rudder_bottom),
        # Parte trasera
        (RUDDER_POS + RUDDER_CHORD * 0.80, rudder_bottom + RUDDER_HEIGHT * 0.5),
    ]
    msp.add_lwpolyline(rudder_points, dxfattribs={"layer": "TIMON"})
    
    # Eje del timón (madre del timón)
    msp.add_line(
        (RUDDER_POS, rudder_bottom - 0.5),
        (RUDDER_POS, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "TIMON"},
    )
    
    # Etiqueta
    _add_text(
        msp,
        "TIMÓN",
        (RUDDER_POS + 1.0, (rudder_bottom + rudder_top) / 2),
        height=0.25,
        align=TextEntityAlignment.MIDDLE_LEFT,
    )


def draw_cross_section_reference(msp: ezdxf.layouts.Modelspace) -> None:
    """Sección transversal de referencia (pequeña vista lateral)."""
    # Posición de la sección
    section_x = ENGINE_ROOM_END + 10.0
    section_scale = 0.4
    
    half_beam_scaled = (BEAM / 2) * section_scale
    depth_scaled = DEPTH * section_scale
    
    # Contorno del casco (simplificado)
    section_points = [
        (section_x - half_beam_scaled, 0),
        (section_x - half_beam_scaled, depth_scaled * 0.85),
        (section_x - half_beam_scaled * 0.85, depth_scaled),
        (section_x + half_beam_scaled * 0.85, depth_scaled),
        (section_x + half_beam_scaled, depth_scaled * 0.85),
        (section_x + half_beam_scaled, 0),
    ]
    msp.add_lwpolyline(section_points, dxfattribs={"layer": "SECCION_TRANSVERSAL", "closed": True})
    
    # Doble fondo
    db_scaled = DOUBLE_BOTTOM_HEIGHT * section_scale
    msp.add_line(
        (section_x - half_beam_scaled * 0.85, db_scaled),
        (section_x + half_beam_scaled * 0.85, db_scaled),
        dxfattribs={"layer": "SECCION_TRANSVERSAL"},
    )
    
    # Doble costado
    ds_scaled = DOUBLE_SIDE_WIDTH * section_scale
    for side in [-1, 1]:
        x_pos = section_x + side * (half_beam_scaled - ds_scaled)
        msp.add_line(
            (x_pos, db_scaled),
            (x_pos, depth_scaled),
            dxfattribs={"layer": "SECCION_TRANSVERSAL"},
        )
    
    # Etiqueta
    _add_text(
        msp,
        "SECCIÓN TRANSVERSAL",
        (section_x, depth_scaled + 0.5),
        height=0.25,
        align=TextEntityAlignment.BOTTOM_CENTER,
    )


def draw_generators(msp: ezdxf.layouts.Modelspace) -> None:
    """Generadores auxiliares con detalles."""
    gen_positions = [GEN1_START, GEN2_START, GEN3_START]
    
    for i, gen_start in enumerate(gen_positions, 1):
        gen_end = gen_start + GEN_LENGTH
        gen_top = GEN_BASE_HEIGHT + GEN_HEIGHT
        
        # Contorno
        gen_points = [
            (gen_start, GEN_BASE_HEIGHT),
            (gen_start, gen_top),
            (gen_end, gen_top),
            (gen_end, GEN_BASE_HEIGHT),
        ]
        msp.add_lwpolyline(gen_points, dxfattribs={"layer": "GENERADORES", "closed": True})
        
        # Detalle interno (motor + generador)
        motor_section = GEN_LENGTH * 0.6
        msp.add_line(
            (gen_start + motor_section, GEN_BASE_HEIGHT),
            (gen_start + motor_section, gen_top),
            dxfattribs={"layer": "GENERADORES"},
        )
        
        # Etiqueta
        _add_text(
            msp,
            f"GEN {i}",
            (gen_start + GEN_LENGTH / 2, gen_top + 0.2),
            height=0.25,
            align=TextEntityAlignment.BOTTOM_CENTER,
        )
        _add_text(
            msp,
            "CAT 3512C - 500kW",
            (gen_start + GEN_LENGTH / 2, gen_top + 0.55),
            height=0.18,
            align=TextEntityAlignment.BOTTOM_CENTER,
        )


def draw_service_tanks(msp: ezdxf.layouts.Modelspace) -> None:
    """Tanques de servicio diario."""
    # Tanque FO (fuel oil)
    fo_top = PLATFORM_2_HEIGHT + SERVICE_TANK_FO_HEIGHT
    fo_rect = [
        (SERVICE_TANK_FO_START, PLATFORM_2_HEIGHT),
        (SERVICE_TANK_FO_START, fo_top),
        (SERVICE_TANK_FO_START + SERVICE_TANK_FO_LENGTH, fo_top),
        (SERVICE_TANK_FO_START + SERVICE_TANK_FO_LENGTH, PLATFORM_2_HEIGHT),
    ]
    msp.add_lwpolyline(fo_rect, dxfattribs={"layer": "TANQUES_SERVICIO", "closed": True})
    _add_text(
        msp,
        "TQ FO DIARIO",
        (SERVICE_TANK_FO_START + SERVICE_TANK_FO_LENGTH / 2, fo_top - 0.5),
        height=0.20,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )
    
    # Tanque LO (lubricating oil)
    lo_top = PLATFORM_2_HEIGHT + SERVICE_TANK_FO_HEIGHT
    lo_rect = [
        (SERVICE_TANK_LO_START, PLATFORM_2_HEIGHT),
        (SERVICE_TANK_LO_START, lo_top),
        (SERVICE_TANK_LO_START + SERVICE_TANK_LO_LENGTH, lo_top),
        (SERVICE_TANK_LO_START + SERVICE_TANK_LO_LENGTH, PLATFORM_2_HEIGHT),
    ]
    msp.add_lwpolyline(lo_rect, dxfattribs={"layer": "TANQUES_SERVICIO", "closed": True})
    _add_text(
        msp,
        "TQ LO",
        (SERVICE_TANK_LO_START + SERVICE_TANK_LO_LENGTH / 2, lo_top - 0.5),
        height=0.20,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )


def draw_piping_systems(msp: ezdxf.layouts.Modelspace) -> None:
    """Sistemas principales de tuberías."""
    # Tubería de combustible principal
    fuel_pipe_y = DOUBLE_BOTTOM_HEIGHT + 0.15
    msp.add_line(
        (ENGINE_ROOM_START, fuel_pipe_y),
        (ENGINE_ROOM_END, fuel_pipe_y),
        dxfattribs={"layer": "TUBERIAS"},
    )
    _add_text(msp, "Ø200 FO", (ENGINE_ROOM_START + 2.0, fuel_pipe_y + 0.3), height=0.15)
    
    # Tubería de agua de mar
    sw_pipe_y = DOUBLE_BOTTOM_HEIGHT + 0.35
    msp.add_line(
        (ENGINE_ROOM_START, sw_pipe_y),
        (ENGINE_ROOM_END, sw_pipe_y),
        dxfattribs={"layer": "TUBERIAS"},
    )
    _add_text(msp, "Ø300 SW", (ENGINE_ROOM_START + 2.0, sw_pipe_y + 0.3), height=0.15)


def draw_legend_detailed(msp: ezdxf.layouts.Modelspace) -> None:
    """Leyenda técnica completa."""
    legend_x = ENGINE_ROOM_START
    legend_y = MAIN_DECK_HEIGHT + 2.0
    
    # Título
    _add_text(
        msp,
        "PLANO LONGITUDINAL DETALLADO - SALA DE MÁQUINAS",
        (legend_x, legend_y),
        height=0.50,
        layer="LEYENDA",
    )
    
    # Datos técnicos
    data_y = legend_y - 0.8
    info_lines = [
        f"Buque: Carga General | LPP: {LPP}m | Manga: {BEAM}m | Puntal: {DEPTH}m",
        f"Sala de Máquinas: {ENGINE_ROOM_LENGTH}m ({ENGINE_ROOM_START}-{ENGINE_ROOM_END}m desde PP popa)",
        f"Motor Principal: MAN 6S50ME-C {MOTOR_POWER_KW}kW @ {MOTOR_RPM}RPM | {MOTOR_CYLINDERS} cilindros",
        f"Generadores: 3 x CAT 3512C 500kW",
        f"Propulsión: Hélice Ø{PROPELLER_DIAMETER}m {PROPELLER_BLADES} palas | Timón compensado",
        f"Eje: Ø{SHAFT_DIAMETER}m | Bocina L={STERN_TUBE_END - STERN_TUBE_START:.1f}m",
        f"Escala: 1:100 | Fecha: 6 noviembre 2025",
    ]
    
    for i, line in enumerate(info_lines):
        _add_text(msp, line, (legend_x, data_y - i * 0.35), height=0.22, layer="LEYENDA")


def draw_dimensions(msp: ezdxf.layouts.Modelspace) -> None:
    """Cotas principales."""
    dim_y = -2.0
    
    # Longitud sala de máquinas
    msp.add_linear_dim(
        base=(ENGINE_ROOM_START, dim_y),
        p1=(ENGINE_ROOM_START, dim_y - 0.3),
        p2=(ENGINE_ROOM_END, dim_y - 0.3),
        dxfattribs={"layer": "COTAS"},
    )
    
    # Altura puntal
    dim_x = ENGINE_ROOM_END + 2.5
    msp.add_linear_dim(
        base=(dim_x, 0.0),
        p1=(dim_x + 0.3, 0.0),
        p2=(dim_x + 0.3, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "COTAS"},
    )


def main() -> None:
    """Genera el DXF completo mejorado."""
    print("=" * 80)
    print("   GENERADOR DE PLANO LONGITUDINAL DETALLADO - SALA DE MÁQUINAS")
    print("=" * 80)
    print()
    
    doc = ezdxf.new("R2010", setup=True)
    doc.units = units.M
    msp = doc.modelspace()
    
    print("📐 Creando capas profesionales...")
    _create_layers(doc)
    
    print("🚢 Dibujando perfil detallado del casco...")
    draw_detailed_hull_profile(msp)
    
    print("⚓ Dibujando doble fondo compartimentado...")
    draw_detailed_double_bottom(msp)
    
    print("🔲 Dibujando mamparos con refuerzos...")
    draw_reinforced_bulkheads(msp)
    
    print("⚙️  Dibujando motor principal con fundación...")
    draw_main_engine_detailed(msp)
    
    print("🔄 Dibujando sistema de propulsión (eje + bocina + chumaceras)...")
    draw_propulsion_shaft_system(msp)
    
    print("🌀 Dibujando hélice de 4 palas...")
    draw_propeller(msp)
    
    print("🎯 Dibujando timón compensado...")
    draw_rudder(msp)
    
    print("🔌 Dibujando generadores auxiliares...")
    draw_generators(msp)
    
    print("⛽ Dibujando tanques de servicio diario...")
    draw_service_tanks(msp)
    
    print("🔧 Dibujando sistemas de tuberías...")
    draw_piping_systems(msp)
    
    print("📊 Dibujando sección transversal de referencia...")
    draw_cross_section_reference(msp)
    
    print("📏 Añadiendo dimensiones...")
    draw_dimensions(msp)
    
    print("📋 Dibujando leyenda técnica...")
    draw_legend_detailed(msp)

    print("🔍 Ejecutando auditoría DXF...")
    auditor = doc.audit()
    if auditor.has_fixes:
        print(f"   • Auditoría aplicó {len(auditor.fixes)} correcciones menores.")
    if auditor.has_errors:
        auditor.print_error_report()
        raise RuntimeError("La auditoría DXF detectó errores no recuperables. Revisar el log anterior.")
    else:
        print("   • Auditoría completada sin errores fatales.")
    print(f"\n💾 Guardando archivo: {DXF_OUTPUT}")
    default_bounds = (DEFAULT_X_MIN, DEFAULT_Y_MIN, DEFAULT_X_MAX, DEFAULT_Y_MAX)
    extmin, extmax = save_dxf_with_extents(
        doc,
        DXF_OUTPUT,
        msp,
        default_bounds=default_bounds,
    )
    print(
        f"   • EXTMIN: ({extmin[0]:.2f}, {extmin[1]:.2f}) | "
        f"EXTMAX: ({extmax[0]:.2f}, {extmax[1]:.2f})"
    )
    
    print()
    print("=" * 80)
    print("✅ PLANO DETALLADO GENERADO EXITOSAMENTE")
    print("=" * 80)
    print(f"\n📁 Archivo: {DXF_OUTPUT}")
    print(f"📊 Elementos incluidos:")
    print(f"   ✓ Doble fondo compartimentado con refuerzos")
    print(f"   ✓ Mamparos estancos con palmejares y refuerzos verticales")
    print(f"   ✓ Motor principal MAN 6S50ME-C con fundación")
    print(f"   ✓ Sistema completo de eje propulsor")
    print(f"   ✓ Bocina (stern tube) y chumaceras")
    print(f"   ✓ Hélice Ø{PROPELLER_DIAMETER}m de {PROPELLER_BLADES} palas")
    print(f"   ✓ Timón compensado tipo semi-balanced")
    print(f"   ✓ 3 Generadores CAT 3512C (500 kW c/u)")
    print(f"   ✓ Tanques de servicio diario (FO y LO)")
    print(f"   ✓ Sistemas de tuberías principales")
    print(f"   ✓ Sección transversal de referencia")
    print()


if __name__ == "__main__":
    main()
