"""Genera un DXF con el plano longitudinal profesional de la sala de máquinas.

Este script crea una vista longitudinal detallada de la sala de máquinas mostrando:
- Perfil del casco (línea base, cubierta principal, cubierta de tanques)
- Mamparos estancos de proa y popa
- Doble fondo con tanques
- Tanques laterales (wing tanks)
- Motor principal diesel
- Generadores auxiliares
- Equipos secundarios (bombas, intercambiadores)
- Dimensiones principales
- Leyenda con capas profesionales

Ejecutar desde la raíz del proyecto:
    python herramientas/generar_plano_longitudinal_sala_maquinas.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment

from utils_dxf import save_dxf_with_extents


# ===== CONFIGURACIÓN DEL PROYECTO =====
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "salidas" / "disposicion_general"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DXF_OUTPUT = OUTPUT_DIR / "Plano_Longitudinal_Sala_Maquinas.dxf"

# ===== DIMENSIONES PRINCIPALES DEL BUQUE =====
LPP = 105.2  # m eslora entre perpendiculares
BEAM = 15.99  # m manga
DEPTH = 7.90  # m puntal
DRAFT = 6.20  # m calado de diseño

# ===== SALA DE MÁQUINAS =====
ENGINE_ROOM_START = 8.20  # m desde PP de popa
ENGINE_ROOM_END = 23.20  # m desde PP de popa
ENGINE_ROOM_LENGTH = ENGINE_ROOM_END - ENGINE_ROOM_START  # 15.0 m

# ===== ESTRUCTURA =====
DOUBLE_BOTTOM_HEIGHT = 1.20  # m altura mínima según DNV
DOUBLE_SIDE_WIDTH = 1.80  # m ancho por banda
TANK_TOP_HEIGHT = 2.00  # m altura de cubierta de tanques
MAIN_DECK_HEIGHT = DEPTH  # m cubierta principal
PLATFORM_HEIGHT = 4.50  # m plataforma intermedia

# ===== EQUIPOS PRINCIPALES =====
# Motor principal (Wärtsilä 16V26 o similar)
MOTOR_START = ENGINE_ROOM_START + 3.50
MOTOR_LENGTH = 8.50
MOTOR_WIDTH = 3.20
MOTOR_HEIGHT = 4.00
MOTOR_BASE_HEIGHT = DOUBLE_BOTTOM_HEIGHT

# Generadores auxiliares (3 x 500 kW)
GEN1_START = ENGINE_ROOM_START + 1.50
GEN2_START = GEN1_START + 4.00
GEN3_START = GEN2_START + 4.00
GEN_LENGTH = 3.00
GEN_WIDTH = 1.60
GEN_HEIGHT = 2.50
GEN_BASE_HEIGHT = DOUBLE_BOTTOM_HEIGHT

# Equipos auxiliares
BOILER_START = ENGINE_ROOM_END - 2.50
BOILER_LENGTH = 2.00
BOILER_DIAMETER = 1.20
BOILER_BASE_HEIGHT = DOUBLE_BOTTOM_HEIGHT

# ===== TANQUES =====
WING_TANK_START = 10.20
WING_TANK_END = 22.20

# ===== ESCALA Y OFFSETS =====
SCALE = 1.0  # Escala 1:100 en el plano final
MARGIN = 3.0  # Margen para textos y cotas


def _add_text(
    msp: ezdxf.layouts.Modelspace,
    text: str,
    position: Sequence[float],
    *,
    height: float = 0.30,
    layer: str = "TEXTOS",
    align: TextEntityAlignment = TextEntityAlignment.LEFT,
) -> None:
    """Añade un texto al modelspace con parámetros por defecto."""
    msp.add_text(text, dxfattribs={"height": height, "layer": layer}).set_placement(
        position, align=align
    )


def _add_dimension(
    msp: ezdxf.layouts.Modelspace,
    p1: tuple[float, float],
    p2: tuple[float, float],
    offset: float = 1.0,
    layer: str = "COTAS",
) -> None:
    """Añade una cota lineal entre dos puntos."""
    # Offset hacia arriba para cotas horizontales
    dim_line = (p1[0], p1[1] + offset)
    msp.add_linear_dim(
        base=dim_line,
        p1=p1,
        p2=p2,
        dxfattribs={"layer": layer},
    )


def _create_layers(doc: ezdxf.EzdxfDocument) -> None:
    """Crea las capas profesionales según estándares navales."""
    layers = {
        # Capas estructurales - colores oscuros y visibles
        "CASCO": 1,  # Rojo - contorno del casco
        "ESTRUCTURA": 3,  # Verde - mamparos y refuerzos
        "CUBIERTAS": 4,  # Cian - cubiertas
        # Capas de equipos
        "MOTOR_PRINCIPAL": 2,  # Amarillo - motor diesel
        "GENERADORES": 6,  # Magenta - generadores auxiliares
        "EQUIPOS_AUX": 5,  # Azul - equipos auxiliares
        # Capas de tanques
        "TANQUES_DB": 30,  # Naranja - doble fondo
        "TANQUES_WING": 40,  # Verde claro - tanques laterales
        # Capas de anotación - negro para máxima visibilidad
        "TEXTOS": 0,  # Negro - etiquetas
        "COTAS": 0,  # Negro - dimensiones
        "LEYENDA": 0,  # Negro - leyenda
        "EJES": 8,  # Gris oscuro - líneas de referencia
    }
    for name, color in layers.items():
        # Eliminar capa si existe para recrearla con color correcto
        if name in doc.layers:
            try:
                doc.layers.remove(name)
            except:
                pass
        # Crear capa con color especificado
        layer = doc.layers.add(name=name)
        layer.color = color


def draw_hull_profile(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja el perfil del casco en la sala de máquinas."""
    # Línea base (quilla)
    msp.add_line(
        (ENGINE_ROOM_START, 0.0),
        (ENGINE_ROOM_END, 0.0),
        dxfattribs={"layer": "CASCO", "lineweight": 50},
    )

    # Cubierta principal
    msp.add_line(
        (ENGINE_ROOM_START, MAIN_DECK_HEIGHT),
        (ENGINE_ROOM_END, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "CUBIERTAS", "lineweight": 35},
    )

    # Cubierta de tanques (tank top)
    msp.add_line(
        (ENGINE_ROOM_START, TANK_TOP_HEIGHT),
        (ENGINE_ROOM_END, TANK_TOP_HEIGHT),
        dxfattribs={"layer": "CUBIERTAS", "lineweight": 25},
    )

    # Plataforma intermedia
    msp.add_line(
        (ENGINE_ROOM_START, PLATFORM_HEIGHT),
        (ENGINE_ROOM_END, PLATFORM_HEIGHT),
        dxfattribs={"layer": "CUBIERTAS", "lineweight": 18, "linetype": "DASHED"},
    )

    # Costados del casco (simplificados)
    # Nota: En vista longitudinal solo se ve un costado
    # Se dibuja como línea vertical en los extremos
    msp.add_line(
        (ENGINE_ROOM_START, 0.0),
        (ENGINE_ROOM_START, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "CASCO", "lineweight": 35},
    )
    msp.add_line(
        (ENGINE_ROOM_END, 0.0),
        (ENGINE_ROOM_END, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "CASCO", "lineweight": 35},
    )

    # Etiquetas de cubiertas
    _add_text(
        msp,
        "CUBIERTA PRINCIPAL",
        (ENGINE_ROOM_START + 0.5, MAIN_DECK_HEIGHT + 0.3),
        height=0.25,
        layer="TEXTOS",
    )
    _add_text(
        msp,
        "PLATAFORMA",
        (ENGINE_ROOM_START + 0.5, PLATFORM_HEIGHT + 0.3),
        height=0.25,
        layer="TEXTOS",
    )
    _add_text(
        msp,
        "TANK TOP",
        (ENGINE_ROOM_START + 0.5, TANK_TOP_HEIGHT + 0.3),
        height=0.25,
        layer="TEXTOS",
    )
    _add_text(
        msp,
        "LÍNEA BASE",
        (ENGINE_ROOM_START + 0.5, -0.5),
        height=0.25,
        layer="TEXTOS",
    )


def draw_bulkheads(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja los mamparos estancos de proa y popa."""
    # Mamparo de popa (límite sala de máquinas)
    msp.add_line(
        (ENGINE_ROOM_START, 0.0),
        (ENGINE_ROOM_START, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "ESTRUCTURA", "lineweight": 40},
    )
    _add_text(
        msp,
        "MAMPARO POPA",
        (ENGINE_ROOM_START - 1.5, MAIN_DECK_HEIGHT / 2),
        height=0.30,
        layer="TEXTOS",
        align=TextEntityAlignment.MIDDLE_RIGHT,
    )

    # Mamparo de proa (límite sala de máquinas)
    msp.add_line(
        (ENGINE_ROOM_END, 0.0),
        (ENGINE_ROOM_END, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "ESTRUCTURA", "lineweight": 40},
    )
    _add_text(
        msp,
        "MAMPARO PROA",
        (ENGINE_ROOM_END + 1.5, MAIN_DECK_HEIGHT / 2),
        height=0.30,
        layer="TEXTOS",
        align=TextEntityAlignment.MIDDLE_LEFT,
    )


def draw_double_bottom_tanks(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja el doble fondo con tanques."""
    # Contorno del doble fondo
    db_points = [
        (ENGINE_ROOM_START, 0.0),
        (ENGINE_ROOM_START, DOUBLE_BOTTOM_HEIGHT),
        (ENGINE_ROOM_END, DOUBLE_BOTTOM_HEIGHT),
        (ENGINE_ROOM_END, 0.0),
    ]
    msp.add_lwpolyline(
        db_points,
        dxfattribs={"layer": "TANQUES_DB", "closed": True, "lineweight": 25},
    )

    # Divisiones de tanques (ejemplo: 3 tanques en el doble fondo)
    tank_div_1 = ENGINE_ROOM_START + ENGINE_ROOM_LENGTH / 3
    tank_div_2 = ENGINE_ROOM_START + 2 * ENGINE_ROOM_LENGTH / 3

    for x in [tank_div_1, tank_div_2]:
        msp.add_line(
            (x, 0.0),
            (x, DOUBLE_BOTTOM_HEIGHT),
            dxfattribs={"layer": "TANQUES_DB", "lineweight": 18, "linetype": "DASHED"},
        )

    # Etiqueta
    _add_text(
        msp,
        "DOBLE FONDO (149.96 m³)",
        (ENGINE_ROOM_START + ENGINE_ROOM_LENGTH / 2, DOUBLE_BOTTOM_HEIGHT / 2),
        height=0.25,
        layer="TEXTOS",
        align=TextEntityAlignment.MIDDLE_CENTER,
    )


def draw_wing_tanks(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja indicación de tanques laterales (wing tanks)."""
    # En vista longitudinal, los wing tanks se representan con líneas punteadas
    # en la parte superior del doble fondo hasta la cubierta de tanques

    wing_height = TANK_TOP_HEIGHT - DOUBLE_BOTTOM_HEIGHT

    # Tanque babor (representación esquemática)
    wing_points_port = [
        (WING_TANK_START, DOUBLE_BOTTOM_HEIGHT),
        (WING_TANK_START, TANK_TOP_HEIGHT),
        (WING_TANK_END, TANK_TOP_HEIGHT),
        (WING_TANK_END, DOUBLE_BOTTOM_HEIGHT),
    ]
    msp.add_lwpolyline(
        wing_points_port,
        dxfattribs={
            "layer": "TANQUES_WING",
            "closed": True,
            "lineweight": 18,
            "linetype": "DASHED",
        },
    )

    # Etiqueta
    _add_text(
        msp,
        "WING TANKS (2 x 113.31 m³)",
        (WING_TANK_START + (WING_TANK_END - WING_TANK_START) / 2, TANK_TOP_HEIGHT + 0.3),
        height=0.25,
        layer="TEXTOS",
        align=TextEntityAlignment.BOTTOM_CENTER,
    )


def draw_main_engine(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja el motor principal diesel."""
    motor_end = MOTOR_START + MOTOR_LENGTH
    motor_top = MOTOR_BASE_HEIGHT + MOTOR_HEIGHT

    # Contorno del motor
    motor_points = [
        (MOTOR_START, MOTOR_BASE_HEIGHT),
        (MOTOR_START, motor_top),
        (motor_end, motor_top),
        (motor_end, MOTOR_BASE_HEIGHT),
    ]
    msp.add_lwpolyline(
        motor_points,
        dxfattribs={"layer": "MOTOR_PRINCIPAL", "closed": True, "lineweight": 35},
    )

    # Detalles: cigüeñal (línea central)
    crankshaft_height = MOTOR_BASE_HEIGHT + MOTOR_HEIGHT / 2
    msp.add_line(
        (MOTOR_START, crankshaft_height),
        (motor_end, crankshaft_height),
        dxfattribs={"layer": "MOTOR_PRINCIPAL", "lineweight": 18},
    )

    # Cilindros (representación esquemática - 6 cilindros)
    cylinder_spacing = MOTOR_LENGTH / 7
    for i in range(1, 7):
        cyl_x = MOTOR_START + i * cylinder_spacing
        msp.add_circle(
            (cyl_x, crankshaft_height),
            radius=0.40,
            dxfattribs={"layer": "MOTOR_PRINCIPAL"},
        )

    # Etiqueta
    _add_text(
        msp,
        "MOTOR PRINCIPAL",
        (MOTOR_START + MOTOR_LENGTH / 2, motor_top + 0.3),
        height=0.35,
        layer="TEXTOS",
        align=TextEntityAlignment.BOTTOM_CENTER,
    )
    _add_text(
        msp,
        "6S50ME-C (8500 kW)",
        (MOTOR_START + MOTOR_LENGTH / 2, motor_top + 0.8),
        height=0.25,
        layer="TEXTOS",
        align=TextEntityAlignment.BOTTOM_CENTER,
    )


def draw_generators(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja los generadores auxiliares."""
    gen_positions = [GEN1_START, GEN2_START, GEN3_START]

    for i, gen_start in enumerate(gen_positions, 1):
        gen_end = gen_start + GEN_LENGTH
        gen_top = GEN_BASE_HEIGHT + GEN_HEIGHT

        # Contorno del generador
        gen_points = [
            (gen_start, GEN_BASE_HEIGHT),
            (gen_start, gen_top),
            (gen_end, gen_top),
            (gen_end, GEN_BASE_HEIGHT),
        ]
        msp.add_lwpolyline(
            gen_points,
            dxfattribs={"layer": "GENERADORES", "closed": True, "lineweight": 25},
        )

        # Etiqueta
        _add_text(
            msp,
            f"GEN {i}",
            (gen_start + GEN_LENGTH / 2, gen_top + 0.2),
            height=0.22,
            layer="TEXTOS",
            align=TextEntityAlignment.BOTTOM_CENTER,
        )


def draw_auxiliary_equipment(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja equipos auxiliares (caldera, intercambiadores, etc.)."""
    # Caldera auxiliar
    boiler_top = BOILER_BASE_HEIGHT + BOILER_DIAMETER

    msp.add_circle(
        (BOILER_START + BOILER_LENGTH / 2, BOILER_BASE_HEIGHT + BOILER_DIAMETER / 2),
        radius=BOILER_DIAMETER / 2,
        dxfattribs={"layer": "EQUIPOS_AUX", "lineweight": 20},
    )

    _add_text(
        msp,
        "CALDERA",
        (BOILER_START + BOILER_LENGTH / 2, boiler_top + 0.2),
        height=0.20,
        layer="TEXTOS",
        align=TextEntityAlignment.BOTTOM_CENTER,
    )

    # Bombas principales (representación esquemática)
    pump_y = DOUBLE_BOTTOM_HEIGHT + 0.3
    pump_positions = [
        ENGINE_ROOM_START + 1.0,
        ENGINE_ROOM_START + 2.0,
        ENGINE_ROOM_END - 1.5,
    ]
    pump_labels = ["BOMBA FO", "BOMBA LO", "BOMBA SW"]

    for x, label in zip(pump_positions, pump_labels):
        msp.add_circle((x, pump_y), radius=0.25, dxfattribs={"layer": "EQUIPOS_AUX"})
        _add_text(
            msp,
            label,
            (x, pump_y + 0.5),
            height=0.18,
            layer="TEXTOS",
            align=TextEntityAlignment.BOTTOM_CENTER,
        )


def draw_dimensions(msp: ezdxf.layouts.Modelspace) -> None:
    """Añade cotas principales al plano."""
    dim_y = -1.5  # Altura de la línea de cota

    # Longitud total de la sala de máquinas
    _add_dimension(
        msp,
        (ENGINE_ROOM_START, dim_y),
        (ENGINE_ROOM_END, dim_y),
        offset=0.5,
    )

    # Altura del doble fondo
    dim_x = ENGINE_ROOM_START - 2.0
    msp.add_linear_dim(
        base=(dim_x, 0.0),
        p1=(dim_x - 0.3, 0.0),
        p2=(dim_x - 0.3, DOUBLE_BOTTOM_HEIGHT),
        dxfattribs={"layer": "COTAS"},
    )

    # Altura total (puntal)
    dim_x = ENGINE_ROOM_END + 2.0
    msp.add_linear_dim(
        base=(dim_x, 0.0),
        p1=(dim_x + 0.3, 0.0),
        p2=(dim_x + 0.3, MAIN_DECK_HEIGHT),
        dxfattribs={"layer": "COTAS"},
    )


def draw_legend(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja leyenda con información del plano."""
    legend_x = ENGINE_ROOM_START
    legend_y = MAIN_DECK_HEIGHT + 2.5

    # Título
    _add_text(
        msp,
        "PLANO LONGITUDINAL - SALA DE MÁQUINAS",
        (legend_x, legend_y),
        height=0.50,
        layer="LEYENDA",
    )

    # Datos del buque
    data_y = legend_y - 0.8
    info_lines = [
        f"Eslora entre PP: {LPP} m",
        f"Manga: {BEAM} m",
        f"Puntal: {DEPTH} m",
        f"Sala de máquinas: {ENGINE_ROOM_LENGTH} m ({ENGINE_ROOM_START}-{ENGINE_ROOM_END} m desde PP popa)",
        f"Escala: 1:100",
        f"Fecha: 6 de noviembre de 2025",
    ]

    for i, line in enumerate(info_lines):
        _add_text(
            msp,
            line,
            (legend_x, data_y - i * 0.4),
            height=0.25,
            layer="LEYENDA",
        )


def draw_reference_axes(msp: ezdxf.layouts.Modelspace) -> None:
    """Dibuja ejes de referencia."""
    # Eje longitudinal (línea de crujía)
    msp.add_line(
        (ENGINE_ROOM_START - 2, 0),
        (ENGINE_ROOM_END + 2, 0),
        dxfattribs={"layer": "EJES", "linetype": "CENTER", "lineweight": 13},
    )

    # Marcas de estaciones (cada 5 m)
    for x in range(int(ENGINE_ROOM_START), int(ENGINE_ROOM_END) + 1, 5):
        if ENGINE_ROOM_START <= x <= ENGINE_ROOM_END:
            msp.add_line(
                (x, -0.3),
                (x, 0.3),
                dxfattribs={"layer": "EJES", "lineweight": 13},
            )
            _add_text(
                msp,
                f"{x}m",
                (x, -0.7),
                height=0.20,
                layer="EJES",
                align=TextEntityAlignment.TOP_CENTER,
            )


def main() -> None:
    """Genera el DXF completo del plano longitudinal de la sala de máquinas."""
    print("=" * 70)
    print("   GENERADOR DE PLANO LONGITUDINAL - SALA DE MÁQUINAS")
    print("=" * 70)
    print()

    # Crear documento DXF
    doc = ezdxf.new("R2010")
    doc.units = units.M
    msp = doc.modelspace()

    print("📐 Creando capas profesionales...")
    _create_layers(doc)

    print("🚢 Dibujando perfil del casco...")
    draw_hull_profile(msp)

    print("🔲 Dibujando mamparos estancos...")
    draw_bulkheads(msp)

    print("⛽ Dibujando doble fondo y tanques...")
    draw_double_bottom_tanks(msp)
    draw_wing_tanks(msp)

    print("⚙️  Dibujando motor principal...")
    draw_main_engine(msp)

    print("🔌 Dibujando generadores...")
    draw_generators(msp)

    print("🔧 Dibujando equipos auxiliares...")
    draw_auxiliary_equipment(msp)

    print("📏 Añadiendo dimensiones...")
    draw_dimensions(msp)

    print("📋 Dibujando leyenda...")
    draw_legend(msp)

    print("📍 Dibujando ejes de referencia...")
    draw_reference_axes(msp)

    print("🔍 Auditando DXF...")
    auditor = doc.audit()
    if auditor.has_fixes:
        print(f"   • Auditoría aplicó {len(auditor.fixes)} correcciones.")
    if auditor.has_errors:
        auditor.print_error_report()
        raise RuntimeError("La auditoría DXF detectó errores fatales. Revisar el log.")

    # Guardar archivo
    print(f"\n💾 Guardando archivo: {DXF_OUTPUT}")
    default_bounds = (
        ENGINE_ROOM_START - 5.0,
        -3.0,
        ENGINE_ROOM_END + 5.0,
        MAIN_DECK_HEIGHT + 3.0,
    )
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
    print("=" * 70)
    print("✅ PLANO GENERADO EXITOSAMENTE")
    print("=" * 70)
    print(f"\n📁 Archivo: {DXF_OUTPUT}")
    print(f"📊 Dimensiones sala de máquinas: {ENGINE_ROOM_LENGTH} m x {BEAM} m x {DEPTH} m")
    print(f"🎯 Vista: Longitudinal (corte por crujía)")
    print(f"📐 Escala recomendada: 1:100")
    print()
    print("💡 Sugerencias:")
    print("   - Abrir en AutoCAD, LibreCAD, QCAD o visor DXF compatible")
    print("   - Verificar capas: CASCO, MOTOR_PRINCIPAL, TANQUES_DB, etc.")
    print("   - Ajustar escala de visualización según necesidad")
    print("   - Exportar a PDF para presentación profesional")
    print()


if __name__ == "__main__":
    main()
