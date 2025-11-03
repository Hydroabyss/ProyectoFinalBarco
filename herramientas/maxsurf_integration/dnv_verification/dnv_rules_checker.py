from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import json
import sys

# Import condicional de COM (Windows) e requests apenas se necessário
try:
    import win32com.client  # type: ignore
except Exception:  # pragma: no cover
    win32com = None  # type: ignore

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None  # type: ignore


@dataclass
class DNVRuleSet:
    name: str
    application: list[str]
    min_length: Optional[float] = None
    max_length: Optional[float] = None
    mandatory_checks: Optional[list[str]] = None


class VerificadorDNV:
    """Verificador DNV simplificado.

    - Carga un set de reglas (mock) desde JSON local o dict embebido
    - Ofrece checks básicos: relación L/B, esfuerzos longitudinales (simplificados)
    - Preparado para extender hacia APIs reales (DNV Rules API, Nauticus)
    """

    def __init__(self, rules_db: Optional[Dict[str, Any]] = None):
        self.maxsurf = None
        self.rules_db = rules_db or {}

    # --------- Carga de normativa ---------
    @staticmethod
    def _default_rules() -> Dict[str, Any]:
        return {
            "dnv_gl_pty": {
                "nombre": "Rules for Classification of Yachts",
                "aplicacion": ["yates", "superyates", "megayates"],
                "eslora_minima": 24,
                "eslora_maxima": 160,
                "verificaciones_obligatorias": [
                    "estabilidad_damage",
                    "estructura_casco",
                    "compartimentacion",
                    "materiales_composite",
                ],
            },
            "dnv_gl_ptc": {
                "nombre": "Rules for Commercial Ships",
                "aplicacion": ["cargueros", "tanqueros", "pesqueros"],
                "eslora_minima": 15,
                "eslora_maxima": 400,
                "verificaciones_obligatorias": [
                    "estabilidad_intacta",
                    "estructura_longitudinal",
                    "fondos_dobles",
                    "prevencion_contaminacion",
                ],
            },
            "dnv_gl_ptd": {
                "nombre": "Rules for High Speed Craft",
                "aplicacion": ["catamaranes", "foils", "planificantes"],
                "velocidad_minima": 15,
                "verificaciones_obligatorias": [
                    "estabilidad_dinamica",
                    "aceleraciones",
                    "fatiga_materiales",
                    "impacto_olas",
                ],
            },
        }

    def cargar_normativa_dnv(self, tipo_embarcacion: str = "yacht") -> Dict[str, Any]:
        db = self.rules_db or self._default_rules()
        mapping = {
            "yacht": "dnv_gl_pty",
            "commercial": "dnv_gl_ptc",
            "high_speed": "dnv_gl_ptd",
        }
        clave = mapping.get(tipo_embarcacion, "dnv_gl_pty")
        return db.get(clave, {})

    # --------- Verificaciones simplificadas ---------
    @staticmethod
    def verificar_eslora_manga(eslora: float, manga: float, tipo_norma: str = "yacht") -> Dict[str, Any]:
        relacion_lb = float(eslora) / float(manga)
        limites = {
            "yacht": {"min": 2.8, "max": 5.0, "optimo": 3.2},
            "commercial": {"min": 3.0, "max": 7.0, "optimo": 4.5},
            "high_speed": {"min": 3.5, "max": 8.0, "optimo": 5.0},
        }
        lim = limites.get(tipo_norma, limites["yacht"])
        return {
            "relacion_LB": relacion_lb,
            "min": lim["min"],
            "max": lim["max"],
            "cumple": lim["min"] <= relacion_lb <= lim["max"],
        }

    @staticmethod
    def limite_material(f_y: float = 235e6) -> float:
        """Límite de fluencia (Pa). Default: acero S235."""
        return float(f_y)

    def calcular_esfuerzos_longitudinales_dnv(
        self, eslora: float, manga: float, puntal: float, velocidad: float
    ) -> Dict[str, Any]:
        # Fórmulas simplificadas con referencias indicativas
        coeficiente_ola = 5.0 + (0.084 * eslora)  # Referencia: Pt.3 Ch.1 Sec.4 (indicativa)
        momento_flexion = (eslora ** 2) * manga * (0.042 + (0.001 * velocidad))
        resultados = {
            "momento_flexion_vertical": momento_flexion * 1.2,  # Factor seguridad
            "esfuerzo_cortante": (0.3 * momento_flexion) / max(eslora, 1e-6),
            "coeficiente_ola_dnv": coeficiente_ola,
            "cumple_dnv": momento_flexion < (self.limite_material() * 0.6),
        }
        return resultados


def main(argv: list[str] | None = None) -> int:
    # CLI mínima para prova rápida
    args = sys.argv[1:] if argv is None else argv
    if not args:
        # demo
        ver = VerificadorDNV()
        reglas = ver.cargar_normativa_dnv("yacht")
        lb = ver.verificar_eslora_manga(30.0, 7.5, "yacht")
        esf = ver.calcular_esfuerzos_longitudinales_dnv(30.0, 7.5, 3.8, 18.0)
        print(json.dumps({"reglas": reglas, "L_B": lb, "esfuerzos": esf}, ensure_ascii=False))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
