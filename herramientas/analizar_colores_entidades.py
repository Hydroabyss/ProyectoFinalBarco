"""
Validación detallada - Verifica colores por entidad
"""
import ezdxf
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DXF_FILE = PROJECT_ROOT / "salidas" / "disposicion_general" / "Plano_Longitudinal_Sala_Maquinas_Detallado.dxf"

doc = ezdxf.readfile(DXF_FILE)
msp = doc.modelspace()

print("=" * 80)
print("   ANÁLISIS DETALLADO DE COLORES POR ENTIDAD")
print("=" * 80)
print()

# Analizar colores de entidades
entity_colors = Counter()
text_entities = []

for entity in msp:
    etype = entity.dxftype()
    layer = entity.dxf.layer
    
    # Obtener color de la entidad
    if hasattr(entity.dxf, 'color'):
        color = entity.dxf.color
    else:
        color = "N/A"
    
    entity_colors[(etype, layer, color)] += 1
    
    if etype == "TEXT":
        text_entities.append({
            'text': entity.dxf.text[:30] if len(entity.dxf.text) > 30 else entity.dxf.text,
            'layer': layer,
            'color': color,
            'pos': (entity.dxf.insert.x, entity.dxf.insert.y)
        })

print("📊 ENTIDADES POR TIPO, CAPA Y COLOR:")
print("-" * 80)
print(f"{'Tipo':<15} {'Capa':<25} {'Color':<10} {'Cantidad':<10}")
print("-" * 80)

for (etype, layer, color), count in sorted(entity_colors.items()):
    color_warning = " ⚠️ " if color in [0, 7, 8, 9, 250, 251, 252, 253, 254, 255, "N/A"] else ""
    print(f"{etype:<15} {layer:<25} {str(color):<10} {count:<10}{color_warning}")

print()
print("📝 PRIMEROS 10 TEXTOS (verificar color):")
print("-" * 80)
for i, txt in enumerate(text_entities[:10], 1):
    color_marker = "⚠️ " if txt['color'] in [0, 7, 8, 9] else "✓ "
    print(f"{color_marker}{i}. '{txt['text']}' | Capa: {txt['layer']} | Color: {txt['color']}")

print()
print("=" * 80)
print(f"✅ Total entidades TEXT analizadas: {len(text_entities)}")
print("=" * 80)
