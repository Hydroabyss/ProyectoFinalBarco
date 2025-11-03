from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from maxsurf_integration.autocad_integration.planos_navales import GeneradorPlanosNavales


class GeneradorPlanosAuto:
    def __init__(self):
        self.generador = GeneradorPlanosNavales()

    def generar_planos_completos(self, parametros_barco: Dict[str, Any], out_dir: str | Path = "./salidas/autocad") -> Dict[str, str]:
        self.generador.conectar_autocad()
        rutas: Dict[str, str] = {}
        rutas["plano_construccion"] = self.generador.crear_plano_construccion(
            eslora=float(parametros_barco.get("eslora_total", 20.0)),
            manga=float(parametros_barco.get("manga_maxima", 5.0)),
            escala=1.25,
            out_dir=out_dir,
        )
        rutas["plano_lineas"] = self.generador.crear_plano_lineas(
            eslora=float(parametros_barco.get("eslora_total", 20.0)),
            manga=float(parametros_barco.get("manga_maxima", 5.0)),
            calado=float(parametros_barco.get("calado", parametros_barco.get("calado_diseño", 2.0))),
            escala=1.0,
            out_dir=out_dir,
        )
        rutas["plano_cuadernas"] = self.generador.crear_plano_cuadernas(
            eslora=float(parametros_barco.get("eslora_total", 20.0)),
            manga=float(parametros_barco.get("manga_maxima", 5.0)),
            escala=1.0,
            n_estaciones=11,
            out_dir=out_dir,
        )
        # Extensible: agregar plano de estructura, etc.
        return rutas


if __name__ == "__main__":
    demo = GeneradorPlanosAuto()
    out = demo.generar_planos_completos({"eslora_total": 12.0, "manga_maxima": 3.8})
    print(out)
