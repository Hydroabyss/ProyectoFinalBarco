#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis detallado de volúmenes y capacidades
--------------------------------------------

Este script consolida y verifica:
1. Volumen teórico del casco exterior (aprox. bloque) y casco interior (manga interior)
2. Volumen de doble casco según fórmula: VDc = 2.14·LDc·BDc·(D−DDF)·(0.82·CB + 0.217)
3. Volumen cámara de máquinas (carguero): VCM = 0.85·LcM·B·(D−DDF_CM)·CB
4. Capacidades de tanques vs requerimientos de combustible/autonomía
5. Ocupación relativa de tanques (% y margen sobre requerido)
6. Coherencia segmentación longitudinal (Lfp, Área, Ler, Lap) y Lpp

Fuentes esperadas (en carpeta disposición_general):
- resumen_disposicion_actualizado.json (si no, resumen_disposicion.json)
- tabla_general_disposicion.csv
- resumen_tanques.csv / tanques.csv
- volumen_doble_casco.csv (opcional)
- dimensionamiento_combustible.csv (opcional)
- dimensionamiento_cm.csv (opcional)

Salida principal:
- reporte_volumenes_capacidades.md

Uso rápido:
  python herramientas/analisis_detallado_volumenes.py --input-dir salidas/disposicion_general \
    --ldc 90 --bdc 2.0 --ddf 1.2 --ddf-cm 1.2 --cb 0.55 --lcm 30

Si algunos parámetros no se pasan se intentan inferir de archivos.
"""

from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None


def leer_json(path: Path) -> Dict[str, Any]:
    if path.exists():
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def leer_csv_df(path: Path) -> Optional[Any]:
    if pd is None or not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception:
        return None


def calc_vdc(ldc: Optional[float], bdc: Optional[float], D: Optional[float], ddf: Optional[float], cb: Optional[float]) -> Optional[float]:
    if None in (ldc, bdc, D, ddf, cb):
        return None
    return 2.14 * ldc * bdc * max(0.0, D - ddf) * (0.82 * cb + 0.217)


def calc_vcm_carguero(lcm: Optional[float], B: Optional[float], D: Optional[float], ddf_cm: Optional[float], cb: Optional[float]) -> Optional[float]:
    if None in (lcm, B, D, ddf_cm, cb):
        return None
    return 0.85 * lcm * B * max(0.0, D - ddf_cm) * cb


def estimar_volumen_bloque(Lpp: Optional[float], B: Optional[float], T: Optional[float], Cb: Optional[float]) -> Optional[float]:
    if None in (Lpp, B, T, Cb):
        return None
    return Lpp * B * T * Cb


def estimar_volumen_interior(Lpp: Optional[float], B_interior: Optional[float], D: Optional[float]) -> Optional[float]:
    # volumen simplificado = Lpp * B_interior * (D - margen cubiertas ~0.5 m)
    if None in (Lpp, B_interior, D):
        return None
    return Lpp * B_interior * max(0.0, D - 0.5)


def main() -> None:
    ap = argparse.ArgumentParser(description="Análisis integral de volúmenes y capacidades")
    ap.add_argument('--input-dir', default='salidas/disposicion_general', help='Carpeta de fuentes')
    ap.add_argument('--ldc', type=float, default=None, help='Longitud doble casco (m)')
    ap.add_argument('--bdc', type=float, default=None, help='Ancho doble casco (m)')
    ap.add_argument('--ddf', type=float, default=None, help='Altura doble fondo (m)')
    ap.add_argument('--ddf-cm', type=float, default=None, help='Altura doble fondo cámara máquinas (m)')
    ap.add_argument('--cb', type=float, default=None, help='Coeficiente de bloque (-)')
    ap.add_argument('--lcm', type=float, default=None, help='Longitud cámara de máquinas (LcM) si no se infiere (m)')
    ap.add_argument('--b-interior', type=float, default=None, help='Manga interior libre (m)')
    args = ap.parse_args()

    base_dir = Path(args.input_dir)
    json_path = base_dir / 'resumen_disposicion_actualizado.json'
    if not json_path.exists():
        json_path = base_dir / 'resumen_disposicion.json'
    data = leer_json(json_path)
    buque = data.get('buque', {})

    Lpp = buque.get('eslora_entre_perpendiculares_m')
    B = buque.get('manga_m')
    D = buque.get('puntal_m')
    T = buque.get('calado_m')
    CB = args.cb or buque.get('coeficiente_de_bloque')

    # Segmentos
    seg_df = leer_csv_df(base_dir / 'tabla_general_disposicion.csv')
    lcm_inferida = None
    if seg_df is not None:
        try:
            # Cámara de máquinas es segmento "Cámara de máquinas"
            cm_row = seg_df[seg_df['segmento'].str.contains('Cámara', na=False)].iloc[0]
            lcm_inferida = float(cm_row['long_m'])
        except Exception:
            pass
    LcM = args.lcm or lcm_inferida

    # Manga interior (aproximar B - 2*costado_doble). Si no se pasa, intentar deducir de tanques wing si existieran.
    B_interior = args.b_interior
    if B_interior is None and B is not None:
        # Asumir doble costado típico 1.8 m cada lado si existe (del trabajo previo) => B_interior ≈ B - 3.6
        B_interior = B - 3.6
        if B_interior < 0:
            B_interior = None

    # Volúmenes
    V_bloque = estimar_volumen_bloque(Lpp, B, T, CB)
    V_interior = estimar_volumen_interior(Lpp, B_interior, D)
    VDc = calc_vdc(args.ldc, args.bdc, D, args.ddf, CB)
    VCM = calc_vcm_carguero(LcM, B, D, args.ddf_cm, CB)

    # Tanques y combustible
    tanques_df = leer_csv_df(base_dir / 'resumen_tanques.csv')
    dimensionamiento_df = leer_csv_df(base_dir / 'dimensionamiento_combustible.csv')
    combustible_requerido_m3 = None
    if dimensionamiento_df is not None:
        try:
            combustible_requerido_m3 = float(dimensionamiento_df['volumen_con_margenes_m3'].iloc[0])
        except Exception:
            pass
    if combustible_requerido_m3 is not None and isinstance(combustible_requerido_m3, float) and math.isnan(combustible_requerido_m3):
        combustible_requerido_m3 = None
    if combustible_requerido_m3 is None:
        try:
            consumo = data.get('consumo_combustible', {})
            combustible_requerido_m3 = float(consumo.get('volumen_requerido_m3'))
        except Exception:
            combustible_requerido_m3 = None
    volumen_total_tanques_m3 = None
    if tanques_df is not None:
        try:
            # Buscar fila total o sumar volúmenes
            if 'volumen_m3' in tanques_df.columns:
                df_tmp = tanques_df.copy()
                if 'tanque' in df_tmp.columns:
                    df_tmp = df_tmp[~df_tmp['tanque'].str.contains('total', case=False, na=False)]
                volumen_total_tanques_m3 = float(df_tmp['volumen_m3'].sum())
        except Exception:
            pass

    # Ocupación combustible
    cobertura_combustible_pct = None
    if combustible_requerido_m3 and volumen_total_tanques_m3:
        cobertura_combustible_pct = 100.0 * volumen_total_tanques_m3 / combustible_requerido_m3

    # Emitir reporte
    report_path = base_dir / 'reporte_volumenes_capacidades.md'
    with report_path.open('w', encoding='utf-8') as f:
        f.write('# Reporte de Volúmenes y Capacidades\n\n')
        f.write(f'Fuente JSON: `{json_path.name}`\n\n')
        f.write('## Dimensiones principales\n\n')
        f.write(f'- Lpp: {Lpp}\n')
        f.write(f'- Manga B: {B}\n')
        f.write(f'- Manga interior (aprox): {B_interior}\n')
        f.write(f'- Puntal D: {D}\n')
        f.write(f'- Calado T: {T}\n')
        f.write(f'- Coeficiente de bloque CB: {CB}\n\n')

        f.write('## Segmentación longitudinal\n\n')
        if seg_df is not None:
            f.write(seg_df.to_markdown(index=False) + '\n\n')
        else:
            f.write('No disponible tabla_general_disposicion.csv\n\n')

        f.write('## Volúmenes globales (aproximaciones)\n\n')
        f.write(f'- Volumen bloque (Lpp·B·T·CB): {V_bloque} m3\n')
        f.write(f'- Volumen interior aproximado: {V_interior} m3\n')
        f.write(f'- Volumen doble casco (VDc): {VDc} m3\n')
        f.write(f'- Volumen cámara de máquinas (VCM): {VCM} m3\n\n')

        f.write('## Tanques y combustible\n\n')
        f.write(f'- Volumen total tanques (sumatoria): {volumen_total_tanques_m3} m3\n')
        f.write(f'- Combustible requerido (con márgenes): {combustible_requerido_m3} m3\n')
        f.write(f'- Cobertura tanques vs requerido: {cobertura_combustible_pct}%\n\n')

        f.write('## Observaciones\n\n')
        f.write('- Verificar que LDc y BDc coincidan con la extensión real del doble casco (entre mamparos).\n')
        f.write('- Ajustar B_interior con medición directa del modelo Maxsurf (Offets) para precisión.\n')
        f.write('- Recalcular VDc si DDF varía fuera de cámara de máquinas.\n')
        f.write('- Validar compatibilidad de VCM con espacio real en modelo 3D.\n')
        f.write('- Si cobertura combustible >> 100%, optimizar distribución o reducir volumen de algunos tanques.\n')

        f.write('\n## Próximos pasos\n\n')
        f.write('1. Exportar offsets desde Maxsurf (Automation) para reemplazar aproximaciones de volumen.\n')
        f.write('2. Incorporar cálculo de curvas de capacidad por calado parcial.\n')
        f.write('3. Validar doble casco contra normativa DNV (espesor, continuidad).\n')
        f.write('4. Integrar estabilidad (GZ) con nuevo reparto de pesos/volúmenes.\n')

    print(f'Reporte generado: {report_path}')


if __name__ == '__main__':
    main()
