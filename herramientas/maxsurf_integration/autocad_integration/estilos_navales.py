from __future__ import annotations

from typing import Dict

try:
    import win32com.client  # type: ignore
except Exception:  # pragma: no cover
    win32com = None  # type: ignore


class ConfiguradorEstilos:
    def __init__(self, autocad=None):
        self.autocad = autocad

    def configurar_estilos_navales(self) -> Dict[str, int]:
        layers_navales = {
            "C-CASC": "Contorno casco",
            "C-CUAD": "Cuadernas",
            "C-LFLOT": "Líneas de flotación",
            "C-PERF": "Perfiles longitudinales",
            "C-COTA": "Cotaciones",
            "C-STR": "Estructura",
            "C-REF": "Refuerzos",
            "C-TEXT": "Texto y anotaciones",
            "C-SIMB": "Símbolos navales",
        }
        colores = self._colores_por_tipo()
        # Si tuviera autocad via COM, crear los layers
        if self.autocad and win32com is not None:  # pragma: no cover
            doc = self.autocad.ActiveDocument
            for layer, _ in layers_navales.items():
                try:
                    doc.Layers.Add(layer)
                    doc.Layers.Item(layer).Color = colores.get(layer, 7)
                except Exception:
                    pass
        return colores

    @staticmethod
    def _colores_por_tipo() -> Dict[str, int]:
        return {
            "C-CASC": 1,
            "C-CUAD": 2,
            "C-LFLOT": 3,
            "C-PERF": 4,
            "C-COTA": 5,
            "C-STR": 6,
            "C-REF": 7,
            "C-TEXT": 8,
            "C-SIMB": 9,
        }
