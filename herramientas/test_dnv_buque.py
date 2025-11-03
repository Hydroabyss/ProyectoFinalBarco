#!/usr/bin/env python3
"""Script para verificar el buque Grupo 9 con normativa DNV."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "maxsurf_integration"))

from dnv_verification.dnv_rules_checker import VerificadorDNV

def main():
    # Datos del Buque Grupo 9
    Lpp = 105.2
    B = 15.99
    D = 7.90
    T = 6.20
    velocidad = 14.0  # nudos estimado para buque de carga
    
    ver = VerificadorDNV()
    
    # 1. Cargar normativa DNV para buque comercial
    print('=' * 60)
    print('NORMATIVA DNV APLICABLE - BUQUE COMERCIAL')
    print('=' * 60)
    reglas = ver.cargar_normativa_dnv('commercial')
    print(json.dumps(reglas, ensure_ascii=False, indent=2))
    
    # 2. Verificar relación L/B
    print('\n' + '=' * 60)
    print('VERIFICACIÓN RELACIÓN L/B')
    print('=' * 60)
    lb = ver.verificar_eslora_manga(Lpp, B, 'commercial')
    print(json.dumps(lb, ensure_ascii=False, indent=2))
    print(f"\n✓ Relación L/B = {lb['relacion_LB']:.2f}")
    print(f"  Rango permitido: {lb['min']} - {lb['max']}")
    print(f"  Estado: {'✓ CUMPLE' if lb['cumple'] else '✗ NO CUMPLE'}")
    
    # 3. Calcular esfuerzos longitudinales DNV
    print('\n' + '=' * 60)
    print('ESFUERZOS LONGITUDINALES DNV')
    print('=' * 60)
    esf = ver.calcular_esfuerzos_longitudinales_dnv(Lpp, B, D, velocidad)
    print(json.dumps(esf, ensure_ascii=False, indent=2))
    print(f"\n✓ Momento de flexión vertical: {esf['momento_flexion_vertical']:.2f} N·m")
    print(f"✓ Esfuerzo cortante: {esf['esfuerzo_cortante']:.2f} N")
    print(f"✓ Coeficiente de ola DNV: {esf['coeficiente_ola_dnv']:.2f}")
    print(f"  Estado: {'✓ CUMPLE DNV' if esf['cumple_dnv'] else '✗ NO CUMPLE DNV'}")
    
    # 4. Verificaciones estructurales adicionales
    print('\n' + '=' * 60)
    print('VERIFICACIONES ESTRUCTURALES')
    print('=' * 60)
    
    doble_fondo_min = B / 20
    doble_costado_min = 0.76 + 0.01 * B
    
    verificaciones = {
        'doble_fondo': {
            'altura_real_m': 1.20,
            'minimo_dnv_m': round(doble_fondo_min, 3),
            'cumple': 1.20 >= doble_fondo_min,
            'normativa': 'DNV Pt.3 Ch.2 Sec.3'
        },
        'doble_costado': {
            'ancho_real_m': 1.80,
            'minimo_solas_m': round(doble_costado_min, 3),
            'cumple': 1.80 >= doble_costado_min,
            'normativa': 'SOLAS II-1 Reg.13'
        },
        'francobordo': {
            'valor_m': round(D - T, 2),
            'puntal_m': D,
            'calado_m': T
        },
        'material': {
            'grado': 'AH36',
            'limite_elastico_MPa': 355,
            'normativa': 'DNV Pt.3 Ch.6'
        }
    }
    
    print(json.dumps(verificaciones, ensure_ascii=False, indent=2))
    
    print('\n' + '=' * 60)
    print('RESUMEN DE CUMPLIMIENTO')
    print('=' * 60)
    print(f"✓ Doble fondo: {verificaciones['doble_fondo']['altura_real_m']}m " +
          f"(mín: {verificaciones['doble_fondo']['minimo_dnv_m']}m) - " +
          f"{'✓ CUMPLE' if verificaciones['doble_fondo']['cumple'] else '✗ NO CUMPLE'}")
    print(f"✓ Doble costado: {verificaciones['doble_costado']['ancho_real_m']}m " +
          f"(mín: {verificaciones['doble_costado']['minimo_solas_m']}m) - " +
          f"{'✓ CUMPLE' if verificaciones['doble_costado']['cumple'] else '✗ NO CUMPLE'}")
    print(f"✓ Relación L/B: {lb['relacion_LB']:.2f} - " +
          f"{'✓ CUMPLE' if lb['cumple'] else '✗ NO CUMPLE'}")
    print(f"✓ Material: {verificaciones['material']['grado']} " +
          f"(σy = {verificaciones['material']['limite_elastico_MPa']} MPa)")
    
    # Guardar resultados
    output_dir = Path(__file__).parent.parent / "salidas" / "dnv"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    resultados_completos = {
        'buque': {
            'Lpp_m': Lpp,
            'manga_m': B,
            'puntal_m': D,
            'calado_m': T,
            'velocidad_nudos': velocidad
        },
        'normativa': reglas,
        'relacion_LB': lb,
        'esfuerzos': esf,
        'verificaciones_estructurales': verificaciones
    }
    
    output_file = output_dir / "verificacion_buque_grupo9.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultados_completos, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Resultados guardados en: {output_file}")

if __name__ == "__main__":
    main()
