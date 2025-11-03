#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json

class AnalizadorCuadernaMaestro:
    
    def __init__(self):
        self.dir_entrega = Path("ENTREGA 4")
        self.dir_entrega.mkdir(exist_ok=True)
        
        self.resultados = {
            'fecha_inicio': datetime.now().isoformat(),
            'pasos_completados': [],
            'errores': [],
            'estado': 'EN PROGRESO'
        }
    
    def ejecutar_analisis_completo(self):
        print("=" * 80)
        print("ANÁLISIS COMPLETO DE CUADERNA MAESTRA - BUQUE GRUPO 9")
        print("=" * 80)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Directorio de salida: {self.dir_entrega}")
        print()
        
        pasos = [
            ("Análisis de plano DXF", self.paso_1_analisis_plano),
            ("Verificación normativa DNV", self.paso_2_verificacion_dnv),
            ("Generación de reportes", self.paso_3_generacion_reportes),
            ("Resumen final", self.paso_4_resumen_final)
        ]
        
        for i, (nombre, funcion) in enumerate(pasos, 1):
            print(f"\n{'=' * 80}")
            print(f"PASO {i}/{len(pasos)}: {nombre.upper()}")
            print("=" * 80)
            
            try:
                resultado = funcion()
                self.resultados['pasos_completados'].append({
                    'paso': i,
                    'nombre': nombre,
                    'estado': 'COMPLETADO',
                    'resultado': resultado
                })
                print(f"✓ {nombre} completado")
            except Exception as e:
                error_msg = f"Error en {nombre}: {str(e)}"
                self.resultados['errores'].append(error_msg)
                print(f"✗ {error_msg}")
                self.resultados['estado'] = 'COMPLETADO CON ERRORES'
        
        if not self.resultados['errores']:
            self.resultados['estado'] = 'COMPLETADO EXITOSAMENTE'
        
        self.resultados['fecha_fin'] = datetime.now().isoformat()
        
        self.guardar_log()
        self.mostrar_resumen_final()
    
    def paso_1_analisis_plano(self):
        print("\n📐 Analizando plano de cuaderna maestra...")
        
        resultado = subprocess.run(
            ['python3', 'herramientas/analizador_plano_cuaderna.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if resultado.returncode == 0:
            print("  ✓ Análisis de plano completado")
            
            archivo_json = self.dir_entrega / "analisis_plano_cuaderna.json"
            if archivo_json.exists():
                with open(archivo_json, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    print(f"  - Capas analizadas: {len(datos.get('capas', {}))}")
                    print(f"  - Entidades totales: {sum(c.get('entidades', 0) for c in datos.get('capas', {}).values())}")
                    print(f"  - Errores: {datos.get('resumen', {}).get('total_errores', 0)}")
                    print(f"  - Advertencias: {datos.get('resumen', {}).get('total_advertencias', 0)}")
                    return datos
        else:
            raise Exception(f"Código de salida: {resultado.returncode}")
        
        return {}
    
    def paso_2_verificacion_dnv(self):
        print("\n🔍 Verificando cumplimiento normativo DNV...")
        
        resultado = subprocess.run(
            ['python3', 'herramientas/verificador_dnv_cuaderna.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        archivo_json = self.dir_entrega / "verificacion_dnv_cuaderna.json"
        if archivo_json.exists():
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                print(f"  ✓ Verificación DNV completada")
                print(f"  - Estado: {datos.get('estado', 'N/A')}")
                print(f"  - Cumplimiento global: {datos.get('cumplimiento_global', 0)}%")
                
                verificaciones = datos.get('verificaciones', {})
                cumple = sum(1 for v in verificaciones.values() if v.get('cumple', False))
                total = len(verificaciones)
                print(f"  - Verificaciones aprobadas: {cumple}/{total}")
                
                return datos
        
        return {}
    
    def paso_3_generacion_reportes(self):
        print("\n📊 Generando reportes, gráficos y tablas...")
        
        resultado = subprocess.run(
            ['python3', 'herramientas/generador_reporte_cuaderna.py'],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if resultado.returncode == 0:
            print("  ✓ Reportes generados")
            
            archivos_generados = []
            
            reporte_md = self.dir_entrega / "REPORTE_CUADERNA_MAESTRA.md"
            if reporte_md.exists():
                archivos_generados.append(str(reporte_md))
                print(f"  - Reporte principal: {reporte_md.name}")
            
            dir_graficos = self.dir_entrega / "graficos"
            if dir_graficos.exists():
                graficos = list(dir_graficos.glob("*.png"))
                archivos_generados.extend([str(g) for g in graficos])
                print(f"  - Gráficos generados: {len(graficos)}")
            
            dir_tablas = self.dir_entrega / "tablas"
            if dir_tablas.exists():
                tablas = list(dir_tablas.glob("*.*"))
                archivos_generados.extend([str(t) for t in tablas])
                print(f"  - Tablas generadas: {len(tablas)}")
            
            return {'archivos_generados': archivos_generados}
        else:
            raise Exception(f"Código de salida: {resultado.returncode}")
    
    def paso_4_resumen_final(self):
        print("\n📋 Generando resumen ejecutivo...")
        
        analisis = {}
        verificacion = {}
        
        archivo_analisis = self.dir_entrega / "analisis_plano_cuaderna.json"
        if archivo_analisis.exists():
            with open(archivo_analisis, 'r', encoding='utf-8') as f:
                analisis = json.load(f)
        
        archivo_verificacion = self.dir_entrega / "verificacion_dnv_cuaderna.json"
        if archivo_verificacion.exists():
            with open(archivo_verificacion, 'r', encoding='utf-8') as f:
                verificacion = json.load(f)
        
        resumen = self.generar_resumen_ejecutivo(analisis, verificacion)
        
        archivo_resumen = self.dir_entrega / "RESUMEN_EJECUTIVO.md"
        with open(archivo_resumen, 'w', encoding='utf-8') as f:
            f.write(resumen)
        
        print(f"  ✓ Resumen ejecutivo generado: {archivo_resumen.name}")
        
        return {'archivo': str(archivo_resumen)}
    
    def generar_resumen_ejecutivo(self, analisis: dict, verificacion: dict) -> str:
        contenido = f"""# RESUMEN EJECUTIVO
## Análisis de Cuaderna Maestra - Buque Grupo 9

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. ESTADO GENERAL

"""
        
        estado_plano = analisis.get('resumen', {}).get('estado', 'N/A')
        estado_dnv = verificacion.get('estado', 'N/A')
        cumplimiento = verificacion.get('cumplimiento_global', 0)
        
        if estado_plano == 'APROBADO' and estado_dnv == 'APROBADO':
            contenido += "### ✅ APROBADO\n\n"
            contenido += "La cuaderna maestra cumple con todos los requisitos de diseño y normativa DNV.\n\n"
        elif cumplimiento >= 80:
            contenido += "### ⚠️ APROBADO CON OBSERVACIONES\n\n"
            contenido += "La cuaderna maestra cumple con la mayoría de requisitos, pero requiere correcciones menores.\n\n"
        else:
            contenido += "### ❌ REQUIERE CORRECCIONES\n\n"
            contenido += "La cuaderna maestra no cumple con requisitos críticos y requiere rediseño.\n\n"
        
        contenido += f"""## 2. RESULTADOS PRINCIPALES

### Análisis de Plano
- **Estado:** {estado_plano}
- **Errores detectados:** {analisis.get('resumen', {}).get('total_errores', 0)}
- **Advertencias:** {analisis.get('resumen', {}).get('total_advertencias', 0)}

### Verificación DNV
- **Estado:** {estado_dnv}
- **Cumplimiento global:** {cumplimiento}%

"""
        
        if 'verificaciones' in verificacion:
            contenido += "### Verificaciones Normativas\n\n"
            contenido += "| Verificación | Estado |\n"
            contenido += "|--------------|--------|\n"
            
            for nombre, datos in verificacion['verificaciones'].items():
                estado = '✓ CUMPLE' if datos.get('cumple', False) else '✗ NO CUMPLE'
                nombre_fmt = nombre.replace('_', ' ').title()
                contenido += f"| {nombre_fmt} | {estado} |\n"
        
        contenido += "\n## 3. DIMENSIONES PRINCIPALES\n\n"
        
        if 'dimensiones' in analisis:
            dim = analisis['dimensiones']
            contenido += f"- **Manga estimada:** {dim.get('manga_estimada', 'N/A')} m\n"
            contenido += f"- **Puntal estimado:** {dim.get('puntal_estimado', 'N/A')} m\n"
        
        contenido += "\n## 4. ACCIONES REQUERIDAS\n\n"
        
        if analisis.get('errores'):
            contenido += "### Errores Críticos\n\n"
            for error in analisis['errores']:
                contenido += f"- {error}\n"
            contenido += "\n"
        
        if analisis.get('advertencias'):
            contenido += "### Advertencias\n\n"
            for adv in analisis['advertencias']:
                contenido += f"- {adv}\n"
            contenido += "\n"
        
        if 'verificaciones' in verificacion:
            no_cumple = [nombre for nombre, datos in verificacion['verificaciones'].items() 
                        if not datos.get('cumple', False)]
            if no_cumple:
                contenido += "### Verificaciones que No Cumplen\n\n"
                for nombre in no_cumple:
                    nombre_fmt = nombre.replace('_', ' ').title()
                    datos = verificacion['verificaciones'][nombre]
                    contenido += f"**{nombre_fmt}**\n"
                    contenido += f"- Normativa: {datos.get('normativa', 'N/A')}\n"
                    contenido += f"- Descripción: {datos.get('descripcion', 'N/A')}\n\n"
        
        contenido += """## 5. DOCUMENTACIÓN GENERADA

- **Reporte completo:** `REPORTE_CUADERNA_MAESTRA.md`
- **Análisis de plano:** `analisis_plano_cuaderna.json`
- **Verificación DNV:** `verificacion_dnv_cuaderna.json`
- **Gráficos:** `graficos/`
- **Tablas:** `tablas/`

## 6. PRÓXIMOS PASOS

1. Revisar el reporte completo en `REPORTE_CUADERNA_MAESTRA.md`
2. Analizar los gráficos generados
3. Corregir los errores y advertencias identificados
4. Re-ejecutar el análisis después de las correcciones
5. Validar con Maxsurf (si está disponible)

---

**Generado automáticamente por el Sistema de Análisis de Cuadernas**
"""
        
        return contenido
    
    def guardar_log(self):
        archivo_log = self.dir_entrega / "analisis_log.json"
        with open(archivo_log, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
    
    def mostrar_resumen_final(self):
        print("\n" + "=" * 80)
        print("RESUMEN FINAL DEL ANÁLISIS")
        print("=" * 80)
        print(f"Estado: {self.resultados['estado']}")
        print(f"Pasos completados: {len(self.resultados['pasos_completados'])}")
        print(f"Errores: {len(self.resultados['errores'])}")
        print()
        
        if self.resultados['errores']:
            print("ERRORES:")
            for error in self.resultados['errores']:
                print(f"  ✗ {error}")
            print()
        
        print("ARCHIVOS GENERADOS:")
        print(f"  - {self.dir_entrega}/REPORTE_CUADERNA_MAESTRA.md")
        print(f"  - {self.dir_entrega}/RESUMEN_EJECUTIVO.md")
        print(f"  - {self.dir_entrega}/analisis_plano_cuaderna.json")
        print(f"  - {self.dir_entrega}/verificacion_dnv_cuaderna.json")
        print(f"  - {self.dir_entrega}/graficos/")
        print(f"  - {self.dir_entrega}/tablas/")
        print(f"  - {self.dir_entrega}/analisis_log.json")
        print()
        print("=" * 80)


def main():
    analizador = AnalizadorCuadernaMaestro()
    analizador.ejecutar_analisis_completo()
    return 0


if __name__ == '__main__':
    exit(main())
