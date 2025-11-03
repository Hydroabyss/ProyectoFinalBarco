#!/usr/bin/env python3
"""
Demo Principal - Integración Maxsurf
====================================

Script de demostración completa de todas las capacidades
de integración con Maxsurf para el Buque 9.

Características demostradas:
    1. Conexión con Maxsurf
    2. Creación de casco paramétrico
    3. Análisis hidrostático
    4. Análisis de estabilidad
    5. Diseño de tanques
    6. Generación de reportes

Uso:
    python demo_completo.py
"""

import logging
import sys
from pathlib import Path

# Añadir ruta de herramientas al PATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from maxsurf_integration import (
    MaxsurfConnector,
    HullDesigner,
    StabilityAnalyzer,
    TankDesigner
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Función principal de demostración."""
    
    print("=" * 80)
    print(" DEMO COMPLETA - INTEGRACIÓN MAXSURF PARA BUQUE 9")
    print("=" * 80)
    print()
    
    try:
        # ============================================
        # 1. CONEXIÓN CON MAXSURF
        # ============================================
        print("\n" + "─" * 80)
        print("1️⃣  CONECTANDO CON MAXSURF")
        print("─" * 80)
        
        with MaxsurfConnector(visible=True) as maxsurf:
            if not maxsurf.is_connected():
                logger.error("❌ No se pudo conectar con Maxsurf")
                logger.error("Verificar que Maxsurf esté instalado")
                return 1
            
            print("✅ Conexión exitosa con Maxsurf")
            info = maxsurf.get_model_info()
            print(f"   Información: {info}")
            
            # ============================================
            # 2. DISEÑO DE CASCO
            # ============================================
            print("\n" + "─" * 80)
            print("2️⃣  CREANDO CASCO DEL BUQUE 9")
            print("─" * 80)
            
            hull_designer = HullDesigner(maxsurf)
            
            if hull_designer.crear_casco_buque9():
                params = hull_designer.get_parametros_actuales()
                print("\n📐 Parámetros del casco creado:")
                for key, value in params.items():
                    print(f"   • {key}: {value}")
                
                # Guardar parámetros
                config_path = Path(__file__).parent.parent.parent / "config"
                config_path.mkdir(exist_ok=True)
                hull_designer.guardar_parametros(
                    str(config_path / "buque9_params.json")
                )
                print("\n💾 Parámetros guardados en config/buque9_params.json")
            else:
                logger.error("❌ Error creando casco")
            
            # ============================================
            # 3. ANÁLISIS DE ESTABILIDAD
            # ============================================
            print("\n" + "─" * 80)
            print("3️⃣  ANÁLISIS DE ESTABILIDAD")
            print("─" * 80)
            
            stability_analyzer = StabilityAnalyzer(maxsurf)
            
            print("\n⚓ Ejecutando análisis completo de estabilidad...")
            resultados_estab = stability_analyzer.analisis_completo_buque9()
            
            if resultados_estab:
                # Mostrar resultados clave
                print(f"\n📊 GM (altura metacéntrica): {resultados_estab['GM']:.3f} m")
                
                cumplimiento = resultados_estab['cumplimiento_solas']
                if cumplimiento.get('cumple_solas'):
                    print("✅ CUMPLE CRITERIOS SOLAS")
                else:
                    print("⚠️  REQUIERE CORRECCIONES PARA CUMPLIR SOLAS")
                
                # Generar reporte
                reporte = stability_analyzer.generar_reporte_estabilidad()
                print("\n" + reporte)
                
                # Guardar resultados
                tablas_path = Path(__file__).parent.parent.parent / "tablas_datos"
                stability_analyzer.exportar_resultados(
                    str(tablas_path / "estabilidad_buque9.json")
                )
                print("\n💾 Resultados guardados en tablas_datos/estabilidad_buque9.json")
            else:
                logger.error("❌ Error en análisis de estabilidad")
            
            # ============================================
            # 4. DISEÑO DE TANQUES
            # ============================================
            print("\n" + "─" * 80)
            print("4️⃣  DISEÑO DE TANQUES")
            print("─" * 80)
            
            tank_designer = TankDesigner(maxsurf)
            
            # Diseñar para escenario realista
            print("\n⛽ Diseñando tanques para escenario 'realista' (5 t/día)...")
            tanques = tank_designer.diseñar_tanques_buque9(
                escenario_consumo='realista'
            )
            
            if tanques:
                # Mostrar tabla
                print("\n" + tank_designer.generar_tabla_tanques())
                
                # Calcular KG con diferentes condiciones
                print("\n📊 Análisis de KG:")
                kg_llenos = tank_designer.calcular_kg_con_tanques('llenos')
                kg_50 = tank_designer.calcular_kg_con_tanques('50%')
                kg_vacios = tank_designer.calcular_kg_con_tanques('vacios')
                
                print(f"   • KG con tanques llenos: {kg_llenos:.3f} m")
                print(f"   • KG con tanques 50%:    {kg_50:.3f} m")
                print(f"   • KG con tanques vacíos: {kg_vacios:.3f} m")
                
                # Exportar diseño
                tank_designer.exportar_tanques(
                    str(tablas_path / "tanques_buque9.csv"),
                    formato='csv'
                )
                tank_designer.exportar_tanques(
                    str(config_path / "tanques_buque9.json"),
                    formato='json'
                )
                print("\n💾 Diseño de tanques guardado en:")
                print("   • tablas_datos/tanques_buque9.csv")
                print("   • config/tanques_buque9.json")
            else:
                logger.error("❌ Error diseñando tanques")
            
            # ============================================
            # 5. GUARDAR MODELO
            # ============================================
            print("\n" + "─" * 80)
            print("5️⃣  GUARDANDO MODELO")
            print("─" * 80)
            
            model_path = Path(__file__).parent.parent.parent / "buque9_modelo.msd"
            if maxsurf.save_model(str(model_path)):
                print(f"✅ Modelo guardado en: {model_path.name}")
            
        # Fin del context manager - desconexión automática
        print("\n" + "=" * 80)
        print("✨ DEMO COMPLETA FINALIZADA EXITOSAMENTE")
        print("=" * 80)
        print()
        print("📁 Archivos generados:")
        print("   • config/buque9_params.json")
        print("   • config/tanques_buque9.json")
        print("   • tablas_datos/estabilidad_buque9.json")
        print("   • tablas_datos/tanques_buque9.csv")
        print("   • buque9_modelo.msd")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
        return 130
    
    except Exception as e:
        logger.error(f"❌ Error en demo: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
