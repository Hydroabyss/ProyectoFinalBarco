#!/usr/bin/env python3
"""
Módulo de Visualización Interactiva para Análisis de Cuaderna Maestra
Genera gráficos interactivos 3D y mapas de calor usando Plotly
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

from datos_buque_correctos import (
    obtener_datos_buque,
    obtener_dimensiones_cuaderna_maestra,
    obtener_propiedades_material
)


class VisualizadorInteractivoCuaderna:
    """Generador de visualizaciones interactivas 3D para cuaderna maestra."""
    
    def __init__(self):
        self.datos_buque = obtener_datos_buque()
        self.dimensiones = obtener_dimensiones_cuaderna_maestra()
        self.material = obtener_propiedades_material()
        
        self.dir_salida = Path("ENTREGA 4/graficos_interactivos")
        self.dir_salida.mkdir(parents=True, exist_ok=True)

    def modelo_3d_cuaderna(self, guardar_html: bool = True):
        """Genera modelo 3D interactivo de la cuaderna maestra."""

        B = self.dimensiones['manga_total_m']
        D = self.dimensiones['puntal_total_m']
        h_df = self.dimensiones['altura_doble_fondo_m']
        b_dc = self.datos_buque['estructura']['doble_costado']['ancho_m']

        # Definir nodos de la estructura
        nodos = {
            # Fondo exterior
            "Fondo_Izq": (-B/2, 0, 0),
            "Fondo_Der": (B/2, 0, 0),

            # Doble fondo
            "DF_Izq": (-B/2 + b_dc, 0, h_df),
            "DF_Der": (B/2 - b_dc, 0, h_df),
            
            # Costados
            "Costado_Izq_Bajo": (-B/2, 0, h_df),
            "Costado_Izq_Alto": (-B/2, 0, D),
            "Costado_Der_Bajo": (B/2, 0, h_df),
            "Costado_Der_Alto": (B/2, 0, D),
            
            # Cubierta
            "Cubierta_Izq": (-B/2 + b_dc, 0, D),
            "Cubierta_Der": (B/2 - b_dc, 0, D),
        }
        
        # Definir elementos estructurales
        elementos = [
            # Fondo exterior
            ("Forro Fondo", "Fondo_Izq", "Fondo_Der", "navy", 8),
            
            # Costados exteriores
            ("Forro Costado Izq", "Fondo_Izq", "Costado_Izq_Alto", "steelblue", 6),
            ("Forro Costado Der", "Fondo_Der", "Costado_Der_Alto", "steelblue", 6),
            
            # Cubierta
            ("Cubierta Principal", "Cubierta_Izq", "Cubierta_Der", "darkgreen", 5),
            
            # Doble fondo
            ("Fondo Interior Izq", "Fondo_Izq", "DF_Izq", "lightblue", 4),
            ("Fondo Interior Der", "Fondo_Der", "DF_Der", "lightblue", 4),
            ("Tapa DF", "DF_Izq", "DF_Der", "lightblue", 4),
            
            # Doble costado
            ("DC Izq Bajo", "Costado_Izq_Bajo", "DF_Izq", "lightcoral", 4),
            ("DC Izq Alto", "Costado_Izq_Alto", "Cubierta_Izq", "lightcoral", 4),
            ("DC Der Bajo", "Costado_Der_Bajo", "DF_Der", "lightcoral", 4),
            ("DC Der Alto", "Costado_Der_Alto", "Cubierta_Der", "lightcoral", 4),
            
            # Conexiones verticales
            ("Mamparo Izq", "DF_Izq", "Cubierta_Izq", "gray", 3),
            ("Mamparo Der", "DF_Der", "Cubierta_Der", "gray", 3),
        ]
        
        fig = go.Figure()
        
        # Agregar elementos
        for nombre, ini, fin, color, ancho in elementos:
            x = [nodos[ini][0], nodos[fin][0]]
            y = [nodos[ini][1], nodos[fin][1]]
            z = [nodos[ini][2], nodos[fin][2]]
            
            fig.add_trace(go.Scatter3d(
                x=x, y=y, z=z,
                mode='lines+markers',
                marker=dict(size=4, color=color),
                line=dict(color=color, width=ancho),
                name=nombre,
                hovertemplate=f"<b>{nombre}</b><br>" +
                             "X: %{x:.2f} m<br>" +
                             "Y: %{y:.2f} m<br>" +
                             "Z: %{z:.2f} m<br>" +
                             "<extra></extra>"
            ))
        
        # Agregar superficie del fondo
        x_fondo = np.array([nodos["Fondo_Izq"][0], nodos["Fondo_Der"][0]])
        y_fondo = np.array([0, 0])
        z_fondo = np.array([0, 0])
        
        fig.add_trace(go.Mesh3d(
            x=[nodos["Fondo_Izq"][0], nodos["Fondo_Der"][0], 
               nodos["Fondo_Der"][0], nodos["Fondo_Izq"][0]],
            y=[0, 0, 0.5, 0.5],
            z=[0, 0, 0, 0],
            color='lightblue',
            opacity=0.3,
            name='Superficie Fondo',
            showlegend=True
        ))
        
        fig.update_layout(
            title=dict(
                text=f"Modelo 3D Interactivo - Cuaderna Maestra<br>" +
                     f"<sub>Buque Grupo 9 | Lpp={self.datos_buque['dimensiones_principales']['eslora_entre_perpendiculares_m']:.1f}m | " +
                     f"Manga={B:.2f}m | Puntal={D:.2f}m</sub>",
                x=0.5,
                xanchor='center'
            ),
            scene=dict(
                xaxis_title="Manga (Y) [m]",
                yaxis_title="Eslora (X) [m]",
                zaxis_title="Altura (Z) [m]",
                aspectmode='data',
                camera=dict(
                    eye=dict(x=1.5, y=-1.5, z=1.2)
                )
            ),
            height=700,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            hovermode='closest'
        )
        
        if guardar_html:
            archivo_html = self.dir_salida / "modelo_3d_cuaderna.html"
            fig.write_html(str(archivo_html))
            print(f"  ✓ Modelo 3D guardado: {archivo_html}")
        
        return fig

    def mapa_presiones_interactivo(self, presiones: Dict, guardar_html: bool = True):
        """Genera mapa de calor interactivo de presiones."""

        B = self.dimensiones['manga_total_m']
        D = self.dimensiones['puntal_total_m']
        T = self.datos_buque['dimensiones_principales']['calado_diseno_m']

        # Crear malla de puntos
        n_puntos = 50
        y = np.linspace(-B/2, B/2, n_puntos)
        z = np.linspace(0, D, n_puntos)
        Y, Z = np.meshgrid(y, z)

        # Calcular presiones en cada punto
        P = np.zeros_like(Y)

        for i in range(n_puntos):
            for j in range(n_puntos):
                z_punto = Z[i, j]
                y_punto = Y[i, j]
                
                # Presión en el fondo
                if z_punto < 0.1:
                    P[i, j] = presiones['hidrostatica_fondo_kpa']
                
                # Presión en costados (bajo el calado)
                elif z_punto < T and abs(y_punto) > B/2 - 0.5:
                    profundidad = T - z_punto
                    P[i, j] = 1.025 * 9.81 * profundidad / 1000  # kPa
                
                # Presión en cubierta
                elif z_punto > D - 0.1:
                    P[i, j] = presiones['cubierta_kpa']

                # Presión en bodega
                else:
                    P[i, j] = presiones.get('bodega_kpa', 0.05)

        fig = go.Figure(data=go.Contour(
            x=y,
            y=z,
            z=P,
            colorscale='Jet',
            colorbar=dict(
                title=dict(
                    text="Presión [kPa]",
                    side="right"
                )
            ),
            contours=dict(
                showlabels=True,
                labelfont=dict(size=10, color='white')
            ),
            hovertemplate="Manga: %{x:.2f} m<br>" +
                         "Altura: %{y:.2f} m<br>" +
                         "Presión: %{z:.2f} kPa<br>" +
                         "<extra></extra>"
        ))
        
        fig.update_layout(
            title="Mapa de Presiones - Cuaderna Maestra",
            xaxis_title="Manga (Y) [m]",
            yaxis_title="Altura (Z) [m]",
            height=600,
            width=900
        )
        
        if guardar_html:
            archivo_html = self.dir_salida / "mapa_presiones_interactivo.html"
            fig.write_html(str(archivo_html))
            print(f"  ✓ Mapa de presiones guardado: {archivo_html}")
        
        return fig
    
    def mapa_esfuerzos_interactivo(self, esfuerzos: Dict, guardar_html: bool = True):
        """Genera mapa de calor 3D de esfuerzos."""
        
        # Crear datos para el gráfico
        elementos = []
        valores_esfuerzo = []
        colores = []
        factores_seguridad = []
        
        # Forro exterior
        elementos.append("Forro Exterior")
        valores_esfuerzo.append(esfuerzos['esfuerzos_forro']['sigma_von_mises_mpa'])
        factores_seguridad.append(esfuerzos['esfuerzos_forro']['factor_seguridad'])
        colores.append('red' if not esfuerzos['esfuerzos_forro']['cumple'] else 'green')
        
        # Fondo
        elementos.append("Fondo")
        valores_esfuerzo.append(esfuerzos['esfuerzos_fondo']['sigma_mpa'])
        factores_seguridad.append(esfuerzos['esfuerzos_fondo']['factor_seguridad'])
        colores.append('red' if not esfuerzos['esfuerzos_fondo']['cumple'] else 'green')
        
        # Cubierta
        elementos.append("Cubierta")
        valores_esfuerzo.append(esfuerzos['esfuerzos_cubierta']['sigma_mpa'])
        factores_seguridad.append(esfuerzos['esfuerzos_cubierta']['factor_seguridad'])
        colores.append('red' if not esfuerzos['esfuerzos_cubierta']['cumple'] else 'green')
        
        # Crear subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Esfuerzos por Elemento", "Factores de Seguridad"),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Gráfico de esfuerzos
        fig.add_trace(
            go.Bar(
                x=elementos,
                y=valores_esfuerzo,
                marker_color=colores,
                text=[f"{v:.1f} MPa" for v in valores_esfuerzo],
                textposition='outside',
                name="Esfuerzo",
                hovertemplate="<b>%{x}</b><br>" +
                             "Esfuerzo: %{y:.2f} MPa<br>" +
                             "<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Línea de límite elástico
        fig.add_hline(
            y=self.material['limite_elastico_mpa'],
            line_dash="dash",
            line_color="orange",
            annotation_text=f"Límite Elástico ({self.material['limite_elastico_mpa']} MPa)",
            row=1, col=1
        )
        
        # Gráfico de factores de seguridad
        colores_fs = ['green' if fs >= 1.5 else 'red' for fs in factores_seguridad]
        
        fig.add_trace(
            go.Bar(
                x=elementos,
                y=factores_seguridad,
                marker_color=colores_fs,
                text=[f"FS={v:.2f}" for v in factores_seguridad],
                textposition='outside',
                name="Factor Seguridad",
                hovertemplate="<b>%{x}</b><br>" +
                             "FS: %{y:.2f}<br>" +
                             "<extra></extra>"
            ),
            row=1, col=2
        )
        
        # Línea de FS mínimo
        fig.add_hline(
            y=1.5,
            line_dash="dash",
            line_color="red",
            annotation_text="FS Mínimo (1.5)",
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Elemento Estructural", row=1, col=1)
        fig.update_xaxes(title_text="Elemento Estructural", row=1, col=2)
        fig.update_yaxes(title_text="Esfuerzo [MPa]", row=1, col=1)
        fig.update_yaxes(title_text="Factor de Seguridad", row=1, col=2)
        
        fig.update_layout(
            title_text="Análisis de Esfuerzos - Cuaderna Maestra",
            showlegend=False,
            height=500,
            width=1200
        )
        
        if guardar_html:
            archivo_html = self.dir_salida / "mapa_esfuerzos_interactivo.html"
            fig.write_html(str(archivo_html))
            print(f"  ✓ Mapa de esfuerzos guardado: {archivo_html}")
        
        return fig
    
    def dashboard_completo(self, resultados: Dict, guardar_html: bool = True):
        """Genera dashboard interactivo completo con todos los resultados."""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Presiones de Diseño",
                "Esfuerzos Calculados",
                "Factores de Seguridad",
                "Módulo Resistente"
            ),
            specs=[
                [{"type": "bar"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "indicator"}]
            ]
        )
        
        # 1. Presiones
        presiones_nombres = ["Fondo", "Costado", "Cubierta"]
        presiones_valores = [
            resultados['presiones']['hidrostatica_fondo_kpa'],
            resultados['presiones']['hidrostatica_costado_kpa'],
            resultados['presiones']['cubierta_kpa']
        ]
        
        fig.add_trace(
            go.Bar(
                x=presiones_nombres,
                y=presiones_valores,
                marker_color='lightblue',
                text=[f"{v:.1f} kPa" for v in presiones_valores],
                textposition='outside',
                name="Presiones"
            ),
            row=1, col=1
        )
        
        # 2. Esfuerzos
        esfuerzos_nombres = ["Forro", "Fondo", "Cubierta"]
        esfuerzos_valores = [
            resultados['esfuerzos_forro']['sigma_von_mises_mpa'],
            resultados['esfuerzos_fondo']['sigma_mpa'],
            resultados['esfuerzos_cubierta']['sigma_mpa']
        ]
        colores_esfuerzos = [
            'red' if not resultados['esfuerzos_forro']['cumple'] else 'green',
            'red' if not resultados['esfuerzos_fondo']['cumple'] else 'green',
            'red' if not resultados['esfuerzos_cubierta']['cumple'] else 'green'
        ]
        
        fig.add_trace(
            go.Bar(
                x=esfuerzos_nombres,
                y=esfuerzos_valores,
                marker_color=colores_esfuerzos,
                text=[f"{v:.1f} MPa" for v in esfuerzos_valores],
                textposition='outside',
                name="Esfuerzos"
            ),
            row=1, col=2
        )
        
        # 3. Factores de Seguridad
        fs_nombres = ["Forro", "Fondo", "Cubierta"]
        fs_valores = [
            resultados['esfuerzos_forro']['factor_seguridad'],
            resultados['esfuerzos_fondo']['factor_seguridad'],
            resultados['esfuerzos_cubierta']['factor_seguridad']
        ]
        colores_fs = ['green' if fs >= 1.5 else 'red' for fs in fs_valores]
        
        fig.add_trace(
            go.Bar(
                x=fs_nombres,
                y=fs_valores,
                marker_color=colores_fs,
                text=[f"FS={v:.2f}" for v in fs_valores],
                textposition='outside',
                name="FS"
            ),
            row=2, col=1
        )
        
        # 4. Módulo Resistente (Indicador)
        W_calc = resultados['modulo_resistente']['W_calculado_m3']
        W_min = resultados['modulo_resistente']['W_minimo_dnv_m3']
        cumple = resultados['modulo_resistente']['cumple']
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=W_calc,
                title={'text': "Módulo Resistente [m³]"},
                delta={'reference': W_min, 'relative': False},
                gauge={
                    'axis': {'range': [None, W_min * 1.2]},
                    'bar': {'color': "green" if cumple else "red"},
                    'threshold': {
                        'line': {'color': "orange", 'width': 4},
                        'thickness': 0.75,
                        'value': W_min
                    }
                }
            ),
            row=2, col=2
        )
        
        # Actualizar layout
        fig.update_xaxes(title_text="Ubicación", row=1, col=1)
        fig.update_xaxes(title_text="Elemento", row=1, col=2)
        fig.update_xaxes(title_text="Elemento", row=2, col=1)
        
        fig.update_yaxes(title_text="Presión [kPa]", row=1, col=1)
        fig.update_yaxes(title_text="Esfuerzo [MPa]", row=1, col=2)
        fig.update_yaxes(title_text="Factor Seguridad", row=2, col=1)
        
        fig.update_layout(
            title_text=f"Dashboard Análisis Estructural - Cuaderna Maestra<br>" +
                      f"<sub>Buque Grupo 9 | Material: {self.datos_buque['material']['acero']}</sub>",
            showlegend=False,
            height=800,
            width=1400
        )
        
        if guardar_html:
            archivo_html = self.dir_salida / "dashboard_completo.html"
            fig.write_html(str(archivo_html))
            print(f"  ✓ Dashboard completo guardado: {archivo_html}")
        
        return fig
    
    def generar_todas_visualizaciones(self, resultados: Dict = None):
        """Genera todas las visualizaciones interactivas."""
        
        print("=" * 80)
        print("GENERANDO VISUALIZACIONES INTERACTIVAS")
        print("=" * 80)
        
        # 1. Modelo 3D
        print("\n1. Generando modelo 3D interactivo...")
        self.modelo_3d_cuaderna()
        
        # 2. Cargar resultados si no se proporcionan
        if resultados is None:
            archivo_json = Path("ENTREGA 4/analisis_resistencia.json")
            if archivo_json.exists():
                with open(archivo_json, 'r', encoding='utf-8') as f:
                    resultados = json.load(f)
            else:
                print("  ⚠️ No se encontraron resultados. Ejecuta primero el análisis.")
                return
        
        # 3. Mapa de presiones
        print("\n2. Generando mapa de presiones interactivo...")
        self.mapa_presiones_interactivo(resultados['presiones'])
        
        # 4. Mapa de esfuerzos
        print("\n3. Generando mapa de esfuerzos interactivo...")
        self.mapa_esfuerzos_interactivo(resultados)
        
        # 5. Dashboard completo
        print("\n4. Generando dashboard completo...")
        self.dashboard_completo(resultados)
        
        print("\n" + "=" * 80)
        print("✓ VISUALIZACIONES INTERACTIVAS GENERADAS")
        print("=" * 80)
        print(f"\nArchivos guardados en: {self.dir_salida}")
        print("\nPara visualizar:")
        print("  - Abre los archivos .html en tu navegador")
        print("  - Los gráficos son completamente interactivos")
        print("  - Puedes hacer zoom, rotar, y explorar los datos")


def main():
    """Función principal para ejecutar las visualizaciones."""
    visualizador = VisualizadorInteractivoCuaderna()
    visualizador.generar_todas_visualizaciones()


if __name__ == '__main__':
    main()
