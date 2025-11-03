from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import json

from maxsurf_integration.dnv_verification.dnv_rules_checker import VerificadorDNV
from maxsurf_integration.reports.report_generator import ReportGenerator


@dataclass
class ModeloEntrada:
    eslora: float
    manga: float
    puntal: float
    calado: float
    desplazamiento: float
    velocidad: float


class VerificadorCompletoDNV:
    def __init__(self):
        self.rules = VerificadorDNV()

    def verificar_cumplimiento_dnv(self, modelo: Dict[str, Any], tipo_embarcacion: str) -> Dict[str, Any]:
        # Normalização dos campos esperados
        eslora = float(modelo.get("eslora_total") or modelo.get("eslora") or 0)
        manga = float(modelo.get("manga_maxima") or modelo.get("manga") or 0)
        puntal = float(modelo.get("puntal") or 0)
        calado = float(modelo.get("calado_diseño") or modelo.get("calado") or 0)
        desplazamiento = float(modelo.get("desplazamiento") or 0)
        velocidad = float(modelo.get("velocidad_maxima") or modelo.get("velocidad") or 0)

        reglas = self.rules.cargar_normativa_dnv(tipo_embarcacion)
        lb = self.rules.verificar_eslora_manga(eslora, manga, tipo_embarcacion)
        esf = self.rules.calcular_esfuerzos_longitudinales_dnv(eslora, manga, puntal, velocidad)

        verificaciones = {
            "geometria": {"relacion_LB": lb, "codigo_dnv": "(indicativo)"},
            "estructural": {
                "momento_flexion": esf["momento_flexion_vertical"],
                "limite_material": self.rules.limite_material(),
                "cumple": esf["cumple_dnv"],
                "codigo_dnv": "Pt.3 Ch.1/Ch.5 (indicativo)",
            },
            "estabilidad": {
                # Placeholders: dependerá da curva GZ real
                "GM_min": None,
                "area_GZ": None,
                "cumple": None,
                "codigo_dnv": "Pt.3 Ch.3 (indicativo)",
            },
        }

        reporte = {
            "fecha_verificacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "normativa_aplicada": f"DNV GL ({tipo_embarcacion})",
            "resultados": verificaciones,
            "cumplimiento_total": all(
                v.get("cumple", True) if isinstance(v, dict) else True for v in verificaciones.values()
            ),
            "observaciones": self._generar_observaciones(verificaciones),
        }
        return reporte

    @staticmethod
    def _generar_observaciones(verifs: Dict[str, Any]) -> List[str]:
        obs: List[str] = []
        # Observação simples baseada em flags
        estr = verifs.get("estructural", {})
        if not estr.get("cumple", True):
            obs.append("Estructural: revisar momento de flexión frente al límite del material.")
        return obs

    def generar_pdf(self, reporte: Dict[str, Any], out_dir: str | Path, basename: str = "reporte_dnv") -> str:
        rg = ReportGenerator(out_dir)
        rg.add_title("Verificación DNV", subtitle=reporte.get("normativa_aplicada", ""))
        rg.add_paragraph(f"Fecha: {reporte.get('fecha_verificacion', '')}")
        # Tabla pequeña con claves principales
        res = reporte.get("resultados", {})
        rows = [["Bloque", "Detalle", "Valor"]]
        # Geometría (L/B)
        lb = res.get("geometria", {}).get("relacion_LB", {})
        rows.append(["Geometría", "L/B", f"{lb.get('relacion_LB', '-'):.3f}" if lb else "-"])
        rows.append(["Geometría", "Cumple L/B", str(lb.get("cumple", "-")) if lb else "-"])
        # Estructural
        estr = res.get("estructural", {})
        rows.append(["Estructura", "M_flexión", f"{estr.get('momento_flexion', '-')}"])
        rows.append(["Estructura", "Cumple", str(estr.get("cumple", "-"))])
        rg.add_table(rows, header=True)
        pdf = rg.build(f"{basename}.pdf")
        return pdf


def demo_yate_30m(out_dir: str | Path) -> Dict[str, Any]:
    ver = VerificadorCompletoDNV()
    params = {
        "eslora_total": 30.2,
        "manga_maxima": 7.1,
        "puntal": 3.8,
        "calado_diseño": 2.2,
        "desplazamiento": 145000,
        "velocidad_maxima": 18,
    }
    rep = ver.verificar_cumplimiento_dnv(params, "yacht")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    json_path = Path(out_dir) / "reporte_dnv_yate_30m.json"
    json_path.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    pdf = ver.generar_pdf(rep, out_dir=out_dir, basename="reporte_dnv_yate_30m")
    return {"json": str(json_path), "pdf": pdf}


if __name__ == "__main__":
    out = demo_yate_30m("./salidas/dnv")
    print(json.dumps(out, ensure_ascii=False))
