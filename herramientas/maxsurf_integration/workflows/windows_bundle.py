from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from maxsurf_integration.workflows.base_ship import (
    ParametrosBuqueBase,
    generar_buque_base,
    _ensure_dir,
)


def ejecutar_bundle_windows(
    parametros: Optional[ParametrosBuqueBase] = None,
    datos_out: str | Path = "./salidas/base_ship",
    planos_out: str | Path = "./salidas/autocad_base",
    msd_out: str | Path = "./salidas/base_ship/base_ship_windows.msd",
    archivador: str | Path = "./artefactos/windows",
    ejecutar_git_lfs: bool = True,
) -> Dict[str, Any]:
    """Ejecuta el flujo completo recomendado para Windows en un solo comando.

    Pasos:
        1. Ejecuta :func:`generar_buque_base` exportando JSON, CSV, DXF y modelo `.msd`.
        2. Verifica que el backend sea ``com`` (Maxsurf real). De lo contrario falla.
        3. Copia los artefactos relevantes a ``artefactos/windows`` para archivado.
    4. Ejecuta ``git lfs track "*.msd"`` (opcional).

    Returns:
        Diccionario con rutas de salida y resumen de operaciones realizadas.
    """

    parametros = parametros or ParametrosBuqueBase()

    resultado = generar_buque_base(
        parametros=parametros,
        out_dir=datos_out,
        autocad_out=planos_out,
        export_csv=True,
        export_msd=msd_out,
    )

    backend = resultado.get("metadata", {}).get("backend")
    if backend != "com":
        raise RuntimeError(
            "El flujo Windows requiere conexión COM real. Ejecuta en una máquina Windows con Maxsurf instalado."
        )

    artefactos_dir = _ensure_dir(Path(archivador))
    base_ship_dir = _ensure_dir(artefactos_dir / "base_ship")
    dxf_dir = _ensure_dir(artefactos_dir / "autocad")
    info: Dict[str, Any] = {
        "backend": backend,
        "artefactos": {},
    }

    # Copiar JSON/CSV
    json_src = Path(resultado["datos_json"])
    json_dst = base_ship_dir / json_src.name
    shutil.copy2(json_src, json_dst)
    info["artefactos"]["datos_json"] = str(json_dst)

    if resultado.get("datos_csv"):
        csv_src = Path(resultado["datos_csv"])
        csv_dst = base_ship_dir / csv_src.name
        shutil.copy2(csv_src, csv_dst)
        info["artefactos"]["datos_csv"] = str(csv_dst)

    # Copiar DXF reales
    planos = resultado.get("planos") or {}
    dxf_archivados = {}
    for nombre, ruta in planos.items():
        src = Path(ruta)
        dst = dxf_dir / src.name
        shutil.copy2(src, dst)
        dxf_archivados[nombre] = str(dst)
    info["artefactos"]["planos"] = dxf_archivados

    # Copiar modelo MSD
    if resultado.get("modelo_msd"):
        msd_src = Path(resultado["modelo_msd"])
        msd_dst = base_ship_dir / msd_src.name
        if msd_src.exists():
            shutil.copy2(msd_src, msd_dst)
            info["artefactos"]["modelo_msd"] = str(msd_dst)

    # Registrar en git-lfs
    if ejecutar_git_lfs:
        try:
            subprocess.run(["git", "lfs", "track", "*.msd"], check=False, capture_output=True)
            info["git_lfs"] = "git lfs track *.msd ejecutado"
        except FileNotFoundError:
            info["git_lfs"] = "git no disponible; omitiendo tracking"

    manifest = artefactos_dir / "bundle_summary.json"
    manifest.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    info["artefactos"]["manifest"] = str(manifest)

    return info