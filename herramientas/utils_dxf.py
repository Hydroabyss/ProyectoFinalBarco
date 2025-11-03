"""Utilidades comunes para generar DXF con límites configurados."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Optional, Tuple

from ezdxf import bbox, units, zoom
from ezdxf.layouts import Layout
from ezdxf.math import Vec3

DEFAULT_MARGIN_MIN = 1.0


def _sanitize_defaults(
    default_bounds: Optional[Tuple[float, float, float, float]],
) -> Tuple[float, float, float, float]:
    if (
        not default_bounds
        or len(default_bounds) != 4
        or default_bounds[2] <= default_bounds[0]
        or default_bounds[3] <= default_bounds[1]
    ):
        return (-10.0, -10.0, 10.0, 10.0)
    return tuple(map(float, default_bounds))  # type: ignore[return-value]


def _compute_layout_extents(
    layout: Layout,
    default_bounds: Optional[Tuple[float, float, float, float]] = None,
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """Calcula los límites del layout aplicando márgenes de seguridad."""
    try:
        box = bbox.extents(layout, fast=True)
    except Exception:
        box = None

    if box and box.has_data:
        xmin, ymin = float(box.extmin.x), float(box.extmin.y)
        xmax, ymax = float(box.extmax.x), float(box.extmax.y)
    else:
        xmin, ymin, xmax, ymax = _sanitize_defaults(default_bounds)

    width = max(xmax - xmin, 10.0)
    height = max(ymax - ymin, 10.0)

    margin_x = max(width * 0.05, DEFAULT_MARGIN_MIN)
    margin_y = max(height * 0.05, DEFAULT_MARGIN_MIN)

    extmin = (xmin - margin_x, ymin - margin_y, 0.0)
    extmax = (xmax + margin_x, ymax + margin_y, 0.0)
    return extmin, extmax


def _rewrite_extents(
    lines: list[str],
    var_name: str,
    values: Tuple[float, float, float],
) -> None:
    for idx, line in enumerate(lines):
        if line.strip() == var_name and idx + 6 < len(lines):
            lines[idx + 2] = f"{values[0]}"
            lines[idx + 4] = f"{values[1]}"
            lines[idx + 6] = f"{values[2]}"
            break


def _rewrite_extents_in_file(
    path: Path,
    extmin: Tuple[float, float, float],
    extmax: Tuple[float, float, float],
    include_paper: bool = True,
) -> None:
    if not path.exists():
        return

    try:
        lines = path.read_text().splitlines()
    except OSError:
        return

    _rewrite_extents(lines, "$EXTMIN", extmin)
    _rewrite_extents(lines, "$EXTMAX", extmax)

    if include_paper:
        _rewrite_extents(lines, "$PEXTMIN", extmin)
        _rewrite_extents(lines, "$PEXTMAX", extmax)

    path.write_text("\n".join(lines) + "\n")


def save_dxf_with_extents(
    doc,
    path: Path,
    layout: Optional[Layout] = None,
    default_bounds: Optional[Tuple[float, float, float, float]] = None,
    include_paper_space: bool = True,
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """Guarda el DXF y fuerza los límites $EXTMIN/$EXTMAX."""
    layout = layout or doc.modelspace()
    extmin, extmax = _compute_layout_extents(layout, default_bounds)

    doc.units = units.M
    doc.header["$INSUNITS"] = units.M
    doc.header["$MEASUREMENT"] = 1
    doc.header["$EXTMIN"] = Vec3(*extmin)
    doc.header["$EXTMAX"] = Vec3(*extmax)
    try:
        zoom.window(layout, (extmin[0], extmin[1]), (extmax[0], extmax[1]))
    except Exception:
        pass

    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(path)
    _rewrite_extents_in_file(
        path, extmin, extmax, include_paper=include_paper_space
    )
    return extmin, extmax
