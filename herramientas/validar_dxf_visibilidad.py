"""
Validador de DXF - Verifica colores y visibilidad
"""
import ezdxf
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DXF_FILE = PROJECT_ROOT / "salidas" / "disposicion_general" / "Plano_Longitudinal_Sala_Maquinas_Detallado.dxf"

print("=" * 80)
print("   VALIDACIÓN DEL PLANO DXF - VERIFICACIÓN DE VISIBILIDAD")
print("=" * 80)
print()

try:
    doc = ezdxf.readfile(DXF_FILE)
    msp = doc.modelspace()
    
    print(f"✓ Archivo leído: {DXF_FILE.name}")
    print(f"✓ Versión DXF: {doc.dxfversion}")
    print()
    
    # Analizar capas
    print("📐 CAPAS Y COLORES:")
    print("-" * 80)
    print(f"{'Capa':<25} {'Color':<10} {'Tipo Línea':<15} {'Entidades':<10}")
    print("-" * 80)
    
    layer_counts = {}
    for entity in msp:
        layer = entity.dxf.layer
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    
    layer_names = [layer.dxf.name for layer in doc.layers]
    for layer_name in sorted(layer_names):
        layer = doc.layers.get(layer_name)
        count = layer_counts.get(layer_name, 0)
        color = layer.dxf.color
        linetype = layer.dxf.linetype
        
        # Advertir sobre colores problemáticos
        warning = ""
        if color in [0, 7, 8, 9, 250, 251, 252, 253, 254, 255]:
            warning = " ⚠️  PUEDE SER INVISIBLE"
        
        print(f"{layer_name:<25} {color:<10} {linetype:<15} {count:<10}{warning}")
    
    print("-" * 80)
    print()
    
    # Resumen de entidades
    print("📊 RESUMEN DE ENTIDADES:")
    print("-" * 80)
    
    entity_types = {}
    for entity in msp:
        etype = entity.dxftype()
        entity_types[etype] = entity_types.get(etype, 0) + 1
    
    total = 0
    for etype, count in sorted(entity_types.items()):
        print(f"  {etype:<20} {count:>5}")
        total += count
    
    print("-" * 80)
    print(f"  {'TOTAL':<20} {total:>5}")
    print()
    
    # Verificar extensión del dibujo
    print("📏 EXTENSIÓN DEL DIBUJO:")
    print("-" * 80)
    
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    
    for entity in msp:
        try:
            if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'start'):
                min_x = min(min_x, entity.dxf.start.x)
                max_x = max(max_x, entity.dxf.start.x)
                min_y = min(min_y, entity.dxf.start.y)
                max_y = max(max_y, entity.dxf.start.y)
                
                if hasattr(entity.dxf, 'end'):
                    min_x = min(min_x, entity.dxf.end.x)
                    max_x = max(max_x, entity.dxf.end.x)
                    min_y = min(min_y, entity.dxf.end.y)
                    max_y = max(max_y, entity.dxf.end.y)
            
            elif hasattr(entity, 'dxf') and hasattr(entity.dxf, 'center'):
                min_x = min(min_x, entity.dxf.center.x - entity.dxf.radius)
                max_x = max(max_x, entity.dxf.center.x + entity.dxf.radius)
                min_y = min(min_y, entity.dxf.center.y - entity.dxf.radius)
                max_y = max(max_y, entity.dxf.center.y + entity.dxf.radius)
        except:
            pass
    
    if min_x != float('inf'):
        print(f"  X: {min_x:.2f} a {max_x:.2f} m  (ancho: {max_x - min_x:.2f} m)")
        print(f"  Y: {min_y:.2f} a {max_y:.2f} m  (alto: {max_y - min_y:.2f} m)")
    else:
        print("  No se pudo calcular extensión")
    
    print()
    print("=" * 80)
    print("✅ VALIDACIÓN COMPLETADA")
    print("=" * 80)
    print()
    print("💡 RECOMENDACIONES:")
    print("  - Abrir en LibreCAD (macOS): brew install --cask librecad")
    print("  - Abrir en QCAD (macOS): brew install --cask qcad")
    print("  - Viewer online: https://sharecad.org")
    print("  - Si los colores 0, 7, 8 no se ven, cambiar fondo a oscuro")
    print()
    
except Exception as e:
    print(f"❌ Error al leer archivo: {e}")
    import traceback
    traceback.print_exc()
