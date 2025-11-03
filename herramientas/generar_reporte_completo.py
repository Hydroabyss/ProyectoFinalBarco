#!/usr/bin/env python3
"""Script para generar reporte completo del Buque Grupo 9 con integración de APIs."""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "maxsurf_integration"))

from dnv_verification.dnv_rules_checker import VerificadorDNV

def main():
    """Genera un reporte completo del buque con todas las verificaciones."""
    
    # Datos del Buque Grupo 9 (del PDF Trabajo 3)
    datos_buque = {
        'identificacion': {
            'nombre': 'Buque Grupo 9',
            'tipo': 'Buque de carga general',
            'clase': 'DNV',
            'fecha_analisis': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'dimensiones_principales': {
            'Lpp_m': 105.2,
            'manga_m': 15.99,
            'puntal_m': 7.90,
            'calado_m': 6.20,
            'francobordo_m': 1.70,
            'desplazamiento_t': 7752.9,
            'Cb': 0.7252
        },
        'estructura': {
            'doble_fondo_m': 1.20,
            'doble_costado_m': 1.80,
            'manga_interior_m': 12.39,
            'espaciamiento_cuadernas_m': 0.70,
            'segunda_cubierta_m': 5.20,
            'cubierta_principal_m': 7.90
        },
        'material': {
            'grado': 'AH36',
            'limite_elastico_MPa': 355,
            'normativa': 'DNV Pt.3 Ch.6'
        },
        'compartimentacion': {
            'pique_popa': {'inicio_m': 0.0, 'fin_m': 8.2, 'longitud_m': 8.2},
            'camara_maquinas': {'inicio_m': 8.2, 'fin_m': 23.2, 'longitud_m': 15.0},
            'bodega_3': {'inicio_m': 23.2, 'fin_m': 45.2, 'longitud_m': 22.0},
            'bodega_2': {'inicio_m': 45.2, 'fin_m': 72.2, 'longitud_m': 27.0},
            'bodega_1': {'inicio_m': 72.2, 'fin_m': 99.2, 'longitud_m': 27.0},
            'pique_proa': {'inicio_m': 99.2, 'fin_m': 105.2, 'longitud_m': 6.0}
        },
        'propulsion': {
            'motor_principal': {
                'modelo': 'MAN 6S50ME-C',
                'potencia_kW': 8500,
                'rpm': 127,
                'cilindros': 6,
                'tipo': 'Diesel 2 tiempos'
            },
            'generadores': {
                'modelo': 'CAT 3512C',
                'cantidad': 3,
                'potencia_unitaria_kW': 500,
                'potencia_total_kW': 1500
            },
            'helice': {
                'diametro_m': 4.20,
                'palas': 4,
                'tipo': 'Paso fijo'
            },
            'eje': {
                'diametro_m': 0.45,
                'longitud_bocina_m': 8.5
            }
        }
    }
    
    # Ejecutar verificaciones DNV
    print('=' * 80)
    print('REPORTE COMPLETO DE VERIFICACIÓN - BUQUE GRUPO 9')
    print('=' * 80)
    print(f"Fecha: {datos_buque['identificacion']['fecha_analisis']}")
    print(f"Tipo: {datos_buque['identificacion']['tipo']}")
    print(f"Clase: {datos_buque['identificacion']['clase']}")
    print()
    
    # 1. Dimensiones principales
    print('1. DIMENSIONES PRINCIPALES')
    print('-' * 80)
    dim = datos_buque['dimensiones_principales']
    print(f"  Eslora entre perpendiculares (Lpp): {dim['Lpp_m']} m")
    print(f"  Manga (B): {dim['manga_m']} m")
    print(f"  Puntal (D): {dim['puntal_m']} m")
    print(f"  Calado de diseño (T): {dim['calado_m']} m")
    print(f"  Francobordo (FB): {dim['francobordo_m']} m")
    print(f"  Desplazamiento (Δ): {dim['desplazamiento_t']} t")
    print(f"  Coeficiente de bloque (Cb): {dim['Cb']}")
    print()
    
    # 2. Verificaciones DNV
    ver = VerificadorDNV()
    
    print('2. VERIFICACIONES NORMATIVA DNV')
    print('-' * 80)
    
    # Relación L/B
    lb = ver.verificar_eslora_manga(dim['Lpp_m'], dim['manga_m'], 'commercial')
    print(f"  Relación L/B: {lb['relacion_LB']:.2f}")
    print(f"    Rango permitido: {lb['min']} - {lb['max']}")
    print(f"    Estado: {'✓ CUMPLE' if lb['cumple'] else '✗ NO CUMPLE'}")
    print()
    
    # Doble fondo
    doble_fondo_min = dim['manga_m'] / 20
    cumple_db = datos_buque['estructura']['doble_fondo_m'] >= doble_fondo_min
    print(f"  Doble fondo:")
    print(f"    Altura real: {datos_buque['estructura']['doble_fondo_m']} m")
    print(f"    Mínimo DNV (B/20): {doble_fondo_min:.3f} m")
    print(f"    Estado: {'✓ CUMPLE' if cumple_db else '✗ NO CUMPLE'} (DNV Pt.3 Ch.2 Sec.3)")
    print()
    
    # Doble costado
    doble_costado_min = 0.76 + 0.01 * dim['manga_m']
    cumple_dc = datos_buque['estructura']['doble_costado_m'] >= doble_costado_min
    print(f"  Doble costado:")
    print(f"    Ancho real: {datos_buque['estructura']['doble_costado_m']} m")
    print(f"    Mínimo SOLAS: {doble_costado_min:.3f} m")
    print(f"    Estado: {'✓ CUMPLE' if cumple_dc else '✗ NO CUMPLE'} (SOLAS II-1 Reg.13)")
    print()
    
    # Esfuerzos longitudinales
    velocidad_estimada = 14.0  # nudos
    esf = ver.calcular_esfuerzos_longitudinales_dnv(
        dim['Lpp_m'], dim['manga_m'], dim['puntal_m'], velocidad_estimada
    )
    print(f"  Esfuerzos longitudinales (V={velocidad_estimada} nudos):")
    print(f"    Momento de flexión vertical: {esf['momento_flexion_vertical']:.2f} N·m")
    print(f"    Esfuerzo cortante: {esf['esfuerzo_cortante']:.2f} N")
    print(f"    Coeficiente de ola DNV: {esf['coeficiente_ola_dnv']:.2f}")
    print(f"    Estado: {'✓ CUMPLE' if esf['cumple_dnv'] else '✗ NO CUMPLE'}")
    print()
    
    # 3. Compartimentación
    print('3. COMPARTIMENTACIÓN LONGITUDINAL')
    print('-' * 80)
    for nombre, datos in datos_buque['compartimentacion'].items():
        print(f"  {nombre.replace('_', ' ').title()}:")
        print(f"    Posición: {datos['inicio_m']:.1f} - {datos['fin_m']:.1f} m")
        print(f"    Longitud: {datos['longitud_m']:.1f} m")
    print()
    
    # 4. Sistema de propulsión
    print('4. SISTEMA DE PROPULSIÓN')
    print('-' * 80)
    motor = datos_buque['propulsion']['motor_principal']
    print(f"  Motor principal: {motor['modelo']}")
    print(f"    Potencia: {motor['potencia_kW']} kW @ {motor['rpm']} RPM")
    print(f"    Configuración: {motor['cilindros']} cilindros, {motor['tipo']}")
    print()
    
    gen = datos_buque['propulsion']['generadores']
    print(f"  Generadores auxiliares: {gen['cantidad']}x {gen['modelo']}")
    print(f"    Potencia unitaria: {gen['potencia_unitaria_kW']} kW")
    print(f"    Potencia total: {gen['potencia_total_kW']} kW")
    print()
    
    helice = datos_buque['propulsion']['helice']
    print(f"  Hélice: Ø{helice['diametro_m']} m, {helice['palas']} palas, {helice['tipo']}")
    print()
    
    # 5. Resumen de cumplimiento
    print('5. RESUMEN DE CUMPLIMIENTO NORMATIVO')
    print('-' * 80)
    cumplimientos = [
        ('Relación L/B', lb['cumple']),
        ('Doble fondo', cumple_db),
        ('Doble costado', cumple_dc),
        ('Esfuerzos longitudinales', esf['cumple_dnv'])
    ]
    
    total = len(cumplimientos)
    cumplidos = sum(1 for _, cumple in cumplimientos if cumple)
    
    for nombre, cumple in cumplimientos:
        print(f"  {'✓' if cumple else '✗'} {nombre}")
    
    print()
    print(f"  RESULTADO GLOBAL: {cumplidos}/{total} verificaciones cumplidas")
    print(f"  Porcentaje de cumplimiento: {(cumplidos/total)*100:.1f}%")
    print()
    
    # Guardar reporte completo
    output_dir = Path(__file__).parent.parent / "salidas" / "reportes"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    reporte_completo = {
        'buque': datos_buque,
        'verificaciones_dnv': {
            'relacion_LB': lb,
            'doble_fondo': {
                'altura_real_m': datos_buque['estructura']['doble_fondo_m'],
                'minimo_dnv_m': round(doble_fondo_min, 3),
                'cumple': cumple_db
            },
            'doble_costado': {
                'ancho_real_m': datos_buque['estructura']['doble_costado_m'],
                'minimo_solas_m': round(doble_costado_min, 3),
                'cumple': cumple_dc
            },
            'esfuerzos_longitudinales': esf
        },
        'resumen': {
            'total_verificaciones': total,
            'verificaciones_cumplidas': cumplidos,
            'porcentaje_cumplimiento': round((cumplidos/total)*100, 1)
        }
    }
    
    # Guardar JSON
    output_json = output_dir / "reporte_completo_buque_grupo9.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(reporte_completo, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Reporte JSON guardado en: {output_json}")
    print(f"✓ Reporte completo generado exitosamente")
    print()
    print('=' * 80)

if __name__ == "__main__":
    main()
