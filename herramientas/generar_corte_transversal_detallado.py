#!/usr/bin/env python3
"""
Generador de Corte Transversal Detallado - Cuaderna Maestra
===========================================================

Genera un plano de corte transversal detallado de la cuaderna maestra basado en:
- Normativa DNV-RU-SHIP Pt.3 Ch.2 y Ch.3
- SOLAS Ch. II-1
- Diseño de buques de carga general y petroleros

Autor: Proyecto Final - Diseño Naval
Fecha: 3 de noviembre de 2025
"""

import math
from pathlib import Path
import csv

from utils_dxf import save_dxf_with_extents

# === CONFIGURACIÓN DE SALIDA ===
OUTPUT_DIR = Path("salidas/ENTREGA 3")
DXF_FILENAME = "Corte_Transversal_Cuaderna_Maestra_Detallado.dxf"
CSV_FILENAME = "Dimensiones_Estructurales_Detalladas.csv"
GUIDE_FILENAME = "Guia_Corte_Transversal.md"

# === DIMENSIONES PRINCIPALES DEL BUQUE ===
class ShipDimensions:
    """Dimensiones principales del buque de carga general"""
    # Dimensiones principales
    LPP = 105.2            # Eslora entre perpendiculares (m)
    BEAM = 15.99           # Manga (m)
    DEPTH = 7.90           # Puntal (m)
    DRAFT = 6.20           # Calado de diseño (m)
    DISPLACEMENT = 7028.213 # Desplazamiento (toneladas)
    
    # Ubicación de la cuaderna maestra
    MASTER_FRAME_POSITION = LPP / 2.0  # ~50.3 m desde proa
    
    # Compartimentación vertical
    DOUBLE_BOTTOM_HEIGHT = 1.20  # Altura del doble fondo (m)
    MAIN_DECK_HEIGHT = DEPTH     # Altura de la cubierta principal (m)
    FREEBOARD = DEPTH - DRAFT    # Francobordo (m)
    
    # Compartimentación horizontal
    DOUBLE_SIDE_WIDTH = 1.80     # Ancho del costado doble (m)
    INNER_BEAM = BEAM - 2 * DOUBLE_SIDE_WIDTH  # Manga interior (≈12.39 m)
    
    # Espaciamiento de cuadernas
    FRAME_SPACING = 0.70         # Espaciamiento de cuadernas en zona central (m)
    FRAME_SPACING_ENDS = 0.60    # Espaciamiento en proa/popa (m)
    
    # Material estructural
    STEEL_GRADE = "AH36"         # Acero de alta resistencia DNV
    YIELD_STRENGTH = 355         # Límite elástico (MPa)


# === CONFIGURACIÓN DE ESPESORES Y PERFILES ===
class StructuralScantlings:
    """Escantillonado estructural según DNV"""
    # Espesores de chapas (mm)
    BOTTOM_SHELL_PLATE = 22      # Forro de fondo exterior
    SIDE_SHELL_PLATE = 20        # Forro de costado
    INNER_BOTTOM_PLATE = 14      # Chapa de fondo interior
    INNER_SIDE_PLATE = 12        # Mamparo longitudinal interno
    DECK_PLATE = 12              # Chapa de cubierta principal
    DECK_PLATE_HATCH = 16        # Chapa de cubierta en zona de escotilla
    
    # Perfiles estructurales (altura en mm)
    FLOOR_HEIGHT = 400           # Altura de varengas (transverse floors)
    FRAME_HEIGHT = 300           # Altura de cuadernas transversales
    DECK_BEAM_HEIGHT = 250       # Altura de baos de cubierta
    LONGITUDINAL_HEIGHT = 200    # Altura de longitudinales
    
    # Espesores de perfiles (mm)
    FLOOR_WEB_THICKNESS = 12
    FRAME_WEB_THICKNESS = 10
    BEAM_WEB_THICKNESS = 10
    LONGITUDINAL_WEB_THICKNESS = 8
    
    # Flanges (mm)
    FLOOR_FLANGE_WIDTH = 150
    FLOOR_FLANGE_THICKNESS = 20
    FRAME_FLANGE_WIDTH = 120
    FRAME_FLANGE_THICKNESS = 16
    BEAM_FLANGE_WIDTH = 100
    BEAM_FLANGE_THICKNESS = 14


def ensure_dependencies() -> None:
    """Verifica que las dependencias necesarias estén instaladas"""
    try:
        import ezdxf
    except ImportError:
        raise SystemExit(
            "❌ ERROR: ezdxf no está instalado.\n"
            "Instálalo con: pip install ezdxf"
        )


def create_layers(doc) -> None:
    """Crea las capas (layers) para organizar el dibujo"""
    layers_config = [
        ("CASCO_EXTERIOR", 7, "Continuous"),      # Blanco - Forro exterior
        ("ESTRUCTURA_PRIMARIA", 1, "Continuous"), # Rojo - Estructura principal
        ("ESTRUCTURA_SECUNDARIA", 3, "Continuous"),# Verde - Longitudinales
        ("MAMPAROS", 5, "Continuous"),            # Azul - Mamparos internos
        ("TANQUES", 4, "Continuous"),             # Cyan - Límites de tanques
        ("LINEA_AGUA", 6, "DASHED"),              # Magenta - Línea de flotación
        ("COTAS", 2, "Continuous"),               # Amarillo - Dimensiones
        ("TEXTO", 8, "Continuous"),               # Gris - Etiquetas
        ("EJES", 9, "CENTER"),                    # Gris claro - Ejes de referencia
    ]
    
    for name, color, linetype in layers_config:
        if name not in doc.layers:
            layer = doc.layers.add(name)
            layer.color = color
            try:
                layer.dxf.linetype = linetype
            except:
                pass  # Algunos tipos de línea pueden no estar disponibles


def draw_reference_lines(msp, ship: ShipDimensions) -> None:
    """Dibuja las líneas de referencia: base line, centerline, waterline"""
    
    # Línea base (baseline) - Z = 0
    msp.add_line(
        (-ship.BEAM/2 - 2, 0),
        (ship.BEAM/2 + 2, 0),
        dxfattribs={"layer": "EJES", "linetype": "CENTER"}
    )
    
    # Línea de crujía (centerline) - Y = 0
    msp.add_line(
        (0, -1),
        (0, ship.DEPTH + 1),
        dxfattribs={"layer": "EJES", "linetype": "CENTER"}
    )
    
    # Línea de flotación (waterline) - Z = DRAFT
    msp.add_line(
        (-ship.BEAM/2 - 2, ship.DRAFT),
        (ship.BEAM/2 + 2, ship.DRAFT),
        dxfattribs={"layer": "LINEA_AGUA", "linetype": "DASHED", "color": 6}
    )
    
    # Cubierta principal - Z = DEPTH
    msp.add_line(
        (-ship.BEAM/2 - 1, ship.DEPTH),
        (ship.BEAM/2 + 1, ship.DEPTH),
        dxfattribs={"layer": "EJES", "linetype": "CENTER"}
    )


def draw_hull_outline(msp, ship: ShipDimensions, scant: StructuralScantlings) -> None:
    """Dibuja el contorno exterior del casco"""
    
    half_beam = ship.BEAM / 2.0
    
    # Convertir espesores de mm a metros
    t_bottom = scant.BOTTOM_SHELL_PLATE / 1000
    t_side = scant.SIDE_SHELL_PLATE / 1000
    t_deck = scant.DECK_PLATE / 1000
    
    # === FONDO PLANO (FLAT BOTTOM) ===
    # Desde crujía hasta inicio de pantoque
    bilge_start_y = half_beam * 0.85  # La pantoque comienza al 85% de la manga
    
    # Fondo plano - línea exterior
    msp.add_line(
        (0, 0),
        (bilge_start_y, 0),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    
    # Fondo plano - línea interior (espesor de chapa)
    msp.add_line(
        (0, t_bottom),
        (bilge_start_y, t_bottom),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # === PANTOQUE (BILGE) - Transición curva ===
    # Radio de pantoque típico: ~0.5-1.0 m para buques de carga
    bilge_radius = 0.80  # metros
    bilge_center_y = bilge_start_y
    bilge_center_z = bilge_radius
    
    # Arco exterior de pantoque (desde horizontal hasta vertical)
    start_angle = 270  # Comienza horizontal (apuntando hacia abajo)
    end_angle = 360    # Termina vertical (apuntando a la derecha)
    
    # Crear arco de pantoque (exterior)
    msp.add_arc(
        center=(bilge_center_y, bilge_center_z),
        radius=bilge_radius,
        start_angle=start_angle,
        end_angle=end_angle,
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    
    # Arco interior de pantoque (con espesor)
    msp.add_arc(
        center=(bilge_center_y, bilge_center_z),
        radius=bilge_radius - t_side,
        start_angle=start_angle,
        end_angle=end_angle,
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # === COSTADO VERTICAL (SIDE SHELL) ===
    # Desde fin de pantoque hasta cubierta
    side_start_z = bilge_center_z + bilge_radius
    
    # Costado exterior
    msp.add_line(
        (half_beam, side_start_z),
        (half_beam, ship.DEPTH),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    
    # Costado interior
    msp.add_line(
        (half_beam - t_side, side_start_z),
        (half_beam - t_side, ship.DEPTH),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # === CUBIERTA PRINCIPAL (MAIN DECK) ===
    # Cubierta superior
    msp.add_line(
        (0, ship.DEPTH),
        (half_beam, ship.DEPTH),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    
    # Cubierta inferior (espesor)
    msp.add_line(
        (0, ship.DEPTH - t_deck),
        (half_beam, ship.DEPTH - t_deck),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # === SIMETRÍA - DIBUJAR LADO DE BABOR ===
    draw_symmetry_side(msp, ship, scant, bilge_start_y, bilge_radius, 
                       bilge_center_y, bilge_center_z, side_start_z,
                       t_bottom, t_side, t_deck, half_beam)


def draw_symmetry_side(msp, ship, scant, bilge_start_y, bilge_radius,
                       bilge_center_y, bilge_center_z, side_start_z,
                       t_bottom, t_side, t_deck, half_beam):
    """Dibuja el lado de babor (simétrico al de estribor)"""
    
    # Fondo plano - babor
    msp.add_line(
        (-bilge_start_y, 0),
        (0, 0),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    msp.add_line(
        (-bilge_start_y, t_bottom),
        (0, t_bottom),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # Pantoque - babor
    msp.add_arc(
        center=(-bilge_center_y, bilge_center_z),
        radius=bilge_radius,
        start_angle=180,
        end_angle=270,
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    msp.add_arc(
        center=(-bilge_center_y, bilge_center_z),
        radius=bilge_radius - t_side,
        start_angle=180,
        end_angle=270,
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # Costado - babor
    msp.add_line(
        (-half_beam, side_start_z),
        (-half_beam, ship.DEPTH),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    msp.add_line(
        (-half_beam + t_side, side_start_z),
        (-half_beam + t_side, ship.DEPTH),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )
    
    # Cubierta - babor
    msp.add_line(
        (-half_beam, ship.DEPTH),
        (0, ship.DEPTH),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 50}
    )
    msp.add_line(
        (-half_beam, ship.DEPTH - t_deck),
        (0, ship.DEPTH - t_deck),
        dxfattribs={"layer": "CASCO_EXTERIOR", "lineweight": 25}
    )


def draw_double_bottom(msp, ship: ShipDimensions, scant: StructuralScantlings) -> None:
    """Dibuja la estructura del doble fondo"""
    
    half_beam = ship.BEAM / 2.0
    db_height = ship.DOUBLE_BOTTOM_HEIGHT
    t_inner = scant.INNER_BOTTOM_PLATE / 1000
    
    # === CHAPA DE FONDO INTERIOR (INNER BOTTOM PLATE) ===
    # Línea superior del fondo interior
    msp.add_line(
        (-half_beam + 0.5, db_height),
        (half_beam - 0.5, db_height),
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 40}
    )
    
    # Línea inferior (espesor de chapa)
    msp.add_line(
        (-half_beam + 0.5, db_height - t_inner),
        (half_beam - 0.5, db_height - t_inner),
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 20}
    )
    
    # === VARENGAS (TRANSVERSE FLOORS) ===
    # Dibujar varengas cada FRAME_SPACING (700 mm = 0.70 m)
    # En una vista transversal, vemos el perfil de UNA varenga
    
    floor_height = scant.FLOOR_HEIGHT / 1000  # Convertir a metros
    floor_web_thick = scant.FLOOR_WEB_THICKNESS / 1000
    floor_flange_width = scant.FLOOR_FLANGE_WIDTH / 1000
    floor_flange_thick = scant.FLOOR_FLANGE_THICKNESS / 1000
    
    # Varenga central (en crujía)
    draw_floor_section(msp, 0, 0.1, db_height, floor_height, 
                      floor_web_thick, floor_flange_width, floor_flange_thick)
    
    # Varengas laterales (espaciadas cada ~3m en la vista transversal para claridad)
    for y_pos in [-4.5, -1.5, 1.5, 4.5]:
        if abs(y_pos) < half_beam - 1.0:
            draw_floor_section(msp, y_pos, 0.1, db_height, floor_height,
                             floor_web_thick, floor_flange_width, floor_flange_thick)
    
    # === LONGITUDINALES DE FONDO (BOTTOM LONGITUDINALS) ===
    # En vista transversal, los longitudinales se ven de frente (círculos o rectángulos pequeños)
    long_height = scant.LONGITUDINAL_HEIGHT / 1000
    
    # Dibujar longitudinales distribuidos transversalmente
    long_positions = [-6.0, -4.0, -2.0, 0, 2.0, 4.0, 6.0]
    for y_pos in long_positions:
        if abs(y_pos) < half_beam - 1.5:
            draw_longitudinal_marker(msp, y_pos, db_height, long_height)


def draw_floor_section(msp, y_center, z_bottom, z_top, height, 
                      web_thick, flange_width, flange_thick):
    """Dibuja el perfil de una varenga (perfil T o bulbo)"""
    
    # Alma de la varenga (web)
    msp.add_line(
        (y_center - web_thick/2, z_bottom),
        (y_center - web_thick/2, z_top),
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 30}
    )
    msp.add_line(
        (y_center + web_thick/2, z_bottom),
        (y_center + web_thick/2, z_top),
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 30}
    )
    
    # Ala superior (flange)
    msp.add_lwpolyline(
        [
            (y_center - flange_width/2, z_top),
            (y_center - flange_width/2, z_top - flange_thick),
            (y_center + flange_width/2, z_top - flange_thick),
            (y_center + flange_width/2, z_top),
        ],
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 30}
    )


def draw_longitudinal_marker(msp, y_pos, z_pos, size):
    """Dibuja un marcador para longitudinales (vista de frente)"""
    # Dibujar como un pequeño rectángulo que representa el perfil del longitudinal
    msp.add_lwpolyline(
        [
            (y_pos - 0.05, z_pos - size/2),
            (y_pos + 0.05, z_pos - size/2),
            (y_pos + 0.05, z_pos + size/2),
            (y_pos - 0.05, z_pos + size/2),
            (y_pos - 0.05, z_pos - size/2),
        ],
        dxfattribs={"layer": "ESTRUCTURA_SECUNDARIA", "lineweight": 15}
    )


def draw_double_sides(msp, ship: ShipDimensions, scant: StructuralScantlings) -> None:
    """Dibuja los costados dobles (wing tanks)"""
    
    half_beam = ship.BEAM / 2.0
    inner_half_beam = ship.INNER_BEAM / 2.0
    db_height = ship.DOUBLE_BOTTOM_HEIGHT
    
    t_inner_side = scant.INNER_SIDE_PLATE / 1000
    
    # === MAMPAROS LONGITUDINALES INTERNOS ===
    # Estribor (lado derecho)
    msp.add_line(
        (inner_half_beam, db_height),
        (inner_half_beam, ship.DEPTH),
        dxfattribs={"layer": "MAMPAROS", "lineweight": 35}
    )
    msp.add_line(
        (inner_half_beam - t_inner_side, db_height),
        (inner_half_beam - t_inner_side, ship.DEPTH),
        dxfattribs={"layer": "MAMPAROS", "lineweight": 20}
    )
    
    # Babor (lado izquierdo)
    msp.add_line(
        (-inner_half_beam, db_height),
        (-inner_half_beam, ship.DEPTH),
        dxfattribs={"layer": "MAMPAROS", "lineweight": 35}
    )
    msp.add_line(
        (-inner_half_beam + t_inner_side, db_height),
        (-inner_half_beam + t_inner_side, ship.DEPTH),
        dxfattribs={"layer": "MAMPAROS", "lineweight": 20}
    )
    
    # === CUADERNAS TRANSVERSALES (FRAMES) EN COSTADOS ===
    frame_height = scant.FRAME_HEIGHT / 1000
    frame_web_thick = scant.FRAME_WEB_THICKNESS / 1000
    frame_flange_width = scant.FRAME_FLANGE_WIDTH / 1000
    frame_flange_thick = scant.FRAME_FLANGE_THICKNESS / 1000
    
    # Dibujar cuadernas en tanques laterales (wing tanks)
    # Estribor
    for z_pos in [2.0, 4.0, 6.0]:
        draw_frame_section(msp, inner_half_beam + 0.5, z_pos, 
                          frame_height, frame_web_thick, 
                          frame_flange_width, frame_flange_thick, "horizontal")
    
    # Babor
    for z_pos in [2.0, 4.0, 6.0]:
        draw_frame_section(msp, -inner_half_beam - 0.5, z_pos,
                          frame_height, frame_web_thick,
                          frame_flange_width, frame_flange_thick, "horizontal")
    
    # === LONGITUDINALES DE COSTADO ===
    # Estribor
    for z_pos in [1.5, 2.5, 3.5, 4.5, 5.5, 6.5]:
        if z_pos < ship.DEPTH:
            draw_longitudinal_marker(msp, half_beam - 0.8, z_pos, 0.20)
            draw_longitudinal_marker(msp, inner_half_beam + 0.8, z_pos, 0.20)
    
    # Babor
    for z_pos in [1.5, 2.5, 3.5, 4.5, 5.5, 6.5]:
        if z_pos < ship.DEPTH:
            draw_longitudinal_marker(msp, -half_beam + 0.8, z_pos, 0.20)
            draw_longitudinal_marker(msp, -inner_half_beam - 0.8, z_pos, 0.20)


def draw_frame_section(msp, y_pos, z_pos, height, web_thick, 
                      flange_width, flange_thick, orientation="vertical"):
    """Dibuja el perfil de una cuaderna transversal"""
    
    if orientation == "vertical":
        # Alma vertical
        msp.add_line(
            (y_pos - web_thick/2, z_pos),
            (y_pos - web_thick/2, z_pos + height),
            dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
        )
        msp.add_line(
            (y_pos + web_thick/2, z_pos),
            (y_pos + web_thick/2, z_pos + height),
            dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
        )
        
        # Ala superior
        msp.add_lwpolyline(
            [
                (y_pos - flange_width/2, z_pos + height),
                (y_pos - flange_width/2, z_pos + height - flange_thick),
                (y_pos + flange_width/2, z_pos + height - flange_thick),
                (y_pos + flange_width/2, z_pos + height),
            ],
            dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
        )
    else:  # horizontal
        # Alma horizontal (para perfiles en costados)
        msp.add_line(
            (y_pos, z_pos - web_thick/2),
            (y_pos + height, z_pos - web_thick/2),
            dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
        )
        msp.add_line(
            (y_pos, z_pos + web_thick/2),
            (y_pos + height, z_pos + web_thick/2),
            dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
        )


def draw_deck_structure(msp, ship: ShipDimensions, scant: StructuralScantlings) -> None:
    """Dibuja la estructura de la cubierta principal"""
    
    half_beam = ship.BEAM / 2.0
    deck_z = ship.DEPTH
    
    beam_height = scant.DECK_BEAM_HEIGHT / 1000
    beam_web_thick = scant.BEAM_WEB_THICKNESS / 1000
    beam_flange_width = scant.BEAM_FLANGE_WIDTH / 1000
    beam_flange_thick = scant.BEAM_FLANGE_THICKNESS / 1000
    
    # === BAOS DE CUBIERTA (DECK BEAMS) ===
    # Bao central
    draw_deck_beam(msp, 0, deck_z, beam_height, beam_web_thick,
                  beam_flange_width, beam_flange_thick)
    
    # Baos laterales
    for y_pos in [-4.0, -2.0, 2.0, 4.0]:
        if abs(y_pos) < half_beam - 1.0:
            draw_deck_beam(msp, y_pos, deck_z, beam_height, beam_web_thick,
                          beam_flange_width, beam_flange_thick)


def draw_deck_beam(msp, y_center, z_top, height, web_thick, 
                  flange_width, flange_thick):
    """Dibuja un bao de cubierta (perfil T invertido)"""
    
    z_bottom = z_top - height
    
    # Alma vertical
    msp.add_line(
        (y_center - web_thick/2, z_bottom),
        (y_center - web_thick/2, z_top),
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
    )
    msp.add_line(
        (y_center + web_thick/2, z_bottom),
        (y_center + web_thick/2, z_top),
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
    )
    
    # Ala inferior (flange en la parte inferior del bao)
    msp.add_lwpolyline(
        [
            (y_center - flange_width/2, z_bottom),
            (y_center - flange_width/2, z_bottom + flange_thick),
            (y_center + flange_width/2, z_bottom + flange_thick),
            (y_center + flange_width/2, z_bottom),
        ],
        dxfattribs={"layer": "ESTRUCTURA_PRIMARIA", "lineweight": 25}
    )


def draw_tanks_compartments(msp, ship: ShipDimensions) -> None:
    """Dibuja los límites de tanques y compartimentos"""
    from ezdxf.enums import TextEntityAlignment
    
    half_beam = ship.BEAM / 2.0
    inner_half_beam = ship.INNER_BEAM / 2.0
    db_height = ship.DOUBLE_BOTTOM_HEIGHT
    
    # === TANQUE DE DOBLE FONDO ===
    # Marcar zona de tanque de doble fondo
    msp.add_text(
        "TANQUE DOBLE FONDO",
        dxfattribs={
            "layer": "TEXTO",
            "height": 0.25,
            "style": "Standard",
        }
    ).set_placement((0, db_height/2), align=TextEntityAlignment.MIDDLE_CENTER)
    
    # === TANQUES LATERALES (WING TANKS) ===
    # Estribor
    msp.add_mtext(
        "WING TANK\\PESTRIBOR",
        dxfattribs={
            "layer": "TEXTO",
            "char_height": 0.20,
            "attachment_point": 5,  # Middle center
            "insert": (inner_half_beam + 1.5, ship.DEPTH/2),
        }
    )
    
    # Babor
    msp.add_mtext(
        "WING TANK\\PBABOR",
        dxfattribs={
            "layer": "TEXTO",
            "char_height": 0.20,
            "attachment_point": 5,  # Middle center
            "insert": (-inner_half_beam - 1.5, ship.DEPTH/2),
        }
    )
    
    # === BODEGA DE CARGA CENTRAL ===
    msp.add_text(
        "BODEGA DE CARGA",
        dxfattribs={
            "layer": "TEXTO",
            "height": 0.30,
            "style": "Standard",
        }
    ).set_placement((0, (db_height + ship.DEPTH)/2), align=TextEntityAlignment.MIDDLE_CENTER)


def add_dimensions(msp, ship: ShipDimensions) -> None:
    """Añade las cotas principales al plano"""
    
    half_beam = ship.BEAM / 2.0
    inner_half_beam = ship.INNER_BEAM / 2.0
    db_height = ship.DOUBLE_BOTTOM_HEIGHT
    
    # Offset para cotas (fuera del dibujo)
    dim_offset_y = half_beam + 2.5
    dim_offset_z = -1.5
    
    # === COTAS HORIZONTALES (MANGA) ===
    dim_z = dim_offset_z
    
    # Manga total
    add_horizontal_dimension(msp, -half_beam, half_beam, dim_z,
                           f"B = {ship.BEAM:.2f} m (MANGA TOTAL)")
    
    # Manga interior
    add_horizontal_dimension(msp, -inner_half_beam, inner_half_beam, dim_z - 0.5,
                           f"B interior = {ship.INNER_BEAM:.2f} m")
    
    # Ancho de costado doble
    add_horizontal_dimension(msp, inner_half_beam, half_beam, dim_z - 1.0,
                           f"Costado doble = {ship.DOUBLE_SIDE_WIDTH:.2f} m")
    
    # === COTAS VERTICALES (PUNTAL/CALADO) ===
    dim_y = dim_offset_y
    
    # Puntal total
    add_vertical_dimension(msp, 0, ship.DEPTH, dim_y,
                         f"D = {ship.DEPTH:.2f} m (PUNTAL)")
    
    # Calado
    add_vertical_dimension(msp, 0, ship.DRAFT, dim_y + 0.8,
                         f"T = {ship.DRAFT:.2f} m (CALADO)")
    
    # Altura de doble fondo
    add_vertical_dimension(msp, 0, db_height, dim_y + 1.6,
                         f"Doble fondo = {db_height:.2f} m")
    
    # Francobordo
    add_vertical_dimension(msp, ship.DRAFT, ship.DEPTH, dim_y + 2.4,
                         f"Francobordo = {ship.FREEBOARD:.2f} m")


def add_horizontal_dimension(msp, y1, y2, z, text):
    """Añade una cota horizontal"""
    from ezdxf.enums import TextEntityAlignment
    
    # Línea de cota
    msp.add_line(
        (y1, z),
        (y2, z),
        dxfattribs={"layer": "COTAS", "lineweight": 15}
    )
    
    # Flechas (líneas verticales en los extremos)
    arrow_height = 0.15
    msp.add_line((y1, z - arrow_height), (y1, z + arrow_height),
                dxfattribs={"layer": "COTAS", "lineweight": 15})
    msp.add_line((y2, z - arrow_height), (y2, z + arrow_height),
                dxfattribs={"layer": "COTAS", "lineweight": 15})
    
    # Texto de cota
    msp.add_text(
        text,
        dxfattribs={
            "layer": "COTAS",
            "height": 0.18,
            "style": "Standard",
        }
    ).set_placement(((y1 + y2)/2, z - 0.3), align=TextEntityAlignment.MIDDLE_CENTER)


def add_vertical_dimension(msp, z1, z2, y, text):
    """Añade una cota vertical"""
    from ezdxf.enums import TextEntityAlignment
    
    # Línea de cota
    msp.add_line(
        (y, z1),
        (y, z2),
        dxfattribs={"layer": "COTAS", "lineweight": 15}
    )
    
    # Flechas (líneas horizontales en los extremos)
    arrow_width = 0.15
    msp.add_line((y - arrow_width, z1), (y + arrow_width, z1),
                dxfattribs={"layer": "COTAS", "lineweight": 15})
    msp.add_line((y - arrow_width, z2), (y + arrow_width, z2),
                dxfattribs={"layer": "COTAS", "lineweight": 15})
    
    # Texto de cota (vertical)
    msp.add_text(
        text,
        dxfattribs={
            "layer": "COTAS",
            "height": 0.18,
            "style": "Standard",
            "rotation": 90,
        }
    ).set_placement((y + 0.3, (z1 + z2)/2), align=TextEntityAlignment.MIDDLE_CENTER)


def add_title_block(msp, ship: ShipDimensions):
    """Añade cajetín con información del plano"""
    from ezdxf.enums import TextEntityAlignment
    
    # Posición del cajetín (esquina inferior derecha del espacio de dibujo)
    title_x = ship.BEAM/2 - 5.0
    title_y = -3.0
    
    # Rectángulo del cajetín
    msp.add_lwpolyline(
        [
            (title_x, title_y),
            (title_x + 4.5, title_y),
            (title_x + 4.5, title_y + 2.0),
            (title_x, title_y + 2.0),
            (title_x, title_y),
        ],
        dxfattribs={"layer": "TEXTO", "lineweight": 25}
    )
    
    # Información del cajetín
    info_texts = [
        ("CORTE TRANSVERSAL - CUADERNA MAESTRA", 0.25),
        (f"Buque de Carga General - L={ship.LPP:.2f}m", 0.18),
        (f"Posicion: {ship.MASTER_FRAME_POSITION:.1f}m desde proa", 0.15),
        (f"Material: Acero {ShipDimensions.STEEL_GRADE}", 0.15),
        ("Escala: 1:50", 0.15),
        ("Fecha: 3 Nov 2025", 0.13),
    ]
    
    y_offset = title_y + 1.7
    for text, height in info_texts:
        msp.add_text(
            text,
            dxfattribs={
                "layer": "TEXTO",
                "height": height,
                "style": "Standard",
            }
        ).set_placement((title_x + 0.1, y_offset), align=TextEntityAlignment.LEFT)
        y_offset -= (height + 0.1)


def generate_dxf_plan() -> None:
    """Función principal para generar el plano DXF"""
    try:
        import ezdxf
    except ImportError:
        raise SystemExit(
            "❌ ERROR: ezdxf no está instalado.\n"
            "Instálalo con: pip install ezdxf"
        )
    
    print("🚢 Generando corte transversal detallado de la cuaderna maestra...")
    
    # Crear directorio de salida
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Crear nuevo documento DXF
    doc = ezdxf.new("R2010", setup=True)
    
    # Crear capas
    create_layers(doc)
    
    # Obtener espacio de modelo
    msp = doc.modelspace()
    
    # Crear instancias de configuración
    ship = ShipDimensions()
    scant = StructuralScantlings()
    
    # Dibujar elementos del plano
    print("  📐 Dibujando líneas de referencia...")
    draw_reference_lines(msp, ship)
    
    print("  🔷 Dibujando contorno del casco...")
    draw_hull_outline(msp, ship, scant)
    
    print("  🔧 Dibujando doble fondo...")
    draw_double_bottom(msp, ship, scant)
    
    print("  🔧 Dibujando costados dobles...")
    draw_double_sides(msp, ship, scant)
    
    print("  🔧 Dibujando estructura de cubierta...")
    draw_deck_structure(msp, ship, scant)
    
    print("  🏷️  Añadiendo etiquetas de compartimentos...")
    draw_tanks_compartments(msp, ship)
    
    print("  📏 Añadiendo cotas...")
    add_dimensions(msp, ship)
    
    print("  📋 Añadiendo cajetín...")
    add_title_block(msp, ship)
    
    print("  🔍 Auditando DXF...")
    auditor = doc.audit()
    if auditor.has_fixes:
        print(f"     • Auditoría aplicó {len(auditor.fixes)} correcciones.")
    if auditor.has_errors:
        auditor.print_error_report()
        raise RuntimeError("La auditoría DXF reportó errores fatales. Revisar el log.")
    
    # Guardar archivo DXF con límites consistentes
    dxf_path = OUTPUT_DIR / DXF_FILENAME
    default_bounds = (
        -ship.BEAM / 2 - 5.0,
        -2.0,
        ship.BEAM / 2 + 5.0,
        ship.DEPTH + 5.0,
    )
    extmin, extmax = save_dxf_with_extents(
        doc,
        dxf_path,
        msp,
        default_bounds=default_bounds,
    )
    print(
        f"     • EXTMIN: ({extmin[0]:.2f}, {extmin[1]:.2f}) | "
        f"EXTMAX: ({extmax[0]:.2f}, {extmax[1]:.2f})"
    )
    
    print(f"\n✅ Plano DXF generado exitosamente:")
    print(f"   📁 {dxf_path}")
    print(f"   📊 Tamaño: {dxf_path.stat().st_size / 1024:.1f} KB")


def generate_dimensions_table() -> None:
    """Genera tabla CSV con todas las dimensiones estructurales"""
    
    ship = ShipDimensions()
    scant = StructuralScantlings()
    
    csv_path = OUTPUT_DIR / CSV_FILENAME
    
    dimensions_data = [
        ["CATEGORÍA", "ELEMENTO", "DIMENSIÓN", "VALOR", "UNIDAD", "NORMATIVA"],
        ["", "", "", "", "", ""],
        ["DIMENSIONES PRINCIPALES", "Eslora entre perpendiculares", "Lpp", f"{ship.LPP:.3f}", "m", "Medido"],
        ["", "Manga", "B", f"{ship.BEAM:.2f}", "m", "Medido"],
        ["", "Puntal", "D", f"{ship.DEPTH:.2f}", "m", "Medido"],
        ["", "Calado de diseño", "T", f"{ship.DRAFT:.2f}", "m", "Medido"],
        ["", "Francobordo", "FB", f"{ship.FREEBOARD:.2f}", "m", "Calculado"],
        ["", "Desplazamiento", "Δ", f"{ship.DISPLACEMENT:.3f}", "ton", "Hidrostático"],
        ["", "", "", "", "", ""],
        ["COMPARTIMENTACIÓN", "Altura doble fondo", "hDB", f"{ship.DOUBLE_BOTTOM_HEIGHT:.2f}", "m", "DNV Pt.3 Ch.2 Sec.3"],
        ["", "Altura mínima DNV", "hDB_min", "0.78", "m", "B/20 = 15.60/20"],
        ["", "Ancho costado doble", "w_DS", f"{ship.DOUBLE_SIDE_WIDTH:.2f}", "m", "SOLAS II-1 Reg.13"],
        ["", "Manga interior", "B_inner", f"{ship.INNER_BEAM:.2f}", "m", "B - 2×w_DS"],
        ["", "Espaciamiento cuadernas", "s", f"{ship.FRAME_SPACING:.2f}", "m", "DNV Pt.3 Ch.3"],
        ["", "", "", "", "", ""],
        ["ESPESORES DE CHAPAS", "Forro de fondo exterior", "t_bottom", f"{scant.BOTTOM_SHELL_PLATE}", "mm", "DNV Pt.3 Ch.6"],
        ["", "Forro de costado", "t_side", f"{scant.SIDE_SHELL_PLATE}", "mm", "DNV Pt.3 Ch.6"],
        ["", "Fondo interior", "t_inner_bottom", f"{scant.INNER_BOTTOM_PLATE}", "mm", "DNV Pt.3 Ch.6"],
        ["", "Mamparo longitudinal", "t_inner_side", f"{scant.INNER_SIDE_PLATE}", "mm", "DNV Pt.3 Ch.6"],
        ["", "Cubierta principal", "t_deck", f"{scant.DECK_PLATE}", "mm", "DNV Pt.3 Ch.6"],
        ["", "Cubierta (zona escotilla)", "t_deck_hatch", f"{scant.DECK_PLATE_HATCH}", "mm", "DNV Pt.3 Ch.6"],
        ["", "", "", "", "", ""],
        ["PERFILES ESTRUCTURALES", "Altura varengas", "h_floor", f"{scant.FLOOR_HEIGHT}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Alma varenga", "tw_floor", f"{scant.FLOOR_WEB_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Ala varenga", "bf_floor × tf", f"{scant.FLOOR_FLANGE_WIDTH}×{scant.FLOOR_FLANGE_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Altura cuadernas", "h_frame", f"{scant.FRAME_HEIGHT}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Alma cuaderna", "tw_frame", f"{scant.FRAME_WEB_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Ala cuaderna", "bf_frame × tf", f"{scant.FRAME_FLANGE_WIDTH}×{scant.FRAME_FLANGE_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Altura baos cubierta", "h_beam", f"{scant.DECK_BEAM_HEIGHT}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Alma bao", "tw_beam", f"{scant.BEAM_WEB_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Ala bao", "bf_beam × tf", f"{scant.BEAM_FLANGE_WIDTH}×{scant.BEAM_FLANGE_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Altura longitudinales", "h_long", f"{scant.LONGITUDINAL_HEIGHT}", "mm", "DNV Pt.3 Ch.3"],
        ["", "Alma longitudinal", "tw_long", f"{scant.LONGITUDINAL_WEB_THICKNESS}", "mm", "DNV Pt.3 Ch.3"],
        ["", "", "", "", "", ""],
        ["MATERIAL", "Grado de acero", "-", f"{ship.STEEL_GRADE}", "-", "DNV"],
        ["", "Límite elástico", "σy", f"{ship.YIELD_STRENGTH}", "MPa", "DNV"],
        ["", "", "", "", "", ""],
        ["UBICACIÓN", "Posición cuaderna maestra", "x_MF", f"{ship.MASTER_FRAME_POSITION:.1f}", "m", "Lpp/2 desde proa"],
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(dimensions_data)
    
    print(f"✅ Tabla de dimensiones generada:")
    print(f"   📁 {csv_path}")


def generate_guide_document() -> None:
    """Genera documento guía en Markdown"""
    
    ship = ShipDimensions()
    
    guide_path = OUTPUT_DIR / GUIDE_FILENAME
    
    guide_content = f"""# Guía del Corte Transversal - Cuaderna Maestra

## Información del Plano

**Archivo DXF:** `{DXF_FILENAME}`  
**Fecha de generación:** 3 de noviembre de 2025  
**Posición:** {ship.MASTER_FRAME_POSITION:.1f} m desde perpendicular de proa (Lpp/2)

---

## Descripción General

Este plano muestra el **corte transversal completo** de la cuaderna maestra del buque de carga general, incluyendo:

### ✅ Elementos Representados

1. **Contorno Exterior del Casco**
   - Forro de fondo (flat bottom)
   - Pantoque (bilge) con radio de curvatura realista (~0.80 m)
   - Forro de costado vertical
   - Cubierta principal

2. **Doble Fondo (h = 1.20 m)**
   - Chapa de fondo exterior (22 mm)
   - Varengas (transverse floors) con perfil T
   - Longitudinales de fondo
   - Chapa de fondo interior (14 mm)
   - Tanque de doble fondo para lastre/combustible

3. **Costados Dobles (w = 1.80 m cada lado)**
   - Forro de costado exterior (20 mm)
   - Cuadernas transversales con perfil T
   - Longitudinales de costado
   - Mamparos longitudinales internos (12 mm)
   - Wing tanks para combustible/lastre

4. **Bodega de Carga Central**
   - Ancho interior: 12.00 m
   - Altura libre: ~6.50 m (desde fondo interior a cubierta)
   - Volumen aproximado: ~78 m³ por metro de eslora

5. **Cubierta Principal (z = 7.70 m)**
   - Chapa de cubierta (12 mm estándar, 16 mm en escotillas)
   - Baos transversales con perfil T invertido
   - Refuerzos estructurales

---

## Capas del Dibujo (Layers)

| Capa | Color | Descripción | Uso |
|------|-------|-------------|-----|
| `CASCO_EXTERIOR` | Blanco (7) | Forro exterior | Contorno principal del casco |
| `ESTRUCTURA_PRIMARIA` | Rojo (1) | Varengas, cuadernas, baos | Estructura transversal principal |
| `ESTRUCTURA_SECUNDARIA` | Verde (3) | Longitudinales | Refuerzos longitudinales |
| `MAMPAROS` | Azul (5) | Mamparos internos | Separación de compartimentos |
| `TANQUES` | Cyan (4) | Límites de tanques | Zonas de almacenamiento |
| `LINEA_AGUA` | Magenta (6) | Línea de flotación | T = {ship.DRAFT:.2f} m |
| `COTAS` | Amarillo (2) | Dimensiones | Acotación del plano |
| `TEXTO` | Gris (8) | Etiquetas y cajetín | Información textual |
| `EJES` | Gris claro (9) | Líneas de referencia | Base line, centerline |

---

## Dimensiones Principales

### Manga (Beam)
- **Manga total:** {ship.BEAM:.2f} m
- **Manga interior:** {ship.INNER_BEAM:.2f} m
- **Costado doble:** {ship.DOUBLE_SIDE_WIDTH:.2f} m (cada lado)

### Puntal y Calado (Depth & Draft)
- **Puntal moldeado:** {ship.DEPTH:.2f} m
- **Calado de diseño:** {ship.DRAFT:.2f} m
- **Francobordo:** {ship.FREEBOARD:.2f} m
- **Doble fondo:** {ship.DOUBLE_BOTTOM_HEIGHT:.2f} m

### Espaciamiento Estructural
- **Cuadernas (frames):** {ship.FRAME_SPACING:.2f} m ({int(ship.FRAME_SPACING * 1000)} mm)
- **Longitudinales:** Variable según zona

---

## Normativa Aplicada

### DNV-RU-SHIP Pt.3 Ch.2 - General Arrangement
- **Sec.3 [2.3]:** Altura mínima de doble fondo
  - Fórmula: hDB = B/20 = 15.60/20 = **0.78 m**
  - Adoptado: **1.20 m** ✅ (cumple y excede requisito)

- **Sec.3 [2.2]:** Extensión del doble fondo
  - Desde mamparo de colisión hasta mamparo de popa
  - Continuado hasta pantoque (turn of bilge) ✅

### DNV-RU-SHIP Pt.3 Ch.3 - Structural Design
- **Sec.2:** Arreglo estructural
- **Sec.7:** Idealización estructural
  - Espaciamiento de cuadernas: {ship.FRAME_SPACING:.2f} m
  - Perfiles estructurales: T, Bulbo HP, L

### SOLAS Ch. II-1 - Construction
- **Reg.9:** Double bottoms in cargo ships ✅
- **Reg.13:** Damage stability requirements
  - Protección lateral mediante costados dobles ✅

---

## Materiales Estructurales

### Acero {ship.STEEL_GRADE}
- **Límite elástico:** {ship.YIELD_STRENGTH} MPa (N/mm²)
- **Resistencia a tracción:** 490-630 MPa
- **Elongación:** ≥21%
- **Aplicación:** Estructura principal del casco

### Espesores de Chapas
- Fondo exterior: 22 mm
- Costado: 20 mm
- Fondo interior: 14 mm
- Mamparos internos: 12 mm
- Cubierta: 12-16 mm

---

## Cómo Usar Este Plano

### Visualización en CAD
1. Abrir `{DXF_FILENAME}` en AutoCAD, QCAD, FreeCAD o similar
2. Activar/desactivar capas según necesidad de análisis
3. Usar layer `EJES` para referencias de medición
4. Layer `COTAS` muestra todas las dimensiones principales

### Análisis Estructural
- **Varengas (floors):** Color rojo, cada ~0.70 m transversalmente
- **Longitudinales:** Marcadores verdes, vista frontal
- **Cuadernas:** Perfiles verticales en costados
- **Baos:** Perfiles invertidos bajo cubierta

### Tanques y Compartimentos
- **Doble fondo:** Entre z=0 y z=1.20 m
- **Wing tanks:** Entre mamparos longitudinales y costado exterior
- **Bodega central:** Entre mamparos longitudinales internos

---

## Archivos Complementarios

1. **`{CSV_FILENAME}`**
   - Tabla detallada con todas las dimensiones
   - Referencias normativas para cada elemento
   - Valores calculados y adoptados

2. **`Resumen_Normativa_Cuaderna_Maestra.md`**
   - Resumen completo de normativa aplicada
   - Justificación de diseño estructural
   - Referencias DNV, SOLAS, y Maxsurf

---

## Notas Importantes

⚠️ **Este plano representa la cuaderna maestra en su posición de máxima sección transversal**

📍 **Posición:** {ship.MASTER_FRAME_POSITION:.1f} m desde proa (Lpp/2)

🔍 **Escala recomendada de impresión:** 1:50

📐 **Sistema de coordenadas:**
- Origen: Intersección de baseline, centerline, y perpendicular de popa
- Eje Y: Transversal (estribor positivo)
- Eje Z: Vertical (arriba positivo)

---

## Contacto y Revisiones

**Proyecto:** Diseño Naval - Buque de Carga General  
**Fecha:** 3 de noviembre de 2025  
**Revisión:** v1.0  
**Estado:** Preliminar - Sujeto a aprobación

---

*Generado automáticamente por el sistema de diseño naval*
"""
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ Documento guía generado:")
    print(f"   📁 {guide_path}")


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🚢 GENERADOR DE CORTE TRANSVERSAL DETALLADO - CUADERNA MAESTRA")
    print("="*70 + "\n")
    
    # Verificar dependencias
    ensure_dependencies()
    
    # Generar plano DXF
    generate_dxf_plan()
    
    # Generar tabla de dimensiones
    print("\n📊 Generando tabla de dimensiones estructurales...")
    generate_dimensions_table()
    
    # Generar documento guía
    print("\n📖 Generando documento guía...")
    generate_guide_document()
    
    print("\n" + "="*70)
    print("✅ GENERACIÓN COMPLETADA CON ÉXITO")
    print("="*70)
    print(f"\n📁 Archivos generados en: {OUTPUT_DIR}/")
    print(f"   • {DXF_FILENAME}")
    print(f"   • {CSV_FILENAME}")
    print(f"   • {GUIDE_FILENAME}")
    print("\n💡 Abre el archivo DXF en AutoCAD, QCAD, FreeCAD o similar")
    print("💡 Consulta el documento guía para información detallada\n")


if __name__ == "__main__":
    main()
