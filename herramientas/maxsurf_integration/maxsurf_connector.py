"""
Maxsurf Connector
================

Conector unificado para Maxsurf con soporte multi-plataforma:
- Windows: API COM (pywin32)
- macOS/Linux: backend mock para desarrollo y pruebas locales

Expone utilidades:
- execute_command / execute
- new_model, open_model, save_model
- set_length, set_beam, set_draft
- run_hydrostatics (aprox. en mock; lectura por COM en Windows)
"""

import sys
import platform
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import math

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


IS_WINDOWS = platform.system().lower().startswith("win")


@dataclass
class _MockMaxsurf:
    """Backend mock con estado mínimo y cálculos aproximados."""
    Visible: bool = True
    _log: List[str] = field(default_factory=list)
    _state: Dict[str, float] = field(default_factory=lambda: {"length": 10.0, "beam": 3.0, "draft": 1.0})
    _cfg: Dict[str, float] = field(default_factory=lambda: {"Cb": 0.55, "Cm": 0.98, "rho": 1.025})

    def ExecuteCommand(self, cmd: str) -> None:
        self._log.append(cmd)
        parts = cmd.strip().split()
        if not parts:
            return
        op = parts[0].upper()
        try:
            if op == "ESLORA" and len(parts) > 1:
                self._state["length"] = float(parts[1])
            elif op == "MANGA" and len(parts) > 1:
                self._state["beam"] = float(parts[1])
            elif op == "CALADO" and len(parts) > 1:
                self._state["draft"] = float(parts[1])
        except Exception:
            pass

    @property
    def ActiveModel(self):  # compat mínima
        return self

    @property
    def Name(self):
        return "MockModel"

    # Métodos auxiliares del mock
    def _hydro(self) -> Dict[str, float]:
        L = float(self._state.get("length", 10.0))
        B = float(self._state.get("beam", 3.0))
        T = float(self._state.get("draft", 1.0))
        Cb = float(self._cfg.get("Cb", 0.55))
        Cm = float(self._cfg.get("Cm", 0.98))
        rho = float(self._cfg.get("rho", 1.025))
        disp_t = rho * L * B * T * Cb
        Cp = Cb / Cm if Cm > 0 else 0.0
        LCB = 0.53 * L
        return {"displacement_t": disp_t, "Cb": Cb, "Cm": Cm, "Cp": Cp, "LCB_m": LCB}

    def get_hydrostatics(self) -> Dict[str, float]:
        return self._hydro()


class MaxsurfConnector:
    """
    Conector principal para Maxsurf API.
    
    Esta clase maneja la conexión con Maxsurf y proporciona
    métodos para ejecutar comandos y obtener datos del modelo.
    
    Attributes:
        app: Objeto de aplicación Maxsurf
        model: Modelo activo de Maxsurf
        connected: Estado de conexión
    """
    
    def __init__(self, visible: bool = True):
        """
        Inicializar el conector de Maxsurf.
        
        Args:
            visible: Si True, muestra la ventana de Maxsurf
        """
        self.app: Optional[Any] = None
        self.model = None
        self.connected = False
        self.visible = visible
        self._is_mock = False

        # Intentar habilitar COM solo en Windows
        self.win32com = None
        if IS_WINDOWS:
            try:
                import win32com.client  # type: ignore
                self.win32com = win32com.client
                logger.info("✅ Módulo win32com disponible (Windows)")
            except Exception:
                logger.warning("⚠️  pywin32 no disponible; se usará modo mock")
    
    def connect(self) -> bool:
        """
        Conectar con la aplicación Maxsurf.
        
        Returns:
            bool: True si la conexión fue exitosa
            
        Raises:
            Exception: Si no se puede conectar con Maxsurf
        """
        logger.info("🔌 Inicializando conexión Maxsurf...")
        # Preferir COM si estamos en Windows y win32com disponible
        if IS_WINDOWS and self.win32com is not None:
            try:
                try:
                    self.app = self.win32com.GetActiveObject("Maxsurf.Application")
                    logger.info("✅ Conectado a instancia existente de Maxsurf")
                except Exception:
                    self.app = self.win32com.Dispatch("Maxsurf.Application")
                    logger.info("✅ Nueva instancia de Maxsurf creada")
                try:
                    self.app.Visible = self.visible
                except Exception:
                    pass
                try:
                    self.model = self.app.ActiveModel
                    if self.model:
                        logger.info(f"📐 Modelo activo: {self.model.Name}")
                except Exception:
                    logger.warning("⚠️  No hay modelo activo")
                self.connected = True
                self._is_mock = False
                logger.info("⚓ Maxsurf (COM) conectado exitosamente")
                return True
            except Exception as e:
                logger.warning(f"⚠️  COM no disponible ({e}); usando modo mock")

        # Fallback: mock en macOS/Linux o si COM falla
        self.app = _MockMaxsurf(Visible=self.visible)
        self.model = self.app  # compat mínima
        self.connected = True
        self._is_mock = True
        logger.info("🧪 Modo mock activo (desarrollo)")
        return True
    
    def disconnect(self):
        """Desconectar de Maxsurf."""
        if self.connected:
            try:
                self.app = None
                self.model = None
                self.connected = False
                logger.info("🔌 Desconectado de Maxsurf")
            except Exception as e:
                logger.error(f"❌ Error al desconectar: {e}")
    
    def execute_command(self, command: str) -> bool:
        """
        Ejecutar un comando en Maxsurf.
        
        Args:
            command: Comando a ejecutar
            
        Returns:
            bool: True si el comando se ejecutó correctamente
        """
        if not self.connected:
            logger.error("❌ No conectado a Maxsurf")
            return False
        
        try:
            logger.debug(f"Ejecutando comando: {command}")
            self.app.ExecuteCommand(command)
            return True
        except Exception as e:
            logger.error(f"❌ Error ejecutando comando '{command}': {e}")
            return False

    # Alias corto
    def execute(self, command: str) -> bool:
        return self.execute_command(command)
    
    def new_model(self, template: str = "Cargo Vessel") -> bool:
        """
        Crear un nuevo modelo desde plantilla.
        
        Args:
            template: Nombre de la plantilla
            
        Returns:
            bool: True si se creó correctamente
        """
        try:
            logger.info(f"📐 Creando nuevo modelo desde plantilla: {template}")
            self.execute_command("NEW")
            
            # Actualizar referencia al modelo
            self.model = self.app.ActiveModel
            
            logger.info("✅ Modelo creado exitosamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error creando modelo: {e}")
            return False
    
    def open_model(self, filepath: str) -> bool:
        """
        Abrir un modelo existente.
        
        Args:
            filepath: Ruta al archivo .msd
            
        Returns:
            bool: True si se abrió correctamente
        """
        try:
            logger.info(f"📂 Abriendo modelo: {filepath}")
            self.execute_command(f'OPEN "{filepath}"')
            self.model = self.app.ActiveModel
            logger.info("✅ Modelo abierto exitosamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error abriendo modelo: {e}")
            return False
    
    def save_model(self, filepath: Optional[str] = None) -> bool:
        """
        Guardar el modelo actual.
        
        Args:
            filepath: Ruta donde guardar (opcional)
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            if filepath:
                logger.info(f"💾 Guardando modelo en: {filepath}")
                self.execute_command(f'SAVEAS "{filepath}"')
            else:
                logger.info("💾 Guardando modelo...")
                self.execute_command("SAVE")
            
            logger.info("✅ Modelo guardado exitosamente")
            return True
        except Exception as e:
            logger.error(f"❌ Error guardando modelo: {e}")
            return False

    # Métodos utilitarios para usar desde otros módulos
    def set_length(self, L: float) -> None:
        self.execute(f"ESLORA {float(L)}")

    def set_beam(self, B: float) -> None:
        self.execute(f"MANGA {float(B)}")

    def set_draft(self, T: float) -> None:
        self.execute(f"CALADO {float(T)}")

    def run_hydrostatics(self) -> Dict[str, float]:
        """Ejecuta hidrostáticas y devuelve coeficientes básicos.
        - Mock: cálculo aproximado
        - COM: lectura de ActiveModel.Hydrostatics si disponible
        """
        try:
            if self._is_mock:
                return self.app.get_hydrostatics()
            # COM
            self.execute("HYDROSTATICS")
            model = getattr(self.app, "ActiveModel", None)
            hydro = getattr(model, "Hydrostatics", None) if model else None
            if hydro is None:
                return {"displacement_t": 0.0, "Cb": 0.0, "Cm": 0.0, "Cp": 0.0, "LCB_m": 0.0}
            disp = float(getattr(hydro, "DisplacementTonnes", 0.0))
            cb = float(getattr(hydro, "BlockCoefficient", 0.0))
            cm = float(getattr(hydro, "MidshipCoefficient", 0.0))
            cp = float(getattr(hydro, "PrismaticCoefficient", 0.0))
            lcb = float(getattr(hydro, "LCB", 0.0))
            return {"displacement_t": disp, "Cb": cb, "Cm": cm, "Cp": cp, "LCB_m": lcb}
        except Exception:
            return {"displacement_t": 0.0, "Cb": 0.0, "Cm": 0.0, "Cp": 0.0, "LCB_m": 0.0}
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtener información del modelo actual.
        
        Returns:
            Dict con información del modelo
        """
        if not self.model:
            logger.warning("⚠️  No hay modelo activo")
            return {}
        
        try:
            info = {
                'nombre': self.model.Name if hasattr(self.model, 'Name') else 'Sin nombre',
                'conectado': self.connected,
                'visible': self.visible
            }
            return info
        except Exception as e:
            logger.error(f"❌ Error obteniendo info del modelo: {e}")
            return {}
    
    def is_connected(self) -> bool:
        """Verificar si está conectado a Maxsurf."""
        return self.connected

    def is_mock_backend(self) -> bool:
        """Indica si el conector está utilizando el backend mock."""
        return self._is_mock
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
    def __repr__(self):
        status = "Conectado" if self.connected else "Desconectado"
        return f"MaxsurfConnector(estado={status}, visible={self.visible})"


# Ejemplo de uso
if __name__ == "__main__":
    print("=" * 60)
    print("   MAXSURF CONNECTOR - TEST")
    print("=" * 60)
    print()
    
    # Usar context manager para conexión automática
    with MaxsurfConnector(visible=True) as maxsurf:
        if maxsurf.is_connected():
            print("✅ Conexión exitosa con Maxsurf")
            
            # Obtener información
            info = maxsurf.get_model_info()
            print(f"\n📊 Información del modelo:")
            for key, value in info.items():
                print(f"  - {key}: {value}")
            
            # Crear nuevo modelo (comentar si no quieres crear uno nuevo)
            # maxsurf.new_model()
            
        else:
            print("❌ No se pudo conectar con Maxsurf")
            print("Verificar que Maxsurf esté instalado")
    
    print("\n🔌 Desconectado de Maxsurf")
