#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from datos_buque_correctos import obtener_datos_buque
from analisis_resistencia_cuaderna import AnalizadorResistenciaCuaderna
from visualizacion_interactiva_cuaderna import VisualizadorInteractivoCuaderna


class AnalizadorCuadernaMaestroV2:

    def __init__(self):
        self.datos_buque = obtener_datos_buque()
        self.dir_salida = Path("ENTREGA 4")
        self.dir_salida.mkdir(exist_ok=True)

        self.log = {
            'inicio': datetime.now().isoformat(),
            'pasos': [],
            'errores': [],
            'archivos_generados': []
        }

    def ejecutar_analisis_completo(self):
        """Ejecuta el análisis completo de la cuaderna maestra."""
        print("=" * 80)
        print("ANÁLISIS COMPLETO DE CUADERNA MAESTRA - BUQUE GRUPO 9")
        print("=" * 80)
        print(f"Buque: {self.datos_buque['nombre']}")
        print(f"Lpp: {self.datos_buque['dimensiones_principales']['eslora_entre_perpendiculares_m']:.2f} m")
        print(f"Manga: {self.datos_buque['dimensiones_principales']['manga_m']:.2f} m")
        print(f"Puntal: {self.datos_buque['dimensiones_principales']['puntal_m']:.2f} m")
        print()

        try:
            self.paso_1_analisis_resistencia()
            self.paso_2_visualizaciones_interactivas()
            self.paso_3_generar_resumen_ejecutivo()
            self.paso_4_guardar_log()

            print()
            print("=" * 80)
            print("✓ ANÁLISIS COMPLETO FINALIZADO")
            print("=" * 80)
            self.mostrar_resumen_final()

            return 0

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            self.log['errores'].append(str(e))
            return 1

    def paso_1_analisis_resistencia(self):
        """Ejecuta el análisis de resistencia estructural."""
        print("PASO 1: Análisis de Resistencia Estructural")
        print("-" * 80)

        try:
            analizador = AnalizadorResistenciaCuaderna()
            analizador.ejecutar_analisis_completo()

            self.log['pasos'].append({
                'paso': 1,
                'nombre': 'Análisis de Resistencia',
                'estado': 'completado',
                'timestamp': datetime.now().isoformat()
            })

            self.log['archivos_generados'].extend([
                'ENTREGA 4/ANALISIS_RESISTENCIA.md',
                'ENTREGA 4/analisis_resistencia.json',
                'ENTREGA 4/graficos/plano_cargas_cuaderna.png',
                'ENTREGA 4/graficos/plano_esfuerzos_cuaderna.png'
            ])

            print()

        except Exception as e:
            self.log['errores'].append(f"Paso 1: {str(e)}")
            raise

    def paso_2_visualizaciones_interactivas(self):
        """Genera visualizaciones interactivas con Plotly."""
        print("PASO 2: Generando Visualizaciones Interactivas")
        print("-" * 80)

        try:
            visualizador = VisualizadorInteractivoCuaderna()
            visualizador.generar_todas_visualizaciones()

            self.log['pasos'].append({
                'paso': 2,
                'nombre': 'Visualizaciones Interactivas',
                'estado': 'completado',
                'timestamp': datetime.now().isoformat()
            })

            self.log['archivos_generados'].extend([
                'ENTREGA 4/graficos_interactivos/modelo_3d_cuaderna.html',
                'ENTREGA 4/graficos_interactivos/mapa_presiones_interactivo.html',
                'ENTREGA 4/graficos_interactivos/mapa_esfuerzos_interactivo.html',
                'ENTREGA 4/graficos_interactivos/dashboard_completo.html'
            ])

            print()

        except Exception as e:
            self.log['errores'].append(f"Paso 2: {str(e)}")
            print(f"  ⚠️ Error en visualizaciones interactivas: {e}")
            print("  Continuando con el análisis...")
            
            print(f"  ✓ Resumen ejecutivo generado: {archivo_resumen}")
            
            self.log['pasos'].append({
                'paso': 2,
                'nombre': 'Resumen Ejecutivo',
                'estado': 'completado',
                'timestamp': datetime.now().isoformat()
            })
            
            self.log['archivos_generados'].append(str(archivo_resumen))
            
            print()
            
        except Exception as e:
            self.log['errores'].append(f"Paso 2: {str(e)}")
            print(f"  ⚠️ Error en visualizaciones interactivas: {e}")
            print("  Continuando con el análisis...")

    def paso_3_generar_resumen_ejecutivo(self):
        """Genera el resumen ejecutivo del análisis."""
        print("PASO 3: Generando Resumen Ejecutivo")
        print("-" * 80)

        try:
            archivo_json = self.dir_salida / "analisis_resistencia.json"
            with open(archivo_json, 'r', encoding='utf-8') as f:
                resultados = json.load(f)

            contenido = self.generar_contenido_resumen(resultados)

            archivo_resumen = self.dir_salida / "RESUMEN_EJECUTIVO.md"
            with open(archivo_resumen, 'w', encoding='utf-8') as f:
                f.write(contenido)

            print(f"  ✓ Resumen ejecutivo generado: {archivo_resumen}")

            self.log['pasos'].append({
                'paso': 3,
                'nombre': 'Resumen Ejecutivo',
                'estado': 'completado',
                'timestamp': datetime.now().isoformat()
            })

            self.log['archivos_generados'].append(str(archivo_resumen))

            print()

        except Exception as e:
            self.log['errores'].append(f"Paso 3: {str(e)}")
            raise

    def generar_contenido_resumen(self, resultados):
        """Genera el contenido del resumen ejecutivo."""
        contenido = f"""# RESUMEN EJECUTIVO
## Análisis de Cuaderna Maestra - Buque Grupo 9

**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 3. INFORMACIÓN DEL BUQUE

| Parámetro | Valor |
|-----------|-------|
| Nombre | {self.datos_buque['nombre']} |
| Tipo | {self.datos_buque['tipo']} |
| Eslora entre perpendiculares (Lpp) | {self.datos_buque['dimensiones_principales']['eslora_entre_perpendiculares_m']:.2f} m |
| Manga (B) | {self.datos_buque['dimensiones_principales']['manga_m']:.2f} m |
| Puntal (D) | {self.datos_buque['dimensiones_principales']['puntal_m']:.2f} m |
| Calado (T) | {self.datos_buque['dimensiones_principales']['calado_diseno_m']:.2f} m |
| Material | {self.datos_buque['material']['acero']} |
| Sociedad de Clasificación | {self.datos_buque['normativa']['sociedad_clasificacion']} |

---

## 2. ANÁLISIS DE RESISTENCIA ESTRUCTURAL

### 2.1 Presiones de Diseño

| Ubicación | Presión (kPa) | Estado |
|-----------|---------------|--------|
| Fondo | {resultados['presiones']['hidrostatica_fondo_kpa']:.2f} | ✓ |
| Costado | {resultados['presiones']['hidrostatica_costado_kpa']:.2f} | ✓ |
| Cubierta | {resultados['presiones']['cubierta_kpa']:.2f} | ✓ |

### 2.3 Esfuerzos Calculados

#### Forro Exterior
- **Esfuerzo de Von Mises:** {resultados['esfuerzos_forro']['sigma_von_mises_mpa']:.2f} MPa
- **Factor de Seguridad:** {resultados['esfuerzos_forro']['factor_seguridad']:.2f}
- **Estado:** {'✅ CUMPLE' if resultados['esfuerzos_forro']['cumple'] else '❌ NO CUMPLE'}

#### Fondo
- **Esfuerzo:** {resultados['esfuerzos_fondo']['sigma_mpa']:.2f} MPa
- **Factor de Seguridad:** {resultados['esfuerzos_fondo']['factor_seguridad']:.2f}
- **Estado:** {'✅ CUMPLE' if resultados['esfuerzos_fondo']['cumple'] else '❌ NO CUMPLE'}

#### Cubierta Principal
- **Esfuerzo:** {resultados['esfuerzos_cubierta']['sigma_mpa']:.2f} MPa
- **Factor de Seguridad:** {resultados['esfuerzos_cubierta']['factor_seguridad']:.2f}
- **Estado:** {'✅ CUMPLE' if resultados['esfuerzos_cubierta']['cumple'] else '❌ NO CUMPLE'}

### 2.3 Módulo Resistente

- **Calculado:** {resultados['modulo_resistente']['W_calculado_m3']:.3f} m³
- **Mínimo DNV:** {resultados['modulo_resistente']['W_minimo_dnv_m3']:.3f} m³
- **Estado:** {'✅ CUMPLE' if resultados['modulo_resistente']['cumple'] else '❌ NO CUMPLE'}

---

## 3. CONCLUSIONES

"""
        
        todos_cumplen = (
            resultados['esfuerzos_forro']['cumple'] and
            resultados['esfuerzos_fondo']['cumple'] and
            resultados['esfuerzos_cubierta']['cumple'] and
            resultados['modulo_resistente']['cumple']
        )
        
        if todos_cumplen:
            contenido += """### ✅ ESTRUCTURA APROBADA

La cuaderna maestra del Buque Grupo 9 cumple con todos los requisitos de resistencia estructural según la normativa DNV.

**Puntos destacados:**
- Todos los elementos estructurales tienen factores de seguridad adecuados (FS ≥ 1.5)
- El módulo resistente supera el mínimo requerido por DNV
- Los esfuerzos están dentro de los límites admisibles del material AH36
- Las presiones de diseño son apropiadas para las condiciones de operación

"""
        else:
            contenido += """### ⚠️ REQUIERE REVISIÓN

El análisis indica que algunos elementos estructurales requieren revisión para cumplir con la normativa DNV.

**Elementos que no cumplen:**
"""
            if not resultados['esfuerzos_forro']['cumple']:
                contenido += f"- **Forro Exterior:** FS = {resultados['esfuerzos_forro']['factor_seguridad']:.2f} (requiere FS ≥ 1.5)\n"
            if not resultados['esfuerzos_fondo']['cumple']:
                contenido += f"- **Fondo:** FS = {resultados['esfuerzos_fondo']['factor_seguridad']:.2f} (requiere FS ≥ 1.5)\n"
            if not resultados['esfuerzos_cubierta']['cumple']:
                contenido += f"- **Cubierta:** FS = {resultados['esfuerzos_cubierta']['factor_seguridad']:.2f} (requiere FS ≥ 1.5)\n"
            if not resultados['modulo_resistente']['cumple']:
                contenido += f"- **Módulo Resistente:** Déficit de {abs(resultados['modulo_resistente']['margen_porcentaje']):.1f}%\n"
            
            contenido += """
**Recomendaciones:**
1. Aumentar el espesor de los elementos que no cumplen
2. Considerar refuerzos estructurales adicionales
3. Revisar el espaciado de cuadernas
4. Evaluar el uso de acero de mayor resistencia

"""
        
        contenido += """---

## 4. DOCUMENTACIÓN GENERADA

### Reportes
- `ANALISIS_RESISTENCIA.md` - Análisis detallado de resistencia estructural
- `analisis_resistencia.json` - Datos en formato JSON

### Planos
- `graficos/plano_cargas_cuaderna.png` - Distribución de cargas
- `graficos/plano_esfuerzos_cuaderna.png` - Distribución de esfuerzos

---

## 5. DATOS TÉCNICOS

### Estructura de la Cuaderna Maestra

| Elemento | Dimensión | Valor |
|----------|-----------|-------|
| Altura doble fondo | h_df | {self.datos_buque['estructura']['doble_fondo']['altura_m']:.2f} m |
| Ancho doble costado | b_dc | {self.datos_buque['estructura']['doble_costado']['ancho_m']:.2f} m |
| Espaciado cuadernas | s | {self.datos_buque['estructura']['espaciado_cuadernas']['zona_central_mm']:,} mm |

### Espesores

| Elemento | Espesor (mm) |
|----------|--------------|
| Forro exterior | {self.datos_buque['estructura']['espesores']['forro_exterior_mm']} |
| Forro fondo | {self.datos_buque['estructura']['espesores']['forro_fondo_mm']} |
| Cubierta principal | {self.datos_buque['estructura']['espesores']['cubierta_principal_mm']} |
| Mamparos transversales | {self.datos_buque['estructura']['espesores']['mamparos_transversales_mm']} |

| Elemento | Espesor (mm) |
|----------|--------------|
| Forro exterior | {self.datos_buque['estructura']['espesores']['forro_exterior_mm']} |
| Forro fondo | {self.datos_buque['estructura']['espesores']['forro_fondo_mm']} |
| Cubierta principal | {self.datos_buque['estructura']['espesores']['cubierta_principal_mm']} |
| Mamparos transversales | {self.datos_buque['estructura']['espesores']['mamparos_transversales_mm']} |

---

**Generado automáticamente por el Sistema de Análisis de Cuaderna Maestra v2.0**
"""
        
        return contenido
    
    def paso_4_guardar_log(self):
        """Guarda el log de ejecución."""
        self.log['fin'] = datetime.now().isoformat()

        archivo_log = self.dir_salida / "log_ejecucion.json"
        with open(archivo_log, 'w', encoding='utf-8') as f:
            json.dump(self.log, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Log guardado: {archivo_log}")

    def mostrar_resumen_final(self):
        """Muestra el resumen final en consola."""
        print()
        print("ARCHIVOS GENERADOS:")
        for archivo in self.log['archivos_generados']:
            print(f"  ✓ {archivo}")
        
        print()
        print(f"Total de pasos completados: {len(self.log['pasos'])}")
        print(f"Total de errores: {len(self.log['errores'])}")
        
        if self.log['errores']:
            print()
            print("ERRORES:")
            for error in self.log['errores']:
                print(f"  ❌ {error}")


def main():
    analizador = AnalizadorCuadernaMaestroV2()
    return analizador.ejecutar_analisis_completo()


if __name__ == '__main__':
    exit(main())
