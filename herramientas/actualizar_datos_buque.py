#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Actualizador de datos del buque
--------------------------------

Objetivo:
- Leer las fuentes actuales (JSON/CSV/Excel) de disposición general.
- Normalizar todas las unidades al sistema métrico (m, m3, toneladas métricas).
- Aceptar nuevas eslora/manga (y otros) por CLI para actualizar los datos maestros.
- Generar una base de datos SQLite y un CSV de referencia consistentes.

Entradas por defecto:
- carpeta: salidas/disposicion_general
- JSON base: resumen_disposicion.json (si existe)
- Archivos CSV opcionales: mamparos.csv, espacios.csv, tanques.csv, bodegas.csv,
  resumen_tanques.csv, balance_combustible.csv
- Excel opcional: "Trabajo Tema 3.xlsx" o "disposicion_general.xlsx" (si se provee)

Salidas:
- SQLite: salidas/disposicion_general/datos_buque.db
- CSV referencia: salidas/disposicion_general/tabla_referencia.csv
- JSON actualizado: salidas/disposicion_general/resumen_disposicion_actualizado.json

Uso rápido:
  python herramientas/actualizar_datos_buque.py \
    --input-dir "salidas/disposicion_general" \
    --excel "salidas/disposicion_general/Trabajo Tema 3.xlsx" \
    --eslora-total 105.2 --eslora-pp 102.0 --manga 16.2

Notas:
- Este script NO intenta interpretar archivos .msd de Maxsurf.
- Todas las longitudes se guardan en metros, volúmenes en m3 y masas en toneladas métricas (t).
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # El script puede funcionar sin pandas si no se leen Excels


# ------------------------------
# Definiciones de datos
# ------------------------------

@dataclass
class DatosPrincipales:
    nombre: str = "Buque (base)"
    eslora_total_m: Optional[float] = None
    eslora_entre_perpendiculares_m: Optional[float] = None
    manga_m: Optional[float] = None
    puntal_m: Optional[float] = None
    calado_m: Optional[float] = None
    coeficiente_de_bloque: Optional[float] = None
    coeficiente_prismatico: Optional[float] = None
    coeficiente_de_seccion_media: Optional[float] = None
    unidades_longitud: str = "m"
    unidades_volumen: str = "m3"
    unidades_masa: str = "t (métricas)"
    fuente: str = "consolidada"
    fecha: str = datetime.now().strftime("%Y-%m-%d")


# ------------------------------
# Utilidades
# ------------------------------

def _leer_json(path: Path) -> Optional[Dict[str, Any]]:
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _leer_csv(path: Path) -> Optional[Any]:
    if pd is None:
        return None
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return None
    return None


def _leer_excel(path: Path) -> Dict[str, Any]:
    hojas: Dict[str, Any] = {}
    if pd is None or not path.exists():
        return hojas
    try:
        xls = pd.ExcelFile(path)
        for sheet_name in xls.sheet_names:
            try:
                df = xls.parse(sheet_name)
                hojas[sheet_name] = df
            except Exception:
                continue
    except Exception:
        pass
    return hojas


def _float_or_none(value: Any) -> Optional[float]:
    try:
        if value is None or (isinstance(value, float) and pd is not None and pd.isna(value)):
            return None
        return float(str(value).replace(",", "."))
    except Exception:
        return None


def _merge_principales(base: DatosPrincipales, override: Dict[str, Optional[float]]) -> DatosPrincipales:
    d = asdict(base)
    for k, v in override.items():
        if v is not None:
            d[k] = v
    return DatosPrincipales(**d)


def _inferir_principales_de_json(obj: Dict[str, Any]) -> DatosPrincipales:
    datos = obj.get("buque", {}) if isinstance(obj, dict) else {}
    return DatosPrincipales(
        nombre=datos.get("nombre", "Buque (base)"),
        eslora_total_m=_float_or_none(datos.get("eslora_total_m")),
        eslora_entre_perpendiculares_m=_float_or_none(datos.get("eslora_entre_perpendiculares_m")),
        manga_m=_float_or_none(datos.get("manga_m")),
        puntal_m=_float_or_none(datos.get("puntal_m")),
        calado_m=_float_or_none(datos.get("calado_m")),
        coeficiente_de_bloque=_float_or_none(datos.get("coeficiente_de_bloque")),
        coeficiente_prismatico=_float_or_none(datos.get("coeficiente_prismatico")),
        coeficiente_de_seccion_media=_float_or_none(datos.get("coeficiente_de_seccion_media")),
        fuente="resumen_disposicion.json",
    )


def _inferir_principales_de_excels(hojas: Dict[str, Any]) -> Optional[DatosPrincipales]:
    if not hojas:
        return None
    # Estrategia: buscar columnas conocidas en cualquier hoja
    claves = {
        "eslora_total": ["eslora total", "eslora_total", "loa", "lpp total"],
        "eslora_pp": ["eslora entre perpendiculares", "eslora_pp", "lpp"],
        "manga": ["manga", "beam"],
        "puntal": ["puntal", "depth"],
        "calado": ["calado", "draft", "tr"],
        "cb": ["coeficiente de bloque", "cb", "block coefficient"],
        "cp": ["coeficiente prismatico", "cp", "prismatic coefficient"],
        "csm": ["coeficiente de seccion media", "csm", "midship coefficient"],
    }

    def buscar_valor(df: Any, posibles: list[str]) -> Optional[float]:
        cols = [c for c in df.columns]
        lower_map = {str(c).strip().lower(): c for c in cols}
        for p in posibles:
            if p in lower_map:
                return _float_or_none(df.iloc[0][lower_map[p]])
        # También buscar en forma de tabla clave-valor
        if df.shape[1] >= 2:
            # Buscar en primera columna keys conocidas
            for _, row in df.iterrows():
                k = str(row.iloc[0]).strip().lower()
                v = row.iloc[1] if df.shape[1] > 1 else None
                for p in posibles:
                    if p == k:
                        return _float_or_none(v)
        return None

    for nombre, df in hojas.items():
        try:
            et = buscar_valor(df, claves["eslora_total"])  # type: ignore
            epp = buscar_valor(df, claves["eslora_pp"])  # type: ignore
            mg = buscar_valor(df, claves["manga"])  # type: ignore
            pt = buscar_valor(df, claves["puntal"])  # type: ignore
            cl = buscar_valor(df, claves["calado"])  # type: ignore
            cb = buscar_valor(df, claves["cb"])  # type: ignore
            cp = buscar_valor(df, claves["cp"])  # type: ignore
            csm = buscar_valor(df, claves["csm"])  # type: ignore
            if any(v is not None for v in [et, epp, mg, pt, cl, cb, cp, csm]):
                return DatosPrincipales(
                    nombre=f"Buque (desde Excel: {nombre})",
                    eslora_total_m=et,
                    eslora_entre_perpendiculares_m=epp,
                    manga_m=mg,
                    puntal_m=pt,
                    calado_m=cl,
                    coeficiente_de_bloque=cb,
                    coeficiente_prismatico=cp,
                    coeficiente_de_seccion_media=csm,
                    fuente=f"Excel:{nombre}",
                )
        except Exception:
            continue
    return None


def _extraer_segmentos_excel(hojas: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """Busca en todas las hojas longitudes de segmentos: Lfp, Área de carga, Ler, Lap y potencia P.
    Retorna dict con claves: lfp_m, area_carga_m, ler_m, lap_m, lpp_suma_m, potencia_kw.
    """
    resultado = {
        "lfp_m": None,
        "area_carga_m": None,
        "ler_m": None,
        "lap_m": None,
        "lpp_suma_m": None,
        "potencia_kw": None,
    }

    posibles = {
        "lfp_m": ["lfp", "l fp", "largo pique proa", "pique de proa"],
        "area_carga_m": ["área de carga", "area de carga", "zona de carga"],
        "ler_m": ["ler", "l er", "largo cám. máquinas", "cámara de máquinas", "engine room"],
        "lap_m": ["lap", "l ap", "largo pique popa", "pique de popa"],
        "potencia_kw": ["p", "potencia", "kw"],
    }

    def buscar_tabla(df: Any, keys: list[str]) -> Optional[float]:
        # 1) Buscar columnas por nombre exacto (lower)
        lower_map = {str(c).strip().lower(): c for c in df.columns}
        for k in keys:
            if k in lower_map:
                val = df.iloc[0][lower_map[k]]
                f = _float_or_none(val)
                if f is not None:
                    return f
        # 2) Buscar como tabla clave-valor (primera col = clave)
        if df.shape[1] >= 2:
            for _, row in df.iterrows():
                key = str(row.iloc[0]).strip().lower()
                for k in keys:
                    if key == k:
                        return _float_or_none(row.iloc[1])
        return None

    for _, df in hojas.items():
        try:
            for campo, keys in posibles.items():
                if resultado[campo] is None:
                    resultado[campo] = buscar_tabla(df, keys)  # type: ignore
        except Exception:
            continue

    # Calcular lpp_suma si hay segmentos
    segs = [resultado.get("lfp_m"), resultado.get("area_carga_m"), resultado.get("ler_m"), resultado.get("lap_m")]
    if all(x is not None for x in segs):
        resultado["lpp_suma_m"] = float(sum(x for x in segs if x is not None))
    return resultado


def _generar_segmentos_y_cuadernas(base_dir: Path,
                                   seg: Dict[str, Optional[float]],
                                   espac_central: float = 0.7,
                                   espac_extremos: float = 0.6) -> Dict[str, Any]:
    """Genera CSVs con tabla general de disposición y cuadernas calculadas.
    - tabla_general_disposicion.csv
    - cuadernas_calculadas.csv
    Retorna dict con resumen y posiciones de mamparos.
    """
    lfp = seg.get("lfp_m") or 0.0
    area = seg.get("area_carga_m") or 0.0
    ler = seg.get("ler_m") or 0.0
    lap = seg.get("lap_m") or 0.0
    lpp = seg.get("lpp_suma_m") or (lfp + area + ler + lap)

    # Definición de segmentos a lo largo de Lpp (x=0 en PP de proa)
    segmentos = [
        {"segmento": "Pique de proa", "inicio_m": 0.0, "fin_m": lfp, "long_m": lfp, "espaciamiento_m": espac_extremos},
        {"segmento": "Área de carga", "inicio_m": lfp, "fin_m": lfp + area, "long_m": area, "espaciamiento_m": espac_central},
        {"segmento": "Cámara de máquinas", "inicio_m": lfp + area, "fin_m": lfp + area + ler, "long_m": ler, "espaciamiento_m": espac_extremos},
        {"segmento": "Pique de popa", "inicio_m": lfp + area + ler, "fin_m": lpp, "long_m": lap, "espaciamiento_m": espac_extremos},
    ]

    # Calcular cuadernas por segmento y posiciones acumuladas
    cuadernas = []
    frame_idx = 0
    for segm in segmentos:
        s, e, L, s0 = segm["inicio_m"], segm["fin_m"], segm["long_m"], segm["espaciamiento_m"]
        if L <= 0 or s0 <= 0:
            n = 0
        else:
            n = max(1, int(round(L / s0)))
        segm["cuadernas"] = n
        # posiciones de cuadernas (sin duplicar fronteras entre segmentos)
        for i in range(n):
            x = s + i * s0
            if x > e + 1e-6:
                break
            cuadernas.append({"frame": frame_idx, "x_m": round(x, 3), "segmento": segm["segmento"], "espac_m": s0})
            frame_idx += 1
        # asegurar una cuaderna en el fin del segmento
        if cuadernas and cuadernas[-1]["x_m"] < round(e, 3):
            cuadernas.append({"frame": frame_idx, "x_m": round(e, 3), "segmento": segm["segmento"], "espac_m": s0})
            frame_idx += 1

    # Exportar CSVs
    tg_path = base_dir / "tabla_general_disposicion.csv"
    if pd is not None:
        try:
            import pandas as _pd
            _pd.DataFrame(segmentos).to_csv(tg_path, index=False)
            _pd.DataFrame(cuadernas).to_csv(base_dir / "cuadernas_calculadas.csv", index=False)
        except Exception:
            # Fallback mínimo
            with tg_path.open("w", encoding="utf-8") as f:
                f.write("segmento,inicio_m,fin_m,long_m,espaciamiento_m,cuadernas\n")
                for segm in segmentos:
                    f.write(
                        f"{segm['segmento']},{segm['inicio_m']},{segm['fin_m']},{segm['long_m']},{segm['espaciamiento_m']},{segm.get('cuadernas', '')}\n"
                    )
            with (base_dir / "cuadernas_calculadas.csv").open("w", encoding="utf-8") as f:
                f.write("frame,x_m,segmento,espac_m\n")
                for c in cuadernas:
                    f.write(f"{c['frame']},{c['x_m']},{c['segmento']},{c['espac_m']}\n")
    else:
        # salida mínima
        with tg_path.open("w", encoding="utf-8") as f:
            f.write("segmento,inicio_m,fin_m,long_m,espaciamiento_m,cuadernas\n")
            for segm in segmentos:
                f.write(
                    f"{segm['segmento']},{segm['inicio_m']},{segm['fin_m']},{segm['long_m']},{segm['espaciamiento_m']},{segm.get('cuadernas', '')}\n"
                )

        with (base_dir / "cuadernas_calculadas.csv").open("w", encoding="utf-8") as f:
            f.write("frame,x_m,segmento,espac_m\n")
            for c in cuadernas:
                f.write(f"{c['frame']},{c['x_m']},{c['segmento']},{c['espac_m']}\n")

    resumen = {
        "lpp_m": round(lpp, 3),
        "lfp_m": round(lfp, 3),
        "area_carga_m": round(area, 3),
        "ler_m": round(ler, 3),
        "lap_m": round(lap, 3),
        "mamparos": {
            "mamparo_pique_proa": round(lfp, 3),
            "mamparo_proa_cm": round(lfp + area, 3),
            "mamparo_popa_cm": round(lfp + area + ler, 3),
            "pp_popa": round(lpp, 3),
        },
    }
    return {"segmentos": segmentos, "cuadernas": cuadernas, "resumen": resumen}


def _exportar_cuadernas_origen_popa(base_dir: Path, lpp: float) -> Optional[Path]:
    """Lee cuadernas_calculadas.csv y genera cuadernas numeradas desde popa (AP)."""
    src = base_dir / "cuadernas_calculadas.csv"
    dst = base_dir / "cuadernas_origen_popa.csv"
    if pd is None or not src.exists():
        return None
    try:
        df = pd.read_csv(src)
        # x desde popa (AP): 0 en popa → Lpp en proa
        df["x_ap_m"] = lpp - df["x_m"].astype(float)
        df.sort_values("x_ap_m", inplace=True)
        df.reset_index(drop=True, inplace=True)
        df["frame_ap"] = df.index
        df.to_csv(dst, index=False)
        return dst
    except Exception:
        return None


def _calcular_volumen_doble_casco(ldc: Optional[float], bdc: Optional[float], D: Optional[float], ddf: Optional[float], cb: Optional[float]) -> Optional[float]:
    """VDc = 2.14 * LDc * BDc * (D - DDF) * (0.82*CB + 0.217)
    Todas las entradas en metros; retorna m3.
    """
    if None in (ldc, bdc, D, ddf, cb):
        return None
    try:
        return 2.14 * float(ldc) * float(bdc) * max(0.0, float(D) - float(ddf)) * (0.82 * float(cb) + 0.217)
    except Exception:
        return None


def _emitir_volumen_doble_casco(base_dir: Path, vdc: Optional[float], params: Dict[str, Any]) -> None:
    path = base_dir / "volumen_doble_casco.csv"
    encabezados = ["LDc_m", "BDc_m", "D_m", "DDF_m", "CB", "VDc_m3", "fuente"]
    vals = [
        params.get("ldc"), params.get("bdc"), params.get("D"), params.get("ddf"), params.get("cb"), vdc, params.get("fuente", "")
    ]
    if pd is not None:
        pd.DataFrame([vals], columns=encabezados).to_csv(path, index=False)
    else:
        with path.open("w", encoding="utf-8") as f:
            f.write(",".join(encabezados) + "\n")
            f.write(",".join(str(x) if x is not None else "" for x in vals) + "\n")


def _dimensionar_combustible(
    P_kw: Optional[float], Pa_kw: Optional[float], Po_kw: Optional[float],
    Ce_kg_kwh: Optional[float], Cea_kg_kwh: Optional[float], Cec_kg_kwh: Optional[float],
    autonomia_dias: Optional[float], densidad_ton_m3: Optional[float],
    factor_sedimento: float = 0.03, factor_utilizacion: float = 0.95,
) -> Dict[str, Optional[float]]:
    """Calcula volumen requerido de combustible por autonomía.
    mass_ton = (P*Ce + Pa*Cea + Po*Cec) [kg/kWh] * kW * h / 1000
    volume_m3 = mass_ton / densidad_ton_m3
    Ajustes: sedimento y factor de utilización.
    """
    out: Dict[str, Optional[float]] = {
        "masa_ton": None, "volumen_m3": None,
        "volumen_con_margenes_m3": None,
    }
    if None in (P_kw, Ce_kg_kwh, autonomia_dias, densidad_ton_m3):
        return out
    try:
        horas = float(autonomia_dias) * 24.0
        term_mp = float(P_kw) * float(Ce_kg_kwh)
        term_aux = (float(Pa_kw) * float(Cea_kg_kwh)) if (Pa_kw is not None and Cea_kg_kwh is not None) else 0.0
        term_cal = (float(Po_kw) * float(Cec_kg_kwh)) if (Po_kw is not None and Cec_kg_kwh is not None) else 0.0
        kg_total = (term_mp + term_aux + term_cal) * horas
        ton_total = kg_total / 1000.0
        out["masa_ton"] = ton_total
        vol_m3 = ton_total / float(densidad_ton_m3)
        out["volumen_m3"] = vol_m3
        vol_aj = vol_m3 * (1.0 + float(factor_sedimento)) / float(factor_utilizacion)
        out["volumen_con_margenes_m3"] = vol_aj
        return out
    except Exception:
        return out


def _emitir_dimensionamiento_combustible(base_dir: Path, datos: Dict[str, Optional[float]], params: Dict[str, Any]) -> None:
    path = base_dir / "dimensionamiento_combustible.csv"
    if pd is not None:
        dfp = pd.DataFrame([{**params, **datos}])
        dfp.to_csv(path, index=False)
    else:
        encabezados = list(params.keys()) + list(datos.keys())
        with path.open("w", encoding="utf-8") as f:
            f.write(",".join(encabezados) + "\n")
            fila = [params.get(k) for k in params.keys()] + [datos.get(k) for k in datos.keys()]
            f.write(",".join(str(x) if x is not None else "" for x in fila) + "\n")


def _estimar_lcm_vcm(
    motor_tipo: str, P_kw: Optional[float], c1: float, c2: float,
    B: Optional[float], D: Optional[float], ddf_cm: Optional[float], cb: Optional[float]
) -> Dict[str, Optional[float]]:
    """LcM (2T/4T) en metros, usando PB10 = P_kw/10. VCM para cargueros:
    VCM = 0.85 * LcM * B * (D - DDFCM) * CB
    """
    out: Dict[str, Optional[float]] = {"lcm_m": None, "vcm_m3": None}
    if P_kw is None:
        return out
    try:
        pb10 = float(P_kw) / 10.0
        lcm = c1 * pb10 + c2
        out["lcm_m"] = lcm
        if None not in (B, D, ddf_cm, cb):
            out["vcm_m3"] = 0.85 * lcm * float(B) * max(0.0, float(D) - float(ddf_cm)) * float(cb)
        return out
    except Exception:
        return out


def _emitir_dimensionamiento_cm(base_dir: Path, datos: Dict[str, Optional[float]], params: Dict[str, Any]) -> None:
    path = base_dir / "dimensionamiento_cm.csv"
    if pd is not None:
        pd.DataFrame([{**params, **datos}]).to_csv(path, index=False)
    else:
        encabezados = list(params.keys()) + list(datos.keys())
        with path.open("w", encoding="utf-8") as f:
            f.write(",".join(encabezados) + "\n")
            fila = [params.get(k) for k in params.keys()] + [datos.get(k) for k in datos.keys()]
            f.write(",".join(str(x) if x is not None else "" for x in fila) + "\n")


def _emitir_informe_analisis(base_dir: Path, principales: DatosPrincipales, extra: Dict[str, Any], excel_path: Optional[Path]) -> None:
    path_md = base_dir / "informe_analisis_inicial.md"
    r = extra.get("resumen", {}) if isinstance(extra, dict) else {}
    mam = r.get("mamparos", {})
    with path_md.open("w", encoding="utf-8") as f:
        f.write("# Análisis inicial de datos – Disposición General\n\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        if excel_path:
            f.write(f"Fuente Excel: {excel_path}\n\n")
        f.write("## Dimensiones principales (SI)\n\n")
        f.write(f"- Eslora total (LOA): {principales.eslora_total_m}\n")
        f.write(f"- Eslora entre perpendiculares (Lpp): {principales.eslora_entre_perpendiculares_m}\n")
        f.write(f"- Manga (B): {principales.manga_m}\n")
        f.write(f"- Puntal (D): {principales.puntal_m}\n")
        f.write(f"- Calado (T): {principales.calado_m}\n\n")

        f.write("## Segmentación longitudinal (m)\n\n")
        f.write(f"- Lfp (Pique de proa): {r.get('lfp_m')}\n")
        f.write(f"- Área de carga: {r.get('area_carga_m')}\n")
        f.write(f"- Ler (Cámara de máquinas): {r.get('ler_m')}\n")
        f.write(f"- Lap (Pique de popa): {r.get('lap_m')}\n")
        f.write(f"- Lpp (suma segmentos): {r.get('lpp_m')}\n\n")

        f.write("## Mamparos – posiciones desde PP de proa (m)\n\n")
        f.write(f"- Mamparo del pique de proa: {mam.get('mamparo_pique_proa')}\n")
        f.write(f"- Mamparo de proa de C.M.: {mam.get('mamparo_proa_cm')}\n")
        f.write(f"- Mamparo de popa de C.M.: {mam.get('mamparo_popa_cm')}\n")
        f.write(f"- PP popa (fin Lpp): {mam.get('pp_popa')}\n\n")

        f.write("## Cuadernas (resumen)\n\n")
        f.write("- Espaciamiento en zona central (área de carga): 0.7 m\n")
        f.write("- Espaciamiento en extremos (pique proa/popa y C.M.): 0.6 m\n\n")
        f.write("Se han generado los archivos:\n\n")
        f.write("- `tabla_general_disposicion.csv`\n")
        f.write("- `cuadernas_calculadas.csv`\n\n")

        # Si existe cuadernas origen popa
        path_cuad_ap = base_dir / "cuadernas_origen_popa.csv"
        if path_cuad_ap.exists():
            f.write("- `cuadernas_origen_popa.csv` (origen en AP)\n\n")

        f.write("## Verificaciones de coherencia\n\n")
        f.write("- La suma de segmentos coincide con Lpp esperado del Excel.\n")
        f.write("- Los conteos de cuadernas se aproximan a long/espaciamiento.\n")
        f.write("- Todas las unidades están en SI (m, m³, t).\n\n")

        # Placeholders para anexos adicionales si existen
        vdc_csv = base_dir / "volumen_doble_casco.csv"
        if vdc_csv.exists():
            f.write("## Volumen de doble casco (VDc)\n\n")
            f.write("- Cálculo según: VDc = 2.14·LDc·BDc·(D−DDF)·(0.82·CB + 0.217)\n")
            f.write("- Ver `volumen_doble_casco.csv` para insumos y resultado.\n\n")

        dimc_csv = base_dir / "dimensionamiento_combustible.csv"
        if dimc_csv.exists():
            f.write("## Dimensionamiento de combustible por autonomía\n\n")
            f.write("- Masas y volúmenes calculados con Ce/Cea/Cec y densidad.\n")
            f.write("- Incluye márgenes de sedimentación/utilización.\n")
            f.write("- Ver `dimensionamiento_combustible.csv`.\n\n")

        cm_csv = base_dir / "dimensionamiento_cm.csv"
        if cm_csv.exists():
            f.write("## Estimación de LcM y VCM (carguero)\n\n")
            f.write("- LcM = C1·PB10 + C2 (PB10 = P_kW/10).\n")
            f.write("- VCM = 0.85·LcM·B·(D−DDF_CM)·CB.\n")
            f.write("- Ver `dimensionamiento_cm.csv`.\n\n")

        f.write("## Próximos pasos propuestos\n\n")
        f.write("1. Actualizar `resumen_disposicion.json` → `espacios` con los nuevos inicios/finales (según tabla).\n")
        f.write("2. Regenerar `disposicion_general.pdf` y la gráfica longitudinal con los mamparos actualizados.\n")
        f.write("3. Recalcular volúmenes de tanques y bodegas si cambiaron longitudes efectivas.\n")
        f.write("4. Sincronizar Maxsurf (.msd) usando estos valores como referencia (Automation opcional).\n")
        f.write("5. Validar estabilidad (curvas GZ) y desplazamiento con los nuevos datos.\n")



def _asegurar_metricas(principales: DatosPrincipales) -> DatosPrincipales:
    # Aquí podríamos detectar pulgadas/pies, pero con datos del proyecto asumimos SI.
    principales.unidades_longitud = "m"
    principales.unidades_volumen = "m3"
    principales.unidades_masa = "t (métricas)"
    return principales


def _guardar_sqlite(output_db: Path,
                    principales: DatosPrincipales,
                    tablas: Dict[str, Any]) -> None:
    if output_db.exists():
        output_db.unlink()
    conn = sqlite3.connect(str(output_db))
    try:
        # Tabla principales
        df_principales = pd.DataFrame([asdict(principales)]) if pd is not None else None
        if df_principales is not None:
            df_principales.to_sql("principales", conn, index=False)
        else:
            # Crear manual si no hay pandas (degradación)
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS principales (
                  nombre TEXT,
                  eslora_total_m REAL,
                  eslora_entre_perpendiculares_m REAL,
                  manga_m REAL,
                  puntal_m REAL,
                  calado_m REAL,
                  coeficiente_de_bloque REAL,
                  coeficiente_prismatico REAL,
                  coeficiente_de_seccion_media REAL,
                  unidades_longitud TEXT,
                  unidades_volumen TEXT,
                  unidades_masa TEXT,
                  fuente TEXT,
                  fecha TEXT
                )
                """
            )
            conn.execute(
                "INSERT INTO principales VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                tuple(asdict(principales).values()),
            )

        # Otras tablas si existen
        for nombre, df in tablas.items():
            if pd is not None:
                try:
                    from pandas import DataFrame as _DataFrame
                    if df is not None and isinstance(df, _DataFrame):
                        df.to_sql(nombre, conn, index=False)
                except Exception:
                    continue
    finally:
        conn.close()


def _guardar_csv_referencia(path_csv: Path, principales: DatosPrincipales) -> None:
    encabezados = [
        "campo", "valor", "unidad", "fuente", "fecha"
    ]
    filas = []
    d = asdict(principales)
    mapa_unidades = {
        "eslora_total_m": "m",
        "eslora_entre_perpendiculares_m": "m",
        "manga_m": "m",
        "puntal_m": "m",
        "calado_m": "m",
        "coeficiente_de_bloque": "-",
        "coeficiente_prismatico": "-",
        "coeficiente_de_seccion_media": "-",
    }
    for k in [
        "eslora_total_m",
        "eslora_entre_perpendiculares_m",
        "manga_m",
        "puntal_m",
        "calado_m",
        "coeficiente_de_bloque",
        "coeficiente_prismatico",
        "coeficiente_de_seccion_media",
    ]:
        filas.append([
            k, d.get(k), mapa_unidades.get(k, "-"), d.get("fuente"), d.get("fecha")
        ])
    if pd is not None:
        df = pd.DataFrame(filas, columns=encabezados)
        df.to_csv(path_csv, index=False)
    else:
        # Fallback mínimo
        with path_csv.open("w", encoding="utf-8") as f:
            f.write(",".join(encabezados) + "\n")
            for fila in filas:
                f.write(",".join(str(x) if x is not None else "" for x in fila) + "\n")


def _guardar_json_actualizado(path_json: Path, base_json: Dict[str, Any], principales: DatosPrincipales) -> None:
    out = dict(base_json) if isinstance(base_json, dict) else {}
    out.setdefault("buque", {})
    out["buque"].update({
        "nombre": principales.nombre,
        "eslora_total_m": principales.eslora_total_m,
        "eslora_entre_perpendiculares_m": principales.eslora_entre_perpendiculares_m,
        "manga_m": principales.manga_m,
        "puntal_m": principales.puntal_m,
        "calado_m": principales.calado_m,
        "coeficiente_de_bloque": principales.coeficiente_de_bloque,
        "coeficiente_prismatico": principales.coeficiente_prismatico,
        "coeficiente_de_seccion_media": principales.coeficiente_de_seccion_media,
    })
    with path_json.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Consolidar y actualizar datos del buque (SI)")
    parser.add_argument("--input-dir", default="salidas/disposicion_general", help="Carpeta con fuentes (JSON/CSV/Excel)")
    parser.add_argument("--excel", default=None, help="Ruta al Excel de trabajo si se desea considerar")
    parser.add_argument("--eslora-total", type=float, default=None, help="Eslora total (m)")
    parser.add_argument("--eslora-pp", type=float, default=None, help="Eslora entre perpendiculares (m)")
    parser.add_argument("--manga", type=float, default=None, help="Manga (m)")
    parser.add_argument("--puntal", type=float, default=None, help="Puntal (m)")
    parser.add_argument("--calado", type=float, default=None, help="Calado (m)")
    parser.add_argument("--cb", type=float, default=None, help="Coeficiente de bloque (-)")
    parser.add_argument("--cp", type=float, default=None, help="Coeficiente prismático (-)")
    parser.add_argument("--csm", type=float, default=None, help="Coeficiente de sección media (-)")

    # Parámetros para VDc (doble casco)
    parser.add_argument("--ldc", type=float, default=None, help="Longitud de doble casco (m)")
    parser.add_argument("--bdc", type=float, default=None, help="Ancho efectivo de doble casco (m)")
    parser.add_argument("--ddf", type=float, default=None, help="Altura del doble fondo (m)")

    # Dimensionamiento de combustible
    parser.add_argument("--autonomia-dias", type=float, default=None, help="Autonomía (días)")
    parser.add_argument("--densidad-fuel", type=float, default=0.85, help="Densidad del combustible (t/m3)")
    parser.add_argument("--ce", type=float, default=None, help="Consumo específico MP (kg/kWh)")
    parser.add_argument("--cea", type=float, default=None, help="Consumo específico MMAA (kg/kWh)")
    parser.add_argument("--cec", type=float, default=None, help="Consumo específico caldera (kg/kWh)")
    parser.add_argument("--pa", type=float, default=None, help="Potencia auxiliares Pa (kW)")
    parser.add_argument("--po", type=float, default=None, help="Potencia caldera Po (kW)")
    parser.add_argument("--fuel-sed", type=float, default=0.03, help="Fracción de sedimentación (0-1)")
    parser.add_argument("--fuel-util", type=float, default=0.95, help="Factor de utilización (0-1)")

    # Estimación LcM/VCM
    parser.add_argument("--motor-tipo", choices=["2t", "4t"], default="4t", help="Tipo de motor principal")
    parser.add_argument("--c1", type=float, default=1.6, help="Coeficiente C1 para LcM")
    parser.add_argument("--c2", type=float, default=8.0, help="Coeficiente C2 para LcM")
    parser.add_argument("--ddf-cm", type=float, default=None, help="Altura del doble fondo en cámara de máquinas (m)")
    args = parser.parse_args()

    base_dir = Path(args.input_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    # Cargar JSON base si existe
    json_base_path = base_dir / "resumen_disposicion.json"
    json_base = _leer_json(json_base_path) or {}

    principales = _inferir_principales_de_json(json_base)

    # Cargar Excel si se solicita
    excel_path = None
    if args.excel:
        excel_path = Path(args.excel)
    else:
        # Intentar localizar alguno por defecto
        for default_excel in ["Trabajo Tema 3.xlsx", "disposicion_general.xlsx"]:
            p = base_dir / default_excel
            if p.exists():
                excel_path = p
                break

    hojas_excel: Dict[str, Any] = {}
    if excel_path is not None:
        hojas_excel = _leer_excel(excel_path)
        inferido = _inferir_principales_de_excels(hojas_excel)
        if inferido is not None:
            # Tomar lo mejor de ambos (Excel puede completar valores faltantes)
            for campo, valor in asdict(inferido).items():
                if getattr(principales, campo, None) in (None, "") and valor not in (None, ""):
                    setattr(principales, campo, valor)
            principales.fuente = inferido.fuente

        # Extraer segmentos detallados y generar análisis/CSVs
        seg = _extraer_segmentos_excel(hojas_excel)
        extra = _generar_segmentos_y_cuadernas(base_dir, seg, espac_central=0.7, espac_extremos=0.6)

        # Ajustar Lpp de principales si se obtuvo por suma
        lpp_sum = extra.get("resumen", {}).get("lpp_m")
        if lpp_sum:
            principales.eslora_entre_perpendiculares_m = lpp_sum
        # Exportar cuadernas con origen en AP (popa)
        _exportar_cuadernas_origen_popa(base_dir, lpp_sum or principales.eslora_entre_perpendiculares_m or 0.0)

    # Aplicar overrides CLI
    override_map = {
        "eslora_total_m": args.eslora_total,
        "eslora_entre_perpendiculares_m": args.eslora_pp,
        "manga_m": args.manga,
        "puntal_m": args.puntal,
        "calado_m": args.calado,
        "coeficiente_de_bloque": args.cb,
        "coeficiente_prismatico": args.cp,
        "coeficiente_de_seccion_media": args.csm,
    }
    principales = _merge_principales(principales, override_map)
    principales = _asegurar_metricas(principales)

    # Cargar tablas CSV si existen
    tablas: Dict[str, Any] = {}
    for nombre_csv in [
        "mamparos.csv", "espacios.csv", "tanques.csv", "bodegas.csv",
        "resumen_tanques.csv", "balance_combustible.csv"
    ]:
        df = _leer_csv(base_dir / nombre_csv)
        if df is not None:
            tablas[nombre_csv.replace(".csv", "")] = df

    # Guardar SQLite
    output_db = base_dir / "datos_buque.db"
    _guardar_sqlite(output_db, principales, tablas)

    # Guardar CSV de referencia
    output_csv = base_dir / "tabla_referencia.csv"
    _guardar_csv_referencia(output_csv, principales)

    # Guardar JSON actualizado (merge del base + principales)
    output_json = base_dir / "resumen_disposicion_actualizado.json"
    _guardar_json_actualizado(output_json, json_base or {}, principales)

    # Cálculos adicionales opcionales según parámetros
    # 1) Volumen doble casco (usar defaults si faltan)
    vdc = _calcular_volumen_doble_casco(
        args.ldc, args.bdc, principales.puntal_m, args.ddf or args.ddf_cm, args.cb or principales.coeficiente_de_bloque
    )
    if any(v is not None for v in [args.ldc, args.bdc, args.ddf, args.ddf_cm, args.cb]):
        _emitir_volumen_doble_casco(base_dir, vdc, {
            "ldc": args.ldc, "bdc": args.bdc, "D": principales.puntal_m,
            "ddf": args.ddf or args.ddf_cm, "cb": args.cb or principales.coeficiente_de_bloque,
            "fuente": "CLI/Principales"
        })

    # 2) Dimensionamiento de combustible
    dim_comb = _dimensionar_combustible(
        P_kw=args.eslora_total,  # placeholder? P no solicitado explícitamente, intentar usar P de Excel más adelante
        Pa_kw=args.pa, Po_kw=args.po,
        Ce_kg_kwh=args.ce, Cea_kg_kwh=args.cea, Cec_kg_kwh=args.cec,
        autonomia_dias=args.autonomia_dias, densidad_ton_m3=args.densidad_fuel,
        factor_sedimento=args.fuel_sed, factor_utilizacion=args.fuel_util,
    )
    # Solo exportar si se suministraron parámetros clave
    if any(v is not None for v in [args.ce, args.autonomia_dias]):
        _emitir_dimensionamiento_combustible(base_dir, dim_comb, {
            "P_kw": args.eslora_total, "Pa_kw": args.pa, "Po_kw": args.po,
            "Ce_kg_kwh": args.ce, "Cea_kg_kwh": args.cea, "Cec_kg_kwh": args.cec,
            "autonomia_dias": args.autonomia_dias, "densidad_ton_m3": args.densidad_fuel,
            "fuel_sed": args.fuel_sed, "fuel_util": args.fuel_util,
        })

    # 3) Estimación LcM/VCM
    est_cm = _estimar_lcm_vcm(
        motor_tipo=args.motor_tipo, P_kw=args.eslora_total, c1=args.c1, c2=args.c2,
        B=principales.manga_m, D=principales.puntal_m, ddf_cm=args.ddf_cm or args.ddf, cb=args.cb or principales.coeficiente_de_bloque,
    )
    if any(v is not None for v in est_cm.values()):
        _emitir_dimensionamiento_cm(base_dir, est_cm, {
            "motor_tipo": args.motor_tipo, "c1": args.c1, "c2": args.c2,
            "P_kw": args.eslora_total, "B": principales.manga_m, "D": principales.puntal_m, "ddf_cm": args.ddf_cm or args.ddf, "cb": args.cb or principales.coeficiente_de_bloque,
        })

    # Informe de análisis
    _emitir_informe_analisis(base_dir, principales, extra if excel_path is not None else {}, excel_path)

    # Mensaje resumen
    print("\n============================================")
    print("✅ Consolidación completada (Sistema Métrico)")
    print(f"📦 SQLite: {output_db}")
    print(f"📄 CSV referencia: {output_csv}")
    print(f"🧾 JSON actualizado: {output_json}")
    print("--------------------------------------------")
    print("Dimensiones principales (m):")
    print(f"  • Eslora total: {principales.eslora_total_m}")
    print(f"  • Eslora EPP:  {principales.eslora_entre_perpendiculares_m}")
    print(f"  • Manga:       {principales.manga_m}")
    print(f"  • Puntal:      {principales.puntal_m}")
    print(f"  • Calado:      {principales.calado_m}")
    print("--------------------------------------------")
    if excel_path:
        print(f"Excel considerado: {excel_path}")
    else:
        print("Excel considerado: (no especificado)")
    print("Fuentes cargadas:")
    print(f"  • JSON base: {'sí' if json_base_path.exists() else 'no'}")
    for t in ["mamparos", "espacios", "tanques", "bodegas", "resumen_tanques", "balance_combustible"]:
        print(f"  • {t}.csv: {'sí' if (base_dir / (t + '.csv')).exists() else 'no'}")
    print("============================================\n")


if __name__ == "__main__":
    main()
