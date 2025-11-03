from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from maxsurf_integration.workflows.base_ship import (
    ParametrosBuqueBase,
    generar_buque_base,
    _ensure_dir,
)
from maxsurf_integration.workflows.windows_bundle import ejecutar_bundle_windows


DEFAULT_DIR_NAME = "planos e informacion base"


def generar_planos_informacion_base(
    parametros: Optional[ParametrosBuqueBase] = None,
    raiz_salida: str | Path = DEFAULT_DIR_NAME,
    ejecutar_git_lfs: bool = True,
) -> Dict[str, Any]:
    """Ejecuta el flujo completo para obtener planos y datos base.

    Intenta usar :func:`ejecutar_bundle_windows` para obtener datos reales via COM.
    Si no es posible (modo mock), recurre a :func:`generar_buque_base`.

    Args:
        parametros: Parámetros objetivo para el casco base.
        raiz_salida: Carpeta donde se centralizarán los resultados.
        ejecutar_git_lfs: Indica si se debe ejecutar ``git lfs track"*.msd"``
            cuando se disponga de backend COM.

    Returns:
        Diccionario con la información recopilada (rutas y metadatos).
    """

    params = parametros or ParametrosBuqueBase()
    raiz = _ensure_dir(Path(raiz_salida))
    datos_dir = _ensure_dir(raiz / "datos")
    planos_dir = _ensure_dir(raiz / "planos")
    modelo_dir = _ensure_dir(raiz / "modelo")
    artefactos_dir = raiz / "artefactos"

    bundle_info: Optional[Dict[str, Any]] = None
    errores: list[str] = []

    try:
        bundle_info = ejecutar_bundle_windows(
            parametros=params,
            datos_out=datos_dir,
            planos_out=planos_dir,
            msd_out=modelo_dir / "Quimiquero_103m_Base.msd",
            archivador=artefactos_dir,
            ejecutar_git_lfs=ejecutar_git_lfs,
        )
    except RuntimeError as exc:
        errores.append(str(exc))
    except Exception as exc:  # pragma: no cover - defensivo
        errores.append(f"Error inesperado en bundle Windows: {exc}")

    if bundle_info and bundle_info.get("backend") == "com":
        resumen = {
            "backend": "com",
            "fuente": "windows_bundle",
            "artefactos": bundle_info.get("artefactos", {}),
            "resumen": str((artefactos_dir / "bundle_summary.json").resolve()),
            "errores": errores,
        }
    else:
        resultado = generar_buque_base(
            parametros=params,
            out_dir=datos_dir,
            autocad_out=planos_dir,
            export_msd=modelo_dir / "Quimiquero_103m_Base.msd",
        )
        resumen = {
            "backend": resultado.get("metadata", {}).get("backend", "mock"),
            "fuente": "mock",
            "datos_json": resultado.get("datos_json"),
            "datos_csv": resultado.get("datos_csv"),
            "planos": resultado.get("planos"),
            "modelo_msd": resultado.get("modelo_msd"),
            "errores": errores,
        }

    resumen_path = raiz / "resumen_planos_informacion.json"
    resumen_path.write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    resumen["resumen"] = str(resumen_path)
    return resumen
