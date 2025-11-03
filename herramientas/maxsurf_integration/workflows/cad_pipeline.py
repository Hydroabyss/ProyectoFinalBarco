from __future__ import annotations

import json
import logging
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Imports opcionales que dependen de la plataforma
TRY_EZDXF = True
try:  # pragma: no cover - import opcional
    import ezdxf  # type: ignore
except Exception:  # pragma: no cover - ezdxf es obligatorio para generar DXF
    ezdxf = None  # type: ignore
    TRY_EZDXF = False

try:  # pragma: no cover - solo disponible en Windows
    import win32com.client  # type: ignore
except Exception:  # pragma: no cover - entorno sin COM
    win32com = None  # type: ignore
else:  # pragma: no cover - alias coherente
    win32com = win32com.client  # type: ignore

from maxsurf_integration.maxsurf_connector import MaxsurfConnector

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

IS_WINDOWS = platform.system().lower().startswith("win")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "cad_integration.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "salidas" / "integracion_cad"
DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class CADIntegrationConfig:
    """Configuración de la integración CAD."""

    output_dir: Path = field(default_factory=lambda: DEFAULT_OUTPUT_DIR)
    dxf_filename: str = "sala_maquinas_integrado.dxf"
    pdf_filename: str = "Plano_Sala_Maquinas_Profesional.pdf"
    title_block_path: Optional[Path] = None
    engine_room_limits: Tuple[float, float] = (82.0, 97.0)
    fallback_hull_data: Dict[str, float] = field(
        default_factory=lambda: {
            "loa": 107.0,
            "lpp": 105.2,
            "beam": 15.99,
            "depth": 7.90,
            "draft": 6.2,
        }
    )
    fallback_bulkheads: List[Tuple[str, float]] = field(
        default_factory=lambda: [
            ("Pique_proa", 0.0),
            ("Mamparo_1", 15.2),
            ("Mamparo_2", 45.6),
            ("Mamparo_3", 76.0),
            ("Mamparo_4", 97.0),
            ("Pique_popa", 105.2),
        ]
    )

    @property
    def dxf_path(self) -> Path:
        return self.output_dir / self.dxf_filename

    @property
    def pdf_path(self) -> Path:
        return self.output_dir / self.pdf_filename


def load_config(path: Optional[Path] = None) -> CADIntegrationConfig:
    """Carga la configuración desde JSON opcional."""

    cfg_path = path or DEFAULT_CONFIG_PATH
    if cfg_path.exists():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - IO
            logger.warning("⚠️  No se pudo leer %s: %s", cfg_path, exc)
        else:
            config = CADIntegrationConfig()
            if "output_dir" in data:
                config.output_dir = Path(data["output_dir"]).expanduser().resolve()
                config.output_dir.mkdir(parents=True, exist_ok=True)
            config.dxf_filename = data.get("dxf_filename", config.dxf_filename)
            config.pdf_filename = data.get("pdf_filename", config.pdf_filename)
            title = data.get("title_block_path")
            if title:
                config.title_block_path = Path(title).expanduser().resolve()
            engine_limits = data.get("engine_room_limits")
            if engine_limits and isinstance(engine_limits, (list, tuple)) and len(engine_limits) == 2:
                config.engine_room_limits = (float(engine_limits[0]), float(engine_limits[1]))
            hull = data.get("fallback_hull_data")
            if isinstance(hull, dict):
                config.fallback_hull_data.update({k: float(v) for k, v in hull.items() if v is not None})
            bulkheads = data.get("fallback_bulkheads")
            if isinstance(bulkheads, list):
                cleaned: List[Tuple[str, float]] = []
                for entry in bulkheads:
                    if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                        cleaned.append((str(entry[0]), float(entry[1])))
                    elif isinstance(entry, dict) and {"name", "position"}.issubset(entry):
                        cleaned.append((str(entry["name"]), float(entry["position"])))
                if cleaned:
                    config.fallback_bulkheads = cleaned
            return config
    return CADIntegrationConfig()


class MaxsurfDataExtractor:
    """Extrae datos geométricos directamente desde Maxsurf vía MaxsurfConnector."""

    def __init__(self, visible: bool = False):
        self.connector = MaxsurfConnector(visible=visible)
        self.model: Any | None = None

    def connect_to_maxsurf(self) -> bool:
        """Conecta a Maxsurf o activa el backend mock."""

        if not self.connector.connect():
            logger.error("❌ No se pudo conectar a Maxsurf")
            return False
        self.model = getattr(self.connector, "model", None)
        if self.model is not None:
            try:
                name = getattr(self.model, "Name", "(sin nombre)")
                logger.info("✅ Conectado a modelo Maxsurf: %s", name)
            except Exception:  # pragma: no cover - atributo opcional
                logger.info("✅ Conectado a Maxsurf")
        else:
            logger.warning("⚠️  No hay modelo activo en Maxsurf")
        return True

    def disconnect(self) -> None:
        self.connector.disconnect()

    def get_hull_geometry(self, fallback: Dict[str, float]) -> Dict[str, float]:
        """Extrae geometría básica del casco desde Maxsurf."""

        if self.model is None:
            logger.info("ℹ️  Usando datos de respaldo para la geometría del casco")
            return dict(fallback)

        geometry: Dict[str, float] = {}
        mapping = {
            "loa": "LengthOverall",
            "lpp": "LengthPerpendiculars",
            "beam": "Beam",
            "depth": "Depth",
            "draft": "DraftDesign",
        }
        for key, attr in mapping.items():
            try:
                geometry[key] = float(getattr(self.model, attr))
            except Exception:
                if key in fallback:
                    geometry[key] = float(fallback[key])
        if not geometry:
            geometry = dict(fallback)
        logger.info("📐 Geometría casco: %s", geometry)
        return geometry

    def get_bulkhead_positions(self, fallback: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """Extrae posiciones de mamparos desde Maxsurf."""

        if self.model is None:
            logger.info("ℹ️  Usando mamparos de respaldo")
            return list(fallback)

        bulkheads: List[Tuple[str, float]] = []
        try:
            collection = getattr(self.model, "Bulkheads", None)
        except Exception:  # pragma: no cover - acceso COM
            collection = None
        if collection is None:
            logger.warning("⚠️  El modelo no expone mamparos; se usan valores de respaldo")
            return list(fallback)

        try:
            count = int(getattr(collection, "Count"))
        except Exception:
            count = 0
        for idx in range(count):
            try:
                bulkhead = collection.Item(idx + 1)
                name = getattr(bulkhead, "Name", f"Mamparo_{idx + 1}")
                position = float(getattr(bulkhead, "Position"))
                bulkheads.append((str(name), position))
            except Exception as exc:  # pragma: no cover - errores COM
                logger.debug("⚠️  No se pudo leer mamparo %s: %s", idx + 1, exc)
        if not bulkheads:
            bulkheads = list(fallback)
        logger.info("🚪 Mamparos extraídos: %d", len(bulkheads))
        return bulkheads


class AutoCADExporter:
    """Exporta y manipula geometría en AutoCAD vía COM. Incluye fallback cuando no está disponible."""

    def __init__(self, title_block_path: Optional[Path] = None):
        self.acad_app: Any | None = None
        self.current_drawing: Any | None = None
        self.title_block_path = title_block_path

    def connect_to_autocad(self) -> bool:
        """Conecta a AutoCAD (solo Windows)."""

        if not IS_WINDOWS or win32com is None:
            logger.info("ℹ️ AutoCAD COM no disponible en esta plataforma; se utilizará flujo offline")
            return False
        try:
            self.acad_app = win32com.Dispatch("AutoCAD.Application")
            self.acad_app.Visible = True
            if self.acad_app.Documents.Count > 0:
                self.current_drawing = self.acad_app.ActiveDocument
            else:
                self.current_drawing = self.acad_app.Documents.Add()
            logger.info("✅ Conectado a AutoCAD")
            return True
        except Exception as exc:  # pragma: no cover - requiere AutoCAD
            logger.error("❌ Error conectando a AutoCAD: %s", exc)
            return False

    def import_dxf_and_enhance(self, dxf_path: Path) -> bool:
        """Importa un DXF y aplica estilos profesionales."""

        if self.current_drawing is None:
            logger.info("ℹ️  AutoCAD no disponible; saltando mejora in-app")
            return False
        try:
            resolved = str(dxf_path.resolve())
            self.current_drawing.SendCommand(f'DXFIN "{resolved}" \n')
            self._apply_professional_styles()
            self._add_title_block()
            self.current_drawing.SendCommand("_REGEN \n")
            self.current_drawing.SendCommand("_ZOOM _E \n")
            logger.info("✅ DXF importado y mejorado en AutoCAD")
            return True
        except Exception as exc:  # pragma: no cover - requiere AutoCAD
            logger.error("❌ Error importando DXF: %s", exc)
            return False

    def _apply_professional_styles(self) -> None:
        if self.current_drawing is None:
            return
        layers_definition = [
            ("CASCO", 1, "Continuous", "0.50mm"),
            ("ESTRUCTURA", 3, "Continuous", "0.30mm"),
            ("MAQUINAS", 2, "Continuous", "0.60mm"),
            ("TANQUES", 6, "Dashed", "0.25mm"),
            ("COTAS", 7, "Continuous", "0.15mm"),
            ("TEXTOS", 4, "Continuous", "0.18mm"),
            ("EQUIPOS", 5, "Continuous", "0.25mm"),
        ]
        for name, color, linetype, lineweight in layers_definition:
            try:
                self.current_drawing.SendCommand(
                    f"-LAYER M {name} C {color} {name} L {linetype} {name} LW {lineweight} {name} \n"
                )
            except Exception as exc:  # pragma: no cover - requiere AutoCAD
                logger.debug("⚠️  No se pudo aplicar estilo a %s: %s", name, exc)

    def _add_title_block(self) -> None:
        if self.current_drawing is None:
            return
        if not self.title_block_path or not self.title_block_path.exists():
            logger.info("ℹ️  Sin cajetín configurado; se omite inserción")
            return
        try:
            block = str(self.title_block_path.resolve())
            self.current_drawing.SendCommand(f'-INSERT "{block}" 0,0 1 1 0 \n')
        except Exception as exc:  # pragma: no cover
            logger.debug("⚠️  No se pudo insertar cajetín: %s", exc)

    def export_to_pdf(self, pdf_path: Path) -> bool:
        if self.current_drawing is None:
            logger.info("ℹ️  AutoCAD no disponible; exportación PDF omitida")
            return False
        plot_sequence = [
            "_PLOT \n",
            "_Y \n",
            "Model \n",
            "DWG To PDF.pc3 \n",
            "A1 \n",
            "_M \n",
            "_L \n",
            "_E \n",
            "1=100 \n",
            "_C \n",
            "_Y \n",
            f"{pdf_path.resolve()} \n",
            "_Y \n",
            "_N \n",
        ]
        try:
            self.current_drawing.SendCommand("".join(plot_sequence))
            logger.info("✅ PDF exportado en %s", pdf_path)
            return True
        except Exception as exc:  # pragma: no cover
            logger.error("❌ Error exportando PDF: %s", exc)
            return False


def _ensure_ezdxf() -> None:
    if not TRY_EZDXF or ezdxf is None:  # pragma: no cover - dependencias
        raise RuntimeError(
            "ezdxf es obligatorio para generar el DXF integrado. Ejecuta 'pip install ezdxf'."
        )


def _add_text(msp: Any, text: str, insert: Tuple[float, float], layer: str, height: float = 0.25, align: str = "CENTER") -> None:
    try:
        entity = msp.add_text(text, dxfattribs={"layer": layer, "height": height})
        entity.set_pos(insert, align=align)
    except Exception as exc:  # pragma: no cover - fallback gráfico
        logger.debug("⚠️  No se pudo añadir texto '%s': %s", text, exc)


def build_dxf_from_cad_systems(config: Optional[CADIntegrationConfig] = None) -> Path:
    """Genera el DXF principal integrando datos reales de Maxsurf."""

    cfg = config or load_config()
    cfg.output_dir.mkdir(parents=True, exist_ok=True)

    _ensure_ezdxf()
    from ezdxf import units as ez_units  # import local para evitar fallo global

    logger.info("🚀 Generando DXF integrado con sistemas CAD...")

    extractor = MaxsurfDataExtractor()
    if extractor.connect_to_maxsurf():
        hull_data = extractor.get_hull_geometry(cfg.fallback_hull_data)
        bulkheads = extractor.get_bulkhead_positions(cfg.fallback_bulkheads)
    else:
        hull_data = dict(cfg.fallback_hull_data)
        bulkheads = list(cfg.fallback_bulkheads)
    extractor.disconnect()

    doc = ezdxf.new("R2010")
    doc.units = ez_units.M
    msp = doc.modelspace()

    for layer_name, color in [
        ("CASCO", 1),
        ("ESTRUCTURA", 3),
        ("MAQUINAS", 2),
        ("TANQUES", 6),
        ("EQUIPOS", 5),
        ("TEXTOS", 4),
        ("COTAS", 7),
    ]:
        if layer_name not in doc.layers:
            doc.layers.add(layer_name, color=color)

    lpp = float(hull_data.get("lpp", cfg.fallback_hull_data["lpp"]))
    beam = float(hull_data.get("beam", cfg.fallback_hull_data["beam"]))
    depth = float(hull_data.get("depth", cfg.fallback_hull_data["depth"]))
    draft = float(hull_data.get("draft", cfg.fallback_hull_data["draft"]))
    engine_start, engine_end = cfg.engine_room_limits
    half_beam = beam / 2.0

    plan_outline = [
        (0.0, -half_beam),
        (0.0, half_beam),
        (lpp, half_beam),
        (lpp, -half_beam),
    ]
    msp.add_lwpolyline(plan_outline, dxfattribs={"layer": "CASCO", "closed": True})

    for name, pos in bulkheads:
        msp.add_line((pos, -half_beam), (pos, half_beam), dxfattribs={"layer": "ESTRUCTURA"})
        _add_text(msp, name, (pos, half_beam + 0.8), layer="TEXTOS", height=0.3, align="BOTTOM_CENTER")

    engine_rect = [
        (engine_start, -half_beam),
        (engine_start, half_beam),
        (engine_end, half_beam),
        (engine_end, -half_beam),
    ]
    msp.add_lwpolyline(engine_rect, dxfattribs={"layer": "MAQUINAS", "closed": True})

    motor_length, motor_width = 8.5, 3.2
    motor_center_x = engine_start + ((engine_end - engine_start) - motor_length) / 2.0
    motor_rect = [
        (motor_center_x, -motor_width / 2.0),
        (motor_center_x + motor_length, -motor_width / 2.0),
        (motor_center_x + motor_length, motor_width / 2.0),
        (motor_center_x, motor_width / 2.0),
    ]
    msp.add_lwpolyline(motor_rect, dxfattribs={"layer": "EQUIPOS", "closed": True})
    _add_text(
        msp,
        "MOTOR 16V26",
        (motor_center_x + motor_length / 2.0, motor_width / 2.0 + 0.4),
        layer="TEXTOS",
        height=0.25,
    )

    section_offset_x = lpp + 8.0
    section_points = [
        (-half_beam, 0),
        (-half_beam, draft * 0.7),
        (-(half_beam - 1.5), draft * 0.9),
        (-(half_beam - 1.8), depth),
        ((half_beam - 1.8), depth),
        ((half_beam - 1.5), draft * 0.9),
        (half_beam, draft * 0.7),
        (half_beam, 0),
    ]
    section_points_offset = [(x + section_offset_x, y) for x, y in section_points]
    msp.add_lwpolyline(section_points_offset, dxfattribs={"layer": "CASCO", "closed": True})

    db_height = 1.2
    db_section = [
        (-(half_beam - 1.8), 0),
        (-(half_beam - 1.8), db_height),
        ((half_beam - 1.8), db_height),
        ((half_beam - 1.8), 0),
    ]
    db_section_offset = [(x + section_offset_x, y) for x, y in db_section]
    msp.add_lwpolyline(db_section_offset, dxfattribs={"layer": "TANQUES", "closed": True})

    elevation_offset_y = depth + 6.0
    profile_points = [
        (0.0, elevation_offset_y),
        (0.0, elevation_offset_y + draft),
        (lpp, elevation_offset_y + draft),
        (lpp, elevation_offset_y),
    ]
    msp.add_lwpolyline(profile_points, dxfattribs={"layer": "CASCO", "closed": True})

    _add_text(
        msp,
        "Sala de máquinas",
        ((engine_start + engine_end) / 2.0, -half_beam - 1.2),
        layer="TEXTOS",
        height=0.35,
    )

    hull_snapshot = {
        "hull_data": hull_data,
        "bulkheads": bulkheads,
        "engine_room": {
            "start": engine_start,
            "end": engine_end,
        },
    }
    snapshot_path = cfg.output_dir / "metadata_sala_maquinas.json"
    snapshot_path.write_text(json.dumps(hull_snapshot, indent=2), encoding="utf-8")

    doc.saveas(cfg.dxf_path)
    logger.info("✅ DXF generado en %s", cfg.dxf_path)
    return cfg.dxf_path


def full_cad_integration_pipeline(config: Optional[CADIntegrationConfig] = None) -> Dict[str, Path]:
    """Ejecuta el pipeline completo: Maxsurf ➜ DXF ➜ AutoCAD ➜ PDF."""

    cfg = config or load_config()
    outputs: Dict[str, Path] = {}

    dxf_path = build_dxf_from_cad_systems(cfg)
    outputs["dxf"] = dxf_path

    exporter = AutoCADExporter(title_block_path=cfg.title_block_path)
    if exporter.connect_to_autocad():
        if exporter.import_dxf_and_enhance(dxf_path):
            if exporter.export_to_pdf(cfg.pdf_path):
                outputs["pdf"] = cfg.pdf_path
    else:
        logger.info("ℹ️  Pipeline detenido en etapa AutoCAD (no disponible)")

    return outputs


def quick_autocad_export(dxf_path: Optional[Path] = None) -> Optional[Path]:
    """Proporciona una exportación rápida a DWG usando AutoCAD si está disponible."""

    if not IS_WINDOWS or win32com is None:
        logger.info("ℹ️  AutoCAD no disponible para exportación rápida")
        return None
    try:
        acad = win32com.Dispatch("AutoCAD.Application")
        acad.Visible = True
        doc = acad.ActiveDocument
        resolved = str((dxf_path or DEFAULT_OUTPUT_DIR / "sala_maquinas_integrado.dxf").resolve())
        doc.SendCommand(f'DXFIN "{resolved}" \n')
        dwg_path = DEFAULT_OUTPUT_DIR / "Plano_Sala_Maquinas.dwg"
        doc.SaveAs(str(dwg_path))
        logger.info("✅ DXF importado y guardado como DWG en %s", dwg_path)
        return dwg_path
    except Exception as exc:  # pragma: no cover
        logger.error("❌ Error en exportación rápida: %s", exc)
        return None


if __name__ == "__main__":  # pragma: no cover - CLI manual
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    resultados = full_cad_integration_pipeline()
    print("Archivos generados:")
    for clave, ruta in resultados.items():
        print(f" - {clave}: {ruta}")
