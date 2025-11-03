#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict
import subprocess

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠ matplotlib no disponible - gráficos deshabilitados")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠ pandas no disponible - tablas Excel deshabilitadas")


class GeneradorReporteCuaderna:
    
    def __init__(self, dir_salida: str = "ENTREGA 4"):
        self.dir_salida = Path(dir_salida)
        self.dir_salida.mkdir(exist_ok=True)
        
        self.dir_graficos = self.dir_salida / "graficos"
        self.dir_graficos.mkdir(exist_ok=True)
        
        self.dir_tablas = self.dir_salida / "tablas"
        self.dir_tablas.mkdir(exist_ok=True)
        
    def generar_reporte_completo(self):
        print("=" * 80)
        print("GENERADOR DE REPORTE COMPLETO - CUADERNA MAESTRA")
        print("=" * 80)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("1. Ejecutando análisis de plano...")
        resultado_plano = self.ejecutar_analisis_plano()
        
        print("2. Ejecutando verificación DNV...")
        resultado_dnv = self.ejecutar_verificacion_dnv()
        
        print("3. Generando gráficos...")
        self.generar_graficos(resultado_plano, resultado_dnv)
        
        print("4. Generando tablas...")
        self.generar_tablas(resultado_plano, resultado_dnv)
        
        print("5. Generando reporte Markdown...")
        self.generar_reporte_markdown(resultado_plano, resultado_dnv)
        
        print()
        print("=" * 80)
        print("✓ REPORTE COMPLETO GENERADO")
        print("=" * 80)
        print(f"Ubicación: {self.dir_salida}")
        print(f"  - Reporte principal: REPORTE_CUADERNA_MAESTRA.md")
        print(f"  - Gráficos: graficos/")
        print(f"  - Tablas: tablas/")
        print()
    
    def ejecutar_analisis_plano(self) -> Dict:
        try:
            resultado = subprocess.run(
                ['python3', 'herramientas/analizador_plano_cuaderna.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            archivo_json = self.dir_salida / "analisis_plano_cuaderna.json"
            if archivo_json.exists():
                with open(archivo_json, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"  ⚠ Error ejecutando análisis: {e}")
        
        return {}
    
    def ejecutar_verificacion_dnv(self) -> Dict:
        try:
            resultado = subprocess.run(
                ['python3', 'herramientas/verificador_dnv_cuaderna.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            archivo_json = self.dir_salida / "verificacion_dnv_cuaderna.json"
            if archivo_json.exists():
                with open(archivo_json, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"  ⚠ Error ejecutando verificación: {e}")
        
        return {}
    
    def generar_graficos(self, resultado_plano: Dict, resultado_dnv: Dict):
        if not MATPLOTLIB_AVAILABLE:
            print("  ⚠ matplotlib no disponible - saltando gráficos")
            return
        
        self.generar_grafico_capas(resultado_plano)
        self.generar_grafico_cumplimiento_dnv(resultado_dnv)
        self.generar_grafico_geometria(resultado_plano)
        
        print("  ✓ Gráficos generados")
    
    def generar_grafico_capas(self, resultado_plano: Dict):
        if 'capas' not in resultado_plano:
            return
        
        capas = resultado_plano['capas']
        nombres = []
        entidades = []
        
        for nombre, datos in capas.items():
            if datos.get('existe', False):
                nombres.append(nombre.replace('_', '\n'))
                entidades.append(datos.get('entidades', 0))
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(nombres, entidades, color='steelblue', edgecolor='navy', linewidth=1.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Capas', fontsize=12, fontweight='bold')
        ax.set_ylabel('Número de Entidades', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de Entidades por Capa', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.dir_graficos / 'distribucion_capas.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generar_grafico_cumplimiento_dnv(self, resultado_dnv: Dict):
        if 'verificaciones' not in resultado_dnv:
            return
        
        verificaciones = resultado_dnv['verificaciones']
        nombres = []
        cumple = []
        colores = []
        
        for nombre, datos in verificaciones.items():
            nombres.append(nombre.replace('_', '\n'))
            cumple_val = 1 if datos.get('cumple', False) else 0
            cumple.append(cumple_val)
            colores.append('green' if cumple_val else 'red')
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(nombres, cumple, color=colores, edgecolor='black', linewidth=1.5)
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            texto = '✓ CUMPLE' if cumple[i] else '✗ NO CUMPLE'
            ax.text(bar.get_x() + bar.get_width()/2., height/2,
                   texto,
                   ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        ax.set_ylim(0, 1.2)
        ax.set_ylabel('Cumplimiento', fontsize=12, fontweight='bold')
        ax.set_title('Verificación de Cumplimiento Normativo DNV', fontsize=14, fontweight='bold')
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['NO CUMPLE', 'CUMPLE'])
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        cumplimiento_global = resultado_dnv.get('cumplimiento_global', 0)
        ax.text(0.5, 1.1, f'Cumplimiento Global: {cumplimiento_global}%',
               ha='center', transform=ax.transAxes, fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(self.dir_graficos / 'cumplimiento_dnv.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generar_grafico_geometria(self, resultado_plano: Dict):
        if 'geometria' not in resultado_plano:
            return
        
        geometria = resultado_plano['geometria']
        
        tipos = []
        cantidades = []
        for tipo, cantidad in geometria.items():
            if cantidad > 0:
                tipos.append(tipo.replace('_', ' ').title())
                cantidades.append(cantidad)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        colors = plt.cm.Set3(range(len(tipos)))
        wedges, texts, autotexts = ax.pie(cantidades, labels=tipos, autopct='%1.1f%%',
                                           colors=colors, startangle=90,
                                           textprops={'fontsize': 10, 'fontweight': 'bold'})
        
        ax.set_title('Distribución de Tipos de Geometría', fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(self.dir_graficos / 'distribucion_geometria.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generar_tablas(self, resultado_plano: Dict, resultado_dnv: Dict):
        if not PANDAS_AVAILABLE:
            print("  ⚠ pandas no disponible - generando tablas CSV")
            self.generar_tablas_csv(resultado_plano, resultado_dnv)
            return
        
        self.generar_tabla_capas_excel(resultado_plano)
        self.generar_tabla_verificaciones_excel(resultado_dnv)
        
        print("  ✓ Tablas generadas")
    
    def generar_tablas_csv(self, resultado_plano: Dict, resultado_dnv: Dict):
        if 'capas' in resultado_plano:
            with open(self.dir_tablas / 'capas.csv', 'w', encoding='utf-8') as f:
                f.write("Capa,Existe,Entidades\n")
                for nombre, datos in resultado_plano['capas'].items():
                    existe = 'Sí' if datos.get('existe', False) else 'No'
                    entidades = datos.get('entidades', 0)
                    f.write(f"{nombre},{existe},{entidades}\n")
        
        if 'verificaciones' in resultado_dnv:
            with open(self.dir_tablas / 'verificaciones_dnv.csv', 'w', encoding='utf-8') as f:
                f.write("Verificación,Cumple,Normativa\n")
                for nombre, datos in resultado_dnv['verificaciones'].items():
                    cumple = 'Sí' if datos.get('cumple', False) else 'No'
                    normativa = datos.get('normativa', '')
                    f.write(f"{nombre},{cumple},{normativa}\n")
    
    def generar_tabla_capas_excel(self, resultado_plano: Dict):
        if 'capas' not in resultado_plano:
            return
        
        datos = []
        for nombre, info in resultado_plano['capas'].items():
            datos.append({
                'Capa': nombre,
                'Existe': 'Sí' if info.get('existe', False) else 'No',
                'Entidades': info.get('entidades', 0),
                'Tipos': ', '.join(info.get('tipos', []))
            })
        
        df = pd.DataFrame(datos)
        df.to_excel(self.dir_tablas / 'analisis_capas.xlsx', index=False, engine='openpyxl')
    
    def generar_tabla_verificaciones_excel(self, resultado_dnv: Dict):
        if 'verificaciones' not in resultado_dnv:
            return
        
        datos = []
        for nombre, info in resultado_dnv['verificaciones'].items():
            datos.append({
                'Verificación': nombre.replace('_', ' ').title(),
                'Cumple': 'Sí' if info.get('cumple', False) else 'No',
                'Normativa': info.get('normativa', ''),
                'Descripción': info.get('descripcion', '')
            })
        
        df = pd.DataFrame(datos)
        df.to_excel(self.dir_tablas / 'verificaciones_dnv.xlsx', index=False, engine='openpyxl')
    
    def generar_reporte_markdown(self, resultado_plano: Dict, resultado_dnv: Dict):
        contenido = f"""# REPORTE DE ANÁLISIS - CUADERNA MAESTRA
## Buque Grupo 9

**Fecha de análisis:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. RESUMEN EJECUTIVO

### Estado General
- **Análisis de Plano:** {resultado_plano.get('resumen', {}).get('estado', 'N/A')}
- **Verificación DNV:** {resultado_dnv.get('estado', 'N/A')}
- **Cumplimiento Normativo:** {resultado_dnv.get('cumplimiento_global', 0)}%

### Errores y Advertencias
- **Errores detectados:** {resultado_plano.get('resumen', {}).get('total_errores', 0)}
- **Advertencias:** {resultado_plano.get('resumen', {}).get('total_advertencias', 0)}

---

## 2. ANÁLISIS DEL PLANO

### 2.1 Información del Archivo
- **Archivo:** {resultado_plano.get('archivo', 'N/A')}
- **Fecha de análisis:** {resultado_plano.get('fecha_analisis', 'N/A')}

### 2.2 Capas Encontradas

"""
        
        if 'capas' in resultado_plano:
            contenido += "| Capa | Existe | Entidades | Tipos |\n"
            contenido += "|------|--------|-----------|-------|\n"
            for nombre, datos in resultado_plano['capas'].items():
                existe = '✓' if datos.get('existe', False) else '✗'
                entidades = datos.get('entidades', 0)
                tipos = ', '.join(datos.get('tipos', []))
                contenido += f"| {nombre} | {existe} | {entidades} | {tipos} |\n"
        
        contenido += "\n### 2.3 Geometría\n\n"
        
        if 'geometria' in resultado_plano:
            geometria = resultado_plano['geometria']
            contenido += f"- **Líneas:** {geometria.get('lineas', 0)}\n"
            contenido += f"- **Arcos:** {geometria.get('arcos', 0)}\n"
            contenido += f"- **Círculos:** {geometria.get('circulos', 0)}\n"
            contenido += f"- **Polilíneas:** {geometria.get('polilineas', 0)}\n"
            contenido += f"- **Splines:** {geometria.get('splines', 0)}\n"
            contenido += f"- **Textos:** {geometria.get('textos', 0)}\n"
            contenido += f"- **Cotas:** {geometria.get('cotas', 0)}\n"
        
        contenido += "\n### 2.4 Dimensiones\n\n"
        
        if 'dimensiones' in resultado_plano:
            dim = resultado_plano['dimensiones']
            contenido += f"- **Manga estimada:** {dim.get('manga_estimada', 'N/A')} m\n"
            contenido += f"- **Puntal estimado:** {dim.get('puntal_estimado', 'N/A')} m\n"
        
        contenido += "\n![Distribución de Capas](graficos/distribucion_capas.png)\n"
        contenido += "\n![Distribución de Geometría](graficos/distribucion_geometria.png)\n"
        
        contenido += "\n---\n\n## 3. VERIFICACIÓN NORMATIVA DNV\n\n"
        
        if 'verificaciones' in resultado_dnv:
            contenido += "### 3.1 Resultados de Verificación\n\n"
            contenido += "| Verificación | Estado | Normativa |\n"
            contenido += "|--------------|--------|----------|\n"
            
            for nombre, datos in resultado_dnv['verificaciones'].items():
                estado = '✓ CUMPLE' if datos.get('cumple', False) else '✗ NO CUMPLE'
                normativa = datos.get('normativa', '')
                nombre_fmt = nombre.replace('_', ' ').title()
                contenido += f"| {nombre_fmt} | {estado} | {normativa} |\n"
            
            contenido += "\n![Cumplimiento DNV](graficos/cumplimiento_dnv.png)\n"
            
            contenido += "\n### 3.2 Detalles de Verificaciones\n\n"
            
            for nombre, datos in resultado_dnv['verificaciones'].items():
                nombre_fmt = nombre.replace('_', ' ').title()
                contenido += f"#### {nombre_fmt}\n\n"
                contenido += f"- **Normativa:** {datos.get('normativa', 'N/A')}\n"
                contenido += f"- **Descripción:** {datos.get('descripcion', 'N/A')}\n"
                contenido += f"- **Estado:** {'✓ CUMPLE' if datos.get('cumple', False) else '✗ NO CUMPLE'}\n"
                
                if 'valores' in datos:
                    contenido += "\n**Valores:**\n"
                    for clave, valor in datos['valores'].items():
                        if isinstance(valor, dict):
                            contenido += f"\n*{clave.replace('_', ' ').title()}:*\n"
                            for k, v in valor.items():
                                contenido += f"  - {k.replace('_', ' ').title()}: {v}\n"
                        else:
                            contenido += f"- {clave.replace('_', ' ').title()}: {valor}\n"
                
                contenido += "\n"
        
        contenido += """---

## 4. CONCLUSIONES Y RECOMENDACIONES

### 4.1 Conclusiones

"""
        
        if resultado_dnv.get('estado') == 'APROBADO':
            contenido += "✓ La cuaderna maestra cumple con todos los requisitos normativos DNV.\n\n"
        else:
            contenido += "⚠ La cuaderna maestra requiere correcciones para cumplir con la normativa DNV.\n\n"
        
        contenido += "### 4.2 Recomendaciones\n\n"
        
        if resultado_plano.get('advertencias'):
            contenido += "**Advertencias del análisis de plano:**\n"
            for adv in resultado_plano['advertencias']:
                contenido += f"- {adv}\n"
            contenido += "\n"
        
        if resultado_dnv.get('verificaciones'):
            no_cumple = [nombre for nombre, datos in resultado_dnv['verificaciones'].items() 
                        if not datos.get('cumple', False)]
            if no_cumple:
                contenido += "**Verificaciones que no cumplen:**\n"
                for nombre in no_cumple:
                    contenido += f"- {nombre.replace('_', ' ').title()}\n"
                contenido += "\n"
        
        contenido += """---

## 5. ANEXOS

### 5.1 Archivos Generados

- **Análisis de plano:** `analisis_plano_cuaderna.json`
- **Verificación DNV:** `verificacion_dnv_cuaderna.json`
- **Gráficos:** `graficos/`
- **Tablas:** `tablas/`

### 5.2 Referencias Normativas

- DNV Pt.3 Ch.2 Sec.2: Disposición de mamparos estancos
- DNV Pt.3 Ch.2 Sec.3: Doble fondo y doble costado
- DNV Pt.3 Ch.3 Sec.2-3: Dimensionamiento de refuerzos transversales
- DNV Pt.3 Ch.3 Sec.4: Espesores de costados y cubiertas
- DNV Pt.3 Ch.5 Sec.1-2: Casos de carga estructural
- SOLAS II-1 Reg.13: Integridad de mamparos
- SOLAS II-1 Reg.26: Seguridad de maquinaria

---

**Generado automáticamente por el Sistema de Análisis de Cuadernas**
"""
        
        archivo_reporte = self.dir_salida / "REPORTE_CUADERNA_MAESTRA.md"
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"  ✓ Reporte Markdown generado: {archivo_reporte}")


def main():
    generador = GeneradorReporteCuaderna("ENTREGA 4")
    generador.generar_reporte_completo()
    return 0


if __name__ == '__main__':
    exit(main())
