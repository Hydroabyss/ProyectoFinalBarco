"""
Tank Designer - Diseñador de Tanques
===================================

Módulo para diseño, cubicación y distribución de tanques.
Implementa cálculos para tanques de combustible, agua y lastre.

Características:
    - Diseño de distribución de tanques
    - Cubicación automática
    - Cálculo de consumos y autonomía
    - Verificación de capacidades
    - Optimización de distribución (KG)
"""

import logging
from typing import Dict, List, Optional, Tuple
import pandas as pd
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class TankDesigner:
    """
    Diseñador de tanques para Maxsurf.
    
    Permite diseñar y cubicar tanques de combustible,
    agua y lastre para el buque.
    """
    
    def __init__(self, maxsurf_connector):
        """
        Inicializar diseñador de tanques.
        
        Args:
            maxsurf_connector: Instancia de MaxsurfConnector
        """
        self.maxsurf = maxsurf_connector
        self.tanques = []
        self.densidades = {
            'fuel_oil': 0.85,      # t/m³
            'diesel': 0.84,
            'agua_dulce': 1.00,
            'agua_mar': 1.025,
            'lastre': 1.025
        }
        
        logger.info("⛽ Tank Designer inicializado")
    
    def calcular_volumen_combustible(
        self,
        autonomia_nm: float,
        velocidad_kn: float,
        consumo_diario_ton: float
    ) -> Dict[str, float]:
        """
        Calcular volumen de combustible necesario.
        
        Args:
            autonomia_nm: Autonomía requerida (millas náuticas)
            velocidad_kn: Velocidad de crucero (nudos)
            consumo_diario_ton: Consumo diario (toneladas/día)
            
        Returns:
            Dict con cálculos de combustible
        """
        logger.info("⛽ Calculando requerimientos de combustible...")
        logger.info(f"   Autonomía: {autonomia_nm} nm")
        logger.info(f"   Velocidad: {velocidad_kn} kn")
        logger.info(f"   Consumo: {consumo_diario_ton} t/día")
        
        try:
            # Tiempo de navegación
            tiempo_dias = autonomia_nm / (velocidad_kn * 24)
            
            # Masa de combustible necesaria
            masa_fuel_ton = consumo_diario_ton * tiempo_dias
            
            # Volumen necesario
            volumen_fuel_m3 = masa_fuel_ton / self.densidades['fuel_oil']
            
            # Agregar margen de seguridad (10%)
            volumen_con_margen = volumen_fuel_m3 * 1.10
            
            resultado = {
                'tiempo_navegacion_dias': tiempo_dias,
                'masa_fuel_ton': masa_fuel_ton,
                'volumen_fuel_m3': volumen_fuel_m3,
                'volumen_con_margen_m3': volumen_con_margen,
                'margen_seguridad_pct': 10
            }
            
            logger.info(f"✅ Volumen combustible calculado:")
            logger.info(f"   Tiempo navegación: {tiempo_dias:.2f} días")
            logger.info(f"   Masa requerida: {masa_fuel_ton:.2f} t")
            logger.info(f"   Volumen neto: {volumen_fuel_m3:.2f} m³")
            logger.info(f"   Volumen con margen: {volumen_con_margen:.2f} m³")
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Error calculando combustible: {e}")
            return {}
    
    def diseñar_tanques_buque9(
        self,
        escenario_consumo: str = 'realista'
    ) -> List[Dict]:
        """
        Diseñar distribución de tanques para Buque 9.
        
        Args:
            escenario_consumo: 'economico' (2 t/día), 'realista' (5 t/día), 
                              'pesado' (10 t/día)
            
        Returns:
            List de tanques diseñados
        """
        logger.info(f"🚢 Diseñando tanques para Buque 9 - Escenario: {escenario_consumo}")
        
        # Parámetros del Buque 9
        LOA = 97.7  # m
        beam = 14.3  # m
        autonomia = 10000  # nm
        velocidad = 14  # kn
        
        # Escenarios de consumo
        consumos = {
            'economico': 2.0,   # t/día
            'realista': 5.0,
            'pesado': 10.0
        }
        
        consumo = consumos.get(escenario_consumo, 5.0)
        
        # Calcular volumen necesario
        req_fuel = self.calcular_volumen_combustible(autonomia, velocidad, consumo)
        volumen_total_fuel = req_fuel.get('volumen_con_margen_m3', 0)
        
        # Diseñar distribución de tanques
        tanques_diseñados = []
        
        # Tanque 1: Combustible Principal (doble fondo central fore)
        tanques_diseñados.append({
            'nombre': 'FUEL_CENTRAL_FORE',
            'tipo': 'fuel_oil',
            'ubicacion': 'doble_fondo',
            'longitud_m': 24.0,
            'ancho_efectivo_m': 12.0,
            'altura_util_m': 0.6,
            'volumen_m3': 24.0 * 12.0 * 0.6,
            'posicion_x_desde_proa_m': 24.0,
            'kg_estimado_m': 0.3,  # Altura CG sobre quilla
            'densidad_tm3': self.densidades['fuel_oil']
        })
        
        # Tanque 2: Combustible Principal (doble fondo central aft)
        tanques_diseñados.append({
            'nombre': 'FUEL_CENTRAL_AFT',
            'tipo': 'fuel_oil',
            'ubicacion': 'doble_fondo',
            'longitud_m': 24.0,
            'ancho_efectivo_m': 12.0,
            'altura_util_m': 0.6,
            'volumen_m3': 24.0 * 12.0 * 0.6,
            'posicion_x_desde_proa_m': 48.0,
            'kg_estimado_m': 0.3,
            'densidad_tm3': self.densidades['fuel_oil']
        })
        
        # Tanques 3 y 4: Wing tanks para ajuste fino
        for lado in ['PORT', 'STBD']:
            tanques_diseñados.append({
                'nombre': f'FUEL_WING_{lado}',
                'tipo': 'fuel_oil',
                'ubicacion': f'wing_tank_{lado.lower()}',
                'longitud_m': 15.0,
                'ancho_efectivo_m': 1.2,
                'altura_util_m': 0.8,
                'volumen_m3': 15.0 * 1.2 * 0.8,
                'posicion_x_desde_proa_m': 40.0,
                'kg_estimado_m': 0.4,
                'densidad_tm3': self.densidades['fuel_oil']
            })
        
        # Tanques de agua dulce
        vol_agua_dulce = 50.0  # m³ estimado para tripulación
        tanques_diseñados.append({
            'nombre': 'FRESH_WATER',
            'tipo': 'agua_dulce',
            'ubicacion': 'doble_fondo',
            'longitud_m': 8.0,
            'ancho_efectivo_m': 5.0,
            'altura_util_m': 1.2,
            'volumen_m3': vol_agua_dulce,
            'posicion_x_desde_proa_m': 72.0,
            'kg_estimado_m': 0.6,
            'densidad_tm3': self.densidades['agua_dulce']
        })
        
        # Tanques de lastre
        for i, pos_x in enumerate([12.0, 84.0]):  # Fore y aft
            tanques_diseñados.append({
                'nombre': f'BALLAST_{"FORE" if i == 0 else "AFT"}',
                'tipo': 'lastre',
                'ubicacion': 'doble_fondo',
                'longitud_m': 10.0,
                'ancho_efectivo_m': 12.0,
                'altura_util_m': 0.8,
                'volumen_m3': 10.0 * 12.0 * 0.8,
                'posicion_x_desde_proa_m': pos_x,
                'kg_estimado_m': 0.4,
                'densidad_tm3': self.densidades['lastre']
            })
        
        # Calcular totales
        vol_fuel_total = sum(t['volumen_m3'] for t in tanques_diseñados 
                            if t['tipo'] == 'fuel_oil')
        
        logger.info(f"\n📊 Resumen de tanques diseñados:")
        logger.info(f"   Total tanques: {len(tanques_diseñados)}")
        logger.info(f"   Volumen combustible total: {vol_fuel_total:.2f} m³")
        logger.info(f"   Volumen requerido: {volumen_total_fuel:.2f} m³")
        
        if vol_fuel_total >= volumen_total_fuel:
            logger.info(f"   ✅ Capacidad SUFICIENTE (margen: {vol_fuel_total - volumen_total_fuel:.2f} m³)")
        else:
            logger.warning(f"   ⚠️  Capacidad INSUFICIENTE (falta: {volumen_total_fuel - vol_fuel_total:.2f} m³)")
        
        self.tanques = tanques_diseñados
        return tanques_diseñados
    
    def crear_tanques_en_maxsurf(self, tanques: Optional[List[Dict]] = None) -> bool:
        """
        Crear tanques en el modelo de Maxsurf.
        
        Args:
            tanques: Lista de tanques a crear (usa self.tanques si None)
            
        Returns:
            bool: True si se crearon exitosamente
        """
        if tanques is None:
            tanques = self.tanques
        
        if not tanques:
            logger.warning("⚠️  No hay tanques para crear")
            return False
        
        logger.info(f"🔧 Creando {len(tanques)} tanques en Maxsurf...")
        
        try:
            for tank in tanques:
                logger.debug(f"Creando tanque: {tank['nombre']}")
                
                # Comandos para crear tanque en Maxsurf
                # Nota: Adaptar a comandos reales de Maxsurf API
                self.maxsurf.execute_command(f"TANK NEW {tank['nombre']}")
                self.maxsurf.execute_command(f"TANK {tank['nombre']} TYPE {tank['tipo']}")
                self.maxsurf.execute_command(f"TANK {tank['nombre']} VOLUME {tank['volumen_m3']}")
                
                # Posicionamiento (si API lo soporta)
                # self.maxsurf.execute_command(f"TANK {tank['nombre']} POS {tank['posicion_x_desde_proa_m']}")
            
            logger.info("✅ Tanques creados exitosamente en Maxsurf")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creando tanques en Maxsurf: {e}")
            return False
    
    def cubicar_tanques(self) -> pd.DataFrame:
        """
        Cubicar tanques y obtener volúmenes y centroides.
        
        Returns:
            DataFrame con resultados de cubicación
        """
        logger.info("📐 Cubicando tanques...")
        
        try:
            # Ejecutar cubicación en Maxsurf
            self.maxsurf.execute_command("TANKS CALCULATE")
            
            # Obtener resultados
            # Nota: Adaptar a API real para obtener resultados
            
            resultados = []
            for tank in self.tanques:
                # Aquí se obtendrían los valores reales de Maxsurf
                resultados.append({
                    'nombre': tank['nombre'],
                    'tipo': tank['tipo'],
                    'volumen_m3': tank['volumen_m3'],
                    'masa_lleno_t': tank['volumen_m3'] * tank['densidad_tm3'],
                    'kg_m': tank['kg_estimado_m'],
                    'lcg_m': tank['posicion_x_desde_proa_m']
                })
            
            df_resultados = pd.DataFrame(resultados)
            
            logger.info(f"✅ {len(resultados)} tanques cubicados")
            return df_resultados
            
        except Exception as e:
            logger.error(f"❌ Error cubicando tanques: {e}")
            return pd.DataFrame()
    
    def calcular_kg_con_tanques(
        self,
        condicion: str = 'llenos'
    ) -> float:
        """
        Calcular KG (altura del CG) con tanques en condición especificada.
        
        Args:
            condicion: 'llenos', 'vacios', '50%', etc.
            
        Returns:
            float: KG total en metros
        """
        logger.info(f"📊 Calculando KG con tanques {condicion}...")
        
        try:
            # Factor de llenado
            factor_llenado = {
                'llenos': 1.0,
                'vacios': 0.0,
                '50%': 0.5,
                '75%': 0.75
            }.get(condicion, 1.0)
            
            momento_total = 0.0
            masa_total = 0.0
            
            for tank in self.tanques:
                masa_tank = tank['volumen_m3'] * tank['densidad_tm3'] * factor_llenado
                momento_tank = masa_tank * tank['kg_estimado_m']
                
                momento_total += momento_tank
                masa_total += masa_tank
            
            if masa_total > 0:
                kg = momento_total / masa_total
                logger.info(f"✅ KG calculado: {kg:.3f} m (masa total tanques: {masa_total:.2f} t)")
                return kg
            else:
                logger.warning("⚠️  Masa total de tanques es cero")
                return 0.0
            
        except Exception as e:
            logger.error(f"❌ Error calculando KG: {e}")
            return 0.0
    
    def exportar_tanques(self, filepath: str, formato: str = 'csv') -> bool:
        """
        Exportar diseño de tanques.
        
        Args:
            filepath: Ruta del archivo
            formato: 'csv' o 'json'
            
        Returns:
            bool: True si se exportó correctamente
        """
        logger.info(f"📤 Exportando tanques a: {filepath}")
        
        try:
            if formato == 'csv':
                df = pd.DataFrame(self.tanques)
                df.to_csv(filepath, index=False)
            elif formato == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.tanques, f, indent=2, ensure_ascii=False)
            
            logger.info("✅ Tanques exportados exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error exportando tanques: {e}")
            return False
    
    def generar_tabla_tanques(self) -> str:
        """
        Generar tabla de tanques en formato Markdown.
        
        Returns:
            str: Tabla en Markdown
        """
        if not self.tanques:
            return "No hay tanques diseñados."
        
        tabla = "## Tabla de Tanques\n\n"
        tabla += "| Nombre | Tipo | Ubicación | Volumen (m³) | Longitud (m) | KG (m) |\n"
        tabla += "|--------|------|-----------|--------------|--------------|--------|\n"
        
        for tank in self.tanques:
            tabla += f"| {tank['nombre']} | {tank['tipo']} | {tank['ubicacion']} | "
            tabla += f"{tank['volumen_m3']:.2f} | {tank['longitud_m']:.1f} | "
            tabla += f"{tank['kg_estimado_m']:.2f} |\n"
        
        # Totales
        vol_total = sum(t['volumen_m3'] for t in self.tanques)
        tabla += f"\n**Volumen total:** {vol_total:.2f} m³\n"
        
        return tabla


# Ejemplo de uso
if __name__ == "__main__":
    from ..maxsurf_connector import MaxsurfConnector
    
    print("=" * 60)
    print("   TANK DESIGNER - TEST")
    print("=" * 60)
    print()
    
    with MaxsurfConnector(visible=True) as maxsurf:
        if maxsurf.is_connected():
            designer = TankDesigner(maxsurf)
            
            # Diseñar tanques para Buque 9
            tanques = designer.diseñar_tanques_buque9(escenario_consumo='realista')
            
            # Mostrar tabla
            print("\n" + designer.generar_tabla_tanques())
            
            # Exportar
            designer.exportar_tanques("../../tablas_datos/tanques_buque9.csv", formato='csv')
            designer.exportar_tanques("../../config/tanques_buque9.json", formato='json')
            
            # Calcular KG
            kg_llenos = designer.calcular_kg_con_tanques('llenos')
            kg_vacios = designer.calcular_kg_con_tanques('vacios')
            print(f"\n📊 KG con tanques llenos: {kg_llenos:.3f} m")
            print(f"📊 KG con tanques vacíos: {kg_vacios:.3f} m")
        else:
            print("❌ No se pudo conectar con Maxsurf")
