"""Genera un DXF con planta, alzado y sección transversal de la cámara de máquinas."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import ezdxf
from ezdxf import units
from ezdxf.enums import TextEntityAlignment

from utils_dxf import save_dxf_with_extents


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "salidas" / "disposicion_general"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DXF_OUTPUT = OUTPUT_DIR / "Camara_Maquinas_Multivista.dxf"

# Parámetros globales (se leerán de configuración en futuras iteraciones)
LPP = 105.2  # m
BEAM = 15.99  # m
DEPTH = 7.90  # m
DRAFT = 6.20  # m

# Sala de máquinas
ENGINE_ROOM_START = 8.20  # m desde PP de popa
ENGINE_ROOM_END = 23.20
ENGINE_ROOM_LENGTH = ENGINE_ROOM_END - ENGINE_ROOM_START

# Doble fondo y costado
DOUBLE_BOTTOM_HEIGHT = 1.20  # m
DOUBLE_SIDE_WIDTH = 1.80  # m por banda
HALF_BEAM = BEAM / 2
INNER_HALF_BEAM = HALF_BEAM - DOUBLE_SIDE_WIDTH

# Tanques
WING_TANK_START = 10.20
WING_TANK_END = 22.20
DOUBLE_BOTTOM_VOLUME = 149.96  # m3
WING_TANK_VOLUME = 113.31  # m3 por tanque

# Equipos principales
MOTOR_LENGTH = 8.50
MOTOR_WIDTH = 3.20
MOTOR_HEIGHT = 4.00

GENERATOR_LENGTH = 3.00
GENERATOR_WIDTH = 1.60

# Offsets para ubicar vistas en el DXF
PLAN_OFFSET = (0.0, 0.0)
SECTION_OFFSET = (ENGINE_ROOM_LENGTH + 25.0, 0.0)
ELEVATION_OFFSET = (0.0, -DEPTH - 12.0)


def _to_plan(x: float, y: float) -> tuple[float, float]:
    """Transforma coordenadas reales a la vista en planta (zona positiva cerca del origen)."""

    return PLAN_OFFSET[0] + (x - ENGINE_ROOM_START), PLAN_OFFSET[1] + y


def _to_section(y: float, z: float) -> tuple[float, float]:
    """Transforma coordenadas a la vista de sección transversal (Y-Z)."""

    return SECTION_OFFSET[0] + y, SECTION_OFFSET[1] + z


def _to_elevation(x: float, z: float) -> tuple[float, float]:
    """Transforma coordenadas a la vista longitudinal (X-Z)."""

    return ELEVATION_OFFSET[0] + (x - ENGINE_ROOM_START), ELEVATION_OFFSET[1] + z


def _add_text(
    msp: ezdxf.layouts.Modelspace,
    text: str,
    position: Sequence[float],
    *,
    height: float = 0.35,
    layer: str = "TEXTOS",
    align: TextEntityAlignment = TextEntityAlignment.LEFT,
) -> None:
    msp.add_text(text, dxfattribs={"height": height, "layer": layer}).set_placement(position, align=align)


def _create_layers(doc: ezdxf.EzdxfDocument) -> None:
    layers = {
        "CASCO": 1,
        "ESTRUCTURA": 2,
        "TANQUES": 3,
        "EQUIPOS": 4,
        "TEXTOS": 7,
        "DIMENSIONES": 140,
        "LEYENDA": 30,
    }
    for name, color in layers.items():
        if name not in doc.layers:
            doc.layers.add(name=name, color=color)


def _lwpolyline(
    msp: ezdxf.layouts.Modelspace,
    points: Iterable[tuple[float, float]],
    *,
    layer: str,
    closed: bool = True,
) -> None:
    pts = list(points)
    if closed and pts and pts[0] != pts[-1]:
        pts.append(pts[0])
    msp.add_lwpolyline(pts, dxfattribs={"layer": layer}, close=closed)


def _draw_plan_view(msp: ezdxf.layouts.Modelspace) -> None:
    """Vista en planta de la sala de máquinas con tanques y equipos principales."""

    outline = [
        _to_plan(ENGINE_ROOM_START, -HALF_BEAM),
        _to_plan(ENGINE_ROOM_START, HALF_BEAM),
        _to_plan(ENGINE_ROOM_END, HALF_BEAM),
        _to_plan(ENGINE_ROOM_END, -HALF_BEAM),
    ]
    _lwpolyline(msp, outline, layer="CASCO")

    inner_lines = [
        (_to_plan(ENGINE_ROOM_START, INNER_HALF_BEAM), _to_plan(ENGINE_ROOM_END, INNER_HALF_BEAM)),
        (_to_plan(ENGINE_ROOM_START, -INNER_HALF_BEAM), _to_plan(ENGINE_ROOM_END, -INNER_HALF_BEAM)),
    ]
    for start, end in inner_lines:
        msp.add_line(start, end, dxfattribs={"layer": "ESTRUCTURA"})

    wing_rects = [
        (
            _to_plan(WING_TANK_START, -HALF_BEAM),
            _to_plan(WING_TANK_END, -HALF_BEAM),
            _to_plan(WING_TANK_END, -INNER_HALF_BEAM),
            _to_plan(WING_TANK_START, -INNER_HALF_BEAM),
        ),
        (
            _to_plan(WING_TANK_START, INNER_HALF_BEAM),
            _to_plan(WING_TANK_END, INNER_HALF_BEAM),
            _to_plan(WING_TANK_END, HALF_BEAM),
            _to_plan(WING_TANK_START, HALF_BEAM),
        ),
    ]
    for rect in wing_rects:
        _lwpolyline(msp, rect, layer="TANQUES")

    motor_x0 = ENGINE_ROOM_START + (ENGINE_ROOM_LENGTH - MOTOR_LENGTH) / 2
    motor_poly = [
        _to_plan(motor_x0, -MOTOR_WIDTH / 2),
        _to_plan(motor_x0 + MOTOR_LENGTH, -MOTOR_WIDTH / 2),
        _to_plan(motor_x0 + MOTOR_LENGTH, MOTOR_WIDTH / 2),
        _to_plan(motor_x0, MOTOR_WIDTH / 2),
    ]
    _lwpolyline(msp, motor_poly, layer="EQUIPOS")
    _add_text(
        msp,
        "Motor principal 16V26",
        _to_plan(motor_x0 + MOTOR_LENGTH / 2, 0.0),
        height=0.32,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )

    generators = [
        ("Generador aux. babor", ENGINE_ROOM_START + 2.0, -INNER_HALF_BEAM + 0.4),
        ("Generador aux. estribor", ENGINE_ROOM_START + 2.0, INNER_HALF_BEAM - GENERATOR_WIDTH - 0.4),
    ]
    for name, gx, gy in generators:
        rect = [
            _to_plan(gx, gy),
            _to_plan(gx + GENERATOR_LENGTH, gy),
            _to_plan(gx + GENERATOR_LENGTH, gy + GENERATOR_WIDTH),
            _to_plan(gx, gy + GENERATOR_WIDTH),
        ]
        _lwpolyline(msp, rect, layer="EQUIPOS")
        _add_text(
            msp,
            name,
            _to_plan(gx + GENERATOR_LENGTH / 2, gy + GENERATOR_WIDTH / 2),
            height=0.25,
            align=TextEntityAlignment.MIDDLE_CENTER,
        )

    _add_text(
        msp,
        "Wing tank estribor (113 m³)",
        _to_plan((WING_TANK_START + WING_TANK_END) / 2, HALF_BEAM - 0.8),
        height=0.26,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )
    _add_text(
        msp,
        "Wing tank babor (113 m³)",
        _to_plan((WING_TANK_START + WING_TANK_END) / 2, -HALF_BEAM + 0.8),
        height=0.26,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )

    _add_text(
        msp,
        "Sala de máquinas – vista en planta",
        _to_plan(ENGINE_ROOM_START, HALF_BEAM + 1.5),
        height=0.38,
    )


def _draw_transverse_section(msp: ezdxf.layouts.Modelspace) -> None:
    section_points = [
        (-HALF_BEAM, 0.0),
        (-HALF_BEAM, DRAFT * 0.65),
        (-(HALF_BEAM - 0.9), DRAFT * 0.85),
        (-INNER_HALF_BEAM, DEPTH),
        (INNER_HALF_BEAM, DEPTH),
        (HALF_BEAM - 0.9, DRAFT * 0.85),
        (HALF_BEAM, DRAFT * 0.65),
        (HALF_BEAM, 0.0),
    ]
    _lwpolyline(msp, (_to_section(y, z) for y, z in section_points), layer="CASCO")

    db_poly = [
        (-INNER_HALF_BEAM, 0.0),
        (-INNER_HALF_BEAM, DOUBLE_BOTTOM_HEIGHT),
        (INNER_HALF_BEAM, DOUBLE_BOTTOM_HEIGHT),
        (INNER_HALF_BEAM, 0.0),
    ]
    _lwpolyline(msp, (_to_section(y, z) for y, z in db_poly), layer="ESTRUCTURA")

    wing_port = [
        (-HALF_BEAM, 0.0),
        (-HALF_BEAM, DOUBLE_BOTTOM_HEIGHT + 2.0),
        (-INNER_HALF_BEAM, DOUBLE_BOTTOM_HEIGHT),
        (-INNER_HALF_BEAM, 0.0),
    ]
    wing_starboard = [
        (INNER_HALF_BEAM, 0.0),
        (INNER_HALF_BEAM, DOUBLE_BOTTOM_HEIGHT),
        (HALF_BEAM, DOUBLE_BOTTOM_HEIGHT + 2.5),
        (HALF_BEAM, 0.0),
    ]
    _lwpolyline(msp, (_to_section(y, z) for y, z in wing_port), layer="TANQUES")
    _lwpolyline(msp, (_to_section(y, z) for y, z in wing_starboard), layer="TANQUES")

    platforms = [
        (-INNER_HALF_BEAM + 0.8, DOUBLE_BOTTOM_HEIGHT + 2.2, INNER_HALF_BEAM - 0.8, DOUBLE_BOTTOM_HEIGHT + 2.2, "Plataforma generadores"),
        (-INNER_HALF_BEAM + 0.5, DOUBLE_BOTTOM_HEIGHT + 4.7, INNER_HALF_BEAM - 0.5, DOUBLE_BOTTOM_HEIGHT + 4.7, "Plataforma tableros"),
    ]
    for y1, z1, y2, z2, label in platforms:
        start = _to_section(y1, z1)
        end = _to_section(y2, z2)
        msp.add_line(start, end, dxfattribs={"layer": "ESTRUCTURA"})
        _add_text(
            msp,
            label,
            ((start[0] + end[0]) / 2, start[1] + 0.25),
            height=0.25,
            align=TextEntityAlignment.MIDDLE_CENTER,
        )

    _add_text(
        msp,
        "Sección transversal – sala de máquinas",
        _to_section(-HALF_BEAM, DEPTH + 0.8),
        height=0.38,
    )
    _add_text(
        msp,
        f"Volumen DB máquina: {DOUBLE_BOTTOM_VOLUME:.1f} m³",
        _to_section(-HALF_BEAM, -1.2),
        height=0.28,
    )


def _draw_longitudinal_elevation(msp: ezdxf.layouts.Modelspace) -> None:
    baseline = [_to_elevation(ENGINE_ROOM_START, 0.0), _to_elevation(ENGINE_ROOM_END, 0.0)]
    db_line = [_to_elevation(ENGINE_ROOM_START, DOUBLE_BOTTOM_HEIGHT), _to_elevation(ENGINE_ROOM_END, DOUBLE_BOTTOM_HEIGHT)]
    deck_line = [_to_elevation(ENGINE_ROOM_START, DEPTH), _to_elevation(ENGINE_ROOM_END, DEPTH)]

    msp.add_line(*baseline, dxfattribs={"layer": "CASCO"})
    msp.add_line(*db_line, dxfattribs={"layer": "ESTRUCTURA"})
    msp.add_line(*deck_line, dxfattribs={"layer": "CASCO"})

    for x, label in ((ENGINE_ROOM_START, "Mamparo popa"), (ENGINE_ROOM_END, "Mamparo proa")):
        start = _to_elevation(x, 0.0)
        end = _to_elevation(x, DEPTH)
        msp.add_line(start, end, dxfattribs={"layer": "ESTRUCTURA"})
        _add_text(
            msp,
            label,
            (start[0] + 0.2, start[1] + DEPTH + 0.3),
            height=0.28,
        )

    motor_x0 = ENGINE_ROOM_START + (ENGINE_ROOM_LENGTH - MOTOR_LENGTH) / 2
    motor_poly = [
        _to_elevation(motor_x0, DOUBLE_BOTTOM_HEIGHT),
        _to_elevation(motor_x0 + MOTOR_LENGTH, DOUBLE_BOTTOM_HEIGHT),
        _to_elevation(motor_x0 + MOTOR_LENGTH, DOUBLE_BOTTOM_HEIGHT + MOTOR_HEIGHT),
        _to_elevation(motor_x0, DOUBLE_BOTTOM_HEIGHT + MOTOR_HEIGHT),
    ]
    _lwpolyline(msp, motor_poly, layer="EQUIPOS")
    _add_text(
        msp,
        "Motor 16V26",
        _to_elevation(motor_x0 + MOTOR_LENGTH / 2, DOUBLE_BOTTOM_HEIGHT + MOTOR_HEIGHT + 0.4),
        height=0.30,
        align=TextEntityAlignment.MIDDLE_CENTER,
    )

    shaft_height = DOUBLE_BOTTOM_HEIGHT + 0.60
    msp.add_line(
        _to_elevation(ENGINE_ROOM_START, shaft_height),
        _to_elevation(ENGINE_ROOM_START - 3.0, shaft_height),
        dxfattribs={"layer": "EQUIPOS"},
    )
    support_poly = [
        _to_elevation(ENGINE_ROOM_START - 1.0, shaft_height - 0.25),
        _to_elevation(ENGINE_ROOM_START - 0.4, shaft_height - 0.25),
        _to_elevation(ENGINE_ROOM_START - 0.2, shaft_height + 0.25),
        _to_elevation(ENGINE_ROOM_START - 0.8, shaft_height + 0.25),
    ]
    _lwpolyline(msp, support_poly, layer="EQUIPOS")
    _add_text(
        msp,
        "Línea de eje",
        _to_elevation(ENGINE_ROOM_START - 1.5, shaft_height + 0.25),
        height=0.26,
    )

    _add_text(
        msp,
        "Vista longitudinal – plano diametral",
        _to_elevation(ENGINE_ROOM_START, DEPTH + 1.2),
        height=0.38,
    )


def _add_dimensions(msp: ezdxf.layouts.Modelspace) -> None:
    start = _to_plan(ENGINE_ROOM_START, HALF_BEAM + 0.8)
    end = _to_plan(ENGINE_ROOM_END, HALF_BEAM + 0.8)
    msp.add_line(start, end, dxfattribs={"layer": "DIMENSIONES"})
    _add_text(
        msp,
        f"L sala = {ENGINE_ROOM_LENGTH:.2f} m",
        ((start[0] + end[0]) / 2, start[1] + 0.3),
        height=0.28,
        layer="DIMENSIONES",
        align=TextEntityAlignment.MIDDLE_CENTER,
    )

    sec_start = _to_section(-HALF_BEAM - 1.0, 0.0)
    sec_end = _to_section(-HALF_BEAM - 1.0, DEPTH)
    msp.add_line(sec_start, sec_end, dxfattribs={"layer": "DIMENSIONES"})
    _add_text(
        msp,
        f"Puntal = {DEPTH:.2f} m",
        (sec_start[0] - 0.4, (sec_start[1] + sec_end[1]) / 2),
        height=0.28,
        layer="DIMENSIONES",
    )

    elev_start = _to_elevation(ENGINE_ROOM_END + 0.8, 0.0)
    elev_end = _to_elevation(ENGINE_ROOM_END + 0.8, DOUBLE_BOTTOM_HEIGHT)
    msp.add_line(elev_start, elev_end, dxfattribs={"layer": "DIMENSIONES"})
    _add_text(
        msp,
        f"h DB = {DOUBLE_BOTTOM_HEIGHT:.2f} m",
        (elev_start[0] + 0.3, (elev_start[1] + elev_end[1]) / 2),
        height=0.28,
        layer="DIMENSIONES",
    )


def _add_legend(msp: ezdxf.layouts.Modelspace) -> None:
    legend_origin = (PLAN_OFFSET[0], ELEVATION_OFFSET[1] - 6.0)
    legend = [
        f"Proyecto: Buque carga general – Lpp {LPP:.2f} m",
        f"Sala de máquinas: {ENGINE_ROOM_LENGTH:.2f} m (de {ENGINE_ROOM_START:.1f} a {ENGINE_ROOM_END:.1f} m)",
        f"Manga interior entre forros: {INNER_HALF_BEAM * 2:.2f} m",
        f"Doble fondo: {DOUBLE_BOTTOM_HEIGHT:.2f} m | Volumen {DOUBLE_BOTTOM_VOLUME:.1f} m³",
        f"Wing tanks: {WING_TANK_VOLUME:.2f} m³ por banda",
        "Motor Wärtsilä 16V26 – 8.5 × 3.2 × 4.0 m",
    ]
    y = legend_origin[1]
    for line in legend:
        _add_text(msp, line, (legend_origin[0], y), height=0.28, layer="LEYENDA")
        y -= 0.45


def build_dxf_engine_room() -> Path:
    doc = ezdxf.new("R2010")
    doc.units = units.M
    _create_layers(doc)
    msp = doc.modelspace()

    _draw_plan_view(msp)
    _draw_transverse_section(msp)
    _draw_longitudinal_elevation(msp)
    _add_dimensions(msp)
    _add_legend(msp)

    print(f"Guardando DXF multivista en: {DXF_OUTPUT}")
    default_bounds = (
        min(PLAN_OFFSET[0] - 5.0, ELEVATION_OFFSET[0] - 5.0),
        ELEVATION_OFFSET[1] - 10.0,
        SECTION_OFFSET[0] + HALF_BEAM + 10.0,
        PLAN_OFFSET[1] + HALF_BEAM + 10.0,
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

    return DXF_OUTPUT


def main() -> None:
    output = build_dxf_engine_room()
    print(f"DXF multivista generado en: {output}")


if __name__ == "__main__":
    main()
