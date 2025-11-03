from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from maxsurf_integration.maxsurf_connector import MaxsurfConnector
from maxsurf_integration.autocad_integration.generador_planos_auto import GeneradorPlanosAuto


@dataclass
class ParametrosBuqueBase:
    loa_m: float = 103.81
    ratio_loa_lpp: float = 0.97
    beam_m: float = 15.60
    depth_m: float = 7.70
    draft_m: float = 6.20
    template: str = "Cargo Vessel"
    descripcion: str = (
        "Modelo base derivado del ejemplo 'Cargo Vessel' de Maxsurf con ajustes "
        "paramétricos para buque quimiquero de referencia."
    )

    def to_dict(self) -> Dict[str, float]:
        data = asdict(self)
        data["lpp_m"] = round(self.loa_m * self.ratio_loa_lpp, 3)
        return data


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def generar_buque_base(
    parametros: Optional[ParametrosBuqueBase] = None,
    out_dir: str | Path = "./salidas/base_ship",
    autocad_out: str | Path | None = "./salidas/autocad_base",
    export_csv: bool = True,
    export_msd: str | Path | None = None,
) -> Dict[str, Any]:
    """Deriva y exporta la información del buque base utilizando Maxsurf.

    Args:
        parametros: Parámetros objetivo para el casco base.
        out_dir: Directorio donde se guardarán los datos (JSON/CSV).
        autocad_out: Directorio para los DXF generados (None para omitir).
        export_csv: Si True, genera además un CSV resumen.

    Returns:
        Diccionario con rutas de salida y metadatos relevantes.
    """
    params = parametros or ParametrosBuqueBase()
    data_dir = _ensure_dir(Path(out_dir))

    msd_path: Optional[Path] = None
    with MaxsurfConnector(visible=False) as con:
        if not con.is_connected():
            raise RuntimeError("No fue posible conectar con Maxsurf (ni siquiera en modo mock)")
        con.new_model(template=params.template)
        con.set_length(params.loa_m)
        con.set_beam(params.beam_m)
        con.set_draft(params.draft_m)
        hydro = con.run_hydrostatics()
        backend = "mock" if con.is_mock_backend() else "com"

        if export_msd:
            msd_path = Path(export_msd)
            _ensure_dir(msd_path.parent)
            if backend == "mock":
                placeholder = msd_path.with_suffix(msd_path.suffix + ".mock.txt")
                placeholder.write_text(
                    "Este archivo se genera en modo mock. Ejecuta en Windows con Maxsurf real para obtener el .msd.",
                    encoding="utf-8",
                )
            else:
                con.save_model(str(msd_path))

    notas = [
        "Profundidad (depth) introducida para referencia; Maxsurf mock solo utiliza calado.",
    ]
    if backend == "mock":
        notas.append("En Windows con Maxsurf real se obtendrán coeficientes y geometría completos.")
    else:
        notas.append("Datos leídos directamente de Maxsurf via COM.")

    dataset: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "backend": backend,
        "parametros": params.to_dict(),
        "hidrostaticas": hydro,
        "notas": notas,
    }

    json_path = data_dir / "datos_buque_base.json"
    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(dataset, fh, indent=2, ensure_ascii=False)

    csv_path = None
    if export_csv:
        import csv

        csv_path = data_dir / "datos_buque_base.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["clave", "valor"])
            for key, value in dataset["parametros"].items():
                writer.writerow([key, value])
            for key, value in dataset["hidrostaticas"].items():
                writer.writerow([key, value])
            writer.writerow(["backend", backend])

    planos: Optional[Dict[str, str]] = None
    if autocad_out is not None:
        planos_dir = _ensure_dir(Path(autocad_out))
        generador = GeneradorPlanosAuto()
        planos = generador.generar_planos_completos(
            {
                "eslora_total": params.loa_m,
                "manga_maxima": params.beam_m,
                "calado": params.draft_m,
            },
            out_dir=planos_dir,
        )

    return {
        "datos_json": str(json_path),
        "datos_csv": str(csv_path) if csv_path else None,
        "planos": planos,
        "metadata": dataset,
        "modelo_msd": str(msd_path) if msd_path else None,
    }


if __name__ == "__main__":
    resultado = generar_buque_base()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
