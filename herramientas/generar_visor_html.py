"""
Generador de vista HTML/SVG del plano
Crea una página HTML interactiva para visualizar el plano sin visor CAD
"""
import ezdxf
from pathlib import Path
import math

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DXF_FILE = PROJECT_ROOT / "salidas" / "disposicion_general" / "Plano_Longitudinal_Sala_Maquinas_Detallado.dxf"
HTML_FILE = PROJECT_ROOT / "salidas" / "disposicion_general" / "Plano_Longitudinal_Sala_Maquinas_Detallado.html"

# Mapa de colores ACI a RGB
ACI_COLORS = {
    0: '#000000',  # Negro
    1: '#FF0000',  # Rojo
    2: '#FFFF00',  # Amarillo
    3: '#00FF00',  # Verde
    4: '#00FFFF',  # Cyan
    5: '#0000FF',  # Azul
    6: '#FF00FF',  # Magenta
    7: '#FFFFFF',  # Blanco (cambiar a negro para visibilidad)
    8: '#808080',  # Gris
    9: '#C0C0C0',  # Gris claro
    30: '#FF8000', # Naranja
    40: '#80FF80', # Verde claro
    256: '#000000', # Negro ByLayer
}

def aci_to_rgb(color):
    """Convierte color ACI a RGB."""
    if color == 7 or color == 256:
        return '#000000'  # Forzar negro para visibilidad
    return ACI_COLORS.get(color, '#000000')

print("=" * 80)
print("   GENERANDO VISOR HTML DEL PLANO")
print("=" * 80)
print()

doc = ezdxf.readfile(DXF_FILE)
msp = doc.modelspace()

# Calcular extensión
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for entity in msp:
    try:
        if entity.dxftype() == 'LINE':
            min_x = min(min_x, entity.dxf.start.x, entity.dxf.end.x)
            max_x = max(max_x, entity.dxf.start.x, entity.dxf.end.x)
            min_y = min(min_y, entity.dxf.start.y, entity.dxf.end.y)
            max_y = max(max_y, entity.dxf.start.y, entity.dxf.end.y)
        elif entity.dxftype() == 'CIRCLE':
            min_x = min(min_x, entity.dxf.center.x - entity.dxf.radius)
            max_x = max(max_x, entity.dxf.center.x + entity.dxf.radius)
            min_y = min(min_y, entity.dxf.center.y - entity.dxf.radius)
            max_y = max(max_y, entity.dxf.center.y + entity.dxf.radius)
        elif entity.dxftype() == 'LWPOLYLINE':
            for point in entity.get_points():
                min_x = min(min_x, point[0])
                max_x = max(max_x, point[0])
                min_y = min(min_y, point[1])
                max_y = max(max_y, point[1])
    except:
        pass

width = max_x - min_x
height = max_y - min_y
margin = 5

# Escala SVG
svg_width = 1800
svg_height = int(svg_width * height / width) if width > 0 else 600
scale = svg_width / (width + 2 * margin) if width > 0 else 1

print(f"📐 Extensión del plano:")
print(f"   X: {min_x:.2f} a {max_x:.2f} m (ancho: {width:.2f} m)")
print(f"   Y: {min_y:.2f} a {max_y:.2f} m (alto: {height:.2f} m)")
print(f"   Escala SVG: {scale:.2f} píxeles/metro")
print()

def transform_y(y):
    """Invertir Y para coordenadas SVG (origen arriba-izquierda)."""
    return (max_y - y + margin) * scale

def transform_x(x):
    """Transformar X para coordenadas SVG."""
    return (x - min_x + margin) * scale

# Generar SVG
svg_lines = []
svg_lines.append(f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">')
svg_lines.append('<rect width="100%" height="100%" fill="white"/>')

entity_count = 0

# Dibujar entidades
for entity in msp:
    try:
        # Obtener color
        color = entity.dxf.color if hasattr(entity.dxf, 'color') else 256
        stroke = aci_to_rgb(color)
        
        if entity.dxftype() == 'LINE':
            x1, y1 = transform_x(entity.dxf.start.x), transform_y(entity.dxf.start.y)
            x2, y2 = transform_x(entity.dxf.end.x), transform_y(entity.dxf.end.y)
            svg_lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1.5"/>')
            entity_count += 1
            
        elif entity.dxftype() == 'CIRCLE':
            cx, cy = transform_x(entity.dxf.center.x), transform_y(entity.dxf.center.y)
            r = entity.dxf.radius * scale
            svg_lines.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{stroke}" stroke-width="1.5" fill="none"/>')
            entity_count += 1
            
        elif entity.dxftype() == 'LWPOLYLINE':
            points = entity.get_points()
            if len(points) >= 2:
                path = f'M {transform_x(points[0][0])} {transform_y(points[0][1])}'
                for point in points[1:]:
                    path += f' L {transform_x(point[0])} {transform_y(point[1])}'
                if entity.closed:
                    path += ' Z'
                svg_lines.append(f'<path d="{path}" stroke="{stroke}" stroke-width="1.5" fill="none"/>')
                entity_count += 1
                
        elif entity.dxftype() == 'TEXT':
            x, y = transform_x(entity.dxf.insert.x), transform_y(entity.dxf.insert.y)
            text = entity.dxf.text
            height = entity.dxf.height * scale * 0.7  # Factor de escala para texto
            svg_lines.append(f'<text x="{x}" y="{y}" font-size="{height}" fill="{stroke}" font-family="Arial">{text}</text>')
            entity_count += 1
            
    except Exception as e:
        print(f"⚠️  Error procesando {entity.dxftype()}: {e}")
        continue

svg_lines.append('</svg>')

print(f"✓ Procesadas {entity_count} entidades de {sum(1 for _ in msp)} totales")
print()

# Generar HTML
html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plano Longitudinal - Sala de Máquinas</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #f0f0f0;
        }}
        .container {{
            max-width: 1900px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .info {{
            color: #666;
            margin-bottom: 20px;
            padding: 10px;
            background: #f9f9f9;
            border-left: 4px solid #FF0000;
        }}
        .svg-container {{
            border: 1px solid #ddd;
            overflow: auto;
            background: white;
        }}
        svg {{
            display: block;
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .legend h3 {{
            margin-top: 0;
            color: #333;
        }}
        .color-item {{
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }}
        .color-box {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 1px solid #ccc;
            margin-right: 5px;
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚢 Plano Longitudinal Detallado - Sala de Máquinas</h1>
        
        <div class="info">
            <strong>Buque:</strong> Carga General | 
            <strong>LPP:</strong> 105.2 m | 
            <strong>Manga:</strong> 15.99 m | 
            <strong>Puntal:</strong> 7.90 m<br>
            <strong>Extensión:</strong> {width:.1f} m × {height:.1f} m | 
            <strong>Entidades:</strong> {entity_count}
        </div>
        
        <div class="svg-container">
            {''.join(svg_lines)}
        </div>
        
        <div class="legend">
            <h3>Leyenda de Colores</h3>
            <div class="color-item">
                <span class="color-box" style="background: #FF0000;"></span>
                <strong>Rojo:</strong> Casco, Eje, Textos
            </div>
            <div class="color-item">
                <span class="color-box" style="background: #FFFF00;"></span>
                <strong>Amarillo:</strong> Motor, Hélice
            </div>
            <div class="color-item">
                <span class="color-box" style="background: #00FF00;"></span>
                <strong>Verde:</strong> Mamparos, Estructura
            </div>
            <div class="color-item">
                <span class="color-box" style="background: #00FFFF;"></span>
                <strong>Cyan:</strong> Cubiertas
            </div>
            <div class="color-item">
                <span class="color-box" style="background: #0000FF;"></span>
                <strong>Azul:</strong> Bocina, Refuerzos
            </div>
            <div class="color-item">
                <span class="color-box" style="background: #FF00FF;"></span>
                <strong>Magenta:</strong> Generadores, Timón
            </div>
            <div class="color-item">
                <span class="color-box" style="background: #FF8000;"></span>
                <strong>Naranja:</strong> Doble fondo
            </div>
        </div>
        
        <div class="info" style="margin-top: 20px; border-left-color: #00AA00;">
            <strong>✅ Contenido del plano:</strong><br>
            • Sistema de propulsión completo: eje, bocina, chumaceras, hélice 4 palas, timón<br>
            • Doble fondo compartimentado (4 tanques DB-1 a DB-4)<br>
            • Mamparos estancos con refuerzos estructurales<br>
            • Motor MAN 6S50ME-C (8500 kW, 6 cilindros)<br>
            • 3× Generadores CAT 3512C (500 kW c/u)<br>
            • Tanques de servicio diario (FO y LO)<br>
            • Sección transversal de referencia
        </div>
    </div>
</body>
</html>"""

# Guardar HTML
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("=" * 80)
print("✅ VISOR HTML GENERADO EXITOSAMENTE")
print("=" * 80)
print()
print(f"📁 Archivo: {HTML_FILE}")
print(f"📊 Entidades renderizadas: {entity_count}")
print()
print("🌐 Abrir en navegador:")
print(f"   open '{HTML_FILE}'")
print()
