from __future__ import annotations

import pytest

from maxsurf_integration.workflows.windows_bundle import ejecutar_bundle_windows


def test_windows_bundle_requiere_backend_com(tmp_path):
    datos = tmp_path / "datos"
    planos = tmp_path / "planos"
    msd = tmp_path / "modelo.msd"
    archive = tmp_path / "artefactos"

    with pytest.raises(RuntimeError):
        ejecutar_bundle_windows(
            datos_out=datos,
            planos_out=planos,
            msd_out=msd,
            archivador=archive,
            ejecutar_git_lfs=False,
        )
