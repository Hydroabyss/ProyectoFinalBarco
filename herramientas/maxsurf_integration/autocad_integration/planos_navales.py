from __future__ import annotations

from pathlib import Path
from typing import Any, List

import os

try:
    import win32com.client  # type: ignore
    import pythoncom  # type: ignore
except Exception:  # pragma: no cover
    win32com = None  # type: ignore
    pythoncom = None  # type: ignore

try:
    import ezdxf
except Exception:  # pragma: no cover
    ezdxf = None  # type: ignore


class GeneradorPlanosNavales:
    """Integración AutoCAD con fallback DXF local (ezdxf) para macOS.

    - En Windows: intenta abrir AutoCAD via COM
    - En macOS/Linux: genera DXF offline con ezdxf (sin AutoCAD)
    """

    def __init__(self, maxsurf: Any | None = None):
        self.maxsurf = maxsurf
        self.autocad = None
        self.doc = None

    # -------- Conexión AutoCAD (Windows) --------
    def conectar_autocad(self) -> bool:
        if win32com is None:
            print("ℹ️ COM no disponible; usaré DXF offline (ezdxf)")
            return False
        try:
            self.autocad = win32com.Dispatch("AutoCAD.Application")
            self.autocad.Visible = True
            self.doc = self.autocad.ActiveDocument
            print("📐 AutoCAD conectado - Listo para generación de planos")
            return True
        except Exception as e:  # pragma: no cover
            print(f"❌ Error conectando AutoCAD: {e}")
            return False

    # -------- Exportación / Importación --------
    def exportar_vista_maxsurf(self, vista: str, nombre_plano: str, out_dir: str | Path = "./salidas/autocad") -> str:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dxf_path = out_dir / f"{nombre_plano}.dxf"
        # Si no hay Maxsurf real, Crear DXF dummy con capa y texto
        if ezdxf is None:
            raise RuntimeError("ezdxf no disponible para generar DXF")
        doc = ezdxf.new("R2010")
        msp = doc.modelspace()
        msp.add_text(f"Vista {vista} exportada", dxfattribs={"height": 0.35})
        doc.saveas(dxf_path)
        return str(dxf_path)

    # -------- Plano de construcción (simplificado) --------
    def crear_plano_construccion(self, eslora: float, manga: float, escala: float = 1.50, out_dir: str | Path = "./salidas/autocad") -> str:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dxf_path = out_dir / "plano_construccion.dxf"
        if ezdxf is None:
            raise RuntimeError("ezdxf no disponible para generar DXF")
        doc = ezdxf.new("R2010")
        msp = doc.modelspace()
        # Perfil: cubierta y quilla
        self._crear_linea(msp, (0, 0), (eslora * escala, 0), layer="C-CUBIERTA")
        self._crear_linea(msp, (0, -0.2 * escala), (eslora * escala, -0.2 * escala), layer="C-QUILLA")
        # Cuadernas principales
        for estacion in [i / 10 for i in range(11)]:
            x = estacion * eslora * escala
            self._crear_linea(msp, (x, -0.2 * escala), (x, 0.5 * escala), layer="C-CUADERNAS")
        doc.saveas(dxf_path)
        return str(dxf_path)

    # -------- Plano de líneas (perfil, planta, sección maestra) --------
    def crear_plano_lineas(self, eslora: float, manga: float, calado: float, escala: float = 1.0, out_dir: str | Path = "./salidas/autocad") -> str:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dxf_path = out_dir / "plano_lineas.dxf"
        if ezdxf is None:
            raise RuntimeError("ezdxf no disponible para generar DXF")
        doc = ezdxf.new("R2010")
        msp = doc.modelspace()
        # Perfil: línea de flotación curva suave (parábola simple)
        puntos_lf = []
        for i in range(21):
            x = (i / 20) * eslora * escala
            y = calado * escala * (1 - ((x - (eslora * escala) / 2) / ((eslora * escala) / 2)) ** 2)
            puntos_lf.append((x, y))
        msp.add_lwpolyline(puntos_lf, dxfattribs={"layer": "C-LFLOT"})
        # Líneas de agua adicionales (0.25T, 0.5T, 0.75T)
        for frac in (0.25, 0.5, 0.75):
            y = calado * escala * frac
            self._crear_linea(msp, (0, y), (eslora * escala, y), layer="C-WATER")
        # Planta: contorno elíptico simple
        rx = (eslora * escala) / 2
        ry = (manga * escala) / 2
        msp.add_ellipse(center=(rx, 0), major_axis=(rx, 0), ratio=ry / rx if rx else 1.0, dxfattribs={"layer": "C-PLANTA"})
        # Buttocks (±0.25B)
        for sign in (-1, 1):
            yb = sign * (manga * escala * 0.25)
            self._crear_linea(msp, (0, yb), (eslora * escala, yb), layer="C-BUTT")
        # Sección maestra: semielipse (polilínea) centrada en x = cx
        cx = eslora * escala * 0.5
        semi = []
        for i in range(0, 181, 6):
            ang = i * 3.14159265 / 180.0
            px = cx + (manga * escala / 2.0) * ( (i - 90) / 90.0 ) * 0.0  # simplificación: eje vertical
            py = (calado * escala) * ( (i) / 180.0 )
            semi.append((px, py))
        # Columna central para altura máxima (referencia)
        self._crear_linea(msp, (cx, 0), (cx, calado * escala), layer="C-SECCION")
        # Diagonales cruzadas alrededor de la sección
        diag_w = manga * escala * 0.4
        self._crear_linea(msp, (cx - diag_w, 0), (cx + diag_w, calado * escala), layer="C-DIAG")
        self._crear_linea(msp, (cx - diag_w, calado * escala), (cx + diag_w, 0), layer="C-DIAG")
        # Cuadernas como rejilla en perfil
        for estacion in [i / 10 for i in range(11)]:
            x = estacion * eslora * escala
            self._crear_linea(msp, (x, -0.1 * escala), (x, calado * escala), layer="C-CUAD")
        # Anotaciones básicas
        try:
            msp.add_text(
                f"Plano de Líneas (L={eslora}m, B={manga}m, T={calado}m)",
                dxfattribs={"height": 0.35, "layer": "C-COTA"},
            ).set_pos((0, -1.8 * escala))
        except Exception:
            pass
        doc.saveas(dxf_path)
        return str(dxf_path)

    # -------- Plano de cuadernas (rejilla simple con etiquetas) --------
    def crear_plano_cuadernas(self, eslora: float, manga: float, escala: float = 1.0, n_estaciones: int = 11, out_dir: str | Path = "./salidas/autocad") -> str:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dxf_path = out_dir / "plano_cuadernas.dxf"
        if ezdxf is None:
            raise RuntimeError("ezdxf no disponible para generar DXF")
        doc = ezdxf.new("R2010")
        msp = doc.modelspace()
        # Rejilla de estaciones
        for i in range(n_estaciones):
            estacion = i / (n_estaciones - 1)
            x = estacion * eslora * escala
            self._crear_linea(msp, (x, -manga * escala * 0.6), (x, manga * escala * 0.6), layer="C-CUAD")
            # etiqueta
            try:
                msp.add_text(f"{i}", dxfattribs={"height": 0.25, "layer": "C-TEXT"}).set_pos((x, manga * escala * 0.65))
            except Exception:
                pass
        # Línea base de referencia
        self._crear_linea(msp, (0, 0), (eslora * escala, 0), layer="C-REF")
        doc.saveas(dxf_path)
        return str(dxf_path)

    # -------- utilidades DXF --------
    @staticmethod
    def _crear_linea(msp, p0, p1, layer: str = "0", width: float | None = None):
        e = msp.add_line(p0, p1)
        e.dxf.layer = layer
        if width is not None:
            try:
                e.dxf.lineweight = int(width * 100)  # aproximado
            except Exception:
                pass


if __name__ == "__main__":
    gen = GeneradorPlanosNavales()
    gen.conectar_autocad()  # en macOS mostrará fallback
    dxfp = gen.crear_plano_construccion(eslora=30.0, manga=7.0, escala=1.5)
    print(dxfp)
