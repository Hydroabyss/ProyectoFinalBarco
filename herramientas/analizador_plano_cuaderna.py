#!/usr/bin/env python3

import ezdxf
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime

class AnalizadorPlanoCuaderna:
    
    def __init__(self, archivo_dxf: str):
        self.archivo = Path(archivo_dxf)
        self.doc = ezdxf.readfile(str(self.archivo))
        self.msp = self.doc.modelspace()
        self.errores = []
        self.advertencias = []
        self.info = []
        
    def analizar_completo(self) -> Dict:
        print("=" * 80)
        print("ANÁLISIS DE PLANO DE CUADERNA MAESTRA")
        print("=" * 80)
        print(f"Archivo: {self.archivo.name}")
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        resultado = {
            'archivo': str(self.archivo),
            'fecha_analisis': datetime.now().isoformat(),
            'capas': self.analizar_capas(),
            'geometria': self.analizar_geometria(),
            'estructura': self.analizar_estructura(),
            'dimensiones': self.extraer_dimensiones(),
            'errores': self.errores,
            'advertencias': self.advertencias,
            'info': self.info,
            'resumen': {}
        }
        
        resultado['resumen'] = {
            'total_errores': len(self.errores),
            'total_advertencias': len(self.advertencias),
            'estado': 'APROBADO' if len(self.errores) == 0 else 'REQUIERE CORRECCIONES'
        }
        
        self.imprimir_resumen(resultado)
        return resultado
    
    def analizar_capas(self) -> Dict:
        print("1. ANÁLISIS DE CAPAS")
        print("-" * 80)
        
        capas_esperadas = [
            'CASCO_EXTERIOR',
            'ESTRUCTURA_PRIMARIA',
            'ESTRUCTURA_SECUNDARIA',
            'MAMPAROS',
            'TANQUES',
            'LINEA_AGUA',
            'COTAS',
            'TEXTO',
            'EJES'
        ]
        
        capas_encontradas = [layer.dxf.name for layer in self.doc.layers]
        capas_info = {}
        
        for capa in capas_esperadas:
            if capa in capas_encontradas:
                entidades = [e for e in self.msp if e.dxf.layer == capa]
                capas_info[capa] = {
                    'existe': True,
                    'entidades': len(entidades),
                    'tipos': list(set([e.dxftype() for e in entidades]))
                }
                print(f"  ✓ {capa}: {len(entidades)} entidades")
                self.info.append(f"Capa {capa} encontrada con {len(entidades)} entidades")
            else:
                capas_info[capa] = {'existe': False, 'entidades': 0, 'tipos': []}
                print(f"  ⚠ {capa}: NO ENCONTRADA")
                self.advertencias.append(f"Capa {capa} no encontrada en el plano")
        
        print()
        return capas_info
    
    def analizar_geometria(self) -> Dict:
        print("2. ANÁLISIS DE GEOMETRÍA")
        print("-" * 80)
        
        geometria = {
            'lineas': 0,
            'arcos': 0,
            'circulos': 0,
            'polilineas': 0,
            'splines': 0,
            'textos': 0,
            'cotas': 0
        }
        
        for entidad in self.msp:
            tipo = entidad.dxftype()
            if tipo == 'LINE':
                geometria['lineas'] += 1
            elif tipo == 'ARC':
                geometria['arcos'] += 1
            elif tipo == 'CIRCLE':
                geometria['circulos'] += 1
            elif tipo in ['LWPOLYLINE', 'POLYLINE']:
                geometria['polilineas'] += 1
            elif tipo == 'SPLINE':
                geometria['splines'] += 1
            elif tipo == 'TEXT' or tipo == 'MTEXT':
                geometria['textos'] += 1
            elif tipo.startswith('DIMENSION'):
                geometria['cotas'] += 1
        
        print(f"  Líneas: {geometria['lineas']}")
        print(f"  Arcos: {geometria['arcos']}")
        print(f"  Círculos: {geometria['circulos']}")
        print(f"  Polilíneas: {geometria['polilineas']}")
        print(f"  Splines: {geometria['splines']}")
        print(f"  Textos: {geometria['textos']}")
        print(f"  Cotas: {geometria['cotas']}")
        print()
        
        if geometria['cotas'] == 0:
            self.advertencias.append("No se encontraron cotas en el plano")
        
        return geometria
    
    def analizar_estructura(self) -> Dict:
        print("3. ANÁLISIS DE ESTRUCTURA")
        print("-" * 80)
        
        estructura = {
            'casco_exterior': self.verificar_capa('CASCO_EXTERIOR'),
            'estructura_primaria': self.verificar_capa('ESTRUCTURA_PRIMARIA'),
            'estructura_secundaria': self.verificar_capa('ESTRUCTURA_SECUNDARIA'),
            'mamparos': self.verificar_capa('MAMPAROS'),
            'tanques': self.verificar_capa('TANQUES')
        }
        
        for elemento, datos in estructura.items():
            if datos['existe']:
                print(f"  ✓ {elemento.replace('_', ' ').title()}: {datos['entidades']} elementos")
            else:
                print(f"  ⚠ {elemento.replace('_', ' ').title()}: NO ENCONTRADO")
        
        print()
        return estructura
    
    def verificar_capa(self, nombre_capa: str) -> Dict:
        entidades = [e for e in self.msp if e.dxf.layer == nombre_capa]
        return {
            'existe': len(entidades) > 0,
            'entidades': len(entidades),
            'tipos': list(set([e.dxftype() for e in entidades]))
        }
    
    def extraer_dimensiones(self) -> Dict:
        print("4. EXTRACCIÓN DE DIMENSIONES")
        print("-" * 80)
        
        dimensiones = {
            'manga_total': None,
            'puntal_total': None,
            'doble_fondo': None,
            'doble_costado': None,
            'bbox': self.calcular_bbox()
        }
        
        bbox = dimensiones['bbox']
        if bbox:
            ancho = bbox['max_x'] - bbox['min_x']
            alto = bbox['max_y'] - bbox['min_y']
            
            dimensiones['manga_estimada'] = round(ancho, 2)
            dimensiones['puntal_estimado'] = round(alto, 2)
            
            print(f"  Manga estimada: {dimensiones['manga_estimada']} m")
            print(f"  Puntal estimado: {dimensiones['puntal_estimado']} m")
            print(f"  Bounding Box:")
            print(f"    X: {bbox['min_x']:.2f} a {bbox['max_x']:.2f} m")
            print(f"    Y: {bbox['min_y']:.2f} a {bbox['max_y']:.2f} m")
        
        print()
        return dimensiones
    
    def calcular_bbox(self) -> Dict:
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for entidad in self.msp:
            try:
                if hasattr(entidad, 'dxf') and hasattr(entidad.dxf, 'start'):
                    min_x = min(min_x, entidad.dxf.start.x)
                    min_y = min(min_y, entidad.dxf.start.y)
                    max_x = max(max_x, entidad.dxf.start.x)
                    max_y = max(max_y, entidad.dxf.start.y)
                if hasattr(entidad, 'dxf') and hasattr(entidad.dxf, 'end'):
                    min_x = min(min_x, entidad.dxf.end.x)
                    min_y = min(min_y, entidad.dxf.end.y)
                    max_x = max(max_x, entidad.dxf.end.x)
                    max_y = max(max_y, entidad.dxf.end.y)
                if hasattr(entidad, 'dxf') and hasattr(entidad.dxf, 'center'):
                    min_x = min(min_x, entidad.dxf.center.x)
                    min_y = min(min_y, entidad.dxf.center.y)
                    max_x = max(max_x, entidad.dxf.center.x)
                    max_y = max(max_y, entidad.dxf.center.y)
            except:
                pass
        
        if min_x == float('inf'):
            return None
        
        return {
            'min_x': round(min_x, 3),
            'min_y': round(min_y, 3),
            'max_x': round(max_x, 3),
            'max_y': round(max_y, 3)
        }
    
    def imprimir_resumen(self, resultado: Dict):
        print("=" * 80)
        print("RESUMEN DEL ANÁLISIS")
        print("=" * 80)
        print(f"Estado: {resultado['resumen']['estado']}")
        print(f"Errores: {resultado['resumen']['total_errores']}")
        print(f"Advertencias: {resultado['resumen']['total_advertencias']}")
        print()
        
        if self.errores:
            print("ERRORES DETECTADOS:")
            for i, error in enumerate(self.errores, 1):
                print(f"  {i}. {error}")
            print()
        
        if self.advertencias:
            print("ADVERTENCIAS:")
            for i, adv in enumerate(self.advertencias, 1):
                print(f"  {i}. {adv}")
            print()
    
    def guardar_reporte(self, archivo_salida: str):
        resultado = self.analizar_completo()
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Reporte guardado en: {archivo_salida}")
        return resultado


def main():
    import sys
    
    if len(sys.argv) < 2:
        archivo_dxf = "salidas/ENTREGA 3 v4/Corte_Transversal_Cuaderna_Maestra_Detallado.dxf"
    else:
        archivo_dxf = sys.argv[1]
    
    analizador = AnalizadorPlanoCuaderna(archivo_dxf)
    
    archivo_salida = "ENTREGA 4/analisis_plano_cuaderna.json"
    Path("ENTREGA 4").mkdir(exist_ok=True)
    
    resultado = analizador.guardar_reporte(archivo_salida)
    
    return 0 if resultado['resumen']['total_errores'] == 0 else 1


if __name__ == '__main__':
    exit(main())
