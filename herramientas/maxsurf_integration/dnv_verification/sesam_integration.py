from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import sys

try:
    import subprocess
except Exception:  # pragma: no cover
    subprocess = None  # type: ignore


class IntegradorSesam:
    def __init__(self, maxsurf=None):
        self.maxsurf = maxsurf
        self.sesam_available = False

    def exportar_a_sesam(self, geometria_maxsurf: Any, archivo_salida: str | Path) -> str:
        """Stub de exportação a SESAM: gera arquivo marcador.
        Substituir por exportação real (FEM) quando a API/CLI estiver disponível.
        """
        archivo_salida = Path(archivo_salida)
        archivo_salida.parent.mkdir(parents=True, exist_ok=True)
        # Marcador simples
        contenido = "SESAM_EXPORT\nFORMAT FEM\nELEMENTS SHELL\nMATERIAL STEEL\n"
        archivo_salida.write_text(contenido, encoding="utf-8")
        return str(archivo_salida)

    def ejecutar_analisis_sesam(self, archivo_entrada: str | Path) -> Dict[str, Any] | None:
        """Executa análise via SESAM CLI se disponível. Aqui simulamos resultado."""
        if subprocess is None:
            return {"status": "simulado", "ok": True, "mensaje": "SESAM no disponible; simulación."}
        try:
            res = subprocess.run(
                ["sesam", "analizar", str(archivo_entrada), "-normativa", "DNVGL-RU-SHIP-Pt3-Ch5"],
                capture_output=True,
                text=True,
                check=False,
            )
            return {"status": "ejecutado", "returncode": res.returncode, "stdout": res.stdout[:500]}
        except Exception as e:  # pragma: no cover
            print(f"Error ejecutando Sesam: {e}", file=sys.stderr)
            return None


if __name__ == "__main__":
    integ = IntegradorSesam()
    out = integ.exportar_a_sesam(geometria_maxsurf=None, archivo_salida="./salidas/sesam/modelo_sesam.fem")
    print(out)
