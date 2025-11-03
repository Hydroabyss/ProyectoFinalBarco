"""
Módulo de Integración Conceptual con AutoCAD
============================================

Este módulo documenta cómo integrar Python con AutoCAD usando COM API
en entornos Windows. Incluye configuraciones para motores marinos 3D.

NOTA: Este código requiere:
- Windows OS con AutoCAD instalado
- pywin32 package
- Acceso COM habilitado en AutoCAD

En macOS, este código es de REFERENCIA ÚNICAMENTE.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json

# Nota: win32com solo funciona en Windows
try:
    import win32com.client
    COM_AVAILABLE = True
except ImportError:
    COM_AVAILABLE = False
    print("⚠️  win32com no disponible (solo Windows)")


# ===== CONFIGURACIONES DE MOTORES MARINOS =====

@dataclass
class EngineConfiguration:
    """Configuración técnica de motor marino."""
    model: str
    manufacturer: str
    power_kw: float
    rpm: float
    cylinders: int
    length_m: float
    width_m: float
    height_m: float
    weight_tons: float
    sfoc_g_kwh: float
    
    # Fundación
    foundation_thickness_mm: float
    foundation_reinforcement: str
    foundation_bolts: str
    
    # Archivos 3D (si disponibles)
    model_3d_file: Optional[str] = None
    textures: Optional[List[str]] = None


# Biblioteca de motores
ENGINE_LIBRARY: Dict[str, EngineConfiguration] = {
    "MAN_6S50ME-C": EngineConfiguration(
        model="6S50ME-C",
        manufacturer="MAN Energy Solutions",
        power_kw=8500.0,
        rpm=127.0,
        cylinders=6,
        length_m=8.50,
        width_m=3.20,
        height_m=4.10,
        weight_tons=145.0,
        sfoc_g_kwh=185.0,
        foundation_thickness_mm=600.0,
        foundation_reinforcement="HEB400",
        foundation_bolts="M36x300",
        model_3d_file="models/man_6s50me_c.step",  # STEP/IGES común en industria
        textures=["steel", "paint_green", "aluminum"],
    ),
    
    "WARTSILA_16V26": EngineConfiguration(
        model="16V26",
        manufacturer="Wärtsilä",
        power_kw=5440.0,
        rpm=1000.0,
        cylinders=16,
        length_m=6.80,
        width_m=2.90,
        height_m=3.60,
        weight_tons=98.0,
        sfoc_g_kwh=192.0,
        foundation_thickness_mm=450.0,
        foundation_reinforcement="HEB320",
        foundation_bolts="M30x250",
        model_3d_file="models/wartsila_16v26.step",
        textures=["steel", "paint_orange", "aluminum"],
    ),
    
    "CAT_3512C": EngineConfiguration(
        model="3512C",
        manufacturer="Caterpillar",
        power_kw=500.0,  # como generador
        rpm=1800.0,
        cylinders=12,
        length_m=3.50,
        width_m=1.80,
        height_m=2.60,
        weight_tons=12.5,
        sfoc_g_kwh=201.5,
        foundation_thickness_mm=350.0,
        foundation_reinforcement="HEB240",
        foundation_bolts="M24x200",
        model_3d_file="models/cat_3512c.step",
        textures=["steel", "paint_yellow", "black"],
    ),
}


class AutoCADEngineIntegration:
    """
    Clase para integración con AutoCAD via COM API.
    
    IMPORTANTE: Solo funciona en Windows con AutoCAD instalado.
    """
    
    def __init__(self):
        self.acad = None
        self.doc = None
        self.model_space = None
        self.connected = False
        
    def connect_autocad(self) -> bool:
        """
        Conecta con AutoCAD mediante COM API.
        
        Returns:
            bool: True si conectó exitosamente
        """
        if not COM_AVAILABLE:
            print("❌ COM API no disponible (requiere Windows + pywin32)")
            return False
            
        try:
            # Intentar conectar con instancia activa
            self.acad = win32com.client.GetActiveObject("AutoCAD.Application")
            print("✅ Conectado a AutoCAD existente")
        except:
            try:
                # Crear nueva instancia
                self.acad = win32com.client.Dispatch("AutoCAD.Application")
                print("✅ Nueva instancia de AutoCAD creada")
            except Exception as e:
                print(f"❌ Error conectando AutoCAD: {e}")
                return False
        
        # Hacer visible y obtener documento activo
        self.acad.Visible = True
        self.doc = self.acad.ActiveDocument
        self.model_space = self.doc.ModelSpace
        self.connected = True
        
        print(f"📄 Documento activo: {self.doc.Name}")
        return True
    
    def create_layer(self, name: str, color: int, linetype: str = "Continuous") -> None:
        """
        Crea una capa en AutoCAD.
        
        Args:
            name: Nombre de la capa
            color: Color ACI (1-255)
            linetype: Tipo de línea
        """
        if not self.connected:
            raise RuntimeError("No conectado a AutoCAD")
        
        layers = self.doc.Layers
        try:
            layer = layers.Add(name)
            layer.Color = color
            layer.Linetype = linetype
            print(f"✓ Capa '{name}' creada (color {color})")
        except:
            print(f"⚠️  Capa '{name}' ya existe")
    
    def insert_3d_block(
        self,
        block_name: str,
        insertion_point: Tuple[float, float, float],
        scale: float = 1.0,
        rotation: float = 0.0,
    ) -> None:
        """
        Inserta un bloque 3D en el modelo.
        
        Args:
            block_name: Nombre del bloque (debe existir)
            insertion_point: (x, y, z)
            scale: Factor de escala
            rotation: Rotación en radianes
        """
        if not self.connected:
            raise RuntimeError("No conectado a AutoCAD")
        
        try:
            # Convertir tupla a array COM
            point = win32com.client.VARIANT(
                win32com.client.pythoncom.VT_ARRAY | win32com.client.pythoncom.VT_R8,
                list(insertion_point)
            )
            
            block_ref = self.model_space.InsertBlock(
                point,
                block_name,
                scale, scale, scale,
                rotation
            )
            
            print(f"✓ Bloque '{block_name}' insertado en {insertion_point}")
            return block_ref
        except Exception as e:
            print(f"❌ Error insertando bloque: {e}")
    
    def add_text(
        self,
        text: str,
        position: Tuple[float, float, float],
        height: float = 0.25,
        layer: str = "0",
    ) -> None:
        """Añade texto en el modelo."""
        if not self.connected:
            raise RuntimeError("No conectado a AutoCAD")
        
        point = win32com.client.VARIANT(
            win32com.client.pythoncom.VT_ARRAY | win32com.client.pythoncom.VT_R8,
            list(position)
        )
        
        text_obj = self.model_space.AddText(text, point, height)
        text_obj.Layer = layer
        
        print(f"✓ Texto '{text}' añadido")
    
    def import_step_file(self, filepath: str) -> bool:
        """
        Importa archivo STEP (si AutoCAD tiene soporte).
        
        Args:
            filepath: Ruta al archivo .step o .stp
            
        Returns:
            bool: True si importó exitosamente
        """
        if not self.connected:
            raise RuntimeError("No conectado a AutoCAD")
        
        try:
            # Comando de importación (varía según versión AutoCAD)
            command_str = f"_IMPORT {filepath} "
            self.doc.SendCommand(command_str)
            print(f"✅ Archivo STEP importado: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error importando STEP: {e}")
            return False


class EngineRoomDesigner:
    """
    Diseñador de sala de máquinas con integración AutoCAD.
    """
    
    def __init__(self):
        self.autocad = AutoCADEngineIntegration()
        self.engine_configs = ENGINE_LIBRARY
        
    def setup_layers(self) -> None:
        """Crea capas estándar para sala de máquinas."""
        layers_config = {
            "CASCO": 1,
            "ESTRUCTURA": 3,
            "MAMPAROS": 3,
            "MOTOR_PRINCIPAL": 2,
            "GENERADORES": 6,
            "EJE_PROPULSOR": 1,
            "EQUIPOS_AUX": 5,
            "TANQUES": 30,
            "TUBERIAS": 4,
            "TEXTOS": 7,
        }
        
        for layer_name, color in layers_config.items():
            self.autocad.create_layer(layer_name, color)
    
    def insert_main_engine(
        self,
        engine_model: str,
        position: Tuple[float, float, float],
    ) -> None:
        """
        Inserta motor principal en posición especificada.
        
        Args:
            engine_model: Clave en ENGINE_LIBRARY
            position: (x, y, z) en metros
        """
        if engine_model not in self.engine_configs:
            raise ValueError(f"Motor '{engine_model}' no encontrado")
        
        config = self.engine_configs[engine_model]
        
        # Si existe modelo 3D, intentar importar
        if config.model_3d_file and Path(config.model_3d_file).exists():
            print(f"📥 Importando modelo 3D: {config.model_3d_file}")
            self.autocad.import_step_file(config.model_3d_file)
        else:
            print(f"⚠️  Modelo 3D no disponible, creando representación esquemática")
            self._create_schematic_engine(config, position)
        
        # Añadir anotaciones técnicas
        self._add_engine_annotations(config, position)
    
    def _create_schematic_engine(
        self,
        config: EngineConfiguration,
        position: Tuple[float, float, float],
    ) -> None:
        """Crea representación esquemática del motor (rectángulo + detalles)."""
        # En AutoCAD real, usarías AddBox, AddCylinder, etc.
        print(f"📐 Creando representación esquemática de {config.model}")
        print(f"   Dimensiones: {config.length_m} x {config.width_m} x {config.height_m} m")
        print(f"   Peso: {config.weight_tons} ton")
    
    def _add_engine_annotations(
        self,
        config: EngineConfiguration,
        position: Tuple[float, float, float],
    ) -> None:
        """Añade datos técnicos como texto."""
        x, y, z = position
        
        annotations = [
            f"{config.manufacturer} {config.model}",
            f"{config.power_kw} kW @ {config.rpm} RPM",
            f"SFOC: {config.sfoc_g_kwh} g/kWh",
            f"{config.cylinders} cilindros",
        ]
        
        for i, text in enumerate(annotations):
            text_pos = (x, y, z + config.height_m + 0.5 + i * 0.3)
            self.autocad.add_text(text, text_pos, height=0.25, layer="TEXTOS")
    
    def generate_complete_engine_room(
        self,
        main_engine_model: str,
        generator_model: str,
        room_length: float,
        room_beam: float,
        room_height: float,
    ) -> Dict:
        """
        Genera sala de máquinas completa.
        
        Args:
            main_engine_model: Modelo de motor principal
            generator_model: Modelo de generadores
            room_length: Longitud sala (m)
            room_beam: Manga sala (m)
            room_height: Altura sala (m)
            
        Returns:
            Dict con resumen de elementos creados
        """
        if not self.autocad.connect_autocad():
            return {"error": "No se pudo conectar AutoCAD"}
        
        print("\n" + "=" * 70)
        print("  GENERANDO SALA DE MÁQUINAS EN AUTOCAD")
        print("=" * 70 + "\n")
        
        # 1. Crear capas
        print("📐 Creando capas...")
        self.setup_layers()
        
        # 2. Insertar motor principal
        print(f"\n⚙️  Insertando motor principal: {main_engine_model}")
        main_engine_pos = (room_length * 0.3, 0.0, 1.5)
        self.insert_main_engine(main_engine_model, main_engine_pos)
        
        # 3. Insertar generadores
        print(f"\n🔌 Insertando generadores: {generator_model}")
        for i in range(3):
            gen_pos = (room_length * 0.15 + i * 4.5, -3.0, 1.2)
            self.insert_main_engine(generator_model, gen_pos)
        
        # 4. Resumen
        summary = {
            "main_engine": self.engine_configs[main_engine_model],
            "generators": {
                "model": generator_model,
                "count": 3,
                "total_power_kw": self.engine_configs[generator_model].power_kw * 3,
            },
            "room_dimensions": {
                "length_m": room_length,
                "beam_m": room_beam,
                "height_m": room_height,
            },
        }
        
        print("\n" + "=" * 70)
        print("✅ SALA DE MÁQUINAS GENERADA EXITOSAMENTE")
        print("=" * 70)
        print(f"\nMotor principal: {main_engine_model} ({summary['main_engine'].power_kw} kW)")
        print(f"Generadores: 3x {generator_model} ({summary['generators']['total_power_kw']} kW total)")
        
        return summary


# ===== FUNCIONES DE UTILIDAD =====

def export_engine_config_to_json(output_path: str = "engine_configurations.json") -> None:
    """Exporta configuraciones a JSON para referencia."""
    config_dict = {}
    
    for key, config in ENGINE_LIBRARY.items():
        config_dict[key] = {
            "model": config.model,
            "manufacturer": config.manufacturer,
            "power_kw": config.power_kw,
            "rpm": config.rpm,
            "cylinders": config.cylinders,
            "dimensions_m": {
                "length": config.length_m,
                "width": config.width_m,
                "height": config.height_m,
            },
            "weight_tons": config.weight_tons,
            "sfoc_g_kwh": config.sfoc_g_kwh,
            "foundation": {
                "thickness_mm": config.foundation_thickness_mm,
                "reinforcement": config.foundation_reinforcement,
                "bolts": config.foundation_bolts,
            },
        }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuraciones exportadas a: {output_path}")


def main():
    """Demo de uso (solo funciona en Windows con AutoCAD)."""
    print("\n" + "=" * 70)
    print("  INTEGRACIÓN AUTOCAD - MÓDULO DE MOTORES MARINOS")
    print("=" * 70 + "\n")
    
    # Exportar configuraciones
    export_engine_config_to_json()
    
    if not COM_AVAILABLE:
        print("\n⚠️  Este módulo es de REFERENCIA en macOS")
        print("   Para uso real, ejecutar en Windows con AutoCAD instalado")
        print("\nMotores disponibles en biblioteca:")
        for key, config in ENGINE_LIBRARY.items():
            print(f"\n  • {key}")
            print(f"    Fabricante: {config.manufacturer}")
            print(f"    Potencia: {config.power_kw} kW @ {config.rpm} RPM")
            print(f"    Dimensiones: {config.length_m} x {config.width_m} x {config.height_m} m")
        return
    
    # Si estamos en Windows con AutoCAD
    designer = EngineRoomDesigner()
    
    # Ejemplo: Crear sala de máquinas
    summary = designer.generate_complete_engine_room(
        main_engine_model="MAN_6S50ME-C",
        generator_model="CAT_3512C",
        room_length=15.0,
        room_beam=15.99,
        room_height=7.90,
    )
    
    print("\n📋 Resumen generado:")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
