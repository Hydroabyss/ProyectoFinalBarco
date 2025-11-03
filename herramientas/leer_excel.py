#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lector resumido de Excel de disposición general.

Lee el archivo indicado, lista las hojas y extrae posibles dimensiones principales:
- Eslora total, Lpp, Manga, Puntal, Calado
- Segmentos longitudinales (Lfp, Área de carga, Ler, Lap)

Salida en consola y posibilidad de exportar CSV y Markdown.

Uso:
  python herramientas/leer_excel.py --excel "salidas/disposicion_general/Trabajo Tema 3.xlsx" \
      --salida "salidas/disposicion_general"
"""

from __future__ import annotations
import argparse
from pathlib import Path
import re
import json
from typing import Any, Dict, List, Optional

import pandas as pd  # type: ignore


ESLORA_COMPLEMENTO_AP = 1.8  # m, agregado hacia popa desde eje de pala si no hay LoA explícita


CLAVES_PRINCIPALES = {
    "eslora_total": ["eslora total", "loa", "lpp total"],
    "lpp": ["lpp", "eslora entre perpendiculares"],
    "manga": ["manga", "beam", "b"],
    "puntal": ["puntal", "depth", "altura", "t"],
    "calado": ["calado", "draft", "tr", "d"],
    "lfp": ["lfp", "pique proa", "pique de proa"],
    "lap": ["lap", "pique popa", "pique de popa"],
    "ler": ["ler", "cámara de máquinas", "camara de maquinas", "engine room"],
    "area_carga": ["área de carga", "area de carga", "zona de carga"],
}


def normalizar(texto: str) -> str:
    return re.sub(r"\s+", " ", texto.strip().lower())


def buscar_valor_en_df(df: pd.DataFrame, lista_claves: List[str]) -> Optional[float]:
    # 1. Buscar en nombres de columnas
    lower_cols = {normalizar(c): c for c in df.columns}
    for clave in lista_claves:
        c_norm = normalizar(clave)
        if c_norm in lower_cols:
            try:
                val = df.iloc[0][lower_cols[c_norm]]
                return float(str(val).replace(',', '.'))
            except Exception:
                pass
    # 2. Buscar en primera columna tipo clave-valor
    if df.shape[1] >= 2:
        for _, row in df.iterrows():
            k = normalizar(str(row.iloc[0]))
            for clave in lista_claves:
                if k == normalizar(clave):
                    try:
                        val = row.iloc[1]
                        return float(str(val).replace(',', '.'))
                    except Exception:
                        return None
    return None


def extraer_principales(hojas: Dict[str, pd.DataFrame]) -> Dict[str, Optional[float]]:
    resultado: Dict[str, Optional[float]] = {k: None for k in CLAVES_PRINCIPALES.keys()}
    for nombre, df in hojas.items():
        for clave, candidatos in CLAVES_PRINCIPALES.items():
            if resultado[clave] is None:
                val = buscar_valor_en_df(df, candidatos)
                if val is not None:
                    resultado[clave] = val
    # lpp de segmentos si faltan
    segs = [resultado.get("lfp"), resultado.get("area_carga"), resultado.get("ler"), resultado.get("lap")]
    if resultado.get("lpp") is None and all(v is not None for v in segs):
        resultado["lpp"] = sum(v for v in segs if v is not None)
    if resultado.get("eslora_total") is None and resultado.get("lpp") is not None:
        resultado["eslora_total"] = float(resultado["lpp"] or 0.0) + ESLORA_COMPLEMENTO_AP
    return resultado


def main() -> None:
    ap = argparse.ArgumentParser(description="Lectura resumida de Excel de disposición")
    ap.add_argument("--excel", required=True, help="Ruta al archivo Excel")
    ap.add_argument("--salida", default=".", help="Carpeta para exportar resumen")
    args = ap.parse_args()

    excel_path = Path(args.excel)
    if not excel_path.exists():
        raise SystemExit(f"❌ No existe el archivo: {excel_path}")

    salida_dir = Path(args.salida)
    salida_dir.mkdir(parents=True, exist_ok=True)

    xls = pd.ExcelFile(excel_path)
    hojas = {nombre: xls.parse(nombre) for nombre in xls.sheet_names}

    principales = extraer_principales(hojas)

    print("==============================================")
    print("✅ RESUMEN EXCEL - DISPOSICIÓN GENERAL")
    print(f"Archivo: {excel_path}")
    print("Hojas detectadas:")
    for h in hojas.keys():
        print(f"  • {h}")
    print("----------------------------------------------")
    print("Dimensiones / Segmentos detectados:")
    for k, v in principales.items():
        print(f"  - {k}: {v}")
    print("----------------------------------------------")
    # Exportar CSV y Markdown
    csv_path = salida_dir / "resumen_excel_trabajo_tema_3.csv"
    md_path = salida_dir / "resumen_excel_trabajo_tema_3.md"
    df_out = pd.DataFrame([
        {"clave": k, "valor": v} for k, v in principales.items()
    ])
    df_out.to_csv(csv_path, index=False)
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Resumen extracción Excel – Trabajo Tema 3\n\n")
        f.write(f"Archivo origen: `{excel_path.name}`\n\n")
        f.write("## Dimensiones y Segmentos\n\n")
        for k, v in principales.items():
            f.write(f"- **{k}**: {v}\n")
        f.write("\n## Notas\n\n")
        f.write("- Si algún valor aparece como None, agregar etiqueta en la hoja o revisar formato.\n")
        f.write("- Lpp se deduce como suma de segmentos si no se encuentra directamente.\n")
    print(f"CSV: {csv_path}")
    print(f"MD:  {md_path}")
    print("==============================================")


if __name__ == "__main__":
    main()
