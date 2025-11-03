#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.collections import LineCollection
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from datos_buque_correctos import (
    obtener_datos_buque,
    obtener_dimensiones_cuaderna_maestra,
    obtener_propiedades_material,
    obtener_cargas_diseno,
    obtener_espesores_estructura
)


class AnalizadorResistenciaCuaderna:
    
    def __init__(self):
        self.datos_buque = obtener_datos_buque()
        self.dim_cuaderna = obtener_dimensiones_cuaderna_maestra()
        self.material = obtener_propiedades_material()
        self.cargas = obtener_cargas_diseno()
        self.espesores = obtener_espesores_estructura()
        
        self.E = self.material['modulo_young_gpa'] * 1e9
        self.nu = self.material['coeficiente_poisson']
        self.sigma_y = self.material['limite_elastico_mpa']
        
        self.dir_salida = Path("ENTREGA 4")
        self.dir_salida.mkdir(exist_ok=True)
        
        self.resultados = {}
    
    def calcular_presiones(self):
        """Calcula las presiones hidrostáticas y de carga."""
        rho = self.cargas['presion_hidrostatica']['densidad_agua_mar_t_m3'] * 1000
        g = self.cargas['presion_hidrostatica']['gravedad_m_s2']
        T = self.dim_cuaderna['calado_m']
        
        presiones = {
            'hidrostatica_fondo_kpa': rho * g * T / 1000,
            'hidrostatica_costado_kpa': rho * g * T / 2 / 1000,
            'cubierta_kpa': self.cargas['cargas_cubierta']['carga_general_kn_m2'],
            'bodega_kpa': self.cargas['cargas_bodega']['carga_graneles_t_m3'] * 
                         self.cargas['cargas_bodega']['altura_carga_m'] * g / 1000
        }

        self.resultados['presiones'] = presiones
        return presiones

    def calcular_esfuerzos_forro_exterior(self):
        """Calcula los esfuerzos en el forro exterior."""
        B = self.dim_cuaderna['manga_total_m']
        T = self.dim_cuaderna['calado_m']
        t = self.espesores['forro_exterior_mm'] / 1000
        s = self.datos_buque['estructura']['espaciado_cuadernas']['zona_central_mm'] / 1000

        p_hidrostatica = self.resultados['presiones']['hidrostatica_costado_kpa']

        sigma_longitudinal = (p_hidrostatica * 1000 * s) / (2 * t * 1000)

        sigma_transversal = (p_hidrostatica * 1000 * s**2) / (12 * t * 1000)

        sigma_von_mises = np.sqrt(sigma_longitudinal**2 -
                                  sigma_longitudinal * sigma_transversal +
                                  sigma_transversal**2)

        factor_seguridad = self.sigma_y / sigma_von_mises if sigma_von_mises > 0 else 999

        esfuerzos_forro = {
            'sigma_longitudinal_mpa': sigma_longitudinal,
            'sigma_transversal_mpa': sigma_transversal,
            'sigma_von_mises_mpa': sigma_von_mises,
            'sigma_admisible_mpa': self.sigma_y,
            'factor_seguridad': factor_seguridad,
            'cumple': factor_seguridad >= 1.5
        }

        self.resultados['esfuerzos_forro'] = esfuerzos_forro
        return esfuerzos_forro
    
    def calcular_esfuerzos_fondo(self):
        """Calcula los esfuerzos en el fondo."""
        t = self.espesores['forro_fondo_mm'] / 1000
        s = self.datos_buque['estructura']['espaciado_cuadernas']['zona_central_mm'] / 1000
        p = self.resultados['presiones']['hidrostatica_fondo_kpa'] * 1000
        
        sigma = (p * s**2) / (12 * t * 1000)
        
        factor_seguridad = self.sigma_y / sigma
        
        esfuerzos_fondo = {
            'sigma_mpa': sigma,
            'sigma_admisible_mpa': self.sigma_y,
            'factor_seguridad': factor_seguridad,
            'cumple': factor_seguridad >= 1.5
        }
        
        self.resultados['esfuerzos_fondo'] = esfuerzos_fondo
        return esfuerzos_fondo
    
    def calcular_esfuerzos_cubierta(self):
        """Calcula los esfuerzos en la cubierta."""
        t = self.espesores['cubierta_principal_mm'] / 1000
        s = self.datos_buque['estructura']['espaciado_cuadernas']['zona_central_mm'] / 1000
        p = self.resultados['presiones']['cubierta_kpa'] * 1000
        
        sigma = (p * s**2) / (12 * t * 1000)
        
        factor_seguridad = self.sigma_y / sigma
        
        esfuerzos_cubierta = {
            'sigma_mpa': sigma,
            'sigma_admisible_mpa': self.sigma_y,
            'factor_seguridad': factor_seguridad,
            'cumple': factor_seguridad >= 1.5
        }
        
        self.resultados['esfuerzos_cubierta'] = esfuerzos_cubierta
        return esfuerzos_cubierta
    
    def calcular_momento_inercia_seccion(self):
        """Calcula el momento de inercia de la sección transversal."""
        B = self.dim_cuaderna['manga_total_m']
        D = self.dim_cuaderna['puntal_total_m']
        h_df = self.dim_cuaderna['altura_doble_fondo_m']
        b_dc = self.datos_buque['estructura']['doble_costado']['ancho_m']
        
        I_total = (B * D**3) / 12
        
        I_doble_fondo = (B * h_df**3) / 12
        
        I_doble_costado = 2 * ((b_dc * D**3) / 12)
        
        I_efectiva = I_total - I_doble_fondo - I_doble_costado
        
        momento_inercia = {
            'I_total_m4': I_total,
            'I_doble_fondo_m4': I_doble_fondo,
            'I_doble_costado_m4': I_doble_costado,
            'I_efectiva_m4': I_efectiva
        }
        
        self.resultados['momento_inercia'] = momento_inercia
        return momento_inercia
    
    def calcular_modulo_resistente(self):
        """Calcula el módulo resistente de la sección."""
        I = self.resultados['momento_inercia']['I_efectiva_m4']
        D = self.dim_cuaderna['puntal_total_m']
        
        y_max = D / 2
        
        W = I / y_max
        
        L = self.datos_buque['dimensiones_principales']['eslora_entre_perpendiculares_m']
        B = self.dim_cuaderna['manga_total_m']
        Cb = self.datos_buque['coeficientes_forma']['coeficiente_bloque']
        
        W_min_dnv = 0.01 * L**2 * B * (Cb + 0.7)
        
        modulo_resistente = {
            'W_calculado_m3': W,
            'W_minimo_dnv_m3': W_min_dnv,
            'cumple': W >= W_min_dnv,
            'margen_porcentaje': ((W - W_min_dnv) / W_min_dnv) * 100
        }
        
        self.resultados['modulo_resistente'] = modulo_resistente
        return modulo_resistente
    
    def generar_plano_cargas(self):
        """Genera el plano de distribución de cargas."""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        B = self.dim_cuaderna['manga_total_m']
        D = self.dim_cuaderna['puntal_total_m']
        T = self.dim_cuaderna['calado_m']
        h_df = self.dim_cuaderna['altura_doble_fondo_m']
        b_dc = self.datos_buque['estructura']['doble_costado']['ancho_m']
        
        ax.plot([-B/2, B/2], [0, 0], 'k-', linewidth=2, label='Línea base')
        ax.plot([-B/2, B/2], [D, D], 'k-', linewidth=2, label='Cubierta principal')
        ax.plot([-B/2, -B/2], [0, D], 'k-', linewidth=2)
        ax.plot([B/2, B/2], [0, D], 'k-', linewidth=2)
        
        ax.plot([-B/2, B/2], [h_df, h_df], 'b--', linewidth=1.5, label='Techo doble fondo')
        ax.plot([-B/2+b_dc, -B/2+b_dc], [0, D], 'b--', linewidth=1.5, label='Mamparo longitudinal')
        ax.plot([B/2-b_dc, B/2-b_dc], [0, D], 'b--', linewidth=1.5)
        
        ax.plot([-B/2, B/2], [T, T], 'c-', linewidth=2, alpha=0.7, label='Línea de flotación')
        
        p_fondo = self.resultados['presiones']['hidrostatica_fondo_kpa']
        escala_presion = 0.5
        ax.arrow(-B/2, 0, 0, -p_fondo*escala_presion, head_width=0.3, head_length=0.2, 
                fc='red', ec='red', linewidth=2)
        ax.arrow(0, 0, 0, -p_fondo*escala_presion, head_width=0.3, head_length=0.2, 
                fc='red', ec='red', linewidth=2)
        ax.arrow(B/2, 0, 0, -p_fondo*escala_presion, head_width=0.3, head_length=0.2, 
                fc='red', ec='red', linewidth=2)
        ax.text(0, -p_fondo*escala_presion-0.5, f'P = {p_fondo:.1f} kPa', 
               ha='center', fontsize=10, color='red', weight='bold')
        
        p_costado = self.resultados['presiones']['hidrostatica_costado_kpa']
        for y in np.linspace(0, T, 5):
            p_local = p_costado * (T - y) / T * 2
            ax.arrow(-B/2, y, -p_local*escala_presion, 0, head_width=0.2, head_length=0.1, 
                    fc='blue', ec='blue', linewidth=1.5, alpha=0.7)
            ax.arrow(B/2, y, p_local*escala_presion, 0, head_width=0.2, head_length=0.1, 
                    fc='blue', ec='blue', linewidth=1.5, alpha=0.7)
        
        p_cubierta = self.resultados['presiones']['cubierta_kpa']
        for x in np.linspace(-B/2+b_dc, B/2-b_dc, 5):
            ax.arrow(x, D, 0, p_cubierta*escala_presion*0.5, head_width=0.3, head_length=0.2, 
                    fc='green', ec='green', linewidth=1.5, alpha=0.7)
        ax.text(0, D+p_cubierta*escala_presion*0.5+0.3, f'P = {p_cubierta:.1f} kPa', 
               ha='center', fontsize=10, color='green', weight='bold')
        
        ax.set_xlim(-B/2-3, B/2+3)
        ax.set_ylim(-p_fondo*escala_presion-2, D+2)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Manga (m)', fontsize=12, weight='bold')
        ax.set_ylabel('Altura (m)', fontsize=12, weight='bold')
        ax.set_title('PLANO DE CARGAS - CUADERNA MAESTRA\nBuque Grupo 9 (Lpp=105.2m, B=15.99m)', 
                    fontsize=14, weight='bold')
        ax.legend(loc='upper right', fontsize=10)
        
        info_text = f"""DATOS PRINCIPALES:
Manga: {B:.2f} m
Puntal: {D:.2f} m
Calado: {T:.2f} m
Doble fondo: {h_df:.2f} m
Doble costado: {b_dc:.2f} m

PRESIONES:
Fondo: {p_fondo:.1f} kPa
Costado: {p_costado:.1f} kPa
Cubierta: {p_cubierta:.1f} kPa"""
        
        ax.text(B/2+1.5, D/2, info_text, fontsize=9, 
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
               verticalalignment='center')
        
        plt.tight_layout()
        archivo_salida = self.dir_salida / "graficos" / "plano_cargas_cuaderna.png"
        archivo_salida.parent.mkdir(exist_ok=True)
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Plano de cargas generado: {archivo_salida}")
        return str(archivo_salida)
    
    def generar_plano_esfuerzos(self):
        """Genera el plano de distribución de esfuerzos."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        B = self.dim_cuaderna['manga_total_m']
        D = self.dim_cuaderna['puntal_total_m']
        T = self.dim_cuaderna['calado_m']
        h_df = self.dim_cuaderna['altura_doble_fondo_m']
        b_dc = self.datos_buque['estructura']['doble_costado']['ancho_m']
        
        sigma_forro = self.resultados['esfuerzos_forro']['sigma_von_mises_mpa']
        sigma_fondo = self.resultados['esfuerzos_fondo']['sigma_mpa']
        sigma_cubierta = self.resultados['esfuerzos_cubierta']['sigma_mpa']
        sigma_max = max(sigma_forro, sigma_fondo, sigma_cubierta)
        
        ax1.plot([-B/2, B/2, B/2, -B/2, -B/2], [0, 0, D, D, 0], 'k-', linewidth=2)
        ax1.plot([-B/2, B/2], [h_df, h_df], 'k--', linewidth=1)
        ax1.plot([-B/2+b_dc, -B/2+b_dc], [0, D], 'k--', linewidth=1)
        ax1.plot([B/2-b_dc, B/2-b_dc], [0, D], 'k--', linewidth=1)
        ax1.plot([-B/2, B/2], [T, T], 'c-', linewidth=1.5, alpha=0.5)
        
        color_fondo = plt.cm.YlOrRd(sigma_fondo / sigma_max)
        rect_fondo = Rectangle((-B/2, 0), B, h_df, facecolor=color_fondo, 
                              edgecolor='black', linewidth=1.5, alpha=0.7)
        ax1.add_patch(rect_fondo)
        ax1.text(0, h_df/2, f'{sigma_fondo:.1f} MPa', ha='center', va='center', 
                fontsize=10, weight='bold')
        
        color_forro = plt.cm.YlOrRd(sigma_forro / sigma_max)
        rect_forro_izq = Rectangle((-B/2, h_df), b_dc, T-h_df, facecolor=color_forro, 
                                   edgecolor='black', linewidth=1.5, alpha=0.7)
        rect_forro_der = Rectangle((B/2-b_dc, h_df), b_dc, T-h_df, facecolor=color_forro, 
                                   edgecolor='black', linewidth=1.5, alpha=0.7)
        ax1.add_patch(rect_forro_izq)
        ax1.add_patch(rect_forro_der)
        ax1.text(-B/2+b_dc/2, (h_df+T)/2, f'{sigma_forro:.1f} MPa', ha='center', va='center', 
                fontsize=9, weight='bold', rotation=90)
        ax1.text(B/2-b_dc/2, (h_df+T)/2, f'{sigma_forro:.1f} MPa', ha='center', va='center', 
                fontsize=9, weight='bold', rotation=90)
        
        color_cubierta = plt.cm.YlOrRd(sigma_cubierta / sigma_max)
        rect_cubierta = Rectangle((-B/2+b_dc, D-0.2), B-2*b_dc, 0.2, facecolor=color_cubierta, 
                                 edgecolor='black', linewidth=1.5, alpha=0.7)
        ax1.add_patch(rect_cubierta)
        ax1.text(0, D-0.1, f'{sigma_cubierta:.1f} MPa', ha='center', va='center', 
                fontsize=10, weight='bold')
        
        ax1.set_xlim(-B/2-1, B/2+1)
        ax1.set_ylim(-0.5, D+0.5)
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel('Manga (m)', fontsize=12, weight='bold')
        ax1.set_ylabel('Altura (m)', fontsize=12, weight='bold')
        ax1.set_title('DISTRIBUCIÓN DE ESFUERZOS (MPa)', fontsize=12, weight='bold')
        
        sm = plt.cm.ScalarMappable(cmap=plt.cm.YlOrRd, 
                                   norm=plt.Normalize(vmin=0, vmax=sigma_max))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax1, orientation='vertical', pad=0.02)
        cbar.set_label('Esfuerzo (MPa)', fontsize=10, weight='bold')
        
        elementos = ['Forro\nExterior', 'Fondo', 'Cubierta']
        esfuerzos = [sigma_forro, sigma_fondo, sigma_cubierta]
        factores = [
            self.resultados['esfuerzos_forro']['factor_seguridad'],
            self.resultados['esfuerzos_fondo']['factor_seguridad'],
            self.resultados['esfuerzos_cubierta']['factor_seguridad']
        ]
        
        x_pos = np.arange(len(elementos))
        bars = ax2.bar(x_pos, esfuerzos, color=['red', 'orange', 'yellow'], 
                      alpha=0.7, edgecolor='black', linewidth=2)
        
        ax2.axhline(y=self.sigma_y, color='r', linestyle='--', linewidth=2, 
                   label=f'Límite elástico ({self.sigma_y} MPa)')
        ax2.axhline(y=self.sigma_y/1.5, color='g', linestyle='--', linewidth=2, 
                   label=f'Esfuerzo admisible ({self.sigma_y/1.5:.1f} MPa)')
        
        for i, (bar, fs) in enumerate(zip(bars, factores)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{height:.1f} MPa\nFS={fs:.2f}',
                    ha='center', va='bottom', fontsize=10, weight='bold')
        
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(elementos, fontsize=11, weight='bold')
        ax2.set_ylabel('Esfuerzo (MPa)', fontsize=12, weight='bold')
        ax2.set_title('ESFUERZOS POR ELEMENTO', fontsize=12, weight='bold')
        ax2.legend(loc='upper right', fontsize=9)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_ylim(0, max(esfuerzos) * 1.3)
        
        plt.suptitle('ANÁLISIS DE ESFUERZOS - CUADERNA MAESTRA\nBuque Grupo 9 (Lpp=105.2m, B=15.99m)', 
                    fontsize=14, weight='bold', y=0.98)
        
        plt.tight_layout()
        archivo_salida = self.dir_salida / "graficos" / "plano_esfuerzos_cuaderna.png"
        plt.savefig(archivo_salida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  ✓ Plano de esfuerzos generado: {archivo_salida}")
        return str(archivo_salida)
    
    def generar_reporte_resistencia(self):
        """Genera el reporte de análisis de resistencia."""
        contenido = f"""# ANÁLISIS DE RESISTENCIA ESTRUCTURAL
## Cuaderna Maestra - Buque Grupo 9

**Fecha:** {Path(__file__).stat().st_mtime}

---

## 1. DATOS DEL BUQUE

### Dimensiones Principales
- **Eslora entre perpendiculares (Lpp):** {self.datos_buque['dimensiones_principales']['eslora_entre_perpendiculares_m']:.2f} m
- **Manga (B):** {self.dim_cuaderna['manga_total_m']:.2f} m
- **Puntal (D):** {self.dim_cuaderna['puntal_total_m']:.2f} m
- **Calado (T):** {self.dim_cuaderna['calado_m']:.2f} m

### Material: {self.material['acero']}
- **Límite elástico:** {self.sigma_y} MPa
- **Módulo de Young:** {self.material['modulo_young_gpa']} GPa
- **Coeficiente de Poisson:** {self.nu}

---

## 2. PRESIONES DE DISEÑO

| Ubicación | Presión (kPa) |
|-----------|---------------|
| Fondo | {self.resultados['presiones']['hidrostatica_fondo_kpa']:.2f} |
| Costado | {self.resultados['presiones']['hidrostatica_costado_kpa']:.2f} |
| Cubierta | {self.resultados['presiones']['cubierta_kpa']:.2f} |
| Bodega | {self.resultados['presiones']['bodega_kpa']:.2f} |

---

## 3. ESFUERZOS CALCULADOS

### Forro Exterior
- **Esfuerzo longitudinal:** {self.resultados['esfuerzos_forro']['sigma_longitudinal_mpa']:.2f} MPa
- **Esfuerzo transversal:** {self.resultados['esfuerzos_forro']['sigma_transversal_mpa']:.2f} MPa
- **Esfuerzo de Von Mises:** {self.resultados['esfuerzos_forro']['sigma_von_mises_mpa']:.2f} MPa
- **Factor de seguridad:** {self.resultados['esfuerzos_forro']['factor_seguridad']:.2f}
- **Estado:** {'✅ CUMPLE' if self.resultados['esfuerzos_forro']['cumple'] else '❌ NO CUMPLE'}

### Fondo
- **Esfuerzo:** {self.resultados['esfuerzos_fondo']['sigma_mpa']:.2f} MPa
- **Factor de seguridad:** {self.resultados['esfuerzos_fondo']['factor_seguridad']:.2f}
- **Estado:** {'✅ CUMPLE' if self.resultados['esfuerzos_fondo']['cumple'] else '❌ NO CUMPLE'}

### Cubierta Principal
- **Esfuerzo:** {self.resultados['esfuerzos_cubierta']['sigma_mpa']:.2f} MPa
- **Factor de seguridad:** {self.resultados['esfuerzos_cubierta']['factor_seguridad']:.2f}
- **Estado:** {'✅ CUMPLE' if self.resultados['esfuerzos_cubierta']['cumple'] else '❌ NO CUMPLE'}

---

## 4. MÓDULO RESISTENTE

- **Módulo resistente calculado:** {self.resultados['modulo_resistente']['W_calculado_m3']:.3f} m³
- **Módulo resistente mínimo DNV:** {self.resultados['modulo_resistente']['W_minimo_dnv_m3']:.3f} m³
- **Margen:** {self.resultados['modulo_resistente']['margen_porcentaje']:.1f}%
- **Estado:** {'✅ CUMPLE' if self.resultados['modulo_resistente']['cumple'] else '❌ NO CUMPLE'}

---

## 5. CONCLUSIONES

"""
        
        todos_cumplen = (
            self.resultados['esfuerzos_forro']['cumple'] and
            self.resultados['esfuerzos_fondo']['cumple'] and
            self.resultados['esfuerzos_cubierta']['cumple'] and
            self.resultados['modulo_resistente']['cumple']
        )
        
        if todos_cumplen:
            contenido += """### ✅ ESTRUCTURA APROBADA

La cuaderna maestra cumple con todos los requisitos de resistencia estructural según DNV.

**Factores de seguridad:**
- Todos los elementos tienen FS ≥ 1.5
- El módulo resistente supera el mínimo requerido
- Los esfuerzos están dentro de los límites admisibles

"""
        else:
            contenido += """### ⚠️ REQUIERE REVISIÓN

Algunos elementos no cumplen con los requisitos de resistencia.

**Acciones requeridas:**
"""
            if not self.resultados['esfuerzos_forro']['cumple']:
                contenido += "- Aumentar espesor del forro exterior\n"
            if not self.resultados['esfuerzos_fondo']['cumple']:
                contenido += "- Aumentar espesor del fondo\n"
            if not self.resultados['esfuerzos_cubierta']['cumple']:
                contenido += "- Aumentar espesor de la cubierta\n"
            if not self.resultados['modulo_resistente']['cumple']:
                contenido += "- Aumentar el módulo resistente de la sección\n"
        
        contenido += """
---

## 6. PLANOS GENERADOS

- Plano de cargas: `graficos/plano_cargas_cuaderna.png`
- Plano de esfuerzos: `graficos/plano_esfuerzos_cuaderna.png`

---

**Generado automáticamente por el Sistema de Análisis de Resistencia Estructural**
"""
        
        archivo_salida = self.dir_salida / "ANALISIS_RESISTENCIA.md"
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"  ✓ Reporte de resistencia generado: {archivo_salida}")
        return str(archivo_salida)
    
    def ejecutar_analisis_completo(self):
        """Ejecuta el análisis completo de resistencia."""
        print("=" * 80)
        print("ANÁLISIS DE RESISTENCIA ESTRUCTURAL - CUADERNA MAESTRA")
        print("=" * 80)
        print(f"Buque: {self.datos_buque['nombre']}")
        print(f"Lpp: {self.datos_buque['dimensiones_principales']['eslora_entre_perpendiculares_m']:.2f} m")
        print(f"Manga: {self.dim_cuaderna['manga_total_m']:.2f} m")
        print(f"Puntal: {self.dim_cuaderna['puntal_total_m']:.2f} m")
        print()
        
        print("1. Calculando presiones...")
        self.calcular_presiones()
        print("  ✓ Presiones calculadas")
        
        print("2. Calculando esfuerzos en forro exterior...")
        self.calcular_esfuerzos_forro_exterior()
        print("  ✓ Esfuerzos en forro calculados")
        
        print("3. Calculando esfuerzos en fondo...")
        self.calcular_esfuerzos_fondo()
        print("  ✓ Esfuerzos en fondo calculados")
        
        print("4. Calculando esfuerzos en cubierta...")
        self.calcular_esfuerzos_cubierta()
        print("  ✓ Esfuerzos en cubierta calculados")
        
        print("5. Calculando momento de inercia...")
        self.calcular_momento_inercia_seccion()
        print("  ✓ Momento de inercia calculado")
        
        print("6. Calculando módulo resistente...")
        self.calcular_modulo_resistente()
        print("  ✓ Módulo resistente calculado")
        
        print("7. Generando plano de cargas...")
        self.generar_plano_cargas()
        
        print("8. Generando plano de esfuerzos...")
        self.generar_plano_esfuerzos()
        
        print("9. Generando reporte de resistencia...")
        self.generar_reporte_resistencia()

        resultados_json = {}
        for key, value in self.resultados.items():
            if isinstance(value, dict):
                resultados_json[key] = {}
                for k, v in value.items():
                    if isinstance(v, (bool, np.bool_)):
                        resultados_json[key][k] = bool(v)
                    elif isinstance(v, (np.integer, np.floating)):
                        resultados_json[key][k] = float(v)
                    else:
                        resultados_json[key][k] = v
            else:
                resultados_json[key] = value

        archivo_json = self.dir_salida / "analisis_resistencia.json"
        with open(archivo_json, 'w', encoding='utf-8') as f:
            json.dump(resultados_json, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Datos guardados: {archivo_json}")
        print("✓ ANÁLISIS COMPLETO")
        print("=" * 80)


def main():
    analizador = AnalizadorResistenciaCuaderna()
    analizador.ejecutar_analisis_completo()
    return 0


if __name__ == '__main__':
    exit(main())
