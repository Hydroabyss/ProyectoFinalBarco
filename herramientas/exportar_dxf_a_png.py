"""
Exportador de DXF a formato imagen PNG
Para visualizar el plano sin necesidad de visor CAD
"""
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DXF_FILE = PROJECT_ROOT / "salidas" / "disposicion_general" / "Plano_Longitudinal_Sala_Maquinas_Detallado.dxf"
PNG_FILE = PROJECT_ROOT / "salidas" / "disposicion_general" / "Plano_Longitudinal_Sala_Maquinas_Detallado.png"

print("=" * 80)
print("   EXPORTANDO DXF A PNG PARA VISUALIZACIÓN")
print("=" * 80)
print()

try:
    # Leer DXF
    print(f"📖 Leyendo: {DXF_FILE.name}")
    doc = ezdxf.readfile(DXF_FILE)
    msp = doc.modelspace()
    
    # Contar entidades
    total = sum(1 for _ in msp)
    print(f"✓ Total de entidades: {total}")
    
    # Configurar renderizado
    print("🎨 Configurando renderizado...")
    fig = plt.figure(figsize=(24, 10), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    
    # Renderizar
    print("🖼️  Renderizando plano...")
    Frontend(ctx, out).draw_layout(msp, finalize=True)
    
    # Ajustar vista
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Guardar PNG
    print(f"💾 Guardando imagen: {PNG_FILE.name}")
    fig.savefig(PNG_FILE, dpi=150, bbox_inches='tight', pad_inches=0.1, 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print()
    print("=" * 80)
    print("✅ IMAGEN GENERADA EXITOSAMENTE")
    print("=" * 80)
    print()
    print(f"📁 Archivo PNG: {PNG_FILE}")
    print(f"📏 Resolución: 3600x1500 píxeles (aprox)")
    print()
    print("💡 Abrir imagen:")
    print(f"   open '{PNG_FILE}'")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
