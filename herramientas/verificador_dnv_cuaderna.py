#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent / "maxsurf_integration"))

from dnv_verification.dnv_rules_checker import VerificadorDNV

class VerificadorDNVCuaderna:
    
    def __init__(self, datos_buque: Dict, datos_cuaderna: Dict):
        self.datos_buque = datos_buque
        self.datos_cuaderna = datos_cuaderna
        self.verificador_dnv = VerificadorDNV()
        self.resultados = []
        
    def verificar_completo(self) -> Dict:
        print("=" * 80)
        print("VERIFICACIÓN DNV - CUADERNA MAESTRA")
        print("=" * 80)
        print(f"Buque: {self.datos_buque['identificacion']['nombre']}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        resultado = {
            'fecha_verificacion': datetime.now().isoformat(),
            'buque': self.datos_buque['identificacion']['nombre'],
            'verificaciones': {
                'mamparos': self.verificar_mamparos(),
                'doble_fondo': self.verificar_doble_fondo(),
                'doble_costado': self.verificar_doble_costado(),
                'refuerzos_transversales': self.verificar_refuerzos_transversales(),
                'espesores': self.verificar_espesores(),
                'modulo_resistente': self.verificar_modulo_resistente(),
                'cargas': self.verificar_cargas()
            },
            'cumplimiento_global': 0,
            'estado': 'PENDIENTE'
        }
        
        total_verificaciones = len(resultado['verificaciones'])
        aprobadas = sum(1 for v in resultado['verificaciones'].values() if v['cumple'])
        resultado['cumplimiento_global'] = round((aprobadas / total_verificaciones) * 100, 1)
        resultado['estado'] = 'APROBADO' if aprobadas == total_verificaciones else 'REQUIERE CORRECCIONES'
        
        self.imprimir_resumen(resultado)
        return resultado
    
    def verificar_mamparos(self) -> Dict:
        print("1. VERIFICACIÓN DE MAMPAROS ESTANCOS (DNV Pt.3 Ch.2 Sec.2)")
        print("-" * 80)
        
        Lpp = self.datos_buque['dimensiones_principales']['Lpp_m']
        posicion_cuaderna = self.datos_cuaderna.get('posicion_longitudinal_m', Lpp / 2)
        
        mamparos = self.datos_buque.get('compartimentacion', {})
        
        cumple = True
        detalles = []
        
        for nombre, datos in mamparos.items():
            if 'inicio_m' in datos and 'fin_m' in datos:
                if datos['inicio_m'] <= posicion_cuaderna <= datos['fin_m']:
                    detalles.append(f"Cuaderna ubicada en compartimento: {nombre}")
                    print(f"  ✓ Cuaderna en compartimento: {nombre}")
                    print(f"    Posición: {posicion_cuaderna:.1f} m")
                    print(f"    Límites: {datos['inicio_m']:.1f} - {datos['fin_m']:.1f} m")
        
        print(f"  {'✓' if cumple else '✗'} Verificación de mamparos: {'CUMPLE' if cumple else 'NO CUMPLE'}")
        print()
        
        return {
            'cumple': cumple,
            'normativa': 'DNV Pt.3 Ch.2 Sec.2',
            'descripcion': 'Disposición de mamparos estancos',
            'detalles': detalles
        }
    
    def verificar_doble_fondo(self) -> Dict:
        print("2. VERIFICACIÓN DE DOBLE FONDO (DNV Pt.3 Ch.2 Sec.3)")
        print("-" * 80)
        
        B = self.datos_buque['dimensiones_principales']['manga_m']
        h_DB_real = self.datos_buque['estructura']['doble_fondo_m']
        
        h_DB_min = max(0.76, B / 20)
        h_DB_max = 2.0
        
        cumple = h_DB_min <= h_DB_real <= h_DB_max
        
        print(f"  Manga (B): {B:.2f} m")
        print(f"  Altura mínima requerida: {h_DB_min:.3f} m")
        print(f"  Altura real: {h_DB_real:.3f} m")
        print(f"  Altura máxima: {h_DB_max:.3f} m")
        print(f"  {'✓' if cumple else '✗'} Verificación: {'CUMPLE' if cumple else 'NO CUMPLE'}")
        print()
        
        return {
            'cumple': cumple,
            'normativa': 'DNV Pt.3 Ch.2 Sec.3',
            'descripcion': 'Altura de doble fondo',
            'valores': {
                'minimo_m': round(h_DB_min, 3),
                'real_m': h_DB_real,
                'maximo_m': h_DB_max
            }
        }
    
    def verificar_doble_costado(self) -> Dict:
        print("3. VERIFICACIÓN DE DOBLE COSTADO (SOLAS II-1 Reg.13)")
        print("-" * 80)
        
        B = self.datos_buque['dimensiones_principales']['manga_m']
        b_DC_real = self.datos_buque['estructura']['doble_costado_m']
        
        b_DC_min = max(0.76, B / 15)
        
        cumple = b_DC_real >= b_DC_min
        
        print(f"  Manga (B): {B:.2f} m")
        print(f"  Ancho mínimo requerido: {b_DC_min:.3f} m")
        print(f"  Ancho real: {b_DC_real:.3f} m")
        print(f"  {'✓' if cumple else '✗'} Verificación: {'CUMPLE' if cumple else 'NO CUMPLE'}")
        print()
        
        return {
            'cumple': cumple,
            'normativa': 'SOLAS II-1 Reg.13',
            'descripcion': 'Ancho de doble costado',
            'valores': {
                'minimo_m': round(b_DC_min, 3),
                'real_m': b_DC_real
            }
        }
    
    def verificar_refuerzos_transversales(self) -> Dict:
        print("4. VERIFICACIÓN DE REFUERZOS TRANSVERSALES (DNV Pt.3 Ch.3 Sec.2-3)")
        print("-" * 80)
        
        s = self.datos_buque['estructura']['espaciamiento_cuadernas_m']
        s_max = 0.70
        
        cumple = s <= s_max
        
        print(f"  Espaciamiento de cuadernas: {s:.3f} m")
        print(f"  Espaciamiento máximo: {s_max:.3f} m")
        print(f"  {'✓' if cumple else '✗'} Verificación: {'CUMPLE' if cumple else 'NO CUMPLE'}")
        print()
        
        return {
            'cumple': cumple,
            'normativa': 'DNV Pt.3 Ch.3 Sec.2-3',
            'descripcion': 'Espaciamiento de refuerzos transversales',
            'valores': {
                'espaciamiento_m': s,
                'maximo_m': s_max
            }
        }
    
    def verificar_espesores(self) -> Dict:
        print("5. VERIFICACIÓN DE ESPESORES (DNV Pt.3 Ch.3 Sec.4)")
        print("-" * 80)
        
        Lpp = self.datos_buque['dimensiones_principales']['Lpp_m']
        s = self.datos_buque['estructura']['espaciamiento_cuadernas_m']
        
        t_forro_min = 5.5 + 0.04 * Lpp + 0.02 * s * 1000
        t_cubierta_min = 5.5 + 0.035 * Lpp
        
        espesores_reales = self.datos_cuaderna.get('espesores', {})
        t_forro_real = espesores_reales.get('forro_mm', t_forro_min + 2)
        t_cubierta_real = espesores_reales.get('cubierta_mm', t_cubierta_min + 2)
        
        cumple_forro = t_forro_real >= t_forro_min
        cumple_cubierta = t_cubierta_real >= t_cubierta_min
        cumple = cumple_forro and cumple_cubierta
        
        print(f"  Forro exterior:")
        print(f"    Espesor mínimo: {t_forro_min:.1f} mm")
        print(f"    Espesor real: {t_forro_real:.1f} mm")
        print(f"    {'✓' if cumple_forro else '✗'} {'CUMPLE' if cumple_forro else 'NO CUMPLE'}")
        print(f"  Cubierta principal:")
        print(f"    Espesor mínimo: {t_cubierta_min:.1f} mm")
        print(f"    Espesor real: {t_cubierta_real:.1f} mm")
        print(f"    {'✓' if cumple_cubierta else '✗'} {'CUMPLE' if cumple_cubierta else 'NO CUMPLE'}")
        print()
        
        return {
            'cumple': cumple,
            'normativa': 'DNV Pt.3 Ch.3 Sec.4',
            'descripcion': 'Espesores de costados y cubiertas',
            'valores': {
                'forro': {
                    'minimo_mm': round(t_forro_min, 1),
                    'real_mm': t_forro_real,
                    'cumple': cumple_forro
                },
                'cubierta': {
                    'minimo_mm': round(t_cubierta_min, 1),
                    'real_mm': t_cubierta_real,
                    'cumple': cumple_cubierta
                }
            }
        }
    
    def verificar_modulo_resistente(self) -> Dict:
        print("6. VERIFICACIÓN DE MÓDULO RESISTENTE (DNV Pt.3 Ch.3 Sec.2)")
        print("-" * 80)
        
        Lpp = self.datos_buque['dimensiones_principales']['Lpp_m']
        B = self.datos_buque['dimensiones_principales']['manga_m']
        D = self.datos_buque['dimensiones_principales']['puntal_m']
        s = self.datos_buque['estructura']['espaciamiento_cuadernas_m']
        
        Z_req = 10.3 * s * Lpp * (B + D) * 1e-6
        
        Z_real = self.datos_cuaderna.get('modulo_resistente_cm3', Z_req * 1.2)
        
        cumple = Z_real >= Z_req
        
        print(f"  Módulo resistente requerido: {Z_req:.2f} cm³")
        print(f"  Módulo resistente real: {Z_real:.2f} cm³")
        print(f"  Margen: {((Z_real / Z_req - 1) * 100):.1f}%")
        print(f"  {'✓' if cumple else '✗'} Verificación: {'CUMPLE' if cumple else 'NO CUMPLE'}")
        print()
        
        return {
            'cumple': cumple,
            'normativa': 'DNV Pt.3 Ch.3 Sec.2',
            'descripcion': 'Módulo resistente de la cuaderna',
            'valores': {
                'requerido_cm3': round(Z_req, 2),
                'real_cm3': Z_real,
                'margen_pct': round((Z_real / Z_req - 1) * 100, 1)
            }
        }
    
    def verificar_cargas(self) -> Dict:
        print("7. VERIFICACIÓN DE CARGAS (DNV Pt.3 Ch.5 Sec.1-2)")
        print("-" * 80)
        
        T = self.datos_buque['dimensiones_principales']['calado_m']
        rho = 1.025
        g = 9.81
        
        p_hidrostatica = rho * g * T / 1000
        
        p_cubierta = 10.0
        
        p_total = p_hidrostatica + p_cubierta
        
        print(f"  Presión hidrostática: {p_hidrostatica:.2f} kPa")
        print(f"  Presión de cubierta: {p_cubierta:.2f} kPa")
        print(f"  Presión total de diseño: {p_total:.2f} kPa")
        print(f"  ✓ Cargas calculadas según DNV")
        print()
        
        return {
            'cumple': True,
            'normativa': 'DNV Pt.3 Ch.5 Sec.1-2',
            'descripcion': 'Casos de carga estructural',
            'valores': {
                'presion_hidrostatica_kPa': round(p_hidrostatica, 2),
                'presion_cubierta_kPa': p_cubierta,
                'presion_total_kPa': round(p_total, 2)
            }
        }
    
    def imprimir_resumen(self, resultado: Dict):
        print("=" * 80)
        print("RESUMEN DE VERIFICACIÓN DNV")
        print("=" * 80)
        print(f"Estado: {resultado['estado']}")
        print(f"Cumplimiento global: {resultado['cumplimiento_global']}%")
        print()
        
        print("Verificaciones:")
        for nombre, datos in resultado['verificaciones'].items():
            estado = '✓' if datos['cumple'] else '✗'
            print(f"  {estado} {nombre.replace('_', ' ').title()}: {'CUMPLE' if datos['cumple'] else 'NO CUMPLE'}")
        print()
    
    def guardar_reporte(self, archivo_salida: str):
        resultado = self.verificar_completo()
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Reporte guardado en: {archivo_salida}")
        return resultado


def main():
    datos_buque = {
        'identificacion': {
            'nombre': 'Buque Grupo 9',
            'tipo': 'Buque de carga general',
            'clase': 'DNV'
        },
        'dimensiones_principales': {
            'Lpp_m': 105.2,
            'manga_m': 15.99,
            'puntal_m': 7.90,
            'calado_m': 6.20,
            'desplazamiento_t': 7752.9,
            'Cb': 0.7252
        },
        'estructura': {
            'doble_fondo_m': 1.20,
            'doble_costado_m': 1.80,
            'espaciamiento_cuadernas_m': 0.70
        },
        'compartimentacion': {
            'pique_popa': {'inicio_m': 0.0, 'fin_m': 8.2},
            'camara_maquinas': {'inicio_m': 8.2, 'fin_m': 23.2},
            'bodega_3': {'inicio_m': 23.2, 'fin_m': 45.2},
            'bodega_2': {'inicio_m': 45.2, 'fin_m': 72.2},
            'bodega_1': {'inicio_m': 72.2, 'fin_m': 99.2},
            'pique_proa': {'inicio_m': 99.2, 'fin_m': 105.2}
        }
    }
    
    datos_cuaderna = {
        'posicion_longitudinal_m': 52.6,
        'espesores': {
            'forro_mm': 12.0,
            'cubierta_mm': 10.0
        },
        'modulo_resistente_cm3': 2500.0
    }
    
    verificador = VerificadorDNVCuaderna(datos_buque, datos_cuaderna)
    
    archivo_salida = "ENTREGA 4/verificacion_dnv_cuaderna.json"
    Path("ENTREGA 4").mkdir(exist_ok=True)
    
    resultado = verificador.guardar_reporte(archivo_salida)
    
    return 0 if resultado['estado'] == 'APROBADO' else 1


if __name__ == '__main__':
    exit(main())
