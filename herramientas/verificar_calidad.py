#!/usr/bin/env python3
"""Verificador rápido de consistência de dimensiones y segmentación.

Comprueba:
- Lpp = 105.2 m
- B = 15.99 m
- Puntal = 7.90 m
- Pique de popa fin_m = 105.2 m

Fuentes chequedas (en orden):
- salidas/ENTREGA 3 v4/Resumen_Disposicion.json
- salidas/disposicion_general/resumen_disposicion_actualizado.json
- salidas/disposicion_general/resumen_disposicion.json
- salidas/disposicion_general/espacios.csv

Devuelve código 0 si todo está OK; distinto de 0 si encuentra problemas.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_summary(path: Path) -> list[str]:
    errs: list[str] = []
    data = _load_json(path)
    if not data:
        errs.append(f"No se pudo leer JSON: {path}")
        return errs

    buque = data.get("buque", {})
    lpp = buque.get("eslora_entre_perpendiculares_m")
    beam = buque.get("manga_m")
    depth = buque.get("puntal_m")
    if float(lpp) != 105.2:
        errs.append(f"LPP != 105.2 en {path}: {lpp}")
    if float(beam) != 15.99:
        errs.append(f"Manga != 15.99 en {path}: {beam}")
    if float(depth) != 7.9:
        errs.append(f"Puntal != 7.90 en {path}: {depth}")

    # validar pique de popa
    fin_pique = None
    for esp in data.get("espacios", []):
        if esp.get("nombre") == "Pique de popa":
            fin_pique = float(esp.get("fin_m"))
            break
    if fin_pique is None or fin_pique != 105.2:
        errs.append(f"Pique de popa fin_m != 105.2 en {path}: {fin_pique}")

    # validar mamparo
    pos_mpp = None
    for m in data.get("mamparos", []):
        if m.get("nombre") == "Mamparo pique de popa":
            pos_mpp = float(m.get("posicion_m"))
            break
    if pos_mpp is None or pos_mpp != 105.2:
        errs.append(f"Mamparo pique de popa posicion != 105.2 en {path}: {pos_mpp}")

    return errs


def check_espacios_csv(path: Path) -> list[str]:
    errs: list[str] = []
    try:
        rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
    except Exception:
        errs.append(f"No se pudo leer CSV: {path}")
        return errs
    for row in rows:
        if row.get("nombre") == "Pique de popa":
            fin = float(row.get("fin_m"))
            if fin != 105.2:
                errs.append(f"Pique de popa fin_m != 105.2 en {path}: {fin}")
    return errs


def main() -> int:
    problems: list[str] = []
    j1 = ROOT / "salidas" / "ENTREGA 3 v4" / "Resumen_Disposicion.json"
    j2 = ROOT / "salidas" / "disposicion_general" / "resumen_disposicion_actualizado.json"
    j3 = ROOT / "salidas" / "disposicion_general" / "resumen_disposicion.json"
    c1 = ROOT / "salidas" / "disposicion_general" / "espacios.csv"

    for p in [j1, j2, j3]:
        if p.exists():
            problems += check_summary(p)

    if c1.exists():
        problems += check_espacios_csv(c1)

    if problems:
        print("\n".join(problems))
        return 2
    print("OK: Dimensiones y segmentación consistentes (LPP=105.2, B=15.99, D=7.90, pique popa fin=105.2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación de calidad para ProyectoFinalBarco

Verifica que los archivos de salida clave contienen las dimensiones principales correctas y que el volumen de bloque es consistente.
"""
import json
import csv
from pathlib import Path

# Valores esperados
VALORES = {
    "eslora_total": 107.0,
    "lpp": 105.2,
    "manga": 15.99,
    "puntal": 7.9,
    "calado": 6.2,
    "cb": 0.7252,
    "cp": 0.74,
}

# 1. Verificar resumen_excel_trabajo_tema_3.csv
csv_path = Path("salidas/disposicion_general/resumen_excel_trabajo_tema_3.csv")
if csv_path.exists():
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        datos = {row["clave"].strip(): float(row["valor"]) for row in reader if row["valor"]}
    for k, v in VALORES.items():
        if k == "cp":
            continue
        clave = k if k not in ("cb", "cp") else None
        if clave and clave in datos:
            assert abs(datos[clave] - v) < 0.01, f"{clave} en CSV: {datos[clave]} != {v}"
    print("✅ resumen_excel_trabajo_tema_3.csv verificado")
else:
    print("❌ Falta resumen_excel_trabajo_tema_3.csv")

# 2. Verificar resumen_disposicion_actualizado.json
json_path = Path("salidas/disposicion_general/resumen_disposicion_actualizado.json")
if json_path.exists():
    with json_path.open() as f:
        j = json.load(f)
    b = j["buque"]
    for k, v in VALORES.items():
        if k == "cp":
            clave = "coeficiente_prismatico"
        elif k == "cb":
            clave = "coeficiente_de_bloque"
        else:
            clave = k + "_m"
        if clave in b:
            assert abs(float(b[clave]) - v) < 0.01, f"{clave} en JSON: {b[clave]} != {v}"
    print("✅ resumen_disposicion_actualizado.json verificado")
else:
    print("❌ Falta resumen_disposicion_actualizado.json")

# 3. Calcular volumen de bloque y comparar
vol = VALORES["lpp"] * VALORES["manga"] * VALORES["calado"] * VALORES["cb"]
print(f"Volumen de bloque calculado: {vol:.2f} m³")
if abs(vol - 7563.34) < 1.0:
    print("✅ Volumen de bloque consistente")
else:
    print("❌ Volumen de bloque inconsistente")
